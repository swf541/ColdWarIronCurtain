#define float4 vec4
#define float3 vec3
#define float2 vec2

#define int4 ivec4
#define int3 ivec3
#define int2 ivec2

#define float4x4 mat4
#define float3x3 mat3

float3x3 Create3x3( in float3 x, in float3 y, in float3 z )
{
	float3x3 Matrix = float3x3( x, y, z );
	Matrix = transpose( Matrix );
	return Matrix;
}

#define static 

#define tex2D texture2D
float4 tex2Dlod( sampler2D tex, float4 UV_lod )
{
#ifdef NO_SHADER_TEXTURE_LOD
	return tex2D( tex, UV_lod.xy );
#else
	return texture2DLod( tex, UV_lod.xy, UV_lod.w );
#endif //NO_SHADER_TEXTURE_LOD
}
#define tex2Dlod0(samp,uv) tex2Dlod(samp, float4((uv), 0.0, 0.0))

#ifdef PIXEL_SHADER
float4 tex2Dbias( sampler2D tex, float4 UV_Bias )
{
	return texture2D( tex, UV_Bias.xy, UV_Bias.w );
}

#define texCUBE textureCube
float4 texCUBEbias( samplerCube tex, float4 UV_Bias )
{
	return texCUBE( tex, UV_Bias.xyz, UV_Bias.w );
}

float4 texCUBElod( samplerCube tex, float4 UV_Lod )
{
#ifdef NO_SHADER_TEXTURE_LOD
	return textureCube( tex, UV_Lod.xyz );
#else
	return textureCubeLod( tex, UV_Lod.xyz, UV_Lod.w );
#endif
}

#endif // PIXEL_SHADER

//#define tex2Dproj shadow2DProj
#define sampler2DShadow sampler2D
#define tex2Dproj(samp,uv_proj) tex2Dlod0(samp, (uv_proj).xy / (uv_proj).w)

#define ddx dFdx
#define ddy dFdy

void sincos( float Value, out float vSin, out float vCos )
{
	vSin = sin(Value);
	vCos = cos(Value);
}

float4 saturate( float4 x )
{
	return clamp( x, 0.0, 1.0 );
}
float3 saturate( float3 x )
{
	return clamp( x, 0.0, 1.0 );
}
float2 saturate( float2 x )
{
	return clamp( x, 0.0, 1.0 );
}
float saturate( float x )
{
	return clamp( x, 0.0, 1.0 );
}
#define clip( X ) if ( (X) < 0 ) { discard; }
#define lerp mix
#define frac fract

float4 mul( float4 X, mat4 Y )
{
	return X * Y;
}

float3 mul( float3 X, mat3 Y )
{
	return X * Y;
}

float4 mul( mat4 X, float4 Y )
{
	return X * Y;
}

float3 mul( mat3 X,  float3 Y )
{
	return X * Y;
}

mat3 mul( mat3 X, mat3 Y )
{
	return X * Y;
}

#define trunc floor

#define fmod_loop( X, Y ) mod( X, Y )

#define GetMatrixData( Matrix, row, col ) ( Matrix [ col ] [ row ] )
//This define exist since OpenGL textures sometimes need to be flipped
#define FIX_FLIPPED_UV( X ) ( -X )

float3x3 CastTo3x3( in float4x4 M )
{
	return float3x3(M);
}

float atan2(float y, float x)
{
	return atan(x, y); // Should x/y be flipped like this? Google thinks it should...
}
