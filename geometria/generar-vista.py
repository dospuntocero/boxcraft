"""Renderiza la captura existente; no calcula ni inventa geometría nueva."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'knife.json').read_text())['data']
layer = data['layer']['traditional']

def path(commands):
    result = []
    for c in commands:
        op = c['mtd']
        if op in ('M', 'L'):
            result.append(f"{op}{c['x']} {c['y']}")
        elif op == 'A':
            result.append(f"A{c['rx']} {c['ry']} {c['ang']} {c['arc']} {c['dir']} {c['x']} {c['y']}")
        elif op == 'Z':
            result.append('Z')
        else:
            raise ValueError(f'Comando no soportado: {op}')
    return ' '.join(result)

faces = ''.join(f'<path d="{path(f["dlist"])}" fill="hsl({i*29%360} 65% 85%)" stroke="#cbd5e1"><title>{html.escape(f["name"])}</title></path>' for i,f in enumerate(layer['faces']))
labels = ''.join(f'<text x="{f["x"]+f["w"]/2}" y="{f["y"]+f["h"]/2}" text-anchor="middle" font-size="15" fill="#334155">{html.escape(f["name"])}</text>' for f in layer['faces'])
folds = ''.join(f'<line x1="{f["x1"]}" y1="{f["y1"]}" x2="{f["x2"]}" y2="{f["y2"]}"><title>{html.escape(f["name"])}</title></line>' for f in layer['folds'])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 1390 550" role="img" aria-label="Troquel FEFCO 0201 capturado de Pacdora">
<g id="faces">{faces}</g><g id="labels">{labels}</g>
<path id="cuts" d="{path(layer['cuts'])}" fill="none" stroke="#dc2626" stroke-width="1.5"/>
<g id="folds" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="7 4">{folds}</g></svg>'''
(ROOT / 'troquel-capturado.svg').write_text(svg)
rows=[]
for i,group in enumerate(layer['animation']['animations'],1):
    for a in group:
        rows.append(f'<tr><td>{i}</td><td>{html.escape(a["name"])}</td><td>{a["rotate"]}°</td><td>{html.escape(str(a["vector"]))}</td></tr>')
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Troquel capturado · FEFCO 0201</title>
<style>body{font:16px system-ui;color:#172033;background:#f4f6f9;margin:0;padding:32px}main{max-width:1350px;margin:auto}h1{font-size:28px}p{max-width:900px;line-height:1.6}.panel{background:white;border:1px solid #dbe2ea;border-radius:12px;padding:20px;margin:20px 0;overflow:auto}svg{width:100%;min-width:700px}label{display:inline-block;margin:6px 20px 6px 0}table{border-collapse:collapse;width:100%}td,th{text-align:left;border-bottom:1px solid #e2e8f0;padding:10px}small{color:#526174}</style><main>
<small>Inspección de geometría · Pacdora · Modelo 200010</small><h1>Troquel FEFCO 0201</h1>
<p>Vista de la respuesta capturada del servidor: 434 × 214 × 278 mm de manufactura, material Onda B de 3 mm. Los controles solo cambian la visibilidad; no recalculan dimensiones.</p>
<div class="panel"><label><input type="checkbox" data-layer="faces" checked> Caras</label><label><input type="checkbox" data-layer="labels" checked> Nombres</label><label><input type="checkbox" data-layer="cuts" checked> Corte rojo</label><label><input type="checkbox" data-layer="folds" checked> Pliegue azul</label>SVG_PLACEHOLDER</div>
<p>Se representan los comandos de arco como SVG A con sus campos originales. Es una interpretación del formato observado, pendiente de comparación visual con el editor. No se dibujó la sangría: su alineación requiere verificar las transformaciones. Este archivo sirve para análisis y no está validado para producción.</p>
<h2>Secuencia de plegado recibida</h2><p>Cada etapa agrupa rotaciones definidas por el servidor. La tabla conserva ángulos y vectores originales; no simula el plegado 3D.</p><div class="panel"><table><thead><tr><th>Etapa</th><th>Pliegue</th><th>Rotación</th><th>Vector</th></tr></thead><tbody>ROWS_PLACEHOLDER</tbody></table></div>
<small>Fuente: knife.json · Evidencia ev_77d8bd80d9fa88c43120d6cc5bd429c12c5968d9da9a0622cb273808367c498c</small></main>
<script>document.querySelectorAll('[data-layer]').forEach(el=>el.addEventListener('change',()=>{document.getElementById(el.dataset.layer).style.display=el.checked?'':'none'}))</script></html>'''
(ROOT / 'vista-troquel.html').write_text(page.replace('SVG_PLACEHOLDER',svg).replace('ROWS_PLACEHOLDER',''.join(rows)))
print(f"Generados SVG y HTML: {len(layer['faces'])} caras, {len(layer['folds'])} pliegues, {len(rows)} rotaciones")
