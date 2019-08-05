Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
	"shadow.fxh"
	"tiled_pointlights.fxh"
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
		ShadowMap =
		{
			Index = 6
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "Point"
			AddressU = "Wrap"
			AddressV = "Wrap"
			Type = "Shadow"
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
	}
}


VertexStruct VS_INPUT_SIMPLEPARTICLE
{
	float2 vUV0			: TEXCOORD0;
	float4 vPosSize		: TEXCOORD1;
	float3 vRotation	: TEXCOORD2;
	uint4 vTile			: TEXCOORD3;
	float4 vColor		: COLOR;
};

VertexStruct VS_OUTPUT_SIMPLEPARTICLE
{
    float4 vPosition	: PDX_POSITION;
	float2 vUV0			: TEXCOORD0;
	float3 vPos			: TEXCOORD1;
	float4 vColor		: COLOR;
};


ConstantBuffer( 1, 32 )
{
	float4x4 ProjectionMatrix;
};

ConstantBuffer( 2, 36 )
{
	float2 Scale;
};

ConstantBuffer( 3, 40 )
{
	float4x4 InstanceWorldMatrix;
	float4	HalfPixelWH_RowsCols;
	float	vLocalTime;
};


VertexShader =
{
	MainCode VertexSimpleParticle
	[[
		VS_OUTPUT_SIMPLEPARTICLE main( const VS_INPUT_SIMPLEPARTICLE v )
		{
		  	VS_OUTPUT_SIMPLEPARTICLE Out;
			
			float2 offset = ( v.vUV0 - 0.5f ) * v.vPosSize.w * Scale.x;

			#ifdef NO_BILLBOARD
				float2 vSinCos;

				// Yaw
				sincos( v.vRotation.x * ( 3.14159265359f / 180.0f ), vSinCos.x, vSinCos.y );
				float3x3 R0 = Create3x3( 
								float3( vSinCos.y, 0, -vSinCos.x ), 
								float3( 0, 1, 0 ), 
								float3( vSinCos.x, 0, vSinCos.y ) );


				// Pitch
				sincos( v.vRotation.y * ( 3.14159265359f / 180.0f ), vSinCos.x, vSinCos.y );	
				float3x3 R1 = Create3x3( 
								float3( 1, 0, 0 ), 
								float3( 0, vSinCos.y, -vSinCos.x ), 
								float3( 0, vSinCos.x, vSinCos.y ) );

				// Roll
				sincos( v.vRotation.z * ( 3.14159265359f / 180.0f ), vSinCos.x, vSinCos.y );
				float3x3 R2 = Create3x3( 
								float3( vSinCos.y, -vSinCos.x, 0 ), 
								float3( vSinCos.x, vSinCos.y, 0 ), 
								float3( 0, 0, 1 ) );

				float3x3 R = mul( R1, R2 );
				R = mul( R0, R );

				float3 vOffset = float3( offset.x, offset.y, 0 );
				vOffset = mul( R, vOffset );

				float3 vScaledPos = v.vPosSize.xyz * Scale.y;
				float3 vNewPos = float3( vScaledPos.x + vOffset.x, vScaledPos.y + vOffset.y, vScaledPos.z + vOffset.z );
				float3 WorldPosition = mul( InstanceWorldMatrix, float4( vNewPos, 1.0 ) ).xyz;
			#else
				float2 vSinCos;
				sincos( v.vRotation.z * ( 3.14159265359f / 180.0f ), vSinCos.x, vSinCos.y );
				offset = float2( 
				offset.x * vSinCos.y - offset.y * vSinCos.x, 
				offset.x * vSinCos.x + offset.y * vSinCos.y );

				float3 vScaledPos = v.vPosSize.xyz * Scale.y;
				float3 WorldPosition = mul( InstanceWorldMatrix, float4( vScaledPos, 1.0 ) ).xyz;
			#endif
	
			Out.vPos = WorldPosition;
			Out.vPosition = mul( ViewProjectionMatrix, float4( WorldPosition, 1.0 ) );		

			#ifndef NO_BILLBOARD
				Out.vPosition.xy += offset * float2( ProjectionMatrix[0][0], ProjectionMatrix[1][1] );
			#endif
		
			Out.vColor = ToLinear(v.vColor);
			
			float2 tmpUV = float2( v.vUV0.x, 1.0f - v.vUV0.y );
			Out.vUV0 = HalfPixelWH_RowsCols.xy + ( v.vTile.xy + tmpUV ) / HalfPixelWH_RowsCols.zw - HalfPixelWH_RowsCols.xy * 2.0f * tmpUV;
			return Out;
		}
	]]
}

