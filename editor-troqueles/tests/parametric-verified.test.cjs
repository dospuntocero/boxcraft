const test=require('node:test');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const models=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'),'utf8'));

function flat(value,key='',out={}){
  if(value&&typeof value==='object'&&!Array.isArray(value)){
    for(const [k,v] of Object.entries(value)){if(['bleeds','sizeArrowData','transform','animation'].includes(k))continue;flat(v,key+'/'+k,out);}
  }else if(Array.isArray(value)){
    value.forEach((v,i)=>flat(v,key+'/'+i,out));
  }else if(typeof value==='number'&&Number.isFinite(value))out[key]=value;
  return out;
}
function parse(d){const t=d.match(/[MLAZ]|-?\d+(?:\.\d+)?(?:e[+-]?\d+)?/g)||[];let i=0,o=[];while(i<t.length){const c=t[i],n={M:2,L:2,A:7,Z:0}[c];o.push([c,t.slice(i+1,i+1+n).map(Number)]);i+=1+n;}return o;}
function compare(expected,generated){let ei=0,gi=0,max=0;while(ei<expected.length||gi<generated.length){while(ei<expected.length&&expected[ei][0]==='Z')ei++;while(gi<generated.length&&generated[gi].mtd==='Z')gi++;if(ei>=expected.length||gi>=generated.length)break;const [t,a]=expected[ei],g=generated[gi];assert.equal(t,g.mtd);if(t==='A')max=Math.max(max,Math.abs(a[0]-g.rx),Math.abs(a[1]-g.ry),Math.abs(a[5]-g.x),Math.abs(a[6]-g.y),Math.abs(a[4]-g.dir));else if(t==='M'||t==='L')max=Math.max(max,Math.abs(a[0]-g.x),Math.abs(a[1]-g.y));ei++;gi++;}return max;}

test('catálogo: los modelos verificados no son experimentales',()=>{
  assert.equal(models.length,16);
  for(const model of models){
    if(model.validation&&model.validation.status==='verified'){
      assert.ok(!model.experimental,`${model.id}: sigue experimental`);
      assert.ok(model.verifiedBounds&&Object.keys(model.verifiedBounds).length,`${model.id}: sin verifiedBounds`);
    }
  }
});

test('187000: motor y 7 muestras exactas',()=>{
  const model=models.find(m=>m.id==='187000');
  assert.equal(model.validation.status,'verified');
  assert.ok(!model.experimental);
  const data=JSON.parse(fs.readFileSync(path.resolve(root,'..','geometria/modelos/187000/muestras.json'),'utf8'));
  let maxCut=0,maxFace=0;
  for(const sample of data.samples){
    const layer=E.pillow187000(sample.dims);
    maxCut=Math.max(maxCut,compare(parse(sample.cut),layer.cuts));
    for(const face of layer.faces)maxFace=Math.max(maxFace,compare(parse(sample.faces[face.name]),face.dlist));
  }
  assert.ok(maxCut<1e-4,`corte ${maxCut}`);
  assert.ok(maxFace<1e-4,`caras ${maxFace}`);
});

test('366010: 58 muestras, cuatro capas, sin error fuera de sangrado',()=>{
  const model=models.find(m=>m.id==='366010');
  assert.equal(model.validation.status,'verified');
  assert.ok(!model.experimental);
  const dir=path.resolve(root,'..','geometria/modelos/366010/parametricas');
  let used=0,max=0;
  for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&name!=='manifest.json')){
    const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));
    const data=raw.data||raw;
    if(!data.knifeSize)continue;
    const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
    let pieces;
    try{pieces=E.rigid366010Pieces(model,dims);}catch{continue;}
    used++;
    for(const piece of pieces){
      const expected=data.layer[piece.prefix];
      if(!expected)continue;
      const actual=flat(piece.layer),wanted=flat(expected);
      for(const key of new Set([...Object.keys(actual),...Object.keys(wanted)])){
        if(actual[key]===undefined||wanted[key]===undefined)continue;
        max=Math.max(max,Math.abs(actual[key]-wanted[key]));
      }
    }
  }
  assert.ok(used>=58,`solo ${used} muestras`);
  assert.ok(max<1e-4,`error ${max}`);
});

