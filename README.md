# Sito Studio Legale Pernorio

Sorgente del sito https://studiolegalepernorio.com (Netlify, progetto `studiolegalepernorio`).

- `src/`: pagine originali, importate dal deploy del 29/10/2026
- `static/fonts/`: font ospitati in locale (prima venivano caricati da Google Fonts)
- `tools/contenuti.py`: testi delle pagine nuove (comuni, costi, gratuito patrocinio, strumenti)
- `tools/build.py`: applica le correzioni SEO e genera il sito in `dist/`
- `tools/agenti.py`: strumenti WebMCP, versioni Markdown, grafo delle entità, robots.txt per gli assistenti IA
- `tools/audit.py`: audit SEO, GEO e agenti IA di `dist/`, scrive `AUDIT.md` (lanciarlo dopo ogni build)
- `tools/indexnow.py`: avvisa Bing e IndexNow degli URL, solo dopo la pubblicazione
- `netlify/`: `_redirects` e `_headers`
- `RICERCA-STRUMENTI.md`: ricerca sugli strumenti open source e prossimi passi

## Build e pubblicazione

```
python3 tools/build.py          # genera dist/
python3 tools/audit.py          # controlla dist/ e scrive AUDIT.md
netlify deploy --dir dist --prod   # pubblica (oppure trascina dist/ su app.netlify.com)
python3 tools/indexnow.py       # dopo la pubblicazione
```

Le modifiche future vanno fatte qui, in `src/` o `tools/`, e poi ricostruite: un deploy fatto da un'altra copia del sito cancellerebbe queste migliorie.
