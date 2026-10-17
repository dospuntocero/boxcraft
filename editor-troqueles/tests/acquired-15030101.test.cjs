const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
global.TroquelEngines=require('../dist/engines.js');const M=require('../dist/materials.js');
const cap=require('../dist/assets/capacidades-materiales.json')['15030101'],model={...require('../dist/assets/modelos.json').find(m=>m.id==='15030101'),materialCapability:cap},materials=require('../dist/assets/materiales.json').materials;
test('15030101: every enabled alternative matches its retained source, including conversion',()=>{
 assert.equal(cap.physicalProfiles.length,17);
 for(const p of cap.physicalProfiles){
  const raw=fs.readFileSync(path.join(__dirname,'../..',p.evidence.path));assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),p.evidence.sha256);
  const source=JSON.parse(raw).data,physical={materialId:p.materialIds[0],thickness:p.thickness};
  assert.equal(source.science.id,physical.materialId);assert.equal(source.layer.traditional.thickness,physical.thickness);
  const expected=Object.fromEntries(Object.entries(source.layer.traditional).filter(([k])=>!['bleeds','sizeArrowData'].includes(k)));
  assert.deepEqual(M.generate(model,model.dims,physical,materials),expected);
  for(const [mode,key] of [['inner','size'],['outer','outSize']]){
   const visible=M.display(cap,model.dims,mode,physical);for(const a of 'LWH')assert.ok(Math.abs(visible[a]-source[key][a])<1e-7);
  }
 }
});
test('15030101: custom thickness stays discrete and dimensions stay exact',()=>{
 for(const id of [8,7,153]){
  assert.deepEqual(M.thicknesses(cap,materials.find(m=>m.id===id)),[.2,.35,.5]);
  assert.throws(()=>M.generate(model,model.dims,{materialId:id,thickness:.3},materials));
  assert.throws(()=>M.generate(model,{...model.dims,H:51},{materialId:id,thickness:.35},materials));
 }
});
