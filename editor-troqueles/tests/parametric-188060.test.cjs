const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const E=require(path.join(root,'dist/engines.js'));
const model=JSON.parse(fs.readFileSync(path.join(root,'dist/assets/modelos.json'))).find(m=>m.id==='188060');
function flat(o,p='',out={}){if(o&&typeof o==='object')for(const [k,v] of Object.entries(o)){if(typeof v==='number')out[p+'/'+k]=v;else if(v&&typeof v==='object')flat(v,p+'/'+k,out);}return out;}
assert.strictEqual(model.engine,'panel188060');
const base=E.generate(model,{L:100.6,W:40.6,H:181.6});
const orig=flat(model.layer), got=flat(base);
for(const [k,v] of Object.entries(orig))assert.ok(Math.abs(v-got[k])<1e-9,`base ${k}`);
const l=E.generate(model,{L:110,W:40.6,H:181.6});
assert.ok(Math.abs(l.totalX-355.5)<1e-9);
assert.ok(Math.abs(l.totalY-262.8)<1e-9);
const tr=l.faces.find(f=>f.name==='TR').dlist;
assert.ok(Math.abs(tr[1].x-355.5)<1e-9&&Math.abs(tr[1].y-20.638333333333335)<1e-9);
const wh=E.generate(model,{L:110,W:45,H:190});
assert.ok(Math.abs(wh.totalX-355.5)<1e-9&&Math.abs(wh.totalY-280)<1e-9);
console.log('188060 OK · panel L/W/H · base exacta · L=110 validado');
