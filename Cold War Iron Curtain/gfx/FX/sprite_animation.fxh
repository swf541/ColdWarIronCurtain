ConstantBuffer( 1, 7 )
{
	float4 ConstantData[10];
}

Code
[[

struct AnimationData
{
	float4 Rotation;
	float4 UVScale;
	float2 RotationOffset;
	float2 TextureStretch;
	float AnimationOffset;
	float BlendFactor;
	float Type; // 1 = Scrolling, 2 = Rotating, 3 = Pulse
	float BlendMode; // 0 = Add, 1 = Multiply, 2 = Overlay
	float ClampAnimation;
};

AnimationData GetAnimationData(int nIndex)
{
	AnimationData data;
	
	data.Rotation = ConstantData[nIndex * 5];
	data.UVScale = ConstantData[nIndex * 5 + 1];
	data.RotationOffset = ConstantData[nIndex * 5 + 2].xy;
	data.TextureStretch = ConstantData[nIndex * 5 + 2].zw;
	data.AnimationOffset = ConstantData[nIndex * 5 + 3].x;
	data.BlendFactor = ConstantData[nIndex * 5 + 3].y;
	data.Type = ConstantData[nIndex * 5 + 3].z;
	data.BlendMode = ConstantData[nIndex * 5 + 3].w;
	data.ClampAnimation = ConstantData[nIndex * 5 + 4].x;

	return data;
}

float2 GetAnimatedTexcoord(float2 Texcoord, AnimationData Data)
{
	float2 AnimatedTexcoord = vec2(0.0);
	float2 OffsetAndScaledTexcoord = (Data.RotationOffset + Texcoord - vec2(0.5)) * Data.UVScale.xy * Data.TextureStretch;
	
	if (Data.Type == 1) // Scrolling
	{
		AnimatedTexcoord = float2(dot(OffsetAndScaledTexcoord, Data.Rotation.xy), dot(OffsetAndScaledTexcoord, Data.Rotation.zw));
		
		AnimatedTexcoord /= Data.UVScale.xy;
		AnimatedTexcoord *= Data.UVScale.zw;
		AnimatedTexcoord.y += Data.AnimationOffset;

		AnimatedTexcoord += float2(0.5, 0.5 * Data.UVScale.w);
	}
	else if (Data.Type == 2) // Scrolling
	{
		AnimatedTexcoord = float2(dot(OffsetAndScaledTexcoord, Data.Rotation.xy), dot(OffsetAndScaledTexcoord, Data.Rotation.zw));
		
		AnimatedTexcoord /= Data.UVScale.xy;
		AnimatedTexcoord *= Data.UVScale.zw;
		
		AnimatedTexcoord += float2(0.5, 0.5);
	}
	
	return AnimatedTexcoord;
}

float4 Blend(float4 Dest, float4 Source, AnimationData Data)
{
	float4 Result = float4(1.0, 0.0, 1.0, 1.0);
	
	if (Data.BlendMode == 0) // Add
	{
		Result.rgb = lerp(Dest.rgb, Dest.rgb + Source.rgb, Source.a);
		Result.a = max(Dest.a, Source.a);
	}

	if (Data.BlendMode == 1) // Multiply
	{
		Result = Dest * Source;
	}

	if (Data.BlendMode == 2) // Overlay
	{
		// no idea what this is doing
		Result.rgb = lerp(Dest.rgb * Source.rgb * 2.0, 1.0 - (2.0 * (1.0 - Dest.rgb) * (1.0 - Source.rgb)), step(0.5, Dest.rgb));
		Result.a = Source.a;
	}

	if (Data.BlendMode == 3) // Normal (classic alpha blending with support for transparent destination)
	{
		Result.rgb = lerp(Dest.rgb * Dest.a, Source.rgb, Source.a);
		Result.a = max(Source.a, Dest.a);
	}

	return Result;
}

float4 GetAnimatedTexcoord(float2 Texcoord)
{
	float4 AnimatedTexcoord = vec4(0.0);
	
	AnimationData data = GetAnimationData(0);
	AnimatedTexcoord.xy = GetAnimatedTexcoord(Texcoord, data);
	
#ifdef NUM_ANIMATIONS_2
	data = GetAnimationData(1);
	AnimatedTexcoord.zw = GetAnimatedTexcoord(Texcoord, data);
#endif	
	
	return AnimatedTexcoord;
}
]]


PixelShader = {
Code 
[[

float4 Animate(float4 BaseColor, in sampler2D MaskTextureSampler, float2 MaskTexcoord, in sampler2D AnimatedTextureSampler, float2 AnimatedTexcoord, AnimationData Data)
{
    float4 Mask = tex2D( MaskTextureSampler, MaskTexcoord );
	float4 Anim = vec4(0.0);
			
	if (Data.Type == 3) // Pulse
	{
		Anim = vec4(Data.AnimationOffset);
	}
	else
	{
		Anim = tex2D( AnimatedTextureSampler, AnimatedTexcoord );
		
		if ((Data.ClampAnimation > 0.0f) && (AnimatedTexcoord.y < 0.0 || AnimatedTexcoord.y > 1.0))
			Mask.a = 0.0;
	}

	float4 Masked = Anim * Mask;
	Masked.a *= Data.BlendFactor;
	float4 Blended = Blend(BaseColor, Masked, Data);
	return Blended;
}

float4 Animate(float4 BaseColor, float2 MaskTexcoord, float4 AnimatedTexcoord, in sampler2D MaskTextureSampler, in sampler2D AnimatedTextureSampler,
				 in sampler2D MaskTexture2Sampler, in sampler2D AnimatedTexture2Sampler)
{
	AnimationData data = GetAnimationData(0);
	
	float4 color = BaseColor;
	color = Animate(color, MaskTextureSampler, MaskTexcoord, AnimatedTextureSampler, AnimatedTexcoord.xy, data);
	
#ifdef NUM_ANIMATIONS_2
	data = GetAnimationData(1);
	color = Animate(color, MaskTexture2Sampler, MaskTexcoord, AnimatedTexture2Sampler, AnimatedTexcoord.zw, data);
#endif	
	
	return color;
}

]]
}

