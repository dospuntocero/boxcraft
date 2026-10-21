/* Valida el motor paramétrico L/W/H de 366010 en sus dos regímenes. */
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const E = require(path.join(root, 'dist/engines.js'));
const model = JSON.parse(fs.readFileSync(path.join(root, 'dist/assets/modelos.json'))).find(m => m.id === '366010');
const sampleDir = path.resolve(root, '..', 'geometria/modelos/366010/parametricas');

function flat(o, p = '', out = {}) {
  if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) {
    if (typeof v === 'number') out[p + '/' + k] = v;
    else if (v && typeof v === 'object') flat(v, p + '/' + k, out);
  }
  return out;
}

const layers = {
  'fondo-gris': 'BoutiqueboxDivideEquallyCoverBottomGreyboard',
  'fondo-papel': 'BoutiqueboxDivideEquallyCoverBottomFacepaper',
  'tapa-gris': 'BoutiqueboxDivideEquallyCoverTopGreyboard',
  'tapa-papel': 'BoutiqueboxDivideEquallyCoverTopFacepaper',
};

assert.strictEqual(model.engine, 'rigid366010');
assert.ok(model.rule && model.rule.regimes.length === 2);
assert.deepStrictEqual(model.bounds, { L: [160, 220], W: [80, 140], H: [30, 70] });

let max = 0, worst = null, count = 0;
for (const file of fs.readdirSync(sampleDir)) {
  if (!file.endsWith('.json') || file === 'manifest.json') continue;
  const data = JSON.parse(fs.readFileSync(path.join(sampleDir, file))).data;
  const dims = { L: data.knifeSize.L, W: data.knifeSize.W, H: data.knifeSize.H };
  if (dims.L < 160 || dims.L > 220 || dims.W < 80 || dims.W > 140 || dims.H < 30 || dims.H > 70) continue;
  count++;
  const pieces = E.rigid366010Pieces(model, dims);
  assert.strictEqual(pieces.length, 4, file);
  for (const piece of pieces) {
    const actual = flat(piece.layer);
    const expected = flat(data.layer[layers[piece.id]]);
    for (const key of Object.keys(expected)) {
      if (actual[key] === undefined) continue;
      const error = Math.abs(actual[key] - expected[key]);
      if (error > max) { max = error; worst = [file, piece.id, key, actual[key], expected[key]]; }
    }
  }
}
assert.ok(count >= 40, `muestras ${count}`);
assert.ok(max < 0.02, `error ${max} ${JSON.stringify(worst)}`);

const base = E.rigid366010(model, { L: 180, W: 100, H: 40 });
assert.strictEqual(base.faces.length, 60);
assert.strictEqual(base.folds.length, 56);
assert.strictEqual(base.cuts.length, 216);
assert.strictEqual(base.bleedCuts.length, 172);
assert.strictEqual(base.bleedFaces.length, 50);
assert.strictEqual(base.pieceLabels.length, 4);
assert.strictEqual(base.totalX, 605.5500000000001);
assert.strictEqual(base.totalY, 476.70000000000005);

// El régimen B cambia la profundidad exterior con H: L=200,H=30 (15 mm)
// frente a L=200,H=40 (20 mm). Ambas configuraciones están capturadas.
const h30 = E.rigid366010Pieces(model, { L: 200, W: 100, H: 30 }).find(p => p.id === 'fondo-papel').layer;
const h40 = E.rigid366010Pieces(model, { L: 200, W: 100, H: 40 }).find(p => p.id === 'fondo-papel').layer;
assert.ok(h40.totalX > h30.totalX + 9, 'outer B');
assert.ok(Math.abs(h30.totalX - 300.95) < 1e-9);
assert.ok(Math.abs(h40.totalX - 330.95) < 1e-9);

assert.throws(() => E.generate(model, { L: 230, W: 100, H: 40 }), /Longitud/);
assert.throws(() => E.generate(model, { L: 180, W: 150, H: 40 }), /Anchura/);
assert.throws(() => E.generate(model, { L: 180, W: 100, H: 20 }), /Altura/);
console.log(`366010 OK · ${count} muestras · error paramétrico ${max.toFixed(4)} mm · A/B`);
