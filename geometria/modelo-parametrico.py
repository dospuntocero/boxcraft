"""Modelo empírico local, limitado a dimensiones y material contrastados."""
import argparse
import copy
import hashlib
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ['knife-00.json', 'knife-02.json', 'knife-04.json', 'knife-06.json']
BASE = (434.0, 214.0, 278.0)
DELTAS = (74.0, 40.0, 26.8)
BOUNDS = ((434.0, 508.0), (214.0, 254.0), (278.0, 304.8))

def load_data(path):
    return json.loads(path.read_text())['data']

def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)

def fit():
    sources = [ROOT / 'experimentos' / name for name in FILES]
    layers = [load_data(p)['layer']['traditional'] for p in sources]
    rules = {}
    def walk(values, path=''):
        first = values[0]
        if isinstance(first, dict):
            if any(set(v) != set(first) for v in values):
                raise ValueError(f'Estructuras distintas: {path}')
            for key in first:
                walk([v[key] for v in values], path+'/'+key)
        elif isinstance(first, list):
            if any(len(v) != len(first) for v in values):
                raise ValueError(f'Longitudes distintas: {path}')
            for i in range(len(first)):
                walk([v[i] for v in values], path+'/'+str(i))
        elif numeric(first):
            slopes = [(v-first)/delta for v,delta in zip(values[1:],DELTAS)]
            if any(abs(s) > 1e-12 for s in slopes):
                rules[path] = {'base': first, 'slopes_LWH': slopes}
        elif any(v != first for v in values) and not path.endswith('/tpointer/value'):
            raise ValueError(f'Campo no numérico variable: {path}')
    walk(layers)
    model = {'kind': 'empirical-affine-model', 'base_mm': BASE, 'bounds_mm': BOUNDS, 'fixed': {'material': 'Onda B', 'thickness_mm': 3, 'OF': 2, 'R': 3, 'G': 45, 'GT': 15}, 'training': [{'file': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources], 'template': layers[0], 'rules': rules, 'limitations': ['Una muestra por eje y una combinación independiente de validación', 'La caja delimitada por las muestras no se verificó exhaustivamente', 'No extrapolar ni usar otro espesor/material', 'No recupera el algoritmo original', 'No validado para fabricación']}
    (ROOT / 'reglas-parametricas.json').write_text(json.dumps(model, indent=2, ensure_ascii=False))
    return model

def generate(model, L, W, H):
    dimensions = (L, W, H)
    for name,value,(low,high) in zip('LWH',dimensions,model['bounds_mm']):
        if not low <= value <= high:
            raise ValueError(f'{name}={value}: rango admitido {low}–{high} mm')
    layer = copy.deepcopy(model['template'])
    for path,rule in model['rules'].items():
        parts = path.lstrip('/').split('/')
        current = layer
        for key in parts[:-1]:
            current = current[int(key)] if isinstance(current,list) else current[key]
        value = rule['base'] + sum(s*(d-b) for s,d,b in zip(rule['slopes_LWH'],dimensions,model['base_mm']))
        key = int(parts[-1]) if isinstance(current,list) else parts[-1]
        current[key] = value
    labels = {'L': L, 'W': W, 'H': H, 'G': 45, 'F': W/2+1, 'F1': W/2+3, 'R': 3, 'OF': 2, 'GT': 15}
    for arrow in layer['sizeArrowData']:
        pointer = arrow.get('tpointer', {})
        label = pointer.get('value', '').split('=')[0]
        if label in labels:
            pointer['value'] = f'{label}={labels[label]:g}'
    return layer

def validate(model):
    target = load_data(ROOT/'validacion-parametrica'/'knife-04.json')
    dimensions = [target['knifeSize'][name] for name in 'LWH']
    predicted = generate(model,*dimensions)
    actual = target['layer']['traditional']
    errors = []
    numeric_count = 0
    def compare(a,b,path=''):
        nonlocal numeric_count
        if isinstance(a,dict):
            if set(a)!=set(b): errors.append({'path':path,'kind':'keys'});return
            for key in a:compare(a[key],b[key],path+'/'+key)
        elif isinstance(a,list):
            if len(a)!=len(b): errors.append({'path':path,'kind':'length'});return
            for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
        elif numeric(a):
            numeric_count += 1
            delta = abs(a-b)
            if delta>1e-6:errors.append({'path':path,'kind':'numeric','absolute_mm_or_units':delta})
        elif a!=b:errors.append({'path':path,'kind':'literal','predicted':a,'actual':b})
    compare(predicted,actual)
    exact_geometry = all(e['path'].startswith('/bleeds/') and e['kind']=='numeric' and e['absolute_mm_or_units']<.001 for e in errors)
    report={'holdout_file':'validacion-parametrica/knife-04.json','holdout_dimensions_mm':dimensions,'numeric_fields_compared':numeric_count,'all_fields_within_1e_6':not errors,'cuts_faces_folds_and_other_fields_within_1e_6':exact_geometry,'bleed_tolerance_mm':.001,'pass':exact_geometry,'differences':errors,'limit':'Validación contra una respuesta del servidor, no contra una muestra física'}
    (ROOT/'validacion-modelo.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    return report

def render_svg(layer):
    def commands(items):
        out=[]
        for c in items:
            if c['mtd'] in ('M','L'):
                out.append(f"{c['mtd']}{c['x']:g} {c['y']:g}")
            elif c['mtd']=='A':
                out.append(f"A{c['rx']:g} {c['ry']:g} {c['ang']:g} {int(c['arc'])} {int(c['dir'])} {c['x']:g} {c['y']:g}")
            elif c['mtd']=='Z': out.append('Z')
            else: raise ValueError(f"Comando no soportado: {c['mtd']}")
        return ' '.join(out)
    faces=''.join(f'<path d="{commands(f["dlist"])}" fill="hsl({i*29%360} 65% 85%)"><title>{html.escape(f["name"])}</title></path>' for i,f in enumerate(layer['faces']))
    holes=''.join(f'<path d="{commands(h)}"/>' for h in (layer.get('holes') or []))
    folds=''.join(f'<line x1="{f["x1"]}" y1="{f["y1"]}" x2="{f["x2"]}" y2="{f["y2"]}"/>' for f in layer['folds'])
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{layer["totalX"]}mm" height="{layer["totalY"]}mm" viewBox="0 0 {layer["totalX"]} {layer["totalY"]}"><title>Modelo empírico FEFCO 0201 · No validado para fabricación</title><g id="faces">{faces}</g><g id="holes" fill="white" stroke="#dc2626" stroke-width="1">{holes}</g><path id="cuts" d="{commands(layer["cuts"])}" fill="none" stroke="#dc2626" stroke-width="1"/><g id="folds" stroke="#2563eb" stroke-width="1" stroke-dasharray="6 3">{folds}</g></svg>'

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--length',type=float,default=457.2)
    parser.add_argument('--width',type=float,default=228.6)
    parser.add_argument('--height',type=float,default=279.4)
    args=parser.parse_args()
    model=fit()
    report=validate(model)
    if not report['pass']:
        raise SystemExit('La validación independiente falló; consulte validacion-modelo.json')
    layer=generate(model,args.length,args.width,args.height)
    output={'source':'local-empirical-model','manufacturing_size_mm':{'L':args.length,'W':args.width,'H':args.height},'thickness_mm':3,'layer':layer,'limitations':model['limitations']}
    (ROOT/'troquel-generado.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    (ROOT/'troquel-generado.svg').write_text(render_svg(layer))
    print(f"PASS: {report['numeric_fields_compared']} campos numéricos comparados; {len(report['differences'])} diferencias de sangría inferiores a 0.001 mm")
