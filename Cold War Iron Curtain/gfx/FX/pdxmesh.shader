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
			#MipMapLodBias = -1.0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SpecularMap =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		NormalMap =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		FlagMap =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SnowMudData =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		IntelMap =
		{
			Index = 5
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		FOWNoise =
		{
			Index = 6
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		EnvironmentMap =
		{
			Index = 7
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
			Type = "Cube"
		}
		LightIndexMap =
		{
			Index = 8
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		LightDataMap =
		{
			Index = 9
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		GradientBorderChannel1 =
		{
			Index = 10
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		GradientBorderChannel2 =
		{
			Index = 11
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}	
		ProvinceSecondaryColorMap =
		{
			Index = 12
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		FOWHeight =
		{
			Index = 13
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT_PDXMESHSTANDARD
{
    float3 vPosition		: POSITION;
	float3 vNormal      	: TEXCOORD0;
	float4 vTangent			: TEXCOORD1;
	float2 vUV0				: TEXCOORD2;
	float2 vUV1				: TEXCOORD3;
};

VertexStruct VS_INPUT_PDXMESHSTANDARD_SKINNED
{
    float3 vPosition		: POSITION;
	float3 vNormal      	: TEXCOORD0;
	float4 vTangent			: TEXCOORD1;
	float2 vUV0				: TEXCOORD2;
	float2 vUV1				: TEXCOORD3;
	uint4 vBoneIndex 		: TEXCOORD4;
	float3 vBoneWeight		: TEXCOORD5;
};

VertexStruct VS_OUTPUT_PDXMESHSTANDARD
{
    float4 vPosition	: PDX_POSITION;
	float3 vNormal		: TEXCOORD0;
	float3 vTangent		: TEXCOORD1;
	float3 vBitangent	: TEXCOORD2;
	float2 vUV0			: TEXCOORD3;
	float2 vUV1			: TEXCOORD4;
	float4 vPos_Height	: TEXCOORD5;
};

VertexStruct VS_OUTPUT_PDXMESHSHADOW
{
    float4 vPosition	: PDX_POSITION;
	float4 vDepthUV0	: TEXCOORD0;
};

VertexStruct VS_INPUT_DEBUGNORMAL
{
    float3 vPosition		: POSITION;
	float3 vNormal      	: TEXCOORD0;
	float4 vTangent			: TEXCOORD1;
	float2 vUV0				: TEXCOORD2;
	float2 vUV1				: TEXCOORD3;
	float  vOffset      	: TEXCOORD6;
};

VertexStruct VS_INPUT_DEBUGNORMAL_SKINNED
{
    float3 vPosition		: POSITION;
	float3 vNormal      	: TEXCOORD0;
	float4 vTangent			: TEXCOORD1;
	float2 vUV0				: TEXCOORD2;
	float2 vUV1				: TEXCOORD3;
	uint4 vBoneIndex		: TEXCOORD4;
	float3 vBoneWeight		: TEXCOORD5;
	float  vOffset      	: TEXCOORD6;
};

VertexStruct VS_OUTPUT_DEBUGNORMAL
{
    float4 vPosition : PDX_POSITION;
	float2 vUV0		 : TEXCOORD0;
	float  vOffset	 : TEXCOORD1;
};


ConstantBuffer( 1, 28 )
{
	float4x4 WorldMatrix;
	float4 AtlasCoordinate;
	float vUVAnimSpeed;
};


ConstantBuffer( 2, 41 )
{
	float4x4 matBones[50]; // : Bones :register( c41 ); // 50 * 4 registers 41 - 241 
};


Code
[[

static const int PDXMESH_MAX_INFLUENCE = 4;

]]


VertexShader =
{
	MainCode VertexPdxMeshStandard
	[[
		
		VS_OUTPUT_PDXMESHSTANDARD main( const VS_INPUT_PDXMESHSTANDARD v )
		{
		  	VS_OUTPUT_PDXMESHSTANDARD Out;
					
			float4 vPosition = float4( v.vPosition.xyz, 1.0f );
			Out.vNormal = normalize( mul( CastTo3x3( WorldMatrix ), v.vNormal ) );
			Out.vTangent = normalize( mul( CastTo3x3( WorldMatrix ), v.vTangent.xyz ) );
			Out.vBitangent = normalize( cross( Out.vNormal, Out.vTangent ) * v.vTangent.w );
		
			Out.vPosition = mul( WorldMatrix, vPosition );
			Out.vPos_Height.xyz = Out.vPosition.xyz;
			Out.vPos_Height.w = v.vPosition.y;
			Out.vPos_Height /= WorldMatrix[3][3];
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );
			
			Out.vUV0 = v.vUV0;
			Out.vUV1 = v.vUV1;
			
			return Out;
		}
	]]

	MainCode VertexPdxMeshStandardSkinned
	[[
		
		VS_OUTPUT_PDXMESHSTANDARD main( const VS_INPUT_PDXMESHSTANDARD_SKINNED v )
		{
		  	VS_OUTPUT_PDXMESHSTANDARD Out;
					
			float4 vPosition = float4( v.vPosition.xyz, 1.0 );
			float4 vSkinnedPosition = float4( 0, 0, 0, 0 );
			float3 vSkinnedNormal = float3( 0, 0, 0 );
			float3 vSkinnedTangent = float3( 0, 0, 0 );
			float3 vSkinnedBitangent = float3( 0, 0, 0 );
		
			float4 vWeight = float4( v.vBoneWeight.xyz, 1.0f - v.vBoneWeight.x - v.vBoneWeight.y - v.vBoneWeight.z );
		
			for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
		    {
				int nIndex = int( v.vBoneIndex[i] );
				float4x4 mat = matBones[nIndex];
				vSkinnedPosition += mul( mat, vPosition ) * vWeight[i];
		
				float3 vNormal = mul( CastTo3x3(mat), v.vNormal );
				float3 vTangent = mul( CastTo3x3(mat), v.vTangent.xyz );
				float3 vBitangent = cross( vNormal, vTangent ) * v.vTangent.w;
		
				vSkinnedNormal += vNormal * vWeight[i];
				vSkinnedTangent += vTangent * vWeight[i];
				vSkinnedBitangent += vBitangent * vWeight[i];
			}
		
			Out.vPosition = mul( WorldMatrix, vSkinnedPosition );
			Out.vPos_Height.xyz = Out.vPosition.xyz;
			Out.vPos_Height.w = vSkinnedPosition.y;
			Out.vPos_Height /= WorldMatrix[3][3];
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );
		
			Out.vNormal = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedNormal ) ) );
			Out.vTangent = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedTangent ) ) );
			Out.vBitangent = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedBitangent ) ) );
		
			Out.vUV0 = v.vUV0;
			Out.vUV1 = v.vUV1;
			
			return Out;
		}
	]]

	MainCode VertexPdxMeshStandardShadow
	[[
		
		VS_OUTPUT_PDXMESHSHADOW main( const VS_INPUT_PDXMESHSTANDARD v )
		{
		  	VS_OUTPUT_PDXMESHSHADOW Out;
			float4 vPosition = float4( v.vPosition.xyz, 1.0 );
			Out.vPosition = mul( WorldMatrix, vPosition );
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );
			Out.vDepthUV0 = float4( Out.vPosition.zw, v.vUV0 );
			return Out;
		}
	]]

	MainCode VertexPdxMeshStandardSkinnedShadow
	[[
	
		VS_OUTPUT_PDXMESHSHADOW main( const VS_INPUT_PDXMESHSTANDARD_SKINNED v )
		{
		  	VS_OUTPUT_PDXMESHSHADOW Out;
					
			float4 vPosition = float4( v.vPosition.xyz, 1.0 );
			float4 vSkinnedPosition = float4( 0, 0, 0, 0 );
		
			float4 vWeight = float4( v.vBoneWeight.xyz, 1.0f - v.vBoneWeight.x - v.vBoneWeight.y - v.vBoneWeight.z );
		
			for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
		    {
				int nIndex = int( v.vBoneIndex[i] );
				float4x4 mat = matBones[nIndex];
				vSkinnedPosition += mul( mat, vPosition ) * vWeight[i];
			}
		
			Out.vPosition = mul( WorldMatrix, vSkinnedPosition );
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );
			Out.vDepthUV0 = float4( Out.vPosition.zw, v.vUV0 );
			return Out;
		}
	]]

	MainCode VertexDebugNormal
	[[
		
		VS_OUTPUT_DEBUGNORMAL main( const VS_INPUT_DEBUGNORMAL v )
		{
		  	VS_OUTPUT_DEBUGNORMAL Out;
		
			Out.vPosition = mul( WorldMatrix, float4( v.vPosition.xyz, 1.0 ) );
			Out.vPosition.xyz += mul( CastTo3x3(WorldMatrix), v.vNormal ) * v.vOffset * 0.3f;
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );	
		
			Out.vUV0 = v.vUV0;
			Out.vOffset = v.vOffset; 
		
			return Out;
		}
	]]

	MainCode VertexDebugNormalSkinned
	[[
		
		VS_OUTPUT_DEBUGNORMAL main( const VS_INPUT_DEBUGNORMAL_SKINNED v )
		{
		  	VS_OUTPUT_DEBUGNORMAL Out;
					
			float4 vPosition = float4( v.vPosition.xyz, 1.0 );
			float4 vSkinnedPosition = float4( 0, 0, 0, 0 );
			float3 vSkinnedNormal = float3( 0, 0, 0 );
		
			float4 vWeight = float4( v.vBoneWeight.xyz, 1.0f - v.vBoneWeight.x - v.vBoneWeight.y - v.vBoneWeight.z );
		
			for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
		    {
				int nIndex = int( v.vBoneIndex[i] );
				float4x4 mat = matBones[nIndex];
				vSkinnedPosition += mul( mat, vPosition ) * vWeight[i];	
				vSkinnedNormal += mul( CastTo3x3(mat), v.vNormal ) * vWeight[i];
			}
		
			Out.vPosition = mul( WorldMatrix, vSkinnedPosition );
			vSkinnedNormal = normalize( mul( CastTo3x3(WorldMatrix), vSkinnedNormal ) );
			Out.vPosition.xyz += vSkinnedNormal * v.vOffset * 0.3f * WorldMatrix[ 3 ][ 3 ];
			Out.vPosition = mul( ViewProjectionMatrix, Out.vPosition );	
		
			Out.vUV0 = v.vUV0;
			Out.vOffset = v.vOffset; 
			return Out;
		}
	]]
}

