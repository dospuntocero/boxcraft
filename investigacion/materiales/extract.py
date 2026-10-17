import json,base64,sys
from pathlib import Path
src=Path(sys.argv[1]);out=Path(__file__).resolve().parent
j=json.loads(src.read_text());summaries=[]
for rec in j['records']:
 r=rec.get('normalized_result',{});r=r.get('error',{}).get('details',{}).get('partial_observation',{}).get('capture',r);steps=r.get('steps',[])
 if not steps:continue
 rid=rec['evidence_id'];folder=out/rid;folder.mkdir(exist_ok=True)
 events=r.get('events',{}).get('items',[]);requests={e['transaction_id']:e for e in events if e['kind']=='request'};got=[]
 for e in events:
  if e['kind']!='network-content' or e['phase']!='response' or not e['body'].get('content'):continue
  req=requests.get(e['transaction_id'],{});url=req.get('url',{}).get('url','')
  if not any(x in url for x in ['/project/knife','/models/preview','category/cal','/projects/info']):continue
  try:data=json.loads(base64.b64decode(e['body']['content']))
  except:continue
  kind='knife' if '/project/knife' in url else 'preview' if '/models/preview' in url else 'cal' if 'category/cal' in url else 'project'
  path=folder/f'{kind}-{e["sequence"]}.json';path.write_text(json.dumps(data,ensure_ascii=False))
  d=data.get('data',{});got.append({'kind':kind,'step':e.get('step_index'),'sequence':e['sequence'],'path':str(path.relative_to(out)),'thickness':d.get('layer',{}).get('traditional',{}).get('thickness',d.get('thickness')),'dims':d.get('knifeSize'),'model':d.get('cate_no'),'supportSciences':d.get('supportSciences')})
 (folder/'steps.json').write_text(json.dumps(steps,ensure_ascii=False))
 summaries.append({'evidence_id':rid,'start':rec.get('parameters',{}).get('start_url'),'steps':[{k:s.get(k) for k in ['step_id','status','error']} for s in steps],'records':got})
(out/'summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2))
for s in summaries:
 print(s['evidence_id'],s['start']);print('FAILED',[(x['step_id'],str(x['error'])[:200]) for x in s['steps'] if x['status']!='completed']);print('KNIVES',[(x['model'],x['thickness'],x['dims']) for x in s['records'] if x['kind']=='knife'])
