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
  assert.equal(models.length,15);
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

test('10002003: reglas compiladas exactas contra 49 capturas',()=>{
  const model=models.find(m=>m.id==='10002003');
  assert.equal(model.engine,'compiled');
  assert.equal(model.validation.status,'verified');
  assert.ok(!model.experimental);
  const dirs=[path.resolve(root,'..','geometria/modelos/10002003/parametrico/full'),path.resolve(root,'..','geometria/modelos/10002003/parametrico/bordes'),path.resolve(root,'..','geometria/modelos/10002003/parametricas')];
  let used=0,max=0;
  for(const dir of dirs){
    for(const file of fs.readdirSync(dir).filter(name=>name.endsWith('.json')&&name!=='manifest.json')){
      const raw=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));const data=raw.data||raw;
      if(!data.knifeSize||!data.layer||!data.layer.traditional)continue;
      const dims={L:data.knifeSize.L,W:data.knifeSize.W,H:data.knifeSize.H};
      const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
      for(const key of Object.keys(expected)){
        assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);
        max=Math.max(max,Math.abs(actual[key]-expected[key]));
      }
      used++;
    }
  }
  assert.ok(used>=45,`solo ${used} muestras`);
  assert.ok(max<1e-4,`error ${max}`);
});

test('10001006: reglas compiladas exactas contra 83 capturas',()=>{
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
      const actual=flat(E.generate(model,dims)),expected=flat(data.layer.traditional);
      for(const key of Object.keys(expected)){assert.ok(actual[key]!==undefined,`${file}: falta ${key}`);max=Math.max(max,Math.abs(actual[key]-expected[key]));}
      used++;
    }
  }
  assert.ok(used>=80,`solo ${used} muestras`);
  assert.ok(max<1e-4,`error ${max}`);
});
