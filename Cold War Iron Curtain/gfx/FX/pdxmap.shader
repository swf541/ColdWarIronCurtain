Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
	"tiled_pointlights.fxh"
	"pdxmap.fxh"
	"shadow.fxh"
	"fow.fxh"
}

PixelShader =
{
	Samplers =
	{
		TerrainDiffuse =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		HeightNormal =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TerrainColorTint =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		SnowTexture =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TerrainNormal =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TerrainIDMap =
		{
			Index = 5
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
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
		SnowMudData =
		{
			Index = 7
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		CityLightsAndSnowNoise =
		{
			Index = 8
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		MudNormalSpec =
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
		ShadowMap =
		{
			Index = 12
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
		}
		MudDiffuseGloss =
		{
			Index = 13
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		GradientBorderChannel1 =
		{
			Index = 14
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		GradientBorderChannel2 =
		{
			Index = 15
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}


VertexStruct VS_INPUT_TERRAIN_NOTEXTURE
{
    float4 position			: POSITION;
	float2 height			: TEXCOORD0;
};

VertexStruct VS_OUTPUT_TERRAIN
{
    float4 position			: PDX_POSITION;
	float2 uv				: TEXCOORD0;
	float2 uv2				: TEXCOORD1;
	float3 prepos 			: TEXCOORD2;
	float4 vShadowProj		: TEXCOORD3;
	float4 vScreenCoord		: TEXCOORD4;
};



VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT_TERRAIN main( const VS_INPUT_TERRAIN_NOTEXTURE VertexIn )
		{
			VS_OUTPUT_TERRAIN VertexOut;
			
			float2 pos = VertexIn.position.xy * QuadOffset_Scale_IsDetail.z + QuadOffset_Scale_IsDetail.xy;
		
			float vSatPosZ = saturate( VertexIn.position.z ); // VertexIn.position.z can have a value [0-4], if != 0 then we shall displace vertex
			float vUseAltHeight = vSatPosZ * vSnap[ int( VertexIn.position.z - 1.0f ) ]; // the snap values are set to either 0 or 1 before each draw call to enable/disable snapping due to LOD
		
			pos += vUseAltHeight 
				* float2( 1.0f - VertexIn.position.w, VertexIn.position.w ) // VertexIn.position.w determines offset direction
				* QuadOffset_Scale_IsDetail.z; // and of course we need to scale it to the same LOD
		
			VertexOut.uv = float2( ( pos.x + 0.5f ) / MAP_SIZE_X,  ( pos.y + 0.5f ) / MAP_SIZE_Y );
			VertexOut.uv2.x = ( pos.x + 0.5f ) / MAP_SIZE_X;
			VertexOut.uv2.y = ( pos.y + 0.5f - MAP_SIZE_Y ) / -MAP_SIZE_Y;	
			VertexOut.uv2.xy *= float2( MAP_POW2_X, MAP_POW2_Y ); //POW2
		
			float vHeight = VertexIn.height.x * ( 1.0f - vUseAltHeight ) + VertexIn.height.y * vUseAltHeight;
			vHeight *= 0.01f;
		
			VertexOut.prepos = float3( pos.x, vHeight, pos.y );
			VertexOut.position = mul( ViewProjectionMatrix, float4( VertexOut.prepos, 1.0f ) );
			
			VertexOut.vShadowProj = mul( ShadowMapTextureMatrix, float4( VertexOut.prepos, 1.0f ) );
			
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
	MainCode PixelShaderTerrain
	[[		
		float4 main( VS_OUTPUT_TERRAIN Input ) : PDX_COLOR
		{
			//return float4( 0, 1.0f, 0, 1.0f );
			clip( Input.prepos.y + TERRAIN_WATER_CLIP_HEIGHT - WATER_HEIGHT );
		
			float2 vOffsets = float2( -0.5f / MAP_SIZE_X, -0.5f / MAP_SIZE_Y );
			
			float vAllSame;
			float4 IndexU;
			float4 IndexV;
			calculate_map_tex_index( tex2D( TerrainIDMap, Input.uv + vOffsets.xy ), IndexU, IndexV, vAllSame );
						
			float2 vTileRepeat = Input.uv2 * TERRAIN_TILE_FREQ;
			vTileRepeat.x *= MAP_SIZE_X/MAP_SIZE_Y;
			
			float lod = clamp( mipmapLevel( vTileRepeat ) - 0.5f, 0.0f, 6.0f );
			float vMipTexels = pow( 2.0f, ATLAS_TEXEL_POW2_EXPONENT - lod );
					
		#ifdef LOW_END_GFX
			float3 normal = float3( 0, 1, 0 );
		#else
			float3 normal = normalize( tex2D( HeightNormal, Input.uv2 ).rbg - 0.5f );
		#endif
			float4 diffuse = tex2Dlod( TerrainDiffuse, sample_terrain( IndexU.w, IndexV.w, vTileRepeat, vMipTexels, lod ) ).rgba;
			float vGlossiness = diffuse.a;
									
		#ifdef NO_SHADER_TEXTURE_LOD
			float3 terrain_normal = float3( 0,1,0 );
		#else	
			float3 terrain_normal;
			float4 terrain_normalRaw = tex2Dlod( TerrainNormal, sample_terrain( IndexU.w, IndexV.w, vTileRepeat, vMipTexels, lod ) );
		#endif //NO_SHADER_TEXTURE_LOD
			
			if ( vAllSame < 1.0f )
			{
				float4 ColorRD = tex2Dlod( TerrainDiffuse, sample_terrain( IndexU.x, IndexV.x, vTileRepeat, vMipTexels, lod ) ).rgba;
				float4 ColorLU = tex2Dlod( TerrainDiffuse, sample_terrain( IndexU.y, IndexV.y, vTileRepeat, vMipTexels, lod ) ).rgba;
				float4 ColorRU = tex2Dlod( TerrainDiffuse, sample_terrain( IndexU.z, IndexV.z, vTileRepeat, vMipTexels, lod ) ).rgba;
		
		#ifndef NO_SHADER_TEXTURE_LOD	
				float4 terrain_normalRD = tex2Dlod( TerrainNormal, sample_terrain( IndexU.x, IndexV.x, vTileRepeat, vMipTexels, lod ) );
				float4 terrain_normalLU = tex2Dlod( TerrainNormal, sample_terrain( IndexU.y, IndexV.y, vTileRepeat, vMipTexels, lod ) );
				float4 terrain_normalRU = tex2Dlod( TerrainNormal, sample_terrain( IndexU.z, IndexV.z, vTileRepeat, vMipTexels, lod ) );
		#endif //NO_SHADER_TEXTURE_LOD
		
				float2 vFrac = frac( float2( Input.uv.x * MAP_SIZE_X - 0.5f, Input.uv.y * MAP_SIZE_Y - 0.5f ) );
		
				diffuse = lerp( 
					lerp( ColorRU, ColorLU, vFrac.x ),
					lerp( ColorRD, diffuse, vFrac.x ), 
						vFrac.y );
		
		#ifndef NO_SHADER_TEXTURE_LOD
				terrain_normalRaw = lerp( 
					lerp( terrain_normalRU, terrain_normalLU, vFrac.x ),
					lerp( terrain_normalRD, terrain_normalRaw, vFrac.x ), 
						vFrac.y );
		#endif //NO_SHADER_TEXTURE_LOD
			}
			
		#ifndef NO_SHADER_TEXTURE_LOD
			terrain_normal =  terrain_normalRaw.rbg - 0.5f; //UnpackRRxGNormal(terrain_normalRaw).rgb;
			//return float4(terrain_normal.rgb, 1.0f);
			#ifdef LOW_END_GFX
				float vSpec = 0.0f;
			#else
				float vSpec = terrain_normalRaw.a;
				vGlossiness = diffuse.a;
			#endif
		#else
			float vSpec = 0.0f;
		#endif

		#ifndef NO_SHADER_TEXTURE_LOD
		 	terrain_normal = normalize( terrain_normal );
			
			//Calculate terrain normal
			normal = RotateVectorByVector( normal, terrain_normal );
			normal = normalize(normal);
		#endif
			
			float4 TerrainColor = tex2D( TerrainColorTint, Input.uv2 );

		#ifndef LOW_END_GFX
			float CityLightsMask = TerrainColor.a;
		#endif
	
			float vSnowAlpha = 1-vSpec;
			diffuse.rgb = GetOverlay( diffuse.rgb, TerrainColor.rgb, COLORMAP_OVERLAY_STRENGTH );

		#ifndef LOW_END_GFX
			float4 vMudSnow = GetMudSnowColor( Input.prepos, SnowMudData );	
			diffuse.rgb = ApplySnow( diffuse.rgb, Input.prepos, normal, vMudSnow, SnowTexture, CityLightsAndSnowNoise, vGlossiness, vSnowAlpha );
			diffuse.rgb = GetMudColor( diffuse.rgb, vMudSnow, Input.prepos, normal, vGlossiness, vSpec, MudDiffuseGloss, MudNormalSpec );
		#endif
							
			// Gradient Borders
			float vBloomAlpha = 0.0f;
			gradient_border_apply( diffuse.rgb, normal, Input.uv2, GradientBorderChannel1, GradientBorderChannel2, 1.0f, vGBCamDistOverride_GBOutlineCutoff.zw, vGBCamDistOverride_GBOutlineCutoff.xy, vBloomAlpha );
					
			// Secondary color mask
			secondary_color_mask( diffuse.rgb, normal, Input.uv2, ProvinceSecondaryColorMap, vBloomAlpha );

			LightingProperties lightingProperties;
			lightingProperties._WorldSpacePos = Input.prepos;
			lightingProperties._ToCameraDir = normalize(vCamPos - Input.prepos);
			lightingProperties._Normal = normal;
			
		#ifdef PDX_IMPROVED_BLINN_PHONG

			#ifdef NO_SHADER_TEXTURE_LOD
				float SpecRemapped = 0.1;
			#else
				float SpecRemapped = vSpec * vSpec * 0.4;
			#endif // NO_SHADER_TEXTURE_LOD			

			float MetalnessRemapped = 0.0;// - (1.0 - vProperties.b) * (1.0 - vProperties.b);
			lightingProperties._Diffuse = MetalnessToDiffuse(MetalnessRemapped, diffuse.rgb);
			lightingProperties._Glossiness = vGlossiness;
			lightingProperties._SpecularColor = MetalnessToSpec(MetalnessRemapped, diffuse.rgb, SpecRemapped);
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vGlossiness);
		#else
			lightingProperties._Diffuse = diffuse.rgb;
			lightingProperties._Glossiness = vGlossiness;
			lightingProperties._SpecularColor = vec3(vSpec);
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vGlossiness);

		#endif //PDX_IMPROVED_BLINN_PHONG

			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);

			float fShadowTerm = max(GetShadowScaled( SHADOW_WEIGHT_TERRAIN, Input.vScreenCoord, ShadowMap ), 0.1f );
		
			CalculateSunLight( lightingProperties, fShadowTerm, diffuseLight, specularLight );

		#ifndef LOW_END_GFX
			CalculatePointLights( lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);
		#endif
			
		#ifdef PDX_IMPROVED_BLINN_PHONG
			float3 vEyeDir = normalize( Input.prepos - vCamPos.xyz );
			//float3 reflection = reflect( vEyeDir, lightingProperties._Normal );
			//float MipmapIndex = GetEnvmapMipLevel(lightingProperties._Glossiness); 
			
			float3 reflectiveColor = FAKE_CUBEMAP_COLOR; //texCUBElod( EnvironmentMap, float4(reflection, MipmapIndex) ).rgb * CubemapIntensity;
			specularLight += reflectiveColor * FresnelGlossy(lightingProperties._SpecularColor, -vEyeDir, lightingProperties._Normal, lightingProperties._Glossiness);
		#endif
			
			float3 vOut = ComposeLightSnow(lightingProperties, diffuseLight, specularLight, vSnowAlpha);
		
			vOut = lerp( vOut, diffuse.rgb, BORDER_LIGHT_REMOVAL_FACTOR * ( 1 - vBloomAlpha ) );
				
			float3 vGlobeNormal = CalcGlobeNormal( Input.prepos.xz );
			float vNightFactor = DayNightFactor( vGlobeNormal );

		#ifndef LOW_END_GFX
			float3 CityLights = tex2D( CityLightsAndSnowNoise, Input.prepos.xz * CITY_LIGHTS_TILING ).rgb;
			vOut += CityLights * CITY_LIGHTS_INTENSITY * CityLightsMask * vNightFactor;
		#endif

			float3 vFOW = ApplyFOW( vOut, ShadowMap, Input.vScreenCoord );
			vOut = lerp( vFOW, vOut, BORDER_FOW_REMOVAL_FACTOR * ( 1 - vBloomAlpha ) );
		
		#ifndef LOW_END_GFX
			vOut = ApplyDistanceFog( vOut, Input.prepos );
		#endif
			
			vOut = DayNightWithBlend( vOut, vGlobeNormal, lerp(BORDER_NIGHT_DESATURATION_MAX, 1.0f, vBloomAlpha) );
			
			DebugReturn(vOut, lightingProperties, fShadowTerm);

		#ifdef LOW_END_GFX
			return float4( vOut, vNightFactor * CITY_LIGHTS_BLOOM_FACTOR );
		#else
			return float4( vOut, saturate(CityLightsMask * vNightFactor * CITY_LIGHTS_BLOOM_FACTOR) );
		#endif
		}		
	]]

	MainCode PixelShaderUnderwater
	[[
		float4 main( VS_OUTPUT_TERRAIN Input ) : PDX_COLOR
		{
			clip( WATER_HEIGHT - Input.prepos.y + TERRAIN_WATER_CLIP_HEIGHT );
		
			float3 normal = normalize( tex2D( HeightNormal,Input.uv2 ).rbg - 0.5f );
			float3 diffuse = tex2D( TerrainDiffuse, Input.uv2 * float2(( MAP_SIZE_X / 32.0f ), ( MAP_SIZE_Y / 32.0f ) ) ).rgb;

			// TOMASZ: SnowTexture texture slot here was some kind of normalmap that is obsolete 
			//         and makes no visual effect, so I've removed it.
			//float3 offset = tex2D( SnowTexture, Input.uv2 * float2(( MAP_SIZE_X / 32.0f ), ( MAP_SIZE_Y / 32.0f ) ) ).rgb;
			//offset -= vec3(0.5);
			
			float3 waterColorTint = tex2D( TerrainColorTint, Input.uv2 /*+ offset.xy * WATER_RIPPLE_EFFECT*/ ).rgb;		
			waterColorTint *= WATER_COLOR_LIGHTNESS;
			
			float vMin = 5.3f; //5.3f; Depthfog ish for bottom
			float vMax = 13.0f; //30.0f; 

			//float vWaterAlpha = saturate( Input.prepos.y * Input.prepos.y * Input.prepos.y * WATER_HEIGHT_RECP_SQUARED * WATER_HEIGHT_RECP  );
			float vWaterAlpha = saturate(( Input.prepos.y - vMin ) / ( vMax - vMin ) );
		
			float vGlossiness = MAP_SPECULAR_WIDTH;
		
			LightingProperties lightingProperties;
			lightingProperties._WorldSpacePos = Input.prepos;
			lightingProperties._ToCameraDir = normalize(vCamPos - Input.prepos);
			lightingProperties._Normal = normal;
			lightingProperties._Diffuse = diffuse;

			lightingProperties._Glossiness = vGlossiness;
			lightingProperties._SpecularColor = SunDiffuseIntensity.rgb * 0.1f;
			lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vGlossiness);
			
			float3 diffuseLight = vec3(0.0);
			float3 specularLight = vec3(0.0);		
			float fShadowTerm = GetShadowScaled( SHADOW_WEIGHT_TERRAIN, Input.vScreenCoord, ShadowMap );
		
			CalculateSunLight( lightingProperties, fShadowTerm, diffuseLight, specularLight );
			CalculatePointLights( lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);
			
			float3 vOut = ComposeLight(lightingProperties, diffuseLight, specularLight );
						
			vOut = lerp( waterColorTint, vOut, vWaterAlpha );			
		
			return float4( vOut, 1.0f );
		}
	]]

	MainCode PixelShaderTerrainUnlit
	[[
		float4 main( VS_OUTPUT_TERRAIN Input ) : PDX_COLOR
		{	
			// Grab the shadow term
			float fShadowTerm = CalculateShadow( Input.vShadowProj, ShadowMap);
			
			float FogColorFactor = 0.0;
			float FogAlphaFactor = 0.0;
			GetFogFactors( FogColorFactor, FogAlphaFactor, Input.prepos, 0.0, TerrainDiffuse, HeightNormal, TerrainColorTint);
			return float4( fShadowTerm, FogColorFactor, FogAlphaFactor, 1.0f );
		}
	]]
}


BlendState BlendState
{
	BlendEnable = no
	AlphaTest = no
	WriteMask = "RED|GREEN|BLUE|ALPHA"
}


Effect terrain_low_gfx
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTerrain"
	Defines = { "LOW_END_GFX" }
}

Effect terrain
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTerrain"
	Defines = { "PDX_IMPROVED_BLINN_PHONG" }
}

Effect underwater
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderUnderwater"
}

Effect terrainunlit
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTerrainUnlit"
}

