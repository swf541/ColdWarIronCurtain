Includes = {
}

PixelShader =
{
	Samplers =
	{
		SimpleTexture =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition  : POSITION;
    float2 vTexCoord  : TEXCOORD0;
	float4 vColor	  : COLOR;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord : TEXCOORD0;
	float4  vColor	  : TEXCOORD1;
};


ConstantBuffer( 0, 0 )
{
	float4x4 Mat;
};


VertexShader =
{
	MainCode VertexShaderSimple3D
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= mul( Mat, v.vPosition );
			
		    Out.vTexCoord  	= v.vTexCoord;
			
			Out.vColor		= v.vColor;
		
		    return Out;
		}
		
		
	]]

	MainCode VertexShaderSimple
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= mul( Mat, v.vPosition );
			
		    Out.vTexCoord  	= v.vTexCoord;
			
			Out.vColor		= v.vColor;
		
		    return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelShaderSimple
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( SimpleTexture, v.vTexCoord );
			OutColor = OutColor * v.vColor;
		    return OutColor;
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect Simple
{
	VertexShader = "VertexShaderSimple"
	PixelShader = "PixelShaderSimple"
}

Effect Simple3D
{
	VertexShader = "VertexShaderSimple3D"
	PixelShader = "PixelShaderSimple"
}

