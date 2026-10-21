#!/usr/bin/env python3
"""Ajusta las reglas paramétricas L/W/H del troquel 366010.

Dos regímenes observados en el servidor de Pacdora:
  A (L < 200): profundidad exterior fija de 15 mm.
  B (L >= 200): profundidad exterior = clamp(floor(H/2), 15, 20).

Dentro de cada régimen la geometría es afín en L/W/H; en B se añade la
variable `outer`. Los coeficientes se ajustan con muestras de un solo eje y
se validan contra todas las demás capturas.
"""
import hashlib
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generar as G

BASE = json.loads((ROOT / 'base' / 'knife-00.json').read_text())['data']
SAMPLES = ROOT / 'parametricas'
THICKNESS_SAMPLES = ROOT / 'espesor'
THICKNESSES = [1.5, 1.75, 2.0, 2.25, 2.5]
BASE_THICKNESS = 2.0
BOUNDS = {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]}


def read(name):
    return json.loads((SAMPLES / name).read_text())['data']


def read_thickness(L, W, H, T):
    name = f'L{L:g}-W{W:g}-H{H:g}-T{T:g}.json'
    path = THICKNESS_SAMPLES / name
    if not path.exists() and abs(T - BASE_THICKNESS) < 1e-9:
        return read(f'L{L:g}-W{W:g}-H{H:g}.json')
    return json.loads(path.read_text())['data']


def flat(layer):
    out = {}

    def walk(value, path):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('transform', 'animation', 'sizeArrowData', 'thickness'):
                    continue
                walk(child, path + '/' + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + f'/{index}')
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            out[path] = float(value)

    walk(layer, '')
    return out


def normalise(sample, piece):
    return G.normalise_layer(sample['layer'][piece['layer']], piece, 0.0, 0.0)


def slope_map(reference, sample, delta):
    ref, cur = flat(reference), flat(sample)
    return {path: (cur[path] - value) / delta
            for path, value in ref.items() if abs((cur[path] - value) / delta) > 1e-12}


def build_rule():
    pieces = []
    for piece in G.PIECES:
        item = dict(piece)
        item['paper'] = item['id'] in ('fondo-papel', 'tapa-papel')
        pieces.append(item)

    templates_a = {}
    templates_b = {}
    for thickness in THICKNESSES:
        template_a = read_thickness(180, 100, 40, thickness)
        template_b = read_thickness(200, 100, 40, thickness)
        key = f'{thickness:g}'
        templates_a[key] = {piece['id']: normalise(template_a, piece) for piece in pieces}
        templates_b[key] = {piece['id']: normalise(template_b, piece) for piece in pieces}
    templates_a_ref = templates_a[f'{BASE_THICKNESS:g}']
    templates_b_ref = templates_b[f'{BASE_THICKNESS:g}']

    l195 = read('L195-W100-H40.json')
    w120 = json.loads((ROOT / 'muestras' / 'W120.json').read_text())['data']
    h60_a = json.loads((ROOT / 'muestras' / 'H60.json').read_text())['data']
    l210 = read('L210-W100-H40.json')
    w120_b = read('L200-W120-H40.json')
    h60_b = read('L200-W100-H60.json')
    h30_b = read('L200-W100-H30.json')

    regime_a = {'id': 'A', 'L': [BOUNDS['L'][0], 199.999999],
                'ref': {'L': 180, 'W': 100, 'H': 40},
                'outer': '15', 'templatesByThickness': templates_a, 'slopes': {}}
    regime_b = {'id': 'B', 'L': [200, BOUNDS['L'][1]],
                'ref': {'L': 200, 'W': 100, 'H': 40},
                'outer': 'clamp(floor(H/2),15,20)', 'templatesByThickness': templates_b,
                'slopes': {}}

    for piece in pieces:
        pid = piece['id']
        a_ref = templates_a_ref[pid]
        s_l = slope_map(a_ref, normalise(l195, piece), 15)
        s_w = slope_map(a_ref, normalise(w120, piece), 20)
        s_h = slope_map(a_ref, normalise(h60_a, piece), 20)
        paths = set(s_l) | set(s_w) | set(s_h)
        regime_a['slopes'][pid] = {
            path: [s_l.get(path, 0.0), s_w.get(path, 0.0), s_h.get(path, 0.0)]
            for path in sorted(paths)
        }

        b_ref = templates_b_ref[pid]
        b_l = slope_map(b_ref, normalise(l210, piece), 10)
        b_w = slope_map(b_ref, normalise(w120_b, piece), 20)
        b_h = slope_map(b_ref, normalise(h60_b, piece), 20)
        b_ref_flat = flat(b_ref)
        b_30 = flat(normalise(h30_b, piece))
        b_60 = flat(normalise(h60_b, piece))
        paths = set(b_l) | set(b_w) | set(b_h)
        for path, value in b_ref_flat.items():
            s_h_value = (b_60[path] - value) / 20
            s_o_value = (b_30[path] - value - (-10 * s_h_value)) / (-5)
            if abs(s_h_value) > 1e-12 or abs(s_o_value) > 1e-12:
                paths.add(path)
        regime_b['slopes'][pid] = {
            path: [b_l.get(path, 0.0), b_w.get(path, 0.0),
                   (b_60[path] - b_ref_flat[path]) / 20,
                   ((b_30[path] - b_ref_flat[path])
                    - (-10 * ((b_60[path] - b_ref_flat[path]) / 20))) / (-5)]
            for path in sorted(paths)
        }

    return {
        'modelo': '366010',
        'base': {'L': 180, 'W': 100, 'H': 40},
        'bounds': BOUNDS,
        'layout': {'gap_mm': 25},
        'pieces': pieces,
        'thicknesses': THICKNESSES,
        'baseThickness': BASE_THICKNESS,
        'regimes': [regime_a, regime_b],
    }


