Includes = {
}


VertexStruct VS_INPUT
{
    float2 vPosition  : POSITION;
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
	MainCode VertexColor
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
			float4 vPosition = float4( v.vPosition.x, v.vPosition.y, 0, 1 );
		    Out.vPosition  	= mul( Mat, vPosition );	
			Out.vColor		= v.vColor;
		    return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelColor
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    return v.vColor;
		}
		
	]]
}



Effect Color
{
	VertexShader = "VertexColor"
	PixelShader = "PixelColor"
}

