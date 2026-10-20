import json
from pathlib import Path
root=Path(__file__).resolve().parent
models={m['id']:m for m in json.load(open(root.parents[1]/'editor-troqueles/dist/assets/modelos.json'))}
slugs={'150010':('custom-dimensions-flip-top-boxes-mailer-dieline-150010',5),'10001029':('body-lotion-box-dieline-10001029',1.5),'102010':('custom-dimensions-tuck-end-boxes-auto-bottome-snap-lock-dieline-102010',3),'112047':('roofing-cord-buckle-bottom-box-dieline-112047',3),'12109002':('cake-box-dieline-12109002',2),'112310':('custom-dimensions-tuck-end-box-variations-auto-bottome-snap-lock-boxes-dieline-112310',5),'200010':('custom-dimensions-cartons-0201-dieline-200010',9)}
for code,(slug,maximum) in slugs.items():
 actions=[]
 def wait(name,ms=700):actions.append({'action':'wait_for_timeout','duration_ms':ms,'step_id':name})
 def click(name,selector,button='left'):actions.append({'action':'click','locator':{'kind':'css','selector':selector},'button':button,'step_id':name,'timeout_ms':8000})
 def edit(name,selector,value):
  actions.append({'action':'fill','locator':{'kind':'css','selector':selector},'value':{'source':'literal','value':str(value)},'step_id':name,'timeout_ms':8000})
  actions.append({'action':'press','locator':{'kind':'css','selector':selector},'key':'Enter','step_id':name+'-apply','timeout_ms':8000});wait(name+'-ready')
 wait('loaded',3500);click('mm','[gtm="ga-dieline_dieline_basic_mm"]')
 current=None
 dims=models[code]['dims'];axes=list(dims)
 # One material-geometry snapshot plus independent mixed dimension trajectories at each verified thickness.
 for ti,t in enumerate([v for v in [.2,.26,.27,.32,.33,.35,.42,.46,.5,.55,.8,1.1,1.5,1.7,2,3,4.5,5,7,9] if v<=maximum]):
  group='white' if t<=.8 else 'corrugated'
  if group!=current:
   click(f'open-{ti}','.tree-select-header');label='Cartulina blanca' if group=='white' else 'Cartón corrugado';custom='Cartón blanco personalizado' if group=='white' else 'Cartón corrugado personalizado'
   click(f'group-{ti}',f'.tree-select-item-header:text-is("{label}")','right');click(f'custom-{ti}',f'.tree-item:not(.disabled) .material-tree-item:text-is("{custom}")');wait(f'custom-{ti}-ready',4000);current=group
  edit(f't-{ti}','.thickness-control input',t)
  # Fitted with the three independent axis changes. Combined halfway state is an independent heldout.
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-axis-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',round(dims[axis]+2,6))
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-hold-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',round(dims[axis]+1,6))
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-reset-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',dims[axis])
 scenario={'browser':{'mode':'launch','executable_path':'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','headless':True},'start_url':{'url':'https://www.pacdora.com/es/dielines-detail/'+slug},'actions':actions,'capture':{'at_end':['accessibility'],'events':['network'],'network':{'response_body':True,'request_body':True,'header_values':False}},'environment':{'locale':'es-CL','timezone':'America/Santiago','service_workers':'block'}}
 (root/f'{code}-geometry-scenario.json').write_text(json.dumps(scenario,ensure_ascii=False))
 print(code,len(actions),'actions')
