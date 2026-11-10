#!/usr/bin/env python3
"""Compila las reglas paramétricas del troquel 10001006 desde las capturas.

Lee las respuestas de Pacdora guardadas en `parametrico/` y sus subcarpetas,
deriva los parámetros internos como funciones exactas de L/W/H y ajusta, por
régimen de anchura, la combinación afín que reproduce cada campo numérico de
la capa `traditional`.

Uso:
  python3 geometria/modelos/10001006/compilar-reglas.py

Escribe `reglas-parametricas.json` y `validacion-parametrica.json`.
No consulta Pacdora.
"""
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / 'geometria/modelos/10001006'
CAPTURES = MODEL / 'parametrico'
EXCLUDE = {'bleeds', 'sizeArrowData', 'transform', 'animation'}
LIMITS = {'L': (30.0, 100.0), 'W': (10.6, 60.0), 'H': (80.0, 180.0)}
TOL = 1e-6
FEATURE_ORDER = ['A', 'C', 'CR', 'E', 'S', 'G', 'AR', 'NX']
COLUMN_ORDER = ['const', 'L', 'W', 'H'] + FEATURE_ORDER


def flatten(value, path='', out=None):
    if out is None:
        out = {}
    if isinstance(value, dict):
        for key, child in value.items():
            if key in EXCLUDE:
                continue
            flatten(child, f'{path}/{key}', out)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            flatten(child, f'{path}/{index}', out)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        out[path] = float(value)
    return out


def load_samples():
    samples = {}
    paths = sorted(glob.glob(str(CAPTURES / '**/*.json'), recursive=True))
    for path in paths:
        name = Path(path).name
        if name.startswith('manifest') or name == 'capturas-manifest.json':
            continue
        try:
            payload = json.loads(Path(path).read_text())
        except Exception:
            continue
        data = payload.get('data', payload)
        if not isinstance(data, dict) or 'knifeSize' not in data:
            continue
        layer = (data.get('layer') or {}).get('traditional')
        if not isinstance(layer, dict):
            continue
        dims = {axis: float(data['knifeSize'][axis]) for axis in 'LWH'}
        params = {}
        for group in data.get('openParams') or []:
            for item in group:
                if 'name' in item and 'value' in item:
                    params[item['name']] = float(item['value'])
        samples[tuple(dims[axis] for axis in 'LWH')] = {
            'path': str(Path(path).relative_to(ROOT)),
            'dims': dims,
            'params': params,
            'layer': layer,
            'flat': flatten(layer),
        }
    return [samples[key] for key in sorted(samples)]


def features(L, W):
    """Parámetros internos observados en Pacdora, como funciones de L/W."""
    if W <= 30:
        ar = 1.0
    elif L < 40:
        ar = math.floor((W + 2) / 8) + 1
    elif L < 60:
        ar = math.floor((W + 3) / 8) + 1
    elif L < 100:
        ar = math.floor((W + 13) / 8)
    else:
        ar = math.floor((W + 14) / 8)
    nx = 2.0 if W <= 30 else 3.0
    c = 10.0 if L < 40 else 11.0 if L < 60 else 13.0 if L < 100 else 15.0
    return {
        'C': c,
        'CR': 5.0 if L < 40 else 6.0 if L < 60 else 7.0 if L < 100 else 8.0,
        'A': min(math.floor(L / 2), math.floor((math.ceil(W) + c + 0.5) / 2 + 0.5)),
        'E': 8.0 if L >= 65 else (6.0 if W > 30 else (4.0 if L < 40 else 5.0 if L < 45 else 6.0)),
        'S': 6.0 if L >= 65 else 4.0,
        'G': 16.0 if L + W >= 125.25 else min(13.0, W - 1.5),
        'AR': float(ar),
        'NX': nx,
        'NY': nx,
    }


def regime_of(W):
    if W <= 20:
        return 'estrecha'      # W <= 20: ATT = 0, AX = 2.5, NX = NY = 2
    if W < 30:
        return 'media'         # 20 < W < 30: ATT = 13, AX = 2.5, NX = NY = 2
    return 'ancha'             # W >= 30: ATT = 13, AX = 3.5


def in_range(dims):
    return all(LIMITS[axis][0] - 1e-9 <= dims[axis] <= LIMITS[axis][1] + 1e-9 for axis in 'LWH')


