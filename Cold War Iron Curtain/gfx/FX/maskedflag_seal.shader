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
    float4 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float4  vTexCoord : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
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
			Out.vTexCoord.zw = v.vTexCoord.zw;
			Out.vTexCoord.xy = v.vTexCoord.xy/FlagCoords.xy;
			Out.vTexCoord.xy += FlagCoords.zw;
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
		 	float4 OutColor = tex2D( BaseTexture, v.vTexCoord.xy );
			OutColor -= tex2D( BaseTexture, v.vTexCoord.xy-0.0009)*2.7f;
			OutColor += tex2D( BaseTexture, v.vTexCoord.xy+0.0009)*2.7f;
			float vC = (( OutColor.r*0.212671+OutColor.g*0.715160+OutColor.b*0.072169)/3.0f );
			OutColor.rgb = float3(vC, vC, vC);
			OutColor.rgb *= float3( 3.0f, 1.0f, 1.0f );
			float4 MaskColor = tex2D( MaskTexture, v.vTexCoord.zw );
			OutColor.a = MaskColor.a;
			
			return OutColor;
		}
		
	]]

	MainCode PixelShaderOver
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord.xy );
			OutColor -= tex2D( BaseTexture, v.vTexCoord.xy-0.0009)*2.7f;
			OutColor += tex2D( BaseTexture, v.vTexCoord.xy+0.0009)*2.7f;
			float vC = ( ( OutColor.r*0.212671+OutColor.g*0.715160+OutColor.b*0.072169)/3.0f );
			OutColor.rgb = float3(vC,vC,vC);
			vC = ( dot( OutColor.rgb, float3( 1.0f, 0.2f, 0.2f ) ) );
			OutColor = float4(vC, vC, vC, vC);
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord.zw );
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
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord.xy );
			OutColor -= tex2D( BaseTexture, v.vTexCoord.xy-0.0009)*2.7f;
			OutColor += tex2D( BaseTexture, v.vTexCoord.xy+0.0009)*2.7f;
			float vC = ( ( OutColor.r*0.212671+OutColor.g*0.715160+OutColor.b*0.072169)/3.0f );
			OutColor.rgb = float3(vC, vC, vC);
			vC = ( dot( OutColor.rgb, float3( 1.0f, 0.2f, 0.2f ) ) );
			OutColor = float4(vC,vC,vC,vC);
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord.zw );
		    float4 MixColor = float4( 0.1, 0.1, 0.1, 0 );
		    OutColor.a = MaskColor.a;
		    OutColor -= MixColor;
		    
		    return OutColor;
		}
		
	]]

	MainCode PixelShaderDisable
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( BaseTexture, v.vTexCoord.xy );
		    float4 MaskColor = tex2D( MaskTexture, v.vTexCoord.zw );
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