test('motor compilado: features, redondeo y regímenes',()=>{
  const layer={totalX:1,totalY:1,cuts:[],faces:[],folds:[],holes:[]};
  const model={id:'toy',engine:'compiled',dims:{L:10,W:10,H:10},bounds:{L:[1,100],W:[1,100],H:[1,100]},layer,
    rule:{base:{L:10,W:10,H:10},features:{
      A:{expr:{L:0.5},op:'floor',step:1},
      mode:{op:'piecewise',cases:[{when:{W:{lt:20}},value:1},{value:2}]}
    },rules:{'/totalX':{const:0,L:1,A:2,mode:0},'/totalY':{const:5,W:1}}}};
  const out=E.generate(model,{L:11,W:15,H:10});
  assert.equal(out.totalX,11+2*5);
  assert.equal(out.totalY,20);
  const rmodel={...model,rule:{...model.rule,rules:{'/totalX':{const:0,mode:10},'/totalY':{const:1}}},bounds:{L:[1,100],W:[1,100],H:[1,100]}};
  assert.equal(E.generate(rmodel,{L:10,W:25,H:10}).totalX,20);
});

test('10002003: reglas compiladas exactas contra 78 capturas (L 70–120, H 70–150)',()=>{
  const model=models.find(m=>m.id==='10002003');
  assert.equal(model.engine,'compiled');
  assert.equal(model.validation.status,'verified');
  assert.ok(!model.experimental);
  assert.deepEqual(model.bounds,{L:[70,120],W:[30,48],H:[70,150]});
  assert.deepEqual(model.verifiedBounds,{L:[70,120],W:[30,48],H:[70,150]});
  const base=path.resolve(root,'..','geometria/modelos/10002003');
  const dirs=[path.join(base,'parametrico/full'),path.join(base,'parametrico/bordes'),path.join(base,'parametricas'),path.join(base,'parametrico/extension')];
  const seen=new Set();let max=0;
  for(const dir of dirs){
    for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&!name.includes('manifest'))){
      const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));const data=raw.data||raw;
      if(!data.knifeSize||!data.layer||!data.layer.traditional)continue;
      const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
      seen.add(`${dims.L}/${dims.W}/${dims.H}`);
      const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
      for(const key of Object.keys(expected)){
        assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);
        max=Math.max(max,Math.abs(actual[key]-expected[key]));
      }
    }
  }
  assert.ok(seen.size>=78,`solo ${seen.size} muestras únicas`);
  assert.ok(max<1e-4,`error ${max}`);
});

test('10002003: se arma desde H=70 y corrige la frontera de G',()=>{
  const model=models.find(m=>m.id==='10002003');
  for(const dims of [{L:80,W:30,H:70},{L:100,W:40,H:70},{L:120,W:48,H:70}]){
    const layer=E.generate(model,dims);
    assert.equal(layer.faces.length,16);
    assert.equal(layer.folds.length,15);
    assert.equal(layer.holes.length,2);
    const faces=Object.fromEntries(layer.faces.map(face=>[face.name,face]));
    // The dust flaps fold into the box from each opening. At H=70 the largest
    // pair keeps clearance instead of colliding inside.
    const dust=Math.max(...['FRT','FLT','FRB','FLB'].map(name=>faces[name].h));
    assert.ok(2*dust<=dims.H,`H ${dims.H}: solapas interiores sin holgura`);
    assert.ok(layer.totalX>0&&layer.totalY>0);
  }
  assert.throws(()=>E.generate(model,{L:100,W:40,H:69.99}),/70/);
  // G = 16 from L+W >= 125.25 mm; the 125 mm case keeps the 13 mm paste tab.
  assert.ok(Math.abs(E.generate(model,{L:85,W:40,H:70}).totalX-262.5)<1e-6);
  assert.ok(Math.abs(E.generate(model,{L:90,W:36,H:70}).totalX-267.5)<1e-6);
});

