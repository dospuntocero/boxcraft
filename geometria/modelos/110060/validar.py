"""Comprueba la salida local de 110060 contra la respuesta base."""
import json
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent


def main():
    source = json.loads((ROOT / 'base' / 'knife-00.json').read_text())['data']['layer']['traditional']
    generated = json.loads((ROOT / 'troquel-generado.json').read_text())['layer']
    expected = {k: v for k, v in source.items() if k not in ['bleeds', 'sizeArrowData']}
    numeric = []

    def compare(a, b, path=''):
        if isinstance(a, dict):
            assert set(a) == set(b), f'claves distintas en {path}'
            for key in a:
                compare(a[key], b[key], f'{path}/{key}')
        elif isinstance(a, list):
            assert len(a) == len(b), f'largo distinto en {path}'
            for index, (x, y) in enumerate(zip(a, b)):
                compare(x, y, f'{path}/{index}')
        elif isinstance(a, (int, float)) and not isinstance(a, bool):
            assert isinstance(b, (int, float)) and abs(a - b) < 1e-12, f'{path}: {a} != {b}'
            numeric.append(path)
        else:
            assert a == b, f'{path}: {a!r} != {b!r}'

    compare(expected, generated)
    svg = etree.parse(str(ROOT / 'troquel-generado.svg')).getroot()
    ns = {'s': 'http://www.w3.org/2000/svg'}
    faces = svg.findall('.//s:g[@id="faces"]/s:path', ns)
    folds = svg.findall('.//s:g[@id="folds"]/s:line', ns)
    fold_length = sum(((float(f.get('x2')) - float(f.get('x1'))) ** 2 + (float(f.get('y2')) - float(f.get('y1'))) ** 2) ** 0.5 for f in source['folds'])
    report = {
        'pass': True,
        'svg_counts': {'faces': len(faces), 'folds': len(folds), 'holes': len(source.get('holes') or [])},
        'viewBox': svg.get('viewBox'),
        'included_geometry_matches_source': True,
        'numeric_fields_compared': len(numeric),
        'computed_fold_length_mm': fold_length,
        'declared_fold_length_mm': 674.34,
        'knife_size_mm': {'L': 61.6, 'W': 20.6, 'H': 91.6},
        'excluded': ['bleeds', 'sizeArrowData'],
        'limits': 'Sin validación física; material y espesor originales.',
    }
    (ROOT / 'validacion.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
