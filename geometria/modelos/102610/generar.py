"""Reproduce el modelo 102610 con las medidas iniciales capturadas."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    data = json.loads((ROOT / 'base' / 'knife-00.json').read_text())['data']
    layer = {k: v for k, v in data['layer']['traditional'].items() if k not in ['bleeds', 'sizeArrowData']}
    output = {
        'model': '102610',
        'source': 'captured-public-template',
        'source_url': 'https://www.pacdora.com/es/dielines-detail/custom-dimensions-back-open-boxes-double-tray-dieline-102610',
        'manufacturing_size_mm': {k: data['knifeSize'][k] for k in 'LWH'},
        'inner_size_mm': {k: data['size'][k] for k in 'LWH'},
        'outer_size_mm': {k: data['outSize'][k] for k in 'LWH'},
        'material': data['science']['name'],
        'thickness_mm': layer['thickness'],
        'layer': layer,
        'excluded': ['bleeds', 'sizeArrowData'],
        'limits': 'Medidas iniciales; motor paramétrico verificado; no validado para fabricación',
    }
    (ROOT / 'troquel-generado.json').write_text(json.dumps(output, indent=2, ensure_ascii=False))
    spec = importlib.util.spec_from_file_location('svg_renderer', ROOT.parents[1] / 'modelo-parametrico.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    svg = renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201', 'Modelo 102610').replace('stroke-width="1"', 'stroke-width="0.2"').replace('stroke-dasharray="6 3"', 'stroke-dasharray="2 1"')
    (ROOT / 'troquel-generado.svg').write_text(svg)
    print('102610: 120,6 × 60,6 × 161,6 mm; 13 caras, 12 pliegues, sin aberturas')


if __name__ == '__main__':
    main()
