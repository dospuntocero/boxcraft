"""Reconstrucción empírica del modelo 10001029, con parámetros básicos."""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TRAIN=[('muestras','knife-00.json'),('muestras','knife-02.json'),('muestras','knife-04.json'),('muestras','knife-06.json'),('ajustes','knife-02.json'),('ajustes','knife-04.json'),('ajustes','knife-05.json'),('ajustes','knife-06.json')]
BASE=[60,45,120,6,29,7]
SCALE=[16.2,18.5,32.4,2,5,2]

def read(path):return json.loads(path.read_text())['data']
def params(data):return {p['name']:p['value'] for group in data['openParams'] for p in group}
def features(dim,p):return [1]+[(v-b)/s for v,b,s in zip([*dim,p['E'],p['A'],p['AR']],BASE,SCALE)]
def numeric(v):return isinstance(v,(int,float)) and not isinstance(v,bool)
def flatten(obj,path=''):
    result={}
    if isinstance(obj,dict):
        for k,v in obj.items():result.update(flatten(v,path+'/'+k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):result.update(flatten(v,path+'/'+str(i)))
    else:result[path]=obj
    return result

def supported_layer(layer):
    result=copy.deepcopy(layer)
    result.pop('bleeds',None)
    result.pop('sizeArrowData',None)
    return result

def solve(matrix,values):
    rows=[r[:]+[v] for r,v in zip(matrix,values)]
    n=len(values)
    for col in range(n):
        pivot=max(range(col,n),key=lambda i:abs(rows[i][col]))
        if abs(rows[pivot][col])<1e-10:raise ValueError('Muestras insuficientes para separar las variables')
        rows[col],rows[pivot]=rows[pivot],rows[col]
        divisor=rows[col][col];rows[col]=[v/divisor for v in rows[col]]
        for i in range(n):
            if i!=col:
                factor=rows[i][col];rows[i]=[v-factor*w for v,w in zip(rows[i],rows[col])]
    return [row[-1] for row in rows]

def fit():
    samples=[read(ROOT/sub/name) for sub,name in TRAIN]
    rows=[features([k['knifeSize'][a] for a in 'LWH'],params(k)) for k in samples]
    flat=[flatten(supported_layer(k['layer']['traditional'])) for k in samples]
    if any(set(f)!=set(flat[0]) for f in flat):raise ValueError('Cambió la estructura geométrica')
    normal=[[sum(r[i]*r[j] for r in rows) for j in range(7)] for i in range(7)]
    rules={}
    for path,value in flat[0].items():
        if numeric(value):
            rhs=[sum(row[i]*f[path] for row,f in zip(rows,flat)) for i in range(7)]
            rules[path]=solve(normal,rhs)
        elif any(f[path]!=value for f in flat) and '/sizeArrowData/' not in path:
            raise ValueError('Campo no numérico cambió: '+path)
    model={'kind':'empirical-feature-model','variables':['1','L','W','H','E','A','AR'],'base':BASE,'scale':SCALE,'template':supported_layer(samples[0]['layer']['traditional']),'rules':rules,'training':[str(Path(s)/n) for s,n in TRAIN],'excluded':['bleeds','sizeArrowData']}
    (ROOT/'reglas.json').write_text(json.dumps(model,indent=2))
    return model

def reconstruct(model,dimensions,p):
    result=copy.deepcopy(model['template']);vector=features(dimensions,p)
    for path,coefficients in model['rules'].items():
        parts=path.lstrip('/').split('/');target=result
        for part in parts[:-1]:target=target[int(part)] if isinstance(target,list) else target[part]
        key=int(parts[-1]) if isinstance(target,list) else parts[-1]
        target[key]=sum(c*v for c,v in zip(coefficients,vector))
    return result

def differences(actual,predicted):
    a,b=flatten(actual),flatten(predicted);errors=[];count=0
    if set(a)!=set(b):return [{'path':'/','kind':'structure'}],0
    for path,value in a.items():
        if numeric(value):
            count+=1;delta=abs(value-b[path]);tol=.001 if path.startswith('/bleeds/') else .000001
            if delta>tol:errors.append({'path':path,'expected':value,'predicted':b[path],'delta':delta})
        elif value!=b[path] and not path.startswith('/sizeArrowData/'):
            errors.append({'path':path,'expected':value,'predicted':b[path]})
    return errors,count

def defaults(L,W,H):
    # Solo rama constante E=8,S=6 contrastada en el rango admitido.
    return {'E':8,'S':6,'A':math.floor(min(L/2,W*.65)+1e-9),'AR':max(7,math.floor(W*.15+1e-9)),'G':13,'C':13,'CR':7,'R':.65,'OF':.5,'GT':15}

def validate(model):
    reports=[]
    for filename in ['knife-02.json','knife-03.json','knife-04.json']:
        actual=read(ROOT/'validacion'/filename);dims=[actual['knifeSize'][a] for a in 'LWH'];p=defaults(*dims)
        errors,count=differences(supported_layer(actual['layer']['traditional']),reconstruct(model,dims,p))
        mismatch={key:{'predicted':value,'actual':params(actual).get(key)} for key,value in p.items() if value!=params(actual).get(key)}
        reports.append({'file':filename,'dimensions_mm':dims,'numeric_fields':count,'differences':errors,'default_parameter_mismatch':mismatch,'pass':not errors and not mismatch})
    report={'pass':all(r['pass'] for r in reports),'holdouts':reports,'excluded_comparison':['bleeds','sizeArrowData'],'bleed_fit_previous_max_error_mm':0.004582290321422988,'limits':'Sangría y anotaciones excluidas de comparación y salida; comparación con servidor, no fabricación'}
    (ROOT/'validacion-generador.json').write_text(json.dumps(report,indent=2))
    return report

def generate(model,L,W,H):
    for name,value,(low,high) in zip('LWH',[L,W,H],[(68.58,76.2),(45,63.5),(120,152.4)]):
        if not math.isfinite(value) or not low<=value<=high:raise ValueError(f'{name}: admite {low}–{high} mm')
    p=defaults(L,W,H);layer=reconstruct(model,[L,W,H],p)
    return {'model':'10001029','source':'local-empirical-model','manufacturing_size_mm':{'L':L,'W':W,'H':H},'material':'Cartón blanco 350g','thickness_mm':.5,'automatic_defaults':p,'layer':layer,'excluded':['bleeds','sizeArrowData'],'limits':'Rango limitado; fórmulas inferidas; no validado para fabricación'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--length',type=float,default=68.58);parser.add_argument('--width',type=float,default=53.34);parser.add_argument('--height',type=float,default=139.7)
    args=parser.parse_args();model=fit();report=validate(model)
    for r in report['holdouts']:print(r['file'],'PASS' if r['pass'] else 'FAIL',r['numeric_fields'],'campos',len(r['differences']),'diferencias')
    if not report['pass']:raise SystemExit('Validación falló; no se generó un SVG')
    data=generate(model,args.length,args.width,args.height)
    (ROOT/'troquel-generado.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
    spec=importlib.util.spec_from_file_location('svg_engine',ROOT.parents[1]/'modelo-parametrico.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    svg=module.render_svg(data['layer']).replace('Modelo empírico FEFCO 0201','Modelo empírico 10001029').replace('stroke-width="1"','stroke-width="0.2"').replace('stroke-dasharray="6 3"','stroke-dasharray="2 1"')
    (ROOT/'troquel-generado.svg').write_text(svg)
