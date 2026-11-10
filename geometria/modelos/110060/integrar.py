"""Alta reproducible del modelo 110060 en el editor local."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / 'geometria/modelos/110060'
ASSETS = ROOT / 'editor-troqueles/dist/assets'


def main():
    base = json.loads((MODEL / 'base/knife-00.json').read_text())['data']
    rule = json.loads((MODEL / 'reglas-parametricas.json').read_text())
    validation = json.loads((MODEL / 'validacion-parametrica.json').read_text())
    dims = {axis: base['knifeSize'][axis] for axis in 'LWH'}
    offsets = {
        'internal': {axis: base['size'][axis] - dims[axis] for axis in dims},
        'external': {axis: base['outSize'][axis] - dims[axis] for axis in dims},
    }
    layer = {k: v for k, v in base['layer']['traditional'].items() if k not in ['bleeds', 'sizeArrowData']}
    ranges = validation['validatedRange']
    entry = {
        'id': '110060',
        'name': 'Caja para baraja',
        'category': 'Plegables',
        'dims': dims,
        'material': 'Cartón blanco 350g',
        'thickness': 0.5,
        'layer': layer,
        'engine': 'compiled',
        'offsets': offsets,
        'bounds': {axis: list(ranges[axis]) for axis in 'LWH'},
        'referenceBounds': {axis: list(ranges[axis]) for axis in 'LWH'},
        'verifiedBounds': {axis: list(ranges[axis]) for axis in 'LWH'},
        'expandedBounds': {axis: list(ranges[axis]) for axis in 'LWH'},
        'minimumDims': {'L': 20.6, 'W': 15.6, 'H': 20.6},
        'rule': {
            'features': rule['features'],
            'tables': rule.get('tables'),
            'tables2d': rule.get('tables2d'),
            'regimes': rule.get('regimes'),
            'rules': rule['rules'],
        },
        'previewImage': 'assets/model-previews/110060.png',
        'experimental': False,
        'method': validation['method'],
        'limits': validation['limits'],
        'validation': validation,
    }
    models_path = ASSETS / 'modelos.json'
    models = json.loads(models_path.read_text())
    models = [m for m in models if m['id'] != '110060']
    models.append(entry)
    models_path.write_text(json.dumps(models, ensure_ascii=False, separators=(',', ':')))

    caps_path = ASSETS / 'capacidades-materiales.json'
    caps = json.loads(caps_path.read_text())
    caps['110060'] = {
        'originalMaterialId': 103,
        'originalThickness': 0.5,
        'observedThicknessLimits': [0.2, 0.5],
        'verifiedThicknessRange': [0.5, 0.5],
        'onlyManufacturing': bool(base['modeCate'].get('IsOnlyManufacture')),
        'offsets': {'inner': offsets['internal'], 'outer': offsets['external']},
        'source': 'geometria/modelos/110060/base/knife-00.json',
        'samples': [],
        'physicalProfiles': [],
        'geometryStatus': 'compiled-parametric',
        'blockedReason': 'Solo cartón blanco de 0,5 mm; no hay geometría para otros materiales o espesores.',
    }
    caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2))

    shutil.copyfile(MODEL / 'troquel-generado.svg', ASSETS / '110060.svg')
    print('110060: alta local completada')


if __name__ == '__main__':
    main()
