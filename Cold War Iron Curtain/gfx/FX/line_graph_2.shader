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
            float width = vFirstColor.r * 1000.f;
            float height = vFirstColor.g * 1000.f;
            float lineWidth = vFirstColor.b * 10.f;

			float value = CurrentState * 1000000.f;
			float end = mod(value, 1000.f) / height;
			float start = floor(value / 1000.f) / height;

            float mod = mod(floor(v.vTexCoord0.x * width), 15);
            if  ((mod < 5) && vSecondColor.r == 0.95) {
                return float4(0, 0, 0, 0);
            }


            float2 p1 = float2(0, height * start);
            float2 p2 = float2(width, height * end);

            float2 currentP = float2(width * v.vTexCoord0.x, height * v.vTexCoord0.y);

            float2 lineDir = p2 - p1;
            float2 perpDir = float2(lineDir.y, -lineDir.x);

            float2 dir1 = p1 + float2(0.f, 0.f) - currentP;
            float dist1 = abs(dot(normalize(perpDir), dir1));

            float2 dir2 = p1 + float2(0.1f, 0.1f) - currentP;
            float dist2 = abs(dot(normalize(perpDir), dir2));

            float2 dir3 = p1 + float2(-0.1f, 0.1f) - currentP;
            float dist3 = abs(dot(normalize(perpDir), dir3));

            float2 dir4 = p1 + float2(-0.1f, -0.1f) - currentP;
            float dist4 = abs(dot(normalize(perpDir), dir4));

            float2 dir5 = p1 + float2(0.1f, -0.1f) - currentP;
            float dist5 = abs(dot(normalize(perpDir), dir5));

            float dist = min(dist1, min(dist2, min(dist3, min(dist4, dist5))));

            if (currentP.y > max(p1.y, p2.y) || currentP.y < min(p1.y, p2.y)) {
                dist = max(dist, min(abs(p1.y - currentP.y), abs(p2.y - currentP.y)));
            }


            float intensity = saturate((lineWidth - dist) / 1.4f);

            float4 toRet = vSecondColor;
            toRet.a *= intensity;
            return toRet;
		}
		
	]]

	MainCode PixelTexture
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
            return float4(1, 1, 1, 1);
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

