"""Build material capabilities from retained Pacdora responses, without inventing thickness samples."""
import json, hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
OUT=ROOT/'dist/assets'
raw=json.loads((ROOT/'investigacion-materiales/catalogo-original.json').read_text())
assert raw['code']==200
materials=[]
groups={'white paperboard':'Cartulina blanca','kraft paperboard':'Cartulina kraft','white kraft paperboard':'Kraft blanco','Corrugated board':'Cartón corrugado','Art paper':'Papel arte','customize':'Personalizados','default':'Kraft','Card board':'Kraft','铜版纸':'Papel arte','grey back duplex board':'Cartón dúplex'}
for m in raw['data']:
 if m.get('special_type'):continue
 name=m['name'].replace('white paperboard','cartón blanco').replace('kraft paperboard','cartón kraft').replace('white kraft paperboard','kraft blanco').replace('art paper','papel arte').replace('Custom','Personalizado:').replace('custom','personalizado').replace('corrugated board','cartón corrugado').replace('material','material').replace('-flute',' · onda')
 if m['name'].endswith('-flute'):name='Onda '+m['name'].split('-')[0]
 if m['id']==103:name='Cartón blanco 350 g'
 if m['id']==101:name='Cartón blanco 250 g'
 materials.append({'id':m['id'],'name':name,'group':groups.get(m['group_name'],m['group_name']),'thickness':m['thickness'],'min':m['min_thickness'],'max':m['max_thickness'],'adjustable':bool(m['can_set']) and m['min_thickness']<m['max_thickness'],'inless':m['inless'],'outless':m['outless']})
(OUT/'materiales.json').write_text(json.dumps({'source':'https://www.pacdora.com/api/v2/materials/science?pageSize=1000&scienceType=1','materials':materials},ensure_ascii=False,indent=2))
models=json.loads((OUT/'modelos.json').read_text());caps={};matrix=['# Estado de materiales y conversiones','', 'Los límites de espesor observados pertenecen a las dimensiones de las muestras. No representan un rango verificado de geometría a otros espesores.','', '| Modelo | Material original | Espesor verificado (mm) | Muestras de conversión coincidentes | Modos | Pendiente |','|---|---|---:|---:|---|---|']
for m in models:
 code=m['id']
 ps=sorted((REPO/'geometria/experimentos').glob('knife-*.json')) if code=='200010' else sorted((REPO/'geometria/modelos'/code).glob('**/knife-*.json'))
 basepath=REPO/'geometria/knife.json' if code=='200010' else next(p for p in ps if p.name=='knife-00.json')
 base=json.loads(basepath.read_text())['data'];axes=list(m['dims']);science=base['science']
 delta=lambda d:{'inner':{a:round(d['size'][a]-d['knifeSize'][a],7) for a in axes},'outer':{a:round(d['outSize'][a]-d['knifeSize'][a],7) for a in axes}}
 offsets=delta(base);matched=[];excluded=[]
 for p in ps:
  d=json.loads(p.read_text())['data']
  rec={'path':str(p.relative_to(REPO)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'manufacturing':d['knifeSize'],'inner':d['size'],'outer':d['outSize'],'thickness':d['science']['thickness']}
  (matched if delta(d)==offsets and d['science']['id']==science['id'] and d['science']['thickness']==science['thickness'] else excluded).append(rec)
 cap={'originalMaterialId':science['id'],'originalThickness':science['thickness'],'observedThicknessLimits':[base['modeCate']['layerList'][0]['minThickness'],base['ccalMap']['traditional']],'verifiedThicknessRange':[science['thickness'],science['thickness']],'onlyManufacturing':bool(base['modeCate'].get('IsOnlyManufacture')),'offsets':offsets,'source':str(basepath.relative_to(REPO)),'samples':matched,'excludedSamples':excluded,'blockedReason':'Faltan muestras de geometría a otros materiales y espesores.','geometryStatus':'height-only' if code=='102010' else 'original-thickness'}
 caps[code]=cap
 matrix.append(f"| {code} | {science['name']} | {science['thickness']} | {len(matched)} | {'Solo manufactura' if cap['onlyManufacturing'] else 'Manufactura / interior / exterior'} | {'Longitud y anchura del fondo; ' if code=='102010' else ''}Otros materiales y espesores; prueba de armado |")
(OUT/'capacidades-materiales.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2))
(ROOT/'investigacion-materiales/matriz-validacion.md').write_text('\n'.join(matrix)+'\n')
print(len(materials),'materiales;',len(caps),'modelos')
import runpy
runpy.run_path(str(ROOT/'incorporar-modelos-adquiridos.py'),run_name='__main__')
