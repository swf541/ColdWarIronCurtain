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
			// Map Fill Palette Shader
			// By Calph
			// =========
			// This shader is set up to work with two images;
			//   First, a map asset (can technically be anything)
			//   Second, a palette.
			//     The palette must be set up as a sequence of equally-sized color blocks, with no spacing.
			//
			// Input is handled as such:
			// 	 textureFile1 points to the map asset
			//   textureFile2 points to the palette asset
			//   color must be in the format { r g b a } and contains;
			//     r: receives to the 'intensity' (or alpha) of the color overlayed on the map asset
			//     g: receives the 'width' of the palette in colors (e.g. a palette that goes 'RGBW' would have a width of 4, or 0.04)
			//     b: receives the height or depth of the palette. Is non functional here.
			//     a: is not used
			//   colortwo is not used.
			//
			// NOTES:
			//   A 'steps' argument *must* be used and it *must* be 10000.
			//   Be aware that all color inputs must be in the format 0.x (example: an 'intensity' of 40 will be entered as 0.40)
			//     That is, all entered values are input as 100 times less than their actual values

			// Usual Fare
			float4 texColor = tex2D(TextureOne, v.vTexCoord0.xy);
			if (texColor.a == 0) return float4(0, 0, 0, 0);
			
			float alpha = vFirstColor.r;
			float paletteWidth = vFirstColor.g * 100.f;
			float correction = 0.01;
			float xCoord = CurrentState * (10000 / paletteWidth) - correction;
			float yCoord = 0;

			// Construct Fill Color
			float4 fillColor = tex2D(TextureTwo, float2 (xCoord, yCoord));
			if (fillColor.a == 0) return texColor;

			// Overlay & Return
			float3 displayColor = texColor.rgb * (1 - alpha) + fillColor.rgb * alpha;
			return float4(displayColor.r, displayColor.g, displayColor.b, 1.0);
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

