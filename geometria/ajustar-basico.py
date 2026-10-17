"""Ajusta un modelo afín L/W/H y comprueba muestras no usadas en el ajuste."""
import argparse
import copy
import json
from pathlib import Path

def flatten(value,path=''):
    result={}
    if isinstance(value,dict):
        for k,v in value.items():result.update(flatten(v,path+'/'+k))
    elif isinstance(value,list):
        for i,v in enumerate(value):result.update(flatten(v,path+'/'+str(i)))
    else:result[path]=value
    return result

def layer(data):
    return {k:v for k,v in data['layer']['traditional'].items() if k not in ['bleeds','sizeArrowData']}

def fit(samples,cumulative=False):
    base=[samples[0]['knifeSize'][a] for a in 'LWH']
    previous=[samples[i] if cumulative else samples[0] for i in range(3)]
    deltas=[samples[i+1]['knifeSize'][a]-previous[i]['knifeSize'][a] for i,a in enumerate('LWH')]
    if not all(deltas):raise ValueError('Las muestras no varían los tres ejes')
    for i,s in enumerate(samples[1:]):
        if any(s['knifeSize'][a]!=previous[i]['knifeSize'][a] for j,a in enumerate('LWH') if i!=j):raise ValueError('Se requiere una variación por eje')
    flats=[flatten(layer(s)) for s in samples]
    if any(set(f)!=set(flats[0]) for f in flats):raise ValueError('Cambió la estructura del plano')
    rules={}
    for path,value in flats[0].items():
        if isinstance(value,(int,float)) and not isinstance(value,bool):
            rules[path]=[value,*[(flats[i+1][path]-(flats[i][path] if cumulative else value))/delta for i,delta in enumerate(deltas)]]
        elif any(f[path]!=value for f in flats):raise ValueError('Cambio no numérico: '+path)
    return {'base':base,'template':layer(samples[0]),'rules':rules,'bounds':[[min(b,b+d),max(b,b+d)] for b,d in zip(base,deltas)],'excluded':['bleeds','sizeArrowData']}

def generate(model,dimensions):
    result=copy.deepcopy(model['template'])
    for path,(intercept,*slopes) in model['rules'].items():
        parts=path.lstrip('/').split('/');target=result
        for p in parts[:-1]:target=target[int(p)] if isinstance(target,list) else target[p]
        key=int(parts[-1]) if isinstance(target,list) else parts[-1]
        target[key]=intercept+sum(s*(v-b) for s,v,b in zip(slopes,dimensions,model['base']))
    return result

def compare(model,data):
    dims=[data['knifeSize'][a] for a in 'LWH'];a=flatten(layer(data));b=flatten(generate(model,dims));errors=[];count=0
    if set(a)!=set(b):return {'pass':False,'reason':'structure','dimensions_mm':dims}
    for path,value in a.items():
        if isinstance(value,(int,float)) and not isinstance(value,bool):
            count+=1
            if abs(value-b[path])>1e-6:errors.append({'path':path,'actual':value,'predicted':b[path],'delta':abs(value-b[path])})
        elif value!=b[path]:errors.append({'path':path,'actual':value,'predicted':b[path]})
    return {'pass':not errors,'dimensions_mm':dims,'numeric_fields':count,'differences':errors}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);args=p.parse_args();root=args.directory
    read=lambda f:json.loads(f.read_text())['data']
    sources=[root/'muestras'/f'knife-{n:02}.json' for n in [0,2,4,6]]
    model=fit([read(f) for f in sources]);model['training']=[str(f.relative_to(root)) for f in sources]
    (root/'reglas.json').write_text(json.dumps(model,indent=2))
    reports=[dict(file=f.name,**compare(model,read(f))) for f in sorted((root/'validacion').glob('knife-*.json'))]
    result={'pass':all(r['pass'] for r in reports),'samples':reports,'excluded':model['excluded']}
    (root/'validacion-generador.json').write_text(json.dumps(result,indent=2))
    for r in reports:print(r['file'],r['pass'],r.get('numeric_fields'),len(r.get('differences',[])))
