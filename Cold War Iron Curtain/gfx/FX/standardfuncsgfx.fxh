
ConstantBuffer( 0, 0 )
{
	float4x4	ViewProjectionMatrix;
	float4x4	InvViewProjMatrix;
	float4 		vGBCamDistOverride_GBOutlineCutoff;
	float4 		vVirtualSunPos;
	float4		vVirtualMoonPos;
	float4 		vSecondVirtualSunPos;
	float4		vSecondVirtualMoonPos;
	float3 		vCamPos;
	float 		HdrRange;
	float3 		vCamLookAtDir;
	float 		vGlobalTime;
	float4		vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed;
	float4		DayNight_Hour_SunDir;

	float3		AmbientPosX;
	float		ShadowFadeFactor;
	float3		AmbientNegX;
	float		FOWFadeFactor;
	float3		AmbientPosY;
	float		MinMeshAlpha;
	float3		AmbientNegY;
	float		NegFogMultiplier;
	float3		AmbientPosZ;
	float3		AmbientNegZ;
	float		CubemapIntensity;
	float4		SunDiffuseIntensity
	float4		MoonDiffuseIntensity
	float		GB_TextureHeight;
};


Code
[[
	float ToGamma(float aLinear)
	{
		return pow(aLinear, 0.45);
	}

	float3 ToGamma(float3 aLinear)
	{
		return pow(aLinear, vec3(0.45));
	}

	float3 ToLinear(float3 aGamma)
	{
		return pow(aGamma, vec3(2.2));
	}

	float4 ToLinear(float4 aGamma)
	{
		return float4(pow(aGamma.rgb, vec3(2.2)), aGamma.a);
	}

	// Standard functions
	float3 RotateVectorByVector( float3 v1, float3 v2 )
	{
		float3 zaxis = v1; //normal
		float3 xaxis = cross( zaxis, float3( 0, 0, 1 ) ); //tangent
		xaxis = normalize( xaxis );
		float3 yaxis = cross( xaxis, zaxis ); //bitangent
		yaxis = normalize( yaxis );
		return xaxis * v2.x + zaxis * v2.y + yaxis * v2.z;
	}

	float2 RotateVector2D( float2 v, float vAngle )
	{
		float oldX = v.x;
		float vCos = cos( vAngle );
		float vSin = sin( vAngle );
		v.x = ( v.x * vCos ) - ( v.y * vSin );
		v.y = ( v.y * vCos ) + ( oldX * vSin );
		return v;
	}

]]

