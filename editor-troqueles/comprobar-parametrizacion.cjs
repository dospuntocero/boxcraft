'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const E=require('./dist/engines.js');
const models=require('./dist/assets/modelos.json');
function numbers(value,path='',out={}){if(typeof value==='number')out[path]=value;else if(value&&typeof value==='object')for(const [k,v] of Object.entries(value))numbers(v,path+'/'+k,out);return out;}
const report=[];
for(const m of models){
  assert(m.engine,`${m.id}: falta generador`);
  m.bounds=m.expandedBounds||m.bounds;
  if(m.materialWidthMm){
    const original=E.generate({...m,materialWidthMm:null},m.dims),a=numbers(original),b=numbers(m.layer);
    assert(Math.max(0,...Object.keys(b).map(k=>Math.abs(a[k]-b[k])))<1e-7);
    const exact=[{L:434,W:144,H:278},{L:400,W:178,H:278},{L:554,W:24,H:20.6},{L:30,W:548,H:20.6}];
    for(const d of exact){assert(Math.abs(E.generate(m,d).totalX-1200)<1e-7);assert.throws(()=>E.generate(m,{...d,W:d.W+.001}),/supera el material/);}
    assert(E.generate(m,{L:30,W:24,H:2000}).totalY>1200);
    assert.equal(E.fieldBounds(m,{L:30,W:24,H:20.6},'L')[1],554);
    assert.equal(E.fieldBounds(m,{L:30,W:24,H:20.6},'W')[1],548);
    assert.equal(E.fieldBounds(m,m.initialDims,'H')[1],2154);
    for(const axis of ['L','W','H'])assert.throws(()=>E.generate(m,{L:30,W:24,H:20.6,[axis]:m.bounds[axis][0]-.01}));
    report.push({id:m.id,materialWidthMm:1200,exactBoundaryCases:exact.length,unboundedMaterialLength:true});
    continue;
  }
  const original=E.generate({...m,materialSheetMm:null},m.dims),a=numbers(original);
  const baseline=m.layer;
  const b=numbers(Object.fromEntries(Object.keys(m.layer).map(k=>[k,baseline[k]])));
  const maxBaseError=Math.max(0,...Object.keys(b).map(k=>Math.abs(a[k]-b[k])));
  assert(maxBaseError<1e-7,`${m.id}: cambió la geometría original`);
  if(m.id==='102010'){
    assert.deepEqual(m.minimumDims,{L:15,W:10.6,H:20.6});
    const taller=E.generate(m,{...m.dims,H:m.dims.H+10});assert(taller.totalY>0);
    assert.throws(()=>E.generate(m,{...m.dims,L:2*m.dims.W+.01}),/L ≤ 2W/);
    const wider=E.generate(m,{...m.dims,W:m.dims.W+1});assert(wider.totalX>0);
    const deeper=E.generate(m,{...m.dims,H:m.dims.H+1});assert(deeper.totalY>0);
    report.push({id:m.id,sheetMm:m.materialSheetMm,minimumDims:m.minimumDims,editableAxes:['L','W','H']});continue;
  }
  if(m.materialSheetMm){
    const specs={'150010':[[20,22,17.6],[1000,700]],'112047':[[30,30,30.6],[1000,700]],'12109002':[[30,30,30.6],[1000,700]],'112310':[[40,40,41],[1200,2300]],'10001006':[[15,10.6,15.6],[1000,700]]};
    if(!specs[m.id]){report.push({id:m.id,sheetMm:m.materialSheetMm,skipped:'sin mínimos específicos en este comprobador'});continue;}
    const [minimums,sheet]=specs[m.id],minimum=Object.fromEntries('LWH'.split('').map((axis,i)=>[axis,minimums[i]]));
    assert.deepEqual(m.materialSheetMm,sheet);assert.deepEqual(m.minimumDims,minimum);
    E.generate(m,minimum);const start=m.initialDims||m.dims;E.generate(m,start);
    for(const axis of ['L','W','H']){
      assert.throws(()=>E.generate(m,{...minimum,[axis]:minimum[axis]-.001}));
      E.generate(m,{...start,[axis]:minimum[axis]});
      const b=E.fieldBounds(m,start,axis),last=E.generate(m,{...start,[axis]:b[1]});
      assert(E.sheetFit(last.totalX,last.totalY,sheet));
      assert.throws(()=>E.generate(m,{...start,[axis]:b[1]+.02}),/no cabe en el pliego/);
    }
    report.push({id:m.id,minimum,sheetMm:sheet,rotationAllowed:true,dynamicBoundaryCases:3});continue;
  }
  const axes=Object.keys(m.bounds);
  for(const axis of axes){
    const changed=E.generate(m,{...m.dims,[axis]:m.dims[axis]*1.03});
    assert.notEqual(JSON.stringify(changed.cuts),JSON.stringify(original.cuts),`${m.id}/${axis}: corte sin cambios`);
    assert.notEqual(JSON.stringify(changed.folds),JSON.stringify(original.folds),`${m.id}/${axis}: pliegues sin cambios`);
    assert.equal(changed.faces.length,original.faces.length);
    assert.equal(changed.holes.length,original.holes.length);
  }
  let checked=0;
  for(let mask=0;mask<2**axes.length;mask++){
    if(axes.some((axis,i)=>!Number.isFinite(m.bounds[axis][mask>>i&1])))continue;
    const dims={...m.dims};axes.forEach((axis,i)=>dims[axis]=m.bounds[axis][mask>>i&1]);
    const layer=E.generate(m,dims);assert(layer.totalX>0&&layer.totalY>0);
    assert(Object.values(numbers(layer)).every(Number.isFinite));checked++;
  }
  const axis=axes[0];assert.throws(()=>E.generate(m,{...m.dims,[axis]:m.bounds[axis][1]+1}));
  assert.throws(()=>E.generate(m,{...m.dims,[axis]:NaN}));
  report.push({id:m.id,axes,cornerCases:checked,baseMaxError:maxBaseError,experimental:!!m.experimental});
}
fs.writeFileSync('comprobacion-motores.json',JSON.stringify({pass:true,models:report},null,2));
console.log(`${models.length} modelos: identidad original, respuesta por eje, topología, extremos y rechazo de medidas inválidas correctos.`);
