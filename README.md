# Sito Studio Legale Pernorio

Sorgente del sito https://studiolegalepernorio.com (Netlify, progetto `studiolegalepernorio`).

- `src/`: pagine originali, importate dal deploy del 29/10/2026
- `static/fonts/`: font ospitati in locale (prima venivano caricati da Google Fonts)
- `tools/contenuti.py`: testi delle pagine nuove (comuni, costi, gratuito patrocinio, strumenti)
- `tools/build.py`: applica le correzioni SEO e genera il sito in `dist/`
- `netlify/`: `_redirects` e `_headers`

## Build e pubblicazione

```
python3 tools/build.py          # genera dist/
netlify deploy --dir dist --prod   # pubblica (oppure trascina dist/ su app.netlify.com)
```

Le modifiche future vanno fatte qui, in `src/` o `tools/`, e poi ricostruite: un deploy fatto da un'altra copia del sito cancellerebbe queste migliorie.
