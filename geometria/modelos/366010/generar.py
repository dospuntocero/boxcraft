#!/usr/bin/env python3
"""Genera el troquel 366010 (caja rígida de dos piezas) desde la respuesta de Pacdora.

La respuesta contiene cuatro capas: cartón gris y papel de envoltura para el
fondo y para la tapa. Se conservan las cuatro geometrías y se componen en una
sola lámina para el catálogo local. No se inventan coordenadas ni se escalan.
"""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'base' / 'knife-00.json'
URL = ('https://www.pacdora.com/es/dielines-detail/'
       'custom-dimensions-box-with-lid-luxury-box-dieline-366010')

# Orden y ubicación de las cuatro piezas en la lámina compuesta. La separación
# es de 25 mm; las columnas se alinean a la izquierda como en la vista oficial.
GAP = 25.0
PIECES = [
    {
        'id': 'fondo-gris',
        'prefix': 'FG',
        'name': 'Fondo · cartón gris 2 mm',
        'layer': 'BoutiqueboxDivideEquallyCoverBottomGreyboard',
        'row': 0, 'col': 0,
    },
    {
        'id': 'fondo-papel',
        'prefix': 'FP',
        'name': 'Fondo · papel 0,15 mm',
        'layer': 'BoutiqueboxDivideEquallyCoverBottomFacepaper',
        'row': 0, 'col': 1,
    },
    {
        'id': 'tapa-gris',
        'prefix': 'TG',
        'name': 'Tapa · cartón gris 2 mm',
        'layer': 'BoutiqueboxDivideEquallyCoverTopGreyboard',
        'row': 1, 'col': 0,
    },
    {
        'id': 'tapa-papel',
        'prefix': 'TP',
        'name': 'Tapa · papel 0,15 mm',
        'layer': 'BoutiqueboxDivideEquallyCoverTopFacepaper',
        'row': 1, 'col': 1,
    },
]


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
            out.append(f"A{num(v['rx'])} {num(v['ry'])} {num(v.get('ang', 0))} "
                       f"{int(v.get('arc', 0))} {int(v.get('dir', 1))} "
                       f"{num(v['x'])} {num(v['y'])}")
        elif m == 'Z':
            out.append('Z')
        else:
            raise ValueError(f'Comando no admitido: {m}')
    return ' '.join(out)


def sha(path_obj):
    return hashlib.sha256(path_obj.read_bytes()).hexdigest()


def translate_point(point, dx, dy):
    if 'x' in point:
        point['x'] += dx
    if 'y' in point:
        point['y'] += dy


def translate_commands(commands, dx, dy):
    for command in commands:
        translate_point(command, dx, dy)
    return commands


def normalise_layer(layer, piece, dx, dy):
    """Copia una capa y traslada toda su geometría 2D; conserva nombres con prefijo."""
    out = {
        'thickness': layer['thickness'],
        'bleedline': layer.get('bleedline', 3),
        'totalX': layer['totalX'],
        'totalY': layer['totalY'],
        'faces': [],
        'cuts': [],
        'folds': [],
        'holes': [],
        'bleeds': [],
    }
    for face in layer.get('faces') or []:
        dlist = [dict(p) for p in face.get('dlist') or []]
        translate_commands(dlist, dx, dy)
        holes = []
        for hole in face.get('holes') or []:
            hole_copy = [dict(p) for p in hole]
            translate_commands(hole_copy, dx, dy)
            holes.append(hole_copy)
        out['faces'].append({
            'name': f"{piece['prefix']}_{face['name']}",
            'w': face['w'], 'h': face['h'],
            'x': face['x'] + dx, 'y': face['y'] + dy,
            'dlist': dlist,
            'holes': holes or None,
        })
    for cut in layer.get('cuts') or []:
        cut = dict(cut)
        translate_point(cut, dx, dy)
        out['cuts'].append(cut)
    for fold in layer.get('folds') or []:
        fold = dict(fold)
        if 'd' in fold:
            raise ValueError('Pliegue con trazado literal no admitido en la traslación.')
        for key in ('x1', 'x2'):
            if key in fold:
                fold[key] += dx
        for key in ('y1', 'y2'):
            if key in fold:
                fold[key] += dy
        fold['name'] = f"{piece['prefix']}_{fold['name']}"
        out['folds'].append(fold)
    for hole in layer.get('holes') or []:
        hole = [dict(p) for p in hole]
        translate_commands(hole, dx, dy)
        out['holes'].append(hole)
    for bleed in layer.get('bleeds') or []:
        bleed = dict(bleed)
        translate_point(bleed, dx, dy)
        out['bleeds'].append(bleed)
    return out


