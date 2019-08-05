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
			if( v.vTexCoord0.x <= CurrentState )
				return vFirstColor;
			else
				return vSecondColor;
		}
		
	]]

	MainCode PixelTexture
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float2 vUVStart = v.vTexCoord0.xy;
			vUVStart.y /= 3.f;
			vUVStart.y += 1.f / 3.f;
			float2 vUVMiddle = vUVStart;
			vUVMiddle.y += 1.f/3.f;
			float2 vUVStop = vUVMiddle;
			vUVStop.y +=  1.f/3.f;
			vUVStop.x += 1.f - CurrentState;
			
			if( v.vTexCoord0.x <= CurrentState )
			{
				float4 vStartColor = tex2D( TextureOne, vUVStart );
				float4 vMiddleColor = tex2D( TextureOne, vUVMiddle );
				float4 vStopColor = tex2D( TextureOne, vUVStop );
				
				float vStartAlpha = vStartColor.a;
				float4 vColor = lerp( vMiddleColor, vStartColor, vStartAlpha );
				vColor = lerp( vColor, vStopColor, vStopColor.a );
				vColor.a = vMiddleColor.a;
				return vColor;
			}
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

