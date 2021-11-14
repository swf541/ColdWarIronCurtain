Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	Samplers =
	{
		ReflectionCubeMap =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
			Type = "Cube"
		}
	}
}


VertexStruct VS_INPUT_SKY
{
    int2 position			: POSITION;
};

VertexStruct VS_OUTPUT_SKY
{
    float4 position	: PDX_POSITION;
	float3 pos		: TEXCOORD0;
};



VertexShader =
{
	MainCode VertexShader
	[[
		
		VS_OUTPUT_SKY main( const VS_INPUT_SKY VertexIn )
		{
			VS_OUTPUT_SKY VertexOut;
		
			VertexOut.position = float4( VertexIn.position, 1.0f, 1.0f );
			float4 position = mul( InvViewProjMatrix, VertexOut.position );
			position.xyz /= position.w;
			VertexOut.pos = position.xyz;
			return VertexOut;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT_SKY Input ) : PDX_COLOR
		{
			float3 color = texCUBE( ReflectionCubeMap, normalize( Input.pos - vCamPos ) ).rgb;
			float3 fog = ApplyDistanceFog( color.rgb, Input.pos );
		
			color = lerp( fog, color, max( saturate( Input.pos.y / 300.0f ), NegFogMultiplier ) );
			return float4( color, 1.0f );
		}
		
		
	]]
}


BlendState BlendState
{
	BlendEnable = no
	AlphaTest = no
}


Effect sky
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

