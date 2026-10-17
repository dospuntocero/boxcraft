"""Reproduce el modelo 112310 con las medidas iniciales capturadas."""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'base'/'knife-00.json').read_text())['data']
    layer={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}
    output={'model':'112310','source':'captured-public-template','source_evidence_id':'ev_a908ce42df7992776ec9aa9f023d02b40ed588be86d11b3e40489dbabec3274f','manufacturing_size_mm':{k:data['knifeSize'][k] for k in 'LWH'},'material':data['science']['name'],'thickness_mm':layer['thickness'],'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Medidas iniciales fijas; no validado para fabricación'}
    (ROOT/'troquel-generado.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    spec=importlib.util.spec_from_file_location('svg_renderer',ROOT.parents[1]/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Modelo 112310').replace('stroke-width="1"','stroke-width="0.3"').replace('stroke-dasharray="6 3"','stroke-dasharray="3 2"')
    (ROOT/'troquel-generado.svg').write_text(svg)
    print('112310: 302 × 152 × 182 mm; 16 caras, 15 pliegues y 3 aberturas')

if __name__=='__main__':main()
