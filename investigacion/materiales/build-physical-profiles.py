import json,copy,math,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent;app=root.parents[1]/'archivo/copias/boxcraft-publicacion';models={m['id']:m for m in json.load(open(app/'dist/assets/modelos.json'))};caps=json.load(open(app/'dist/assets/capacidades-materiales.json'));materials=json.load(open(app/'dist/assets/materiales.json'))['materials']
def flat(o,p=''):
 if isinstance(o,dict):return {k:v for a,b in o.items() for k,v in flat(b,p+'/'+a).items()}
 if isinstance(o,list):return {k:v for a,b in enumerate(o) for k,v in flat(b,p+'/'+str(a)).items()}
 return {p:o}
def canonical(o):return {k:copy.deepcopy(o.get(k,[] if k in ['holes','faces','cuts','folds'] else 0)) for k in ['faces','cuts','folds','holes','totalX','totalY']}
def topo(o):return {k:'number' if type(v) in [float,int] else [type(v).__name__,v] for k,v in flat(o).items()}
def inverse(matrix):
 n=len(matrix);a=[list(row)+[float(i==j) for j in range(n)] for i,row in enumerate(matrix)]
 for i in range(n):
  p=max(range(i,n),key=lambda j:abs(a[j][i]));a[i],a[p]=a[p],a[i]
  if abs(a[i][i])<1e-9:raise ValueError('rank')
  s=a[i][i];a[i]=[x/s for x in a[i]]
  for j in range(n):
   if i!=j:
    f=a[j][i];a[j]=[x-f*y for x,y in zip(a[j],a[i])]
 return [r[n:] for r in a]
def close_dims(a,b,axes):return all(abs(a[k]-b[k])<1e-6 for k in axes)
reports=[];evidence={};samples={}
for rec in json.load(open(root/'collected.json')):
 for item in rec['samples']:
  if item['kind']!='knife':continue
  d=json.load(open(root/item['file']))['data'];code=str(d['cate_no']);layer=d['layer']['traditional'];t=layer['thickness'];dims=d['knifeSize'];sid=layer.get('science_id',d['science']['id']);record={'data':d,'layer':canonical(layer),'dims':dims,'t':t,'materialId':sid,'file':item['file'],'evidenceId':rec['evidenceId'],'step':rec.get('stepIds',{}).get(str(item['step']))}
  samples.setdefault(code,{}).setdefault(t,[]).append(record)
for code,by_t in samples.items():
 if code not in models:continue
 model=models[code];cap=caps[code];axes=list(model['dims']);desired=model.get('initialDims',model['dims']);profiles=[]
 for t,ss in sorted(by_t.items()):
  bases=[s for s in ss if close_dims(s['dims'],desired,axes)]
  if not bases:
   reports.append({'model':code,'thickness':t,'status':'no-current-base','samples':len(ss)});continue
  base=bases[-1];bf=flat(base['layer']);bt=topo(base['layer']);compatible=[s for s in ss if topo(s['layer'])==bt]
  # Derive full geometry only from measured independent axis variations.
  training=[base]
  current=dict(desired)
  for axis in axes:
   current[axis]+=2
   found=[s for s in compatible if close_dims(s['dims'],current,axes)]
   if found:training.append(found[-1])
  if len(training)!=len(axes)+1:
   reports.append({'model':code,'thickness':t,'status':'insufficient-axis-samples','samples':len(ss)});continue
  inv=inverse([[1]+[s['dims'][a]-desired[a] for a in axes] for s in training]);rules={};trainflat=[flat(s['layer']) for s in training]
  for p,v in bf.items():
   if type(v) not in (int,float):continue
   coef=[sum(inv[i][j]*trainflat[j][p] for j in range(len(training))) for i in range(len(training))]
   if any(abs(c)>1e-10 for c in coef[1:]):rules[p]=coef
  held=[s for s in ss if any(abs(s['dims'][a]-(desired[a]+1))<1e-6 for a in axes)]
  maxerr=0;badtopo=False;failures=[]
  for s in held:
   if topo(s['layer'])!=bt:badtopo=True;continue
   sf=flat(s['layer']);vector=[1]+[s['dims'][a]-desired[a] for a in axes]
   err=max((abs((sum(c*x for c,x in zip(rules[p],vector)) if p in rules else v)-sf[p]) for p,v in bf.items() if type(v) in (int,float)),default=0);maxerr=max(maxerr,err)
   if err>1e-5:failures.append(s['file'])
  passed=bool(held) and not badtopo and maxerr<=1e-5
  # Only measured materials; no assumption that equal thickness makes every science equivalent.
  ids=sorted(set(s['materialId'] for s in ss));ids=[mid for mid in ids if any(m['id']==mid and m['min']-1e-8<=t<=m['max']+1e-8 for m in materials)]
  offsets={mode:{a:round(base['data'][key][a]-base['dims'][a],7) for a in axes} for mode,key in [('inner','size'),('outer','outSize')]}
  all_offsets=all(all(abs(s['data'][key][a]-s['dims'][a]-offsets[mode][a])<1e-6 for a in axes) for s in ss for mode,key in [('inner','size'),('outer','outSize')])
  passed=passed and all_offsets and bool(ids)
  report={'model':code,'thickness':t,'status':'validated-local-affine' if passed else 'not-validated','materialIds':ids,'samples':len(ss),'heldouts':len(held),'maxErrorMm':maxerr,'topologyMismatch':badtopo,'constantOffsets':all_offsets}
  reports.append(report)
  if not passed:continue
  # Keep the verified neighborhood explicit; do not extrapolate material geometry.
  p={'materialIds':ids,'thickness':t,'engine':'derived','layer':base['layer'],'rule':{'base':[desired[a] for a in axes],'axes':axes,'rules':rules},'bounds':{a:[desired[a],desired[a]+2] for a in axes},'offsets':offsets,'geometryStatus':'validated-local-affine','evidence':{'samples':len(ss),'heldouts':len(held),'maxErrorMm':round(maxerr,10),'evidenceIds':sorted(set(s['evidenceId'] for s in ss))}}
  profiles.append(p)
 cap['physicalProfiles']=profiles
(root/'profile-build-report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
(app/'dist/assets/capacidades-materiales.json').write_text(json.dumps(caps,ensure_ascii=False,separators=(',',':'))+'\n')
for code in models:print(code,[(p['thickness'],p['materialIds']) for p in caps[code].get('physicalProfiles',[])])
print('VALID',sum(r['status']=='validated-local-affine' for r in reports),'of',len(reports))
