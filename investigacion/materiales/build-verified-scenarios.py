import json
from pathlib import Path
root=Path(__file__).resolve().parent
models={m['id']:m for m in json.load(open(root.parents[1]/'archivo/copias/boxcraft-publicacion/dist/assets/modelos.json'))}
slugs={'150010':('custom-dimensions-flip-top-boxes-mailer-dieline-150010',5),'10001029':('body-lotion-box-dieline-10001029',1.5),'102010':('custom-dimensions-tuck-end-boxes-auto-bottome-snap-lock-dieline-102010',3),'112047':('roofing-cord-buckle-bottom-box-dieline-112047',3),'12109002':('cake-box-dieline-12109002',2),'112310':('custom-dimensions-tuck-end-box-variations-auto-bottome-snap-lock-boxes-dieline-112310',5),'200010':('custom-dimensions-cartons-0201-dieline-200010',9),'10001006':('tuck-end-software-box-dieline-10001006',1.5),'10002003':('custom-dimensions-hook-boxes-double-hook-dieline-10002003-10002003',3),'180370':('french-fries-box-dieline-180370',.8),'180320':('sandwich-box-with-window-dieline-180320',2)}
choices=[('Papel arte','200g',.2,False),('Cartulina kraft','190g',.26,False),('Cartulina blanca','210g',.27,False),('Papel arte','350g',.32,False),('Cartulina kraft','250g',.33,False),('Cartulina blanca','250g',.35,False),('Cartulina blanca','300g',.42,False),('Cartulina kraft','350g',.46,False),('Cartulina blanca','350g',.5,False),('Cartulina blanca','400g',.55,False),('Cartón corrugado','Onda N',.8,True),('Cartón corrugado','Onda N',1,True),('Cartón corrugado','Onda F',1.2,True),('Cartón corrugado','Onda E',1.5,True),('Cartón corrugado','Onda E',1.7,True),('Cartón corrugado','Onda E',2,True),('Cartón corrugado','Onda B',3,True),('Cartón corrugado','Onda C',4,True),('Cartón corrugado','Onda A',5,True),('Cartón corrugado','Onda BB',6,True),('Cartón corrugado','Onda BC',7,True),('Cartón corrugado','Onda AB',8,True),('Cartón corrugado','Onda AC',9,True)]
for code,(slug,maximum) in slugs.items():
 actions=[]
 def wait(name,ms=800):actions.append({'action':'wait_for_timeout','duration_ms':ms,'step_id':name})
 def click(name,selector,button='left'):actions.append({'action':'click','locator':{'kind':'css','selector':selector},'button':button,'step_id':name,'timeout_ms':8000})
 def edit(name,selector,value):
  actions.append({'action':'fill','locator':{'kind':'css','selector':selector},'value':{'source':'literal','value':str(value)},'step_id':name,'timeout_ms':8000});actions.append({'action':'press','locator':{'kind':'css','selector':selector},'key':'Enter','step_id':name+'-apply','timeout_ms':8000});wait(name+'-ready')
 wait('loaded',3500);click('mm','[gtm="ga-dieline_dieline_basic_mm"]')
 dims=models[code].get('initialDims') or models[code]['dims'];axes=list(dims)
 for axis in axes:
  i=axes.index(axis)+1;edit(f'base-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',dims[axis])
 for ti,(group,label,t,variable) in enumerate(c for c in choices if c[2]<=maximum):
  click(f'open-{ti}','.tree-select-header');click(f'group-{ti}',f'.tree-select-item-header:text-is("{group}")','right');selector=f'.tree-item:not(.disabled) .material-tree-item:{"text-is" if variable else "has-text"}("{label}")';click(f'material-{ti}',selector);wait(f'material-{ti}-ready',1800)
  if variable:edit(f't-{ti}','.thickness-control input',t)
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-axis-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',round(dims[axis]+2,6))
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-hold-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',round(dims[axis]+1,6))
  for axis in axes:
   i=axes.index(axis)+1;edit(f't{ti}-reset-{axis}',f'.proper-content > .proper-item:nth-child({i}) input',dims[axis])
 scenario={'browser':{'mode':'launch','executable_path':'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','headless':True},'start_url':{'url':'https://www.pacdora.com/es/dielines-detail/'+slug},'actions':actions,'capture':{'after_each_step':['accessibility'],'at_end':['accessibility'],'events':['network'],'network':{'response_body':True,'request_body':True,'header_values':False}},'environment':{'locale':'es-CL','timezone':'America/Santiago','service_workers':'block'}}
 (root/f'{code}-verified-scenario.json').write_text(json.dumps(scenario,ensure_ascii=False))
 print(code,len(actions))
