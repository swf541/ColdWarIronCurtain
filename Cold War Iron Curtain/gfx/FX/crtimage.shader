Includes = {
	"buttonstate.fxh"
	"sprite_animation.fxh"
}

PixelShader =
{
	Samplers =
	{
		MapTexture =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		MaskTexture =
		{
			Index = 1
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		AnimatedTexture =
		{
			Index = 2
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		MaskTexture2 =
		{
			Index = 3
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
		AnimatedTexture2 =
		{
			Index = 4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_OUTPUT
{
	float4  vPosition : PDX_POSITION;
	float2  vTexCoord : TEXCOORD0;
@ifdef ANIMATED
	float4  vAnimatedTexCoord : TEXCOORD1;
@endif
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  = mul( WorldViewProjectionMatrix, float4( v.vPosition.xyz, 1 ) );
		
		    Out.vTexCoord = v.vTexCoord;
			Out.vTexCoord += Offset;
			
		#ifdef ANIMATED
			Out.vAnimatedTexCoord = GetAnimatedTexcoord(v.vTexCoord);	
		#endif
		
		    return Out;
		}
	]]
}

PixelShader =
{
	MainCode PixelShaderUp
	[[
		static float valueForNoise = 0.5f;
		float rand () {
			return frac(sin(Time)*1e4);
		}
		float modd(float x, float y) {
			return x - (y * floor(x/y));
		}
		float ramp(float y, float start, float end)
		{
			float inside = step(start,y) - step(end,y);
			float fact = (y-start)/(end-start)*inside;
			return ((1.0f-fact) * inside);
			//return 1.0f;
		}
		float myramp(float y, float start, float end)
		{
			float inside = step(start,y) - step(end,y);
			float fact = (y-start)/(end-start)*inside;
			return ((1.0f-fact) * inside);
			//return 1.0f;
		}
		float onOff(float a, float b, float c)
		{
			return step(c, sin(Time + a*cos(Time*b)));
		}

		float2 screenDistort(float2 uv)
		{
			uv -= float2(0.5f,0.5f);
			uv = uv*1.2f*(1.0f/1.2f+2.0f*uv.x*uv.x*uv.y*uv.y);
			uv += float2(0.5f,0.5f);
			return uv;
		}
		float rand_1_05(float2 uv)
		{
			float2 noises = (frac(sin(dot(uv ,float2(12.9898,78.233)*2.0)) * 43758.5453));
			return abs(noises.x + noises.y) * 0.5;
		}
		float stripes(float2 uv)
		{
			
			float noi = rand_1_05(uv*float2(0.5f,1.0f) + float2(1.0f,3.0f));
			return ramp(modd(uv.y*4.0f + Time/2.0f+sin(Time + sin(Time*0.63f)),1.0f),0.5f,0.6f)*noi;
			//return 1.0f;
		}
		
		float hash( float n )
		{
			return frac(sin(n)*43758.5453);
		}
		float gen_noise( float3 x )
		{
			// The noise function returns a value in the range -1.0f -> 1.0f

			float3 p = floor(x);
			float3 f = frac(x);

			f       = f*f*(3.0-2.0*f);
			float n = p.x + p.y*57.0 + 113.0*p.z;

			return lerp(lerp(lerp( hash(n+0.0), hash(n+1.0),f.x),
						   lerp( hash(n+57.0), hash(n+58.0),f.x),f.y),
					   lerp(lerp( hash(n+113.0), hash(n+114.0),f.x),
						   lerp( hash(n+170.0), hash(n+171.0),f.x),f.y),f.z);
		}
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float2 uv = v.vTexCoord;
			float2 dynamicUV = float2(uv.x+sin(Time), uv.y+sin(Time));
			uv = screenDistort(uv);
			float2 screenUV = uv;
			float2 look = uv;
			float window = 1.0f/(1.0f+20.0f*(look.y-mod(Time/4.0f,1.0f))*(look.y-mod(Time/4.0f,1.0f)));
			look.x = look.x + sin(look.y*10.0f + Time)/50.0f*onOff(4.0f,4.0f,0.3f)*(1.0f+cos(Time*80.0f))*window*0.02f; 
			float vShift = 0.4f*onOff(2.0f,3.0f,0.9f)*(sin(Time)*sin(Time*20.0f) + 
												 (0.5f + 0.1f*sin(Time*200.0f)*cos(Time)));
			look.y = mod(look.y + vShift*0.002f, 1.0f); 
			uv = look;
			
			
			
			float2 uvR = uv;
			float2 uvB = uv;

			uvR.x = uv.x * 1.0f - rand() * 0.02f * 0.1f;
			uvB.y = uv.y * 1.0f + rand() * 0.02f * 0.06f; 
			
			 
			if(uv.y < rand() && uv.y > rand() -0.1f && sin(Time) < 0.0f)
			{
				uv.x = (uv + 0.008f * rand()).x;
			}
			
			
			float4 c = float4(1.0f, 1.0f, 1.0f, 1.0f);
			c.x = tex2D( MapTexture, uvR ).x;
			c.y = tex2D( MapTexture, uv ).y;
			c.z = tex2D( MapTexture, uvB ).z;
			c.w = tex2D( MapTexture, uvB ).w;
			
			float scanline = sin( uv.y * 800.0f * rand())/30.0f; 
			c *= 1.0f - scanline; 
			
		    float4 OutColor = tex2D( MapTexture, v.vTexCoord );
			OutColor = c;
			 
			float2 vig_uv = uv * (1.0f - uv.xy);    //vec2(1.0)- uv.yx; -> 1.-u.yx; Thanks FabriceNeyret !
    
			float vig = vig_uv.x*vig_uv.y * 50.0f; // multiply with sth for intensity
			if (vig>1.0f) {vig = 1.0f;}
			vig_uv = v.vTexCoord * (1.0f - v.vTexCoord.xy);
			vig = pow(vig, 0.45f);		 	//vec2(1.0)- uv.yx; -> 1.-u.yx; Thanks FabriceNeyret !
			OutColor.rgb = OutColor.rgb * float3(vig,vig,vig);
			vig = vig_uv.x*vig_uv.y * 85.0f; // multiply with sth for intensity
			if (vig>1.0f) {vig = 1.0f;}
			vig = pow(vig, 0.8f); 
			OutColor.rgb = OutColor.rgb * float3(vig,vig,vig);
			  
			float vigAmt = 3.1f+0.05f+0.01f*sin(Time + 0.05f*cos(Time*5.0f));
			float vignette = (1.0f-vigAmt*(uv.y-0.5f)*(uv.y-0.5f))*1.0f*(1.0f-vigAmt*(uv.x-0.5f)*(uv.x-0.5f)); 
			vigAmt = 3.1f+0.05f+0.01f*sin(Time + 0.05f*cos(Time*5.0f));
			vignette = (1.0f-vigAmt*(v.vTexCoord.y-0.5f)*(v.vTexCoord.y-0.5f))*1.0f*(1.0f-vigAmt*(v.vTexCoord.x-0.5f)*(v.vTexCoord.x-0.5f)); 
			OutColor.rgb = OutColor.rgb * (12.0f+modd(uv.y*30.0f+Time,1.0f))/13.0f; 
			
			OutColor *= Color;
			return OutColor;
		}
	]]

	MainCode PixelShaderDisable
	[[
		static float valueForNoise = 0.5f;
		float rand () {
			return frac(sin(Time)*1e4);
		}
		float modd(float x, float y) {
			return x - (y * floor(x/y));
		}
		float ramp(float y, float start, float end)
		{
			float inside = step(start,y) - step(end,y);
			float fact = (y-start)/(end-start)*inside;
			return ((1.0f-fact) * inside);
			//return 1.0f;
		}
		float myramp(float y, float start, float end)
		{
			float inside = step(start,y) - step(end,y);
			float fact = (y-start)/(end-start)*inside;
			return ((1.0f-fact) * inside);
			//return 1.0f;
		}
		float onOff(float a, float b, float c)
		{
			return step(c, sin(Time + a*cos(Time*b)));
		}

		float2 screenDistort(float2 uv)
		{
			uv -= float2(0.5f,0.5f);
			uv = uv*1.2f*(1.0f/1.2f+2.0f*uv.x*uv.x*uv.y*uv.y);
			uv += float2(0.5f,0.5f);
			return uv;
		}
		float rand_1_05(float2 uv)
		{
			float2 noises = (frac(sin(dot(uv ,float2(12.9898,78.233)*2.0)) * 43758.5453));
			return abs(noises.x + noises.y) * 0.5;
		}
		float stripes(float2 uv)
		{
			
			float noi = rand_1_05(uv*float2(0.5f,1.0f) + float2(1.0f,3.0f));
			return ramp(modd(uv.y*4.0f + Time/2.0f+sin(Time + sin(Time*0.63f)),1.0f),0.5f,0.6f)*noi;
			//return 1.0f;
		}
		
		float hash( float n )
		{
			return frac(sin(n)*43758.5453);
		}
		float gen_noise( float3 x )
		{
			// The noise function returns a value in the range -1.0f -> 1.0f

			float3 p = floor(x);
			float3 f = frac(x);

			f       = f*f*(3.0-2.0*f);
			float n = p.x + p.y*57.0 + 113.0*p.z;

			return lerp(lerp(lerp( hash(n+0.0), hash(n+1.0),f.x),
						   lerp( hash(n+57.0), hash(n+58.0),f.x),f.y),
					   lerp(lerp( hash(n+113.0), hash(n+114.0),f.x),
						   lerp( hash(n+170.0), hash(n+171.0),f.x),f.y),f.z);
		}
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			
	
			float2 uv = v.vTexCoord;
			float2 dynamicUV = float2(uv.x+sin(Time), uv.y+sin(Time));
			uv = screenDistort(uv);
			float2 screenUV = uv;
			float2 look = uv;
			float window = 1.0f/(1.0f+20.0f*(look.y-mod(Time/4.0f,1.0f))*(look.y-mod(Time/4.0f,1.0f)));
			look.x = look.x + sin(look.y*10.0f + Time)/50.0f*onOff(4.0f,4.0f,0.3f)*(1.0f+cos(Time*80.0f))*window*0.02f; 
			float vShift = 0.4f*onOff(2.0f,3.0f,0.9f)*(sin(Time)*sin(Time*20.0f) + 
												 (0.5f + 0.1f*sin(Time*200.0f)*cos(Time)));
			look.y = mod(look.y + vShift*0.002f, 1.0f); 
			uv = look;
			
			
			
			float2 uvR = uv;
			float2 uvB = uv;

			uvR.x = uv.x * 1.0f - rand() * 0.02f * 0.1f;
			uvB.y = uv.y * 1.0f + rand() * 0.02f * 0.06f; 
			
			 
			if(uv.y < rand() && uv.y > rand() -0.1f && sin(Time) < 0.0f)
			{
				uv.x = (uv + 0.008f * rand()).x;
			}
			
			
			float4 c = float4(1.0f, 1.0f, 1.0f, 1.0f);
			c.x = tex2D( MapTexture, uvR ).x;
			c.y = tex2D( MapTexture, uv ).y;
			c.z = tex2D( MapTexture, uvB ).z;
			c.w = tex2D( MapTexture, uvB ).w;
			
			float scanline = sin( uv.y * 800.0f * rand())/30.0f; 
			c *= 1.0f - scanline; 
			
		    float4 OutColor = tex2D( MapTexture, v.vTexCoord );
			OutColor = c;
			 
			float2 vig_uv = uv * (1.0f - uv.xy);    //vec2(1.0)- uv.yx; -> 1.-u.yx; Thanks FabriceNeyret !
    
			float vig = vig_uv.x*vig_uv.y * 50.0f; // multiply with sth for intensity
			if (vig>1.0f) {vig = 1.0f;}
			vig_uv = v.vTexCoord * (1.0f - v.vTexCoord.xy);
			vig = pow(vig, 0.45f);		 	//vec2(1.0)- uv.yx; -> 1.-u.yx; Thanks FabriceNeyret !
			OutColor.rgb = OutColor.rgb * float3(vig,vig,vig);
			vig = vig_uv.x*vig_uv.y * 85.0f; // multiply with sth for intensity
			if (vig>1.0f) {vig = 1.0f;}
			vig = pow(vig, 0.8f); 
			OutColor.rgb = OutColor.rgb * float3(vig,vig,vig);
			  
			float vigAmt = 3.1f+0.05f+0.01f*sin(Time + 0.05f*cos(Time*5.0f));
			float vignette = (1.0f-vigAmt*(uv.y-0.5f)*(uv.y-0.5f))*1.0f*(1.0f-vigAmt*(uv.x-0.5f)*(uv.x-0.5f)); 
			vigAmt = 3.1f+0.05f+0.01f*sin(Time + 0.05f*cos(Time*5.0f));
			vignette = (1.0f-vigAmt*(v.vTexCoord.y-0.5f)*(v.vTexCoord.y-0.5f))*1.0f*(1.0f-vigAmt*(v.vTexCoord.x-0.5f)*(v.vTexCoord.x-0.5f)); 
			OutColor.rgb = OutColor.rgb * (12.0f+modd(uv.y*30.0f+Time,1.0f))/13.0f; 
			
			OutColor *= Color;
			return OutColor;
		}
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
}


Effect Up
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderUp"
}

Effect Down
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderUp"
}

Effect Disable
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderDisable"
}

Effect Over
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderUp"
}

