Includes = {
}

PixelShader =
{
	Samplers =
	{
		TextureOne =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TextureTwo =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition  : POSITION;
    float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord0 : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix; 
	float4 vFirstColor;
	float4 vSecondColor;
	float CurrentState;
};


VertexShader =
{
	MainCode VertexShader
	[[
		
		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
		   	Out.vPosition  = mul( WorldViewProjectionMatrix, v.vPosition );
			Out.vTexCoord0  = v.vTexCoord;
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelColor
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			if( v.vTexCoord0.x <= CurrentState / 2.f )
				return vFirstColor;
			else
				return vSecondColor;
		}
		
	]]

	MainCode PixelTexture
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float y1 = 0.5f / 20.f;
			float y2 = CurrentState / 20.f;

			float xPos = v.vTexCoord0.x - 0.04f;
			float xPos2 = v.vTexCoord0.x;
			float xPos3 = v.vTexCoord0.x + 0.04f;
			float xPos4 = v.vTexCoord0.x + 0.08f;
			float yPos = v.vTexCoord0.y / 20.f; 

			float dist = abs((y2 - y1) * xPos - (1.f) * yPos + y1) / sqrt((y2 - y1) * (y2 - y1) + 1.f);
			float dist2 = abs((y2 - y1) * xPos2 - (1.f) * yPos + y1) / sqrt((y2 - y1) * (y2 - y1) + 1.f);
			float dist3 = abs((y2 - y1) * xPos3 - (1.f) * yPos + y1) / sqrt((y2 - y1) * (y2 - y1) + 1.f);
			float dist4 = abs((y2 - y1) * xPos4 - (1.f) * yPos + y1) / sqrt((y2 - y1) * (y2 - y1) + 1.f);

			if (dist < 0.0004f || dist2 < 0.0004f || dist3 < 0.0004f || dist4 < 0.0004f)
				return tex2D( TextureOne, v.vTexCoord0.xy );
			else
				return tex2D( TextureTwo, v.vTexCoord0.xy );
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect Color
{
	VertexShader = "VertexShader"
	PixelShader = "PixelColor"
}

Effect Texture
{
	VertexShader = "VertexShader"
	PixelShader = "PixelTexture"
}

