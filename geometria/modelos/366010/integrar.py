#!/usr/bin/env python3
"""Da de alta el modelo 366010 en el catálogo local del editor."""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DIST = REPO / 'editor-troqueles' / 'dist'
ASSETS = DIST / 'assets'
import importlib.util
_spec = importlib.util.spec_from_file_location('generar_366010', ROOT / 'generar.py')
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)


def read(path):
    return json.loads(path.read_text())


def write(path, data, pretty=False):
    text = json.dumps(data, ensure_ascii=False, indent=2 if pretty else None,
                      separators=None if pretty else (',', ':'))
    path.write_text(text + ('\n' if pretty else ''))


def ensure_material():
    path = ASSETS / 'materiales.json'
    catalog = read(path)
    material = {
        'id': 366010,
        'name': 'Cartón gris + papel 0,15 mm',
        'group': 'Rígido',
        'thickness': 2.0,
        'min': 1.5,
        'max': 2.5,
        'adjustable': True,
        'inless': 0,
        'outless': 0,
    }
    catalog['materials'] = [m for m in catalog['materials'] if m['id'] != 366010] + [material]
    write(path, catalog, pretty=True)


def ensure_category():
    path = DIST / 'index.html'
    text = path.read_text()
    if 'value="Rígidas"' not in text:
        text = text.replace(
            '<option value="Plegables" data-i18n="Plegables">Plegables</option>',
            '<option value="Plegables" data-i18n="Plegables">Plegables</option>'
            '<option value="Rígidas" data-i18n="Rígidas">Rígidas</option>')
        path.write_text(text)
    import re
    for locale, label in (('es', 'Rígidas'), ('en', 'Rigid')):
        locale_path = DIST / 'locales' / f'{locale}.js'
        locale_text = locale_path.read_text()
        if '"Rígidas"' not in locale_text:
            locale_text = re.sub(
                r'(\n\s*"Plegables": "[^"]*",)',
                rf'\1\n  "Rígidas": "{label}",',
                locale_text, count=1)
            locale_path.write_text(locale_text)


def main():
    G.build()
    generated = read(ROOT / 'troquel-generado.json')
    rule = read(ROOT / 'reglas.json')
    layer = generated['compuesto']
    layer['multiPiece'] = True
    layer['thickness'] = 2.0
    # El sangrado dibujado se calcula desde el corte (3 mm). La capa `bleeds`
    # original se conserva en la evidencia, pero no se usa para dibujar porque
    # es un polígono escalonado que no sigue el contorno.
    layer['officialBleeds'] = False
    layer['bleedFromCuts'] = True
    layer['bleedPath'] = generated['compuesto'].get('bleedPath', '')

    models_path = ASSETS / 'modelos.json'
    models = read(models_path)
    entry = {
        'id': '366010',
        'name': 'Caja rígida con tapa',
        'category': 'Rígidas',
        'dims': {k: generated['dimensiones_manufactura_mm'][k] for k in ('L', 'W', 'H')},
        'material': 'Cartón gris + papel 0,15 mm',
        'thickness': 2.0,
        'layer': layer,
        'engine': 'rigid366010',
        'rule': rule,
        'minimumDims': {'L': 160, 'W': 80, 'H': 30},
        'printMinimumDims': None,
        'offsets': {'internal': {'L': 0, 'W': 0, 'H': 0},
                    'external': {'L': 0, 'W': 0, 'H': 0}},
        'bounds': {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]},
        'referenceBounds': {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]},
        'expandedBounds': {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]},
        'verifiedBounds': {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]},
        'initialDims': {'L': 180, 'W': 100, 'H': 40},
        'previewImage': 'assets/model-previews/366010.jpg?v=1',
        'method': 'Ajuste afín por régimen (A: L<200; B: L≥200 con exterior variable); error máximo 0,01 mm',
        'experimental': True,
        'limits': ('L 160–220 mm, W 80–140 mm, H 30–70 mm. En L=200 cambia la profundidad '
                   'exterior; no se extrapola fuera del rango ni se validó el armado físico.'),
        'multiPiece': True,
        'source': generated['url'],
    }
    models = [m for m in models if m['id'] != '366010'] + [entry]
    write(models_path, models)

    caps_path = ASSETS / 'capacidades-materiales.json'
    caps = read(caps_path)
    caps['366010'] = {
        'originalMaterialId': 366010,
        'originalThickness': 2.0,
        'observedThicknessLimits': [1.5, 2.5],
        'verifiedThicknessRange': [1.5, 2.5],
        'thicknessRange': [1.5, 2.5],
        'thicknessStep': 0.25,
        'onlyManufacturing': True,
        'offsets': {'inner': {'L': 0, 'W': 0, 'H': 0},
                    'outer': {'L': 0, 'W': 0, 'H': 0}},
        'source': 'geometria/modelos/366010/base/geometria.json',
        'samples': [{'manufacturing': {'L': 180, 'W': 100, 'H': 40}}],
        'physicalProfiles': [],
        'geometryStatus': 'parametric-piecewise',
        'blockedReason': ('L 160–220 mm, W 80–140 mm, H 30–70 mm y espesor '
                          '1,5–2,5 mm. Fuera de ese rango no hay geometría verificada.'),
    }
    write(caps_path, caps, pretty=True)

    ensure_material()
    ensure_category()

    shutil.copyfile(ROOT / 'troquel-generado.svg', ASSETS / '366010.svg')
    (ASSETS / 'model-previews').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'icono-3d.jpg', ASSETS / 'model-previews' / '366010.jpg')
    shutil.copyfile(ROOT / 'vista-previa.png', ASSETS / 'model-previews' / '366010.png')

    validation = read(ROOT / 'validacion.json')
    validation['integracion'] = {
        'catalogo': 'editor-troqueles/dist/assets/modelos.json',
        'capacidades': 'editor-troqueles/dist/assets/capacidades-materiales.json',
        'material': 366010,
        'assets': ['assets/366010.svg', 'assets/model-previews/366010.jpg',
                   'assets/model-previews/366010.png'],
        'categoria': 'Rígidas',
    }
    (ROOT / 'validacion.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
    print('OK 366010 integrado;', len(layer['faces']), 'caras,', len(layer['cuts']), 'cortes')


if __name__ == '__main__':
    main()
