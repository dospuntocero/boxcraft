import json,glob,math
files=sorted(glob.glob('investigacion/materiales/ev_525*/knife-*.json'))
samples={}
def flat(x,p=''):
 r={}
 if isinstance(x,dict):
  for k,v in x.items():r.update(flat(v,p+'/'+k))
 elif isinstance(x,list):
  for k,v in enumerate(x):r.update(flat(v,p+'/'+str(k)))
 else:r[p]=x
 return r
for f in files:
 d=json.load(open(f))['data']; t=d['layer']['traditional']['thickness'];samples[t]=(d,flat({'faces':{f['name']:f for f in d['layer']['traditional']['faces']},'totalX':d['layer']['traditional']['totalX'],'totalY':d['layer']['traditional']['totalY']}))
samples=sorted(samples.items()); samples=[s for s in samples if s[0]>0.8]
paths=set.intersection(*(set(z[1][1]) for z in samples)); num=[p for p in paths if all(type(z[1][1][p]) in (int,float) for z in samples)]; non=[p for p in paths if p not in num]
print('thicknesses',[t for t,_ in samples],'numeric paths',len(num),'non numeric differences',[p for p in non if len(set(str(z[1][1][p]) for z in samples))>1])
print('shape counts',[(t,len(v[1]),len(v[0]['layer']['traditional']['cuts'])) for t,v in samples])
def solve(a,b):
 n=len(b);m=[list(a[i])+[b[i]] for i in range(n)]
 for i in range(n):
  j=max(range(i,n),key=lambda j:abs(m[j][i]));m[i],m[j]=m[j],m[i]
  if abs(m[i][i])<1e-9:raise ValueError('rank')
  q=m[i][i];m[i]=[v/q for v in m[i]]
  for j in range(n):
   if j!=i:
    q=m[j][i];m[j]=[v-q*w for v,w in zip(m[j],m[i])]
 return [row[-1] for row in m]
for features in ['t','t_id','t_id_ed']:
 def vec(s):
  t,(d,_)=s
  return [1,t]+([d['size']['id']] if features!='t' else [])+([d['size']['ed']] if features=='t_id_ed' else [])
 errs=[]
 for h in range(len(samples)):
  train=[s for i,s in enumerate(samples) if i!=h];X=[vec(s) for s in train];n=len(X[0]);a=[[sum(x[i]*x[j] for x in X) for j in range(n)] for i in range(n)]; pe=[]
  try:
   for p in num:
    y=[s[1][1][p] for s in train];b=[sum(x[i]*v for x,v in zip(X,y)) for i in range(n)];c=solve(a,b);e=abs(sum(v*w for v,w in zip(vec(samples[h]),c))-samples[h][1][1][p]);pe.append((e,p))
   errs.append((samples[h][0], max(pe)))
  except ValueError:errs.append((samples[h][0],'rank deficient'))
 print(features,'LOO',errs)
