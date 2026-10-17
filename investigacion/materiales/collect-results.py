import json,base64,hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parent;out=root/'samples';out.mkdir(exist_ok=True)
all_records=[]
for path in sorted(list(root.glob('*result.json'))+[root/'retained-audit-final.json']):
 if not path.stat().st_size:continue
 try:j=json.loads(path.read_text())
 except json.JSONDecodeError:continue
 recs=j.get('records',[j]);
 for rec in recs:
  r=rec.get('normalized_result',rec.get('details',{}).get('partial_observation',{}).get('capture',{}));r=r.get('error',{}).get('details',{}).get('partial_observation',{}).get('capture',r)
  if not r.get('steps'):continue
  recid=rec.get('evidence_id') or 'sha256-'+hashlib.sha256(path.read_bytes()).hexdigest();events=r.get('events',{}).get('items',[]);reqs={e['transaction_id']:e for e in events if e['kind']=='request'};samples=[]
  for e in events:
   if e['kind']!='network-content' or e['phase']!='response' or not e.get('body',{}).get('content'):continue
   req=reqs.get(e['transaction_id'],{});url=req.get('url',{}).get('url','')
   if not any(x in url for x in ['/project/knife','/models/preview','category/cal']):continue
   try:d=json.loads(base64.b64decode(e['body']['content']))
   except:continue
   kind='knife' if '/project/knife' in url else 'preview' if '/models/preview' in url else 'cal';data=d.get('data')
   if not isinstance(data,dict):continue
   folder=out/path.stem/recid;folder.mkdir(parents=True,exist_ok=True);dest=folder/f'{kind}-{e["sequence"]}.json';dest.write_text(json.dumps(d,ensure_ascii=False))
   samples.append({'file':str(dest.relative_to(root)),'kind':kind,'step':e.get('step_index'), 'model':str(data.get('cate_no','')), 'thickness':data.get('layer',{}).get('traditional',{}).get('thickness'),'dims':data.get('knifeSize'),'sequence':e['sequence']})
  failed=next((s for s in r['steps'] if s['status']!='completed'),None)
  record={'file':path.name,'evidenceId':recid,'failed':{k:failed.get(k) for k in ['step_id','status','error']} if failed else None,'samples':samples,'stepIds':{s['step_index']:s['step_id'] for s in r['steps']}}
  all_records.append(record)
(root/'collected.json').write_text(json.dumps(all_records,ensure_ascii=False,indent=2))
for r in all_records:print(r['file'],'knives',sum(x['kind']=='knife' for x in r['samples']),'failure',r['failed'])
