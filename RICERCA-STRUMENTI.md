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

---

# Seconda ricerca, più a fondo (6 novembre 2026)

## Cosa dicono i dati più recenti

- **Studio di Yext** su 6,8 milioni di citazioni in ChatGPT, Gemini e Perplexity: il 44% viene dai siti delle aziende e il 42% dalle schede e dagli elenchi delle attività. Gli elenchi pesano quasi quanto il sito.
- **Sterling Sky** (giugno 2026): i risultati locali dati dalle IA mostrano molte meno attività rispetto ai 3 risultati della mappa di Google (5.943 contro 18.330 in 322 mercati). Chi entra lo fa a spese degli altri.
- **Princeton (KDD 2024)**: citare fonti precise, dati con la loro provenienza e citazioni di esperti aumenta la probabilità di essere ripresi dai motori IA.
- **Varietà tra motori**: ogni IA cita fonti diverse per la stessa domanda, quindi la visibilità va misurata motore per motore.
- **Mappe di ChatGPT**: usano Mapbox, che si basa su OpenStreetMap, e i risultati locali vengono anche da Bing.

## Cosa è stato aggiunto

1. **Fonti normative su tutte le 25 guide**: 70 riferimenti con link permanenti a Normattiva (URN:NIR ufficiali; i 15 atti sono stati controllati uno per uno con `tools/fonti.py --verifica`). Ogni fonte compare anche nei dati strutturati dell'articolo (`citation` di tipo `Legislation`). Nessuno studio della zona lo fa.
2. **Server MCP dello Studio** su `/mcp`, con la scheda di scoperta in `/.well-known/mcp/server-card.json`. Chiunque può aggiungere lo Studio come connettore in ChatGPT, Claude e negli altri programmi MCP, senza registrazione. Ha 6 strumenti di sola lettura: informazioni sullo Studio, ricerca nel sito, lettura di una pagina, quote di eredità, imposta di successione, scadenze di una multa. È stato provato con tutte le chiamate del protocollo. Va pubblicato con `--functions functions`.
3. **Nuovo strumento: calcolo dell'imposta di successione**, con franchigie, aliquote del 4, 6 e 8%, imposte ipotecaria e catastale e agevolazione prima casa (D.Lgs. 346/1990). È una ricerca molto frequente e attira link. È disponibile anche come strumento WebMCP e MCP.
4. **Guide correlate** in fondo a ogni guida, scelte in base al contenuto: le guide con un solo link in entrata sono scese da 6 a 1.
5. **Navigazione istantanea** (Speculation Rules): Chrome ed Edge precaricano la pagina quando il dito si avvicina al link. Migliora i Core Web Vitals.
6. **`ELENCHI.md`**: dati identici per Google, Bing Places, Apple Business Connect, OpenStreetMap (tag pronti), Pagine Gialle, Yelp, Foursquare e gli elenchi forensi.
7. **`tools/visibilita_ia.py`**: 15 domande da cliente poste a Gemini, ChatGPT, Perplexity e Claude con la ricerca web attiva, senza mai nominare lo Studio. Conta quante volte lo Studio viene citato e salva lo storico. Le chiamate alle API non sono ancora state provate: mancano le chiavi.

## Scartato, e perché

- **Pagine "servizio + comune" a tappeto** (es. 18 materie × 7 comuni): Google le tratta come pagine doorway. Le pagine dei comuni attuali sono diverse tra loro al 62% o più, e così devono restare.
- **Valutazioni a stelle nei dati strutturati**: Google non le mostra per le recensioni pubblicate dall'attività stessa e può penalizzarle.
- **Wikidata**: lo Studio non ha ancora fonti indipendenti che lo rendano rilevante. Rischio di cancellazione.
- **Risposte con IA sul sito (NLWeb, endpoint /ask)**: servirebbe un modello IA a pagamento e c'è il rischio di risposte legali sbagliate a nome dello Studio. MCP e WebMCP danno dati e calcoli certi, lasciando l'interpretazione all'assistente di chi chiede.

## Fonti della ricerca

- https://arxiv.org/pdf/2606.20065 (GEO at Scale)
- https://arxiv.org/pdf/2605.25517 (What Gets Cited)
- https://arxiv.org/pdf/2607.14035 (rassegna GEO 2023-2026)
- https://metavert.io/industry/generative-engine-optimization-for-local-businesses
- https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1649 (MCP Server Cards)
- https://bndy.org/posts/chatgpt-attribution-mapbox-openstreetmap/
- https://www.normattiva.it/staticPage/utilita (link URN)
- https://github.com/Sanrovax/ai-visibility-checker

---

# Terzo giro: lavoro fatto in autonomia (6 novembre 2026)

