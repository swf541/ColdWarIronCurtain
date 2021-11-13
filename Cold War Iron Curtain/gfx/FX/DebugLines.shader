
VertexStruct VS_INPUT
{
    float3 vPosition  : POSITION;
	float4 vColor	  : COLOR;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
 	float4  vColor	  : TEXCOORD1;
};


ConstantBuffer( 0, 0 )
{
	float4x4 Mat;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  	= mul( Mat, float4( v.vPosition.rgb, 1.0f ) );	
			Out.vColor		= v.vColor;
		    return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		  	float4 OutColor = v.vColor;
		    return OutColor;
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = no
	WriteMask = "RED|GREEN|BLUE"
}


Effect DebugLines
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
}