def build():
    raw = json.loads(BASE.read_text())
    data = raw['data']
    layers = data['layer']
    for piece in PIECES:
        if piece['layer'] not in layers:
            raise KeyError(piece['layer'])

    widths = [0.0, 0.0]
    heights = [0.0, 0.0]
    for piece in PIECES:
        width = layers[piece['layer']]['totalX']
        height = layers[piece['layer']]['totalY']
        widths[piece['col']] = max(widths[piece['col']], width)
        heights[piece['row']] = max(heights[piece['row']], height)

    origins = {}
    for piece in PIECES:
        x = 0.0 if piece['col'] == 0 else widths[0] + GAP
        y = 0.0 if piece['row'] == 0 else heights[0] + GAP
        origins[piece['id']] = (x, y)

    composite = {
        'faces': [], 'cuts': [], 'folds': [], 'holes': [], 'bleeds': [],
        'bleedFromCuts': False, 'officialBleeds': True,
        'pieceLabels': [],
    }
    piezas = []
    for piece in PIECES:
        source = layers[piece['layer']]
        dx, dy = origins[piece['id']]
        layer = normalise_layer(source, piece, dx, dy)
        composite['faces'] += layer['faces']
        composite['cuts'] += layer['cuts']
        composite['folds'] += layer['folds']
        composite['holes'] += layer['holes']
        composite['bleeds'] += layer['bleeds']
        composite['pieceLabels'].append({
            'id': piece['id'],
            'name': piece['name'],
            'x': dx + 2.0,
            'y': dy + 5.0,
        })
        piezas.append({
            'id': piece['id'],
            'prefix': piece['prefix'],
            'nombre': piece['name'],
            'capa': piece['layer'],
            'espesor_mm': source['thickness'],
            'offset_mm': {'x': dx, 'y': dy},
            'extension_mm': {'x': source['totalX'], 'y': source['totalY']},
            'conteos': {
                'caras': len(layer['faces']),
                'pliegues': len(layer['folds']),
                'cortes': len(layer['cuts']),
                'sangrados': len(layer['bleeds']),
                'orificios': len(layer['holes']),
            },
            'geometria': layer,
        })

    total_x = widths[0] + GAP + widths[1]
    total_y = heights[0] + GAP + heights[1]
    composite['totalX'] = total_x
    composite['totalY'] = total_y
    # La capa `bleeds` de Pacdora es un polígono escalonado que no sigue el
    # corte con un offset uniforme. Para dibujar usamos un contorno calculado
    # a 3 mm del corte (Clipper del editor), conservado en base/bleed-path.txt.
    bleed_path_file = ROOT / 'base' / 'bleed-path.txt'
    composite['bleedPath'] = bleed_path_file.read_text().strip() if bleed_path_file.exists() else ''
    composite['knifeSize'] = {k: data['knifeSize'][k] for k in ('L', 'W', 'H', 'D')}
    composite['size'] = {k: data['size'][k] for k in ('L', 'W', 'H', 'D')}
    composite['outSize'] = {k: data['outSize'][k] for k in ('L', 'W', 'H', 'D')}
    composite['science'] = data['science']
    composite['thickness'] = 2.0
    composite['bleedline'] = 3

    geometry = {
        'modelo': '366010',
        'url': URL,
        'pacdora': {
            'id': data.get('id', 1563),
            'cate_no': data['cate_no'],
            'nameKey': 'custom-dimensions-box-with-lid-luxury-box-dieline-366010',
            'knifeSize': data['knifeSize'],
            'size': data['size'],
            'outSize': data['outSize'],
            'science': data['science'],
            'layerNames': data['layerNames'],
        },
        'layout': {'gap_mm': GAP, 'column_widths': widths, 'row_heights': heights},
        'piezas': piezas,
        'compuesto': composite,
    }
    (ROOT / 'base' / 'geometria.json').write_text(
        json.dumps(geometry, ensure_ascii=False, separators=(',', ':')) + '\n')

    # SVG de la lámina completa. Se dibujan las cuatro piezas en una sola
    # lámina, con una etiqueta por pieza y las capas en orden de impresión.
    width, height = total_x, total_y
    margin = 5.0
    labels = []
    for piece in piezas:
        x0, y0 = piece['offset_mm']['x'], piece['offset_mm']['y']
        label = piece['nombre']
        label_width = len(label) * 2.6 + 3
        labels.append(
            f'<g id="{piece["id"]}-etiqueta">'
            f'<rect x="{num(x0 + 1.5)}" y="{num(y0 + 1.5)}" width="{num(label_width)}" '
            f'height="7.5" rx="0.9" fill="#ffffff" fill-opacity="0.94" stroke="none"/>'
            f'<text x="{num(x0 + 2.5)}" y="{num(y0 + 6.8)}" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="4.5" '
            f'fill="#444b57">{label}</text></g>')

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{num(width + 2 * margin)}mm" height="{num(height + 2 * margin)}mm"
     viewBox="{num(-margin)} {num(-margin)} {num(width + 2 * margin)} {num(height + 2 * margin)}">
