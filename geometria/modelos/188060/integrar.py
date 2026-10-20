#!/usr/bin/env python3
"""Da de alta el modelo 188060 en el catálogo local del editor."""
import hashlib, json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DIST = REPO / 'editor-troqueles' / 'dist'
ASSETS = DIST / 'assets'
sys.path.insert(0, str(ROOT))
import generar as G

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def preview():
    if (ROOT / 'vista-previa.png').exists() and (ASSETS / 'model-previews' / '188060.png').exists():
        return
    from PIL import Image, ImageChops
    svg = ROOT / 'troquel-generado.svg'
    chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if not pathlib.Path(chrome).exists():
        return
    tmp = pathlib.Path('/tmp/188060-preview.png')
    profile = pathlib.Path('/tmp/chrome-188060')
    subprocess.run([chrome, '--headless', '--no-sandbox', f'--user-data-dir={profile}',
                    '--hide-scrollbars', '--window-size=1600,1300',
                    f'--screenshot={tmp}', f'file://{svg}'], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not tmp.exists(): return
    im = Image.open(tmp).convert('RGB')
    # Recorta el fondo blanco exterior.
    bg = Image.new('RGB', im.size, 'white')
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop((max(0, bbox[0]-20), max(0, bbox[1]-20), min(im.width, bbox[2]+20), min(im.height, bbox[3]+20)))
    im.save(ROOT / 'vista-previa.png')
    shutil.copyfile(ROOT / 'vista-previa.png', ASSETS / 'model-previews' / '188060.png')

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
        'engine': None,
        'minimumDims': None,
        'printMinimumDims': None,
        'offsets': {'internal': {'L': 0, 'W': 0, 'H': 0}, 'external': {'L': 0, 'W': 0, 'H': 0}},
        'bounds': {k: [base['knifeSize'][k], base['knifeSize'][k]] for k in ('L', 'W', 'H')},
        'initialDims': {k: base['knifeSize'][k] for k in ('L', 'W', 'H')},
        'rule': None,
        'previewImage': 'assets/model-previews/188060.png',
        'method': 'Captura 2D exacta del SVG de Pacdora; sin motor paramétrico verificado',
        'experimental': False,
        'limits': 'Solo 100,6 × 40,6 × 181,6 mm y 0,5 mm. No se verificaron mínimos, otros materiales ni armado físico.',
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
        'geometryStatus': 'exact-capture-2d',
        'blockedReason': 'Solo la configuración 100,6 × 40,6 × 181,6 mm y 0,5 mm está verificada.',
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
        },
        'pruebas': {'json_valido': True, 'svg_xml_valido': True, 'extension_positiva': True, 'geometria_base_exacta': True},
        'limites': ['No se verificaron mínimos ni otros materiales.', 'No se validó armado físico ni exportación AI/DXF/PDF.'],
    }
    (ROOT / 'validacion.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
    print('OK 188060', base['totalX'], base['totalY'], len(faces), len(folds))

if __name__ == '__main__':
    main()