PixelShader =
{
	MainCode PixelSimpleParticle
	[[
		//#define PARTICLE_SHADOWS
		//#define PARTICLE_CAMERA_POINTLIGHT
		float4 main( VS_OUTPUT_SIMPLEPARTICLE In ) : PDX_COLOR
		{
			float4 vColor = tex2D( DiffuseMap, In.vUV0 ) * In.vColor;
			
		#if defined(PARTICLE_SHADOWS) || defined(PARTICLE_CAMERA_POINTLIGHT)
			float3 diffuse = vColor.rgb;
		#endif
		
		#ifdef PARTICLE_SHADOWS
			float fShadowTerm = CalculateShadowCascaded(In.vPos, ShadowMap);	
			float3 sunIntensity = LightDiffuse_Intensity.rgb * LightDiffuse_Intensity.a * fShadowTerm;
			vColor.rgb = saturate((AmbientLight(normalize(float3(1,1,0))) + sunIntensity) * diffuse) * HdrRange;
		#endif
				
		#ifdef PARTICLE_CAMERA_POINTLIGHT
			PointLight cameraPointlight = GetPointLight(CameraLightPosRadius, CameraLightColorFalloff);
			float3 posToLight = cameraPointlight._Position - In.vPos;
			float lightDistance = length(posToLight);
			
			float lightIntensity = cameraPointlight._Color * saturate((cameraPointlight._Radius - lightDistance) / cameraPointlight._Falloff);// * 0.3;
			vColor.rgb += lightIntensity * diffuse * HdrRange;
		#endif

		#ifdef FOG
			vColor.rgb = ApplyDistanceFog( vColor.rgb, In.vPos );
		#endif
			

			return vColor;
		}
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	WriteMask = "RED|GREEN|BLUE"
}

BlendState BlendStateAdditive
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "ONE"
	WriteMask = "RED|GREEN|BLUE"
}

BlendState BlendStatePreAlphaBlend
{
	BlendEnable = yes
	SourceBlend = "ONE"
	DestBlend = "INV_SRC_ALPHA"
	WriteMask = "RED|GREEN|BLUE"
}


RasterizerState RasterizerState
{
	FillMode = "FILL_SOLID"
	CullMode = "CULL_BACK"
	FrontCCW = no
}

RasterizerState RasterizerStateNoCulling
{
	FillMode = "FILL_SOLID"
	CullMode = "CULL_NONE"
	FrontCCW = no
}

Effect ParticleAlphaBlend
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	Defines = { "FOG" }
}

Effect ParticlePreAlphaBlend
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	BlendState = "BlendStatePreAlphaBlend"
	Defines = { "FOG" }
}

Effect ParticleAdditive
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	BlendState = "BlendStateAdditive"
}

Effect ParticleAlphaBlendNoBillboard
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	RasterizerState = "RasterizerStateNoCulling"
	Defines = { "NO_BILLBOARD" "FOG" }
}

Effect ParticlePreAlphaBlendNoBillboard
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	BlendState = "BlendStatePreAlphaBlend"
	RasterizerState = "RasterizerStateNoCulling"
	Defines = { "NO_BILLBOARD" "FOG" }
}

Effect ParticleAdditiveNoBillboard
{
	VertexShader = "VertexSimpleParticle"
	PixelShader = "PixelSimpleParticle"
	BlendState = "BlendStateAdditive"
	RasterizerState = "RasterizerStateNoCulling"
	Defines = { "NO_BILLBOARD" }
}