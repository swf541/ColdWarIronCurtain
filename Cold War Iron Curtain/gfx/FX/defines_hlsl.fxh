#define PDX_DIRECTX_9

#define mod( X, Y ) ( X % Y )

float fmod_loop( float x, float y )
{
  return x - y * floor( x / y );
}

#define GetMatrixData( Matrix, row, col ) ( Matrix [ row ] [ col ] )
#define FIX_FLIPPED_UV( X ) ( X )

#define sampler2DShadow sampler2D

float3x3 CastTo3x3( in float4x4 M )
{
	return (float3x3)M;
}
#define Create3x3 float3x3

float2 vec2(float vValue) { return float2(vValue, vValue); }
float3 vec3(float vValue) { return float3(vValue, vValue, vValue); }
float4 vec4(float vValue) { return float4(vValue, vValue, vValue, vValue); }

#define tex2Dlod0(samp,uv) tex2Dlod(samp, float4((uv), 0.0, 0.0))

#define PDX_POSITION POSITION

#define PDX_COLOR COLOR