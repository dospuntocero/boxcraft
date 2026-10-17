import json,copy,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent;app=root.parents[1]/'archivo/copias/boxcraft-publicacion';models={m['id']:m for m in json.load(open(app/'dist/assets/modelos.json'))};caps=json.load(open(app/'dist/assets/capacidades-materiales.json'));catalog={m['id']:m for m in json.load(open(app/'dist/assets/materiales.json'))['materials']}
# Exact measured configurations. No interpolation or extrapolation is implied.
candidates={};ledger=[]
def geometry(layer):return {k:copy.deepcopy(layer.get(k,[])) for k in ['faces','cuts','folds','holes','totalX','totalY']}
for rec in json.load(open(root/'collected.json')):
 for item in rec['samples']:
  if item['kind']!='knife':continue
  d=json.load(open(root/item['file']))['data'];code=str(d['cate_no'])
  if code not in models:continue
  layer=d['layer']['traditional'];t=layer['thickness'];mid=layer.get('science_id',d['science']['id']);axes=list(models[code]['dims']);dims={a:d['knifeSize'][a] for a in axes};base=models[code].get('initialDims',models[code]['dims'])
  if not all(abs(dims[a]-base[a])<1e-7 for a in axes):continue
  model=models[code]
  if model.get('materialWidthMm') and layer['totalX']>model['materialWidthMm']+1e-7:continue
  if model.get('materialSheetMm'):
   x,y=layer['totalX'],layer['totalY'];w,h=model['materialSheetMm']
   if not (x<=w+1e-7 and y<=h+1e-7 or x<=h+1e-7 and y<=w+1e-7):continue
  material=catalog.get(mid)
  if not material or not(material['min']-1e-8<=t<=material['max']+1e-8):continue
  if t<caps[code]['observedThicknessLimits'][0]-1e-8 or t>caps[code]['observedThicknessLimits'][1]+1e-8:continue
  if mid==caps[code]['originalMaterialId'] and abs(t-caps[code]['originalThickness'])<1e-8:continue
  p={'materialIds':[mid],'thickness':t,'layer':geometry(layer),'bounds':{a:[dims[a],dims[a]] for a in axes},'offsets':{mode:{a:round(d[key][a]-dims[a],7) for a in axes} for mode,key in [('inner','size'),('outer','outSize')]},'geometryStatus':'observed-snapshot','evidence':{'captureReference':rec['evidenceId'],'responseSha256':hashlib.sha256((root/item['file']).read_bytes()).hexdigest(),'configuration':dims}}
  key=(code,mid,t);candidates[key]=p
for code,cap in caps.items():cap['physicalProfiles']=[p for (c,mid,t),p in sorted(candidates.items()) if c==code]
(app/'dist/assets/capacidades-materiales.json').write_text(json.dumps(caps,ensure_ascii=False,separators=(',',':'))+'\n')
for code,model in models.items():
 cap=caps[code];profiles=cap.get('physicalProfiles',[]);entry={'model':code,'name':model['name'],'originalMaterialId':cap['originalMaterialId'],'newMaterials':sorted(set(mid for p in profiles for mid in p['materialIds'])),'newProfiles':len(profiles),'thicknesses':sorted(set(p['thickness'] for p in profiles)),'scope':'Exact captured manufacturing dimensions; other configurations remain unverified.'};ledger.append(entry);print(entry)
(root/'observed-profile-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
