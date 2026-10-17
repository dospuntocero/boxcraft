"""Reproduce el modelo 180320 con las medidas iniciales capturadas."""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'base'/'knife-00.json').read_text())['data']
    layer={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}
    output={'model':'180320','source':'captured-public-template','source_evidence_id':'ev_9e09f689ace42c23508869c90acd37b28df78921975b0730b2b74f72a35d73b1','manufacturing_size_mm':{k:data['knifeSize'][k] for k in 'LW'},'material':data['science']['name'],'thickness_mm':layer['thickness'],'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Medidas iniciales fijas; no validado para fabricación'}
    output['parameterization']='Dos medidas; H=0 auxiliar en la API, no altura física'
    (ROOT/'troquel-generado.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    spec=importlib.util.spec_from_file_location('svg_renderer',ROOT.parents[1]/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Modelo 180320').replace('stroke-width="1"','stroke-width="0.2"').replace('stroke-dasharray="6 3"','stroke-dasharray="2 1"')
    (ROOT/'troquel-generado.svg').write_text(svg)
    print('180320: 120 × 75 mm; 12 caras, 13 pliegues y 1 ventana')

if __name__=='__main__':main()
