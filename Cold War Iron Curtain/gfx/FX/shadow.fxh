PixelShader = 
{
	Code
	[[

	float CalculateShadow( float4 vShadowProj, sampler2DShadow ShadowSample )
	{
		//float fShadowTerm = 0.0f;
		//fShadowTerm = tex2Dproj( ShadowSample, vShadowProj ).r;
		//fShadowTerm = ( fShadowTerm < 0.99f && fShadowTerm < (vShadowProj.z - 0.001f) ) ? 0.1f : 1.0f;
		//return fShadowTerm;

		// Generate the texture co-ordinates for a PCF kernel
		float4 vTexCoords[5];

		// Texel size
		float fTexelSize = 0.5f / 2048.0f;

		// Generate the tecture co-ordinates for the specified depth-map size
		vTexCoords[0] = vShadowProj + float4( -fTexelSize, 0.0f, 0.0f, 0.0f );
		vTexCoords[1] = vShadowProj + float4( 0.0f, fTexelSize, 0.0f, 0.0f );
		vTexCoords[2] = vShadowProj + float4(  fTexelSize, 0.0f, 0.0f, 0.0f );
		vTexCoords[3] = vShadowProj + float4( 0.0f, -fTexelSize, 0.0f, 0.0f );
		vTexCoords[4] = vShadowProj;
		
		const float fBias = 0.001f;
		
		// Sample each of them checking whether the pixel under test is shadowed or not
		float fShadowTerm = 0.0f;
		for( int i = 0; i < 5; i++ )
		{
			float A = tex2Dproj( ShadowSample, vTexCoords[i] ).r;
			float B = vShadowProj.z - fBias;
			
			// Texel is shadowed
			fShadowTerm += ( A < 0.99f && A < B ) ? 0.1f : 1.0f;
		}
		
		// Get the average
		fShadowTerm = fShadowTerm / 5.0f;
		return fShadowTerm;
	}

	float GetShadowScaled( float fScaler, in float4 vBlurTexCoord, in sampler2DShadow ShadowSample )
	{
		fScaler = saturate( fScaler );
		float vShadowValue = tex2Dproj( ShadowSample, vBlurTexCoord ).r;
		
		//Hide shadow after a certain distance
		vShadowValue += (1.0 - ShadowFadeFactor);
		vShadowValue = saturate( vShadowValue );
		
		return ( 1.0 - fScaler ) + fScaler * vShadowValue;
	}

	]]
}