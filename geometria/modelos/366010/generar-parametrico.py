#!/usr/bin/env python3
"""Genera un SVG/JSON local para una configuración L/W/H de 366010, sin red.

Uso:
  python3 generar-parametrico.py --L 210 --W 120 --H 50

El sangrado de 3 mm se calcula con ClipperLib mediante Node; el resto es
Python puro y no consulta Pacdora.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generar as G
import parametrizar as P

RULE = json.loads((ROOT / 'reglas.json').read_text())
GAP = RULE['layout']['gap_mm']


def translate(layer, dx, dy):
    for face in layer['faces']:
        face['x'] += dx
        face['y'] += dy
        for point in face['dlist']:
            if 'x' in point:
                point['x'] += dx
            if 'y' in point:
                point['y'] += dy
        for hole in face.get('holes') or []:
            for point in hole:
                if 'x' in point:
                    point['x'] += dx
                if 'y' in point:
                    point['y'] += dy
    for key in ('cuts', 'bleeds'):
        for point in layer[key]:
            if 'x' in point:
                point['x'] += dx
            if 'y' in point:
                point['y'] += dy
    for fold in layer['folds']:
        if 'x1' in fold:
            fold['x1'] += dx
        if 'x2' in fold:
            fold['x2'] += dx
        if 'y1' in fold:
            fold['y1'] += dy
        if 'y2' in fold:
            fold['y2'] += dy
    return layer


def bleed_path(cuts):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as handle:
        json.dump({'cuts': cuts}, handle)
        source = handle.name
    try:
        result = subprocess.check_output(
            ['node', str(ROOT / 'bleed-node.cjs'), source], text=True)
    finally:
        pathlib.Path(source).unlink(missing_ok=True)
    return result.strip()


def build(L, W, H, T=2.0):
    bounds = RULE['bounds']
    for axis, value in (('L', L), ('W', W), ('H', H)):
        low, high = bounds[axis]
        if not (low <= value <= high):
            raise SystemExit(f'{axis}={value} fuera de {low}–{high} mm')
    if T not in RULE['thicknesses']:
        raise SystemExit(f'T={T} fuera de {RULE["thicknesses"]}')
    regime = RULE['regimes'][0] if L < 200 else RULE['regimes'][1]
    templates = regime['templatesByThickness'][f'{T:g}']
    dims = {'L': L, 'W': W, 'H': H, 'T': T}
    pieces = []
    for piece in RULE['pieces']:
        layer = P.apply(templates[piece['id']],
                        regime['slopes'][piece['id']], regime, dims)
        pieces.append({**piece, 'layer': layer})
    widths = [0.0, 0.0]
    heights = [0.0, 0.0]
    for piece in pieces:
        widths[piece['col']] = max(widths[piece['col']], piece['layer']['totalX'])
        heights[piece['row']] = max(heights[piece['row']], piece['layer']['totalY'])
    for piece in pieces:
        dx = 0.0 if piece['col'] == 0 else widths[0] + GAP
        dy = 0.0 if piece['row'] == 0 else heights[0] + GAP
        piece['offset'] = {'x': dx, 'y': dy}
        translate(piece['layer'], dx, dy)
    total_x = widths[0] + GAP + widths[1]
    total_y = heights[0] + GAP + heights[1]
    paper_cuts = [c for p in pieces if p['paper'] for c in p['layer']['cuts']]
    path = bleed_path(paper_cuts)
    return pieces, total_x, total_y, path


def write(pieces, total_x, total_y, path, dims, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{G.num(total_x + 10)}mm" '
            f'height="{G.num(total_y + 10)}mm" viewBox="-5 -5 {G.num(total_x + 10)} {G.num(total_y + 10)}">',
            f'<rect x="-5" y="-5" width="{G.num(total_x + 10)}" height="{G.num(total_y + 10)}" fill="#ffffff"/>']
    body.append('<g id="caras" fill="#fcfbf8" stroke="#e2e5ea" stroke-width="0.15">')
    for piece in pieces:
        body.extend(f'<path d="{G.path(f["dlist"])}"/>' for f in piece['layer']['faces'])
    body.append('</g>')
    body.append(f'<path id="sangrado" d="{path}" fill="none" stroke="#51aa20" stroke-width="0.45"/>')
    body.append('<g id="corte" fill="none" stroke="#2028b0" stroke-width="0.8">')
    for piece in pieces:
        body.append(f'<path d="{G.path(piece["layer"]["cuts"])}"/>')
    body.append('</g><g id="pliegues" fill="none" stroke="#d02020" stroke-width="0.55" stroke-dasharray="3 2">')
    for piece in pieces:
        body.extend(f'<line x1="{G.num(f["x1"])}" y1="{G.num(f["y1"])}" '
                    f'x2="{G.num(f["x2"])}" y2="{G.num(f["y2"])}"/>'
                    for f in piece['layer']['folds'])
    body.append('</g><g id="etiquetas" font-family="Arial" font-size="4.5" fill="#444b57">')
    for piece in pieces:
        body.append(f'<text x="{G.num(piece["offset"]["x"] + 2.5)}" '
                    f'y="{G.num(piece["offset"]["y"] + 6.8)}">{piece["name"]}</text>')
    body.append('</g></svg>')
    stem = f'L{dims["L"]:g}-W{dims["W"]:g}-H{dims["H"]:g}' + (f'-T{dims["T"]:g}' if abs(dims['T'] - 2.0) > 1e-9 else '')
    (out_dir / f'{stem}.svg').write_text('\n'.join(body) + '\n')
    data = {
        'modelo': '366010',
        'medidas': dims,
        'regimen': 'A' if dims['L'] < 200 else 'B',
        'espesor': dims['T'],
        'extension_mm': {'x': total_x, 'y': total_y},
        'bleed_path': path,
        'piezas': [{'id': p['id'], 'nombre': p['name'], 'offset': p['offset'],
                    'extension': {'x': p['layer']['totalX'], 'y': p['layer']['totalY']},
                    'conteos': {k: len(p['layer'][k]) for k in ('faces', 'cuts', 'folds', 'bleeds')}}
                   for p in pieces],
    }
    (out_dir / f'{stem}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    return out_dir / f'{stem}.svg'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--L', type=float, required=True)
    parser.add_argument('--W', type=float, required=True)
    parser.add_argument('--H', type=float, required=True)
    parser.add_argument('--T', type=float, default=2.0)
    parser.add_argument('--out', type=pathlib.Path, default=ROOT / 'salidas')
    args = parser.parse_args()
    pieces, total_x, total_y, path = build(args.L, args.W, args.H, args.T)
    dest = write(pieces, total_x, total_y, path,
                 {'L': args.L, 'W': args.W, 'H': args.H, 'T': args.T}, args.out)
    print(dest, f'{total_x} x {total_y} mm')


if __name__ == '__main__':
    main()
