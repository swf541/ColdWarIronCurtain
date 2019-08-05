PixelShader = 
{
	ConstantBuffer( 2, 62 ) # after shadowmap constants
	{
		float4 GridStart_InvCellSize;
	}

	Code
	[[

	static const float2 INV_LIGHT_INDEX_TEXTURE_SIZE = float2(1.0 / 64.0, 1.0 / 64.0);
	static const float INV_LIGHT_DATA_TEXTURE_SIZE = float(1.0 / 128.0);

	float2 GetLightIndexUV(float3 WorldSpacePos)
	{
		float2 XZ = WorldSpacePos.xz;
		XZ -= GridStart_InvCellSize.xy;
		
		float2 cellIndex = XZ * GridStart_InvCellSize.zw;
		return cellIndex * INV_LIGHT_INDEX_TEXTURE_SIZE;
	}

	void CalculatePointLights(LightingProperties aProperties, in sampler2D LightData_, in sampler2D LightIndexMap, inout float3 aDiffuseLightOut, inout float3 aSpecularLightOut)
	{
		float2 LightIndexUV = GetLightIndexUV(aProperties._WorldSpacePos);
		float4 LightIndices = tex2Dlod(LightIndexMap, float4(LightIndexUV, 0, 0));
		
		for (int i = 0; i < 4; ++i)
		{
			float LightIndex = LightIndices[i] * 255.0;
			if (LightIndex >= 255.0)
				break;
			
			float4 LightData1 = tex2Dlod(LightData_, float4((LightIndex * 2 + 0.5) * INV_LIGHT_DATA_TEXTURE_SIZE, 0, 0, 0));
			float4 LightData2 = tex2Dlod(LightData_, float4((LightIndex * 2 + 1.5) * INV_LIGHT_DATA_TEXTURE_SIZE, 0, 0, 0));
			PointLight pointlight = GetPointLight(LightData1, LightData2);
				
			CalculatePointLight(pointlight, aProperties, aDiffuseLightOut, aSpecularLightOut);
		}
	}

	/*
	float2 LightIndexUV = GetLightIndexUV(lightingProperties._WorldSpacePos);
	if (LightIndexUV.x < 0 || LightIndexUV.x > 1 || LightIndexUV.y < 0 || LightIndexUV.y > 1)
		vColor = float3(1, 0, 0);
	else
		vColor = float3(0, 1, 0);
	vColor = tex2D(LightIndexMap, LightIndexUV).rgb; // 0 = b, 1 = g, 2 = r, 3 = a
	*/

	]]
}