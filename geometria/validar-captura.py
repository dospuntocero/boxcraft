"""Comprueba relaciones internas de esta captura, sin validar fabricación."""
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
raw = (root / 'knife.json').read_bytes()
data = json.loads(raw)['data']
layer = data['layer']['traditional']
checks = []

def check(name, ok, detail):
    checks.append({'check': name, 'pass': bool(ok), 'detail': detail})

faces = {f['name']: f for f in layer['faces']}
folds = {f['name']: f for f in layer['folds']}
check('unique_names', len(faces) == len(layer['faces']) and len(folds) == len(layer['folds']), 'Nombres únicos de caras y pliegues')
adj = {name: set() for name in faces}
bad = []
for name in folds:
    pair = name.split('_')
    if len(pair) != 2 or any(n not in faces for n in pair):
        bad.append(name)
    else:
        a, b = pair
        adj[a].add(b)
        adj[b].add(a)
seen = set()
pending = [next(iter(faces))]
while pending:
    name = pending.pop()
    if name not in seen:
        seen.add(name)
        pending.extend(adj[name] - seen)
check('fold_graph', not bad and len(seen) == len(faces) and len(folds) == len(faces)-1, {'unknown': bad, 'reachable_faces': len(seen), 'faces': len(faces), 'edges': len(folds), 'interpretation': 'Los nombres de pliegue se interpretan como pares de caras'})
refs = [c['foldline'] for f in faces.values() for c in f['dlist'] if 'foldline' in c]
check('contour_fold_references', set(refs) == set(folds), {'unknown': sorted(set(refs)-set(folds)), 'unreferenced': sorted(set(folds)-set(refs))})
animations = [a for group in layer['animation']['animations'] for a in group]
check('animation_references', all(a['name'] in folds for a in animations), {'stages': len(layer['animation']['animations']), 'rotations': len(animations)})
length = sum(math.hypot(f['x2']-f['x1'], f['y2']-f['y1']) for f in folds.values())
check('fold_length', abs(length-data['extra']['foldlineLength']) < .01, {'computed_mm': length, 'declared_mm': data['extra']['foldlineLength'], 'tolerance_mm': .01})
coords = [c for c in layer['cuts'] if 'x' in c and 'y' in c]
bounds = {'min_x': min(c['x'] for c in coords), 'min_y': min(c['y'] for c in coords), 'max_x': max(c['x'] for c in coords), 'max_y': max(c['y'] for c in coords)}
check('cut_endpoint_bounds', all(-1e-8 <= c['x'] <= layer['totalX']+1e-8 and -1e-8 <= c['y'] <= layer['totalY']+1e-8 for c in coords), {'endpoint_bounds': bounds, 'totalX': layer['totalX'], 'totalY': layer['totalY'], 'limit': 'Solo extremos; no prueba los extremos interiores de arcos'})
params = [p for group in data['openParams'] for p in group]
check('open_parameter_limits', all(p['min'] <= p['value'] <= p['max'] for p in params), [{'name': p['name'], 'value': p['value'], 'min': p['min'], 'max': p['max'], 'unit': p['unit']} for p in params])
check('science_thickness', data['science']['min_thickness'] <= layer['thickness'] <= data['science']['max_thickness'], {'value': layer['thickness'], 'min': data['science']['min_thickness'], 'max': data['science']['max_thickness']})
result = {'input': 'knife.json', 'sha256': hashlib.sha256(raw).hexdigest(), 'all_pass': all(c['pass'] for c in checks), 'checks': checks, 'limitations': ['Coherencia de una sola captura, no precisión de fabricación', 'No se calcularon longitud de corte ni intersecciones de arcos', 'El grafo usa nombres de pliegue como relación entre caras', 'No se ejecutó el motor de plegado']}
(root / 'validacion-captura.json').write_text(json.dumps(result, indent=2, ensure_ascii=False))
for c in checks:
    print(('PASS' if c['pass'] else 'FAIL') + ' ' + c['check'])
raise SystemExit(0 if result['all_pass'] else 1)
