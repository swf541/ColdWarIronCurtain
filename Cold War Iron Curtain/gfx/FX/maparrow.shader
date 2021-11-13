Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
	"tiled_pointlights.fxh"
	"pdxmap.fxh"
	"shadow.fxh"
}

PixelShader =
{
	Samplers =
	{
		TexMask =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TexPattern =
		{
			Index = 1
			MipMapLodBias = -0.5
			MipMapMaxLod = 4
			MipMapMinLod = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		ShadowMap =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
		}
		TerrainIDMap =
		{
			Index = 3
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		HeightMap =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		TerrainNormal =
		{
			Index = 5
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Point"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		HeightNormal =
		{
			Index = 6
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		LeanTexture1 =
		{
			Index = 7
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		LeanTexture2 =
		{
			Index = 8
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Wrap"
			AddressV = "Wrap"
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
		LightIndexMap =
		{
			Index = 10
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}


VertexStruct VS_INPUT_MAPARROW
{
	float3 position				: POSITION;
	float4 uv_isHead_variant	: TEXCOORD0;
};

VertexStruct VS_OUTPUT_MAPARROW
{
	float4 position				: PDX_POSITION;
	float4 uv_isHead_variant	: TEXCOORD0;
	float4 vScreenCoord			: TEXCOORD1;
	float2 uv_terrain			: TEXCOORD2;
	float2 uv_terrain_id		: TEXCOORD3;
	float3 prepos				: TEXCOORD4;
};

VertexStruct VS_INPUT_MAPSYMBOL
{
    float3 position			: POSITION;
	float3 uv				: TEXCOORD0;
};

VertexStruct VS_OUTPUT_MAPSYMBOL
{
    float4 position			: PDX_POSITION;
	float2 uv				: TEXCOORD0;
	float4 vScreenCoord		: TEXCOORD1;
	float2 uv_terrain		: TEXCOORD2;
	float2 uv_terrain_id	: TEXCOORD3;
	float3 prepos			: TEXCOORD4;
};


ConstantBuffer( 3, 32 ) # For arrow shader
{
	float4 ArrowMask;
	float4 ArrowColor;
	float4 ArrowSecondaryColor;
	float4 vTime_IsSelected_FadeInOut;
	float4 vOfsX_vOfsTex_vOfsFx;
	float vBodyUvScale;
	float vSecondaryBodyUvScale;
	float vTextureVariantScale; // 1.0f / (number of variants)
	float fCullingOffset;
	float vShadowFactor;
	float vNormalMapFactor;
};

ConstantBuffer( 4, 32 ) # For symbol shader
{
	float4 SymbolColor;
	float4 Position_Scale;
	float4 vTime_IsSelected_IsIntersect_Rot;
};



VertexShader =
{
	MainCode ArrowVertexShader
	[[
		VS_OUTPUT_MAPARROW main( const VS_INPUT_MAPARROW VertexIn )
		{
			VS_OUTPUT_MAPARROW VertexOut;
			float3 vPos = VertexIn.position;
			vPos.x += vOfsX_vOfsTex_vOfsFx.x;
			VertexOut.prepos = vPos;
			VertexOut.position = mul( ViewProjectionMatrix, float4( vPos, 1.0f ) );
			VertexOut.uv_isHead_variant = VertexIn.uv_isHead_variant;
		#ifdef ANIM_TEXTURE
			VertexOut.uv_isHead_variant.x -= vTime_IsSelected_FadeInOut.x * vOfsX_vOfsTex_vOfsFx.y;
		#endif
			VertexOut.uv_isHead_variant.y = fCullingOffset > 0 ? fCullingOffset - VertexOut.uv_isHead_variant.y : VertexOut.uv_isHead_variant.y;
			VertexOut.uv_terrain_id = float2( ( vPos.x + 0.5f ) / MAP_SIZE_X, ( vPos.z + 0.5f ) / MAP_SIZE_Y );
			VertexOut.uv_terrain.x = ( vPos.x + 0.5f ) / MAP_SIZE_X;
			VertexOut.uv_terrain.y = ( vPos.z + 0.5f - MAP_SIZE_Y ) / -MAP_SIZE_Y;	
			VertexOut.uv_terrain.xy *= float2( MAP_POW2_X, MAP_POW2_Y );
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

	MainCode SymbolVertexShader
	[[
		VS_OUTPUT_MAPSYMBOL main( const VS_INPUT_MAPSYMBOL VertexIn )
		{
			VS_OUTPUT_MAPSYMBOL VertexOut;
			float vSize = Position_Scale.w + ( vTime_IsSelected_IsIntersect_Rot.z * ( Position_Scale.w * 0.25f ) );
			float3 vTruePosition = VertexIn.position.xyz * vSize;
			vTruePosition.xz = RotateVector2D( vTruePosition.xz, vTime_IsSelected_IsIntersect_Rot.w );
			vTruePosition += Position_Scale.xyz;
			VertexOut.prepos = vTruePosition;
			VertexOut.position = mul( ViewProjectionMatrix, float4( vTruePosition, 1.0f ) );
			VertexOut.uv = VertexIn.uv.xy;
			VertexOut.uv_terrain_id = float2( ( vTruePosition.x + 0.5f ) / MAP_SIZE_X, ( vTruePosition.z + 0.5f ) / MAP_SIZE_Y );
			VertexOut.uv_terrain.x = ( vTruePosition.x + 0.5f ) / MAP_SIZE_X;
			VertexOut.uv_terrain.y = ( vTruePosition.z + 0.5f - MAP_SIZE_Y ) / -MAP_SIZE_Y;	
			VertexOut.uv_terrain.xy *= float2( MAP_POW2_X, MAP_POW2_Y );
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

	Code
	[[

	float calculate_water_or_land( float2 vUV )
	{
		float vHeight = tex2D( HeightMap, vUV ).x * 255.0f;
		float vStart = WATER_HEIGHT * 10.0f;
		float vEnd = vStart - 5.0f;
		vHeight = Levels( vHeight, vEnd, vStart );
		return 1.0f - vHeight;
	}

	float3 CalculateTerrainNormal( float2 vUvTerrain, float2 vUvTerrainId, out float vWaterValue, float vTime )
	{
		vWaterValue = 0;

		// Calculate heightmap normal
		float3 normal = normalize( tex2D( HeightNormal, vUvTerrain ).rbg - 0.5f );

	#ifdef NO_SHADER_TEXTURE_LOD
		return normal;
	#else
		// Calculate terrain tile normal
		float vAllSame;
		float4 IndexU;
		float4 IndexV;
		float2 vTerrainUV = vUvTerrainId + float2( -0.5f / MAP_SIZE_X, -0.5f / MAP_SIZE_Y );
		calculate_map_tex_index( tex2D( TerrainIDMap, vTerrainUV ), IndexU, IndexV, vAllSame );
		vWaterValue = calculate_water_or_land( vUvTerrain );
		float2 vTileRepeat = vUvTerrain * TERRAIN_TILE_FREQ;
		vTileRepeat.x *= MAP_SIZE_X/MAP_SIZE_Y;
		float lod = clamp( trunc( mipmapLevel( vTileRepeat ) - 0.5f ), 0.0f, 6.0f );
		float vMipTexels = pow( 2.0f, ATLAS_TEXEL_POW2_EXPONENT - lod );
		float3 terrain_normal = tex2Dlod( TerrainNormal, sample_terrain( IndexU.w, IndexV.w, vTileRepeat, vMipTexels, lod ) ).rbg - 0.5f;
		if( vAllSame < 1.0f )
		{
			float3 terrain_normalRD = tex2Dlod( TerrainNormal, sample_terrain( IndexU.x, IndexV.x, vTileRepeat, vMipTexels, lod ) ).rbg - 0.5f;
			float3 terrain_normalLU = tex2Dlod( TerrainNormal, sample_terrain( IndexU.y, IndexV.y, vTileRepeat, vMipTexels, lod ) ).rbg - 0.5f;
			float3 terrain_normalRU = tex2Dlod( TerrainNormal, sample_terrain( IndexU.z, IndexV.z, vTileRepeat, vMipTexels, lod ) ).rbg - 0.5f;
			terrain_normal += terrain_normalRD + terrain_normalLU + terrain_normalRU;
			terrain_normal *= 0.25f;
		}
		//return normalize( terrain_normal );

		float3 water_normal;
		SampleWater( vUvTerrain, vTime, water_normal, LeanTexture1, LeanTexture2 );
		//return water_normal;

		// Ignore topology normal when over the water
		normal = lerp( normal, float3( 0, 1, 0 ), vWaterValue );

		// Interpolate between water and land normal
		terrain_normal = lerp( terrain_normal, water_normal, vWaterValue );
		terrain_normal = normalize( terrain_normal );

		// Blend normals
		float3 zaxis = normal; //normal
		float3 xaxis = cross( zaxis, float3( 0, 0, 1 ) ); //tangent
		xaxis = normalize( xaxis );
		float3 yaxis = cross( xaxis, zaxis ); //bitangent
		yaxis = normalize( yaxis );
		normal = xaxis * terrain_normal.x + zaxis * terrain_normal.y + yaxis * terrain_normal.z;
		return normal;
	#endif
	}

	float3 CalculateLighting( float3 prepos, float4 vScreenCoord, float3 vNormal, float4 vColor )
	{
		float3 reflectiveColor = vec3(0.0f); // ArrowColor
		LightingProperties lightingProperties;
		lightingProperties._WorldSpacePos = prepos;
		lightingProperties._ToCameraDir = normalize(vCamPos - prepos);
		lightingProperties._Normal = vNormal;
		lightingProperties._Diffuse = vColor.rgb;
		lightingProperties._Glossiness = 0.05f;
		lightingProperties._SpecularColor = vec3(vColor.a);
		lightingProperties._NonLinearGlossiness = GetNonLinearGlossiness(vColor.a);
		float3 diffuseLight = vec3(0.0);
		float3 specularLight = vec3(0.0);
		float fShadowTerm = GetShadowScaled( SHADOW_WEIGHT_TERRAIN, vScreenCoord, ShadowMap );
		CalculateSunLight( lightingProperties, fShadowTerm, diffuseLight, specularLight );
		CalculatePointLights( lightingProperties, LightDataMap, LightIndexMap, diffuseLight, specularLight);
		diffuseLight += reflectiveColor * lightingProperties._Glossiness;
		return ComposeLight(lightingProperties, diffuseLight, specularLight);
	}

	float FxMask( in float2 vUV, in float vIsHead )
	{
		float v = vUV.y > 0.5f ? 1.0f - vUV.y: vUV.y;
		float u = 1.0f - ( vUV.x * 5.0f - vTime_IsSelected_FadeInOut.x * vOfsX_vOfsTex_vOfsFx.y * 5.0f );
		float t = 3.14159 / 4.0;
		float w = 25;
		float stripeVal = cos( ( u * cos( t ) * w ) + ( v * sin( t ) * w ) ); 
		float camDist = cam_distance( 300.0, 1200.0 );
		stripeVal += camDist * 1.5;
		stripeVal = smoothstep(0.0, 1.0, stripeVal*1.7) * lerp(1.0, 0.3, camDist);
		return 1.0f - vOfsX_vOfsTex_vOfsFx.z * stripeVal * ( 1.0f - vIsHead );
	}

	]]

	MainCode ArrowPixelShader
	[[
		float4 main( VS_OUTPUT_MAPARROW Input ) : PDX_COLOR
		{
			//return float4( 1, 0, 1, 1 );
			float vIsHead = Input.uv_isHead_variant.z < 0.5f ? 0.0f : 1.0f;
			float vTextureVariant = 1.0f - step( Input.uv_isHead_variant.w, 0.0f );
			
			float vVariantBodyUvScale = lerp( vBodyUvScale, vSecondaryBodyUvScale, vTextureVariant );

			float2 vUV;
			vUV.x = Input.uv_isHead_variant.x * 0.5f + ( vIsHead * 0.5f );
			float vHeadV = Input.uv_isHead_variant.y;
			float vBodyV = ( ( Input.uv_isHead_variant.y - 0.5f ) * vVariantBodyUvScale + 0.5f + vTextureVariant ) * vTextureVariantScale; // Adjust UV vertically to select the correct packed texture variant.
			vUV.y = lerp( vBodyV, vHeadV, vIsHead );

			float vWaterValue = 0;
			float3 vNormal = vNormalMapFactor * CalculateTerrainNormal( Input.uv_terrain, Input.uv_terrain_id, vWaterValue, vTime_IsSelected_FadeInOut.x );
			vUV += vNormal.xz * ( /*vNormal.y **/ MAP_ARROW_NORMALS_STR_TERR );
			vUV -= vNormal.xz * ( vWaterValue * MAP_ARROW_NORMALS_STR_WATER );
			vUV = clamp( vUV, 0.001f, 0.998f );

			float4 vMask = tex2D( TexMask, vUV );
			vMask -= ( ( sin( vTime_IsSelected_FadeInOut.x * MAP_ARROW_SEL_BLINK_SPEED ) * MAP_ARROW_SEL_BLINK_RANGE + 1.0f - MAP_ARROW_SEL_BLINK_RANGE * 0.5f ) * 0.5f ) * vTime_IsSelected_FadeInOut.y;
			vMask = saturate( vMask );
			clip( vMask.a <= 0 ? -1 : 1 );
			vMask.rgb = vMask.rgb * ArrowMask.rgb * vMask.a;
			float vMaskValue = saturate( vMask.r + vMask.g + vMask.b );
			vMaskValue *= vTime_IsSelected_FadeInOut.z > 0 ? saturate( Levels( Input.uv_isHead_variant.x, 0.0f, vTime_IsSelected_FadeInOut.z ) + vIsHead ) : 1;
			vMaskValue *= vTime_IsSelected_FadeInOut.w > 0 ? saturate( Levels( 1.0f - Input.uv_isHead_variant.x, 0.0f, vTime_IsSelected_FadeInOut.w ) + vIsHead ) : 1;
			clip( vMaskValue <= 0 ? 0 : 1 );
			vMaskValue *= FxMask( float2( vUV.x * 2.0f, vUV.y ), vIsHead );

			float4 vPattern = tex2D( TexPattern, vUV );

			float4 vArrowColor = lerp( ArrowColor, ArrowSecondaryColor, vTextureVariant );
		#if 1
			vArrowColor.rgb = RGBtoHSV(vArrowColor.rgb);
			vArrowColor.r = mod( vArrowColor.r, 6.0 ); //H
			vArrowColor.g *= 1.5; //S bump up the saturation and light
			vArrowColor.b *= 1.0; //V
			vArrowColor.rgb = HSVtoRGBPost(vArrowColor.rgb);

			float4 vColor = saturate( vPattern * vArrowColor );
			float3 vColor2 = CalculateLighting( Input.prepos, Input.vScreenCoord, vNormal, vColor );
			vColor.rgb = lerp(vColor.rgb, vColor2, 0.5);
		#else
			float4 vColor = saturate( vPattern * vArrowColor );
			vColor.rgb = CalculateLighting( Input.prepos, Input.vScreenCoord, vNormal, vColor );
		#endif

			vColor.rgb = ApplyDistanceFog( vColor.rgb, Input.prepos );
			vColor.rgb = DayNightWithBlend( vColor.rgb, CalcGlobeNormal( Input.prepos.xz ), 0.2f );
			return float4( vColor.rgb, vColor.a * vMaskValue );
		}
		
	]]

	MainCode ArrowPixelShaderNoHead
	[[
		float4 main( VS_OUTPUT_MAPARROW Input ) : PDX_COLOR
		{
			//return float4( 1, 0, 1, 1 );
			float vTextureVariant = 1.0f - step( Input.uv_isHead_variant.w, 0.0f );
			
			float vVariantBodyUvScale = lerp( vBodyUvScale, vSecondaryBodyUvScale, vTextureVariant );
			float2 vUV = Input.uv_isHead_variant.xy;
			vUV.y = ( ( vUV.y - 0.5f ) * vVariantBodyUvScale + 0.5f + vTextureVariant ) * vTextureVariantScale; // Adjust UV vertically to select the correct packed texture variant.

			float vWaterValue = 0;
			float3 vNormal = vNormalMapFactor * CalculateTerrainNormal( Input.uv_terrain, Input.uv_terrain_id, vWaterValue, vTime_IsSelected_FadeInOut.x );

			vUV += vNormal.xz * ( vNormal.y * MAP_ARROW_NORMALS_STR_TERR );
			vUV -= vNormal.xz * ( vWaterValue * MAP_ARROW_NORMALS_STR_WATER );

			float4 vMask = tex2D( TexMask, vUV );
			vMask -= ( ( sin( vTime_IsSelected_FadeInOut.x * MAP_ARROW_SEL_BLINK_SPEED ) * MAP_ARROW_SEL_BLINK_RANGE + 1.0f - MAP_ARROW_SEL_BLINK_RANGE * 0.5f ) * 0.5f ) * vTime_IsSelected_FadeInOut.y;
			vMask = saturate( vMask );
			//clip( vMask.a <= 0 ? -1 : 1 );
			vMask.rgb = vMask.rgb * ArrowMask.rgb * vMask.a;
			float vMaskValue = saturate( vMask.r + vMask.g + vMask.b );
			clip( vMaskValue <= 0 ? -1 : 1 );

			float4 vPattern = tex2D( TexPattern, vUV );

			float4 vArrowColor = lerp( ArrowColor, ArrowSecondaryColor, vTextureVariant );
			#if 1
				vArrowColor.rgb = RGBtoHSV(vArrowColor.rgb);
				vArrowColor.r = mod( vArrowColor.r, 6.0 ); //H
				vArrowColor.g *= 2.0; //S bump up the saturation and light
				vArrowColor.b *= 1.5; //V
				vArrowColor.rgb = HSVtoRGBPost(vArrowColor.rgb);

				float4 vColor = saturate( vPattern * vArrowColor );
				float3 vColor2 = CalculateLighting( Input.prepos, Input.vScreenCoord, vNormal, vColor );
				vColor.rgb = lerp(vColor.rgb, vColor2, 0.5);
			#else
				float4 vColor = saturate( vPattern * vArrowColor );
				vColor.rgb = CalculateLighting( Input.prepos, Input.vScreenCoord, vNormal, vColor );
			#endif
			
			vColor.rgb *= GetShadowScaled( vShadowFactor * SHADOW_WEIGHT_TERRAIN, Input.vScreenCoord, ShadowMap );
			vColor.rgb = ApplyDistanceFog( vColor.rgb, Input.prepos );
			vColor.rgb = DayNightWithBlend( vColor.rgb, CalcGlobeNormal( Input.prepos.xz ), 0.2f );
			return float4( vColor.rgb, vColor.a * vMaskValue );
		}
		
	]]

	MainCode SymbolPixelShader
	[[
		float4 main( VS_OUTPUT_MAPSYMBOL Input ) : PDX_COLOR
		{
			//return float4( 1, 0, 1, 1 );
		
			// Calculate terrain/water normal
			float2 vUV = Input.uv;
			float vWaterValue = 0;
			float3 vNormal = CalculateTerrainNormal( Input.uv_terrain, Input.uv_terrain_id, vWaterValue, vTime_IsSelected_IsIntersect_Rot.x );
			vUV += vNormal.xz * ( vNormal.y * MAP_ARROW_NORMALS_STR_TERR );
			vUV -= vNormal.xz * ( vWaterValue * MAP_ARROW_NORMALS_STR_WATER );
			//float3 vNormal = float3( 0, 1, 0 );
		
			// Grab texture color
			float4 vColor = tex2D( TexPattern, vUV );
			vColor *= SymbolColor;
		
			// Blinking transparency
			//vColor.a -= ( ( sin( vTime_IsSelected.x * MAP_ARROW_SEL_BLINK_SPEED ) * MAP_ARROW_SEL_BLINK_RANGE + 1.0f - MAP_ARROW_SEL_BLINK_RANGE * 0.5f ) * 0.5f ) * vTime_IsSelected.y;
			//clip( vColor.a );
		
			vColor.rgb = CalculateLighting( Input.prepos, Input.vScreenCoord, vNormal, vColor );
			vColor.rgb = ApplyDistanceFog( vColor.rgb, Input.prepos );
			//vColor.rgb = DayNight( vColor.rgb, CalcGlobeNormal( Input.prepos.xz ) );
			return vColor;
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

BlendState BlendStateAdd
{
	BlendEnable = yes
	AlphaTest = no
	BlendOp = "blend_op_add" 
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
	StencilEnable = yes
	FrontStencilFailOp = "stencil_op_keep"
	FrontStencilDepthFailOp = "stencil_op_keep"
	FrontStencilPassOp = "stencil_op_incr"
	FrontStencilFunc = "comparison_equal"
}

DepthStencilState NoDepthStencilState
{
	DepthEnable = no
	StencilEnable = no
}

DepthStencilState DefaultDepthNoStencil
{
	DepthEnable = yes
	DepthWriteMask = "depth_write_all"
	DepthFunction = "comparison_less_equal"
	StencilEnable = no
}

Effect MapArrowDefault
{
	VertexShader = "ArrowVertexShader"
	PixelShader = "ArrowPixelShader"
	DepthStencilState = "DepthStencilState"
}

Effect MapArrowDefaultWithDepth
{
	VertexShader = "ArrowVertexShader"
	PixelShader = "ArrowPixelShader"
	DepthStencilState = "DefaultDepthNoStencil"
}

Effect MapArrowNoHeadWidthDepth
{
	VertexShader = "ArrowVertexShader"
	PixelShader = "ArrowPixelShaderNoHead"
	DepthStencilState = "DefaultDepthNoStencil"
	Defines = { "ANIM_TEXTURE" }
}

Effect MapArrowNoHead
{
	VertexShader = "ArrowVertexShader"
	PixelShader = "ArrowPixelShaderNoHead"
	DepthStencilState = "DepthStencilState"
	Defines = { "ANIM_TEXTURE" }
}

Effect MapSymbolDefault
{
	VertexShader = "SymbolVertexShader"
	PixelShader = "SymbolPixelShader"
	DepthStencilState = "NoDepthStencilState"
}

Effect MapSymbolDefaultAdd
{
	VertexShader = "SymbolVertexShader"
	PixelShader = "SymbolPixelShader"
	DepthStencilState = "NoDepthStencilState"
	BlendState = "BlendStateAdd"
}
