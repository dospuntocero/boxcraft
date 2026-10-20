"""Alta reproducible de adquisiciones exactas; ejecutar tras preparar datos/materiales."""
import importlib.util,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'geometria/modelos/15030101'
def main():
    spec=importlib.util.spec_from_file_location('acquired',SOURCE/'generar.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    d,layer,dims=m.main();out=ROOT/'dist/assets'
    offsets={kind:{a:d[key][a]-dims[a] for a in dims} for kind,key in [('inner','size'),('outer','outSize')]}
    entry={'id':'15030101','name':'Caja para tarta con ventana','category':'Alimentos','dims':dims,'material':'Cartón blanco 350g','thickness':.5,'layer':layer,'engine':None,'minimumDims':{'L':40,'W':40,'H':30},'offsets':{'internal':offsets['inner'],'external':offsets['outer']},'bounds':{a:[v,v] for a,v in dims.items()},'rule':None,'previewImage':'assets/model-previews/15030101.png'}
    path=out/'modelos.json';models=json.loads(path.read_text());models=[x for x in models if x['id']!='15030101'];models.append(entry);path.write_text(json.dumps(models,ensure_ascii=False,separators=(',',':')))
    path=out/'capacidades-materiales.json';caps=json.loads(path.read_text());caps['15030101']={'originalMaterialId':103,'originalThickness':.5,'observedThicknessLimits':[.2,.5],'verifiedThicknessRange':[.5,.5],'onlyManufacturing':False,'offsets':offsets,'source':'geometria/modelos/15030101/base/knife-00.json','samples':[],'physicalProfiles':[],'geometryStatus':'exact-capture','blockedReason':'Solo configuración original verificada; alternativas pendientes.'};path.write_text(json.dumps(caps,ensure_ascii=False,indent=2))
    registry=json.loads((SOURCE/'configuraciones.json').read_text())
    profiles=[]
    for case in registry['cases']:
        if case['dims']!=dims or (case['materialId']==103 and case['thickness']==.5):continue
        raw=(SOURCE/case['path']).read_bytes()
        import hashlib
        assert hashlib.sha256(raw).hexdigest()==case['sha256']
        captured=json.loads(raw)['data']['layer']['traditional']
        profiles.append({'materialIds':[case['materialId']],'thickness':case['thickness'],'layer':{k:v for k,v in captured.items() if k not in ['bleeds','sizeArrowData']},'offsets':case['offsets'],'bounds':{a:[v,v] for a,v in dims.items()},'geometryStatus':'verified','evidence':{'configuration':dims,'path':'geometria/modelos/15030101/'+case['path'],'sha256':case['sha256'],'evidence_id':case['evidence_id']}})
    caps['15030101']['physicalProfiles']=profiles
    caps['15030101']['blockedReason']='No hay geometría verificada para este material y espesor.'
    caps['15030101']['samples']=[{'manufacturing':dims,'inner':d['size'],'outer':d['outSize']}]
    path.write_text(json.dumps(caps,ensure_ascii=False,indent=2))
    shutil.copyfile(SOURCE/'troquel-generado.svg',out/'15030101.svg');(out/'model-previews').mkdir(exist_ok=True);shutil.copyfile(SOURCE/'icono.png',out/'model-previews/15030101.png')
    # 187000: captura 2D exacta del troquel de caja almohada.
    spec2=importlib.util.spec_from_file_location('acquired187',ROOT.parent/'geometria/modelos/187000/integrar.py');m2=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(m2);m2.main()
if __name__=='__main__':main()
