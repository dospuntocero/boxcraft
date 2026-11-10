const test=require('node:test');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const models=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'),'utf8'));
const model=models.find(m=>m.id==='102610');
function flat(value,key='',out={}){
  if(value&&typeof value==='object'&&!Array.isArray(value)){
    for(const [k,v] of Object.entries(value)){if(['bleeds','sizeArrowData','transform','animation'].includes(k))continue;flat(v,key+'/'+k,out);}
  }else if(Array.isArray(value)){value.forEach((v,i)=>flat(v,key+'/'+i,out));}
  else if(typeof value==='number'&&Number.isFinite(value))out[key]=value;
  return out;
}
test('102610: motor compilado reproduce las capturas del rango validado',()=>{
  assert.ok(model);assert.equal(model.engine,'compiled');assert.equal(model.validation.status,'verified');assert.equal(model.experimental,false);
  const dir=path.resolve(root,'..','geometria/modelos/102610/parametrico');let used=0,max=0;
  for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&name!=='manifest.json')){
    const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));const data=raw.data||raw;
    if(!data.knifeSize||!data.layer||!data.layer.traditional)continue;
    const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
    if(!Object.entries(dims).every(([axis,value])=>value>=model.bounds[axis][0]-1e-9&&value<=model.bounds[axis][1]+1e-9))continue;
    const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
    for(const key of Object.keys(expected)){assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);max=Math.max(max,Math.abs(actual[key]-expected[key]));}
    used++;
  }
  assert.ok(used>=70,`solo ${used} muestras`);assert.ok(max<1e-4,`error ${max}`);
});
test('102610: medidas iniciales, límites y trazado con curvas Q',()=>{
  assert.deepEqual(model.bounds,{L:[60,200],W:[20,100],H:[50,250]});
  assert.deepEqual(model.minimumDims,{L:60,W:20,H:50});
  const base=E.generate(model,{L:120.6,W:60.6,H:161.6});
  assert.ok(Math.abs(base.totalX-377.9)<1e-6);assert.ok(Math.abs(base.totalY-311.3)<1e-6);
  assert.equal(base.faces.length,13);assert.equal(base.folds.length,12);
  assert.ok(base.faces.some(face=>face.dlist.some(c=>c.mtd==='Q')),'faltan curvas Q');
  for(const dims of [{L:60,W:20,H:50},{L:200,W:100,H:250},{L:80,W:30,H:120}]){
    const layer=E.generate(model,dims);assert.equal(layer.faces.length,13);assert.equal(layer.folds.length,12);
    assert.ok(layer.totalX>0&&layer.totalY>0);
    assert.ok(['direct','rotated'].includes(E.sheetFit(layer.totalX,layer.totalY,[1000,700])));
  }
});
test('102610: regímenes de anchura 20, 25, 30 y 31 mm',()=>{
  const layers=[20,25,30,31].map(W=>E.generate(model,{L:120.6,W,H:160}));
  const flatLayers=layers.map(layer=>flat(layer));
  for(let i=1;i<flatLayers.length;i++)assert.ok(Object.keys(flatLayers[i]).some(key=>Math.abs(flatLayers[i][key]-flatLayers[i-1][key])>1e-9));
});
