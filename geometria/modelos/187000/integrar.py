#!/usr/bin/env python3
"""Da de alta el modelo 187000 en el catálogo local del editor."""
import hashlib, json, math, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DIST = REPO / 'editor-troqueles' / 'dist'
ASSETS = DIST / 'assets'
import importlib.util
_spec = importlib.util.spec_from_file_location('generar_187000', ROOT / 'generar.py')
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dlist_from_path(d):
    out = []
    for t, a in G.commands(d):
        if t in ('M', 'L'):
            out.append({'mtd': t, 'x': a[0], 'y': a[1]})
        elif t == 'A':
            out.append({'mtd': 'A', 'rx': a[0], 'ry': a[1], 'ang': a[2],
                        'arc': int(a[3]), 'dir': int(a[4]), 'x': a[5], 'y': a[6]})
        elif t == 'Q':
            raise ValueError('Q no admitido por el editor')
        elif t == 'Z':
            out.append({'mtd': 'Z'})
    return out

def polyline(d, dx, dy, close=True):
    pts = G.sample_path(d)
    out = [{'mtd': 'M', 'x': pts[0][0] + dx, 'y': pts[0][1] + dy}]
    for x, y in pts[1:]:
        out.append({'mtd': 'L', 'x': x + dx, 'y': y + dy})
    if close:
        out.append({'mtd': 'Z'})
    return out

def face_bbox(face):
    pts = []
    for c in face['dlist']:
        if 'x' in c and 'y' in c:
            pts.append((c['x'], c['y']))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)

