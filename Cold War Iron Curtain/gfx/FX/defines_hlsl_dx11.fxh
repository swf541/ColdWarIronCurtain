#define PDX_DIRECTX_11

#define PDX_POSITION SV_POSITION
#define PDX_COLOR SV_TARGET

#define mod( X, Y ) ( X % Y )

#define FIX_FLIPPED_UV( X ) ( X )
#define FLIP_TEXTURE_V( vCoordinate ) ( vCoordinate )

float3x3 CastTo3x3( in float4x4 M )
{
	return (float3x3)M;
}
#define Create3x3 float3x3
#define GetMatrixData( Matrix, row, col ) ( Matrix [ row ] [ col ] )

float2 vec2(float vValue) { return float2(vValue, vValue); }
float3 vec3(float vValue) { return float3(vValue, vValue, vValue); }
float4 vec4(float vValue) { return float4(vValue, vValue, vValue, vValue); }


struct STextureSampler2D
{
    Texture2D 		_Texture;
    SamplerState 	_Sampler;
};
STextureSampler2D CreateSampler2D( Texture2D Texture, SamplerState Sampler )
{
    STextureSampler2D ret = { Texture, Sampler };
    return ret;
}

struct STextureSamplerCube
{
    TextureCube 	_Texture;
    SamplerState 	_Sampler;
};
STextureSamplerCube CreateSamplerCube( TextureCube Texture, SamplerState Sampler )
{
    STextureSamplerCube ret = { Texture, Sampler };
    return ret;
}

#define TextureSampler2D STextureSampler2D

#define sampler2DShadow STextureSampler2D
#define sampler2D STextureSampler2D

#define tex2D(samp,uv) samp._Texture.Sample(samp._Sampler, uv)
#define tex2Dlod(samp,uv_lod) samp._Texture.SampleLevel(samp._Sampler, (uv_lod).xy, (uv_lod).w)
#define tex2Dlod0(samp,uv_lod) samp._Texture.SampleLevel(samp._Sampler, (uv_lod).xy, 0)
#define tex2Dbias(samp,uv_bias) samp._Texture.SampleBias(samp._Sampler, (uv_bias).xy, (uv_bias).w)
#define tex2Dproj(samp,uv_proj) samp._Texture.SampleLevel(samp._Sampler, (uv_proj).xy / (uv_proj).w, 0)
#define tex2Dgrad(samp,uv,ddx,ddy) samp._Texture.SampleGrad(samp._Sampler, uv, ddx, ddy)

#define texCUBE(samp,uv) samp._Texture.Sample(samp._Sampler, uv)
#define texCUBElod(samp,uv_lod) samp._Texture.SampleLevel(samp._Sampler, (uv_lod).xyz, (uv_lod).w)
#define texCUBEbias(samp,uv_bias) samp._Texture.SampleBias(samp._Sampler, (uv_bias).xyz, (uv_bias).w)

float fmod_loop( float x, float y )
{
  return x - y * floor( x / y );
}
