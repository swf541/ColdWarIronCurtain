Includes = {
}

PixelShader =
{
	Samplers =
	{
		BaseLUT1 =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		BaseLUT2 =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		BlendLUT1 =
		{
			Index = 2
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		BlendLUT2 =
		{
			Index = 3
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
    int2 position : POSITION;
};

VertexStruct VS_OUTPUT
{
    float4 position	: PDX_POSITION;
	float2 uv		: TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float2 InvWindowSize;
	float vBlendFactor1;
	float vBlendFactor2;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT VertexIn )
		{
			VS_OUTPUT VertexOut;
			VertexOut.position = float4( VertexIn.position, 0.0f, 1.0f );
		
			VertexOut.uv = float2( VertexIn.position.x, FIX_FLIPPED_UV(VertexIn.position.y) ) * 0.5 + 0.5;
			VertexOut.uv.y = 1.0 - VertexOut.uv.y;
		
		#ifdef PDX_DIRECTX_9 // Half pixel offset
			VertexOut.position.xy += float2( -InvWindowSize.x, InvWindowSize.y );
		#endif
		
			return VertexOut;
		}
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT Input ) : PDX_COLOR
		{
			float3 base = tex2Dlod0( BaseLUT1, Input.uv ).rgb;
			float3 blend = tex2Dlod0( BlendLUT1, Input.uv ).rgb;
			
		#ifdef DOUBLE_BLEND
			base = lerp(base, tex2Dlod0( BaseLUT2, Input.uv ).rgb, vBlendFactor1);
			blend = lerp(blend, tex2Dlod0( BlendLUT2, Input.uv ).rgb, vBlendFactor1);
		#endif
			
			//return float4( 1, 0, 0, 1 );
			return float4( lerp(base, blend, vBlendFactor2), 1 );
		}
	]]
}


BlendState BlendState
{
	BlendEnable = no
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
	DepthWriteMask = "DEPTH_WRITE_ZERO"
}

Effect LutBlend1
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

Effect LutBlend2
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
	
	Defines = { "DOUBLE_BLEND" }
}