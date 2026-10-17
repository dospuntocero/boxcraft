"""Reproduce la configuración base exacta; no escala ni interpola dimensiones."""
import hashlib, importlib.util, json, math, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
EVIDENCE='ev_89ba7b7dfd2c598f54c4d2f5658241fffcecfaef8870723ea2044b409341aae2'
def main(configuration=None, output_dir=None):
    destination=Path(output_dir) if output_dir else ROOT
    destination.mkdir(parents=True,exist_ok=True)
    source=ROOT/configuration['path'] if configuration else ROOT/'base/knife-00.json'
    evidence=configuration['evidence_id'] if configuration else EVIDENCE
    if configuration:assert hashlib.sha256(source.read_bytes()).hexdigest()==configuration['sha256']
    data=json.loads(source.read_text())['data']
    assert str(data['cate_no'])=='15030101'
    layer={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}
    dims={a:data['knifeSize'][a] for a in 'LWH'}
    output={'model':'15030101','source_evidence_id':evidence,'manufacturing_size_mm':dims,'material':data['science']['name'],'thickness_mm':layer['thickness'],'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Configuración exacta; no validado para fabricación'}
    (destination/'troquel-generado.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
    spec=importlib.util.spec_from_file_location('renderer',ROOT.parents[1]/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Caja para tarta 15030101').replace('stroke-width="1"','stroke-width="0.3"')
    (destination/'troquel-generado.svg').write_text(svg)
    import xml.etree.ElementTree as ET
    ET.fromstring(svg)
    def check(x):
        if isinstance(x,dict):return all(check(v) for v in x.values())
        if isinstance(x,list):return all(check(v) for v in x)
        return math.isfinite(x) if isinstance(x,(int,float)) else True
    assert check(layer) and layer['totalX']>0 and layer['totalY']>0
    counts={k:len(layer[k]) for k in ['faces','folds','cuts','holes']}
    report={'base_geometry_matches_original':layer=={k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']},'xml_valid':True,'finite':True,'counts':counts,'extent_mm':[layer['totalX'],layer['totalY']],'parameterization':'not enabled','physical_validation':False}
    (destination/'validacion.json').write_text(json.dumps(report,indent=2))
    manifest={'code':'15030101','url':'https://www.pacdora.com/es/dielines-detail/cake-box-dieline-15030101','date':'2026-10-17','evidence_id':EVIDENCE,'requested':dims,'effective':dims,'unit':'mm','material_id':data['science']['id'],'thickness_mm':layer['thickness'],'icon_url':'https://cdn.pacdora.com/render/1776047197934/14108280.png','sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'base/knife-00.json',ROOT/'base/details.json',ROOT/'icono.png']}}
    if configuration is None:(ROOT/'base/manifest.json').write_text(json.dumps(manifest,indent=2))
    return data,layer,dims
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--material-id',type=int,default=103)
    parser.add_argument('--thickness',type=float,default=.5)
    parser.add_argument('--length',type=float,default=150)
    parser.add_argument('--width',type=float,default=150)
    parser.add_argument('--height',type=float,default=50)
    parser.add_argument('--output-dir')
    args=parser.parse_args()
    dims=dict(zip('LWH',[args.length,args.width,args.height]))
    cases=json.loads((ROOT/'configuraciones.json').read_text())['cases']
    case=next((c for c in cases if c['dims']==dims and c['materialId']==args.material_id and abs(c['thickness']-args.thickness)<1e-8),None)
    if case is None:parser.error('No hay una captura exacta de estas medidas, material y espesor; consulta configuraciones.json.')
    main(case,args.output_dir)
