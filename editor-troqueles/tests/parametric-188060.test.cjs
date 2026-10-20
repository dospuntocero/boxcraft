const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const model=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'))).find(m=>m.id==='188060');
const sampleDir=path.resolve(root,'..','geometria/modelos/188060/muestras');
function flat(o,p='',out={}){if(o&&typeof o==='object')for(const [k,v] of Object.entries(o)){if(typeof v==='number')out[p+'/'+k]=v;else if(v&&typeof v==='object')flat(v,p+'/'+k,out);}return out;}
function parse(d){const t=d.match(/[MLAZ]|-?\d+(?:\.\d+)?(?:e[+-]?\d+)?/g)||[];let i=0,o=[];while(i<t.length){const c=t[i],n={M:2,L:2,A:7,Z:0}[c];o.push([c,t.slice(i+1,i+1+n).map(Number)]);i+=1+n;}return o;}
assert.strictEqual(model.engine,'panel188060');
const base=E.generate(model,{L:100.6,W:40.6,H:181.6});
const orig=flat(model.layer),got=flat(base);
for(const [k,v] of Object.entries(orig))assert.ok(Math.abs(v-got[k])<1e-9,`base ${k}`);
const limits={L110:0.8,W45:0.2,H190:1e-6};
for(const [name,limit] of Object.entries(limits)){
  const s=JSON.parse(fs.readFileSync(path.join(sampleDir,name+'.json')));
  const out=E.generate(model,s.dims);let max=0;
  for(const f of out.faces){
    const exp=parse(s.faces[f.name]);const gen=f.dlist;assert.strictEqual(exp.length,gen.length);
    for(let i=0;i<exp.length;i++){
      const [t,a]=exp[i],g=gen[i];assert.strictEqual(t,g.mtd);
      if(t==='A')max=Math.max(max,Math.abs(a[5]-g.x),Math.abs(a[6]-g.y));
      else if(t==='M'||t==='L')max=Math.max(max,Math.abs(a[0]-g.x),Math.abs(a[1]-g.y));
    }
  }
  assert.ok(max<limit,`${name}: ${max}`);
}
const l=E.generate(model,{L:110,W:40.6,H:181.6});
assert.ok(Math.abs(l.totalX-355.5)<1e-9&&Math.abs(l.totalY-262.8)<1e-9);
const wh=E.generate(model,{L:110,W:45,H:190});
assert.ok(Math.abs(wh.totalX-355.5)<1e-9&&Math.abs(wh.totalY-280)<1e-9);
console.log('188060 OK · panel L/W/H · L110 0,70 · W45 0,16 · H190 0,00 mm');