- **Misura della visibilità** nella ricerca web di Claude, con domande da cliente: per le domande generiche lo Studio non compare, compaiono gli elenchi (Dequo, Virgilio, Lawzana). Dettagli in `dati/visibilita-2026-11-06.md`. Lawzana ha dati sbagliati. Le chiavi API per misurare ChatGPT e Gemini non sono state fornite.
- **IndexNow inviato** per le 66 pagine già online (risposta 200): Bing, Yandex, Seznam e Naver sono avvisati. Nessuna pubblicazione di contenuti nuovi.
- **Immagini di anteprima per ogni pagina** (67, 1200x630) in `static/og/`, collegate con og:image e twitter:image e nel nodo `primaryImageOfPage`. Quando un link viene condiviso su WhatsApp, Facebook o LinkedIn mostra il titolo della pagina e il volto dell'avvocata, non più la stessa immagine per tutte.
- **14 caroselli Instagram** (5 immagini ciascuno, 4:5) dalle guide, con didascalie, hashtag e post per la scheda Google in `social/PIANO-SOCIAL.md`. Calendario settimanale dal 9 novembre 2026.
- **Content-Security-Policy rigorosa**, generata a ogni build con le impronte dei 7 script interni e senza `unsafe-inline` per gli script. Provata su tutte le 69 pagine: 0 violazioni, tutti gli strumenti funzionano.
- **Prestazioni** misurate su un telefono simulato con CPU rallentata 4 volte: LCP 0,56-0,70 secondi e CLS 0 su home, guide, competenze, comuni e contatti (la soglia "buono" di Google è 2,5 secondi).

## Cosa non ho potuto fare, e perché

- **Google Business Profile, Bing Places, Apple Business Connect, Dequo, Lawzana, Italiaonline, OpenStreetMap**: servono un account intestato allo Studio e, per Google, Bing e Apple, una verifica del titolare (cartolina, telefono o video). Non posso creare account o fare verifiche a nome dell'avvocata. Tutto il testo da copiare è in `ELENCHI.md`.
- **Email sul dominio**: serve un servizio di posta (es. Google Workspace o Zoho) e la modifica del DNS, che è un'azione sul sito pubblicato.
- **Lettura diretta delle schede Virgilio, Pagine Bianche e Lawzana**: quei siti bloccano la lettura automatica.

---

# Pubblicazione (6 novembre 2026)

Rifiniture finali: title entro 65 caratteri su tutte le pagine (la firma si accorcia, il tema resta), descrizioni riscritte per home, diritto di famiglia, guide, cookie e privacy, e un paragrafo nell'informativa privacy su calcolatori, server MCP e WebMCP. Audit: 0 errori, 0 avvisi.

Pubblicato in produzione su studiolegalepernorio.com (deploy 6aeddf8453f260ed4f941a16), con il sito e la funzione `/mcp`. Controlli sul sito vero:
- tutte le pagine, le versioni `.md`, `cerca.json`, `agenti.js`, la scheda MCP e le immagini di anteprima rispondono 200;
- CSP e HSTS sono attivi, i file `.md` sono `noindex`;
- il server MCP risponde a initialize, cerca_nel_sito e leggi_pagina;
- nessun errore JavaScript o CSP in un browser reale su 10 pagine chiave;
- Netlify rileva entrambi i moduli (contatti e colloquio online);
- IndexNow ha ricevuto i 67 URL.

---

# Quarto giro: farsi trovare da più strumenti (9 novembre 2026)

Preparato e salvato su GitHub. **Non pubblicato**: serve il permesso.

1. **Ricerca nel sito** (`/cerca`). Una casella di ricerca nella pagina Guide, nella pagina di errore 404 e nel piè di pagina. Capisce le parole di tutti i giorni: "affitto" trova le locazioni, "padrone di casa" i diritti dell'inquilino, "nonno anziano" l'amministrazione di sostegno. Funziona nel browser: ciò che si scrive non viene inviato né salvato. Provata con 15 ricerche su computer e telefono, senza errori.
2. **Il sito si cerca dalla barra del browser** (OpenSearch) e dichiara la ricerca a Google e agli assistenti (SearchAction).
3. **Glossario legale** (`/glossario-legale`): 40 termini spiegati in poche righe, ognuno con l'articolo di legge su Normattiva e il collegamento alla guida. Risponde alle ricerche del tipo "cosa significa precetto". Dati strutturati DefinedTermSet. **Da far rileggere all'avvocata prima della pubblicazione.**
4. **Date vere per Google**. Prima, a ogni build, tutte le 67 pagine risultavano modificate "oggi": Google in questi casi smette di fidarsi delle date. Ora la data cambia solo se cambia il testo (`dati/date-pagine.json`), e le guide tengono la data di prima pubblicazione.
5. **Feed delle guide** (`/feed.xml`): lettori di feed, Bing e aggregatori vedono subito le guide nuove.
6. **Sitemap con immagini**: le foto dello Studio e le anteprime entrano in Google Immagini.
7. **Anteprime grandi e testo completo** nei risultati (`max-image-preview:large`, `max-snippet:-1`): servono anche per Google Discover.
8. **Markdown su richiesta**: un assistente che chiede `Accept: text/markdown` riceve la pagina in testo pulito, allo stesso indirizzo. Le persone non vedono differenze.
9. **Catalogo per gli agenti** (`/.well-known/api-catalog`, RFC 9727) e intestazioni `Link` sulla home: indicano dove sono llms.txt, sitemap, feed e server MCP.
10. **Indice di ricerca più ricco**: comprende le domande frequenti di ogni pagina e i termini del glossario. Lo usano anche il server MCP e gli strumenti WebMCP.

Audit: 0 errori, 0 avvisi. Nuovi controlli in `tools/audit.py` su feed, sitemap, ricerca e date.

Non provata in produzione: la funzione `markdown.js` gira solo su Netlify. La logica è stata provata a parte e in caso di errore lascia passare la pagina normale.

## Cosa resta fuori dal codice

Sono ancora le mosse con più effetto, e richiedono un account intestato allo Studio: scheda Google curata e recensioni, Bing Places, Apple Business Connect, Dequo, correzione di Lawzana e di Virgilio/Pagine Bianche. I testi sono in `ELENCHI.md`.
