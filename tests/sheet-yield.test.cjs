const test=require('node:test'),assert=require('node:assert/strict');
const {sheetYield}=require('../dist/engines.js');
test('cuadrícula incluye 3 mm a cada lado',()=>{const r=sheetYield(194,94,[1000,700]);assert.equal(r.count,35);assert.equal(r.columns,5);assert.equal(r.rows,7);assert.equal(r.blankWidth,200);});
test('selecciona giro de 90 grados cuando caben más',()=>{const r=sheetYield(294,194,[1000,700]);assert.equal(r.count,10);assert.equal(r.rotated,true);assert.equal(r.columns,5);assert.equal(r.rows,2);});
test('caja pastel de referencia cabe girada',()=>{const r=sheetYield(609.13,742.18,[1000,700]);assert.equal(r.count,1);assert.equal(r.rotated,true);});
test('el sangrado puede hacer que ya no quepa una caja',()=>{assert.equal(sheetYield(1000,700,[1000,700]).count,0);assert.equal(sheetYield(1000,700,[1000,700],0).count,1);});
test('cambiar medidas recalcula cantidad y admite pliego grande',()=>{assert.equal(sheetYield(194,194,[1000,700]).count,15);assert.equal(sheetYield(94,94,[1000,700]).count,70);assert.equal(sheetYield(194,94,[1200,2300]).count,138);});
test('rechaza medidas inválidas y mantiene exactitud decimal',()=>{assert.throws(()=>sheetYield(0,20,[1000,700]));assert.throws(()=>sheetYield(NaN,20,[1000,700]));assert.equal(sheetYield(94.1,94,[1001,700]).count,70);});
