# Sito Studio Legale Pernorio

Sorgente del sito https://studiolegalepernorio.com (Netlify, progetto `studiolegalepernorio`).

- `src/`: pagine originali, importate dal deploy del 29/10/2026
- `static/fonts/`: font ospitati in locale (prima venivano caricati da Google Fonts)
- `tools/contenuti.py`: testi delle pagine nuove (comuni, costi, gratuito patrocinio, strumenti)
- `tools/build.py`: applica le correzioni SEO e genera il sito in `dist/`
- `tools/agenti.py`: strumenti WebMCP, versioni Markdown, grafo delle entità, robots.txt per gli assistenti IA
- `tools/cerca.py`: ricerca sul testo completo, uguale per persone e IA. Indice dei passaggi (`/cerca-testo.json`), motore (`/cerca.js`), pagina `/cerca`, API `/api/cerca?q=` (funzione `functions/cerca.mjs`, generata), `openapi.json`, `opensearch.xml`. Sinonimi del linguaggio comune in `SINONIMI`
- `tools/prova_cerca.mjs`: 30 domande da cliente con la pagina attesa (`node tools/prova_cerca.mjs -v`); la lancia anche l'audit
- `netlify/edge-functions/markdown.js`: chi chiede una pagina con `Accept: text/markdown` riceve la versione Markdown
- `tools/audit.py`: audit SEO, GEO e agenti IA di `dist/`, scrive `AUDIT.md` (lanciarlo dopo ogni build)
- `tools/indexnow.py`: avvisa Bing e IndexNow degli URL, solo dopo la pubblicazione
- `tools/fonti.py`: fonti normative delle guide con link Normattiva (`python3 tools/fonti.py --verifica` controlla i link)
- `tools/visibilita_ia.py`: misura se ChatGPT, Gemini, Perplexity e Claude citano lo Studio (servono le chiavi API)
- `functions/mcp.mjs`: server MCP generato dalla build (non modificarlo a mano)
- `tools/immagini_og.mjs`: immagini di anteprima 1200x630 per ogni pagina (`node tools/immagini_og.mjs` dopo la build, scrive `static/og/`)
- `tools/social.mjs`: caroselli Instagram e piano editoriale (`social/`)
- `tools/ricerche.py`: sezioni, FAQ e title scritti sulle ricerche reali di Search Console; testi del riquadro "Il suo caso" nelle guide
- `tools/misura/`: misura senza cookie (provenienza delle visite, clic su Chiama/WhatsApp, visite dalle IA). Script `conta.js`, funzione `/api/conta` e `/api/statistiche` (Netlify Blobs), pagina riservata `/statistiche#k=CHIAVE`. In `chiave.sha256` c'è solo l'impronta della chiave, non la chiave
- `netlify/edge-functions/bot-ia.js`: conta le letture dei bot delle IA (gira solo per i loro user-agent)
- `dati/`: misure di visibilità nelle IA
- `ELENCHI.md`: dati identici da usare su Google, Bing, Apple, OpenStreetMap e negli elenchi
- `netlify/`: `_redirects` e `_headers`
- `RICERCA-STRUMENTI.md`: ricerca sugli strumenti open source e prossimi passi

## Build e pubblicazione

```
npm install                     # una volta: dipendenze delle funzioni (@netlify/blobs)
python3 tools/build.py          # genera dist/ e functions/
python3 tools/audit.py          # controlla dist/ e scrive AUDIT.md
netlify deploy --prod           # dalla radice: usa netlify.toml (dist, functions, edge functions). Il trascinamento di dist/ pubblica solo il sito, senza /mcp né misura
python3 tools/indexnow.py       # dopo la pubblicazione
```

Le modifiche future vanno fatte qui, in `src/` o `tools/`, e poi ricostruite: un deploy fatto da un'altra copia del sito cancellerebbe queste migliorie.
