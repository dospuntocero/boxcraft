"""Integra las reconstrucciones locales; no depende del servicio de Pacdora."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEOMETRY = ROOT.parent / 'geometria/modelos'
ASSET = ROOT / 'dist/assets/modelos.json'

def integrate():
    models = json.loads(ASSET.read_text())
    report = []
    sheet_limits = {
        '150010': ([20, 22, 17.6], [1000, 700]),
        '112047': ([30, 30, 30.6], [1000, 700]),
        '12109002': ([30, 30, 30.6], [1000, 700]),
        '112310': ([40, 40, 41], [1200, 2300]),
        '10001006': ([15, 10.6, 15.6], [1000, 700]),
        '10002003': ([15, 16.1, 20.6], [1000, 700]),
    }
    for model in models:
        code = model['id']
        preview = ROOT/'dist/assets/model-previews'/f'{code}.png'
        if preview.exists():
            model['previewImage'] = f'assets/model-previews/{code}.png'
        elif (ROOT/'dist/assets/pacdora'/f'{code}.png').exists():
            model['previewImage'] = f'assets/pacdora/{code}.png'
        if code == '102010':
            model['materialSheetMm'] = [1000, 700]
            model['minimumDims'] = {'L': 15, 'W': 10.6, 'H': 20.6}
            model['referenceBounds'] = {'H': [20.6, None]}
            model['bounds'] = model['referenceBounds'].copy()
            model['expandedBounds'] = model['referenceBounds'].copy()
        if code == '10001029':
            model['materialSheetMm'] = [1000, 700]
            model['referenceBounds'] = {axis: [low, None] for axis, low in {'L': 15, 'W': 10.6, 'H': 15.6}.items()}
            model['bounds'] = model['referenceBounds'].copy()
            model['expandedBounds'] = model['referenceBounds'].copy()
        if code == '200010':
            # Width of the unfolded blank is the material constraint, not an arbitrary box maximum.
            minimums = {'L': 30, 'W': 24, 'H': 20.6}
            model['materialWidthMm'] = 1200
            model['materialSheetMm'] = [1200, 2300]
            model['sheetBleed'] = 0  # the blank uses the full 1200 mm sheet width
            model['initialDims'] = {'L': 434, 'W': 144, 'H': 278}
            model['referenceBounds'] = {axis: [low, None] for axis, low in minimums.items()}
            model['bounds'] = model['referenceBounds'].copy()
            model['expandedBounds'] = model['referenceBounds'].copy()
        if code in ['150010', '112047', '12109002', '112310', '10002003', '180370']:
            folder = GEOMETRY / code / 'parametricas'
            rule = json.loads((folder / 'reglas.json').read_text())
            model['layer'] = rule['template']
            model['engine'] = 'derived'
            model['rule'] = {'base': rule['base'], 'axes': list('LWH'), 'rules': rule['rules']}
            model['bounds'] = dict(zip('LWH', rule['bounds']))
            validations = json.loads((folder / 'validacion.json').read_text()) if (folder / 'validacion.json').exists() else []
            model['experimental'] = not validations or not all(v['pass'] for v in validations)
            model['method'] = 'Reglas por coordenada obtenidas de variaciones de medidas'
            model['verifiedBounds'] = model['bounds'].copy() if not model['experimental'] else {}
            model['referenceBounds'] = model['bounds'].copy()
            model['expandedBounds'] = {axis: [round(v*.75, 3), round(v*1.5, 3)] for axis, v in model['dims'].items()}
            report.append({'id': code, 'method': model['method'], 'experimental': model['experimental'], 'validation': validations})
        elif code in ['10001006', '180320']:
            model['engine'] = 'panels'
            model['experimental'] = True
            model['method'] = 'Reconstrucción por paneles y líneas de plegado del plano original'
            model['bounds'] = {axis: [round(v*.9, 3), round(v*1.1, 3)] for axis, v in model['dims'].items()}
            model['referenceBounds'] = model['bounds'].copy()
            model['verifiedBounds'] = {}
            model['expandedBounds'] = {axis: [round(v*.75, 3), round(v*1.5, 3)] for axis, v in model['dims'].items()}
            model['rule'] = {'recipe': code}
            report.append({'id': code, 'method': model['method'], 'experimental': True, 'validation': 'Identity at original dimensions; independent source variations unavailable'})
        if code == '10002003':
            model.pop('editabilityIssue', None)
        if code == '180370':
            model['materialSheetMm'] = [1000, 700]
            model['minimumDims'] = {'L': 40, 'W': 30}
            for bounds_key in ['bounds', 'referenceBounds', 'expandedBounds']:
                model[bounds_key].update({'L': [40, None], 'W': [30, None]})
        if code in sheet_limits:
            minimums, sheet = sheet_limits[code]
            model['materialSheetMm'] = sheet
            model['minimumDims'] = dict(zip('LWH', minimums))
            model['referenceBounds'] = {axis: [low, None] for axis, low in model['minimumDims'].items()}
            model['bounds'] = model['referenceBounds'].copy()
            model['expandedBounds'] = model['referenceBounds'].copy()
            if code == '12109002':
                model['initialDims'] = {'L': 200, 'W': 140, 'H': 120}
    ASSET.write_text(json.dumps(models, ensure_ascii=False, separators=(',', ':')))
    (ROOT/'validacion-parametrizacion.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print('Modelos editables:', sum(bool(m['engine']) for m in models))

if __name__ == '__main__':
    integrate()
