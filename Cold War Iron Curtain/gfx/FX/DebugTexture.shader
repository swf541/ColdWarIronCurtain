PixelShader =
{
	Samplers =
	{
		Texture =
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
    float2 Position : POSITION;
	float2 UV : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4 Position : PDX_POSITION;
 	float2 UV : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4 UVOffset_UVScale;
	float4 ChannelScale_Alpha;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v)
		{
		    VS_OUTPUT Out;
			Out.Position = float4( v.Position, 0.0f, 1.0f );
			Out.UV = v.UV * UVOffset_UVScale.zw + UVOffset_UVScale.xy;
		    return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT Input ) : PDX_COLOR
		{
			float3 color = tex2D( Texture, Input.UV ).rgb;
		    return float4(color * ChannelScale_Alpha.rgb, ChannelScale_Alpha.w);
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}


Effect DebugTexture
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

