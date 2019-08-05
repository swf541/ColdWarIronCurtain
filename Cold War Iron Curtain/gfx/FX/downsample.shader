Includes = {
	"posteffect_base.fxh"
	"constants.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	Samplers =
	{
		MainScene =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
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
			
		#ifdef PDX_DIRECTX_9 // Half pixel offset
			VertexOut.position.xy += float2( -InvDownSampleSize.x, InvDownSampleSize.y );
		#endif
		
			return VertexOut;
		}
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT_DOWNSAMPLE Input ) : PDX_COLOR
		{
			float4 vColor = tex2Dlod0( MainScene, Input.uv );
			//float vMax = saturate( max( max( vColor.r, vColor.g ), vColor.b ) - BrightThreshold );
			float vMax = max(0, max( max( vColor.r, vColor.g ), vColor.b ) - BrightThreshold );
			vMax /= (0.5 + vMax);
			vMax += vColor.a * EmissiveBloomStrength;
		
			float logLuminance = log(max(0.0, dot(vColor.rgb, LUMINANCE_VECTOR)) + 0.0001f);
			
			return float4( vColor.rgb * vMax, logLuminance );
		}
	]]
}


BlendState BlendState
{
	BlendEnable = no
}


Effect downsample
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

