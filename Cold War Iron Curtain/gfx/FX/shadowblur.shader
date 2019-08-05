Includes = {
}

PixelShader =
{
	Samplers =
	{
		BlurSample =
		{
			Index = 0
			MagFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition  : POSITION;
    float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4  	vGaussianOffsetsWeights[2];
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT In )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= In.vPosition;
		    Out.vTexCoord  	= In.vTexCoord;
		
		    return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode HorizontalPixelShader
	[[
		float4 main( VS_OUTPUT In ) : PDX_COLOR
		{
			// Accumulated color
			float fAccum = 0.0f;
		
			float vOffset[3];
			float vWeight[3];
			vOffset[0] = vGaussianOffsetsWeights[0].x;
			vOffset[1] = vGaussianOffsetsWeights[0].y;
			vOffset[2] = vGaussianOffsetsWeights[0].z;	
			vWeight[0] = vGaussianOffsetsWeights[0].w;
			vWeight[1] = vGaussianOffsetsWeights[1].x;
			vWeight[2] = vGaussianOffsetsWeights[1].y;		
			
			float4 OriginalSample = tex2D( BlurSample, In.vTexCoord );
			fAccum = OriginalSample.r * vWeight[0];
			for (int i=1; i<3; i++) {
				fAccum += tex2D( BlurSample, ( In.vTexCoord+float2(vOffset[i], 0.0) ) ).r * vWeight[i];
				fAccum += tex2D( BlurSample, ( In.vTexCoord-float2(vOffset[i], 0.0) ) ).r * vWeight[i];
			}	
		
			return float4( fAccum, OriginalSample.g, OriginalSample.b, 1.0f );	
		}
		
	]]

	MainCode VerticalPixelShader
	[[
		float4 main( VS_OUTPUT In ) : PDX_COLOR
		{
			// Accumulated color
			float fAccum = 0.0f;
		
			float vOffset[3];
			float vWeight[3];
			vOffset[0] = vGaussianOffsetsWeights[0].x;
			vOffset[1] = vGaussianOffsetsWeights[0].y;
			vOffset[2] = vGaussianOffsetsWeights[0].z;	
			vWeight[0] = vGaussianOffsetsWeights[0].w;
			vWeight[1] = vGaussianOffsetsWeights[1].x;
			vWeight[2] = vGaussianOffsetsWeights[1].y;		
			
			float4 OriginalSample = tex2D( BlurSample, In.vTexCoord );
			fAccum = OriginalSample.r * vWeight[0];
			for (int i=1; i<3; i++) {
				fAccum += tex2D( BlurSample, ( In.vTexCoord+float2(0.0, vOffset[i]) ) ).r * vWeight[i];
				fAccum += tex2D( BlurSample, ( In.vTexCoord-float2(0.0, vOffset[i]) ) ).r * vWeight[i];
			}	
			
			return float4( fAccum, OriginalSample.g, OriginalSample.b, 1.0f );	
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = no
	AlphaTest = no
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect ShadowBlurHorizontal
{
	VertexShader = "VertexShader"
	PixelShader = "HorizontalPixelShader"
}

Effect ShadowBlurVertical
{
	VertexShader = "VertexShader"
	PixelShader = "VerticalPixelShader"
}

