//#target vs_1_1

struct VS_INPUT
{
	float4 position	: POSITION;
	float2 texCoord0: TEXCOORD0;
	float4 color	: COLOR0;
};

struct VS_OUTPUT
{
	float4 screenPosition	: POSITION;
    float2 texCoord0		: TEXCOORD0;
    float2 texCoord1		: TEXCOORD1;
	float4 color			: COLOR0;
};

// Note: this is hardcoded for a 1024x1024 hue texture with four 256-pixel columns
static const float c_fHueUOffset = 256.0f / 1024.0f;
static const float c_fHueVOffset = 1.0f / 1024.0f;

VS_OUTPUT main(	uniform float4x3 worldTransform,	
				uniform float4x4 viewProjMatrix,
				uniform float3x3 spriteTransform,
				uniform float hueIndex,
				const VS_INPUT IN )
{
	VS_OUTPUT OUT;
	
	float4 worldPosition = float4(mul(IN.position, worldTransform).xyz, 1.0f);
	OUT.screenPosition = mul(worldPosition, viewProjMatrix);
    OUT.texCoord0 = mul(float3(IN.texCoord0.xy, 1.0f), spriteTransform).xy;
    
    // calc hue uv here, hue texture is 1024x1024 with each row of 256 pixels a hue
	OUT.texCoord1.y = modf(hueIndex * c_fHueVOffset, OUT.texCoord1.x);
	OUT.texCoord1.x *= c_fHueUOffset;
	
	OUT.color = IN.color;
    
	return OUT;
}