def apply(template, slopes, regime, dims):
    layer = json.loads(json.dumps(template))
    ref = regime['ref']
    outer = 15
    if regime['id'] == 'B':
        outer = min(20, max(15, math.floor(dims['H'] / 2)))
    for path, values in slopes.items():
        parts = path[1:].split('/')
        target = layer
        for key in parts[:-1]:
            target = target[int(key)] if isinstance(target, list) else target[key]
        key = parts[-1]
        index = int(key) if isinstance(target, list) else key
        target[index] += (values[0] * (dims['L'] - ref['L'])
                          + values[1] * (dims['W'] - ref['W'])
                          + values[2] * (dims['H'] - ref['H']))
        if regime['id'] == 'B' and len(values) > 3:
            target[index] += values[3] * (outer - 20)
    return layer


def validate(rule):
    results = []
    max_error = 0.0
    for path in sorted(SAMPLES.glob('*.json')):
        if path.name == 'manifest.json':
            continue
        data = json.loads(path.read_text())['data']
        dims = {axis: data['knifeSize'][axis] for axis in 'LWH'}
        if any(dims[axis] < BOUNDS[axis][0] - 1e-9
               or dims[axis] > BOUNDS[axis][1] + 1e-9 for axis in 'LWH'):
            continue
        regime = rule['regimes'][0] if dims['L'] < 200 else rule['regimes'][1]
        local_max = 0.0
        worst = None
        templates = regime['templatesByThickness'][f'{BASE_THICKNESS:g}']
        for piece in rule['pieces']:
            predicted = apply(templates[piece['id']],
                              regime['slopes'][piece['id']], regime, dims)
            actual = normalise(data, piece)
            a, b = flat(predicted), flat(actual)
            for key in sorted(set(a) & set(b)):
                error = abs(a[key] - b[key])
                if error > local_max:
                    local_max = error
                    worst = (piece['id'], key, a[key], b[key])
        max_error = max(max_error, local_max)
        results.append({
            'archivo': path.name,
            'tipo': 'lwh',
            'medidas': dims,
            'regimen': regime['id'],
            'error_max_mm': local_max,
            'peor_campo': worst,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    for path in sorted(THICKNESS_SAMPLES.glob('L*-W*-H*-T*.json')):
        data = json.loads(path.read_text())['data']
        dims = {axis: data['knifeSize'][axis] for axis in 'LWH'}
        thickness = float(path.stem.rsplit('-T', 1)[1])
        if thickness not in THICKNESSES:
            continue
        if any(dims[axis] < BOUNDS[axis][0] - 1e-9
               or dims[axis] > BOUNDS[axis][1] + 1e-9 for axis in 'LWH'):
            continue
        regime = rule['regimes'][0] if dims['L'] < 200 else rule['regimes'][1]
        templates = regime['templatesByThickness'][f'{thickness:g}']
        local_max = 0.0
        worst = None
        for piece in rule['pieces']:
            predicted = apply(templates[piece['id']],
                              regime['slopes'][piece['id']], regime, dims)
            actual = normalise(data, piece)
            a, b = flat(predicted), flat(actual)
            for key in sorted(set(a) & set(b)):
                error = abs(a[key] - b[key])
                if error > local_max:
                    local_max = error
                    worst = (piece['id'], key, a[key], b[key])
        max_error = max(max_error, local_max)
        results.append({
            'archivo': path.name,
            'tipo': 'espesor',
            'medidas': dims,
            'espesor': thickness,
            'regimen': regime['id'],
            'error_max_mm': local_max,
            'peor_campo': worst,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return max_error, results


def sample_manifest(results):
    rows = []
    for path in sorted(SAMPLES.glob('L*-W*-H*.json')):
        data = json.loads(path.read_text())['data']
        dims = {axis: data['knifeSize'][axis] for axis in 'LWH'}
        row = next((item for item in results if item['archivo'] == path.name), None)
        rows.append({
            'archivo': path.name,
            'medidas': dims,
            'regimen': row['regimen'] if row else ('A' if dims['L'] < 200 else 'B'),
            'error_max_mm': row['error_max_mm'] if row else None,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'capas': {name: {'totalX': layer['totalX'], 'totalY': layer['totalY'],
                             'caras': len(layer['faces']), 'cortes': len(layer['cuts']),
                             'pliegues': len(layer['folds']), 'sangrados': len(layer['bleeds'])}
                      for name, layer in data['layer'].items()},
        })
    (SAMPLES / 'manifest.json').write_text(
        json.dumps({'modelo': '366010', 'capturado': '2026-10-20',
                    'fuente': 'Pacdora /api/v2/project/knife vía CDP controlado',
                    'bounds': BOUNDS, 'muestras': rows},
                   ensure_ascii=False, indent=2) + '\n')
    return rows


def main():
    rule = build_rule()
    max_error, results = validate(rule)
    sample_manifest(results)
    if max_error > 0.05:
        raise SystemExit(f'Error paramétrico {max_error:.6f} mm > 0,05 mm')
    text = json.dumps(rule, ensure_ascii=False, separators=(',', ':'))
    (ROOT / 'reglas.json').write_text(text + '\n')
    validation = {
        'modelo': '366010',
        'fecha': '2026-10-20',
        'metodo': 'Ajuste afín por régimen con variable exterior; sin extrapolación',
        'limites': BOUNDS,
        'regimenes': [
            {'id': 'A', 'L': [BOUNDS['L'][0], 199.999999], 'outer': 15},
            {'id': 'B', 'L': [200, BOUNDS['L'][1]],
             'outer': 'clamp(floor(H/2),15,20)'},
        ],
        'muestras': len(results),
        'error_max_mm': max_error,
        'resultado': 'ok' if max_error <= 0.05 else 'falla',
        'detalle': sorted(results, key=lambda row: (-row['error_max_mm'], row['archivo']))[:10],
        'sha256_reglas': hashlib.sha256((ROOT / 'reglas.json').read_bytes()).hexdigest(),
        'notas': [
            'La geometría de las cuatro capas se conserva; solo se ajustan campos numéricos.',
            'El régimen B introduce un salto real en la profundidad exterior al cruzar L=200.',
            'El sangrado se recalcula en el editor a 3 mm del corte para las piezas de papel.',
        ],
    }
    (ROOT / 'validacion-parametrica.json').write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
    print(f"reglas {len(text.encode())} bytes; {len(results)} muestras; "
          f"error máximo {max_error:.6f} mm")


if __name__ == '__main__':
    main()