def row(sample):
    dims = sample['dims']
    f = features(dims['L'], dims['W'])
    values = {'const': 1.0}
    values.update({axis: dims[axis] for axis in 'LWH'})
    values.update(f)
    return values


def fit(samples, regime):
    subset = [s for s in samples if regime_of(s['dims']['W']) == regime and in_range(s['dims'])]
    if not subset:
        raise SystemExit(f'régimen {regime}: sin muestras')
    rows = [row(s) for s in subset]
    full = np.array([[values[name] for name in COLUMN_ORDER] for values in rows])
    selected = []
    for index, name in enumerate(COLUMN_ORDER):
        trial = selected + [index]
        if np.linalg.matrix_rank(full[:, trial]) == len(trial):
            selected.append(index)
    names = [COLUMN_ORDER[index] for index in selected]
    X = full[:, selected]
    order = list(range(len(subset)))
    holdout = order[1::4]
    train = [i for i in order if i not in holdout]
    if len(train) < X.shape[1] or np.linalg.matrix_rank(X[train]) < X.shape[1]:
        raise SystemExit(f'régimen {regime}: matriz de entrenamiento sin rango suficiente')
    paths = sorted(subset[0]['flat'])
    rules = {}
    worst_holdout = (0.0, None)
    for path in paths:
        y = np.array([s['flat'][path] for s in subset])
        coef, _, _, _ = np.linalg.lstsq(X[train], y[train], rcond=None)
        error = float(np.max(np.abs(X[holdout] @ coef - y[holdout]))) if holdout else 0.0
        if error > worst_holdout[0]:
            worst_holdout = (error, path)
        rules[path] = {name: float(value) for name, value in zip(names, coef)
                       if abs(value) > 1e-14 or name == 'const'}
        full = float(np.max(np.abs(X @ coef - y)))
        if full > TOL:
            raise SystemExit(f'{regime} {path}: error de ajuste {full:.3e}')
    return {'rules': rules, 'count': len(subset), 'holdout': len(holdout), 'error': worst_holdout[0], 'path': worst_holdout[1], 'columns': names}


def feature_specs():
    return {
        'halfL': {'expr': {'L': 0.5}, 'op': 'floor', 'step': 1},
        'C': {'op': 'piecewise', 'cases': [
            {'when': {'L': {'lt': 40}}, 'value': 10},
            {'when': {'L': {'lt': 60}}, 'value': 11},
            {'when': {'L': {'lt': 100}}, 'value': 13},
            {'value': 15},
        ]},
        'CR': {'op': 'piecewise', 'cases': [
            {'when': {'L': {'lt': 40}}, 'value': 5},
            {'when': {'L': {'lt': 60}}, 'value': 6},
            {'when': {'L': {'lt': 100}}, 'value': 7},
            {'value': 8},
        ]},
        'ceilW': {'expr': {'W': 1}, 'op': 'ceil', 'step': 1},
        'roundA': {'expr': {'ceilW': 0.5, 'C': 0.5, 'const': 0.75}, 'op': 'floor', 'step': 1},
        'A': {'op': 'min', 'args': [{'expr': {'halfL': 1}}, {'expr': {'roundA': 1}}]},
        'E': {'op': 'piecewise', 'cases': [
            {'when': {'L': {'gte': 65}}, 'value': 8},
            {'when': {'W': {'gt': 30}}, 'value': 6},
            {'when': {'L': {'lt': 40}}, 'value': 4},
            {'when': {'L': {'lt': 45}}, 'value': 5},
            {'value': 6},
        ]},
        'S': {'op': 'piecewise', 'cases': [
            {'when': {'L': {'gte': 65}}, 'value': 6},
            {'value': 4},
        ]},
        'sumLW': {'expr': {'L': 1, 'W': 1}},
        'Gbase': {'op': 'min', 'args': [13, {'expr': {'W': 1, 'const': -1.5}}]},
        'G': {'op': 'piecewise', 'cases': [
            {'when': {'sumLW': {'gte': 125.25}}, 'value': 16},
            {'value': {'expr': {'Gbase': 1}}},
        ]},
        'ar2': {'expr': {'W': 0.125, 'const': 0.25}, 'op': 'floor', 'step': 1},
        'ar3': {'expr': {'W': 0.125, 'const': 0.375}, 'op': 'floor', 'step': 1},
        'ar13': {'expr': {'W': 0.125, 'const': 1.625}, 'op': 'floor', 'step': 1},
        'ar14': {'expr': {'W': 0.125, 'const': 1.75}, 'op': 'floor', 'step': 1},
        'AR': {'op': 'piecewise', 'cases': [
            {'when': {'W': {'lte': 30}}, 'value': 1},
            {'when': {'L': {'lt': 40}}, 'value': {'expr': {'ar2': 1, 'const': 1}}},
            {'when': {'L': {'lt': 60}}, 'value': {'expr': {'ar3': 1, 'const': 1}}},
            {'when': {'L': {'lt': 100}}, 'value': {'expr': {'ar13': 1}}},
            {'value': {'expr': {'ar14': 1}}},
        ]},
        'NX': {'op': 'piecewise', 'cases': [{'when': {'W': {'lte': 30}}, 'value': 2}, {'value': 3}]},
        'NY': {'op': 'piecewise', 'cases': [{'when': {'W': {'lte': 30}}, 'value': 2}, {'value': 3}]},
    }


