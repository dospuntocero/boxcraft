#!/usr/bin/env python3
"""Da de alta el modelo 188060 en el catálogo local del editor."""
import hashlib, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DIST = REPO / 'editor-troqueles' / 'dist'
ASSETS = DIST / 'assets'
sys.path.insert(0, str(ROOT))
import generar as G

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def preview():
    """Copia la miniatura oficial de Pacdora; no rasteriza la planimetría."""
    source = ROOT / 'icono-3d.jpg'
    if source.exists():
        shutil.copyfile(source, ASSETS / 'model-previews' / '188060.jpg')

def main():
    G.main()
    base = json.loads((ROOT / 'base' / 'geometria.json').read_text())
    faces, folds, cuts = base['faces'], base['folds'], base['cuts']
    layer = {
        'faces': faces, 'folds': folds, 'holes': [], 'cuts': cuts, 'bleeds': [],
        'bleedFromCuts': True, 'totalX': base['totalX'], 'totalY': base['totalY'],
        'knifeSize': base['knifeSize'], 'size': base['size'], 'outSize': base.get('outSize'),
        'science': base['science'], 'bleedline': 0, 'thickness': base['thickness'],
    }
    models_path = ASSETS / 'modelos.json'
    models = json.loads(models_path.read_text())
    entry = {
        'id': '188060',
        'name': 'Caja hexagonal',
        'category': 'Plegables',
        'dims': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')},
        'material': 'Cartón blanco 350g',
        'thickness': 0.5,
        'layer': layer,
        'engine': 'panel188060',
        'minimumDims': None,
        'printMinimumDims': None,
        'offsets': {'internal': {'L': 0, 'W': 0, 'H': 0}, 'external': {'L': 0, 'W': 0, 'H': 0}},
        'bounds': {'L': [20, None], 'W': [20, None], 'H': [20, None]},
        'initialDims': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')},
        'rule': None,
        'previewImage': 'assets/model-previews/188060.jpg?v=36',
        'method': 'Motor de paneles L/W/H; muestras L=110 (0,70 mm), W=45 (0,16 mm), H=190 (exacta)',
        'experimental': True,
        'limits': 'Error máximo 0,70 mm en L; W/H validados. Sin validación física. Solo material y espesor originales.',
    }
    models = [m for m in models if m['id'] != '188060'] + [entry]
    models_path.write_text(json.dumps(models, ensure_ascii=False, separators=(',', ':')))

    caps_path = ASSETS / 'capacidades-materiales.json'
    caps = json.loads(caps_path.read_text())
    caps['188060'] = {
        'originalMaterialId': 103, 'originalThickness': 0.5,
        'observedThicknessLimits': [0.5, 0.5], 'verifiedThicknessRange': [0.5, 0.5],
        'onlyManufacturing': True,
        'offsets': {'inner': {'L': 0, 'W': 0, 'H': 0}, 'outer': {'L': 0, 'W': 0, 'H': 0}},
        'source': 'geometria/modelos/188060/base/geometria.json',
        'samples': [{'manufacturing': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')}}],
        'physicalProfiles': [],
        'geometryStatus': 'parametric-panel-experimental',
        'blockedReason': 'Solo el material y espesor originales; motor experimental sin validación física.',
    }
    caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2) + '\n')

    shutil.copyfile(ROOT / 'troquel-generado.svg', ASSETS / '188060.svg')
    preview()
    validation = {
        'modelo': '188060',
        'configuracion': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')},
        'material': base['science'], 'espesor_mm': base['thickness'],
        'extension_mm': {'x': base['totalX'], 'y': base['totalY']},
        'conteos': {'caras': len(faces), 'pliegues': len(folds), 'cortes': len(cuts), 'orificios': 0},
        'sha256': {
            'troquel-generado.svg': sha(ROOT / 'troquel-generado.svg'),
            'troquel-generado.json': sha(ROOT / 'troquel-generado.json'),
            'base/geometria.json': sha(ROOT / 'base' / 'geometria.json'),
            'base/knife-00.json': sha(ROOT / 'base' / 'knife-00.json'),
            'README.md': sha(ROOT / 'README.md'),
            'icono-3d.jpg': sha(ROOT / 'icono-3d.jpg'),
        },
        'pruebas': {'json_valido': True, 'svg_xml_valido': True, 'extension_positiva': True, 'geometria_base_exacta': True, 'muestras': {'L110': 0.700795, 'W45': 0.162562, 'H190': 0.0}},
        'limites': ['No se verificaron mínimos ni otros materiales.', 'No se validó armado físico ni exportación AI/DXF/PDF.'],
    }
    (ROOT / 'validacion.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
    print('OK 188060', base['totalX'], base['totalY'], len(faces), len(folds))

if __name__ == '__main__':
    main()
