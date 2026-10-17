"""Reproduce la plantilla pública 150010; no el proyecto privado 70845997."""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    source=ROOT/'base-publica'/'knife-00.json'
    data=json.loads(source.read_text())['data']
    layer={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}
    output={'model':'150010','source':'captured-public-template','source_evidence_id':'ev_d08c5f2a484622e0e1879ed095969a4b8e9aca75e8d3199b8ca638fc1ba95afe','requested_project_id':'70845997','requested_project_reproduced':False,'manufacturing_size_mm':{k:data['knifeSize'][k] for k in 'LWH'},'material':'Onda E','thickness_mm':1.5,'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Medidas iniciales públicas; ajustes del proyecto desconocidos; no validado para fabricación'}
    output['user_selected_public_template']=True
    (ROOT/'troquel-base-publica.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    spec=importlib.util.spec_from_file_location('svg_renderer',ROOT.parents[1]/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Plantilla pública 150010').replace('stroke-width="1"','stroke-width="0.3"').replace('stroke-dasharray="6 3"','stroke-dasharray="3 2"')
    (ROOT/'troquel-base-publica.svg').write_text(svg)
    print('Plantilla pública 150010: 315 × 202 × 62 mm; 19 caras, 22 pliegues y 4 ranuras')

if __name__=='__main__':main()
