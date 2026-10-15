const test=require('node:test'),assert=require('node:assert/strict');
global.TroquelEngines=require('../dist/engines.js');
const M=require('../dist/materials.js'),models=require('../dist/assets/modelos.json'),caps=require('../dist/assets/capacidades-materiales.json'),catalog=require('../dist/assets/materiales.json').materials;
const close=(a,b)=>assert.ok(Math.abs(a-b)<.000001,`${a} != ${b}`);
for(const model of models){
 const cap=caps[model.id],m={...model,materialCapability:cap},physical={materialId:cap.originalMaterialId,thickness:cap.originalThickness};
 test(`${m.id}: original geometry unchanged and guarded`,()=>{
  const dims=m.initialDims||m.dims;
  assert.deepEqual(M.generate(m,dims,physical,catalog),TroquelEngines.generate(model,dims));
  assert.throws(()=>M.generate(m,dims,{...physical,thickness:physical.thickness+.05},catalog));
  assert.throws(()=>TroquelEngines.generate(m,dims,{...physical,thickness:NaN}));
  const other=catalog.find(x=>x.id!==physical.materialId);assert.ok(M.reason(cap,other));assert.throws(()=>M.generate(m,dims,{...physical,materialId:other.id},catalog));
 });
 test(`${m.id}: conversions reproduce every retained matching sample`,()=>{
  for(const sample of cap.samples){const dims=Object.fromEntries(Object.keys(m.dims).map(a=>[a,sample.manufacturing[a]]));
   for(const mode of Object.keys(M.modes)){
    if(cap.onlyManufacturing&&mode!=='manufacturing'){assert.throws(()=>M.display(cap,dims,mode));continue;}
    const visible=M.display(cap,dims,mode),roundTrip=M.manufacture(cap,visible,mode);
    for(const axis of Object.keys(dims)){close(roundTrip[axis],dims[axis]);close(visible[axis],mode==='manufacturing'?dims[axis]:sample[mode][axis]);}
   }
  }
 });
 test(`${m.id}: converted minimum, material range, and sheet rejection`,()=>{
  const dims=m.initialDims||m.dims,mat=catalog.find(x=>x.id===physical.materialId),range=M.limits(cap,mat);
  assert.ok(range[0]<=physical.thickness&&range[1]>=physical.thickness);
  for(const mode of Object.keys(M.modes)){if(cap.onlyManufacturing&&mode!=='manufacturing')continue;
   const visible=M.display(cap,dims,mode);
   for(const a of Object.keys(model.bounds)){const bound=model.bounds[a][0],shift=visible[a]-dims[a];const changed=M.manufacture(cap,{...visible,[a]:bound+shift-.01},mode);assert.throws(()=>M.generate(m,changed,physical,catalog));}
  }
  if(m.materialSheetMm||m.materialWidthMm)assert.throws(()=>M.generate(m,{...dims,H:10000,L:10000},physical,catalog));
 });
}
