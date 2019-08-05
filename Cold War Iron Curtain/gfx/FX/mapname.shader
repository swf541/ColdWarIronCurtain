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
			MipMapLodBias = -0.4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}

		
ConstantBuffer( 1, 32 )
{
	float4 Transp_OffsetX;
};

VertexStruct VS_INPUT
{
    float3 vPosition  : POSITION;
	float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4 vPosition : PDX_POSITION;
	float3 vPrepos   : TEXCOORD0;
    float2 vTexCoord : TEXCOORD1;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT v )
		{
			VS_OUTPUT Out;
		
			float4 vPos = float4( v.vPosition, 1.0f );
			vPos.x += Transp_OffsetX.y;
			float4 vDistortedPos = vPos - float4( vCamLookAtDir * 0.5f, 0.0f );
		
			vPos = mul( ViewProjectionMatrix, vPos );
			
			// move z value slightly closer to camera to avoid intersections with terrain
			float vNewZ = dot( vDistortedPos, float4( GetMatrixData( ViewProjectionMatrix, 2, 0 ), GetMatrixData( ViewProjectionMatrix, 2, 1 ), GetMatrixData( ViewProjectionMatrix, 2, 2 ), GetMatrixData( ViewProjectionMatrix, 2, 3 ) ) );
			
			Out.vPosition = float4( vPos.xy, vNewZ, vPos.w );
			Out.vPrepos = v.vPosition.xyz;
			Out.vTexCoord = v.vTexCoord;
		
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
			float4 vSample = tex2D( DiffuseTexture, v.vTexCoord );
			vSample.a *= Transp_OffsetX.x;// * vFade;	
			vSample.rgb *= 1.0f - ( DayNightFactor( CalcGlobeNormal( v.vPrepos.xz ) ) * 0.35f );
			return vSample;
		}
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	AlphaTest = no
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
	DepthWriteMask = "depth_write_all"
	DepthFunction = "comparison_less_equal"
	StencilEnable = no
	FrontStencilFailOp = "stencil_op_keep"
	FrontStencilDepthFailOp = "stencil_op_keep"
	FrontStencilPassOp = "stencil_op_incr"
	FrontStencilFunc = "comparison_equal"
}


Effect mapname
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

