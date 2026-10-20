const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const model=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'))).find(m=>m.id==='15030101');
function flat(o,p='',out={}){if(o&&typeof o==='object')for(const [k,v] of Object.entries(o)){if(typeof v==='number')out[p+'/'+k]=v;else if(v&&typeof v==='object')flat(v,p+'/'+k,out);}return out;}
assert.strictEqual(model.engine,'affine');
const samples=['knife-00','knife-02','knife-04','knife-06','knife-07','knife-08'];
let max=0;
for(const n of samples){
  const d=JSON.parse(fs.readFileSync(path.resolve(root,'..','geometria/modelos/15030101/parametricas',n+'.json'))).data;
  const out=E.generate(model,{L:d.knifeSize.L,W:d.knifeSize.W,H:d.knifeSize.H});
  const a=flat(out),b=flat(d.layer.traditional);
  for(const k of Object.keys(b)){if(a[k]!==undefined)max=Math.max(max,Math.abs(a[k]-b[k]));}
}
assert.ok(max<4.0,`error afín ${max}`);
console.log(`15030101 OK · ${samples.length} muestras · error afín ${max.toFixed(2)} mm`);
