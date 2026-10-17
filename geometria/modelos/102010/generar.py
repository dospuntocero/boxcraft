"""Modelo 102010: medidas iniciales y variación acotada de altura."""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ENGINE=ROOT.parents[1]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def read(n):return json.loads((ROOT/'muestras'/f'knife-{n:02}.json').read_text())['data']

def fit_height(engine):
    a,b=read(3),read(4)
    assert a['knifeSize']['L']==b['knifeSize']['L'] and a['knifeSize']['W']==b['knifeSize']['W']
    delta=b['knifeSize']['H']-a['knifeSize']['H']
    first,second=engine.flatten(engine.layer(a)),engine.flatten(engine.layer(b))
    if set(first)!=set(second):raise ValueError('Cambió la estructura con la altura')
    slopes={p:(second[p]-v)/delta for p,v in first.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
    return {'kind':'empirical-height-model','source_pair_mm':[a['knifeSize']['L'],a['knifeSize']['W']],'source_heights_mm':[a['knifeSize']['H'],b['knifeSize']['H']],'height_slopes':slopes,'excluded':['bleeds','sizeArrowData'],'fixed_manufacturing_size_mm':{'L':120.6,'W':60.6},'material':'Cartón blanco 350g','thickness_mm':.5}

def apply_height(layer,delta,model):
    result=copy.deepcopy(layer)
    for path,slope in model['height_slopes'].items():
        parts=path.lstrip('/').split('/');target=result
        for part in parts[:-1]:target=target[int(part)] if isinstance(target,list) else target[part]
        key=int(parts[-1]) if isinstance(target,list) else parts[-1]
        target[key]+=slope*delta
    return result

def validate(model,engine):
    source,target=read(6),read(7)
    predicted=apply_height(engine.layer(source),target['knifeSize']['H']-source['knifeSize']['H'],model)
    actual,flat=engine.flatten(engine.layer(target)),engine.flatten(predicted)
    errors=[];count=0
    for path,v in actual.items():
        if isinstance(v,(int,float)) and not isinstance(v,bool):
            count+=1
            if abs(v-flat[path])>1e-6:errors.append({'path':path,'expected':v,'predicted':flat[path]})
        elif v!=flat[path]:errors.append({'path':path,'expected':v,'predicted':flat[path]})
    return {'pass':not errors,'numeric_fields':count,'differences':errors,'training':['muestras/knife-03.json','muestras/knife-04.json'],'holdout':['muestras/knife-06.json','muestras/knife-07.json'],'holdout_dimensions_mm':[target['knifeSize'][a] for a in 'LWH'],'excluded':model['excluded'],'limit':'La regla de altura se comprobó en otra pareja L/W; su aplicación fuera de la altura inicial en la base es una transferencia empírica, no otra comprobación directa del servidor'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--height',type=float,default=161.1)
    args=parser.parse_args()
    if not math.isfinite(args.height) or not 161.1<=args.height<=190.5:raise SystemExit('Altura admitida: 161.1–190.5 mm')
    engine=module('geometry_engine',ENGINE/'ajustar-basico.py')
    model=fit_height(engine);report=validate(model,engine)
    (ROOT/'reglas-altura.json').write_text(json.dumps(model,indent=2))
    (ROOT/'validacion-generador.json').write_text(json.dumps(report,indent=2))
    if not report['pass']:raise SystemExit('La comprobación de altura falló')
    data=read(0);layer=apply_height(engine.layer(data),args.height-161.1,model)
    output={'model':'102010','source':'captured-base-with-empirical-height-rule','manufacturing_size_mm':{'L':120.6,'W':60.6,'H':args.height},'material':model['material'],'thickness_mm':.5,'layer':layer,'excluded':model['excluded'],'limits':'Largo y ancho fijos por indicación del usuario; no validado para fabricación'}
    (ROOT/'troquel-generado.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    renderer=module('svg_renderer',ENGINE/'modelo-parametrico.py')
    svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201','Modelo 102010').replace('stroke-width="1"','stroke-width="0.2"').replace('stroke-dasharray="6 3"','stroke-dasharray="2 1"')
    (ROOT/'troquel-generado.svg').write_text(svg)
    print('SVG y JSON generados: 120.6 × 60.6 ×',args.height,'mm; comprobación de altura:',report['numeric_fields'],'campos')

if __name__=='__main__':main()