PixelShader =
{

	MainCode PixelPdxMeshStandard
	[[
		float3 ApplySnowMesh( float3 vColor, float3 vPos, inout float3 vNormal, float4 vFoWColor, out float vSnowAlpha )
		{
			float vIsSnow = GetSnow( vFoWColor );
			float vSnowFade = saturate( saturate( vNormal.y - saturate( 1.0f - vIsSnow ) )*vIsSnow*5.5f*saturate( ( vNormal.y - 0.5f ) * 1000.0f ) );
						
			float vOpacity = cam_distance( SNOW_CAM_MIN, SNOW_CAM_MAX );
			vOpacity = SNOW_OPACITY_MIN + vOpacity * ( SNOW_OPACITY_MAX - SNOW_OPACITY_MIN );
			
			vColor = lerp( vColor, SNOW_COLOR, vSnowFade * vOpacity );
			vSnowAlpha = saturate( vIsSnow * 1.5f ) * vOpacity;
			
			//vNormal.y += 0.5f * vSnowFade;
			//vNormal = normalize( vNormal );
			
			return vColor;
		}

		float4 main( VS_OUTPUT_PDXMESHSTANDARD In ) : PDX_COLOR
		{
			float2 vUV0 = In.vUV0;

		#ifdef UV_ANIM
			const float SPEED_SCALE = 2.0f;
			float t = frac(vGlobalTime * vUVAnimSpeed * SPEED_SCALE);
			vUV0.y += t;
		#endif
		
		#ifdef ATLAS
			float4 vDiffuse = tex2D( DiffuseMap, (vUV0 + AtlasCoordinate.xy) / AtlasCoordinate.zw );
		#else
			float4 vDiffuse = tex2D( DiffuseMap, vUV0 );
		#endif	

		#ifdef ALPHA_TEST
			clip(vDiffuse.a - 1.0);
		#endif
		
			float3 vPos = In.vPos_Height.xyz;
		
			float3 vColor = vDiffuse.rgb;
			float3 vInNormal = normalize( In.vNormal );
			float4 vProperties = tex2D( SpecularMap, vUV0 );
			
			LightingProperties lightingProperties;
			
		#ifdef PDX_IMPROVED_BLINN_PHONG
			float4 vNormalMap = tex2D( NormalMap, vUV0 );
			
			#ifdef EMISSIVE
				float vEmissive = vNormalMap.b;
			#endif
			float3 vNormalSample =  UnpackRRxGNormal(vNormalMap);
			
			lightingProperties._Glossiness = vProperties.a;
		#else
			#ifdef EMISSIVE
				float vEmissive = vProperties.b;
			#endif
			float3 vNormalSample = UnpackNormal( NormalMap, vUV0 );
			
			lightingProperties._SpecularColor = vec3(vProperties.a);
			#ifdef GLOSSINESS
				lightingProperties._Glossiness = vProperties.g * 2048.0 * vProperties.g + 0.00001; // Small epsilon to avoid 0^0
			#else
				lightingProperties._Glossiness = SPECULAR_WIDTH;
			#endif
		#endif
		
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(lightingProperties._Glossiness);
		
			float3x3 TBN = Create3x3( normalize( In.vTangent ), normalize( In.vBitangent ), vInNormal );
			float3 vNormal = normalize(mul( vNormalSample, TBN ));
			
			// self shadowing
			float fShadowTerm = 1.0f;//CalculateShadowCascaded(vPos, ShadowMap);
			//fShadowTerm = (1.0f - SHADOW_WEIGHT_MESH) + SHADOW_WEIGHT_MESH * fShadowTerm;

			float vSnowAlpha = 0;
		#ifdef PDX_SNOW
			float4 vFoWColor = GetMudSnowColor( vPos, SnowMudData );
			vColor = ApplySnowMesh( vColor, vPos, vNormal, vFoWColor, vSnowAlpha );	
		#endif

		#ifdef PDX_GRADIENT_BORDERS
			// Gradient Borders
			float2 map_uv = float2( ( ( vPos.x+0.5f ) / MAP_SIZE_X ), ( ( vPos.z+0.5f-MAP_SIZE_Y ) / -MAP_SIZE_Y ));
			
			float vBloomAlpha = 0.0f;
			gradient_border_apply( vColor.rgb, vNormal, map_uv, GradientBorderChannel1, GradientBorderChannel2, 1.0f, vGBCamDistOverride_GBOutlineCutoff.zw, vGBCamDistOverride_GBOutlineCutoff.xy, vBloomAlpha );

			// Secondary color mask
			secondary_color_mask( vColor.rgb, vNormal, map_uv, ProvinceSecondaryColorMap, vBloomAlpha );	
		#endif
		
			lightingProperties._WorldSpacePos = vPos;
			lightingProperties._ToCameraDir = normalize(vCamPos - vPos);
			lightingProperties._Normal = vNormal;

		#ifdef PDX_IMPROVED_BLINN_PHONG
			float SpecRemapped = vProperties.g * vProperties.g * 0.4;
			float MetalnessRemapped = 1.0 - (1.0 - vProperties.b) * (1.0 - vProperties.b);
			lightingProperties._Diffuse = MetalnessToDiffuse(MetalnessRemapped, vColor);
			lightingProperties._SpecularColor = MetalnessToSpec(MetalnessRemapped, vColor, SpecRemapped);
		#else
			lightingProperties._Diffuse = vColor;
		#endif
			
			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);
			CalculateSunLight(lightingProperties, fShadowTerm, diffuseLight, specularLight);
			CalculatePointLights(lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);
		
		#ifdef PDX_IMPROVED_BLINN_PHONG
			float3 vEyeDir = normalize( vPos - vCamPos.xyz );
			float3 reflection = reflect( vEyeDir, vNormal );
			float MipmapIndex = GetEnvmapMipLevel(lightingProperties._Glossiness); 
			
			float3 reflectiveColor = texCUBElod( EnvironmentMap, float4(reflection, MipmapIndex) ).rgb * CubemapIntensity;
			specularLight += reflectiveColor * FresnelGlossy(lightingProperties._SpecularColor, -vEyeDir, lightingProperties._Normal, lightingProperties._Glossiness);
		#endif
		
		#ifdef PDX_SNOW
			vColor = ComposeLightSnow(lightingProperties, diffuseLight, specularLight, vSnowAlpha);
		#else
			vColor = ComposeLightMesh(lightingProperties, diffuseLight, specularLight, vSnowAlpha);
		#endif

			float3 vGlobalNormal = CalcGlobeNormal( vPos.xz );

			float alpha = 0.0f;
		#ifdef EMISSIVE
			float vDayNightFactor = DayNightFactor( vGlobalNormal );
			vEmissive = vEmissive * vDayNightFactor;
			//vColor = lerp( vColor, float3(1,0.7,0), vEmissive * vDayNightFactor );	
			vColor = lerp( vColor, vDiffuse.rgb, vEmissive );
			alpha = vEmissive;
		#endif
		
			float FogColorFactor = 0.0;
			float FogAlphaFactor = 0.0;
			GetFogFactors( FogColorFactor, FogAlphaFactor, vPos, 0.0 /*In.vPos_Height.w * 1.0 + 2.5*/, FOWNoise, FOWHeight, IntelMap);
			vColor = ApplyFOW( vColor, FogColorFactor, min( FogAlphaFactor, NegFogMultiplier ) );

			vColor.rgb = ApplyDistanceFog( vColor.rgb, vPos );			
			vColor.rgb = DayNight( vColor.rgb, vGlobalNormal );

/*		#ifdef RIM_LIGHT
			float vRim = smoothstep( RIM_START, RIM_END, 1.0f - dot( vInNormal, lightingProperties._ToCameraDir ) );
			vColor.rgb = lerp( vColor.rgb, RIM_COLOR.rgb, vRim );
		#endif	
*/			

			DebugReturn(vColor, lightingProperties, fShadowTerm);
			return float4(vColor, max(alpha, MinMeshAlpha));
		}
	]]
	
	MainCode PixelPdxMeshBorder
	[[
	
		float4 main( VS_OUTPUT_PDXMESHSTANDARD In ) : PDX_COLOR
		{
			float4 vDiffuse = tex2D( DiffuseMap, In.vUV0 );
			
		#ifdef ALPHA_TEST
			clip(vDiffuse.a - 1.0);
		#endif
			
			float3 vPos = In.vPos_Height.xyz;
		
			float3 vColor = vDiffuse.rgb;
			float4 vProperties = tex2D( SpecularMap, In.vUV0 );
			
			float4 vNormalMap = tex2D( NormalMap, In.vUV0 );
			float3 vNormalSample = UnpackRRxGNormal(vNormalMap);
			
			LightingProperties lightingProperties;
			lightingProperties._Glossiness = vProperties.a;
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(lightingProperties._Glossiness);
		
			float3 vInNormal = normalize( In.vNormal );
			float3x3 TBN = Create3x3( normalize( In.vTangent ), normalize( In.vBitangent ), vInNormal );
			float3 vNormal = normalize( mul( vNormalSample, TBN ) );

			lightingProperties._WorldSpacePos = vPos;
			lightingProperties._ToCameraDir = normalize(vCamPos - vPos);
			lightingProperties._Normal = vNormal;

			float SpecRemapped = vProperties.g * vProperties.g * 0.4;
			float MetalnessRemapped = 1.0 - (1.0 - vProperties.b) * (1.0 - vProperties.b);
			lightingProperties._Diffuse = MetalnessToDiffuse(MetalnessRemapped, vColor);
			lightingProperties._SpecularColor = MetalnessToSpec(MetalnessRemapped, vColor, SpecRemapped);
			
			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);
			ImprovedBlinnPhong(BORDER_SUN_INTENSITY, normalize(BORDER_SUN_DIRECTION), lightingProperties, diffuseLight, specularLight);
		
			//float3 vEyeDir = normalize( vPos - vCamPos.xyz );
			//float3 reflection = reflect( vEyeDir, vNormal );
			//float MipmapIndex = GetEnvmapMipLevel(lightingProperties._Glossiness); 
			
			//float3 reflectiveColor = texCUBElod( EnvironmentMap, float4(reflection, MipmapIndex) ).rgb * CubemapIntensity;
			//specularLight += reflectiveColor * FresnelGlossy(lightingProperties._SpecularColor, -vEyeDir, lightingProperties._Normal, lightingProperties._Glossiness);
		
			float3 DayAmbientColors[6];
			DayAmbientColors[0] = AmbientPosX;
			DayAmbientColors[1] = AmbientNegX;
			DayAmbientColors[2] = AmbientPosY;
			DayAmbientColors[3] = AmbientNegY;
			DayAmbientColors[4] = AmbientPosZ;
			DayAmbientColors[5] = AmbientNegZ;
		
			float3 vAmbientColor = AmbientLight(lightingProperties._Normal, 0.0, DayAmbientColors, DayAmbientColors);
			float3 diffuse = ((vAmbientColor + diffuseLight) * lightingProperties._Diffuse) * HdrRange;
			vColor = diffuse + specularLight;

			//vColor.rgb = ApplyDistanceFog( vColor.rgb, vPos );			
			
			return float4( vColor, 0 );
		}
	]]

	MainCode PixelPdxMeshStandardShadow
	[[
			
		float4 main( VS_OUTPUT_PDXMESHSHADOW In ) : PDX_COLOR
		{
			return float4( In.vDepthUV0.xxx / In.vDepthUV0.y, 1.0f );
		}
	]]

	MainCode PixelPdxMeshNoShadow
	[[
			
		float4 main( VS_OUTPUT_PDXMESHSHADOW In ) : PDX_COLOR
		{
			clip( -1.f );
			return float4( 1,1,1,1 );
		}
	]]

	MainCode PixelPdxMeshAlphaBlendShadow
	[[
			
		float4 main( VS_OUTPUT_PDXMESHSHADOW In ) : PDX_COLOR
		{
			float4 vColor = tex2D( DiffuseMap, In.vDepthUV0.zw );
			clip( vColor.a - 0.5f );
			return float4( In.vDepthUV0.xxx / In.vDepthUV0.y, 1.0f );
		}
	]]

	MainCode PixelDebugNormal
	[[
			
		float4 main( VS_OUTPUT_DEBUGNORMAL In ) : PDX_COLOR
		{
			float4 vColor = float4( 1.0f - In.vOffset, In.vOffset, 0.0f,  1.0f );
			return vColor;
		}
	]]
}


