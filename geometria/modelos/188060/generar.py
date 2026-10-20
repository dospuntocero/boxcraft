#!/usr/bin/env python3
"""Genera el SVG y el JSON del troquel 188060 a partir de la respuesta base."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'base' / 'geometria.json'

def num(v):
    return f'{v:.12g}'

def path(dlist):
    out = []
    for v in dlist:
        m = v.get('mtd')
        if m == 'M':
            out.append(f"M{num(v['x'])} {num(v['y'])}")
        elif m == 'L':
            out.append(f"L{num(v['x'])} {num(v['y'])}")
        elif m == 'A':
            out.append(f"A{num(v['rx'])} {num(v['ry'])} {num(v.get('ang',0))} {int(v.get('arc',0))} {int(v.get('dir',1))} {num(v['x'])} {num(v['y'])}")
        elif m == 'Z':
            out.append('Z')
        else:
            raise ValueError(f'Comando no admitido: {m}')
    return ' '.join(out)

def main():
    base = json.loads(BASE.read_text())
    faces = base['faces']
    cuts = base['cuts']
    folds = base['folds']
    w, h = base['totalX'], base['totalY']
    body = []
    for f in faces:
        body.append(f'<path d="{path(f["dlist"])}" fill="#fff7f8" stroke="#d9dde5" stroke-width="0.25"/>')
    body.append(f'<path d="{path(cuts)}" fill="none" stroke="#2028b0" stroke-width="0.9" stroke-linejoin="round"/>')
    for f in folds:
        if 'x1' in f:
            body.append(f'<line x1="{num(f["x1"])}" y1="{num(f["y1"])}" x2="{num(f["x2"])}" y2="{num(f["y2"])}" stroke="#d02020" stroke-width="0.7" stroke-dasharray="3 2"/>')
        elif f.get('d'):
            body.append(f'<path d="{f["d"]}" fill="none" stroke="#d02020" stroke-width="0.7" stroke-dasharray="3 2"/>')
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{num(w)}mm" height="{num(h)}mm" viewBox="-1 -1 {num(w+2)} {num(h+2)}">
<rect x="-1" y="-1" width="{num(w+2)}" height="{num(h+2)}" fill="#fff"/>
<g id="caras">{''.join(body[:len(faces)])}</g>
<g id="cortes">{body[len(faces)]}</g>
<g id="pliegues">{''.join(body[len(faces)+1:])}</g>
</svg>
'''
    (ROOT / 'troquel-generado.svg').write_text(svg)
    out = {
        'modelo': '188060',
        'nombre': 'Caja hexagonal',
        'url': base['source']['url'],
        'dimensiones_manufactura_mm': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')},
        'dimensiones_interiores_mm': {k: base['size'][k] for k in ('L', 'W', 'H')},
        'dimensiones_exteriores_mm': {k: base.get('outSize', {}).get(k) for k in ('L', 'W', 'H')},
        'material': base['science'],
        'espesor_mm': base['thickness'],
        'extension_mm': {'x': w, 'y': h},
        'conteos': {'caras': len(faces), 'pliegues': len(folds), 'cortes': len(cuts), 'orificios': len(base.get('holes') or [])},
        'geometria': {'faces': faces, 'folds': folds, 'cuts': cuts, 'holes': base.get('holes') or [], 'totalX': w, 'totalY': h},
        'procedencia': base['source'],
        'limites': ['Captura 2D exacta; no se verificó un motor paramétrico.', 'No se validó armado físico ni exportación AI/DXF/PDF.'],
    }
    (ROOT / 'troquel-generado.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(f"188060: {w} x {h} mm; caras={len(faces)}; pliegues={len(folds)}; cortes={len(cuts)}")

if __name__ == '__main__':
    main()