PixelShader = 
{
	Code
	[[

	static const float3 STANDARD_vDiffuseLight = float3( 1.4f, 1.2f, 1.0f );
	static const float  STANDARD_vIntensity    = 1.f;
	static const float STANDARD_HDR_RANGE 	= 0.9f;

	// Photoshop filters, kinda...
	float3 HuePost( float H )
	{
		float X = 1 - abs( ( mod( H, 2 ) ) - 1 );
		if ( H < 1.0f )			return float3( 1.0f,    X, 0.0f );
		else if ( H < 2.0f )	return float3(    X, 1.0f, 0.0f );
		else if ( H < 3.0f )	return float3( 0.0f, 1.0f,    X );
		else if ( H < 4.0f )	return float3( 0.0f,    X, 1.0f );
		else if ( H < 5.0f )	return float3(    X, 0.0f, 1.0f );
		else					return float3( 1.0f, 0.0f,    X );
	}

	float3 HSVtoRGBPost( in float3 aHSV )
	{
		if ( aHSV.y != 0.0f )
		{
			float C = aHSV.y * aHSV.z;
			return clamp( HuePost( aHSV.x ) * C + ( aHSV.z - C ), 0.0f, 1.0f );
		}
		return saturate( aHSV.zzz );
	}

	float3 RGBtoHSV( in float3 RGB )
	{
		float Cmax = max( RGB.r, max( RGB.g, RGB.b ) );
		float Cmin = min( RGB.r, min( RGB.g, RGB.b ) );
		float diff = Cmax - Cmin;
		
		float H = 0.0;
		float S = 0.0;
		if (diff != 0.0)
		{
			S = diff / Cmax;
			
			if (Cmax == RGB.r)
				H = (RGB.g - RGB.b) / diff + 6.0;
			else if (Cmax == RGB.g)
				H = (RGB.b - RGB.r) / diff + 2.0;
			else
				H = (RGB.r - RGB.g) / diff + 4.0;
		}

		return float3(H, S, Cmax);
	}


	float3 Hue(float H)
	{
	    float R = abs(H * 6 - 3) - 1;
	    float G = 2 - abs(H * 6 - 2);
	    float B = 2 - abs(H * 6 - 4);
	    return saturate(float3(R,G,B));
	}

	// used for manual input, converts to linear
	float3 HSVtoRGB(float H, float S, float V)
	{
		float3 hue = Hue(H);
		float3 val = (hue - vec3(1)) * S + vec3(1);
		val *= V;

	    return ToLinear( val );
	}

	float3 HSVtoRGB(float3 hsv)
	{
		return HSVtoRGB(hsv.r, hsv.g, hsv.b);
	}

	float3 GetOverlay( float3 vColor, float3 vOverlay, float vOverlayPercent )
	{
		float3 vColorGamma = ToGamma(vColor);
		float3 vOverlayGamma = ToGamma(vOverlay);

		float3 res;
		res.r = vOverlayGamma.r < .5 ? (2 * vOverlayGamma.r * vColorGamma.r) : (1 - 2 * (1 - vOverlayGamma.r) * (1 - vColorGamma.r));
		res.g = vOverlayGamma.g < .5 ? (2 * vOverlayGamma.g * vColorGamma.g) : (1 - 2 * (1 - vOverlayGamma.g) * (1 - vColorGamma.g));
		res.b = vOverlayGamma.b < .5 ? (2 * vOverlayGamma.b * vColorGamma.b) : (1 - 2 * (1 - vOverlayGamma.b) * (1 - vColorGamma.b));
		res = ToLinear(res);
		return lerp( vColor, res, vOverlayPercent );
	}

	float3 Levels( float3 vInColor, float vMinInput, float vMaxInput )
	{
		float3 vRet = saturate( vInColor - vMinInput );
		vRet /= vMaxInput - vMinInput;
		return saturate( vRet );
	}

	float Levels( float vInValue, float vMinValue, float vMaxValue )
	{
		return saturate( ( vInValue - vMinValue ) / ( vMaxValue - vMinValue ) );
	}

	float cam_distance( float vMin, float vMax )
	{
		return ( clamp( vCamPos.y, vMin, vMax ) - vMin ) / ( vMax - vMin );
	}

	float GetFoW( float3 vPos, in sampler2D TexFoW )
	{
		float vStrength = 1.0f - cam_distance( FOW_CAMERA_MIN, FOW_CAMERA_MAX );
		vStrength *= FOW_MAX;
		return tex2D( TexFoW, float2( ( ( vPos.x + 0.5f ) / MAP_SIZE_X ) * FOW_POW2_X, ( (vPos.z + 0.5f ) / MAP_SIZE_Y) ) * FOW_POW2_Y ).a * vStrength;
		//return GetFoWColor( vPos, TexFoW ).a;
		//float vFoWDiffuse = tex2D( FoWDiffuse, ( vPos.xz + 0.5f ) / 256.0f + vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.y * 0.02f ).r;
		//vFoWDiffuse = sin( ( vFoWDiffuse + frac( vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.y * 0.1f ) ) * 6.28318531f ) * 0.1f;
		//float vShade = vFoWDiffuse + 0.5f;
		//float vIsFow = vFoWColor.a;
		//return lerp( 1.0f, saturate( vIsFow + vShade ), vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.x );
		//return 1.0f; // <- TODO
	}

	float CalculateDistanceFogFactor(float3 vPos)
	{
		float3 vDiff = vCamPos - vPos;
		float vFogFactor = 1.0f - abs( normalize( vDiff ).y ); // abs b/c of reflections
		float vSqDistance = dot( vDiff, vDiff );

		float vBegin = FOG_BEGIN;
		float vEnd = FOG_END;
		vBegin *= vBegin;
		vEnd *= vEnd;
		
		float vMaxFog = FOG_MAX;
		
		float vMin = min( ( vSqDistance - vBegin ) / ( vEnd - vBegin ), vMaxFog );

		return saturate( vMin ) * vFogFactor;
	}

	float3 ApplyDistanceFog( float3 vColor, float vFogFactor )
	{
		return lerp( vColor, FOG_COLOR, vFogFactor );
	}

	float3 ApplyDistanceFog( float3 vColor, float3 vPos )
	{
		return ApplyDistanceFog( vColor, CalculateDistanceFogFactor(vPos) );
	}
	
	float4 GetMudSnowColor( float3 vPos, in sampler2D MudSnowTexture)
	{
		return tex2D( MudSnowTexture, float2( ( ( vPos.x + 0.5f ) / MAP_SIZE_X ) * FOW_POW2_X, ( (vPos.z + 0.5f ) / MAP_SIZE_Y) ) * FOW_POW2_Y );
	}

	
	float3 GetMudColor( in float3 vResult, in float4 vMudSnowColor, in float3 vPos, inout float3 vNormal, inout float vGlossiness, inout float vSpec,
						 in sampler2D MudDiffuseGlossSampler, in sampler2D MudNormalSpecSampler )
	{
		float vMudCurrent = lerp( vMudSnowColor.r, vMudSnowColor.a, vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.z );
		vMudCurrent *= 1.0 - saturate( saturate( vNormal.y - MUD_NORMAL_CUTOFF ) * ( ( 1.0 - MUD_NORMAL_CUTOFF ) * 1000.0 ) );
		vMudCurrent = saturate( vMudCurrent * MUD_STRENGHTEN );
		float4 vMudDiffuseGloss = tex2D( MudDiffuseGlossSampler, vPos.xz * MUD_TILING );
		float4 vMudNormalSpec = tex2D( MudNormalSpecSampler, vPos.xz * MUD_TILING );
		
		float3 vMudNormal = normalize( vMudNormalSpec.rbg - 0.5 );
		vMudNormal = normalize( RotateVectorByVector( vMudNormal, vNormal ) );
		vNormal = normalize( lerp( vNormal, vMudNormal, vMudCurrent ) );
		vGlossiness = lerp( vGlossiness, vMudDiffuseGloss.a, vMudCurrent );
		vSpec = lerp( vSpec, vMudNormalSpec.a, vMudCurrent );
		
		return lerp( vResult, vMudDiffuseGloss.rgb, vMudCurrent );
	}

	float GetSnow( float4 vMudSnowColor )
	{
		return lerp( vMudSnowColor.b, vMudSnowColor.g, vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.z ); //Get winter;
	}

	float3 ApplySnow( float3 vColor, float3 vPos, inout float3 vNormal, float4 vMudSnowColor, in sampler2D SnowTextureSampler,
					 in sampler2D SnowNoise, inout float vGlossiness, inout float vSnowAlphaOut )
	{
		float vSnowFade = saturate( vPos.y - SNOW_START_HEIGHT );
		float vNormalFade = saturate( saturate( vNormal.y - SNOW_NORMAL_START ) * SNOW_CLIFFS );
		float4 vSnowTexture = tex2D( SnowTextureSampler, vPos.xz * SNOW_TILING );
		float vNoise = tex2D( SnowNoise, vPos.xz * SNOW_NOISE_TILING ).a;
		
		float vIsSnow = GetSnow( vMudSnowColor );

		//Increase snow on ridges
		float vTransp = vNoise;
		vTransp += saturate( vPos.y - SNOW_RIDGE_START_HEIGHT )*( saturate( (vNormal.y-0.9f) * 1000.0f )*vIsSnow );
		vTransp = saturate( vTransp );
		
		float vSnow = saturate( saturate( vTransp - ( 1.0f - vIsSnow ) ) * 5.0f );
		float vFrost = saturate( saturate( vTransp + 0.5f ) - ( 1.0f - vIsSnow ) );
		
		float vOpacity = cam_distance( SNOW_CAM_MIN, SNOW_CAM_MAX );
		vOpacity = SNOW_OPACITY_MIN + vOpacity * ( SNOW_OPACITY_MAX - SNOW_OPACITY_MIN );
		
		float vSnowAlpha = saturate( ( saturate( vSnow + vFrost ) * vSnowFade * vNormalFade * saturate(vIsSnow * 2.25) * vOpacity ) );
		float vMinSnow = smoothstep( 0.0f, 1.0f, vIsSnow );
		vColor = lerp( vColor, vSnowTexture.a * SNOW_COLOR, vSnowAlphaOut * saturate( vSnowAlpha + ( SNOW_FROST_MIN_EFFECT * vMinSnow ) ) );	

		// if we want to flatten
		//vNormal.y += 1.0f * vSnowAlpha;
		//vNormal = normalize( vNormal );

		float3 vSnowNormal = normalize( vSnowTexture.rbg - 0.5f );
		vSnowNormal = normalize( RotateVectorByVector( vSnowNormal, vNormal ) );
		vNormal = normalize(lerp( vNormal, vSnowNormal, vSnowAlpha )); // mah physics!

		vSnowAlphaOut = vSnowAlpha;
		vGlossiness += vSnowTexture.a * vSnowAlpha * SNOW_SPEC_GLOSS_MULT;

		return vColor;
	}

	float3 UnpackNormal( in sampler2D NormalTex, float2 uv )
	{
		float3 vNormalSample = normalize( tex2D( NormalTex, uv ).rgb - 0.5f );
		vNormalSample.g = -vNormalSample.g;
		return vNormalSample;
	}


	float3 UnpackRRxGNormal(float4 NormalMapSample)
	{
		float x = NormalMapSample.g * 2.0 - 1.0;
		float y = NormalMapSample.a * 2.0 - 1.0;
		y = -y;
		float z = sqrt(saturate(1.0 - x * x - y * y));
		return float3(x, y, z);
	}


	//#define NO_NIGHT

	static const float GMT_OFFSET = 2793.0f; // X position on map, of Greenwitch GMT+0
	static const float FEATHER_MIN = -0.01f;
	static const float FEATHER_MAX = 0.01f;
	static const float MOON_FEATHER_MIN = -0.01f;
	static const float MOON_FEATHER_MAX = 0.01;
	static const float NIGHT_OPACITY = 0.85f;
	static const float NIGHT_DARKNESS = 0.5f;
	static const float SOUTH_POLE_OFFSET = 0.17f; // Our map is missing big parts of globe on north and south
	static const float NORTH_POLE_OFFSET = 0.93f;
	static const float GLOBE_NORMAL_LIMIT = 0.8f;


	float3 GlobeNormalToMapNormal( float3 vGlobeNormal, float3 vNormal )
	{
		float3 vOrigNormal = vNormal;
		float vTemp = vGlobeNormal.y;
		vGlobeNormal.y = clamp( abs( vGlobeNormal.z ), GLOBE_NORMAL_LIMIT, 1.0f );
		vGlobeNormal.z = vTemp;
		vGlobeNormal.x = -vGlobeNormal.x;
		vGlobeNormal = normalize( vGlobeNormal );
		vNormal = RotateVectorByVector( vNormal, vGlobeNormal );
		return lerp( vOrigNormal, normalize( vNormal ), vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.w );
	}

	float3 CalcGlobeNormal( float2 vWorldXZ )
	{
		float x = fmod_loop( ( vWorldXZ.x - GMT_OFFSET ) / MAP_SIZE_X + DayNight_Hour_SunDir.x, 1.0f );
		float y = vWorldXZ.y / MAP_SIZE_Y;
		y = SOUTH_POLE_OFFSET + ( NORTH_POLE_OFFSET - SOUTH_POLE_OFFSET ) * y;
		y = -cos( y * 3.1415f );
		float xzLen = 1.0f - abs( y );
		float3 vGlobeNormal = float3( sin( x * 6.2831f ) * xzLen, y, cos( x * 6.2831f ) * xzLen );
		return normalize( vGlobeNormal );
	}

	float DayNightFactor( float3 vGlobeNormal, float vMin, float vMax )
	{
		float vDot = dot( vGlobeNormal, DayNight_Hour_SunDir.yzw );
		return saturate( ( vDot - vMin ) / ( vMax - vMin ) ) * vFoWOpacity_FoWTime_SnowMudFade_MaxGameSpeed.w;
	}


	float DayNightFactor( float3 vGlobeNormal )
	{
		return DayNightFactor( vGlobeNormal, FEATHER_MIN, FEATHER_MAX );
	}

	float3 NightifyColor( float3 vDayColor, float vBlend )
	{

		float vDesaturation = lerp(0.0f, 0.8f, vBlend * vBlend * vBlend );	

		float Grey = dot( vDayColor.rgb, float3( 0.4f, 0.3f, 0.05f ) );
		float3 vNightColor = saturate(lerp(vec3(Grey), Grey * float3(0.2,0.7,1.2), vec3(0.25f) ));

		float3 vColor = lerp(vDayColor, vNightColor, vec3(vDesaturation));

	    return vColor * NIGHT_DARKNESS;
	}


	float3 DayNightWithBlend( float3 vDayColor, float3 vGlobeNormal, float vBlend )
	{	
		#ifdef NO_NIGHT
		return vDayColor;
		#endif

		//return vec3( DayNightFactor( vGlobeNormal ) );

	    // lerp between day and night
		return lerp( vDayColor, NightifyColor(vDayColor, vBlend), DayNightFactor( vGlobeNormal ) * NIGHT_OPACITY );
	}

	// Darken the color by the night opacity
	float3 DayNight( float3 vDayColor, float3 vGlobeNormal )
	{	
		return DayNightWithBlend(vDayColor, vGlobeNormal, 1.0f);
	}

	float3 DayNightCityMask( float3 vDayColor, float3 vGlobeNormal, float vCityLightMask, float vFogFactor )
	{
		#ifdef NO_NIGHT
		return vDayColor;
		#endif

		float vNightFactor = DayNightFactor( vGlobeNormal );

	    // lerp between day and night
		float3 Result = lerp( vDayColor, NightifyColor(vDayColor , 0.0f), vNightFactor * NIGHT_OPACITY );

		Result += vCityLightMask * float3(2.0f, 2.0f, 0.3f) * vNightFactor * (1.0f - vFogFactor * vFogFactor);

		return Result;
	}








	struct PointLight
	{
		float3 _Position;
		float _Radius;
		float3 _Color;
		float _Falloff;
	};

	PointLight GetPointLight(float4 PositionAndRadius, float4 ColorAndFalloff)
	{
		PointLight pointLight;
		pointLight._Position = PositionAndRadius.xyz;
		pointLight._Radius = PositionAndRadius.w;
		pointLight._Color = ColorAndFalloff.xyz;
		pointLight._Falloff = ColorAndFalloff.w;
		return pointLight;
	}

	struct LightingProperties
	{
		float3 _WorldSpacePos;
		float3 _ToCameraDir;
		float3 _Normal;
		float3 _Diffuse;
		
		float3 _SpecularColor;
		float _Glossiness;
		float _NonLinearGlossiness;
	};


	float3 AmbientLight( float3 WorldNormal, float vDayFactor, float3 DayAmbientColors_[6], float3 NightAmbientColors_[6] ) 
	{	
		// add more of bottom ambient below objects
		WorldNormal = lerp( WorldNormal, normalize(WorldNormal - smoothstep(-0.6, 0.5, dot(WorldNormal, float3(0, -1, 0))) * float3(0, 0.9, 0)), NegFogMultiplier );

		float3 Squared = WorldNormal * WorldNormal; 
	#ifdef	PDX_OPENGL
		int3 isNegative = int3(lessThan(WorldNormal, vec3(0.0)));
	#else
		int3 isNegative = (WorldNormal < 0.0);
	#endif
	
		float3 Color = Squared.x * lerp( DayAmbientColors_[isNegative.x], saturate(NIGHT_AMBIENT_BOOST * NightAmbientColors_[isNegative.x]), vDayFactor )
			+ Squared.y * lerp( DayAmbientColors_[isNegative.y+2],  saturate(NIGHT_AMBIENT_BOOST * NightAmbientColors_[isNegative.y+2]), vDayFactor )
			+ Squared.z * lerp( DayAmbientColors_[isNegative.z+4],  saturate(NIGHT_AMBIENT_BOOST * NightAmbientColors_[isNegative.z+4]), vDayFactor );

		return Color;
	}

	float3 AmbientLight( float3 WorldNormal, float vDayFactor ) 
	{	
		float3 DayAmbientColors[6];
		DayAmbientColors[0] = DayAmbientMapPosX;
		DayAmbientColors[1] = DayAmbientMapNegX;
		DayAmbientColors[2] = DayAmbientMapPosY;
		DayAmbientColors[3] = DayAmbientMapNegY;
		DayAmbientColors[4] = DayAmbientMapPosZ;
		DayAmbientColors[5] = DayAmbientMapNegZ;

		float3 NightAmbientColors[6];
		NightAmbientColors[0] = NightAmbientMapPosX;
		NightAmbientColors[1] = NightAmbientMapNegX;
		NightAmbientColors[2] = NightAmbientMapPosY;
		NightAmbientColors[3] = NightAmbientMapNegY;
		NightAmbientColors[4] = NightAmbientMapPosZ;
		NightAmbientColors[5] = NightAmbientMapNegZ;


		return AmbientLight(WorldNormal, vDayFactor, DayAmbientColors, NightAmbientColors);
	}

	// Direct lighting
	float3 FresnelSchlick(float3 SpecularColor, float3 E, float3 H)
	{
		return SpecularColor + (vec3(1.0f) - SpecularColor) * pow(1.0 - saturate(dot(E, H)), 5.0);
	}

	// Indirect lighting
	float3 FresnelGlossy(float3 SpecularColor, float3 E, float3 N, float Smoothness)
	{
		return SpecularColor + (max(vec3(Smoothness), SpecularColor) - SpecularColor) * pow(1.0 - saturate(dot(E, N)), 5.0);
	}

	float3 MetalnessToDiffuse(float Metalness, float3 DiffuseValue)
	{
		return lerp(DiffuseValue, vec3(0.0), Metalness);
	}

	float3 MetalnessToSpec(float Metalness, float3 DiffuseValue, float Spec)
	{
		return lerp(vec3(Spec), DiffuseValue, Metalness);
	}

	//------------------------------
	// Phong -----------------------
	//------------------------------
	float3 CalculatePBRSpecularPower( float3 vPos, float3 vNormal, float3 vMaterialSpecularColor, float vSpecularPower, float3 vLightColor, float3 vLightDirIn )
	{	
		float3 H = normalize( normalize( vCamPos - vPos ) + -vLightDirIn );
		float NdotH = saturate( dot( H, vNormal ) );
		float NdotL = saturate( dot( -vLightDirIn, vNormal ) );
		float3 vSpecularColor = vLightColor * saturate( pow( NdotH, vSpecularPower ) * SPECULAR_MULTIPLIER ) * vMaterialSpecularColor;
		vSpecularColor = FresnelSchlick( vMaterialSpecularColor * SPECULAR_MULTIPLIER, -vLightDirIn, H) * ((vSpecularPower + 2) / 8 ) * saturate( pow( NdotH, vSpecularPower ) ) * NdotL * vLightColor;
		return vSpecularColor;
	}

	float3 CalculateLight( float3 vNormal, float3 vLightDirection, float3 vLightIntensity )
	{
		float NdotL = dot( vNormal, -vLightDirection );
		return max(NdotL, 0.0) * vLightIntensity;
	}

	void PhongPointLight(PointLight aPointlight, LightingProperties aProperties, inout float3 aDiffuseLightOut, inout float3 aSpecularLightOut)
	{
		float3 lightdir = aProperties._WorldSpacePos - aPointlight._Position;
		float lightdist = length(lightdir);
		
		float vLightIntensity = saturate((aPointlight._Radius - lightdist) / aPointlight._Falloff);

		if (vLightIntensity > 0)
		{
			lightdir /= lightdist;
			aDiffuseLightOut += CalculateLight(aProperties._Normal, lightdir, aPointlight._Color * vLightIntensity);
			aSpecularLightOut += CalculatePBRSpecularPower(aProperties._WorldSpacePos, aProperties._Normal, aProperties._SpecularColor, aProperties._Glossiness, aPointlight._Color * vLightIntensity, lightdir);
		}
	}


	//------------------------------
	// Blinn-Phong -----------------
	//------------------------------
	float GetNonLinearGlossiness(float aGlossiness)
	{
		return exp2(11.0 * aGlossiness); //exp2(GlossScale * Gloss + GlossBias)
	}

	float GetEnvmapMipLevel(float aGlossiness)
	{
		return (1.0 - aGlossiness) * (8.0);
	}

	void ImprovedBlinnPhong(float3 aLightColor, float3 aToLightDir, LightingProperties aProperties, out float3 aDiffuseLightOut, out float3 aSpecularLightOut)
	{
		float3 H = normalize(aProperties._ToCameraDir + aToLightDir);
		float NdotL = saturate(dot(aProperties._Normal, aToLightDir));
		float NdotH = saturate(dot(aProperties._Normal, H));

		float normalization = (aProperties._NonLinearGlossiness + 2.0) / 8.0;
		float3 specColor = normalization * pow(NdotH, aProperties._NonLinearGlossiness) * FresnelSchlick(aProperties._SpecularColor, aToLightDir, H);
		
		aDiffuseLightOut = aLightColor * NdotL;
		aSpecularLightOut = specColor * aLightColor * NdotL;
	}

	// TODO other, square, falloff?
	void ImprovedBlinnPhongPointLight(PointLight aPointlight, LightingProperties aProperties, inout float3 aDiffuseLightOut, inout float3 aSpecularLightOut)
	{
		float3 posToLight = aPointlight._Position - aProperties._WorldSpacePos;
		float lightDistance = length(posToLight);
		
		float lightIntensity = saturate((aPointlight._Radius - lightDistance) / aPointlight._Falloff);
		if (lightIntensity > 0)
		{
			float3 toLightDir = posToLight / lightDistance;
			float3 diffLight;
			float3 specLight;
			ImprovedBlinnPhong(aPointlight._Color * lightIntensity, toLightDir, aProperties, diffLight, specLight);
			aDiffuseLightOut += diffLight;
			aSpecularLightOut += specLight;
		}
	}

	float3 CalculateSunDirection( float3 vWorldPos, float3 SunPos, float3 SecondSunPos, float3 MoonPos, float3 SecondMoonPos )
	{
		float vSelected = DayNightFactor( CalcGlobeNormal( vWorldPos.xz ), 0.0f, 0.0001f  );
		float3 vSourcePos = lerp( SunPos, MoonPos, vSelected );
		float3 vSecondSourcePos = lerp( SecondSunPos, SecondMoonPos, vSelected );

		if ( vWorldPos.x - vSourcePos.x > MAP_SIZE_X * 0.5 )
		{
			vSourcePos.x += MAP_SIZE_X;
		}
		else if ( vWorldPos.x - vSourcePos.x < -MAP_SIZE_X * 0.5 )
		{
			vSourcePos.x -= MAP_SIZE_X;
		}
		
		if ( vWorldPos.x - vSecondSourcePos.x > MAP_SIZE_X * 0.5 )
		{
			vSecondSourcePos.x += MAP_SIZE_X;
		}
		else if ( vWorldPos.x - vSecondSourcePos.x < -MAP_SIZE_X * 0.5 )
		{
			vSecondSourcePos.x -= MAP_SIZE_X;
		}
		
		float lerpFactor = abs( vWorldPos.x - vSourcePos.x ) / (MAP_SIZE_X * 0.5);
		lerpFactor = smoothstep(0.5, 1.0, lerpFactor);
		vSourcePos = lerp( vSourcePos, vSecondSourcePos, lerpFactor );

		return normalize( vWorldPos - vSourcePos );
	}
	
	float3 CalculateSunDirection( float3 vWorldPos )
	{
		return CalculateSunDirection( vWorldPos, vVirtualSunPos.xyz, vSecondVirtualSunPos.xyz, vVirtualMoonPos.xyz, vSecondVirtualMoonPos.xyz );
	}

	float3 CalculateSunDirectionWater( float3 vWorldPos )
	{
		return CalculateSunDirection( vWorldPos, vVirtualSunPos.xwz, vSecondVirtualSunPos.xwz, vVirtualMoonPos.xwz, vSecondVirtualMoonPos.xwz );
	}

	//-------------------------------
	// Common lighting functions ----
	//-------------------------------
	void CalculateSunLight(LightingProperties aProperties, float aShadowTerm, float3 vLightSourceDirection, out float3 aDiffuseLightOut, out float3 aSpecularLightOut )
	{
		float vDayFactor = 1.0f - DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ) );
		float vNightFactor = DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ), MOON_FEATHER_MIN, MOON_FEATHER_MAX );

		aShadowTerm = aShadowTerm * saturate( vDayFactor + vNightFactor );

		float3 sunIntensity = 
			SunDiffuseIntensity.rgb * SunDiffuseIntensity.a * aShadowTerm * vDayFactor
			+ MoonDiffuseIntensity.rgb * MoonDiffuseIntensity.a * aShadowTerm * vNightFactor;	
		//sunIntensity += 0.6f * (1.0f - (vDayFactor  * aShadowTerm + vNightFactor));

	#ifdef PDX_IMPROVED_BLINN_PHONG
		ImprovedBlinnPhong(sunIntensity, -vLightSourceDirection, aProperties, aDiffuseLightOut, aSpecularLightOut);
	#else
		aDiffuseLightOut = CalculateLight(aProperties._Normal, vLightSourceDirection, sunIntensity);
		aSpecularLightOut = CalculatePBRSpecularPower(aProperties._WorldSpacePos, aProperties._Normal, aProperties._SpecularColor, aProperties._Glossiness, sunIntensity, vLightSourceDirection);
	#endif
	}

	void CalculateSunLight(LightingProperties aProperties, float aShadowTerm, out float3 aDiffuseLightOut, out float3 aSpecularLightOut )
	{
		float3 vLightSourceDirection = CalculateSunDirection( aProperties._WorldSpacePos );
		CalculateSunLight(aProperties, aShadowTerm, vLightSourceDirection, aDiffuseLightOut, aSpecularLightOut );
	}

	void CalculatePointLight(PointLight aPointlight, LightingProperties aProperties, inout float3 aDiffuseLightOut, inout float3 aSpecularLightOut)
	{
	#ifdef PDX_IMPROVED_BLINN_PHONG
		ImprovedBlinnPhongPointLight(aPointlight, aProperties, aDiffuseLightOut, aSpecularLightOut);
	#else
		PhongPointLight(aPointlight, aProperties, aDiffuseLightOut, aSpecularLightOut);
	#endif
	}

	float3 ComposeLight(LightingProperties aProperties, float3 aDiffuseLight, float3 aSpecularLight )
	{
		float vDayNight = DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ) );

		float3 vAmbientColor = AmbientLight(aProperties._Normal, vDayNight);
		float3 diffuse = ((vAmbientColor + aDiffuseLight) * aProperties._Diffuse) * HdrRange;
		float3 specular = aSpecularLight;

		return diffuse + specular;
	}

	float3 CalcSnowAmbient( float3 aDiffuseLight, float vSnowFactor )
	{
		//float vAmbientIntensity = 1 - saturate(dot(aDiffuseLight, float3(1,1,1)));
		return float3(0.2, 0.7, 1) * 0.07 * smoothstep(0.0, 0.1, vSnowFactor );
	}

	float3 ComposeLightSnow(LightingProperties aProperties, float3 aDiffuseLight, float3 aSpecularLight, float vSnowFactor )
	{
		float vDayNight = DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ) );
		float3 vAmbientColor = AmbientLight(aProperties._Normal, vDayNight);
	#ifdef LOW_END_GFX
		return (((vAmbientColor + aDiffuseLight) * aProperties._Diffuse) * HdrRange) + aSpecularLight;
	#else
		float3 SnowAmbient = CalcSnowAmbient(aDiffuseLight, vSnowFactor);
		return (((SnowAmbient + vAmbientColor + aDiffuseLight) * aProperties._Diffuse) * HdrRange) + aSpecularLight;
	#endif
	}

	float3 ComposeLightMesh(LightingProperties aProperties, float3 aDiffuseLight, float3 aSpecularLight, float vSnowFactor )
	{
		float vDayNight = DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ) );

		float3 DayAmbientColors[6];
		DayAmbientColors[0] = AmbientPosX;
		DayAmbientColors[1] = AmbientNegX;
		DayAmbientColors[2] = AmbientPosY;
		DayAmbientColors[3] = AmbientNegY;
		DayAmbientColors[4] = AmbientPosZ;
		DayAmbientColors[5] = AmbientNegZ;

		float3 NightAmbientColors[6];
		NightAmbientColors[0] = NightAmbientPosX;
		NightAmbientColors[1] = NightAmbientNegX;
		NightAmbientColors[2] = NightAmbientPosY;
		NightAmbientColors[3] = NightAmbientNegY;
		NightAmbientColors[4] = NightAmbientPosZ;
		NightAmbientColors[5] = NightAmbientNegZ;

		float3 vAmbientColor = AmbientLight(aProperties._Normal, vDayNight, DayAmbientColors, NightAmbientColors);
		float3 SnowAmbient = CalcSnowAmbient(aDiffuseLight, vSnowFactor);
		float3 diffuse = ((SnowAmbient + vAmbientColor + aDiffuseLight) * aProperties._Diffuse) * HdrRange;
		float3 specular = aSpecularLight;

		return diffuse + specular;
	}


	//-------------------------------
	// Debugging --------------------
	//-------------------------------
	//#define PDX_DEBUG_NORMAL
	//#define PDX_DEBUG_DIFFUSE
	//#define PDX_DEBUG_SPEC
	//#define PDX_DEBUG_GLOSSINESS
	//#define PDX_DEBUG_SHADOW
	//#define PDX_DEBUG_SUN_LIGHT
	//#define PDX_DEBUG_SUN_LIGHT_WITH_SHADOW
	//#define PDX_DEBUG_AMBIENT
	void DebugReturn(inout float3 aReturn, LightingProperties aProperties, float aShadowTerm)//
	{
	#ifdef PDX_DEBUG_NORMAL
		aReturn = saturate(aProperties._Normal);
	#endif

	#ifdef PDX_DEBUG_DIFFUSE
		aReturn = aProperties._Diffuse;
	#endif

	#ifdef PDX_DEBUG_SPEC
		aReturn = aProperties._SpecularColor;
	#endif

	#ifdef PDX_DEBUG_GLOSSINESS
		aReturn = vec3(aProperties._Glossiness);
	#endif

	#ifdef PDX_DEBUG_SHADOW
		aReturn = vec3(aShadowTerm);
	#endif

	#if defined(PDX_DEBUG_SUN_LIGHT) || defined (PDX_DEBUG_SUN_LIGHT_WITH_SHADOW)
		float3 diffuseLight = vec3(0.0);
		float3 specularLight = vec3(0.0);
		aProperties._SpecularColor = vec3(0);
		aProperties._Diffuse = vec3(0.5);
		
		#ifdef PDX_DEBUG_SUN_LIGHT_WITH_SHADOW
			CalculateSunLight(aProperties, aShadowTerm, diffuseLight, specularLight);
		#else
			CalculateSunLight(aProperties, 1.0, diffuseLight, specularLight);
		#endif
		
		aReturn = ComposeLight(aProperties, diffuseLight, specularLight);
	#endif

	#ifdef PDX_DEBUG_AMBIENT 
		float vDayNight = DayNightFactor( CalcGlobeNormal( aProperties._WorldSpacePos.xz ) );
		aReturn = AmbientLight(aProperties._Normal, vDayNight) * aProperties._Diffuse;
	#endif
	}

	float4 gradient_border_multisample_alpha( in float4 vCh, in sampler2D TexCh, in float2 vUV )
	{
	#ifdef LOW_END_GFX
		return vCh;
	#else
		float vOffsetX = -0.5f / MAP_SIZE_X;
		float vOffsetY = -0.5f / MAP_SIZE_Y;
		float4 vResult = vCh;
		vResult += tex2D( TexCh, vUV + float2( -vOffsetX, 0 ) );
		vResult += tex2D( TexCh, vUV + float2( 0, -vOffsetY ) );
		vResult += tex2D( TexCh, vUV + float2( vOffsetX, 0 ) );
		vResult += tex2D( TexCh, vUV + float2( 0, vOffsetY ) );
		vResult += tex2D( TexCh, vUV + float2( -vOffsetX, -vOffsetY ) );
		vResult += tex2D( TexCh, vUV + float2(  vOffsetX, -vOffsetY ) );
		vResult += tex2D( TexCh, vUV + float2(  vOffsetX,  vOffsetY ) );
		vResult += tex2D( TexCh, vUV + float2( -vOffsetX,  vOffsetY ) );
		vResult /= 9;
		return vResult;
		//return vCh;
	#endif
	}

	float gradient_border_camera_distance()
	{
		return 1.0f - clamp( cam_distance( GB_CAM_MIN, GB_CAM_MAX ), 0, GB_CAM_MAX_FILLING_CLAMP );
	}

	float gradient_border_distance_to_alpha( float vDist, float vCamDist )
	{
		vDist = 1.0f - vDist;
		vDist *= ( vCamDist - GB_THRESHOLD ) / ( GB_THRESHOLD2 );
		return 1.0f - saturate( vDist );
	}

	float CalculateBorderStripes( in float2 uv )
	{
		// diagonal
		float t = 3.14159 * 2 / 3;	    
		float w = BORDER_MAP_TILE;			  // larger value gives smaller width
		
		float stripeVal = cos( ( uv.x * cos( t ) * w ) + ( uv.y * sin( t ) * w ) ); 
		float camDist = cam_distance( 100.0, 200.0 );
		stripeVal += .75f + camDist;

		stripeVal = smoothstep(0.0, 1.0, stripeVal * 2 ) * lerp(1.0, 0.3, camDist);
		stripeVal = lerp ( lerp( -.03, .01, stripeVal ), 0.f, camDist );
		return stripeVal;
	}	
	
	float gradient_border_process_channel( out float3 vCh, float3 vInit, float vCamDist, float3 vNormal, float2 uv, in sampler2D gbTex, in sampler2D gbTex2, float vOutlineMult, float vOutlineCutoff, float vStrength )
	{
		vCh = vInit;

		const float PulseSpeedMult = 3.5f;
		float FX = tex2D( gbTex2, uv ).b;
		vStrength *= lerp( lerp( 0.45f, 1.0f, 1.0f - FX ), 1.0f, ( sin( vGlobalTime * PulseSpeedMult ) + 1.0f ) / 2 );

		float vFullWidth = 5.25f / 255.0f;//lerp( 5.25f, 0.01f, FX ) / 255.f;
		float vGradientWidth = 0.5f / 255.0f;//lerp( 0.5f, 0.1f, FX ) / 255.f;

		// Grab multisampled border color
		float4 vGBDist = gradient_border_multisample_alpha( tex2D( gbTex, uv ), gbTex, uv );

		float Alpha = vGBDist.a;

		// Check how much color and how much outline there is
		float vColorOpacity = Levels( Alpha, 0.0f, vOutlineCutoff );
		float vOutline = 1.0f - Levels( Alpha, vOutlineCutoff, 1.0f );
		float vOldOutline = vOutline;
		vOutline *= floor(vColorOpacity);
		vOutline *= vOutlineMult;

			
		// Convert "heightmap" to "fill" regarding camera distance (the whole magic in this function)
		vColorOpacity = gradient_border_distance_to_alpha( vColorOpacity, vCamDist );

		// Now when vOutline > 0 then vColorOpacity = 0, and other way around.
		// Never both values will be > 0.
		vColorOpacity *= floor(vOldOutline);
	

		float vThick = smoothstep( 0.f, 1.f, Levels( Alpha, vOutlineCutoff - vFullWidth, vOutlineCutoff - vFullWidth + vGradientWidth ) ) ;
		
		vThick *= floor(vOldOutline);

		float vMaxGradient = max( vColorOpacity, vOutline );

		vCh = lerp( vCh, vGBDist.rgb, max( vMaxGradient, vThick )* vStrength);

		// Compensate the brightness since the 2nd layer is now black (not white) although it's alpha is 0
		vCh *= 1.15f;
		vCh = min( vCh, float3( 1, 1, 1 ) );

		// Make the outline edge darker
		vCh = lerp( vCh, vCh * .5, vThick );

		return max( vMaxGradient, vThick );
	}

	void gradient_border_apply( inout float3 vColor, float3 vNormal, float2 vUV, 
		in sampler2D TexCh1, in sampler2D TexCh2, 
		float vOutlineMult, float2 vOutlineCutoff, float2 vCamDistOverride, inout float vBloomAlpha )
	{

	#ifndef GRADIENT_BORDERS
		vBloomAlpha = 1.0f;
		return;
	#endif

		// Check the distance of camera (value 0-1)
		float vGBCamDist = gradient_border_camera_distance();

		// Handle camera distance overriding (unique for each channel)
		float vGBCamDistCh1 = saturate( ( vGBCamDist * int( 1.0f - vCamDistOverride.x ) ) + vCamDistOverride.x );
		float vGBCamDistCh2 = saturate( ( vGBCamDist * int( 1.0f - vCamDistOverride.y ) ) + vCamDistOverride.y );

		// Split UV to correct offset in height, as 1st channel is the top half part of the texture, and 2nd channel is bottom half
		float HalfPix = 0.5f / GB_TextureHeight;
		vUV.y *= 0.5f - HalfPix;
		float2 vUV2 = float2( vUV.x, vUV.y + 0.5f );

		// Calculate color and transparency of both channels
		float3 vGradMix;
		
		float vAlpha1 = gradient_border_process_channel( vGradMix, vColor, vGBCamDistCh1, vNormal, vUV, TexCh1, TexCh2, vOutlineMult, vOutlineCutoff.x, GB_STRENGTH_CH1 );
		// Now mix, the resultat with background
		float TranspA = 1.0f - tex2D( TexCh2, vUV ).g;		
		vColor = lerp( vColor, vGradMix, ( GB_OPACITY_NEAR + ( 1.0f - vGBCamDist ) * ( GB_OPACITY_FAR - GB_OPACITY_NEAR ) ) * TranspA );
		
		
		float vAlpha2 = gradient_border_process_channel( vGradMix, vColor, vGBCamDistCh2, vNormal, vUV2, TexCh1, TexCh2, vOutlineMult, vOutlineCutoff.y, (1.0 - vAlpha1 * GB_STRENGTH_CH1 * GB_FIRST_LAYER_PRIORITY) * GB_STRENGTH_CH2 );
		float TranspB = 1.0f - tex2D( TexCh2, vUV2 ).g;
		vColor = lerp( vColor, vGradMix, ( GB_OPACITY_NEAR + ( 1.0f - vGBCamDist ) * ( GB_OPACITY_FAR - GB_OPACITY_NEAR ) ) * TranspB );
		
	//vColor = GetOverlay( vColor, ToLinear(vGradMix), 0.80);

		// Return some alpha, so the postprocess will ignore gradient borders
		// when applying season coloring overlay 
		// (we don't want to affect the colors especially when camera is zoomed out, and
		//  everything is 100% filled)
		vBloomAlpha = 1.0f - max( vAlpha1, vAlpha2 );
	}

	/*
	float gradient_border_process_channel( out float3 vCh, float3 vInit, float vCamDist, float3 vNormal, float2 uv, in sampler2D gbTex, float vOutlineMult, float vOutlineCutoff, float vStrength )
	{
		vCh = vInit;

		// Grab multisampled border color
		float4 vGBDist = gradient_border_multisample_alpha( tex2D( gbTex, uv ), gbTex, uv );
		// Check how much color and how much outline there is
		float vColorOpacity = Levels( vGBDist.a, 0.0f, vOutlineCutoff );
		float vOutline = 1.0f - Levels( vGBDist.a, vOutlineCutoff, 1.0f );
		float vOldOutline = vOutline;
		vOutline *= floor(vColorOpacity);
		vOutline *= vOutlineMult;

			
		// Convert "heightmap" to "fill" regarding camera distance (the whole magic in this function)
		vColorOpacity = gradient_border_distance_to_alpha( vColorOpacity, vCamDist );

		// Now when vOutline > 0 then vColorOpacity = 0, and other way around.
		// Never both values will be > 0.
		vColorOpacity *= floor(vOldOutline);
	
		float vFullWidth = 2.25f / 255.f;
		float vGradientWidth = .5f / 255.f;

		float vThick = smoothstep( 0.f, 1.f, Levels( vGBDist.a, vOutlineCutoff - vFullWidth, vOutlineCutoff - vFullWidth + vGradientWidth ) ) ;
		//vThick *= floor(vOldOutline);
		float vMaxGradient = max( vColorOpacity, vOutline );
		vCh = lerp( vCh, vGBDist.rgb,vMaxGradient* vStrength);
		vCh = lerp( vCh, vCh * .5, vThick );
	
		return max( vMaxGradient * 0.5, vThick );
	}
	*/
	
	float CalculateOccupationMask( in float2 uv )
	{
		// diagonal
		float t = 3.14159 / 8.0;	    
		float w = SEC_MAP_TILE;			  // larger value gives smaller width
		
		float stripeVal = cos( ( uv.x * cos( t ) * w ) + ( uv.y * sin( t ) * w ) ); 
		float camDist = cam_distance( 300.0, 1200.0 );
		stripeVal += camDist * 1.5;

		stripeVal = smoothstep(0.0, 1.0, stripeVal*1.7) * lerp(1.0, 0.3, camDist);
		return stripeVal;
	}	
	
	void secondary_color_mask( inout float3 vColor, float3 vNormal, float2 vUV, in sampler2D TexMaskSampler, inout float vBloomAlpha )
	{
		float4 vColorMask = tex2D( TexMaskSampler, vUV ).rgba;

		float vOccupationMask = CalculateOccupationMask( vUV );
		vOccupationMask *= vColorMask.a;
		vBloomAlpha = vBloomAlpha * ( 1.0f - vOccupationMask );
		vColor = lerp( vColor, vColorMask.rgb, vOccupationMask );
	}

	// Taken out from pdxmap.lua so other shaders can have access to it
	void calculate_map_tex_index( float4 IDs, out float4 IndexU, out float4 IndexV, out float vAllSame )
	{
		IDs *= 255.0f;
		vAllSame = saturate( IDs.z - 98.0f ); // we've added 100 to first if all IDs are same
		IDs.z -= vAllSame * 100.0f;

		IndexV = trunc( ( IDs + 0.5f ) / MAP_NUM_TILES );
		IndexU = trunc( IDs - ( IndexV * MAP_NUM_TILES ) + 0.5f );
	}

	/*float calculate_water_or_land( float4 IDs )
	{
		IDs *= 255.0f;
		float vAllSame = saturate( IDs.z - 98.0f ); // we've added 100 to first if all IDs are same
		IDs.z -= vAllSame * 100.0f;
		IDs.x = Levels( IDs.x, 64.0f, 255.0f );
		IDs.y = Levels( IDs.y, 64.0f, 255.0f );
		IDs.z = Levels( IDs.z, 64.0f, 255.0f );
		IDs.w = Levels( IDs.w, 64.0f, 255.0f );
		return ( IDs.x + IDs.y + IDs.z + IDs.w ) * 0.25f;
	}*/

	/*float calculate_water_or_land_mutilsample( in sampler2D TerrainId, in float2 vUV )
	{
		float vOffsetX = -0.5f / MAP_SIZE_X;
		float vOffsetY = -0.5f / MAP_SIZE_Y;
		float vValue = calculate_water_or_land( tex2D( TerrainId, vUV ) );
		vValue += calculate_water_or_land( tex2D( TerrainId, vUV + float2( -vOffsetX, 0 ) ) );
		vValue += calculate_water_or_land( tex2D( TerrainId, vUV + float2(  vOffsetX, 0 ) ) );
		vValue += calculate_water_or_land( tex2D( TerrainId, vUV + float2( 0, -vOffsetY ) ) );
		vValue += calculate_water_or_land( tex2D( TerrainId, vUV + float2( 0,  vOffsetY ) ) );
		return saturate( vValue / 5 );
	}*/

	float mipmapLevel( float2 uv )
	{
	#ifdef PDX_OPENGL

	#ifdef NO_SHADER_TEXTURE_LOD
		return 1.0f;
	#else

	#ifdef	PIXEL_SHADER
		float dx = fwidth( uv.x * TEXELS_PER_TILE );
		float dy = fwidth( uv.y * TEXELS_PER_TILE );
	    float d = max( dot(dx, dx), dot(dy, dy) );
		return 0.5 * log2( d );
	#else
		return 3.0f;
	#endif //PIXEL_SHADER

	#endif // NO_SHADER_TEXTURE_LOD

	#else
	    float2 dx = ddx( uv * TEXELS_PER_TILE );
	    float2 dy = ddy( uv * TEXELS_PER_TILE );
	    float d = max( dot(dx, dx), dot(dy, dy) );
	    return 0.5f * log2( d );
	#endif //PDX_OPENGL
	}

	float4 sample_terrain( float IndexU, float IndexV, float2 vTileRepeat, float vMipTexels, float lod )
	{
		vTileRepeat = frac( vTileRepeat );
	#ifdef NO_SHADER_TEXTURE_LOD
		vTileRepeat *= 0.96;
		vTileRepeat += 0.02;
	#endif
		
		float vTexelsPerTile = vMipTexels / MAP_NUM_TILES;

		vTileRepeat *= ( vTexelsPerTile - 1.0f ) / vTexelsPerTile;
		return float4( ( float2( IndexU, IndexV ) + vTileRepeat ) / MAP_NUM_TILES + 0.5f / vMipTexels, 0.0f, lod );
	}

	float3 CalcWaterNormal( float2 uv, float vSpeed, in sampler2D NoiseSampler )
	{
		float2 time1 = vSpeed * float2( 0.3f, 0.7f ) * 2.0f;
		float2 uv1 = uv * 250.f;
		
		float2 time2 = vSpeed * float2( -0.6f, 0.45f ) * 2.0f;
		float2 uv2 = uv * 190.f;

		float2 time3 = vSpeed * float2( 0.3f, -0.7f ) * 2.0f;
		float2 uv3 = uv * 80.f;

		float2 time4 = vSpeed * float2( -0.2f, 0.5f ) * 3.75f;
		float2 uv4 = uv * 160.f;

		float3 noiseNormal1 = normalize( tex2D( NoiseSampler, uv1 + time1 ).rbg - 0.5f );
		float3 noiseNormal2 = normalize( tex2D( NoiseSampler, uv2 + time2 ).rbg - 0.5f );
		float3 noiseNormal3 = normalize( ( tex2D( NoiseSampler, uv3 + time3 ).rbg - 0.5f ) * float3( 1, 4, 1 ) );
		float3 noiseNormal4 = normalize( ( tex2D( NoiseSampler, uv4 + time4 ).rbg - 0.5f ) * float3( 1, 4, 1 ) );

		float3 normalNoise = lerp( noiseNormal1 + noiseNormal2, noiseNormal3 + noiseNormal4, saturate( vCamPos.y / 500.0f ) );
		//normalNoise = noiseNormal4;
		return normalize( normalNoise );
	}


	void BlendLEAN( float t, float2 B1, float3 M1, float2 B2, float3 M2, out float2 Bout, out float3 Mout )
	{
		float u = t;
		t = 1.0f - t;
		float t2 = t * t;
		float u2 = u * u;

		Bout = B1 * t + B2 * u;

		Mout.x = M1.x*t2 + M2.x*u2 + 2*t*u*B1.x*B2.x;
		Mout.y = M1.y*t2 + M2.y*u2 + 2*t*u*B1.y*B2.y;
		Mout.z = M1.z*t2 + M2.z*u2 + t*u*B1.x*B2.y + t*u*B1.y*B2.x;
	}

	void SampleLEAN( float2 uv, out float2 Bout, out float3 Mout, in sampler2D LeanTexture1Sampler, in sampler2D LeanTexture2Sampler )
	{
		float4 lean1 = tex2D( LeanTexture1Sampler, uv );
		float4 lean2 = tex2D( LeanTexture2Sampler, uv );

		float vScale = 1.7f;
		Bout = ( 2*lean2.xy - 1 ) * vScale;
		Mout = float3( lean2.zw, ( 2*lean1.w - 1 ) * 0.5) * vScale * vScale;
	}

	void SampleBlendLEAN( float t, float2 uv1, float2 uv2, out float2 Bout, out float3 Mout, in sampler2D Lean1, in sampler2D Lean2 )
	{
		float2 B1, B2;
		float3 M1, M2;

		SampleLEAN( uv1, B1, M1, Lean1, Lean2 );
		SampleLEAN( uv2, B2, M2, Lean1, Lean2 );

		BlendLEAN( t, B1, M1, B2, M2, Bout, Mout );
	}

	void SampleWater( float2 uv, float2 vUVMultipliers[4], float vTime, float2 vTimeMultipliers[4], out float2 B, out float3 M, out float3 normal, in sampler2D Lean1, in sampler2D Lean2 )
	{
		float2 B1;
		float2 B2;
		float3 M1;
		float3 M2;

		SampleBlendLEAN( 0.5f,
			uv * vUVMultipliers[0] + vTime * vTimeMultipliers[0],
			uv * vUVMultipliers[1] + vTime * vTimeMultipliers[1],
			B1, M1, Lean1, Lean2 );

		SampleBlendLEAN( 0.5f, 
			uv * vUVMultipliers[2] + vTime * vTimeMultipliers[2],
			uv * vUVMultipliers[3] + vTime * vTimeMultipliers[3],
			B2, M2, Lean1, Lean2 );

		BlendLEAN( 0.5f, B1, M1, B2, M2, B, M );

		normal = float3( B.x, 1.0f, B.y );

		// because sometimes, normalize() crashes the compiler(and with sometimes, I mean always)
		float vMultiplier = 1.0f / sqrt( normal.x * normal.x + normal.y * normal.y + normal.z * normal.z );
		normal *= vMultiplier;
	}

	void SampleWater( float2 uv, float vTime, out float2 B, out float3 M, out float3 normal, in sampler2D Lean1, in sampler2D Lean2 )
	{
		float2 vUVMultipliers[4];
		vUVMultipliers[0] = 1000.0f * float2( 0.9f, 1.0f );
		vUVMultipliers[1] = 700.0f * float2( 0.95f, 1.05f );
		vUVMultipliers[2] = 534.0f * float2( 1.05f, 0.95f );
		vUVMultipliers[3] = 300.0f * float2( 1.0f, 1.0f );

		float2 vTimeMultipliers[4];
		vTimeMultipliers[0] = float2( 1.0f, 0.1f );
		vTimeMultipliers[1] = float2( 0.1f, 2.0f );
		vTimeMultipliers[2] = float2( -0.2f, -2.0f );
		vTimeMultipliers[3] = float2( -1.0f, -0.1f );

		SampleWater( uv, vUVMultipliers, vTime * WATER_TIME_SCALE, vTimeMultipliers, B, M, normal, Lean1, Lean2 );
	}

	void SampleWater( float2 uv, float vTime, out float3 normal, in sampler2D Lean1, in sampler2D Lean2 )
	{
		float2 B;
		float3 M;
		SampleWater( uv, vTime, B, M, normal, Lean1, Lean2 );
	}	
	]]

}

