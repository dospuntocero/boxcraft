#!/usr/bin/env python3
"""Ajusta reglas compiladas a partir de muestras de Pacdora.

Uso:
  python3 ajustar-playwright.py CODE SAMPLES_DIR [SAMPLES_DIR ...]

- Fusiona `geometria/modelos/CODE/parametricas/knife-*.json` y los directorios indicados.
- Deriva fórmulas exactas para los parámetros internos (`openParams`).
- Ajusta cada campo de la capa como combinación afín de L/W/H y esos parámetros.
- Reserva una parte de las muestras como holdout y solo escribe reglas si predice exacto.
"""
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = {'bleeds', 'sizeArrowData', 'transform', 'animation'}
DIM_AXES = ('L', 'W', 'H')
STEPS = (0.01, 0.1, 0.25, 0.5, 1.0)
TOL = 1e-9


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


def load_payload(path):
    raw = json.loads(Path(path).read_text())
    return raw.get('data', raw)


def collect(code, extra_dirs):
    paths = sorted(glob.glob(str(ROOT / 'geometria' / 'modelos' / code / 'parametricas' / 'knife-*.json')))
    for directory in extra_dirs:
        paths += sorted(glob.glob(str(Path(directory) / '*.json')))
    samples = {}
    for path in paths:
        if Path(path).name == 'manifest.json':
            continue
        try:
            data = load_payload(path)
        except Exception:
            continue
        if not isinstance(data, dict) or 'knifeSize' not in data or 'layer' not in data:
            continue
        layer = data['layer'].get('traditional') if isinstance(data['layer'], dict) else None
        if not isinstance(layer, dict):
            continue
        dims = {axis: float(data['knifeSize'][axis]) for axis in DIM_AXES}
        key = tuple(round(dims[axis], 8) for axis in DIM_AXES)
        pars = {}
        for group in data.get('openParams') or []:
            for item in group:
                if 'name' in item and 'value' in item:
                    pars[item['name']] = float(item['value'])
        # Keep the last occurrence (new captures win over historical duplicates).
        samples[key] = {'path': str(path), 'dims': dims, 'params': pars,
                        'layer': layer, 'flat': flatten(layer),
                        'science': (data.get('science') or {}).get('id'),
                        'thickness': layer.get('thickness')}
    return [samples[key] for key in sorted(samples)]


def candidates(values, dims):
    """Return exact candidate formulas for one parameter."""
    y = np.array(values, dtype=float)
    names = list(DIM_AXES)
    matrices = []
    matrices.append(('const', np.ones((len(y), 1))))
    for name in names:
        matrices.append((name, np.array([[1.0, dims[i][name]] for i in range(len(y))])))
    for a in range(3):
        for b in range(a + 1, 3):
            matrices.append((f'{names[a]}+{names[b]}',
                             np.array([[1.0, dims[i][names[a]], dims[i][names[b]]] for i in range(len(y))])))
    found = []
    for label, X in matrices:
        coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        raw = X @ coef
        for op in ('none', 'round', 'floor', 'ceil'):
            for step in (STEPS if op != 'none' else (1.0,)):
                if op == 'round':
                    pred = np.round(raw / step) * step
                elif op == 'floor':
                    pred = np.floor(raw / step) * step
                elif op == 'ceil':
                    pred = np.ceil(raw / step) * step
                else:
                    pred = raw
                for clamp in (False, True):
                    final = pred.copy()
                    if clamp:
                        final = np.clip(final, float(np.min(y)), float(np.max(y)))
                    if np.max(np.abs(final - y)) <= 1e-8:
                        terms = {'const': float(coef[0])}
                        if label != 'const':
                            for i, name in enumerate(names):
                                if label.startswith(name) or f'+{name}' in label:
                                    terms[name] = float(coef[names.index(name) + 1])
                        expr = {k: v for k, v in terms.items() if abs(v) > 1e-12 or k == 'const'}
                        item = {'expr': expr, 'op': op, 'step': step if op not in ('none',) else 1,
                                'clamp': [float(np.min(y)), float(np.max(y))] if clamp else None}
                        # Score: fewer terms, then simpler op, then no clamp.
                        score = (len(expr) - 1, 0 if op == 'none' else 1, 0 if not clamp else 1)
                        found.append((score, item, label))
    if not found:
        return None
    found.sort(key=lambda item: item[0])
    return found[0][1]


