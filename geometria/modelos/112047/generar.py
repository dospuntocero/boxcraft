"""Reproduce el troquel 112047 con sus medidas iniciales capturadas."""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'base'/'knife-00.json').read_text())['data']
    layer={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}
    output={'model':'112047','source':'captured-public-template','source_evidence_id':'ev_4f668f2c1bdecad06f7412545afea068086c1ad9e77e5d01e76afba6a6b770c0','manufacturing_size_mm':{k:data['knifeSize'][k] for k in 'LWH'},'material':data['science']['name'],'thickness_mm':layer['thickness'],'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Medidas iniciales fijas; no validado para fabricación'}
    (ROOT/'troquel-generado.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    spec=importlib.util.spec_from_file_location('svg_renderer',ROOT.parents[1]/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Modelo 112047').replace('stroke-width="1"','stroke-width="0.2"').replace('stroke-dasharray="6 3"','stroke-dasharray="2 1"')
    (ROOT/'troquel-generado.svg').write_text(svg)
    print('112047: 70 × 50 × 60 mm; 19 caras, 18 pliegues y 4 orificios')

if __name__=='__main__':main()
