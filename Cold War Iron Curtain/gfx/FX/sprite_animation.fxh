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

float3 Blend(float3 Base, float3 Blend, AnimationData Data)
{
	float3 Result = vec3(0.0);
	
	if (Data.BlendMode == 0) // Add
	{
		Result = Base + Blend;
	}

	if (Data.BlendMode == 1) // Multiply
	{
		Result = Base * Blend;
	}

	if (Data.BlendMode == 2) // Overlay
	{
		Result = lerp(Base * Blend * 2.0, 1.0 - (2.0 * (1.0 - Base) * (1.0 - Blend)), step(0.5, Base));
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

float4 Animate(float4 BaseColor, in sampler2D MaskTexture_, float2 MaskTexcoord, in sampler2D AnimatedTexture_, float2 AnimatedTexcoord, AnimationData Data)
{
    float4 Mask = tex2D( MaskTexture_, MaskTexcoord );
	float4 Anim = vec4(0.0);
			
	if (Data.Type == 3) // Pulse
	{
		Anim = vec4(Data.AnimationOffset);
	}
	else
	{
		Anim = tex2D( AnimatedTexture_, AnimatedTexcoord );
		
		if ((Data.ClampAnimation > 0.0f) && (AnimatedTexcoord.y < 0.0 || AnimatedTexcoord.y > 1.0))
			Mask.a = 0.0;
	}

	float animationAlpha = Data.BlendFactor * Mask.a * Anim.a;
	return float4(lerp(BaseColor.rgb, Blend(BaseColor.rgb, Anim.rgb * Mask.rgb, Data), animationAlpha), max(BaseColor.a, animationAlpha));
}

float4 Animate(float4 BaseColor, float2 MaskTexcoord, float4 AnimatedTexcoord, in sampler2D MaskTexture_, in sampler2D AnimatedTexture_, in sampler2D MaskTexture2_, in sampler2D AnimatedTexture2_)
{
	AnimationData data = GetAnimationData(0);
	
	float4 color = BaseColor;
	color = Animate(color, MaskTexture_, MaskTexcoord, AnimatedTexture_, AnimatedTexcoord.xy, data);
	
#ifdef NUM_ANIMATIONS_2
	data = GetAnimationData(1);
	color = Animate(color, MaskTexture2_, MaskTexcoord, AnimatedTexture2_, AnimatedTexcoord.zw, data);
#endif	
	
	return color;
}

]]
}

