#!/usr/bin/env node
/* Calcula el sangrado de 3 mm de un conjunto de cortes con ClipperLib. */
const fs = require('fs'), vm = require('vm'), path = require('path');
const clipperPath = process.argv[3] || path.resolve(__dirname, '..', '..', '..', 'editor-troqueles', 'dist', 'clipper.js');
const ctx = vm.createContext({ console, navigator: { userAgent: '' } });
ctx.self = ctx; ctx.window = ctx;
vm.runInContext(fs.readFileSync(clipperPath, 'utf8'), ctx);
const ClipperLib = ctx.ClipperLib;
const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const scale = 10000;

function arcPoints(x0, y0, cmd) {
  let rx = Math.abs(cmd.rx || 0), ry = Math.abs(cmd.ry || 0);
  if (!rx || !ry) return [[cmd.x, cmd.y]];
  const phi = (cmd.ang || 0) * Math.PI / 180;
  const cos = Math.cos(phi), sin = Math.sin(phi);
  const dx = (x0 - cmd.x) / 2, dy = (y0 - cmd.y) / 2;
  const x1 = cos * dx + sin * dy, y1 = -sin * dx + cos * dy;
  let lambda = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry);
  if (lambda > 1) { rx *= Math.sqrt(lambda); ry *= Math.sqrt(lambda); }
  const sign = (cmd.arc ? 1 : 0) === (cmd.dir ? 1 : 0) ? -1 : 1;
  const num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1;
  const den = rx * rx * y1 * y1 + ry * ry * x1 * x1;
  const coef = sign * Math.sqrt(Math.max(0, num / den));
  const cx1 = coef * (rx * y1 / ry), cy1 = coef * (-ry * x1 / rx);
  const cx = cos * cx1 - sin * cy1 + (x0 + cmd.x) / 2;
  const cy = sin * cx1 + cos * cy1 + (y0 + cmd.y) / 2;
  const angle = (ux, uy, vx, vy) => {
    const d = Math.max(-1, Math.min(1, (ux * vx + uy * vy) / (Math.hypot(ux, uy) * Math.hypot(vx, vy))));
    return (ux * vy - uy * vx < 0 ? -1 : 1) * Math.acos(d);
  };
  const theta1 = angle(1, 0, (x1 - cx1) / rx, (y1 - cy1) / ry);
  let delta = angle((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry);
  if (!cmd.dir && delta > 0) delta -= 2 * Math.PI;
  if (cmd.dir && delta < 0) delta += 2 * Math.PI;
  const steps = Math.max(8, Math.ceil(Math.abs(delta) / (Math.PI / 24)));
  const points = [];
  for (let i = 1; i <= steps; i++) {
    const t = theta1 + delta * i / steps;
    points.push([cx + rx * Math.cos(t) * cos - ry * Math.sin(t) * sin,
                 cy + rx * Math.cos(t) * sin + ry * Math.sin(t) * cos]);
  }
  return points;
}

const paths = [];
let points = [], last = null;
function finish() {
  if (points.length > 2) {
    const cleaned = ClipperLib.Clipper.CleanPolygon(points, 2);
    if (cleaned.length > 2) {
      if (!ClipperLib.Clipper.Orientation(cleaned)) cleaned.reverse();
      paths.push(cleaned);
    }
  }
  points = [];
}
function add(x, y) { points.push({ X: Math.round(x * scale), Y: Math.round(y * scale) }); }
for (const cmd of input.cuts || []) {
  if (cmd.mtd === 'M') { finish(); add(cmd.x, cmd.y); last = cmd; }
  else if (cmd.mtd === 'L') { add(cmd.x, cmd.y); last = cmd; }
  else if (cmd.mtd === 'A') {
    for (const [x, y] of arcPoints(last.x, last.y, cmd)) add(x, y);
    last = cmd;
  } else if (cmd.mtd === 'Z') finish();
}
finish();

const union = new ClipperLib.Clipper();
union.AddPaths(paths, ClipperLib.PolyType.ptSubject, true);
const merged = [];
union.Execute(ClipperLib.ClipType.ctUnion, merged, ClipperLib.PolyFillType.pftNonZero, ClipperLib.PolyFillType.pftNonZero);
const outer = merged.filter(p => ClipperLib.Clipper.Orientation(p));
const offset = new ClipperLib.ClipperOffset(2, 0.01 * scale), result = [];
offset.AddPaths(outer, ClipperLib.JoinType.jtRound, ClipperLib.EndType.etClosedPolygon);
offset.Execute(result, 3 * scale);
process.stdout.write(result.map(p => 'M' + p.map(v => `${v.X / scale} ${v.Y / scale}`).join('L') + 'Z').join(''));
