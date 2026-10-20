/* Valida el motor 187000 contra los cortes y caras capturados del editor. */
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const E = require(path.join(root, 'dist', 'engines.js'));
const data = JSON.parse(fs.readFileSync(path.resolve(root, '..', 'geometria', 'modelos', '187000', 'muestras.json'), 'utf8'));

function parse(d) {
  const toks = d.match(/[MLAZ]|-?\d+(?:\.\d+)?(?:e[+-]?\d+)?/g) || [];
  let i = 0;
  const out = [];
  while (i < toks.length) {
    const t = toks[i];
    const n = { M: 2, L: 2, A: 7, Z: 0 }[t];
    out.push([t, toks.slice(i + 1, i + 1 + n).map(Number)]);
    i += 1 + n;
  }
  return out;
}

function compare(expected, generated, label, allowTrailingClose = false) {
  let ei = 0, gi = 0, max = 0;
  while (ei < expected.length || gi < generated.length) {
    while (ei < expected.length && expected[ei][0] === 'Z') ei++;
    while (gi < generated.length && generated[gi].mtd === 'Z') gi++;
    if (ei >= expected.length || gi >= generated.length) break;
    const [t, a] = expected[ei], g = generated[gi];
    if (t !== g.mtd) {
      if (allowTrailingClose && t === 'L' && ei === expected.length - 1) break;
      throw new Error(`${label}: comando ${t} != ${g.mtd} (${ei}/${gi})`);
    }
    if (t === 'A') {
      max = Math.max(max, Math.abs(a[0] - g.rx), Math.abs(a[1] - g.ry), Math.abs(a[5] - g.x), Math.abs(a[6] - g.y), Math.abs(a[4] - g.dir));
    } else if (t === 'M' || t === 'L') {
      max = Math.max(max, Math.abs(a[0] - g.x), Math.abs(a[1] - g.y));
    }
    ei++; gi++;
  }
  return max;
}

let maxCut = 0, maxFace = 0;
for (const sample of data.samples) {
  const { L, W, H } = sample.dims;
  const layer = E.pillow187000({ L, W, H });
  assert.ok(Math.abs(layer.totalX - (L + H)) < 1e-9, `${sample.label}: totalX`);
  assert.ok(Math.abs(layer.totalY - ((W >= 100 ? 18 : 15) + 2 * W)) < 1e-9, `${sample.label}: totalY`);
  maxCut = Math.max(maxCut, compare(parse(sample.cut), layer.cuts, `${sample.label} corte`));
  for (const face of layer.faces) {
    const expected = sample.faces[face.name];
    assert.ok(expected, `${sample.label}: falta cara ${face.name}`);
    maxFace = Math.max(maxFace, compare(parse(expected), face.dlist, `${sample.label} ${face.name}`, true));
  }
}
assert.ok(maxCut < 1e-3, `error de corte ${maxCut}`);
assert.ok(maxFace < 1e-3, `error de caras ${maxFace}`);
assert.strictEqual(E.sheetFit(143, 155, [330, 480]), 'direct');
assert.strictEqual(E.sheetFit(185, 155, [330, 480]), 'direct');
assert.strictEqual(E.sheetFit(480, 323.33, [330, 480]), 'rotated');
console.log(`187000 OK · ${data.samples.length} muestras · corte ${maxCut.toExponential(2)} mm · caras ${maxFace.toExponential(2)} mm`);
