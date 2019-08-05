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
		WaterColor =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		Diffuse =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Clamp"
		}
		NormalMap =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Clamp"
		}
		RiverData =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		LeanTexture1 =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		LeanTexture2 =
		{
			Index = 5
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ProvinceSecondaryColorMap =
		{
			Index = 6
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		HeightNormal =
		{
			Index = 7
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SnowMudTexture =
		{
			Index = 8
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		CityLightsAndSnowNoise =
		{
			Index = 9
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
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
		ReflectionCubeMap =
		{
			Index = 14
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
			Type = "Cube"
		}
		ShadowMap =
		{
			Index = 15
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition   : POSITION;
	float4 vUV_Tangent : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4 vPosition	    : PDX_POSITION;
	float2 vUV			    : TEXCOORD0;
	float2 vTangent			: TEXCOORD1;
	float4 vPrePos_Fade		: TEXCOORD2;
	float4 vScreenCoord		: TEXCOORD3;		
	float2 vWorldUV			: TEXCOORD4;
	float vTransp			: TEXCOORD5;
};


ConstantBuffer( 1, 32 )
{
	float4x4 ShadowMapTextureMatrix;
	float3 vTimeDirectionSeasonLerp;
};




VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT v )
		{
			VS_OUTPUT Out;
		
			Out.vPosition = float4( v.vPosition.xyz, 1.0f );
		
			Out.vTransp = v.vPosition.w;
		
			float4 vTmpPos = float4( v.vPosition.xyz, 1.0f );
			Out.vPrePos_Fade.xyz = vTmpPos.xyz;
		
			float4 vDistortedPos = vTmpPos - float4( vCamLookAtDir * 0.05f, 0.0f );
		
			vTmpPos = mul( ViewProjectionMatrix, vTmpPos );
			
			// move z value slightly closer to camera to avoid intersections with terrain
			float vNewZ = dot( vDistortedPos, float4( GetMatrixData( ViewProjectionMatrix, 2, 0 ), GetMatrixData( ViewProjectionMatrix, 2, 1 ), GetMatrixData( ViewProjectionMatrix, 2, 2 ), GetMatrixData( ViewProjectionMatrix, 2, 3 ) ) );
			Out.vPosition = float4( vTmpPos.xy, vNewZ, vTmpPos.w );
			
			Out.vUV.yx = v.vUV_Tangent.xy;
			Out.vUV.x *= 0.15f;
		
			Out.vTangent = v.vUV_Tangent.zw;
			Out.vPrePos_Fade.w = saturate( 1.0f - v.vUV_Tangent.y );
		
			// Output the screen-space texture coordinates
			Out.vScreenCoord.x = ( Out.vPosition.x * 0.5 + Out.vPosition.w * 0.5 );
			Out.vScreenCoord.y = ( Out.vPosition.w * 0.5 - Out.vPosition.y * 0.5 );
		#ifdef PDX_OPENGL
			Out.vScreenCoord.y = -Out.vScreenCoord.y;
		#endif			
			Out.vScreenCoord.z = Out.vPosition.w;
			Out.vScreenCoord.w = Out.vPosition.w;
		
			Out.vWorldUV.x = ( Out.vPrePos_Fade.x + 0.5f ) / MAP_SIZE_X;
			Out.vWorldUV.y = ( Out.vPrePos_Fade.z + 0.5f - MAP_SIZE_Y ) / -MAP_SIZE_Y;	
			Out.vWorldUV.xy *= float2( MAP_POW2_X, MAP_POW2_Y );
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float3 ApplyRiverSnow( float3 vColor, float3 vReflectColor, float3 vPos, inout float3 vNormal, float4 vMudSnowColor, in sampler2D SnowNoise, in float waterSideAlpha, out float vOutSpecGloss )
		{
			float vNoiseColor = tex2D( SnowNoise, vPos.xz * SNOW_ICE_NOISE_TILING ).a;
		
			float vIsSnow = GetSnow( vMudSnowColor );

			float vOpacity = cam_distance( SNOW_CAM_MIN, SNOW_CAM_MAX );
			vOpacity = SNOW_OPACITY_MIN + vOpacity * ( SNOW_OPACITY_MAX - SNOW_OPACITY_MIN );

			float vSnowAlpha = smoothstep( 0.0f, 1.0f, saturate( vIsSnow * vOpacity * 1.7 ) );
			vColor = lerp( vColor, 
			               lerp( saturate(SNOW_WATER_COLOR * vReflectColor), SNOW_COLOR, smoothstep(0.4, 0.75, saturate(vNoiseColor + waterSideAlpha))), 
			               vSnowAlpha );

			vNormal.y += lerp(20.0f, 1.0f, waterSideAlpha) * vSnowAlpha;
			vNormal = normalize( vNormal );
		
			vOutSpecGloss = vSnowAlpha;
		
			return vColor;
		}
	
		float4 main( VS_OUTPUT Input ) : PDX_COLOR
		{
			float2 vNewUV = Input.vUV;
			
			float vFlip = -1.0f;
			if ( Input.vUV.y < 0.5f )
			{
				vNewUV.y = 1.0f - vNewUV.y;
				vFlip = 1.0f;
			}
		
			vNewUV.y = saturate(vNewUV.y * 4 - 3);
		
			float3 waterColor = tex2D( WaterColor, Input.vWorldUV ).rgb;
		#ifdef LOW_END_GFX
			float4 diffuseColor = float4( waterColor, 1.0f );
			float2 waterSideAlpha = float2( 0, ( 1.0f - vNewUV.y ) * 0.8f );
		#else
			float4 diffuseColor = tex2D( Diffuse, float2( vNewUV.x, 1.0f - vNewUV.y ) );
			float2 waterSideAlpha = tex2D( RiverData, vNewUV ).br;
			if ( abs( Input.vUV.y - 0.5f ) <= 0.25f )
			{
				waterSideAlpha.x = 0.0f;
				waterSideAlpha.y = 1.0f; 
			}
		#endif
				
			float2 B;
			float3 M;
			float3 waterNormal;
			float2 vTimeMultipliers[4];
			float loltime = 0.4;
			vTimeMultipliers[0] = vec2( 0.98f ) * loltime;
			vTimeMultipliers[1] = vec2( 1.03f ) * loltime;
			vTimeMultipliers[2] = vec2( 0.95f ) * loltime;
			vTimeMultipliers[3] = vec2( 1.02f ) * loltime;

			float2 vUVMultipliers[4];
			float lol1 = 0.6f;
			vUVMultipliers[0] = vec2( 0.4 ) * lol1;
			vUVMultipliers[1] = vec2( 0.4 ) * lol1;
			float lol = 0.4f;
			vUVMultipliers[2] = float2( 1.0f * lol, -1.0f * lol);
			vUVMultipliers[3] = float2( 1.0f * lol, -1.0f * lol);
		
			SampleWater( Input.vUV, vUVMultipliers, vTimeDirectionSeasonLerp.x * vTimeDirectionSeasonLerp.y * 0.05f, vTimeMultipliers, B, M, waterNormal, LeanTexture1, LeanTexture2 );
			
		#ifdef LOW_END_GFX
			float3 SunDirWater = float3( 0, 1, 0 );
		#else
			float3 SunDirWater = CalculateSunDirectionWater( Input.vPrePos_Fade.xyz );
		#endif
			float3 H = normalize( normalize(vCamPos - Input.vPrePos_Fade.xyz).xzy + -SunDirWater.xzy );
			float2 HWave = H.xy/H.z - B;
		
			float3 sigma = M - float3( B*B, B.x*B.y);
			float det = sigma.x*sigma.y - sigma.z*sigma.z;
			float e = HWave.x*HWave.x*sigma.y + HWave.y*HWave.y*sigma.x - 2*HWave.x*HWave.y*sigma.z;
			float spec = (det <= 0) ? 0.0f : exp( -0.5f*e/det ) / sqrt(det);
		
		#ifdef LOW_END_GFX
			float3 normal = waterNormal;
		#else
			//float3 vHeightNormal = normalize( tex2D( HeightNormal, Input.vWorldUV ).rbg - 0.5f );
			float3 vCanalNormal = normalize( tex2D( NormalMap, float2( vNewUV.x, 1.0f - vNewUV.y ) ).rbg - 0.5f );
			vCanalNormal.z *= vFlip;
			
			float3 vTangent = normalize( float3( Input.vTangent.x, 0.0f, Input.vTangent.y ) );
			float3 vBitangent = normalize( float3( Input.vTangent.y, 0.0f, -Input.vTangent.x ) );
			float3 vTmpNormal = normalize( cross( vTangent, vBitangent ) );
			float3x3 TNB = Create3x3( vTangent, vTmpNormal, vBitangent );
			float3 vSideNormal = normalize( mul( vCanalNormal, TNB ) );
			float3 normal = normalize( lerp( waterNormal, vSideNormal, waterSideAlpha.x ) );
		#endif
		
			// Gradient Borders
			float gradientBorderFactor = 1.0f - gradient_border_camera_distance();

			float vBloomAlpha = 0.0f;	
		#ifndef LOW_END_GFX
			gradient_border_apply( diffuseColor.rgb, normal, Input.vWorldUV, GradientBorderChannel1, GradientBorderChannel2, 1.0f, vGBCamDistOverride_GBOutlineCutoff.zw, vGBCamDistOverride_GBOutlineCutoff.xy, vBloomAlpha );
		
			float3 gradientBorderWaterColor = waterColor;
			gradient_border_apply( gradientBorderWaterColor, normal, Input.vWorldUV, GradientBorderChannel1, GradientBorderChannel2, 1.0f, vGBCamDistOverride_GBOutlineCutoff.zw, vGBCamDistOverride_GBOutlineCutoff.xy, vBloomAlpha );
			waterColor = lerp( waterColor, gradientBorderWaterColor, gradientBorderFactor );
		#endif
			
			float3 vEyeDir = normalize( Input.vPrePos_Fade.xyz - vCamPos.xyz );
			float3 reflection = reflect( vEyeDir, normal );
			float3 reflectiveColor = texCUBE( ReflectionCubeMap, reflection ).rgb * 1.3;

			float fresnelBias = 0.5f;
			float fresnel = saturate( dot( -vEyeDir, normal ) ) * 0.5f;
			fresnel = saturate( fresnelBias + ( 1.0f - fresnelBias ) * pow( 1.0f - fresnel, 10.0) );
			waterColor = waterColor * ( 1.0f - fresnel ) + reflectiveColor * fresnel;

			float3 diffuse = lerp( waterColor, diffuseColor.rgb, waterSideAlpha.x );
			
			float vSnowSpecGloss = 0;
		#ifndef LOW_END_GFX
			float4 vMudSnow = GetMudSnowColor( Input.vPrePos_Fade.xyz, SnowMudTexture );
			diffuse = ApplyRiverSnow( diffuse.rgb, reflectiveColor, Input.vPrePos_Fade.xyz, normal, vMudSnow, CityLightsAndSnowNoise, waterSideAlpha.x, vSnowSpecGloss );
		#endif
			
			float vSpecularIntensity = lerp(.085, 0.051, vSnowSpecGloss);
			vSpecularIntensity = lerp( vSpecularIntensity, diffuseColor.a, waterSideAlpha.x ) * ( 1.0f - gradientBorderFactor*0.5 );
			float vGlossiness =  lerp( spec / 0.5f, 5.0f, waterSideAlpha.x ) + vSnowSpecGloss * SNOW_SPEC_GLOSS_MULT;
			
			LightingProperties lightingProperties;
			lightingProperties._WorldSpacePos = Input.vPrePos_Fade.xyz;
			lightingProperties._ToCameraDir = normalize(vCamPos - Input.vPrePos_Fade.xyz);
			lightingProperties._Diffuse = diffuse;
			lightingProperties._Normal = normal;
			lightingProperties._Glossiness = vGlossiness;
			lightingProperties._SpecularColor = vec3(vSpecularIntensity);
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vGlossiness);
			
			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);
		
			float fShadowTerm = GetShadowScaled( SHADOW_WEIGHT_RIVER, Input.vScreenCoord, ShadowMap );
		
			CalculateSunLight( lightingProperties, fShadowTerm, diffuseLight, specularLight );

		#ifndef LOW_END_GFX
			CalculatePointLights( lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);
		#endif

			float3 vOut = ComposeLight(lightingProperties, diffuseLight, specularLight);
			
			vOut = ApplyFOW( vOut, ShadowMap, Input.vScreenCoord );
		#ifndef LOW_END_GFX
			vOut = ApplyDistanceFog( vOut, Input.vPrePos_Fade.xyz );
		#endif
			vOut = DayNightWithBlend( vOut, CalcGlobeNormal( Input.vPrePos_Fade.xz ), lerp(BORDER_NIGHT_DESATURATION_MAX, 1.0f, vBloomAlpha) );
				
			float vFadeValue = ( 1.0f - Input.vPrePos_Fade.w );
		
			float vFastFade = vFadeValue * vFadeValue * vFadeValue * vFadeValue;
			vFastFade = vFastFade * vFastFade;
		
			// fade slower if water, faster if land(help river crossings)
			float vDesiredFade = (lerp( vFadeValue * 2.0f, 0.0f, saturate( waterSideAlpha.x * 4.0f ) ));
			float vAlphaMultiplier = saturate(lerp( vDesiredFade, 1.0f, vFastFade ));
			

			DebugReturn(vOut, lightingProperties, fShadowTerm);

			return float4( vOut, waterSideAlpha.y * vAlphaMultiplier * Input.vTransp );
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

Effect river_low_gfx
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
	Defines = { "LOW_END_GFX" }
}

Effect river
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}