def evaluate(feature, dims, features):
    expr = feature.get('expr', {})
    value = expr.get('const', 0.0)
    for key, coef in expr.items():
        if key == 'const':
            continue
        value += coef * (dims[key] if key in dims else features.get(key, 0.0))
    op = feature.get('op', 'none')
    step = feature.get('step', 1) or 1
    if op == 'round':
        value = round(value / step) * step
    elif op == 'floor':
        value = math.floor(value / step) * step
    elif op == 'ceil':
        value = math.ceil(value / step) * step
    if feature.get('clamp'):
        value = min(feature['clamp'][1], max(feature['clamp'][0], value))
    return value


def fit(code, samples, holdout_fraction=0.25):
    dims = [s['dims'] for s in samples]
    pnames = sorted({name for s in samples for name in s['params']})
    dynamic = [name for name in pnames if len({round(s['params'].get(name, 0.0), 9) for s in samples}) > 1]
    formulas = {}
    for name in dynamic:
        values = [s['params'].get(name, 0.0) for s in samples]
        formula = candidates(values, dims)
        if formula is None:
            print(f'  AVISO: no se encontró fórmula exacta para {name}')
            continue
        formulas[name] = formula
    feature_names = list(formulas)
    # Evaluate features in order (formulas may depend on previous features).
    values = {name: [] for name in feature_names}
    for s in samples:
        current = {}
        for name in feature_names:
            current[name] = evaluate(formulas[name], s['dims'], current)
            values[name].append(current[name])
    columns = [np.ones(len(samples))]
    labels = ['const']
    for name in feature_names:
        columns.append(np.array(values[name]))
        labels.append(name)
    X = np.column_stack(columns)
    # Drop linearly dependent features (keep the earliest, simplest).
    rank = np.linalg.matrix_rank(X)
    keep = [0]
    for j in range(1, X.shape[1]):
        candidate = keep + [j]
        if np.linalg.matrix_rank(X[:, candidate]) == len(candidate):
            keep = candidate
    X = X[:, keep]
    labels = [labels[j] for j in keep]
    paths = sorted(samples[0]['flat'])
    # Deterministic holdout: every fourth sample, but always keep at least 20% and not the base.
    order = list(range(len(samples)))
    holdout = set(order[1::4]) if len(order) >= 8 else set(order[-max(1, len(order)//4):])
    train = [i for i in order if i not in holdout]
    if len(train) < X.shape[1] or np.linalg.matrix_rank(X[train]) < X.shape[1]:
        raise SystemExit(f'{code}: la matriz de entrenamiento no tiene rango suficiente ({X.shape[1]} columnas)')
    rules = {}
    worst = (0.0, None)
    for path in paths:
        y = np.array([s['flat'][path] for s in samples])
        coef, _, _, _ = np.linalg.lstsq(X[train], y[train], rcond=None)
        predicted = X[holdout] @ coef if holdout else np.array([])
        error = float(np.max(np.abs(predicted - y[list(holdout)]))) if holdout else 0.0
        if error > worst[0]:
            worst = (error, path)
        rules[path] = {label: float(value) for label, value in zip(labels, coef) if abs(value) > 1e-12 or label == 'const'}
    topology = {
        'faces': len(samples[0]['layer'].get('faces') or []),
        'folds': len(samples[0]['layer'].get('folds') or []),
        'cuts': len(samples[0]['layer'].get('cuts') or []),
        'holes': len(samples[0]['layer'].get('holes') or [])
    }
    return {
        'engine': 'compiled',
        'base': {axis: samples[0]['dims'][axis] for axis in DIM_AXES},
        'features': formulas,
        'rules': rules,
        'topology': topology,
        'sampleCount': len(samples),
        'holdoutCount': len(holdout),
        'maxErrorMm': worst[0],
        'worstPath': worst[1],
        'validatedRange': {axis: [min(dims[i][axis] for i in range(len(dims))), max(dims[i][axis] for i in range(len(dims)))] for axis in DIM_AXES},
        'labels': labels
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    code = sys.argv[1]
    extra = sys.argv[2:]
    samples = collect(code, extra)
    if len(samples) < 8:
        raise SystemExit(f'{code}: solo {len(samples)} muestras')
    print(f'{code}: {len(samples)} muestras; parámetros dinámicos:')
    result = fit(code, samples)
    print(f'  features: {list(result["features"])}')
    print(f'  columnas usadas: {result["labels"]}')
    print(f'  holdouts: {result["holdoutCount"]}; error máximo: {result["maxErrorMm"]:.9f} en {result["worstPath"]}')
    out = ROOT / 'geometria' / 'modelos' / code / 'reglas-parametricas.json'
    out.write_text(json.dumps({k: v for k, v in result.items() if k not in ('labels',)}, ensure_ascii=False, indent=1))
    print(f'  escrito {out}')


if __name__ == '__main__':
    main()
