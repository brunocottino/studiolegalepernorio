// Contenuti social pronti: caroselli Instagram 1080x1350 dalle guide (copertina, 3 domande, chiusura)
// e piano editoriale con didascalie e post per la scheda Google.
// Uso: node tools/social.mjs   (scrive social/instagram/<guida>/ e social/PIANO-SOCIAL.md)
import { createRequire } from 'module';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url'; import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const G = JSON.parse(execSync(`python3 -c "import sys,json;sys.path.insert(0,'tools');import guide_nuove as G;print(json.dumps([{k:g[k] for k in ('slug','cat','titolo','sommario','faq')} for g in G.GUIDE if g['slug']!='guida-domiciliazioni-tribunale-pavia'],ensure_ascii=False))"`, { cwd: ROOT }).toString());
const font = f => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'static/fonts', f)).toString('base64');
const foto = 'data:image/webp;base64,' + fs.readFileSync(path.join(ROOT, 'src/img/ritratto-viso-900.webp')).toString('base64');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const CSS = `@font-face{font-family:C;src:url(${font('cormorant-garamond-2fed1d1b-latin.woff2')})}
@font-face{font-family:I;src:url(${font('inter-56724408-latin.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;font-family:I;color:#1B1D1C;background:#F5F3EE;display:flex;flex-direction:column;padding:96px 88px 80px}
.k{margin-top:auto;font-size:26px;letter-spacing:.22em;text-transform:uppercase;color:#9E8459}
h1{font-family:C;font-weight:500;font-size:104px;line-height:1.02;margin-top:40px;letter-spacing:-.01em}
h2{font-family:C;font-weight:500;font-size:76px;line-height:1.05;margin-top:36px}
p{font-size:38px;line-height:1.45;color:#2b2f2d;margin-top:44px}
.f{margin-top:auto;display:flex;align-items:center;justify-content:space-between;color:#5B605C;font-size:26px}
.m{font-family:C;font-size:40px;letter-spacing:.32em;color:#1B1D1C}.n{font-size:26px;color:#9E8459}
body.dark{background:#1F3A2E;color:#F1EEE7}body.dark p,body.dark .f{color:#d9d4c8}body.dark .m{color:#F1EEE7}
.ph{width:300px;height:300px;border-radius:50%;background:url(${foto}) center 20%/cover;margin-top:56px}`;
const slide = (body, n, tot, cls = '') => `<!doctype html><html><head><style>${CSS}</style></head><body class="${cls}">${body}<div class="f"><span class="m">PERNORIO</span><span class="n">${n} / ${tot}</span></div></body></html>`;
const b = await pw.chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
let md = '# Piano social: Instagram e scheda Google\n\nUn carosello Instagram e un post Google alla settimana, dalle guide del sito. Immagini in `social/instagram/<guida>/` (formato 4:5, 1080x1350). Per il post Google si usa l\'immagine `static/og/<guida>.jpg`.\n\nTono sempre informativo (art. 17 e 35 del Codice deontologico forense): niente superlativi, promesse di risultato o riferimenti a clienti.\n\n';
const start = new Date(Date.UTC(2026, 10, 9));
for (const [i, g] of G.entries()) {
  const dir = path.join(ROOT, 'social', 'instagram', g.slug.replace('guida-', '')); fs.mkdirSync(dir, { recursive: true });
  const tot = 2 + g.faq.length;
  const pages = [slide(`<div class="k">${esc(g.cat)} · Guida pratica</div><h1>${esc(g.titolo)}</h1><p>${esc(g.sommario)}</p>`, 1, tot)];
  g.faq.forEach(([q, a], j) => pages.push(slide(`<div class="k">Domanda ${j + 1}</div><h2>${esc(q)}</h2><p>${esc(a)}</p>`, j + 2, tot)));
  pages.push(slide(`<div class="k">Approfondisci</div><h2>La guida completa è sul sito</h2><p>studiolegalepernorio.com<br>Link in bio · Via Egidio Sacchetti 14, Vigevano<br>Tel. 0381 386276</p><div class="ph"></div>`, tot, tot, 'dark'));
  for (const [k, h] of pages.entries()) { await pg.setContent(h); await pg.evaluate(() => document.fonts.ready); await pg.screenshot({ path: path.join(dir, `${k + 1}.jpg`), type: 'jpeg', quality: 85 }); }
  const d = new Date(start.getTime() + i * 7 * 864e5).toISOString().slice(0, 10);
  const url = `https://studiolegalepernorio.com/${g.slug}`;
  md += `## ${d} · ${g.titolo}\n\n**Instagram** (carosello \`social/instagram/${g.slug.replace('guida-', '')}/\`, ${tot} immagini)\n\n> ${g.sommario}\n>\n> ${g.faq.map(([q]) => '▸ ' + q).join('\n> ')}\n>\n> Le risposte sono nelle immagini; la guida completa è sul sito (link in bio).\n> Studio Legale Pernorio · Avv. Daniela Pernorio · Vigevano\n>\n> #Vigevano #Lomellina #Pavia #avvocato #dirittocivile #${g.cat.toLowerCase().replace(/[^a-zà-ù]/g, '')} #studiolegale\n\n**Post Google** (aggiornamento con pulsante "Scopri di più" → ${url})\n\n> ${g.titolo}. ${g.sommario} ${g.faq[0][0]} ${g.faq[0][1]} La guida completa è sul sito dello Studio.\n\n`;
}
await b.close();
fs.writeFileSync(path.join(ROOT, 'social', 'PIANO-SOCIAL.md'), md);
console.log(`${G.length} caroselli e piano in social/`);
