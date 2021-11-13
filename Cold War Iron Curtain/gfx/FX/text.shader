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
	float4x4 	Matrix;//			: register( c0 );
	float4		ModColor;
};


VertexShader =
{
	MainCode VertexShaderText3D
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= mul( Matrix, v.vPosition );
			
		    Out.vTexCoord  	= v.vTexCoord;
			
			Out.vColor		= v.vColor * ModColor;
		
		    return Out;
		}
		
		
	]]

	MainCode VertexShaderText
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= mul( Matrix, v.vPosition );
			
		    Out.vTexCoord  	= v.vTexCoord;
			
			Out.vColor		= v.vColor * ModColor;
		
		    return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelShaderText
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			//return float4( 1, 0, 0, 1 );
		    float4 OutColor = tex2D( SimpleTexture, v.vTexCoord );
			OutColor = OutColor * v.vColor;
		    return OutColor;
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	AlphaTest = no
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	BlendOpAlpha = blend_op_max
}


Effect Text
{
	VertexShader = "VertexShaderText"
	PixelShader = "PixelShaderText"
}

Effect Text3D
{
	VertexShader = "VertexShaderText3D"
	PixelShader = "PixelShaderText"
}

