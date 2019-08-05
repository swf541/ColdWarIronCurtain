Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	Samplers =
	{
		DiffuseTexture =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		FoWTexture =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		FoWDiffuse =
		{
			Index = 2
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
    float4 vPosition		: POSITION;
	float4 vUV				: TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition 	: PDX_POSITION;
    float2	vUV		  	: TEXCOORD0;
	float3	vPos		: TEXCOORD1;
};

VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT v )
		{
			VS_OUTPUT Out;
		   	
			float4 vPos = float4( v.vPosition.xyz, 1.0f );
		   	Out.vPosition  = mul( ViewProjectionMatrix, vPos );
		
			// move z value slightly closer to camera to avoid intersections with terrain
			float4 vDistortedPos = vPos - float4( vCamLookAtDir * 0.05f, 0.0f );
			float vNewZ = dot( vDistortedPos, float4( GetMatrixData( ViewProjectionMatrix, 2, 0 ), GetMatrixData( ViewProjectionMatrix, 2, 1 ), GetMatrixData( ViewProjectionMatrix, 2, 2 ), GetMatrixData( ViewProjectionMatrix, 2, 3 ) ) );
			Out.vPosition.z = vNewZ;
			
		   	Out.vUV = v.vUV.xy;
			Out.vPos = vPos.rgb;
			
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
			float4 vColor = tex2D( DiffuseTexture, v.vUV );
			vColor.rgb = ApplyDistanceFog( vColor.rgb, v.vPos );	
			
			return vColor;
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

DepthStencilState DepthStencil
{
	DepthEnable = yes
}

RasterizerState RasterizerState
{
	FillMode = "FILL_SOLID"
	CullMode = "CULL_BACK"
	FrontCCW = no
}


Effect strait
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

