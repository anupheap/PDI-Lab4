// Render the actual source files and recorded stdout, then take browser screenshots.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'output', 'report');
const evidence = JSON.parse(fs.readFileSync(path.join(output, 'evidence', 'runs.json'), 'utf8'));
const shots = path.join(output, 'screenshots');
fs.mkdirSync(shots, { recursive: true });
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

function chunks(lines, maximum = 36) {
  const count = Math.ceil(lines.length / maximum);
  const size = Math.ceil(lines.length / count);
  return Array.from({ length: count }, (_, i) => lines.slice(i * size, (i + 1) * size));
}

function outputChunks(lines, maximum = 36) {
  const result = [];
  let remaining = lines;
  while (remaining.length > maximum) {
    const target = Math.ceil(remaining.length / Math.ceil(remaining.length / maximum));
    const breaks = Array.from({ length: maximum }, (_, i) => i + 1)
      .filter(i => i >= Math.floor(target / 2) && remaining[i - 1] === '');
    const boundary = breaks.sort((a, b) => Math.abs(a - target) - Math.abs(b - target))[0] || target;
    result.push(remaining.slice(0, boundary));
    remaining = remaining.slice(boundary);
  }
  result.push(remaining);
  return result;
}

(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  const page = await browser.newPage({ viewport: { width: 1680, height: 1300 }, deviceScaleFactor: 1 });
  const manifest = [];
  async function screenshot(run, kind, lines, subtitle, start = 1, part = 1, count = 1) {
    const file = `${run.class}-${kind}-${part}.png`;
    const content = lines.map((line, i) => kind === 'source'
      ? `<div class="line"><span class="number">${start + i}</span><span>${escape(line) || ' '}</span></div>`
      : `<div class="line">${escape(line) || ' '}</div>`).join('');
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>
      *{box-sizing:border-box}body{margin:0;background:#eef2f6;color:#142434;font-family:Segoe UI,Arial,sans-serif}
      .capture{width:1660px;padding:24px;background:#eef2f6}.bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
      .brand{color:#126575;font-size:19px;font-weight:700;letter-spacing:3px}.label{font-size:20px;color:#52677a}
      .window{background:${kind === 'source' ? '#ffffff' : '#142434'};border:1px solid #c9d4df;border-radius:12px;overflow:hidden}
      .window-head{padding:15px 22px;background:${kind === 'source' ? '#e1e9f0' : '#22374a'};color:${kind === 'source' ? '#23384c' : '#dce8f2'};font-size:21px;font-weight:600}
      .code{padding:18px 20px;font:22px/28px Consolas,'Courier New',monospace;color:${kind === 'source' ? '#192c3d' : '#eef6fd'}}
      .line{display:flex;white-space:pre-wrap;overflow-wrap:anywhere;min-height:28px}.number{flex:0 0 54px;margin-right:22px;text-align:right;color:#748b9e;user-select:none}
    </style></head><body><main class="capture"><div class="bar"><div class="brand">PDI / LAB 04</div><div class="label">${kind === 'source' ? 'JAVA SOURCE' : 'CAPTURED CONSOLE OUTPUT'}</div></div>
    <section class="window"><div class="window-head">${escape(subtitle)}</div><div class="code">${content}</div></section></main></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.locator('.capture').screenshot({ path: path.join(shots, file) });
    manifest.push({ file: `output/report/screenshots/${file}`, title: run.title,
      description: run.description, kind, subtitle, part, count, source: run.source });
  }
  for (const run of evidence.runs) {
    const source = fs.readFileSync(path.join(root, run.source), 'utf8').trimEnd().split(/\r?\n/);
    const sourceChunks = chunks(source);
    let start = 1;
    for (let i = 0; i < sourceChunks.length; i++) {
      const lines = sourceChunks[i];
      await screenshot(run, 'source', lines, `${run.source} | lines ${start}-${start + lines.length - 1}`, start, i + 1, sourceChunks.length);
      start += lines.length;
    }
    const inputLabel = run.class === 'Exercise2' ? 'INPUT' : 'INPUT (fictional demonstration students)';
    const transcript = [`$ ${run.command}`, '', ...(run.stdin ? [inputLabel, ...run.stdin.trimEnd().split('\n'), ''] : []),
      'CAPTURED STDOUT', ...run.stdout.trimEnd().split('\n')];
    const transcriptChunks = outputChunks(transcript);
    for (let i = 0; i < transcriptChunks.length; i++) {
      await screenshot(run, 'output', transcriptChunks[i], `${run.class} | successful run${transcriptChunks.length > 1 ? ` | part ${i + 1}/${transcriptChunks.length}` : ''}`, 1, i + 1, transcriptChunks.length);
    }
  }
  await screenshot({ class: 'Verification', title: 'Verification - integration checks',
    description: 'Independent checks compare Java output with Python CSV calculations.', source: 'tests/verify.py' },
    'output', evidence.verification.trimEnd().split('\n'), 'python tests/verify.py | all checks passed');
  fs.writeFileSync(path.join(output, 'screenshots.json'), JSON.stringify(manifest, null, 2) + '\n');
  await browser.close();
  console.log(`Captured ${manifest.length} browser screenshots of source and recorded output.`);
})().catch(error => { console.error(error); process.exit(1); });
