//#target vs_1_1

struct VS_INPUT
{
	float4 position	: POSITION;	
	float2 texCoord0: TEXCOORD0;	// sprite uv
	float2 texCoord1: TEXCOORD1;	// world-space uv
	float2 texCoord2: TEXCOORD2;	// offset into hue texture
	float4 color	: COLOR0;		// diffuse
};

struct VS_OUTPUT
{
	float4 screenPosition	: POSITION;
    float2 texCoord0		: TEXCOORD0;
	float2 texCoord1		: TEXCOORD1;
	float4 color			: COLOR0;
};

VS_OUTPUT main(	uniform float4x3 worldTransform,	
				uniform float4x4 viewProjMatrix,
				uniform float3x3 spriteTransform,
				const VS_INPUT IN )
{
	VS_OUTPUT OUT;
	
	float4 worldPosition = float4(mul(IN.position, worldTransform), 1.0f);
	OUT.screenPosition = mul(worldPosition, viewProjMatrix);
    OUT.texCoord0.xy = mul(float3(IN.texCoord0.xy, 1.0f), spriteTransform).xy;
    OUT.texCoord1 = IN.texCoord2;
		
	if (any(IN.color.rgb - 1.0f))
	{
		OUT.color = IN.color;
	}
	else
	{
		OUT.color = float4(0.0f, 0.0f, 0.0f, IN.color.a);
	}
		
	return OUT;
}