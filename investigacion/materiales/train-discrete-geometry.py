"""Fit one discrete thickness affine geometry and independently validate it.
Usage: python3 train-discrete-geometry.py BASE L_CAPTURE W_CAPTURE H_CAPTURE HOLDOUT [HOLDOUT ...]
All paths are actual REA knife response JSON files. Output JSON to stdout.
No approximation is labeled supported unless all supplied heldouts have equal topology and <=1e-6 error.
"""
import sys,json,copy

def flatten(value,path=''):
 out={}
 if isinstance(value,dict):
  for key,item in value.items():out.update(flatten(item,path+'/'+str(key)))
 elif isinstance(value,list):
  for key,item in enumerate(value):out.update(flatten(item,path+'/'+str(key)))
 else:out[path]=value
 return out

def load(path):
 data=json.load(open(path))['data'];layer=copy.deepcopy(data['layer']['traditional'])
 # Dimension arrows are presentation data, not generated production geometry.
 layer.pop('sizeArrowData',None)
 return data,layer,flatten(layer)

def topology(flat):return {key:'number' if type(value) in (int,float) else [type(value).__name__,value] for key,value in flat.items()}

def inverse(matrix):
 n=len(matrix);a=[list(row)+[float(i==j) for j in range(n)] for i,row in enumerate(matrix)]
 for i in range(n):
  pivot=max(range(i,n),key=lambda j:abs(a[j][i]));a[i],a[pivot]=a[pivot],a[i]
  if abs(a[i][i])<1e-10:raise ValueError('Capture dimension matrix is rank deficient')
  divisor=a[i][i];a[i]=[value/divisor for value in a[i]]
  for j in range(n):
   if i!=j:
    factor=a[j][i];a[j]=[x-factor*y for x,y in zip(a[j],a[i])]
 return [row[n:] for row in a]

sources=sys.argv[1:]
if len(sources)<5:raise SystemExit(__doc__)
samples=[load(path) for path in sources];base=samples[0];base_dims=[base[0]['knifeSize'][axis] for axis in 'LWH'];thickness=base[1]['thickness'];topo=topology(base[2])
for path,sample in zip(sources,samples):
 if sample[1]['thickness']!=thickness:raise ValueError('Mixed thickness: '+path)
 if topology(sample[2])!=topo:raise ValueError('Different nonnumeric topology or numeric paths: '+path)
x=[[1]+[s[0]['knifeSize'][axis]-b for axis,b in zip('LWH',base_dims)] for s in samples[:4]]; inv=inverse(x)
rules={}
for path,value in base[2].items():
 if type(value) in (int,float):rules[path]=[sum(inv[i][j]*samples[j][2][path] for j in range(4)) for i in range(4)]
validation=[]
for source,s in zip(sources[4:],samples[4:]):
 vector=[1]+[s[0]['knifeSize'][axis]-b for axis,b in zip('LWH',base_dims)]
 errors=sorted(((abs(sum(a*b for a,b in zip(vector,coeff))-s[2][path]),path) for path,coeff in rules.items()),reverse=True)
 validation.append({'source':source,'maxErrorMm':errors[0][0],'worstPath':errors[0][1],'passed':errors[0][0]<=1e-6})
print(json.dumps({'thickness':thickness,'base':base_dims,'axes':list('LWH'),'layer':base[1],'rules':rules,'validation':validation,'supportedOnHeldouts':all(v['passed'] for v in validation)},ensure_ascii=False))
