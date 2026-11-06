# Sito Studio Legale Pernorio

Sorgente del sito https://studiolegalepernorio.com (Netlify, progetto `studiolegalepernorio`).

- `src/`: pagine originali, importate dal deploy del 29/10/2026
- `static/fonts/`: font ospitati in locale (prima venivano caricati da Google Fonts)
- `tools/contenuti.py`: testi delle pagine nuove (comuni, costi, gratuito patrocinio, strumenti)
- `tools/build.py`: applica le correzioni SEO e genera il sito in `dist/`
- `tools/agenti.py`: strumenti WebMCP, versioni Markdown, grafo delle entità, robots.txt per gli assistenti IA
- `tools/audit.py`: audit SEO, GEO e agenti IA di `dist/`, scrive `AUDIT.md` (lanciarlo dopo ogni build)
- `tools/indexnow.py`: avvisa Bing e IndexNow degli URL, solo dopo la pubblicazione
- `tools/fonti.py`: fonti normative delle guide con link Normattiva (`python3 tools/fonti.py --verifica` controlla i link)
- `tools/visibilita_ia.py`: misura se ChatGPT, Gemini, Perplexity e Claude citano lo Studio (servono le chiavi API)
- `functions/mcp.mjs`: server MCP generato dalla build (non modificarlo a mano)
- `ELENCHI.md`: dati identici da usare su Google, Bing, Apple, OpenStreetMap e negli elenchi
- `netlify/`: `_redirects` e `_headers`
- `RICERCA-STRUMENTI.md`: ricerca sugli strumenti open source e prossimi passi

## Build e pubblicazione

```
python3 tools/build.py          # genera dist/
python3 tools/audit.py          # controlla dist/ e scrive AUDIT.md
netlify deploy --dir dist --functions functions --prod   # pubblica sito + server MCP (il trascinamento di dist/ pubblica solo il sito, senza /mcp)
python3 tools/indexnow.py       # dopo la pubblicazione
```

Le modifiche future vanno fatte qui, in `src/` o `tools/`, e poi ricostruite: un deploy fatto da un'altra copia del sito cancellerebbe queste migliorie.
