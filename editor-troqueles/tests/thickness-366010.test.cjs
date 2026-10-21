/* Valida el eje de espesor 1,5–2,5 mm de 366010. */
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const repo = path.resolve(root, '..');
const E = require(path.join(root, 'dist/engines.js'));
const M = require(path.join(root, 'dist/materials.js'));
const model = JSON.parse(fs.readFileSync(path.join(root, 'dist/assets/modelos.json'))).find(m => m.id === '366010');
const cap = JSON.parse(fs.readFileSync(path.join(root, 'dist/assets/capacidades-materiales.json')))['366010'];
const material = JSON.parse(fs.readFileSync(path.join(root, 'dist/assets/materiales.json'))).materials.find(m => m.id === 366010);

function flat(o, p = '', out = {}) {
  if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) {
    if (k === 'thickness') continue;
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

assert.deepStrictEqual(M.thicknesses(cap, material), [1.5, 1.75, 2, 2.25, 2.5]);
for (const t of [1.5, 1.75, 2, 2.25, 2.5]) {
  assert.ok(M.profile(cap, { materialId: 366010, thickness: t }), `profile ${t}`);
}
assert.strictEqual(M.profile(cap, { materialId: 366010, thickness: 3 }), null);

let max = 0, worst = null, count = 0;
const dir = path.join(repo, 'geometria/modelos/366010/espesor');
for (const file of fs.readdirSync(dir)) {
  if (!file.endsWith('.json') || file === 'manifest.json') continue;
  const data = JSON.parse(fs.readFileSync(path.join(dir, file))).data;
  const dims = { L: data.knifeSize.L, W: data.knifeSize.W, H: data.knifeSize.H };
  const thickness = data.layer['BoutiqueboxDivideEquallyCoverBottomGreyboard'].thickness;
  const pieces = E.rigid366010Pieces(model, dims, { materialId: 366010, thickness });
  for (const piece of pieces) {
    const actual = flat(piece.layer);
    const expected = flat(data.layer[layers[piece.id]]);
    for (const key of Object.keys(expected)) {
      if (actual[key] === undefined) continue;
      const error = Math.abs(actual[key] - expected[key]);
      if (error > max) { max = error; worst = [file, piece.id, key, actual[key], expected[key]]; }
    }
  }
  count++;
}
assert.ok(count >= 17, `muestras ${count}`);
assert.ok(max < 0.02, `error ${max} ${JSON.stringify(worst)}`);
for (const t of [1.5, 2.5]) {
  const layer = E.rigid366010(model, { L: 180, W: 100, H: 40 }, { materialId: 366010, thickness: t });
  assert.strictEqual(layer.thickness, t);
  assert.strictEqual(layer.bleedCuts.length, 172);
}
assert.throws(() => E.rigid366010(model, { L: 180, W: 100, H: 40 }, { materialId: 366010, thickness: 3 }), /espesor/i);
console.log(`366010 espesor OK · ${count} muestras · error ${max.toFixed(4)} mm · 1,5–2,5 mm`);
