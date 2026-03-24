Shader "UO/WaterSprite" {
    Properties {
        _MainTex ("Water Texture", 2D) = "white" {}
        _WaterAlpha ("Water Alpha Mask", 2D) = "white" {}
        _Speed ("Animation Speed", Float) = 0.04
        _Tint ("Water Tint", Color) = (0.05, 0.3, 0.5, 0.85)
    }
    SubShader {
        Tags { "Queue"="Geometry-10" "RenderType"="Opaque" }
        ZWrite On
        Cull Off

        Pass {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            sampler2D _MainTex;
            sampler2D _WaterAlpha;
            float _Speed;
            fixed4 _Tint;

            struct appdata {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float4 color : COLOR;
            };

            struct v2f {
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
                float2 worldUV : TEXCOORD1;
                float4 color : COLOR;
            };

            v2f vert(appdata v) {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                // Use world position for consistent UV offset across tiles
                float3 wp = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.worldUV = wp.xy * 0.3;
                o.color = v.color;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target {
                float t = _Time.y * _Speed;

                // Two scrolling layers based on world position for seamless variation
                float2 uv1 = i.worldUV + float2(t, t * 0.7);
                float2 uv2 = i.worldUV + float2(-t * 0.6, t * 0.4);

                fixed4 w1 = tex2D(_MainTex, uv1);
                fixed4 w2 = tex2D(_MainTex, uv2);

                // Alpha mask for surface variation
                float2 alphaUV = i.worldUV * 2.0 + float2(t * 0.3, -t * 0.2);
                float alphaMask = tex2D(_WaterAlpha, alphaUV).r;

                // Blend layers
                fixed4 water = lerp(w1, w2, 0.5);
                water.rgb = water.rgb * 0.6 + _Tint.rgb * 0.4;

                // Subtle brightness variation from alpha mask
                water.rgb *= 0.85 + alphaMask * 0.3;
                water.a = 1.0;

                return water * i.color;
            }
            ENDCG
        }
    }
}
