Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	Samplers =
	{
		Scene =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		LastLuminance =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}


VertexStruct VS_INPUT
{
    int2 position	: POSITION;
};

VertexStruct VS_OUTPUT_DOWNSAMPLE
{
    float4 position			: PDX_POSITION;
	float2 uv				: TEXCOORD0;
};


ConstantBuffer( 2, 39 )
{
	float4 InvLuminanceSize;
	float4 UVScale;
	float2 Dummy;
};

ConstantBuffer( 2, 39 )
{
	float4 InvSize_TauDeltaTime;
	float4 GatherSize_PixelSize;
	float2 MinHdr_MaxHdr;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT_DOWNSAMPLE main( const VS_INPUT VertexIn )
		{
			VS_OUTPUT_DOWNSAMPLE VertexOut;
			VertexOut.position = float4( VertexIn.position, 0.0f, 1.0f );
			
			VertexOut.uv = float2(VertexIn.position.x, FIX_FLIPPED_UV(VertexIn.position.y)) * 0.5 + 0.5;
			VertexOut.uv.y = 1.0f - VertexOut.uv.y;
			VertexOut.uv *= UVScale.xy;
			
		#ifdef PDX_DIRECTX_9 // Half pixel offset
			VertexOut.position.xy += float2( -InvLuminanceSize.x, InvLuminanceSize.y );
		#endif
		
			return VertexOut;
		}
	]]
}

PixelShader =
{
	MainCode PixelShaderDownsample
	[[
		float4 main( VS_OUTPUT_DOWNSAMPLE Input ) : PDX_COLOR
		{
		#ifdef LUMINANCE_SAMPLE_ALPHA
			float vLogLuminance = tex2Dlod0( Scene, Input.uv ).a;
		#else
			float vLogLuminance = tex2Dlod0( Scene, Input.uv ).r;
		#endif
		
			return float4( vLogLuminance, 0.0, 0.0, 1.0 );
		}
	]]

	MainCode PixelShaderGather
	[[
		float CalculateAdaptedLuminance(float vCurrentLuminance)
		{
			float vLastLuminance = tex2Dlod0(LastLuminance, vec2(0.5)).r; 
			float vAdaptedLum = vLastLuminance + (vCurrentLuminance - vLastLuminance) * (1.0 - exp(-InvSize_TauDeltaTime.z)); 
		
			return vAdaptedLum; 
		}
		
		float4 main( VS_OUTPUT_DOWNSAMPLE Input ) : PDX_COLOR
		{
			float2 baseOffset = GatherSize_PixelSize.zw * 0.5;
			
			float vSum = 0.0;
			float v = baseOffset.y;
			for (int y = 0; y < GatherSize_PixelSize.y; ++y)
			{
				float u = baseOffset.x;
				for (int x = 0; x < GatherSize_PixelSize.x; ++x)
				{
					vSum += tex2Dlod0( Scene, float2(u, v) ).r;
					
					u += GatherSize_PixelSize.z;
				}
				
				v += GatherSize_PixelSize.w;
			}
			
			vSum /= GatherSize_PixelSize.x * GatherSize_PixelSize.y;
			
			float vCurrentLuminance = clamp(exp(vSum), MinHdr_MaxHdr.x, MinHdr_MaxHdr.y);
			return float4( CalculateAdaptedLuminance(vCurrentLuminance), 0.0, 0.0, 1.0 );
		}
	]]
}


BlendState BlendState
{
	BlendEnable = no
}


Effect LuminanceDownsample
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderDownsample"
}

Effect LuminanceGather
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderGather"
}

