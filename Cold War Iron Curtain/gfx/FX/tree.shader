Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
	"shadow.fxh"
	"tiled_pointlights.fxh"
	"fow.fxh"
}

PixelShader =
{
	Samplers =
	{
		DiffuseMap =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		NormalMap =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TintMap =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SeasonMap =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ColorMap =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ColorMapSecond =
		{
			Index = 5
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SnowMudData =
		{
			Index = 6
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ShadowMap =
		{
			Index = 8
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
		}
		EnvironmentMap =
		{
			Index = 9
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
			Type = "Cube"
		}
		LightIndexMap =
		{
			Index = 10
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		LightDataMap =
		{
			Index = 11
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}	
		GradientBorderChannel1 =
		{
			Index = 12
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		GradientBorderChannel2 =
		{
			Index = 13
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		TreeMaskTexture =
		{
			Index = 14
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}		
		ProvinceSecondaryColorMap =
		{
			Index = 15
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}			
	}
}


VertexStruct VS_INPUT_INSTANCE
{
    float3 vPosition	: POSITION;
	float3 vNormal      : TEXCOORD0;
	float4 vTangent		: TEXCOORD1;
	float2 vUV0			: TEXCOORD2;
	float2 vUV1			: TEXCOORD3;
	float4 vPos_YRot   	: TEXCOORD4;
	float3 vSlopes    	: TEXCOORD5;
};

VertexStruct VS_OUTPUT
{
    float4 vPosition		  	: PDX_POSITION;
	float4 vTexCoord0_TintUV  	: TEXCOORD0;
	float3 vNormal          	: TEXCOORD1;
	float3 vPos				  	: TEXCOORD2;
	float4 vShadowProj			: TEXCOORD3;
	float4 vScreenCoord			: TEXCOORD4;
	float3 vTangent          	: TEXCOORD5;
	float3 vBitangent          	: TEXCOORD6;
	float4 vPrePos_vSeasonColumn : TEXCOORD7;
};

VertexStruct VS_OUTPUT_SHADOW
{
    float4 	vPosition  		: PDX_POSITION;
	float2 	fDepth 			: TEXCOORD0;
	float2	vTexCoord0_UV  	: TEXCOORD1;
	float3 	vPos			: TEXCOORD2;
};


ConstantBuffer( 1, 32 )
{
	float4x4 	ShadowMapTextureMatrix;
	float	 	vSeasonLerp;
	float		vSeasonColumn;
	float		vTreeFade;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT_INSTANCE v )
		{
			VS_OUTPUT Out;
		
			float vRandom = v.vPos_YRot.w / 6.28318531f;
			float vSummedRandom = v.vUV1.x + vRandom;
			vSummedRandom = vSummedRandom >= 1.0f ? vSummedRandom - 1.0f : vSummedRandom;
			
			float vHeightScaleFactor = 0.75f + vSummedRandom * 0.5f;
			Out.vPosition = float4( v.vPosition.xyz, 1.0 );
			Out.vPosition.y *= vHeightScaleFactor;
		
			float randSin = sin( v.vPos_YRot.w );
			float randCos = cos( v.vPos_YRot.w );
		
			Out.vPosition.xz = float2( 
				Out.vPosition.x * randCos - Out.vPosition.z * randSin, 
				Out.vPosition.x * randSin + Out.vPosition.z * randCos );
		
			Out.vPosition.y += Out.vPosition.x * v.vSlopes.x + Out.vPosition.z * v.vSlopes.y;
			Out.vPosition.xyz += v.vPos_YRot.xyz;
			
			Out.vPos = Out.vPosition.xyz;
		
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );
			
			Out.vTexCoord0_TintUV.xy = v.vUV0;
		
			Out.vNormal = v.vNormal;
			Out.vNormal.xz = float2( 
				Out.vNormal.x * randCos - Out.vNormal.z * randSin, 
				Out.vNormal.x * randSin + Out.vNormal.z * randCos );
			
			Out.vTangent = v.vTangent.xyz;
			Out.vTangent.xz = float2( 
				Out.vTangent.x * randCos - Out.vTangent.z * randSin, 
				Out.vTangent.x * randSin + Out.vTangent.z * randCos );
		
			Out.vBitangent = cross( Out.vTangent, Out.vNormal ) * v.vTangent.w;
			
			Out.vTexCoord0_TintUV.zw = float2( vRandom, 0.0f ) + v.vUV1;
			
			Out.vShadowProj = mul( ShadowMapTextureMatrix, float4( Out.vPos, 1.0f ) );	
			
			// Output the screen-space texture coordinates
			Out.vScreenCoord.x = ( Out.vPosition.x * 0.5 + Out.vPosition.w * 0.5 );
			Out.vScreenCoord.y = ( Out.vPosition.w * 0.5 - Out.vPosition.y * 0.5 );
		#ifdef PDX_OPENGL
			Out.vScreenCoord.y = -Out.vScreenCoord.y;
		#endif			
			Out.vScreenCoord.z = Out.vPosition.w;
			Out.vScreenCoord.w = Out.vPosition.w;
			
			Out.vPrePos_vSeasonColumn.xyz = v.vPosition.xyz;
			Out.vPrePos_vSeasonColumn.w = vSeasonColumn / 8.0;
			Out.vPrePos_vSeasonColumn.w += 1.0 / 16.0;
			
			return Out;
		}
		
	]]

	MainCode VertexShaderShadow
	[[
		VS_OUTPUT_SHADOW main( const VS_INPUT_INSTANCE v )
		{
			VS_OUTPUT_SHADOW Out;
		
			float vRandom = v.vPos_YRot.w / 6.28318531f;
			float vSummedRandom = v.vUV1.x + vRandom;
			vSummedRandom = vSummedRandom >= 1.0f ? vSummedRandom - 1.0f : vSummedRandom;
			
			float vHeightScaleFactor = 0.75f + vSummedRandom * 0.5f;
			Out.vPosition = float4( v.vPosition.xyz, 1.0f );
			Out.vPosition.y *= vHeightScaleFactor;
		
			float randSin = sin( v.vPos_YRot.w );
			float randCos = cos( v.vPos_YRot.w );
		
			Out.vPosition.xz = float2( 
				Out.vPosition.x * randCos - Out.vPosition.z * randSin, 
				Out.vPosition.x * randSin + Out.vPosition.z * randCos );
		
			Out.vPosition.y += Out.vPosition.x * v.vSlopes.x + Out.vPosition.z * v.vSlopes.y;
			Out.vPosition.xyz += v.vPos_YRot.xyz;
		
			Out.vPos = Out.vPosition.xyz;
		
			Out.vPosition 	= mul( ViewProjectionMatrix, Out.vPosition );
			Out.fDepth 		= Out.vPosition.zw;	
			
			Out.vTexCoord0_UV = v.vUV0;
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	Code
	[[
		float GetTreeMask( in sampler2D TreeMaskTexture, float3 vPos )
		{
			float vMask = tex2D( TreeMaskTexture, float2( ( ( vPos.x-0.5 ) / MAP_SIZE_X ), ( ( vPos.z+2.0f-MAP_SIZE_Y ) / -MAP_SIZE_Y )) ).a;
			return vMask;
		}
	]]

	MainCode PixelShader
	[[	
		float3 ApplySnowTree( float3 vColor, float3 vPos, inout float3 vNormal, float4 vFoWColor, out float vSnowAlpha )
		{
			float vIsSnow = GetSnow( vFoWColor );
			//float vSnowFade = saturate( saturate( vNormal.y - saturate( 1.0f - vIsSnow ) )*vIsSnow*5.5f*saturate( ( vNormal.y - 0.8f ) * 1000.0f ) );
			float vSnowFade = saturate( vIsSnow * 1.5f );
			
			float vOpacity = cam_distance( SNOW_CAM_MIN, SNOW_CAM_MAX );
			vOpacity = SNOW_OPACITY_MIN + vOpacity * ( SNOW_OPACITY_MAX - SNOW_OPACITY_MIN );
			
			vColor = lerp( vColor, SNOW_COLOR, vSnowFade * vOpacity );
			
			//vNormal.y += 1.0f * vSnowFade;
			//vNormal = normalize( vNormal );
			vSnowAlpha = vSnowFade * vOpacity;
			
			return vColor;
		}
		
		float4 main( VS_OUTPUT In ) : PDX_COLOR
		{
			float4 vDiffuseColor = tex2D( DiffuseMap, In.vTexCoord0_TintUV.xy );
			if( vCamPos.y < 80.0f )
				clip( vDiffuseColor.a - 0.5f );
			
			clip( 0.17 - GetTreeMask( TreeMaskTexture, In.vPos ) );
			
			float2 uv = float2( ( ( In.vPos.x+0.5f ) / MAP_SIZE_X ), ( ( In.vPos.z+0.5f-MAP_SIZE_Y ) / -MAP_SIZE_Y )); 
			
			float3 vColor = GetOverlay( vDiffuseColor.rgb, tex2D( TintMap, In.vTexCoord0_TintUV.zw ).rgb, 0.5f );	
			
			float3 vSeasonColorMap = lerp( tex2D( ColorMap, uv), tex2D( ColorMapSecond, uv), vSeasonLerp ).rgb;	
		
			vColor = GetOverlay( vColor, vSeasonColorMap, 0.25f );
			
			float vSeasonTreeFade = saturate( saturate( (In.vPos.z/MAP_SIZE_Y) - TREE_SEASON_MIN )*TREE_SEASON_FADE_TWEAK );
			vColor += ( tex2D( SeasonMap, float2( In.vPrePos_vSeasonColumn.w, In.vTexCoord0_TintUV.w ) ).rgb-0.5f ) * vSeasonTreeFade;
		
			float3 vNormalSample = normalize( tex2D( NormalMap, In.vTexCoord0_TintUV.xy  ).rgb - 0.5f );
			float3x3 TBN = Create3x3( normalize( In.vTangent ), normalize( In.vBitangent ), normalize( In.vNormal ) );
			float3 vNormal = mul( vNormalSample, TBN );	
			
			float vSnowAlpha = 0;
		#ifndef LOW_END_GFX
			float4 vFoWColor = GetMudSnowColor( In.vPos, SnowMudData );
			vColor = ApplySnowTree( vColor, In.vPos, vNormal, vFoWColor, vSnowAlpha );	
		#endif

			// Gradient Borders
			float vBloomAlpha = 0.0f;
			gradient_border_apply( vColor.rgb, vNormal, uv, GradientBorderChannel1, GradientBorderChannel2, 1.0f, vGBCamDistOverride_GBOutlineCutoff.zw, vGBCamDistOverride_GBOutlineCutoff.xy, vBloomAlpha );

			// Secondary color mask
			secondary_color_mask( vColor.rgb, vNormal, uv, ProvinceSecondaryColorMap, vBloomAlpha );			

			float vSpecular 	= TREE_SPECULAR;
			float vRoughness 	= TREE_ROUGHNESS;
			float3 vPos = In.vPos.xyz;
		
			LightingProperties lightingProperties;
			lightingProperties._WorldSpacePos = vPos;
			lightingProperties._ToCameraDir = normalize(vCamPos - vPos);
			lightingProperties._Normal = vNormal;
			lightingProperties._Diffuse = vColor;
			lightingProperties._Glossiness = vRoughness;
			lightingProperties._SpecularColor = vec3(vSpecular);
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vSpecular);
			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);
		
			float fShadowTerm = GetShadowScaled( SHADOW_WEIGHT_TREE, In.vScreenCoord, ShadowMap );	
			CalculateSunLight(lightingProperties, fShadowTerm, diffuseLight, specularLight);

		#ifndef LOW_END_GFX
			CalculatePointLights(lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);

			float3 vEyeVec = vPos - vCamPos.xyz;
			float3 vEyeDir = normalize( vEyeVec );
			float4 reflection = float4( reflect( vEyeDir, vNormal ), 3 - vRoughness * 3 );
			float3 reflectiveColor = texCUBEbias( EnvironmentMap, reflection ).rgb;
		
			diffuseLight += reflectiveColor * vSpecular;
		#endif
			
			vColor = ComposeLightSnow(lightingProperties, diffuseLight, specularLight, vSnowAlpha );

			float3 vGlobalNormal = CalcGlobeNormal( vPos.xz );
		
			float3 vFOWColor = ApplyFOW( vColor, ShadowMap, In.vScreenCoord );
			vColor = lerp( vFOWColor, vColor, BORDER_FOW_REMOVAL_FACTOR * ( 1 - vBloomAlpha ) );
		#ifndef LOW_END_GFX
			vColor = ApplyDistanceFog( vColor, vPos );
		#endif
			vColor.rgb = DayNight( vColor.rgb, vGlobalNormal );

			DebugReturn(vColor, lightingProperties, fShadowTerm);
			//return float4( vColor, 1.0 - saturate( (length(vEyeVec) - 100.0) / 200.0 ) );
			return float4( vColor, vTreeFade );
		}
	]]

	MainCode PixelShaderShadow
	[[	
		float4 main( VS_OUTPUT_SHADOW In ) : PDX_COLOR
		{
			float4 vDiffuseColor = tex2D( DiffuseMap, In.vTexCoord0_UV.xy );
			clip( vDiffuseColor.a - 0.5f );
			
			clip( 0.1f - GetTreeMask( TreeMaskTexture, In.vPos ) );
			
			return float4( In.fDepth.xxx * In.fDepth.y, 1.0f);
		}
	]]

	MainCode PixelShaderUnlit
	[[
		float4 main( VS_OUTPUT In ) : PDX_COLOR
		{
			float4 vDiffuseColor = tex2D( DiffuseMap, In.vTexCoord0_TintUV.xy );
			if( vCamPos.y < 80.0f )
				clip( vDiffuseColor.a - 0.5f );
			
			clip( 0.17 - GetTreeMask( TreeMaskTexture, In.vPos ) );
		
			// Grab the shadow term
			float fShadowTerm = CalculateShadow( In.vShadowProj, ShadowMap);
			
			float FogColorFactor = 0.0;
			float FogAlphaFactor = 0.0;
			float ExtraHeight = In.vPrePos_vSeasonColumn.y * 4 - In.vPos.y * 0.5 + 6;
			GetFogFactors( FogColorFactor, FogAlphaFactor, In.vPos.xyz, ExtraHeight, TintMap, SeasonMap, ColorMap);
			
			return float4( fShadowTerm, FogColorFactor, FogAlphaFactor, 1.0f );
		}				
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	AlphaTest = no
	WriteMask = "RED|GREEN|BLUE"
	
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect tree_low_gfx
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
	Defines = { "LOW_END_GFX" }
}

Effect tree
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

Effect treeshadow
{
	VertexShader = "VertexShaderShadow"
	PixelShader = "PixelShaderShadow"
}

Effect treeunlit
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderUnlit"
}

