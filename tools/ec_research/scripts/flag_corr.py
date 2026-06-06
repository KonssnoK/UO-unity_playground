"""EC tileart 0x39 flags <-> CC tiledata TileFlag bit-correlation matrix."""
import sys, struct, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
spec = importlib.util.spec_from_file_location("m73", str(Path(__file__).resolve().parent / "73_tileart_vs_tiledata.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

cc = m.load_cc_static_tiledata()
ec = m.load_ec_tileart_offsets()

CCNAME = {0:'Background',1:'Weapon',2:'Transparent',3:'Translucent',4:'Wall',5:'Damaging',
6:'Impassable',7:'Wet',8:'Unknown1',9:'Surface',10:'Bridge',11:'Generic/Stack',12:'Window',
13:'NoShoot',14:'PrefixA',15:'PrefixAn',16:'Internal',17:'Foliage',18:'PartialHue',19:'NoHouse',
20:'Map',21:'Container',22:'Wearable',23:'LightSource',24:'Animation',25:'NoDiagonal',
26:'Armor/Roof',27:'Door',28:'StairBack',29:'StairRight',30:'AlphaBlend',31:'UseNewArt',
32:'ArtUsed',33:'Backward',34:'NoFootstep'}

pairs = []
for tid, b in ec.items():
    # The EC tileart TileID (offset 0x06, the dict key here) IS the CC item_id
    # directly -- do NOT subtract 0x4000 (that art-offset pairing is wrong and
    # makes the flags look uncorrelated).
    if tid not in cc: continue
    ecf = struct.unpack_from('<Q', b, 0x39)[0]
    pairs.append((ecf, cc[tid]['flags']))
import math
N = len(pairs)
print('paired tiles:', N)
ecbits = [[(ef >> b) & 1 for ef, cf in pairs] for b in range(40)]
ccbits = [[(cf >> b) & 1 for ef, cf in pairs] for b in range(40)]
def phi(a, b):
    n11 = n10 = n01 = n00 = 0
    for x, y in zip(a, b):
        if x and y: n11 += 1
        elif x: n10 += 1
        elif y: n01 += 1
        else: n00 += 1
    d = (n11+n10)*(n01+n00)*(n11+n01)*(n10+n00)
    if d == 0: return 0.0
    return (n11*n00 - n10*n01) / math.sqrt(d)
print('%5s %6s   %-7s %6s  %6s   %s' % ('ECbit','set%','bestCC','phi','samephi','CCname'))
for eb in range(40):
    ones = sum(ecbits[eb])
    if ones == 0: continue
    scored = sorted(((phi(ecbits[eb], ccbits[cb]), cb) for cb in range(40)), reverse=True)
    bphi, bcb = scored[0]
    sphi = phi(ecbits[eb], ccbits[eb])
    tag = 'SAME-POS' if bcb == eb else ('REMAP<-bit%d' % eb)
    print('%5d %6.1f   ccbit%2d  %6.2f  %6.2f   %-12s %s' % (eb, 100*ones/N, bcb, bphi, sphi, CCNAME.get(bcb,'?'), tag))
