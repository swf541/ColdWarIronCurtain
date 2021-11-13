Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
	"pdxmap.fxh"
	"shadow.fxh"
	"fow.fxh"
}

PixelShader =
{
	Samplers =
	{
		BorderDiffuse =
		{
			Index = 0
			MipMapLodBias = -0.5
			MipMapMaxLod = 4
			MipMapMinLod = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Clamp"
		}
		SnowMudData =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		IntelMap =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ShadowMap =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
		}
	}
}


VertexStruct VS_INPUT_BORDER
{
    float3 position			: POSITION;
	int2 uv					: TEXCOORD0;
};

VertexStruct VS_OUTPUT_BORDER
{
    float4 position			: PDX_POSITION;
	float3 pos				: TEXCOORD0;
	float2 uv				: TEXCOORD1;
	float4 vScreenCoord		: TEXCOORD2;
};


ConstantBuffer( 2, 48 )
{
	float4 vSelectionColor;
	float2 vTime_Transparency;
};



VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT_BORDER main( const VS_INPUT_BORDER VertexIn )
		{
			VS_OUTPUT_BORDER VertexOut;
		
			float4 pos = float4( VertexIn.position, 1.0f );
		
			float vClampHeight = saturate( ( WATER_HEIGHT - VertexIn.position.y ) * 10000 );
		
			pos.y = vClampHeight * WATER_HEIGHT + ( 1.0f - vClampHeight ) * pos.y;
			VertexOut.pos = pos.xyz;
		
			float4 vDistortedPos = pos - float4( vCamLookAtDir * 0.05f, 0.0f );
			pos = mul( ViewProjectionMatrix, pos );
			
			// move z value slightly closer to camera to avoid intersections with terrain
			float vNewZ = dot( vDistortedPos, float4( GetMatrixData( ViewProjectionMatrix, 2, 0 ), GetMatrixData( ViewProjectionMatrix, 2, 1 ), GetMatrixData( ViewProjectionMatrix, 2, 2 ), GetMatrixData( ViewProjectionMatrix, 2, 3 ) ) );
			VertexOut.position = float4( pos.xy, vNewZ, pos.w );
		
			VertexOut.uv = VertexIn.uv;
			
			// Output the screen-space texture coordinates
			VertexOut.vScreenCoord.x = ( VertexOut.position.x * 0.5 + VertexOut.position.w * 0.5 );
			VertexOut.vScreenCoord.y = ( VertexOut.position.w * 0.5 - VertexOut.position.y * 0.5 );
		#ifdef PDX_OPENGL
			VertexOut.vScreenCoord.y = -VertexOut.vScreenCoord.y;
		#endif		
			VertexOut.vScreenCoord.z = VertexOut.position.w;
			VertexOut.vScreenCoord.w = VertexOut.position.w;	
			
			return VertexOut;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		
		float4 main( VS_OUTPUT_BORDER Input ) : PDX_COLOR
		{
			float4 vColor = tex2D( BorderDiffuse, float2( Input.uv.y * BORDER_TILE, Input.uv.x ) );
						
			//float4 vMudSnow = GetMudSnowColor( Input.pos, SnowMudData );	
			//float vIsSnow = saturate( GetSnow( vMudSnow ) * 5.0 );
			//vColor.rgb = lerp(vColor.rgb, vec3(0.5) - vColor.rgb, (1.0 - vIsSnow));
			
			float vPulseFactor = saturate( smoothstep( 0.0f, 1.0f, ( 0.8f - abs( Input.uv.x - 0.5f ) ) + sin( vTime_Transparency.x * 2.5f ) * 0.15f ) ) * vSelectionColor.a; 
			vColor.rgb = saturate( vColor.rgb + vSelectionColor.rgb * saturate( vPulseFactor - vColor.a * 0.35f ) );
			
			// Grab the shadow term
			float fShadowTerm = GetShadowScaled( SHADOW_WEIGHT_BORDER, Input.vScreenCoord, ShadowMap );		
			vColor.rgb *=  fShadowTerm;
			
			float3 vFOW = ApplyFOW( vColor.rgb, ShadowMap, Input.vScreenCoord );
			vColor.rgb = lerp( vFOW, vColor.rgb, BORDER_FOW_REMOVAL_FACTOR );
		
			vColor.rgb = ApplyDistanceFog( vColor.rgb, Input.pos ) * max( 1.0f, vPulseFactor );
			vColor.rgb = DayNightWithBlend( vColor.rgb, CalcGlobeNormal( Input.pos.xz ), 1.0 );
			
			return float4( vColor.rgb, max( vColor.a, vPulseFactor - 0.2f ) * vTime_Transparency.y );
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


Effect border
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

