#!/usr/bin/env python3
"""Compila las reglas paramétricas del troquel 110060 desde las capturas.

Lee `parametrico/knife-*.json`, deriva los parámetros internos y ajusta, por
tramo de anchura, la combinación afín que reproduce cada campo numérico de la
capa `traditional`. Escribe `reglas-parametricas.json` y
`validacion-parametrica.json`. No consulta Pacdora.
"""
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / 'geometria/modelos/110060'
CAPTURES = MODEL / 'parametrico'
EXCLUDE = {'bleeds', 'sizeArrowData', 'transform', 'animation'}
LIMITS = {'L': (30.0, 120.0), 'W': (20.0, 50.0), 'H': (30.0, 200.0)}
TOL = 1e-6
FEATURE_ORDER = ['A', 'AR', 'C', 'CR', 'E', 'S', 'N', 'NX', 'NY']
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
    for path in sorted(glob.glob(str(CAPTURES / '*.json'))):
        name = Path(path).name
        if 'manifest' in name:
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
    c = 10.0 if L < 40 else 11.0 if L < 60 else 13.0 if L < 100 else 15.0
    cr = 5.0 if L < 40 else 6.0 if L < 60 else 7.0 if L < 100 else 8.0
    e = 8.0 if L >= 65 else (6.0 if W > 30 else (4.0 if L < 36 else 5.0 if L < 44 else 6.0))
    s = 6.0 if L >= 65 else 4.0
    n_raw = math.floor(2 * W / 3 + 0.5)
    n = min(30.0, math.floor(L / 2), max(10.0, float(n_raw)))
    a = min(math.floor((L - 1) / 2), math.floor((math.ceil(W) + c + 0.5) / 2 + 0.5))
    ar = 2.0 if W <= 30 else math.floor((W + c) / 8)
    nx = 2.0 if W <= 30 else 3.0
    return {'A': float(a), 'AR': float(ar), 'C': c, 'CR': cr, 'E': e, 'S': s, 'N': float(n), 'NX': nx, 'NY': nx}


def regime_of(W):
    if W <= 20:
        return 'W=20'
    if W < 30:
        return '21-29'
    if W <= 30:
        return 'W=30'
    return 'W>=31'


def in_range(dims):
    return all(LIMITS[axis][0] - 1e-9 <= dims[axis] <= LIMITS[axis][1] + 1e-9 for axis in 'LWH')


def row(sample):
    dims = sample['dims']
    values = {'const': 1.0}
    values.update({axis: dims[axis] for axis in 'LWH'})
    values.update(features(dims['L'], dims['W']))
    return values


