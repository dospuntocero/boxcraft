"""Aplica el estado de validación de cada modelo al catálogo local.

El estado no se escribe a mano: se deriva de `validacion-parametrica.json`.
Un modelo solo queda como verificado si el informe declara `status: verified`,
la topología es estable y el error máximo está dentro de la tolerancia.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEOMETRY = ROOT.parent / 'geometria' / 'modelos'
ASSET = ROOT / 'dist' / 'assets' / 'modelos.json'


def load_report(code):
    path = GEOMETRY / code / 'validacion-parametrica.json'
    if not path.exists():
        return None
    return json.loads(path.read_text())


def apply(models, check=False):
    changed = []
    for model in models:
        code = model['id']
        report = load_report(code)
        if report:
            status = report.get('status')
            if status not in ('verified', 'experimental', 'fixed'):
                raise SystemExit(f'{code}: estado inválido {status!r}')
            tolerance = float(report.get('toleranceMm', 1e-4))
            max_error = float(report.get('maxErrorMm', report.get('error_max_mm', 0)))
            sample_count = int(report.get('sampleCount', report.get('holdoutCount', report.get('muestras', 0))))
            if status == 'verified' and (max_error > tolerance or not report.get('topologyStable', True) or sample_count < 1):
                raise SystemExit(f'{code}: informe verificado incoherente')
            model['validation'] = report
            model['experimental'] = status != 'verified'
            if status == 'verified':
                model['verifiedBounds'] = report.get('validatedRange') or model.get('bounds', {})
                model['referenceBounds'] = model.get('bounds', {}).copy() if isinstance(model.get('bounds'), dict) else model.get('referenceBounds')
            model['method'] = report.get('method', model.get('method'))
            if report.get('limits'):
                model['limits'] = report['limits']
            changed.append(code)
    return changed


def main(check=False):
    models = json.loads(ASSET.read_text())
    before = json.dumps(models, ensure_ascii=False, separators=(',', ':'))
    changed = apply(models, check=check)
    after = json.dumps(models, ensure_ascii=False, separators=(',', ':'))
    if check and before != after:
        raise SystemExit('aplicar-estados: el catálogo no está actualizado')
    if not check:
        ASSET.write_text(after)
    print(f'{len(changed)} modelos con informe aplicado: {", ".join(changed)}')


if __name__ == '__main__':
    import sys
    main(check='--check' in sys.argv)
