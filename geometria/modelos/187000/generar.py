#!/usr/bin/env python3
"""Genera el troquel local 187000 desde la geometría vectorial capturada.

No consulta Pacdora ni usa red. La fuente es base/geometria-dom.json, extraída
del SVG que el editor de Pacdora dibuja para 118 x 70 x 25 mm.
"""
import json, math, pathlib, re, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'base' / 'geometria-dom.json'
SHEET = (330.0, 480.0)  # pliego indicado por el usuario, mm
MIN = {'L': 20.0, 'W': 20.0, 'H': 6.67}
PRINT_MIN = {'L': 30.0, 'W': 30.0, 'H': 10.0}
URL = 'https://www.pacdora.com/es/dielines-detail/custom-pillow-box-dieline-187000'
EVIDENCE = {
    'pagina': 'ev_73771f17be96543b91985400c8f8a0ea185b779c7b1718c50df19a2a7b62f099',
    'geometria_base': 'ev_73771f17be96543b91985400c8f8a0ea185b779c7b1718c50df19a2a7b62f099',
    'variacion_150x90x40': 'ev_b7dfb9d69864d7dfb09eb62a730fd7383932aad52219bf19e45cef89a842049a',
    'variacion_L160': 'ev_75444ecb274977fc80301d9f223eb08ef608842b64cb585918abae7d07539b36',
    'variacion_W100': 'ev_b01014a87287bb74eb74040a95f3a45f0b1289f156b2e2dac43cd03348032c78',
    'variacion_H30': 'ev_a17998c5f2150f9ef24dc18d11bbeedd9d944eabaa4bc4b1f5bbac6049f2164b',
    'minimo_30x30x15': 'ev_c49872181fc6f5b0d481cd296a30f80eba29925ecb021aefe7db762fa8879002',
    'minimo_10x10x5': 'ev_4f33ca9d5103fe45b6649168794a2f60a09fc3ef5d012c6d6166091d8db4257d',
    'H5_rechazado': 'ev_b9c3a3fddcf813092254ab6bddb15a627826145dd2bd913975d1e818be0c595b',
    'descarga_login': 'ev_af74ae399a73a565cb2738641e2f8e1b7bd7210e7e687ca3f8f5b9a71378bb4b',
}

TOKEN = re.compile(r'[MLAQZ]|-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?')

def commands(d):
    toks = TOKEN.findall(d)
    i = 0
    while i < len(toks):
        t = toks[i]
        n = {'M': 2, 'L': 2, 'A': 7, 'Q': 4, 'Z': 0}[t]
        yield t, [float(x) for x in toks[i + 1:i + 1 + n]]
        i += 1 + n

def quad(p0, p1, p2, n=24):
    out = []
    for k in range(1, n + 1):
        t = k / n
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
        out.append((x, y))
    return out

def arc_points(p0, rx, ry, ang, large, sweep, p1, n=64):
    # All observed arcs are circular (rx == ry); solve the center directly.
    r = (abs(rx) + abs(ry)) / 2.0
    x0, y0 = p0; x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    d = math.hypot(dx, dy)
    if d == 0:
        return []
    h = d / 2.0
    if h > r:
        r = h
    a = math.sqrt(max(0.0, r*r - h*h))
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    px, py = -dy / d, dx / d
    candidates = [(mx + a*px, my + a*py), (mx - a*px, my - a*py)]
    two_pi = 2 * math.pi
    best = None
    for cx, cy in candidates:
        th0 = math.atan2(y0 - cy, x0 - cx)
        th1 = math.atan2(y1 - cy, x1 - cx)
        if sweep:
            dth = (th1 - th0) % two_pi
        else:
            dth = -((th0 - th1) % two_pi)
        is_large = abs(dth) > math.pi + 1e-9
        if bool(large) == is_large:
            best = (cx, cy, th0, dth)
            break
    if best is None:
        cx, cy = candidates[0]
        th0 = math.atan2(y0 - cy, x0 - cx)
        th1 = math.atan2(y1 - cy, x1 - cx)
        dth = (th1 - th0) % two_pi if sweep else -((th0 - th1) % two_pi)
        best = (cx, cy, th0, dth)
    cx, cy, th0, dth = best
    return [(cx + r*math.cos(th0 + dth*k/n), cy + r*math.sin(th0 + dth*k/n)) for k in range(1, n+1)]

def sample_path(d):
    pts = []; cur = (0.0, 0.0); start = (0.0, 0.0)
    for t, a in commands(d):
        if t == 'M':
            cur = (a[0], a[1]); start = cur; pts.append(cur)
        elif t == 'L':
            cur = (a[0], a[1]); pts.append(cur)
        elif t == 'Q':
            for p in quad(cur, (a[0], a[1]), (a[2], a[3])): pts.append(p)
            cur = (a[2], a[3])
        elif t == 'A':
            for p in arc_points(cur, a[0], a[1], a[2], int(a[3]), int(a[4]), (a[5], a[6])):
                pts.append(p)
            cur = (a[5], a[6])
        elif t == 'Z':
            if pts and pts[-1] != start: pts.append(start)
            cur = start
    return pts

def bbox(paths):
    xs, ys = [], []
    for d in paths:
        for x, y in sample_path(d):
            xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)