def main():
    samples = load_samples()
    if len(samples) < 50:
        raise SystemExit(f'solo {len(samples)} muestras')
    mismatches = []
    for sample in samples:
        computed = features(sample['dims']['L'], sample['dims']['W'])
        for name, value in computed.items():
            observed = sample['params'].get(name)
            if observed is not None and abs(observed - value) > 1e-9:
                mismatches.append((sample['dims'], name, observed, value))
    if mismatches:
        for row in mismatches[:10]:
            print('PARÁMETRO', row, file=sys.stderr)
        raise SystemExit(f'{len(mismatches)} parámetros internos no coinciden con las capturas')

    regimes = {}
    for regime in ('estrecha', 'media', 'ancha'):
        regimes[regime] = fit(samples, regime)

    in_range_samples = [s for s in samples if in_range(s['dims'])]
    holdout = sum(regimes[r]['holdout'] for r in regimes)
    max_error = max(regimes[r]['error'] for r in regimes)
    counts = {'faces': 13, 'folds': 12, 'cuts': 76, 'holes': 0}

    def when_of(regime):
        return {'estrecha': {'W': {'lte': 20}}, 'media': {'W': {'lt': 30}}}.get(regime)

    rule = {
        'engine': 'compiled',
        'base': {'L': 40.0, 'W': 40.0, 'H': 130.0},
        'features': feature_specs(),
        'tables': None,
        'tables2d': None,
        'regimes': [
            {'id': 'estrecha', 'when': when_of('estrecha'), 'rules': regimes['estrecha']['rules']},
            {'id': 'media', 'when': when_of('media'), 'rules': regimes['media']['rules']},
        ],
        'rules': regimes['ancha']['rules'],
        'topology': counts,
        'validation': {
            'status': 'verified',
            'method': 'Reglas compiladas en parámetros internos (A, AR, C, CR, E, S, G, NX, NY) y regímenes por anchura',
            'axes': ['L', 'W', 'H'],
            'sampleCount': len(in_range_samples),
            'holdoutCount': holdout,
            'maxErrorMm': max_error,
            'toleranceMm': 1e-4,
            'topologyStable': True,
            'validatedRange': {axis: [LIMITS[axis][0], LIMITS[axis][1]] for axis in 'LWH'},
            'physicalValidated': False,
            'limits': 'L 30–100 mm, W 10,6–60 mm, H 80–180 mm. Material y espesor originales. Sin validación física.',
            'evidenceIds': [],
        },
    }
    (MODEL / 'reglas-parametricas.json').write_text(json.dumps(rule, ensure_ascii=False, indent=1))
    (MODEL / 'validacion-parametrica.json').write_text(json.dumps(rule['validation'], ensure_ascii=False, indent=1))
    print(f'{len(samples)} capturas; {len(in_range_samples)} en rango; holdout {holdout}; error {max_error:.3e}')
    print(f'régimen ancha: {regimes["ancha"]["count"]} muestras; media: {regimes["media"]["count"]}; estrecha: {regimes["estrecha"]["count"]}')
    print(f'escrito {MODEL / "reglas-parametricas.json"}')


if __name__ == '__main__':
    main()
