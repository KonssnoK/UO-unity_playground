Shader "UO/TerrainBlend" {
    Properties {
        _TerrainTextures ("Terrain Array", 2DArray) = "" {}
        _TileIndexMap ("Tile Index Map", 2D) = "black" {}
        _Repetition ("Default Repetition", Float) = 0.25
        _BlendWidth ("Blend Width", Range(0.01, 0.5)) = 0.15
        _WaterAlpha ("Water Alpha Mask", 2D) = "white" {}
        _WaterTexIdx ("Water Texture Index", Int) = -1
        _WaterSpeed ("Water Animation Speed", Float) = 0.03
        _WaterColor ("Water Tint", Color) = (0.1, 0.4, 0.6, 1)
        [Toggle] _DebugIndices ("Debug: Show Indices", Float) = 0
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
            sampler2D _WaterAlpha;
            float _Repetition;
            float _Repetitions[64];
            float _BlendWidth;
            float _DebugIndices;
            int _WaterTexIdx;
            float _WaterSpeed;
            fixed4 _WaterColor;

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
                float2 uv = (tilePos + 1.5) / 66.0;
                return (int)round(tex2Dlod(_TileIndexMap, float4(uv, 0, 0)).r * 255.0);
            }

            fixed4 indexToColor(int idx) {
                if (idx == 0) return fixed4(1, 0, 0, 1);
                if (idx == 1) return fixed4(0, 1, 0, 1);
                if (idx == 2) return fixed4(0, 0, 1, 1);
                if (idx == 3) return fixed4(1, 1, 0, 1);
                if (idx == 4) return fixed4(1, 0, 1, 1);
                if (idx == 5) return fixed4(0, 1, 1, 1);
                if (idx == 6) return fixed4(1, 0.5, 0, 1);
                if (idx == 7) return fixed4(0.5, 0, 1, 1);
                if (idx == 8) return fixed4(0, 0.5, 0, 1);
                if (idx == 9) return fixed4(0.5, 0.5, 0, 1);
                if (idx == 10) return fixed4(0, 0.5, 0.5, 1);
                if (idx == 11) return fixed4(0.5, 0, 0, 1);
                if (idx == 12) return fixed4(1, 1, 0.5, 1);
                if (idx == 13) return fixed4(0.5, 1, 0.5, 1);
                if (idx == 14) return fixed4(0.5, 0.5, 1, 1);
                return fixed4(idx / 20.0, idx / 20.0, idx / 20.0, 1);
            }

            fixed4 sampleTerrain(float2 gridUV, int idx) {
                float rep = _Repetitions[idx];
                if (rep <= 0) rep = _Repetition;
                return UNITY_SAMPLE_TEX2DARRAY(_TerrainTextures, float3(gridUV * rep, idx));
            }

            // Sample water with animated scrolling UVs
            fixed4 sampleWater(float2 gridUV) {
                float rep = _Repetitions[_WaterTexIdx];
                if (rep <= 0) rep = _Repetition;
                float2 waterUV = gridUV * rep;

                // Two layers scrolling in different directions for organic movement
                float t = _Time.y * _WaterSpeed;
                float2 uv1 = waterUV + float2(t, t * 0.7);
                float2 uv2 = waterUV + float2(-t * 0.5, t * 0.3);

                fixed4 w1 = UNITY_SAMPLE_TEX2DARRAY(_TerrainTextures, float3(uv1, _WaterTexIdx));
                fixed4 w2 = UNITY_SAMPLE_TEX2DARRAY(_TerrainTextures, float3(uv2, _WaterTexIdx));

                // Blend the two layers and tint
                fixed4 water = lerp(w1, w2, 0.5);
                water.rgb = water.rgb * 0.7 + _WaterColor.rgb * 0.3;
                return water;
            }

            // Sample terrain or water depending on index
            fixed4 sampleTerrainOrWater(float2 gridUV, int idx) {
                if (_WaterTexIdx >= 0 && idx == _WaterTexIdx)
                    return sampleWater(gridUV);
                return sampleTerrain(gridUV, idx);
            }

            fixed4 frag(v2f i) : SV_Target {
                float2 shifted = i.uv - 0.5;
                float2 tileA = floor(shifted);
                float2 f = shifted - tileA;

                int idx00 = sampleTileIndex(tileA);

                if (_DebugIndices > 0.5) {
                    return indexToColor(idx00);
                }

                // Look up the 4 surrounding tiles' texture indices
                int idx10 = sampleTileIndex(tileA + float2(1, 0));
                int idx01 = sampleTileIndex(tileA + float2(0, 1));
                int idx11 = sampleTileIndex(tileA + float2(1, 1));

                // Check if any neighbor is water — use alpha mask for coast blending
                bool anyWater = _WaterTexIdx >= 0 && (
                    idx00 == _WaterTexIdx || idx10 == _WaterTexIdx ||
                    idx01 == _WaterTexIdx || idx11 == _WaterTexIdx);

                // Discard pure water pixels — water sprites render behind mesh
                // and show through these holes. Keep coast blend pixels.
                if (_WaterTexIdx >= 0 && idx00 == _WaterTexIdx &&
                    idx10 == _WaterTexIdx && idx01 == _WaterTexIdx && idx11 == _WaterTexIdx) {
                    discard;
                }

                // Early out: if all 4 are the same, no blend needed
                if (idx00 == idx10 && idx10 == idx01 && idx01 == idx11) {
                    return sampleTerrain(i.uv, idx00);
                }

                // Sharpen blend for non-water edges
                float2 bf = smoothstep(0.5 - _BlendWidth, 0.5 + _BlendWidth, f);

                if (anyWater) {
                    // Coast edge: some corners are water, some are land.
                    // Discard water-heavy pixels (water sprites show through),
                    // render land-heavy pixels as terrain.
                    float w00 = (idx00 == _WaterTexIdx) ? 1.0 : 0.0;
                    float w10 = (idx10 == _WaterTexIdx) ? 1.0 : 0.0;
                    float w01 = (idx01 == _WaterTexIdx) ? 1.0 : 0.0;
                    float w11 = (idx11 == _WaterTexIdx) ? 1.0 : 0.0;

                    float topW = lerp(w00, w10, bf.x);
                    float botW = lerp(w01, w11, bf.x);
                    float waterWeight = lerp(topW, botW, bf.y);

                    // Discard where mostly water — let water sprites show through
                    if (waterWeight > 0.5) discard;

                    // Render land texture for the land portion
                    int landIdx = idx00;
                    if (landIdx == _WaterTexIdx) landIdx = idx10;
                    if (landIdx == _WaterTexIdx) landIdx = idx01;
                    if (landIdx == _WaterTexIdx) landIdx = idx11;

                    return sampleTerrain(i.uv, landIdx);
                }

                // Standard terrain blending (no water involved)
                fixed4 c00 = sampleTerrain(i.uv, idx00);
                fixed4 c10 = sampleTerrain(i.uv, idx10);
                fixed4 c01 = sampleTerrain(i.uv, idx01);
                fixed4 c11 = sampleTerrain(i.uv, idx11);

                fixed4 top = lerp(c00, c10, bf.x);
                fixed4 bottom = lerp(c01, c11, bf.x);
                return lerp(top, bottom, bf.y);
            }
            ENDCG
        }
    }
    FallBack "Diffuse"
}
