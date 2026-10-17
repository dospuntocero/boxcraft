"""Ajuste por eje y contraste independiente; nunca habilita un ajuste fallido."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=[1,2,4,6,7,8]
def audit():
    data=[json.loads((ROOT/f'parametricas/knife-{i:02}.json').read_text())['data'] for i in FILES]
    layers=[d['layer']['traditional'] for d in data]; differences=[]; count=0;rules={}
    def walk(values,path=''):
        nonlocal count
        first=values[0]
        if isinstance(first,dict):
            if any(set(v)!=set(first) for v in values):differences.append({'path':path,'kind':'keys'});return
            for k in first:
                if k not in ['bleeds','sizeArrowData']:walk([v[k] for v in values],path+'/'+k)
        elif isinstance(first,list):
            if any(len(v)!=len(first) for v in values):differences.append({'path':path,'kind':'length'});return
            for i in range(len(first)):walk([v[i] for v in values],path+'/'+str(i))
        elif isinstance(first,(int,float)) and not isinstance(first,bool):
            count+=1; slopes=[(v-first)/10 for v in values[1:4]]
            if any(abs(s)>1e-12 for s in slopes):rules[path]={'base':first,'slopes_LWH':slopes}
            for n,target in enumerate(values[4:]):
                delta=[data[n+4]['knifeSize'][a]-data[0]['knifeSize'][a] for a in 'LWH'];predicted=first+sum(s*d for s,d in zip(slopes,delta));error=abs(target-predicted)
                if error>1e-6:differences.append({'path':path,'sample':FILES[n+4],'kind':'numeric','error_mm_or_units':error})
        elif any(v!=first for v in values):differences.append({'path':path,'kind':'literal'})
    walk(layers)
    report={'method':'affine fit from independent L/W/H variations','training':[f'knife-{i:02}.json' for i in FILES[:4]],'validation':[f'knife-{i:02}.json' for i in FILES[4:]],'numeric_fields_per_sample':count,'tolerance':1e-6,'pass':not differences,'max_error_mm_or_units':max([x.get('error_mm_or_units',0) for x in differences],default=0),'differences':differences,'enabled':False,'decision':'Rejected; keep exact captured configurations' if differences else 'Candidate requires additional verification','evidence_id':'ev_44cda8270657702f72a0085860e251ed8c058492bca976ff675ebcd529971e56'}
    (ROOT/'validacion-parametrizacion.json').write_text(json.dumps(report,indent=2));return report
if __name__=='__main__':
    r=audit();print({k:v for k,v in r.items() if k!='differences'})
