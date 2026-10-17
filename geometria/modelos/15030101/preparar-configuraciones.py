"""Indexa respuestas completas por medidas, material y espesor efectivos."""
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE_EVIDENCE='ev_89ba7b7dfd2c598f54c4d2f5658241fffcecfaef8870723ea2044b409341aae2'
def main():
    cases={}
    def add(path,evidence,cleanup):
        raw=path.read_bytes();d=json.loads(raw)['data'];layer=d['layer']['traditional'];assert str(d['cate_no'])=='15030101'
        dims={a:d['knifeSize'][a] for a in 'LWH'};material=layer.get('science_id',d['science']['id']);t=layer['thickness']
        assert d['science']['id']==material
        assert float(d['science']['min_thickness'])-1e-8<=t<=float(d['science']['max_thickness'])+1e-8
        def finite(x):
            if isinstance(x,dict):return all(finite(v) for v in x.values())
            if isinstance(x,list):return all(finite(v) for v in x)
            return math.isfinite(x) if isinstance(x,(int,float)) else True
        assert finite(layer) and layer['totalX']>0 and layer['totalY']>0
        key=tuple(dims.values())+(material,t)
        cases[key]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'evidence_id':evidence,'cleanup':cleanup,'dims':dims,'materialId':material,'materialName':d['science']['name'],'thickness':t,'extent':[layer['totalX'],layer['totalY']],'offsets':{mode:{a:d[field][a]-dims[a] for a in dims} for mode,field in [('inner','size'),('outer','outSize')]}}
    add(ROOT/'base/knife-00.json',BASE_EVIDENCE,'terminated-owned-process')
    for folder in ['parametricas','materiales','personalizados','independiente']:
        manifest=json.loads((ROOT/folder/'manifest.json').read_text())
        for sample in manifest['samples']:
            path=ROOT/folder/sample['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==sample['sha256'];add(path,manifest['evidence_id'],manifest['cleanup'])
    data={'model':'15030101','unit':'mm','interpolation':False,'cases':list(cases.values())}
    (ROOT/'configuraciones.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    return data
if __name__=='__main__':
    data=main();print('Configuraciones exactas:',len(data['cases']))
