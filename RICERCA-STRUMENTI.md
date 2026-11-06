# Ricerca: strumenti nuovi per farsi trovare (novembre 2026)

Obiettivo: lo Studio deve essere trovato per primo da chi cerca su Google e da chi chiede a ChatGPT, Gemini, Claude, Perplexity o Copilot. Ho cercato su GitHub i progetti più attivi, non solo di studi legali, ne ho studiato il codice e ho portato nel sito le idee migliori. Niente è stato pubblicato su Netlify.

## Cosa ho trovato su GitHub

| Progetto | Cosa fa | Cosa ne abbiamo preso |
|---|---|---|
| webmachinelearning/webmcp (W3C, circa 4.900 stelle) | Standard per far usare il sito agli assistenti IA nel browser. È attivo in Chrome 149 ed Edge 150 (in prova), in ChatGPT Desktop e in Brave. | 5 strumenti che l'assistente può usare sul nostro sito. Nessuno studio legale italiano lo usa ancora. |
| squirrelscan/squirrelscan | Audit con oltre 300 regole, tra cui quelle sulla leggibilità del sito da parte degli agenti IA | Pagine anche in Markdown, un'unica identità dello Studio nei dati strutturati, Content-Signal in robots.txt, controllo del peso in token |
| Auriti-Labs/geo-optimizer-skill | Misura da 0 a 100 quanto un sito viene citato da ChatGPT, Perplexity e Gemini | Elenco aggiornato dei bot IA (27), controlli sulla preparazione per gli AI Overviews di Google e per WebMCP |
| AgriciDaniel/claude-seo (circa 27.000 stelle) | Audit SEO completo, con una parte di SEO locale | "Swap test" contro le pagine dei comuni troppo simili, che Google penalizza; controllo che nome, indirizzo e telefono siano uguali ovunque |
| yaojingang/GEOInflow, elmohq/elmo, GetCito | Monitorano le visite dei bot IA e le citazioni nelle risposte delle IA | Prossimo passo, servono chiavi o un server (vedi sotto) |
| avalonreset/legends-geogrid, local-falcon/mcp | Mostrano la posizione su Google Maps strada per strada (geo-grid) | Prossimo passo, serve una chiave Google |
| nlweb-ai/NLWeb (Microsoft) | Fa rispondere il sito alle domande in linguaggio naturale | Valutato. Per ora basta WebMCP con l'indice di ricerca. |

Installare pacchetti esterni in questa sessione era bloccato dai permessi. Così ho letto il codice e le regole di questi strumenti e le ho riscritte in `tools/audit.py`, che giro io a ogni modifica.

## Cosa è stato aggiunto al sito

1. **Strumenti per gli assistenti IA (WebMCP)**, nel file `/agenti.js` caricato su tutte le pagine. Un assistente che sta guardando il sito può:
   - `informazioni-studio`: leggere indirizzo, telefono, orari, materie, comuni serviti e tribunali;
   - `cerca-nel-sito`: cercare tra guide, competenze, comuni e strumenti;
   - `calcola-quote-eredita`: calcolare le quote di eredità senza testamento;
   - `scadenze-multa`: calcolare le scadenze di una multa;
   - `prepara-richiesta-allo-studio`: precompilare il modulo contatti. Non invia mai nulla da solo: la persona rilegge, accetta la privacy e preme Invia.

   Anche il modulo contatti ha gli attributi WebMCP (`toolname`, `toolparamdescription`), senza invio automatico. È stato provato in Chromium simulando l'agente: tutti e 5 gli strumenti rispondono, il modulo si precompila e non ci sono errori. Sui browser senza WebMCP lo script non fa nulla.
2. **Versione Markdown di ogni pagina** (66 file, ad esempio `/attivita-separazione-divorzio.md` e `/index.md`). Ognuna è segnalata nella pagina con `<link rel="alternate" type="text/markdown">`. Gli assistenti leggono il testo pulito, senza grafica, e costa loro molti meno token. Sono `noindex` per Google, quindi non creano doppioni.
3. **Un'unica identità dello Studio**: ogni pagina ha un nodo WebPage collegato a `#studio`, `#sito` e, nelle guide e nelle materie, a `#avvocato` come autore e revisore, con la data di revisione. Ognuna delle 18 materie ha anche un nodo `Service`, con i comuni serviti e i due canali, in Studio e online. Ora Google e le IA vedono un solo Studio con una sola avvocata su 66 pagine.
4. **robots.txt con Content-Signal**: permesso esplicito per la ricerca, per le risposte IA e per l'addestramento, con 18 bot elencati. Per impedire l'addestramento basta mettere `ai-train=no` in `tools/agenti.py`.
5. **`/cerca.json`**: indice di tutte le pagine, usato da WebMCP e leggibile dagli agenti.
6. **llms.txt** con una nuova sezione dedicata agli agenti.
7. **Description riscritte** per `attivita` e `domiciliazioni`, prima troppo corte.
8. **`tools/indexnow.py`**: avvisa subito Bing di ogni pagina nuova. Bing alimenta anche Copilot e la ricerca di ChatGPT. Va lanciato solo dopo la pubblicazione.

## Risultato dell'audit (`tools/audit.py`, vedi AUDIT.md)

- 0 errori.
- Prima delle modifiche: nessuna versione Markdown, nessuno strumento WebMCP, niente Content-Signal e l'identità dello Studio presente su 1 pagina sola.
- Dopo: `#studio` e `#sito` collegati in 66 pagine su 66, `#avvocato` in 46.
- Pagine dei comuni: la somiglianza massima è del 38%, sotto la soglia di rischio del 50%. Non sono pagine fotocopia.
- Avvisi rimasti: molti title delle guide superano i 65 caratteri. Non è un errore (Google li taglia in anteprima), ma vanno accorciati a mano, uno per uno, perché sono testi che vanno scelti con cura.

## Prossimi passi (servono account o chiavi, che li forniate voi)

1. **Bing Places e Bing Webmaster Tools**: Bing alimenta ChatGPT e Copilot. Rivendicare la scheda, poi lanciare `tools/indexnow.py` dopo ogni pubblicazione.
2. **Monitorare le citazioni nelle IA** (sul modello di elmo e GetCito): ogni settimana si fanno le stesse 30 domande ("avvocato separazione Vigevano", "chi segue successioni in Lomellina"...) a ChatGPT, Gemini, Perplexity e Claude e si registra se lo Studio viene citato. Servono le chiavi API di quei servizi. Posso farlo girare io con una routine settimanale.
3. **Geo-grid su Google Maps** (sul modello di legends-geogrid): la posizione dello Studio per "avvocato" in una griglia di punti tra Vigevano, Mortara e Abbiategrasso. Serve una chiave Google Places.
4. **Log dei bot IA** (sul modello di GEOInflow): una piccola Edge Function su Netlify che conta quali bot IA leggono quali pagine. Va decisa insieme perché aggiunge codice lato server.
5. **Espansione su più sedi**: la struttura è pronta. Ogni sede nuova avrà un nodo `LegalService` con il proprio `@id` (es. `/#sede-pavia`), collegato a `#studio` con `parentOrganization`, una sua pagina `/sede-<città>` e una sua scheda Google. Il codice va scritto quando ci sarà l'indirizzo vero: inventare sedi è vietato da Google e dal codice deontologico.

Limite deontologico sempre valido: i testi restano informativi (art. 17 e 35 del Codice deontologico forense). Niente "primo studio d'Italia" sul sito, nemmeno negli strumenti per le IA: l'obiettivo si raggiunge con i fatti, non con lo slogan.
