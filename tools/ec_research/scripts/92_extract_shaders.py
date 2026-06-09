"""Extract shader bytecode from Shaders.uop. Probe naming conventions, dump
every shader as a .dxbc file, and disassemble UOStaticTerrainShader-related
shaders if we can identify them."""
import io, sys, struct
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
shaders = UopArchive(EC / 'Shaders.uop')
print(f'Shaders.uop total entries: {len(shaders.by_hash)}')

SEP = chr(92)
candidates = [
    "shaders/uostatic_terrain.vsh",
    "shaders/uostaticterrain.vsh",
    "shaders/UOStaticTerrainShader.vsh",
    "shaders/UOTerrainShader.vsh",
    f"Data{SEP}Shaders{SEP}UOStaticTerrainShader.vsh",
    f"Data{SEP}Shaders{SEP}UOTerrainShader.vsh",
    "data/shaders/uostaticterrain.vsh",
    "data/shaders/uostaticterrain.psh",
    "build/shaders/uostaticterrain.vsh",
    "build/shaders/uostaticterrain.psh",
    "build/shaders/uoterrainshader.vsh",
    "build/shaders/uoterrainshader.psh",
    "shaders/gameterrain_offscreen.vsh",
    "build/shaders/gameterrain_offscreen.vsh",
    "build/shaders/gameterrain_vertexlighting.vsh",
    "build/shaders/gameterrain_vertexlighting.psh",
    "Build/Shaders/UOTerrainShader.vsh",
    "Build/Shaders/GameTerrain_VertexLighting.vsh",
]
print('\n--- probing common naming patterns ---')
hits = 0
for c in candidates:
    h = hash_name(c)
    if h in shaders.by_hash:
        e = shaders.by_hash[h]
        print(f'  HIT  {c}  size={e.decompressed_size}')
        hits += 1
print(f'(probe hits: {hits})')

# Dump every entry — see how many there are, what sizes
sizes = []
for h, e in shaders.by_hash.items():
    sizes.append(e.decompressed_size)
print(f'\nsize stats: min={min(sizes)} max={max(sizes)} count={len(sizes)}')

# Dump first 20 entries' first 32 bytes — DX shader bytecode starts with
# 0x44424358 ('DXBC' = SM4+) or 0xfffeXXXX (vs) / 0xffffXXXX (ps) for SM3-
OUT = Path(r"C:\src\ClassicUO\tools\ec_research\dump_shaders")
OUT.mkdir(exist_ok=True)
for i, (h, e) in enumerate(list(shaders.by_hash.items())[:40]):
    d = shaders.read(e)
    if len(d) < 8: continue
    head = d[:8].hex()
    # Identify shader type by 1st u32
    u32 = struct.unpack_from('<I', d, 0)[0]
    typ = '?'
    if (u32 >> 16) == 0xffff: typ = f'PS sm{(u32 >> 8) & 0xff}.{u32 & 0xff}'
    elif (u32 >> 16) == 0xfffe: typ = f'VS sm{(u32 >> 8) & 0xff}.{u32 & 0xff}'
    elif u32 == 0x43425844: typ = 'DXBC'  # SM4+
    print(f'  [{i}] hash={h:#x} size={len(d):6d} head={head} type={typ}')
    out_name = f'shader_{i:03d}_h{h:016x}.bin'
    (OUT / out_name).write_bytes(d)

print(f'\nDumped {len(shaders.by_hash)} -> {OUT}')
shaders.close()
