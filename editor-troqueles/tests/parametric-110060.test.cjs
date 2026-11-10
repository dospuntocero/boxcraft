const test=require('node:test');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const models=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'),'utf8'));
const model=models.find(m=>m.id==='110060');

function flat(value,key='',out={}){
  if(value&&typeof value==='object'&&!Array.isArray(value)){
    for(const [k,v] of Object.entries(value)){if(['bleeds','sizeArrowData','transform','animation'].includes(k))continue;flat(v,key+'/'+k,out);}
  }else if(Array.isArray(value)){
    value.forEach((v,i)=>flat(v,key+'/'+i,out));
  }else if(typeof value==='number'&&Number.isFinite(value))out[key]=value;
  return out;
}

test('110060: motor compilado reproduce las capturas del rango validado',()=>{
  assert.ok(model);
  assert.equal(model.engine,'compiled');
  assert.equal(model.validation.status,'verified');
  assert.equal(model.experimental,false);
  const dir=path.resolve(root,'..','geometria/modelos/110060/parametrico');
  let used=0,max=0;
  for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&name!=='manifest.json')){
    const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));const data=raw.data||raw;
    if(!data.knifeSize||!data.layer||!data.layer.traditional)continue;
    const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
    if(!Object.entries(dims).every(([axis,value])=>value>=model.bounds[axis][0]-1e-9&&value<=model.bounds[axis][1]+1e-9))continue;
    const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
    for(const key of Object.keys(expected)){assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);max=Math.max(max,Math.abs(actual[key]-expected[key]));}
    used++;
  }
  assert.ok(used>=70,`solo ${used} muestras`);
  assert.ok(max<1e-4,`error ${max}`);
});

test('110060: medidas iniciales, límites y pliego',()=>{
  assert.deepEqual(model.bounds,{L:[30,120],W:[20,50],H:[30,200]});
  assert.deepEqual(model.minimumDims,{L:20.6,W:15.6,H:20.6});
  const base=E.generate(model,{L:61.6,W:20.6,H:91.6});
  assert.ok(Math.abs(base.totalX-101.8)<1e-6);
  assert.ok(Math.abs(base.totalY-236.15)<1e-6);
  for(const dims of [{L:30,W:20,H:30},{L:120,W:50,H:200},{L:80,W:30,H:120}]){
    const layer=E.generate(model,dims);
    assert.equal(layer.faces.length,13);
    assert.equal(layer.folds.length,12);
    assert.ok(layer.totalX>0&&layer.totalY>0);
    assert.ok(E.sheetFit(layer.totalX,layer.totalY,[1000,700]));
  }
});

test('110060: regímenes de anchura 20, 30 y 31 mm',()=>{
  const a=E.generate(model,{L:70,W:20,H:100});
  const b=E.generate(model,{L:70,W:20.5,H:100});
  const c=E.generate(model,{L:70,W:30,H:100});
  const d=E.generate(model,{L:70,W:30.5,H:100});
  const differs=(x,y)=>Object.keys(flat(x)).some(key=>Math.abs(flat(x)[key]-flat(y)[key])>1e-9);
  assert.ok(differs(a,b));
  assert.ok(differs(c,d));
});
