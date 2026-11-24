"""DXF -> PNG (ezdxf drawing add-on + matplotlib) and a text dump of the drawing.
Usage: python3 tools/cad_render.py in.dxf out_prefix"""
import sys, ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
doc, auditor = recover.readfile(src)
msp = doc.modelspace()
fig = plt.figure(figsize=(24, 24))
ax = fig.add_axes([0, 0, 1, 1])
cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(msp, finalize=True)
fig.savefig(out + '.png', dpi=150, facecolor='white')
texts = []
for e in msp.query('TEXT MTEXT INSERT'):
    if e.dxftype() == 'TEXT':
        texts.append(f"TEXT\t{e.dxf.layer}\t{e.dxf.insert[0]:.1f},{e.dxf.insert[1]:.1f}\t{e.dxf.text}")
    elif e.dxftype() == 'MTEXT':
        texts.append(f"MTEXT\t{e.dxf.layer}\t{e.dxf.insert[0]:.1f},{e.dxf.insert[1]:.1f}\t{e.plain_text()}")
    else:
        texts.append(f"INSERT\t{e.dxf.layer}\t{e.dxf.insert[0]:.1f},{e.dxf.insert[1]:.1f}\t{e.dxf.name}")
open(out + '.txt', 'w', encoding='utf-8').write('\n'.join(texts) + '\n')
print(out, len(texts), 'items')
