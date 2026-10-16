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

test('verified profiles filter material and thickness together without inventing a continuous range',()=>{
 const materialA={id:1,min:.5,max:3},materialB={id:2,min:1,max:2},materialC={id:3,min:.5,max:3};
 const cap={originalMaterialId:1,originalThickness:1,offsets:{inner:{L:-2},outer:{L:2}},observedThicknessLimits:[.5,3],physicalProfiles:[{materialIds:[1,2],thickness:2,layer:{totalX:42},offsets:{inner:{L:-4},outer:{L:4}},bounds:{L:[10,20]},geometryStatus:'verified'},{materialIds:[3],thickness:2,layer:{},geometryStatus:'unverified'},{materialIds:[2],thickness:3,layer:{},geometryStatus:'verified'}]};
 assert.deepEqual(M.compatible(cap,[materialA,materialB,materialC]).map(m=>m.id),[1,2]);
 assert.deepEqual(M.thicknesses(cap,materialB),[2]);
 assert.deepEqual(M.thicknesses(cap,materialA),[1,2]);
 assert.throws(()=>M.validate(cap,[materialA],{materialId:1,thickness:1.5}));
 const physical={materialId:2,thickness:2};M.validate(cap,[materialB],physical);
 assert.deepEqual(M.display(cap,{L:15},'inner',physical),{L:11});
 assert.deepEqual(M.manufacture(cap,{L:11},'inner',physical),{L:15});
 // Converting old visible dimensions using the NEW profile preserves the requested interior size.
 const visible=M.display(cap,{L:15},'inner',{materialId:1,thickness:1});
 assert.deepEqual(M.manufacture(cap,visible,'inner',physical),{L:17});
 const model={dims:{L:15},materialCapability:cap,layer:{totalX:10},bounds:{L:[1,100]},engine:'derived'};
 const selected=M.modelFor(model,physical);assert.equal(selected.layer.totalX,42);assert.deepEqual(selected.bounds,{L:[10,20]});assert.equal(selected.engine,null);
 assert.throws(()=>M.generate(model,{L:30},physical,[materialB]),/rango verificado/);
});
test('profiles without captured conversion offsets cannot reuse original conversion',()=>{
 const cap={originalMaterialId:1,originalThickness:1,offsets:{inner:{L:-2}},physicalProfiles:[{materialIds:[1],thickness:2,layer:{}}]};
 assert.throws(()=>M.display(cap,{L:10},'inner',{materialId:1,thickness:2}),/Conversión/);
 assert.deepEqual(M.display(cap,{L:10},'manufacturing',{materialId:1,thickness:2}),{L:10});
});