<title>366010 · Caja rígida con tapa · 180 × 100 × 40 mm</title>
<desc>Cuatro piezas: fondo y tapa, cartón gris de 2 mm y papel de 0,15 mm. Geometría capturada de Pacdora.</desc>
<rect x="{num(-margin)}" y="{num(-margin)}" width="{num(width + 2 * margin)}" height="{num(height + 2 * margin)}" fill="#ffffff"/>
<g id="caras" fill="#fcfbf8" stroke="#e2e5ea" stroke-width="0.15">{''.join(f'<path d="{path(f["dlist"])}"/>' for f in composite['faces'])}</g>
<g id="sangrado" fill="none" stroke="#51aa20" stroke-width="0.45" stroke-linejoin="round"><path d="{composite['bleedPath'] or path(composite['bleeds'])}"/></g>
<g id="corte" fill="none" stroke="#2028b0" stroke-width="0.8" stroke-linejoin="round"><path d="{path(composite['cuts'])}"/></g>
<g id="pliegues" fill="none" stroke="#d02020" stroke-width="0.55" stroke-dasharray="3 2">{''.join(f'<line x1="{num(f["x1"])}" y1="{num(f["y1"])}" x2="{num(f["x2"])}" y2="{num(f["y2"])}"/>' for f in composite['folds'])}</g>
<g id="etiquetas">{''.join(labels)}</g>
</svg>
'''
    (ROOT / 'troquel-generado.svg').write_text(svg)

    out = {
        'modelo': '366010',
        'nombre': 'Caja rígida con tapa',
        'url': URL,
        'fecha_captura': '2026-10-20',
        'dimensiones_manufactura_mm': {k: data['knifeSize'][k] for k in ('L', 'W', 'H')},
        'dimensiones_interiores_mm': {k: data['size'][k] for k in ('L', 'W', 'H')},
        'dimensiones_exteriores_mm': {k: data['outSize'][k] for k in ('L', 'W', 'H')},
        'material': data['science'],
        'espesor_papel_mm': 0.15,
        'espesor_carton_mm': 2.0,
        'extension_mm': {'x': total_x, 'y': total_y},
        'piezas': piezas,
        'conteos': {
            'piezas': len(piezas),
            'caras': len(composite['faces']),
            'pliegues': len(composite['folds']),
            'cortes': len(composite['cuts']),
            'sangrados': len(composite['bleeds']),
            'orificios': len(composite['holes']),
        },
        'compuesto': composite,
        'procedencia': {
            'url': URL,
            'pacdora_id': data.get('id', 1563),
            'cate_no': data['cate_no'],
            'nameKey': 'custom-dimensions-box-with-lid-luxury-box-dieline-366010',
            'captura': 'REA capture_browser_scenario ev_9bbab1a9d4276e5f6454243d88be37c523f6071b25883dbfdd7913a043478f1a',
        },
        'limites': [
            'Geometría fija de la configuración 180 × 100 × 40 mm; no se reconstruyó un motor paramétrico.',
            'Las muestras L=200, W=120, H=60 y la combinación 190 × 110 × 50 mostraron interacción no aditiva; no se habilitaron medidas editables.',
            'No se validó armado físico, tolerancias de fabricación ni exportación AI/PDF/DXF.',
        ],
    }
    (ROOT / 'troquel-generado.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + '\n')

    manifest = {
        'modelo': '366010',
        'url': URL,
        'capturado': '2026-10-20T15:34:00-03:00',
        'configuracion': {
            'manufactura_mm': {k: data['knifeSize'][k] for k in ('L', 'W', 'H')},
            'interiores_mm': {k: data['size'][k] for k in ('L', 'W', 'H')},
            'exteriores_mm': {k: data['outSize'][k] for k in ('L', 'W', 'H')},
            'material_papel': data['science'],
            'espesor_papel_mm': 0.15,
            'espesor_carton_mm': 2.0,
        },
        'capas': data['layerNames'],
        'archivos': {
            'base/knife-00.json': sha(BASE),
            'base/details.json': sha(ROOT / 'base' / 'details.json'),
            'base/geometria.json': sha(ROOT / 'base' / 'geometria.json'),
            'troquel-generado.svg': sha(ROOT / 'troquel-generado.svg'),
            'troquel-generado.json': sha(ROOT / 'troquel-generado.json'),
            'icono-3d.jpg': sha(ROOT / 'icono-3d.jpg'),
            'dieline-oficial.png': sha(ROOT / 'dieline-oficial.png'),
            'exportado-editor.svg': sha(ROOT / 'exportado-editor.svg'),
            'exportado-editor-210x120x50.svg': sha(ROOT / 'exportado-editor-210x120x50.svg'),
            'exportado-editor-210x120x50-T2.5.svg': sha(ROOT / 'exportado-editor-210x120x50-T2.5.svg'),
            'captura-espesor.png': sha(ROOT / 'captura-espesor.png'),
            'captura-editor.png': sha(ROOT / 'captura-editor.png'),
            'base/bleed-path.txt': sha(ROOT / 'base' / 'bleed-path.txt'),
            'muestras/base-cdp.json': sha(ROOT / 'muestras' / 'base-cdp.json'),
            'muestras/L200.json': sha(ROOT / 'muestras' / 'L200.json'),
            'muestras/W120.json': sha(ROOT / 'muestras' / 'W120.json'),
            'muestras/H60.json': sha(ROOT / 'muestras' / 'H60.json'),
            'muestras/combo.json': sha(ROOT / 'muestras' / 'combo.json'),
            'reglas.json': sha(ROOT / 'reglas.json'),
            'validacion-parametrica.json': sha(ROOT / 'validacion-parametrica.json'),
            'parametricas/manifest.json': sha(ROOT / 'parametricas' / 'manifest.json'),
            'espesor/manifest.json': sha(ROOT / 'espesor' / 'manifest.json'),
            'bleed-node.cjs': sha(ROOT / 'bleed-node.cjs'),
        },
        'evidencia': {
            'rea_captura_pagina_y_geometria': 'ev_9bbab1a9d4276e5f6454243d88be37c523f6071b25883dbfdd7913a043478f1a',
            'rea_segunda_captura_base': 'ev_8a1f522b2feaaf33ae7d8b02bf6d78896d54af4583da1044013d07d7fba9017e',
            'rea_pagina_l200': 'ev_700ae83528d04468565ebaa8c797a41ee7ba549744bc572db355405341c67f77',
            'cdp_matriz': 'parametricas/manifest.json',
            'cdp_espesor': 'espesor/manifest.json',
            'cdp_muestras_iniciales': [
                'muestras/L200.json',
                'muestras/W120.json',
                'muestras/H60.json',
                'muestras/combo.json',
            ],
        },
        'iconos': {
            'mockup': 'https://cdn.pacdora.com/preview/mockup-366010.jpg',
            'dieline': 'https://cdn.pacdora.com/preview/dieline-366010.png',
        },
    }
    (ROOT / 'base' / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f"366010: {total_x:.2f} x {total_y:.2f} mm; "
          f"{len(composite['faces'])} caras, {len(composite['folds'])} pliegues, "
          f"{len(composite['cuts'])} cortes, {len(composite['bleeds'])} sangrados")


if __name__ == '__main__':
    build()
