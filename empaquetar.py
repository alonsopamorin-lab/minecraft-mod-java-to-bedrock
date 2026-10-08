"""Empaqueta las fuentes actuales; no cambia versiones ni UUID."""
from pathlib import Path
import argparse, io, json, zipfile
parser=argparse.ArgumentParser()
parser.add_argument('--salida',default='dist/Permadeath_actual.mcaddon')
args=parser.parse_args()
root=Path(__file__).resolve().parent
out=Path(args.salida)
if not out.is_absolute():out=root/out
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as addon:
 for folder,label in [('Permadeath_BP','Comportamiento'),('Permadeath_RP','Recursos')]:
  base=root/'pack'/folder
  manifest=json.loads((base/'manifest.json').read_text())
  print(manifest['header']['name'],manifest['header']['version'])
  data=io.BytesIO()
  with zipfile.ZipFile(data,'w',zipfile.ZIP_DEFLATED) as pack:
   for p in sorted(base.rglob('*')):
    if p.is_file():pack.write(p,p.relative_to(base))
  addon.writestr('Permadeath_'+label+'.mcpack',data.getvalue())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out)