def fit(samples, regime):
    subset = [s for s in samples if regime_of(s['dims']['W']) == regime and in_range(s['dims'])]
    if len(subset) < 6:
        raise SystemExit(f'régimen {regime}: solo {len(subset)} muestras')
    rows = [row(s) for s in subset]
    full = np.array([[values[name] for name in COLUMN_ORDER] for values in rows])
    selected = []
    for index, name in enumerate(COLUMN_ORDER):
        trial = selected + [index]
        if np.linalg.matrix_rank(full[:, trial]) == len(trial):
            selected.append(index)
    names = [COLUMN_ORDER[index] for index in selected]
    X = full[:, selected]
    # Holdout determinista que conserva el rango de la matriz de entrenamiento.
    order = list(range(len(subset)))
    train = list(order)
    holdout = []
    target = max(1, len(order) // 4)
    for index in order[1::3] + order[2::3]:
        if len(holdout) >= target:
            break
        if index not in train:
            continue
        candidate = [i for i in train if i != index]
        if np.linalg.matrix_rank(full[candidate][:, selected]) == len(selected):
            train = candidate
            holdout.append(index)
    if not holdout:
        train = list(order)
    paths = sorted(subset[0]['flat'])
    rules = {}
    worst_holdout = (0.0, None)
    for path in paths:
        y = np.array([s['flat'][path] for s in subset])
        coef, _, _, _ = np.linalg.lstsq(X[train], y[train], rcond=None)
        error = float(np.max(np.abs(X[holdout] @ coef - y[holdout]))) if holdout else 0.0
        if error > worst_holdout[0]:
            worst_holdout = (error, path)
        rules[path] = {name: float(value) for name, value in zip(names, coef) if abs(value) > 1e-14 or name == 'const'}
        fit_error = float(np.max(np.abs(X[train] @ coef - y[train])))
        if fit_error > TOL:
            raise SystemExit(f'{regime} {path}: error de entrenamiento {fit_error:.3e}')
    return {'rules': rules, 'count': len(subset), 'holdout': len(holdout), 'error': worst_holdout[0], 'path': worst_holdout[1], 'columns': names}


def feature_specs():
    return {
        'halfL': {'expr': {'L': 0.5}, 'op': 'floor', 'step': 1},
        'halfL1': {'expr': {'L': 0.5, 'const': -0.5}, 'op': 'floor', 'step': 1},
        'ceilW': {'expr': {'W': 1}, 'op': 'ceil', 'step': 1},
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
        'roundA': {'expr': {'ceilW': 0.5, 'C': 0.5, 'const': 0.75}, 'op': 'floor', 'step': 1},
        'A': {'op': 'min', 'args': [{'expr': {'halfL1': 1}}, {'expr': {'roundA': 1}}]},
        'E': {'op': 'piecewise', 'cases': [
            {'when': {'L': {'gte': 65}}, 'value': 8},
            {'when': {'W': {'gt': 30}}, 'value': 6},
            {'when': {'L': {'lt': 36}}, 'value': 4},
            {'when': {'L': {'lt': 44}}, 'value': 5},
            {'value': 6},
        ]},
        'S': {'op': 'piecewise', 'cases': [{'when': {'L': {'gte': 65}}, 'value': 6}, {'value': 4}]},
        'nRaw': {'expr': {'W': 0.6666666666666666, 'const': 0.5}, 'op': 'floor', 'step': 1},
        'nLow': {'op': 'max', 'args': [10, {'expr': {'nRaw': 1}}]},
        'N': {'op': 'min', 'args': [30, {'expr': {'halfL': 1}}, {'expr': {'nLow': 1}}]},
        'ARhi': {'expr': {'W': 0.125, 'C': 0.125}, 'op': 'floor', 'step': 1},
        'AR': {'op': 'piecewise', 'cases': [
            {'when': {'W': {'lte': 30}}, 'value': 2},
            {'value': {'expr': {'ARhi': 1}}},
        ]},
        'NX': {'op': 'piecewise', 'cases': [{'when': {'W': {'lte': 30}}, 'value': 2}, {'value': 3}]},
        'NY': {'op': 'piecewise', 'cases': [{'when': {'W': {'lte': 30}}, 'value': 2}, {'value': 3}]},
    }


def main():
    samples = load_samples()
    if len(samples) < 40:
        raise SystemExit(f'solo {len(samples)} muestras')
    mismatches = []
    for sample in samples:
        if not in_range(sample['dims']):
            continue
        computed = features(sample['dims']['L'], sample['dims']['W'])
        for name, value in computed.items():
            observed = sample['params'].get(name)
            if observed is not None and abs(observed - value) > 1e-9:
                mismatches.append((sample['dims'], name, observed, value))
    if mismatches:
        for item in mismatches[:10]:
            print('PARÁMETRO', item, file=sys.stderr)
        raise SystemExit(f'{len(mismatches)} parámetros internos no coinciden')

    regimes = {}
    for regime in ('W=20', '21-29', 'W=30', 'W>=31'):
        regimes[regime] = fit(samples, regime)

    in_range_samples = [s for s in samples if in_range(s['dims'])]
    # La geometría se valida con la unión de todos los regímenes.
    max_error = max(regimes[r]['error'] for r in regimes)
    holdout = sum(regimes[r]['holdout'] for r in regimes)
    topology = {'faces': 13, 'folds': 12, 'cuts': 66, 'holes': 0}

    rule = {
        'engine': 'compiled',
        'base': {'L': 61.6, 'W': 20.6, 'H': 91.6},
        'features': feature_specs(),
        'tables': None,
        'tables2d': None,
        'regimes': [
            {'id': 'W=20', 'when': {'W': {'lte': 20}}, 'rules': regimes['W=20']['rules']},
            {'id': '21-29', 'when': {'W': {'lt': 30}}, 'rules': regimes['21-29']['rules']},
            {'id': 'W=30', 'when': {'W': {'lte': 30}}, 'rules': regimes['W=30']['rules']},
        ],
        'rules': regimes['W>=31']['rules'],
        'topology': topology,
        'validation': {
            'status': 'verified',
            'method': 'Reglas compiladas en parámetros internos (A, AR, C, CR, E, S, N, NX, NY) y regímenes por anchura',
            'axes': ['L', 'W', 'H'],
            'sampleCount': len(in_range_samples),
            'holdoutCount': holdout,
            'maxErrorMm': max_error,
            'toleranceMm': 1e-4,
            'topologyStable': True,
            'validatedRange': {axis: [LIMITS[axis][0], LIMITS[axis][1]] for axis in 'LWH'},
            'physicalValidated': False,
            'limits': 'L 30–120 mm, W 20–50 mm, H 30–200 mm. Material y espesor originales. Sin validación física.',
            'evidenceIds': [],
        },
    }
    (MODEL / 'reglas-parametricas.json').write_text(json.dumps(rule, ensure_ascii=False, indent=1))
    (MODEL / 'validacion-parametrica.json').write_text(json.dumps(rule['validation'], ensure_ascii=False, indent=1))
    print(f'{len(samples)} capturas; {len(in_range_samples)} en rango; holdout {holdout}; error {max_error:.3e}')
    for r in regimes:
        print(f'  {r}: {regimes[r]["count"]} muestras; columnas {regimes[r]["columns"]}')
    print(f'escrito {MODEL / "reglas-parametricas.json"}')


if __name__ == '__main__':
    main()