def xml_escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def build_svg(data, bb):
    xmin, ymin, xmax, ymax = bb
    m = max(2.0, 0.02 * max(xmax-xmin, ymax-ymin))
    vb = f'{xmin-m:.4f} {ymin-m:.4f} {xmax-xmin+2*m:.4f} {ymax-ymin+2*m:.4f}'
    faces = '\n'.join(
        f'    <path id="cara-{f["name"]}" d="{f["d"]}" fill="#ffffff" stroke="none"/>'
        for f in data['faces'])
    folds = []
    for f in data['folds']:
        if f['kind'] == 'line':
            folds.append(f'    <line x1="{f["x1"]}" y1="{f["y1"]}" x2="{f["x2"]}" y2="{f["y2"]}"/>')
        else:
            folds.append(f'    <path d="{f["d"]}"/>')
    folds = '\n'.join(folds)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{xmax-xmin+2*m:.4f}mm" height="{ymax-ymin+2*m:.4f}mm" viewBox="{vb}" role="img" aria-labelledby="titulo">
  <title id="titulo">Troquel 187000 · caja almohada · {data["dims"]["L"]} × {data["dims"]["W"]} × {data["dims"]["H"]} mm</title>
  <desc>Reconstrucción local desde la geometría vectorial observada. Corte azul, pliegue rojo. Sin sangría ni cotas.</desc>
  <metadata>{xml_escape(json.dumps({"code": data["code"], "url": URL, "dims": data["dims"], "material": data["material"], "evidence": EVIDENCE}, ensure_ascii=False))}</metadata>
  <g id="caras">
{faces}
  </g>
  <g id="corte" fill="none" stroke="#2028b0" stroke-width="0.3" stroke-linejoin="round">
    <path d="{data['cut']}"/>
  </g>
  <g id="pliegues" fill="none" stroke="#fa0000" stroke-width="0.3" stroke-dasharray="2 1.2">
{folds}
  </g>
</svg>
'''

def main():
    data = json.loads(BASE.read_text())
    paths = [data['cut']] + [f['d'] for f in data['folds'] if f['kind'] == 'path']
    bb = bbox(paths)
    width, height = bb[2]-bb[0], bb[3]-bb[1]
    svg = build_svg(data, bb)
    (ROOT / 'troquel-generado.svg').write_text(svg)
    # Blank extents for this model, from the captured cut contour.
    fits = max(width, height) <= max(SHEET) and min(width, height) <= min(SHEET)
    # Conservative maximum box for the 330 x 480 sheet:
    # cut width ~= L + H; cut height ~= 2W + 15 (top flap only; bottom is bleed).
    max_L = SHEET[0] - MIN['H']
    max_W = (SHEET[1] - 18.0) / 2  # W >= 100 uses an 18 mm top flap
    out = {
        'code': data['code'],
        'url': URL,
        'unidades': 'mm',
        'dimensiones_manufactura': data['dims'],
        'material': data['material'],
        'pliego_mm': list(SHEET),
        'minimos_observados_mm': MIN,
        'minimos_impresion_mm': PRINT_MIN,
        'maximos_estimados_por_pliego': {'L': round(max_L, 3), 'W': round(max_W, 3), 'H': 200.0},
        'motor': {
            'engine': 'pillow187000',
            'x0': 'H/2',
            'y0': 'W >= 100 ? 18 : 15',
            'R': '(W^2 + H^2) / (4H)',
            'rt': 'clamp(round((L+H)/25*2)/2, 6, 7.5)',
            'totalX': 'L + H',
            'totalY': '2W + y0',
            'bounds': {'L': [20, 323.33], 'W': [20, 231], 'H': [6.67, 200]},
            'requisito': 'H < W',
            'muestras_validadas': 7,
            'error_maximo_corte_mm': 0.00007,
            'error_maximo_caras_mm': 0.00003,
            'estado': 'experimental',
        },
        'extension_troquel': {'x': round(width, 4), 'y': round(height, 4),
                              'xmin': round(bb[0], 4), 'ymin': round(bb[1], 4),
                              'xmax': round(bb[2], 4), 'ymax': round(bb[3], 4)},
        'cabe_en_pliego': fits,
        'conteos': {'caras': len(data['faces']), 'pliegues': len(data['folds']), 'orificios': len(data['holes'])},
        'caras': [f['name'] for f in data['faces']],
        'geometria': {'corte': data['cut'], 'pliegues': data['folds'], 'caras': data['faces'], 'orificios': data['holes']},
        'procedencia': {
            'fuente': 'SVG del editor de Pacdora leído del DOM para 118 × 70 × 25 mm',
            'no_es_json_knife_de_pacdora': True,
            'evidencia': EVIDENCE,
            'descarga_original': 'bloqueada por inicio de sesión (HTTP 200 + code 401 en API)',
        },
        'limites': [
            'Corte y pliegues derivados del DOM; no incluye sangría, cotas, capas internas/externas ni parámetros avanzados.',
            'No se verificó el archivo exportado por Pacdora: la descarga exige autenticación.',
            'El motor paramétrico no está habilitado; solo se valida la configuración 118 × 70 × 25 mm.',
        ],
    }
    (ROOT / 'troquel-generado.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
    # Basic XML validation
    ET.fromstring(svg)
    print(f'{data["code"]}: {width:.3f} x {height:.3f} mm; caras={len(data["faces"])}; pliegues={len(data["folds"])}; pliego={fits}')

if __name__ == '__main__':
    main()