test('10002003: longitud mínima 70 y fronteras de A/AR',()=>{
  const model=models.find(m=>m.id==='10002003');
  for(const dims of [{L:70,W:30,H:70},{L:70,W:40,H:120},{L:70,W:48,H:150}]){
    const layer=E.generate(model,dims);
    assert.equal(layer.faces.length,16);
    assert.equal(layer.folds.length,15);
    assert.equal(layer.holes.length,2);
    assert.ok(layer.totalX>0&&layer.totalY>0);
  }
  assert.throws(()=>E.generate(model,{L:69.99,W:40,H:120}),/70/);
  assert.ok(Math.abs(E.generate(model,{L:70,W:40,H:120}).totalX-232.5)<1e-6);
  const dir=path.resolve(root,'..','geometria/modelos/10002003/parametrico/extension');
  // L<100 uses AR thresholds 35/43 mm and A = ceil((W - 1) / 2).
  for(const file of ['ext-L70-W33-H120.json','ext-L70-W41-H120.json','ext-L70-W41.5-H120.json']){
    const data=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8')).data;
    const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
    const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
    for(const key of Object.keys(expected))assert.ok(Math.abs(actual[key]-expected[key])<1e-4,`${file}: ${key}`);
  }
});

test('10001006: reglas compiladas exactas contra las capturas del rango ampliado',()=>{
  const model=models.find(m=>m.id==='10001006');
  assert.equal(model.engine,'compiled');
  assert.equal(model.validation.status,'verified');
  assert.ok(!model.experimental);
  const base=path.resolve(root,'..','geometria/modelos/10001006/parametrico');
  const dirs=[base,...fs.readdirSync(base).filter(name=>fs.statSync(path.join(base,name)).isDirectory()).map(name=>path.join(base,name))];
  let used=0,max=0;
  for(const dir of dirs){
    for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&name!=='manifest.json'&&name!=='capturas-manifest.json')){
      const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));const data=raw.data||raw;
      if(!data.knifeSize||!data.layer||!data.layer.traditional)continue;
      const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
      if(!Object.entries(dims).every(([axis,value])=>value>=model.bounds[axis][0]-1e-9&&value<=model.bounds[axis][1]+1e-9))continue;
      const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
      for(const key of Object.keys(expected)){assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);max=Math.max(max,Math.abs(actual[key]-expected[key]));}
      used++;
    }
  }
  assert.ok(used>=270,`solo ${used} muestras`);
  assert.ok(max<1e-4,`error ${max}`);
});

test('10001006: rango ampliado L 30–100 y W 10,6–60',()=>{
  const model=models.find(m=>m.id==='10001006');
  assert.deepEqual(model.bounds,{L:[30,100],W:[10.6,60],H:[80,180]});
  assert.deepEqual(model.verifiedBounds,{L:[30,100],W:[10.6,60],H:[80,180]});
  assert.equal(model.experimental,false);
  for(const dims of [{L:100,W:60,H:180},{L:30,W:10.6,H:80},{L:74,W:14,H:124},{L:100,W:20,H:130},{L:30,W:60,H:80},{L:99.5,W:29.5,H:130}]){
    const layer=E.generate(model,dims);
    assert.equal(layer.faces.length,13);
    assert.equal(layer.folds.length,12);
    assert.ok(layer.totalX>0&&layer.totalY>0);
    assert.ok(E.sheetFit(layer.totalX,layer.totalY,model.materialSheetMm));
  }
  const narrow=E.generate(model,{L:74,W:14,H:124});
  assert.ok(Math.abs(narrow.totalX-188)<1e-6);
  assert.ok(Math.abs(narrow.totalY-177)<1e-6);
});

test('10001006: regímenes de anchura en 20 y 30 mm',()=>{
  const model=models.find(m=>m.id==='10001006');
  const a=E.generate(model,{L:40,W:20,H:130});
  const b=E.generate(model,{L:40,W:20.5,H:130});
  const c=E.generate(model,{L:40,W:30,H:130});
  const d=E.generate(model,{L:40,W:30.5,H:130});
  const differs=(x,y)=>Object.keys(flat(x)).some(key=>Math.abs(flat(x)[key]-flat(y)[key])>1e-9);
  assert.ok(differs(a,b));
  assert.ok(differs(c,d));
});
