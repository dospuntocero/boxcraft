#!/usr/bin/env node
/* Captura respuestas /project/knife de Pacdora para una matriz L/W/H.
   Uso: node capturar-playwright.cjs --plan plan.json --out dir
   El plan: {url, materialId?, thickness?, configs:[{L,W,H}], waitMs?}
*/
const fs = require('fs');
const path = require('path');
const { chromium } = require('/Users/fran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i += 2) out[argv[i].replace(/^--/, '')] = argv[i + 1];
  return out;
}
const args = parseArgs(process.argv);
if (!args.plan || !args.out) {
  console.error('Uso: node capturar-playwright.cjs --plan plan.json --out dir');
  process.exit(2);
}
const plan = JSON.parse(fs.readFileSync(args.plan, 'utf8'));
const axes = plan.axes || ['L', 'W', 'H'];
const outDir = path.resolve(args.out);
fs.mkdirSync(outDir, { recursive: true });
const executablePath = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

function sameDims(a, b, axes) {
  return a && b && axes.every(k => Math.abs(Number(a[k]) - Number(b[k])) < 1e-7);
}

(async () => {
  const browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const responses = [];
  page.on('response', async response => {
    if (!response.url().includes('/project/knife')) return;
    try {
      const json = await response.json();
      responses.push({ url: response.url(), status: response.status(), json });
    } catch (error) {
      responses.push({ url: response.url(), status: response.status(), error: String(error) });
    }
  });
  const report = [];
  try {
    await page.goto(plan.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(plan.loadMs || 3500);
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(500);
    await page.locator('[gtm="ga-dieline_dieline_basic_mm"]').click({ timeout: 8000, force: true }).catch(() => {});
    await page.waitForTimeout(500);
    for (let i = 0; i < plan.configs.length; i++) {
      const config = plan.configs[i];
      responses.length = 0;
      for (const [index, axis] of axes.map((axis, i) => [i + 1, axis])) {
        const input = page.locator(`.proper-content > .proper-item:nth-child(${index}) input`);
        await input.click({ timeout: 8000, force: true }).catch(() => {});
        await input.fill(String(config[axis]), { timeout: 8000 });
        await input.press('Enter', { timeout: 8000 });
        await page.waitForTimeout(plan.stepMs || 700);
      }
      await page.waitForTimeout(plan.waitMs || 1500);
      const match = [...responses].reverse().find(item => item.json && item.json.data && sameDims(item.json.data.knifeSize, config, axes));
      if (!match) {
        report.push({ config, saved: false, seen: responses.map(r => r.json && r.json.data && r.json.data.knifeSize) });
        continue;
      }
      const data = match.json.data;
      const fileName = `${String(i).padStart(3, '0')}-L${config.L}-W${config.W}-H${config.H}.json`;
      fs.writeFileSync(path.join(outDir, fileName), JSON.stringify(match.json));
      report.push({
        config,
        saved: true,
        file: fileName,
        url: match.url,
        knifeSize: data.knifeSize,
        science: data.science && data.science.id,
        thickness: data.layer && data.layer.traditional && data.layer.traditional.thickness,
        openParams: data.openParams ? data.openParams.flat().length : 0
      });
    }
    fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ url: plan.url, date: new Date().toISOString(), materialId: plan.materialId, thickness: plan.thickness, report }, null, 2));
    const saved = report.filter(r => r.saved).length;
    console.log(`${saved}/${plan.configs.length} respuestas guardadas en ${outDir}`);
    if (saved !== plan.configs.length) process.exitCode = 1;
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
