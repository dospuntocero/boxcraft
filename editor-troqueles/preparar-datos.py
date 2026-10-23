import json, pathlib, importlib.util
ROOT=pathlib.Path(__file__).resolve().parent
G=ROOT.parent/'geometria'
OUT=ROOT/'dist'/'assets'
OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('renderer',G/'modelo-parametrico.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
entries=[('200010','Caja de envío FEFCO','Envío',G/'knife.json','affine'),('102010','Caja con fondo encajable','Plegables',G/'modelos/102010/muestras/knife-00.json','height'),('150010','Caja mailer con tapa','Envío',G/'modelos/150010/base-publica/knife-00.json',None),('112047','Caja con techo y cordón','Con asa',G/'modelos/112047/base/knife-00.json',None),('12109002','Caja para pastel','Con asa',G/'modelos/12109002/base/knife-00.json',None),('112310','Caja con asa y fondo','Con asa',G/'modelos/112310/base/knife-00.json',None),('10001006','Estuche con solapas','Plegables',G/'modelos/10001006/base/knife-00.json',None),('10002003','Estuche para colgar','Plegables',G/'modelos/10002003/base/knife-00.json',None),('180370','Envase para papas fritas','Alimentos',G/'modelos/180370/base/knife-00.json',None),('180320','Caja sándwich con ventana','Alimentos',G/'modelos/180320/base/knife-00.json',None)]
result=[]
for code,name,category,path,engine in entries:
 k=json.loads(path.read_text())['data'];layer={key:v for key,v in k['layer']['traditional'].items() if key not in ['bleeds','sizeArrowData']};dims={a:k['knifeSize'][a] for a in ('LW' if code=='180320' else 'LWH')}
 model={'id':code,'name':name,'category':category,'dims':dims,'material':k['science']['name'].split(' (')[0],'thickness':layer['thickness'],'layer':layer,'engine':engine,'offsets':{typ:{a:k[key][a]-dims[a] for a in dims} for typ,key in [('internal','size'),('external','outSize')]},'bounds':{},'rule':None}
 if engine=='affine':
  rule=json.loads((G/'reglas-parametricas.json').read_text());model['rule']={'base':rule['base_mm'],'rules':{p:v for p,v in rule['rules'].items() if not p.startswith(('/bleeds/','/sizeArrowData/'))}};model['bounds']=dict(zip('LWH',rule['bounds_mm']))
 elif engine=='height':
  rule=json.loads((G/'modelos/102010/reglas-altura.json').read_text());model['rule']={'slopes':rule['height_slopes'],'baseH':161.1};model['bounds']={'H':[161.1,190.5]}
 # Keep geometry and parameter coefficients only; no captured network or project data.
 svg=renderer.render_svg(layer).replace('Modelo empírico FEFCO 0201',name).replace('stroke-width="1"','stroke-width="0.5"')
 (OUT/f'{code}.svg').write_text(svg)
 if engine:
  model['verifiedBounds']=model['bounds'].copy()
  model['expandedBounds']={axis:[round(v*.5,3),round(v*2,3)] for axis,v in dims.items() if axis in model['bounds']}
 result.append(model)
(OUT/'modelos.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')))
print(len(result),'modelos; assets',sum(p.stat().st_size for p in OUT.iterdir()),'bytes')

# Reapply the reconstructed generators after refreshing the original assets.
import runpy
runpy.run_path(str(ROOT/"parametrizar-modelos.py"),run_name="__main__")
runpy.run_path(str(ROOT/"incorporar-modelos-adquiridos.py"),run_name="__main__")
runpy.run_path(str(ROOT/"incorporar-materiales-187000.py"),run_name="__main__")
# Aplica el estado derivado de las validaciones después de todas las altas.
import sys
sys.argv=[sys.argv[0]]+(["--check"] if "--check" in sys.argv else [])
runpy.run_path(str(ROOT/"aplicar-estados.py"),run_name="__main__")
