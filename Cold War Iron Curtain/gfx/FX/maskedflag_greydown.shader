Includes = {
}

PixelShader =
{
	Samplers =
	{
		BaseTexture =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		MaskTexture =
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
    float2 vMaskCoord  : TEXCOORD1;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord0 : TEXCOORD0;
    float2  vTexCoord1 : TEXCOORD1;
};


ConstantBuffer( 1, 32 )
{
	float4x4 WorldViewProjectionMatrix; 
	float4	 FlagCoords;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
		
			Out.vPosition  = mul( WorldViewProjectionMatrix, v.vPosition );
		
			Out.vTexCoord1 = v.vMaskCoord;
		
			Out.vTexCoord0.x = v.vTexCoord.x/FlagCoords.x;
			Out.vTexCoord0.x = Out.vTexCoord0.x + FlagCoords.z;
			Out.vTexCoord0.y = v.vTexCoord.y/FlagCoords.y;
			Out.vTexCoord0.y = Out.vTexCoord0.y + FlagCoords.w;
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float4 OutColor = tex2D( BaseTexture, v.vTexCoord0.xy );
			float4 MaskColor = tex2D( MaskTexture, v.vTexCoord1.xy );
			OutColor.a = MaskColor.a;
			
			return OutColor;
		}
		
	]]

	MainCode PixelShaderOver
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord0.xy );
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord1.xy );
		    float4 MixColor = float4( 0.1, 0.1, 0.1, 0 );
		    OutColor.a = MaskColor.a;
		    OutColor += MixColor;
		    
		    return OutColor;
		}
		
	]]

	MainCode PixelShaderDown
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord0.xy );
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord1.xy );
		    float Grey = dot( OutColor.rgb, float3( 0.212671f, 0.715160f, 0.072169f ) ); 
		    
		    OutColor.rgb = float3(Grey,Grey,Grey);
		    OutColor.a = MaskColor.a;
		    
		    return OutColor;
		}
		
	]]

	MainCode PixelShaderDisable
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord0.xy );
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord1.xy );
		    float Grey = dot( OutColor.rgb, float3( 0.212671f, 0.715160f, 0.072169f ) ); 
		    
		    OutColor.rgb = float3(Grey,Grey,Grey);
		    OutColor.a = MaskColor.a;
		    
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
}


Effect Up
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

Effect Down
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderDown"
}

Effect Disable
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderDisable"
}

Effect Over
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderOver"
}

