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
			Out.vTexCoord0.y = -Out.vTexCoord0.y;

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
			float segment = 1.f/5.f * 3.14159265f * 2.f;
			float rot = 0 * segment;

			int inValue = floor(CurrentState * 100.f);
			int i1 = floor(inValue / 10.f);
			int i2 = (inValue + 0.01f) % 10; // 0.01f here bc float grossness

			float3 p1 = float3(0.5f + (sin(rot) * (i1+1) * 0.05f), 0.5f + (cos(rot) * (i1+1) * 0.05f), 0.f);
			float3 p2 = float3(0.5f + (sin(rot + segment) * (i2+1) * 0.05f), 0.5f + (cos(rot + segment) * (i2+1) * 0.05f), 0.f);
			float3 p3 = float3(0.5f, 0.5f, 0.f);
			float3 pt = float3(v.vTexCoord0.x, -v.vTexCoord0.y, 0.f);

			float3 cp1 = cross(p2 - p1, p3-p1);
			float3 cp2 = cross(p2 - p1, pt-p1);
			float d = dot(cp1, cp2);
			if (d < 0) {
				return tex2D( TextureTwo, v.vTexCoord0.xy );
			}

			cp1 = cross(p3 - p1, p2-p1);
			cp2 = cross(p3 - p1, pt-p1);
			d = dot(cp1, cp2);
			if (d < 0) {
				return tex2D( TextureTwo, v.vTexCoord0.xy );
			}

			cp1 = cross(p3 - p2, p1-p2);
			cp2 = cross(p3 - p2, pt-p2);
			d = dot(cp1, cp2);
			if (d < 0) {
				return tex2D( TextureTwo, v.vTexCoord0.xy );
			}


			return tex2D( TextureOne, v.vTexCoord0.xy );
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

