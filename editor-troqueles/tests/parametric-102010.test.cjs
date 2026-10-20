/* Valida la reconstrucción afín L/W/H de 102010 en la topología de 80 cortes. */
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const E = require(path.join(root, 'dist/engines.js'));
const model = JSON.parse(fs.readFileSync(path.join(root, 'dist/assets/modelos.json'))).find(m => m.id === '102010');
const samples = ['knife-00', 'knife-03', 'knife-04', 'knife-05', 'knife-06', 'knife-07'];

function flat(o, p = '', out = {}) {
  if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) {
    if (typeof v === 'number') out[p + '/' + k] = v;
    else if (v && typeof v === 'object') flat(v, p + '/' + k, out);
  }
  return out;
}

assert.strictEqual(model.engine, 'affine');
assert.ok(model.rule && model.rule.rules);
let max = 0;
for (const name of samples) {
  const data = JSON.parse(fs.readFileSync(path.resolve(root, '..', 'geometria/modelos/102010/muestras', name + '.json'))).data;
  const dims = { L: data.knifeSize.L, W: data.knifeSize.W, H: data.knifeSize.H };
  const actual = flat(E.generate(model, dims));
  const expected = flat(data.layer.traditional);
  for (const key of Object.keys(expected)) {
    if (actual[key] === undefined) continue;
    max = Math.max(max, Math.abs(actual[key] - expected[key]));
  }
}
assert.ok(max < 1.9, `error afín ${max}`);
const base = E.generate(model, { L: 120.6, W: 60.6, H: 161.1 });
const original = flat(JSON.parse(fs.readFileSync(path.resolve(root, '..', 'geometria/modelos/102010/muestras/knife-00.json'))).data.layer.traditional);
for (const [k, v] of Object.entries(flat(base))) assert.ok(Math.abs(v - original[k]) < 1e-9, `base ${k}`);
assert.throws(() => E.generate(model, { L: 140, W: 60.6, H: 161.1 }), /L ≤ 2W/);
const lb = E.fieldBounds(model, { L: 120.6, W: 60.6, H: 161.1 }, 'L');
assert.ok(lb[1] <= 2 * 60.6 + 0.01, `L bound ${lb}`);
console.log(`102010 OK · ${samples.length} muestras · error afín ${max.toFixed(4)} mm · L≤2W`);
