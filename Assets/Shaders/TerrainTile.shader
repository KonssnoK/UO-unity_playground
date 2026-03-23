Shader "UO/TerrainBlend" {
    Properties {
        _TerrainTextures ("Terrain Array", 2DArray) = "" {}
        _TileIndexMap ("Tile Index Map", 2D) = "black" {}
        _Repetition ("Default Repetition", Float) = 0.25
        _BlendWidth ("Blend Width", Range(0.01, 0.5)) = 0.15
    }
    SubShader {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.5
            #include "UnityCG.cginc"

            UNITY_DECLARE_TEX2DARRAY(_TerrainTextures);
            sampler2D _TileIndexMap;
            float _Repetition;
            float _Repetitions[64];
            float _BlendWidth;

            struct appdata {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f {
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            v2f vert(appdata v) {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            int sampleTileIndex(float2 tilePos) {
                // Index map is 66x66 with 1-pixel border from neighbors
                // tilePos 0-63 maps to pixels 1-64, border at 0 and 65
                float2 uv = (tilePos + 1.5) / 66.0;
                return (int)round(tex2Dlod(_TileIndexMap, float4(uv, 0, 0)).r * 255.0);
            }

            fixed4 sampleTerrain(float2 gridUV, int idx) {
                float rep = _Repetitions[idx];
                if (rep <= 0) rep = _Repetition;
                return UNITY_SAMPLE_TEX2DARRAY(_TerrainTextures, float3(gridUV * rep, idx));
            }

            fixed4 frag(v2f i) : SV_Target {
                float2 shifted = i.uv - 0.5;
                float2 tileA = floor(shifted);
                float2 f = shifted - tileA;

                // Sharpen blend — only blend in narrow band near tile edges
                f = smoothstep(0.5 - _BlendWidth, 0.5 + _BlendWidth, f);

                // Look up the 4 surrounding tiles' texture indices
                int idx00 = sampleTileIndex(tileA);
                int idx10 = sampleTileIndex(tileA + float2(1, 0));
                int idx01 = sampleTileIndex(tileA + float2(0, 1));
                int idx11 = sampleTileIndex(tileA + float2(1, 1));

                // Early out: if all 4 are the same, no blend needed
                if (idx00 == idx10 && idx10 == idx01 && idx01 == idx11) {
                    return sampleTerrain(i.uv, idx00);
                }

                // Sample each terrain texture
                fixed4 c00 = sampleTerrain(i.uv, idx00);
                fixed4 c10 = sampleTerrain(i.uv, idx10);
                fixed4 c01 = sampleTerrain(i.uv, idx01);
                fixed4 c11 = sampleTerrain(i.uv, idx11);

                // Bilinear blend
                fixed4 top = lerp(c00, c10, f.x);
                fixed4 bottom = lerp(c01, c11, f.x);
                return lerp(top, bottom, f.y);
            }
            ENDCG
        }
    }
    FallBack "Diffuse"
}
