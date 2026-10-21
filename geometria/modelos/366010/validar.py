#!/usr/bin/env python3
"""Valida el troquel 366010 contra la respuesta original y el SVG generado."""
import hashlib
import json
import math
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
BASE = json.loads((ROOT / 'base' / 'knife-00.json').read_text())['data']
GEN = json.loads((ROOT / 'troquel-generado.json').read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(finite(v) for v in value.values())
    if isinstance(value, list):
        return all(finite(v) for v in value)
    return True


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


checks = []


def check(ident, description, ok, detail=''):
    checks.append({'id': ident, 'descripcion': description,
                   'ok': bool(ok), 'detalle': detail})


# 1. Estructura y conteos por capa.
expected = {
    'fondo-gris': ('BoutiqueboxDivideEquallyCoverBottomGreyboard', 5, 22, 4, 0, 0),
    'fondo-papel': ('BoutiqueboxDivideEquallyCoverBottomFacepaper', 25, 86, 24, 0, 38),
    'tapa-gris': ('BoutiqueboxDivideEquallyCoverTopGreyboard', 5, 22, 4, 0, 0),
    'tapa-papel': ('BoutiqueboxDivideEquallyCoverTopFacepaper', 25, 86, 24, 0, 38),
}
counts_ok = True
for piece in GEN['piezas']:
    source = BASE['layer'][piece['capa']]
    counts = (len(source['faces']), len(source['cuts']), len(source['folds']),
              len(source.get('holes') or []), len(source.get('bleeds') or []))
    want = expected[piece['id']][1:]
    if counts != want:
        counts_ok = False
check('conteos_por_pieza', 'Cada pieza conserva caras, cortes, pliegues, orificios y sangrados.',
      counts_ok, '; '.join(f"{p['id']}={tuple(p['conteos'][k] for k in ('caras','cortes','pliegues','orificios','sangrados'))}" for p in GEN['piezas']))

check('total_general', 'La lámina compuesta suma las cuatro piezas.',
      GEN['conteos'] == {'piezas': 4, 'caras': 60, 'pliegues': 56, 'cortes': 216,
                         'sangrados': 76, 'orificios': 0},
      json.dumps(GEN['conteos']))

# 2. Traslación exacta de cada pieza.
translation_ok = True
max_error = 0.0


def compare_point(original, generated, dx, dy):
    global max_error, translation_ok
    if 'x' in original:
        max_error = max(max_error, abs((original['x'] + dx) - generated['x']))
    if 'y' in original:
        max_error = max(max_error, abs((original['y'] + dy) - generated['y']))
    if original.get('mtd') != generated.get('mtd'):
        translation_ok = False


for piece in GEN['piezas']:
    source = BASE['layer'][piece['capa']]
    layer = piece['geometria']
    dx, dy = piece['offset_mm']['x'], piece['offset_mm']['y']
    if len(source['faces']) != len(layer['faces']):
        translation_ok = False
        continue
    for original, generated in zip(source['faces'], layer['faces']):
        if generated['name'] != f"{piece['prefix']}_{original['name']}":
            translation_ok = False
        if not (close(original['w'], generated['w']) and close(original['h'], generated['h'])):
            translation_ok = False
        if not (close(original['x'] + dx, generated['x']) and close(original['y'] + dy, generated['y'])):
            translation_ok = False
        if len(original['dlist']) != len(generated['dlist']):
            translation_ok = False
            continue
        for a, b in zip(original['dlist'], generated['dlist']):
            compare_point(a, b, dx, dy)
    for original, generated in zip(source['cuts'], layer['cuts']):
        compare_point(original, generated, dx, dy)
    for original, generated in zip(source['bleeds'], layer['bleeds']):
        compare_point(original, generated, dx, dy)
    for original, generated in zip(source['folds'], layer['folds']):
        for key, delta in (('x1', dx), ('x2', dx), ('y1', dy), ('y2', dy)):
            if key in original:
                max_error = max(max_error, abs(original[key] + delta - generated[key]))
        if generated['name'] != f"{piece['prefix']}_{original['name']}":
            translation_ok = False

check('traslacion_exacta', 'Todas las coordenadas son la respuesta original más un desplazamiento.',
      translation_ok and max_error <= 1e-9, f'error máximo {max_error:.3e} mm')

# 3. Nombres únicos y geometría finita.
names = [f['name'] for f in GEN['compuesto']['faces']] + [f['name'] for f in GEN['compuesto']['folds']]
check('nombres_unicos', 'Los nombres de caras y pliegues son únicos tras el prefijo.',
      len(names) == len(set(names)), f'{len(names)} nombres')

check('valores_finitos', 'No hay NaN ni infinitos en la geometría.',
      finite(GEN['compuesto']) and finite(GEN['piezas']))

# 4. Extensiones y no solapamiento.
extents_ok = (GEN['extension_mm']['x'] > 0 and GEN['extension_mm']['y'] > 0 and
              close(GEN['compuesto']['totalX'], GEN['extension_mm']['x']) and
              close(GEN['compuesto']['totalY'], GEN['extension_mm']['y']))
check('extension_positiva', 'La extensión compuesta es positiva y coincide con totalX/totalY.',
      extents_ok, f"{GEN['extension_mm']['x']} × {GEN['extension_mm']['y']} mm")

rects = [(p['id'], p['offset_mm']['x'], p['offset_mm']['y'],
          p['offset_mm']['x'] + p['extension_mm']['x'],
          p['offset_mm']['y'] + p['extension_mm']['y']) for p in GEN['piezas']]
overlaps = []
for i, a in enumerate(rects):
    for b in rects[i + 1:]:
        if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
            overlaps.append((a[0], b[0]))
check('sin_solapamiento', 'Las cuatro piezas no se solapan en la lámina.',
      not overlaps, 'sin solapes' if not overlaps else str(overlaps))

# 5. Comandos de trazado y SVG.
allowed = {'M', 'L', 'A', 'Z'}
commands = [c['mtd'] for c in GEN['compuesto']['cuts'] + GEN['compuesto']['bleeds']]
for face in GEN['compuesto']['faces']:
    commands += [c['mtd'] for c in face['dlist']]
    for hole in face.get('holes') or []:
        commands += [c['mtd'] for c in hole]
check('comandos_admitidos', 'Solo se usan M, L, A y Z.',
      set(commands) <= allowed, str(sorted(set(commands))))

svg_path = ROOT / 'troquel-generado.svg'
try:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    svg_ok = True
    detail = root.tag
except Exception as exc:  # pragma: no cover
    svg_ok = False
    detail = str(exc)
check('svg_xml', 'El SVG es XML válido.', svg_ok, detail)

svg_text = svg_path.read_text()
check('svg_sin_nan', 'El SVG no contiene NaN ni Infinity.', 'NaN' not in svg_text and 'Infinity' not in svg_text)
check('svg_cuatro_etiquetas', 'El SVG incluye una etiqueta por pieza.',
      svg_text.count('-etiqueta') == 4, f"{svg_text.count('-etiqueta')} etiquetas")

exported_path = ROOT / 'exportado-editor.svg'
if exported_path.exists():
    exported_text = exported_path.read_text()
    try:
        ET.parse(exported_path)
        exported_ok = True
        exported_detail = 'XML válido'
    except Exception as exc:
        exported_ok = False
        exported_detail = str(exc)
    check('exportado_editor', 'El SVG exportado por el editor es XML válido y conserva corte, sangrado y etiquetas.',
          exported_ok and 'id="corte"' in exported_text and 'id="sangrado"' in exported_text
          and exported_text.count('<text') == 4,
          exported_detail)

# 6. Metadatos de la respuesta original.
check('material_original', 'Se conserva el material de papel y el espesor del cartón.',
      GEN['material']['id'] == 48 and close(GEN['espesor_papel_mm'], 0.15) and close(GEN['espesor_carton_mm'], 2.0),
      f"science={GEN['material']['id']}, papel={GEN['espesor_papel_mm']}, cartón={GEN['espesor_carton_mm']}")

cdp_path = ROOT / 'muestras' / 'base-cdp.json'
if cdp_path.exists():
    cdp = json.loads(cdp_path.read_text())['data']
    check('base_independiente', 'La respuesta base coincide capa por capa con una captura CDP independiente.',
          cdp['layer'] == BASE['layer'] and cdp['knifeSize'] == BASE['knifeSize']
          and cdp['science'] == BASE['science'],
          f"{len(cdp['layer'])} capas")

bleed_path = GEN['compuesto'].get('bleedPath', '')
bleed_points = [(float(x), float(y)) for x, y in
                re.findall(r'[ML](-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)', bleed_path)]
if bleed_points:
    bxs = [p[0] for p in bleed_points]
    bys = [p[1] for p in bleed_points]
    bleed_ok = (bleed_path.count('M') == 2
                and min(bxs) > 280
                and max(bxs) <= GEN['extension_mm']['x'] + 3 + 1e-6
                and abs(min(bys) + 3) <= 1e-6
                and abs(max(bys) - (GEN['extension_mm']['y'] + 3)) <= 1e-6)
    bleed_detail = (f"{len(bleed_points)} puntos, 2 subperfiles, "
                    f"x={min(bxs):.2f}..{max(bxs):.2f}, y={min(bys):.2f}..{max(bys):.2f}")
else:
    bleed_ok = False
    bleed_detail = 'sin trazado'
check('sangrado_calculado', 'El sangrado dibujado es un contorno de 3 mm solo para las piezas de papel.',
      bleed_ok, bleed_detail)

check('dimensiones', 'Las dimensiones de manufactura son 180 × 100 × 40 mm.',
      GEN['dimensiones_manufactura_mm'] == {'L': 180, 'W': 100, 'H': 40},
      json.dumps(GEN['dimensiones_manufactura_mm']))
check('exteriores', 'Las dimensiones exteriores coinciden con la respuesta.',
      all(close(GEN['dimensiones_exteriores_mm'][k], BASE['outSize'][k]) for k in 'LWH'),
      json.dumps(GEN['dimensiones_exteriores_mm']))

ok = all(c['ok'] for c in checks)
validation = {
    'modelo': '366010',
    'fecha': '2026-10-20',
    'configuracion': GEN['dimensiones_manufactura_mm'],
    'material': GEN['material'],
    'extension_mm': GEN['extension_mm'],
    'conteos': GEN['conteos'],
    'comprobaciones': checks,
    'resultado': 'ok' if ok else 'falla',
    'sha256': {
        'base/knife-00.json': sha(ROOT / 'base' / 'knife-00.json'),
        'base/geometria.json': sha(ROOT / 'base' / 'geometria.json'),
        'base/bleed-path.txt': sha(ROOT / 'base' / 'bleed-path.txt'),
        'troquel-generado.svg': sha(ROOT / 'troquel-generado.svg'),
        'troquel-generado.json': sha(ROOT / 'troquel-generado.json'),
        'vista-previa.png': sha(ROOT / 'vista-previa.png'),
        'icono-3d.jpg': sha(ROOT / 'icono-3d.jpg'),
        'exportado-editor.svg': sha(ROOT / 'exportado-editor.svg'),
        'exportado-editor-210x120x50.svg': sha(ROOT / 'exportado-editor-210x120x50.svg'),
        'exportado-editor-210x120x50-T2.5.svg': sha(ROOT / 'exportado-editor-210x120x50-T2.5.svg'),
        'captura-espesor.png': sha(ROOT / 'captura-espesor.png'),
        'captura-editor.png': sha(ROOT / 'captura-editor.png'),
        'reglas.json': sha(ROOT / 'reglas.json'),
        'validacion-parametrica.json': sha(ROOT / 'validacion-parametrica.json'),
        'parametricas/manifest.json': sha(ROOT / 'parametricas' / 'manifest.json'),
        'espesor/manifest.json': sha(ROOT / 'espesor' / 'manifest.json'),
        'bleed-node.cjs': sha(ROOT / 'bleed-node.cjs'),
    },
    'limites': [
        'No se reconstruyó un motor paramétrico: las muestras mostraron interacción no aditiva.',
        'No se validó armado físico ni tolerancias de fabricación.',
        'No se descargaron AI/PDF/DXF originales; la descarga de Pacdora exige autenticación.',
        'La vista previa es una rasterización local del SVG, no una imagen oficial.',
    ],
    'verificacion_editor': {
        'navegador': 'Chromium 155 sin interfaz, servidor local 8111',
        'seleccion': '366010',
        'motor': 'rigid366010',
        'rango': {'L': [160, 220], 'W': [80, 140], 'H': [30, 70]},
        'edicion_probada': {'L': 210, 'W': 120, 'H': 50, 'T': 2.5},
        'rango_espesor_mm': [1.5, 2.5],
        'espesores_verificados_mm': [1.5, 1.75, 2.0, 2.25, 2.5],
        'conteos': {'caras': 60, 'pliegues': 56, 'aberturas': 0},
        'sangrado': '2 subperfiles, solo piezas de papel',
        'archivo': 'exportado-editor.svg',
        'archivo_espesor': 'exportado-editor-210x120x50-T2.5.svg',
        'descarga': 'troquel-366010-180x100x40mm.svg',
        'descarga_espesor': 'troquel-366010-210x120x50-T2.5mm.svg',
        'error_parametrico_mm': (json.loads((ROOT / 'validacion-parametrica.json').read_text())['error_max_mm']
                                  if (ROOT / 'validacion-parametrica.json').exists() else None),
    },
}
previous_path = ROOT / 'validacion.json'
if previous_path.exists():
    try:
        previous = json.loads(previous_path.read_text())
        if 'integracion' in previous:
            validation['integracion'] = previous['integracion']
    except Exception:
        pass
(ROOT / 'validacion.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
print(('OK' if ok else 'FALLA'), len(checks), 'comprobaciones')
for c in checks:
    if not c['ok']:
        print(' -', c['id'], c['detalle'])
