VertexStruct VS_INPUT
{
	float3 vPosition  : POSITION;
	float2 vTexCoord  : TEXCOORD0;
};

ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix;	
	float4 Color;
	float2 Offset;
	float2 NextOffset;
	float Time;
	float AnimationTime;
};
