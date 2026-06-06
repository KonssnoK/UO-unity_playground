# How the Enhanced Client renders (from `Shaders.uop`)

`Shaders.uop` ships **12 plain-HLSL shaders** (D3D9, `ps_2_0`/`vs_1_1`/`vs_2_0`,
with `//#param` permutation directives). They are the **ground truth** for the EC
rendering model — far more authoritative than guessing from output. Extracted
sources: `tools/ec_research/shaders_extracted/`.

## Hue / recolour model — DEFINITIVE

The whole EC hue system is three lines of `uosprite.psh`:

```hlsl
float4 colorout = tex2D(SpriteSampler, uv0);          // base sprite pixel
colorout.a *= IN.color.a;

if (any(IN.texCoord1.xy)) {                            // texCoord1 != 0 -> apply hue
    IN.texCoord1.x += colorout.r * (255.0/1024.0);    // RED channel picks the ramp column
    float4 hue = tex2D(HueSampler, IN.texCoord1);      // HueSampler = build/hues/hues.dds (1024^2)
    hue.a *= colorout.a;
    #if HAS_HUEMASK_TEX
        float mask = tex2D(HueMaskSampler, uv0).a;     // per-pixel mask (the sprite's mask DDS, alpha)
        colorout = lerp(colorout, hue, mask);          // 0 = keep original, 1 = fully hued
    #else
        colorout = hue;                                // full hue
    #endif
}
```

Confirmed facts (these tie the [Hues.md](Hues.md) findings to the actual draw):

- **The hue index is the pixel's RED channel** (`colorout.r`) → it selects the
  *column* (intensity step) of the hue ramp. `texCoord1.y` carries the **hue id**
  (the ramp *row* — and `row == hue id`, see Hues.md).
- **`HueSampler` is `build/hues/hues.dds`** (entry 1, 1024×1024 BGRA). The
  `c_fHuePixelUVOffset = 255/1024` + the "four 255-pixel columns" comment confirm
  the ramp is sampled with a 255-step column.
- **`HueMaskSampler.a` is the per-pixel partial-hue mask** — `lerp(original, hued,
  mask)`. With no mask texture the sprite is fully hued. This is EC's equivalent
  of CC's `R==G==B` partial-hue test, but explicit per-pixel.
- `texCoord1 == (0,0)` ⇒ **no hue** (the "hue 0" / pass-through case).

`uospriteui.psh` (gumps/UI) is identical **minus** the lighting step below.

## Lighting

The last block of `uosprite.psh`:

```hlsl
if (any(IN.color.rgb))
    colorout.rgb = IN.color.rgb * lerp(0.1f, 0.9f, colorout.r);
```

So **world lighting = the vertex `COLOR0` (a light colour) modulated by the
pixel's red-luminance**, clamped to the 0.1–0.9 range (never fully black/white).
UI sprites skip this (no `color.rgb` term).

## Effects shader (`unnamed_9`, `EffectSampler`)

Spell/visual effects use a separate pixel shader with `HAS_HUE_TEX`,
`HAS_GRUNGE_TEX`, `IS_ETHEREAL` permutations:

- Hue index here is **proper luminance** `dot(rgb, {0.2125,0.7154,0.0721})` (Rec.709),
  not just red — effects need accurate luminance.
- `IS_ETHEREAL` tints toward `{0, 0.01, 0.025}` (the translucent-blue ethereal
  mount look); `HAS_GRUNGE_TEX` multiplies a grunge overlay.

## Post-processing — EC has a full HDR pipeline (CC has none)

`Post Process shader` (`ps_2_0`) implements a multi-pass chain selected by
`TECHNIQUE_INDEX`:

| idx | technique | purpose |
|----:|-----------|---------|
| 0 | DownScale4x4 | ⅟₁₆ downsample (×`LumaScale`=0.1) |
| 1 | GaussBlur5x5 | 13-tap gaussian |
| 2 | DownScale2x2 | ¼ downsample |
| 3 | Bloom | bright-pass bloom |
| 4 | BloomFinal | composite bloom (×`BloomScale`=2.0) |
| 5 | Monochrome | desaturate |
| 6 | Tonemap | HDR → LDR tonemap (×`Luminance`=2.0) |
| 7 | BrightPass | extract bright regions |

So EC composites the world to an offscreen target, then bloom + tonemap. A
faithful EC look needs this post chain; a CC-targeted port can skip it.

## Death effect

`Death effect shader` simply runs the whole screen through Monochrome
(`dot(rgb, {0.2125,0.7154,0.0721})`) — the grayscale "you are dead" view.

## Vertex shaders

- World sprites/terrain: `worldPosition = mul(pos, worldTransform); screenPos =
  mul(float4(worldPos,1), viewProjMatrix)` — standard world→view-proj.
- UI (`unnamed_8`, `vs_2_0`): screen-space transform via `screenParams`
  (`pos.x*sx+sz-1`, …), optional vertex colours / texture.

## Practical takeaways for the ClassicUO EC port

1. **Hue:** index `build/hues/hues.dds` by `(hueId_row, red_column)`; lerp by the
   sprite's mask-DDS alpha for partial hue. This is exactly reproducible.
2. **Lighting:** modulate by a per-vertex light colour × `lerp(0.1,0.9,red)`.
3. **Bloom/tonemap** are EC-only polish — optional for a CC-compatible client.
4. The render-state details (blend modes, texture stages per draw) are best
   confirmed by hooking D3D9 at runtime — see [RuntimeTracing.md](RuntimeTracing.md).