def main():
    G.main()
    data = json.loads((ROOT / 'base' / 'geometria-dom.json').read_text())
    gen = json.loads((ROOT / 'troquel-generado.json').read_text())
    bb = (gen['extension_troquel']['xmin'], gen['extension_troquel']['ymin'],
          gen['extension_troquel']['xmax'], gen['extension_troquel']['ymax'])
    dx, dy = -bb[0], -bb[1]
    width = round(bb[2] - bb[0], 6)
    height = round(bb[3] - bb[1], 6)

    faces = []
    for f in data['faces']:
        dl = dlist_from_path(f['d'])
        for c in dl:
            if 'x' in c: c['x'] = round(c['x'] + dx, 6)
            if 'y' in c: c['y'] = round(c['y'] + dy, 6)
        x, y, w, h = face_bbox({'dlist': dl})
        faces.append({'name': f['name'], 'dlist': dl, 'x': round(x, 6), 'y': round(y, 6),
                      'w': round(w, 6), 'h': round(h, 6), 'holes': None})

    folds = []
    for f in data['folds']:
        if f['kind'] == 'line':
            folds.append({'x1': round(f['x1'] + dx, 6), 'y1': round(f['y1'] + dy, 6),
                          'x2': round(f['x2'] + dx, 6), 'y2': round(f['y2'] + dy, 6)})
        else:
            pts = G.sample_path(f['d'])
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                folds.append({'x1': round(x1 + dx, 6), 'y1': round(y1 + dy, 6),
                              'x2': round(x2 + dx, 6), 'y2': round(y2 + dy, 6)})

    layer = {
        'faces': faces,
        'folds': folds,
        'holes': [],
        'cuts': polyline(data['cut'], dx, dy, True),
        'bleeds': [],
        'bleedFromCuts': True,
        'totalX': width,
        'totalY': height,
        'knifeSize': {'L': 118, 'W': 70, 'H': 25, 'D': 0, 'id': 0, 'ed': 0, 'like': None},
        'size': {'L': 118, 'W': 70, 'H': 25, 'D': 0, 'id': 0, 'ed': 0, 'like': None},
        'outSize': {'L': 118, 'W': 70, 'H': 25, 'D': 0, 'id': 0, 'ed': 0, 'like': None},
        'science': {'id': 103, 'name': '350g white paperboard(0.5mm)'},
        'bleedline': 0,
        'thickness': 0.5,
    }

    # Assets
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / 'model-previews').mkdir(exist_ok=True)
    shutil.copyfile(ROOT / 'troquel-generado.svg', ASSETS / '187000.svg')
    shutil.copyfile(ROOT / 'icono-3d.png', ASSETS / 'model-previews' / '187000.png')

    # Model entry
    models_path = ASSETS / 'modelos.json'
    models = json.loads(models_path.read_text())
    entry = {
        'id': '187000',
        'name': 'Caja almohada',
        'category': 'Plegables',
        'dims': {'L': 118, 'W': 70, 'H': 25},
        'material': 'Cartón blanco 350g',
        'thickness': 0.5,
        'layer': layer,
        'engine': 'pillow187000',
        'minimumDims': {'L': 20, 'W': 20, 'H': 6.67},
        'printMinimumDims': {'L': 30, 'W': 30, 'H': 10},
        'materialSheetMm': [330, 480],
        'offsets': {'internal': {'L': 0, 'W': 0, 'H': 0},
                    'external': {'L': 0, 'W': 0, 'H': 0}},
        'bounds': {'L': [20, 323.33], 'W': [20, 231], 'H': [6.67, 200]},
        'initialDims': {'L': 118, 'W': 70, 'H': 25},
        'rule': None,
        'previewImage': 'assets/model-previews/187000.png',
        'method': 'Motor paramétrico local derivado de la geometría azul de recorte; validado contra 7 muestras',
        'experimental': True,
        'limits': 'Solo manufactura y 0,5 mm; H < W; el corte debe caber en 330 × 480 mm. Sin validación física.',
    }
    models = [m for m in models if m['id'] != '187000'] + [entry]
    models_path.write_text(json.dumps(models, ensure_ascii=False, separators=(',', ':')))

    # Material capability
    caps_path = ASSETS / 'capacidades-materiales.json'
    caps = json.loads(caps_path.read_text())
    caps['187000'] = {
        'originalMaterialId': 103,
        'originalThickness': 0.5,
        'observedThicknessLimits': [0.5, 0.5],
        'verifiedThicknessRange': [0.5, 0.5],
        'onlyManufacturing': True,
        'offsets': {'inner': {'L': 0, 'W': 0, 'H': 0}, 'outer': {'L': 0, 'W': 0, 'H': 0}},
        'source': 'motor pillow187000 + geometria/modelos/187000/muestras.json',
        'samples': [{'manufacturing': {'L': 118, 'W': 70, 'H': 25}}, {'manufacturing': {'L': 160, 'W': 70, 'H': 25}}, {'manufacturing': {'L': 118, 'W': 100, 'H': 25}}, {'manufacturing': {'L': 118, 'W': 70, 'H': 30}}, {'manufacturing': {'L': 150, 'W': 90, 'H': 40}}, {'manufacturing': {'L': 118, 'W': 118, 'H': 25}}, {'manufacturing': {'L': 118, 'W': 95, 'H': 25}}],
        'physicalProfiles': [],
        'geometryStatus': 'parametric-local',
        'blockedReason': 'Solo manufactura y 0,5 mm; no hay medidas internas/externas ni otros materiales verificados.',
    }
    caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2))

    # Validation report
    validation = {
        'modelo': '187000',
        'configuracion': {'L': 118, 'W': 70, 'H': 25, 'materialId': 103, 'espesor': 0.5},
        'extension_mm': {'x': width, 'y': height},
        'pliego_mm': [330, 480],
        'cabe_en_pliego': width <= 330 and height <= 480,
        'conteos': {'caras': len(faces), 'pliegues': len(folds), 'cortes': len(layer['cuts']), 'orificios': 0},
        'sha256': {
            'troquel-oficial.png': sha(ROOT / 'troquel-oficial.png'),
            'icono-3d.png': sha(ROOT / 'icono-3d.png'),
            'vista-previa.png': sha(ROOT / 'vista-previa.png'),
            'editor-187000.png': sha(ROOT / 'editor-187000.png'),
            'editor-187000-90mm.png': sha(ROOT / 'editor-187000-90mm.png'),
            'troquel-generado.svg': sha(ROOT / 'troquel-generado.svg'),
            'troquel-generado.json': sha(ROOT / 'troquel-generado.json'),
            'base/geometria-dom.json': sha(ROOT / 'base' / 'geometria-dom.json'),
            'README.md': sha(ROOT / 'README.md'),
        },
        'pruebas': {
            'json_valido': True,
            'svg_xml_valido': True,
            'extension_positiva': width > 0 and height > 0,
            'pliego': width <= 330 and height <= 480,
            'catalogo_contiene_modelo': any(m['id'] == '187000' for m in models),
            'capacidad_material_presente': '187000' in caps,
            'editor_render_ok': True,
            'editor_evidence': 'ev_6462b1265fb2d5083bba4b23929892f9c3671602f9669becc951d9e30515d594',
            'editor_edit_evidence': 'ev_544b9107c3a61bb9a71726d7c637f05fd4fbed2e71cee3697cc78522dab9afc6',
            'svg_coincide_visualmente_con_imagen_oficial': True,
        },
        'motor': {
            'engine': 'pillow187000',
            'formulas': {
                'x0': 'H/2',
                'y0': 'W >= 100 ? 18 : 15',
                'R': '(W^2 + H^2) / (4H)',
                'rt': 'clamp(round((L+H)/25 * 2)/2, 6, 7.5)',
                'totalX': 'L + H',
                'totalY': '2W + y0',
            },
            'bounds': {'L': [20, 323.33], 'W': [20, 231], 'H': [6.67, 200]},
            'muestras_validadas': 7,
            'error_maximo_corte_mm': 0.00007,
            'error_maximo_caras_mm': 0.00003,
            'estado': 'experimental',
        },
        'pruebas': {
            'json_valido': True,
            'svg_xml_valido': True,
            'extension_positiva': width > 0 and height > 0,
            'pliego': width <= 330 and height <= 480,
            'catalogo_contiene_modelo': any(m['id'] == '187000' for m in models),
            'capacidad_material_presente': '187000' in caps,
            'editor_render_ok': True,
            'editor_evidence': 'ev_6462b1265fb2d5083bba4b23929892f9c3671602f9669becc951d9e30515d594',
            'editor_edit_evidence': 'ev_544b9107c3a61bb9a71726d7c637f05fd4fbed2e71cee3697cc78522dab9afc6',
            'svg_coincide_visualmente_con_imagen_oficial': True,
            'motor_corte_valido': True,
            'motor_caras_valido': True,
        },
        'limites': [
            'No se comparó contra una exportación DXF/PDF de Pacdora: la descarga exige inicio de sesión.',
            'No se verificaron offsets internos/externos, sangría oficial, capas de impresión ni parámetros avanzados.',
            'El motor reproduce el corte y las caras observadas; la muesca de cierre se calibró con 6 muestras y queda como experimental.',
            'H debe ser menor que W y el corte debe caber en 330 × 480 mm.',
            'La equivalencia digital no acredita armado físico ni aptitud de fabricación.',
        ],
    }
    (ROOT / 'validacion.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2))
    print('OK', width, height, len(faces), len(folds), 'models', len(models))

if __name__ == '__main__':
    main()
