const test=require('node:test'),assert=require('node:assert/strict');
global.TroquelEngines=require('../dist/engines.js');
const M=require('../dist/materials.js'),models=require('../dist/assets/modelos.json'),caps=require('../dist/assets/capacidades-materiales.json'),materials=require('../dist/assets/materiales.json').materials;
for(const model of models){
 const cap=caps[model.id],m={...model,materialCapability:cap};
 test(`${model.id}: observed materials respect thickness, conversion and measurement scope`,()=>{
  for(const p of cap.physicalProfiles||[]){
   const dims=p.evidence.configuration;
   for(const materialId of p.materialIds){
    const physical={materialId,thickness:p.thickness},mat=materials.find(x=>x.id===materialId);
    assert.ok(M.compatible(cap,materials).includes(mat));assert.ok(M.thicknesses(cap,mat).includes(p.thickness));
    const actual=M.generate(m,dims,physical,materials);
    assert.equal(actual.totalX,p.layer.totalX);assert.equal(actual.totalY,p.layer.totalY);
    assert.deepEqual(actual.cuts,p.layer.cuts);assert.deepEqual(actual.folds,p.layer.folds);
    assert.throws(()=>M.generate(m,{...dims,[Object.keys(dims)[0]]:dims[Object.keys(dims)[0]]+.1},physical,materials));
    assert.throws(()=>M.generate(m,dims,{materialId,thickness:p.thickness+.0001},materials));
    for(const mode of Object.keys(M.modes)){
     if(cap.onlyManufacturing&&mode!=='manufacturing')continue;
     const visible=M.display(cap,dims,mode,physical),back=M.manufacture(cap,visible,mode,physical);
     for(const axis of Object.keys(dims)){assert.ok(Math.abs(back[axis]-dims[axis])<1e-7);assert.ok(Math.abs(visible[axis]-dims[axis]-(mode==='manufacturing'?0:p.offsets[mode][axis]))<1e-7);}
    }
   }
  }
 });
}
test('changing physical settings changes measured production geometry, not only labels',()=>{
 const model=models.find(m=>m.id==='150010'),cap=caps[model.id],m={...model,materialCapability:cap},a={materialId:152,thickness:.8},b={materialId:152,thickness:1.7};
 const dims={L:315,W:202,H:62},thin=M.generate(m,dims,a,materials),thick=M.generate(m,dims,b,materials);
 assert.equal(thin.totalX,566);assert.equal(thick.totalX,577);assert.notDeepEqual(thin.cuts,thick.cuts);
 assert.notDeepEqual(M.display(cap,dims,'inner',a),M.display(cap,dims,'inner',b));
});