BlendState BlendState
{
	BlendEnable = no
	AlphaTest = no
}

BlendState BlendStateAlphaTest
{
	BlendEnable = no
	AlphaTest = yes
}


Effect PdxMeshStandard
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
}

Effect PdxMeshStandardSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
}

Effect PdxMeshStandardShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}

Effect PdxMeshStandardSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshStandardSnow
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "PDX_GRADIENT_BORDERS" }
}

Effect PdxMeshStandardSnowShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshAdvanced
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" "RIM_LIGHT" }
}

Effect PdxMeshAdvancedSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" "ATLAS" "RIM_LIGHT"  }
}

Effect PdxMeshAdvancedShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}

Effect PdxMeshAdvancedSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshAdvancedSnow
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" "RIM_LIGHT" "PDX_SNOW" "PDX_GRADIENT_BORDERS" }
}

Effect PdxMeshAdvancedSnowSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" "ATLAS" "PDX_SNOW" "RIM_LIGHT"  }
}

Effect PdxMeshAdvancedSnowShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}

Effect PdxMeshAdvancedSnowSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshAdvancedSkinnedAlphaTest
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "ALPHA_TEST" "ADD_COLOR" "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" }
}

Effect PdxMeshAdvancedSkinnedAlphaTestShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
	Defines = { "ALPHA_TEST" }
}


Effect PdxMeshAdvancedAnimSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "EMISSIVE" "PDX_IMPROVED_BLINN_PHONG" "UV_ANIM" "RIM_LIGHT" }
}

Effect PdxMeshAdvancedAnimSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshAlphaBlend
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
	BlendState = "BlendStateAlphaTest"
}

Effect PdxMeshAlphaBlendSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	BlendState = "BlendStateAlphaTest"
}

Effect PdxMeshAlphaBlendShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
}

Effect PdxMeshAlphaBlendSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
}


Effect PdxMeshSnow
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "PDX_SNOW" "PDX_IMPROVED_BLINN_PHONG" "EMISSIVE" "RIM_LIGHT" "PDX_GRADIENT_BORDERS" }
}

Effect PdxMeshSnowSkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
	Defines = { "PDX_SNOW" }
}

Effect PdxMeshSnowShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}

Effect PdxMeshSnowSkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}


Effect PdxMeshBorder
{
	VertexShader = "VertexPdxMeshStandard"
	PixelShader = "PixelPdxMeshBorder"
	Defines = { "ALPHA_TEST" }
}

Effect PdxMeshBorderShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshNoShadow"
}


Effect DebugNormal
{
	VertexShader = "VertexDebugNormal"
	PixelShader = "PixelDebugNormal"
}

Effect DebugNormalSkinned
{
	VertexShader = "VertexDebugNormalSkinned"
	PixelShader = "PixelDebugNormal"
}

Effect PdxMeshStandard_NoFoW_NoTISkinned
{
	VertexShader = "VertexPdxMeshStandardSkinned"
	PixelShader = "PixelPdxMeshStandard"
}

Effect PdxMeshStandard_NoFoW_NoTISkinnedShadow
{
	VertexShader = "VertexPdxMeshStandardSkinnedShadow"
	PixelShader = "PixelPdxMeshStandardShadow"
}