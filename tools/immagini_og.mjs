// Genera un'immagine di anteprima 1200x630 per ogni pagina (WhatsApp, Facebook, LinkedIn, X).
// Uso: python3 tools/build.py && node tools/immagini_og.mjs   (scrive static/og/<pagina>.jpg)
import { createRequire } from 'module';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright'); }
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const DIST = path.join(ROOT, 'dist'), OUT = path.join(ROOT, 'static', 'og');
fs.mkdirSync(OUT, { recursive: true });
const font = f => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'static/fonts', f)).toString('base64');
const foto = 'data:image/webp;base64,' + fs.readFileSync(path.join(DIST, 'img/ritratto-viso-900.webp')).toString('base64');
const dec = s => s.replace(/<[^>]+>/g, '').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ').trim();
const pagine = fs.readdirSync(DIST).filter(f => f.endsWith('.html') && !['404.html', 'grazie.html'].includes(f));
const b = await pw.chromium.launch(); const pg = await b.newPage({ viewport: { width: 1200, height: 630 } });
for (const f of pagine) {
  const h = fs.readFileSync(path.join(DIST, f), 'utf8');
  let h1 = dec((h.match(/<h1[^>]*>(.*?)<\/h1>/s) || [, ''])[1].replace(/<span class="h1s">.*?<\/span>/s, ''));
  let label = dec((h.match(/<span class="label">(.*?)<\/span>/s) || [, ''])[1]);
  if (f === 'index.html') { h1 = 'Avvocato a Vigevano'; label = 'Studio Legale Pernorio'; }
  const size = h1.length > 70 ? 54 : h1.length > 45 ? 64 : 76;
  await pg.setContent(`<!doctype html><html><head><style>
@font-face{font-family:C;src:url(${font('cormorant-garamond-2fed1d1b-latin.woff2')})}
@font-face{font-family:I;src:url(${font('inter-56724408-latin.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;display:flex;background:#F5F3EE;font-family:I}
.l{flex:1;padding:64px 56px 52px 72px;display:flex;flex-direction:column}
.k{font-size:20px;letter-spacing:.22em;text-transform:uppercase;color:#9E8459}
h1{font-family:C;font-weight:500;font-size:${size}px;line-height:1.04;color:#1B1D1C;margin-top:26px;letter-spacing:-.01em}
.f{margin-top:auto;display:flex;align-items:center;gap:18px;color:#5B605C;font-size:22px}
.m{font-family:C;font-size:34px;letter-spacing:.32em;color:#1B1D1C}.r{width:40px;height:2px;background:#9E8459}
.p{width:400px;background:#1F3A2E url(${foto}) center 22%/cover}
</style></head><body><div class="l"><div class="k">${label}</div><h1>${h1}</h1>
<div class="f"><span class="m">PERNORIO</span><span class="r"></span><span style="white-space:nowrap">Avv. Daniela Pernorio · Vigevano</span></div></div><div class="p"></div></body></html>`);
  await pg.evaluate(() => document.fonts.ready);
  await pg.screenshot({ path: path.join(OUT, f.replace('.html', '.jpg')), type: 'jpeg', quality: 82 });
}
await b.close();
console.log(`${pagine.length} immagini in static/og/`);
