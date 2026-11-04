const fs = require('node:fs');
const crypto = require('node:crypto');
const os = require('node:os');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const extensions = path.join(os.homedir(), '.vscode', 'extensions');
const extensionPath = process.env.CODESNAP_EXTENSION_PATH || fs.readdirSync(extensions)
  .filter(name => name.startsWith('local-tools.codesnap-rs-local-')).sort().reverse()
  .map(name => path.join(extensions, name))[0];
if (!extensionPath) throw new Error('Install anupheap/codesnap-rs-vscode in VS Code first.');
const metadata = JSON.parse(fs.readFileSync(path.join(extensionPath, 'package.json'), 'utf8'));
if (metadata.repository?.url !== 'https://github.com/anupheap/codesnap-rs-vscode.git') {
  throw new Error('Expected the adapter from anupheap/codesnap-rs-vscode.');
}
const { render, normalizeCode } = require(path.join(extensionPath, 'renderer.js'));
const directory = path.join(root, 'output', 'report', 'codesnap');
fs.mkdirSync(directory, { recursive: true });
(async () => {
  const manifest = { extension: `${metadata.publisher}.${metadata.name}@${metadata.version}`,
    repository: metadata.repository.url, images: [] };
  for (const filename of fs.readdirSync(path.join(root, 'src')).filter(name => name.endsWith('.java')).sort()) {
    const source = fs.readFileSync(path.join(root, 'src', filename));
    const code = normalizeCode(source.toString('utf8'), 4);
    const png = await render(extensionPath, { code, filename, copy: false, scale: 2,
      theme: 'candy', background: '#abb8c3', windowControls: true,
      lineNumbers: true, startLine: 1, title: filename });
    const output = filename.replace('.java', '.png');
    fs.writeFileSync(path.join(directory, output), png);
    manifest.images.push({ source: `src/${filename}`, image: `output/report/codesnap/${output}`,
      source_sha256: crypto.createHash('sha256').update(source).digest('hex') });
    console.log(`CodeSnap RS: ${filename}`);
  }
  fs.writeFileSync(path.join(directory, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
})().catch(error => { console.error(error); process.exitCode = 1; });
