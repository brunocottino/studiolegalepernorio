# Brief operativo per il sito studiolegalepernorio.com

> Da incollare così com'è alla sessione Cowork che gestisce il sito.

---

Sei responsabile del sito **studiolegalepernorio.com**, dello Studio Legale dell'Avv. Daniela Pernorio, Via Egidio Sacchetti 14, 27029 Vigevano (PV). Il sito è statico e pubblicato su Netlify, con pagine `.html`, immagini in `/img/*.webp` e il modulo contatti su Netlify Forms.

**Obiettivo:** primo risultato su Google, in mappa e nei risultati organici, per "avvocato Vigevano" e per le ricerche "avvocato + materia + Vigevano/Lomellina". Primo anche nei paesi vicini e nelle risposte dei motori AI (ChatGPT, Perplexity, Gemini, Claude). Il sito deve convertire la visita in una telefonata, un WhatsApp o una prenotazione.

Lavora per fasi, nell'ordine indicato. Alla fine di ogni fase pubblica un deploy preview, esegui i controlli elencati in "Verifica" e passa alla fase successiva solo se sono tutti verdi. **Non inventare dati biografici, numeri, casi o recensioni.** Dove servono, metti il segnaposto `[[DA COMPILARE: ...]]` e raccoglili tutti nella lista finale delle domande.

---

## FASE 1 – Correzioni tecniche critiche

Stato attuale verificato il 2/11/2026:
- tutti i `<link rel="canonical">`, la sitemap, `og:url` e il JSON-LD puntano a `https://www.studiolegalepernorio.com/....html`;
- `www.studiolegalepernorio.com` fa un redirect 301 verso `https://studiolegalepernorio.com/`, quindi **ogni canonical punta a un URL che reindirizza**;
- ogni pagina risponde sia a `/pagina` sia a `/pagina.html` con status 200: contenuto duplicato;
- in `/contatti` è visibile il testo "Anteprima: nel sito pubblicato la richiesta arriva via email allo Studio."

Da fare:
1. **Dominio unico: `https://studiolegalepernorio.com` (senza www), URL senza `.html`.** Esempi: `/`, `/studio`, `/attivita`, `/attivita-affidamento-minori`, `/guida-sfratto-per-morosita`.
2. Aggiorna in **ogni** pagina il canonical, `og:url`, i link interni (`href`) e tutti gli URL nel JSON-LD (`url`, `image`, `@id`, `logo`) alla forma scelta. Nessun link interno deve più contenere `.html` o `www.`.
3. Crea o aggiorna `_redirects` con:
   ```
   https://www.studiolegalepernorio.com/*  https://studiolegalepernorio.com/:splat  301!
   http://www.studiolegalepernorio.com/*   https://studiolegalepernorio.com/:splat  301!
   ```
   Aggiungi poi **una regola esplicita per ogni pagina** (generale con uno script dall'elenco dei file):
   ```
   /studio.html  /studio  301!
   /attivita-affidamento-minori.html  /attivita-affidamento-minori  301!
   ...
   /index.html  /  301!
   ```
   Se compare un loop di redirect, sposta le pagine in cartelle (`/studio/index.html`) e aggiorna di conseguenza.
4. Rigenera `sitemap.xml` con soli URL canonici, `lastmod` reale, home e pagine principali comprese. Aggiungi `Sitemap: https://studiolegalepernorio.com/sitemap.xml` in fondo a `robots.txt`.
5. **Modulo contatti**: rimuovi il testo "Anteprima". Verifica `data-netlify="true"`, `name` del form, input hidden `form-name`, honeypot con `netlify-honeypot="bot-field"` e campo nascosto con CSS (non visibile né letto dagli screen reader). Redirect dopo l'invio a una pagina `/grazie` con `<meta name="robots" content="noindex">`, numero di telefono e pulsante WhatsApp. Fai un invio di prova e conferma che la notifica email arriva.
6. Crea una pagina **404** personalizzata, con ricerca delle materie, telefono e link alle guide.
7. Aggiungi header di sicurezza e cache in `netlify.toml`: `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`, e cache lunga (`max-age=31536000, immutable`) su `/img/*`, CSS e JS con nomi versionati.

**Verifica:** per 5 pagine a campione, `curl -sI` sulla versione `www` e su quella `.html` deve dare un **unico** 301 verso l'URL canonico, e l'URL canonico deve rispondere 200. Il canonical di ogni pagina deve essere uguale al suo URL finale. La sitemap non deve contenere né `www` né `.html`.

---

## FASE 2 – Prestazioni (Core Web Vitals)

1. **Google Fonts in locale.** Scarica i file `woff2` dei font usati, servili da `/fonts/` con `font-display: swap` e `preload` del font principale. Elimina ogni chiamata a `fonts.googleapis.com`/`gstatic.com`. È più veloce e risolve il trasferimento di IP a Google oggi dichiarato nella cookie policy: aggiorna quella pagina.
2. Su ogni `<img>` metti `width`/`height` espliciti, `loading="lazy"` e `decoding="async"`, tranne l'immagine principale della pagina, che va con `fetchpriority="high"` e senza lazy. Crea varianti `srcset` a 480, 960 e 1600 px.
3. CSS critico inline nell'`<head>`, il resto in un file differito. JS con `defer`.
4. Target Lighthouse mobile: **Performance ≥ 95, SEO 100, Accessibility ≥ 95, Best Practices 100**. LCP < 2,0 s, CLS < 0,05, INP < 200 ms.

**Verifica:** Lighthouse mobile su home, `/attivita`, una pagina materia e una guida. Riporta i punteggi.

---

## FASE 3 – Dati strutturati completi

Un unico grafo JSON-LD per pagina con `@id` stabili:

- `https://studiolegalepernorio.com/#studio`: `LegalService`. Conserva i dati attuali e aggiungi:
  - `openingHoursSpecification`: `[[DA COMPILARE: orari reali]]`;
  - `sameAs`: scheda Google, LinkedIn, Instagram, Facebook (solo quelli esistenti);
  - `logo`, `image` (più foto dello studio), `hasOfferCatalog` con le 18 materie come `Offer`/`Service` e il link alla rispettiva pagina;
  - `areaServed` come oggetti `City`/`AdministrativeArea` con nome e, dove possibile, `sameAs` a Wikipedia;
  - `email`: aggiornala quando sarà attiva la casella sul dominio (vedi Parte B).
- `https://studiolegalepernorio.com/#avvocato`: `Person` (Attorney) con `name`, `honorificPrefix`, `jobTitle`, `worksFor` → `#studio`, `memberOf` Ordine Avvocati di Pavia, `alumniOf`, `knowsLanguage`, `image`, `sameAs` (LinkedIn) e `hasCredential` (`[[DA COMPILARE: anno iscrizione Albo, titoli]]`).
- `https://studiolegalepernorio.com/#sito`: `WebSite` con `publisher` → `#studio` e `inLanguage: it-IT`.
- Su ogni pagina: `WebPage` con `isPartOf` → `#sito`, più `BreadcrumbList`, con i breadcrumb resi visibili anche in pagina.
- Sulle pagine materia: `Service` con `provider` → `#studio`, `areaServed` e `serviceType`.
- Sulle guide: `Article` con `author` → `#avvocato`, `publisher` → `#studio`, `datePublished`, `dateModified`, `image` e `mainEntityOfPage`.
- Su `/domande` e nei blocchi FAQ delle pagine: `FAQPage`. Le domande in JSON-LD devono essere identiche a quelle visibili in pagina.
- **Non** aggiungere `aggregateRating`/`review` sul proprio `LegalService`: Google non le mostra per le recensioni pubblicate dall'attività stessa e può penalizzarle.

**Verifica:** Rich Results Test e validator.schema.org senza errori su home, `/studio`, una materia, una guida e `/domande`.

---

## FASE 4 – Rafforzare le 18 pagine materia

Per ogni pagina `attivita-*`:
1. `<title>`: `Avvocato [materia] a Vigevano · Avv. Daniela Pernorio` (massimo circa 60 caratteri; accorcia la materia se serve).
2. `<h1>`: `Avvocato per [materia] a Vigevano e in Lomellina`.
3. Meta description di 140–155 caratteri, con materia, Vigevano, il beneficio e un invito all'azione.
4. Porta il contenuto a **900–1.400 parole**, con questa struttura H2:
   - Quando serve un avvocato per [materia];
   - Come lavora lo Studio, passo per passo;
   - Tempi indicativi e tribunale competente (Pavia per Vigevano e la Lomellina; verifica gli altri comuni);
   - Documenti da preparare per il primo colloquio (checklist);
   - Costi: come si forma il preventivo, ed eventuale gratuito patrocinio;
   - Domande frequenti (4–6, con `FAQPage`);
   - Guide collegate (link alle guide pertinenti).
5. **Blocco contatti fisso** a fine pagina: telefono cliccabile, WhatsApp, "Prenota il primo colloquio".
6. Link interni: ogni pagina materia rimanda ad almeno 2 guide e 2 materie affini; ogni guida rimanda alla sua materia con un testo-link descrittivo, ad esempio "avvocato per separazioni a Vigevano".

Priorità di scrittura, per volume di ricerca: Separazione e divorzio → Affidamento minori → Successioni → Sfratti → Saldo e stralcio → Sinistri → Diritto del lavoro → Codice della strada → tutte le altre.

---

## FASE 5 – Nuove pagine

### 5a. Pagine per i comuni
`/avvocato-mortara`, `/avvocato-gambolo`, `/avvocato-garlasco`, `/avvocato-cassolnovo`, `/avvocato-cilavegna`, `/avvocato-abbiategrasso`, `/avvocato-lomellina`.

Ogni pagina ha **contenuto unico, almeno 700 parole, mai un testo uguale con il nome cambiato**:
- H1: `Avvocato per i cittadini di [Comune]`;
- distanza e tempo dallo studio in auto, parcheggio vicino allo studio, possibilità di colloquio in videochiamata;
- tribunale e giudice di pace competenti per quel comune (**verifica** sul sito del Ministero della Giustizia);
- le 5–6 materie più richieste, con link alle pagine materia;
- una mappa statica (immagine) con il percorso, oppure un link a Google Maps, senza iframe che rallentano;
- 3 FAQ specifiche del comune;
- JSON-LD: `WebPage` con `about` → `#studio` e `areaServed` = quel comune.
- Inserisci tutte queste pagine nel footer, sotto "Dove operiamo".

### 5b. Pagine ad alta intenzione
- `/costi-avvocato`: come si calcola il compenso (parametri del DM 55/2014 e successivi aggiornamenti; **verifica che siano in vigore**), cosa include il primo colloquio, preventivo scritto, pagamenti rateali `[[DA COMPILARE: sì/no]]`.
- `/gratuito-patrocinio`: requisiti di reddito (soglia **aggiornata**, da verificare), documenti, procedura a Pavia.
- `/prenota`: prenotazione del primo colloquio in studio o in videochiamata. Integra il calendario scelto (Google Calendar Appointment Schedule o Calendly `[[DA COMPILARE: quale]]`) caricando lo script **solo al clic**, per non pesare sulla pagina.
- `/avvocato-separazione-consensuale-vigevano`: pagina specifica sul percorso consensuale (tempi, costi, negoziazione assistita contro ricorso in tribunale). Mettila sotto la materia "Separazione e divorzio" e collegala in entrambe le direzioni.

### 5c. Strumenti interattivi (calamite di traffico e di link)
Tutto in JS vanilla, senza dipendenze esterne, utilizzabile da mobile. Ogni strumento ha in fondo una CTA verso la materia collegata.
1. `/strumenti/calcolo-quote-eredita`: successione **senza testamento** (artt. 565–586 c.c.) e quote di legittima (artt. 536–548 c.c.). Input: coniuge sì/no, numero di figli, genitori viventi, fratelli. Output: le quote in frazione e in percentuale, più un esempio su un valore inserito dall'utente. Scrivi i test dei casi base e verificali contro il codice civile, per esempio: coniuge + 1 figlio = 1/2 ciascuno; coniuge + 2 o più figli = 1/3 coniuge e 2/3 divisi tra i figli; solo coniuge = tutto.
2. `/strumenti/scadenze-multa`: dalla data di notifica calcola la scadenza del pagamento ridotto del 30% (5 giorni), del pagamento in misura ridotta (60 giorni), del ricorso al Prefetto (60 giorni) e del ricorso al Giudice di Pace (30 giorni). **Verifica i termini vigenti** e prevedi un link alla guida autovelox.
3. `/strumenti/checklist-separazione`: checklist dei documenti con caselle spuntabili (stato salvato in `localStorage`, dentro try/catch) e pulsante "Stampa / salva PDF".

### 5d. Guide: calendario editoriale
Aggiungi in `/guide` le seguenti guide, una o due a settimana, ciascuna di 1.200–1.800 parole, con indice, FAQ e un riquadro "In sintesi" in apertura (utile per Google e per le risposte AI):
1. Quanto costa una separazione consensuale nel 2026
2. Separazione: chi resta nella casa familiare
3. Assegno di mantenimento per i figli: come si calcola
4. Convivenza finita: cosa spetta a ciascuno
5. Divorzio breve: tempi reali a Pavia
6. Eredità con debiti: rinuncia o accettazione con beneficio d'inventario
7. Testamento olografo: come farlo valido
8. Caparra e affitto: quando il proprietario deve restituirla
9. Il padrone di casa può entrare in casa? Diritti dell'inquilino
10. Licenziamento: cosa fare nei primi 60 giorni
11. Incidente stradale: cosa fare con l'assicurazione
12. Prestito non restituito tra privati: come recuperarlo
13. Condominio: come contestare una delibera
14. Cartelle e debiti con le finanziarie: quando conviene il saldo e stralcio
15. Domiciliazioni presso il Tribunale di Pavia: come funzionano (per i colleghi)

Per ogni guida: firma dell'avvocato con foto, "Aggiornata al [data]", link alla materia e allo strumento pertinente.

---

## FASE 6 – Conversione e mobile

1. **Barra fissa in basso su mobile** con tre pulsanti: Chiama, WhatsApp, Prenota. Deve restare entro `env(safe-area-inset-bottom)` e non coprire il contenuto.
2. Header: numero di telefono cliccabile sempre visibile.
3. Blocco "Recensioni Google" (le 3 già presenti, più un link "Leggi tutte le 64 recensioni"), ripetuto anche sulle pagine materia.
4. Pagina `/studio`: biografia estesa (`[[DA COMPILARE: anno iscrizione, laurea, corsi, specializzazioni, lingue, associazioni]]`), foto, "Come lavoro", collegamenti a LinkedIn e Instagram.
5. Immagine Open Graph 1200×630 dedicata per ogni pagina principale, generata con titolo e foto, così le condivisioni su WhatsApp mostrano un'anteprima curata.

---

## FASE 7 – Motori AI e misurazione

1. Crea `/llms.txt` con la descrizione dello studio, il NAP, le materie con i link, i comuni serviti e l'elenco delle guide.
2. In ogni guida apri con una risposta diretta di 2–3 frasi alla domanda del titolo, prima dell'indice.
3. **Statistiche senza cookie**: attiva Netlify Analytics lato server, oppure Plausible/Umami (senza cookie). Aggiorna la cookie policy.
4. Traccia come eventi i clic su telefono, WhatsApp, prenotazione e invio del modulo.
5. Prepara il file di verifica per Google Search Console e Bing Webmaster Tools (proprietà sul dominio, se possibile via DNS) e invia la sitemap.

---

## Consegna

A fine lavoro restituisci:
1. l'elenco delle pagine create e modificate;
2. i punteggi Lighthouse prima e dopo;
3. l'esito del Rich Results Test;
4. l'output dei controlli `curl` della Fase 1;
5. **la lista di tutti i `[[DA COMPILARE]]`** in forma di domande da girare all'Avv. Pernorio.

---
---

# Parte B – Fuori dal sito (Bruno e Daniela)

Queste attività non le può fare l'agente del sito, ma pesano quanto il sito e per la mappa di Google anche di più.

1. **Scheda Google Business Profile**
   - Categoria principale: Avvocato. Secondarie: Avvocato divorzista, Avvocato di diritto di famiglia, Avvocato civilista, Studio legale, Avvocato del lavoro.
   - Inserisci tutti i servizi, gli orari precisi, il link a `/prenota`, almeno 15 foto (studio, ingresso, avvocato) e la descrizione con le parole "avvocato Vigevano", "separazioni", "successioni" e "Lomellina".
   - Un post a settimana che riprende una guida del sito.
   - Inserisci e rispondi alle domande nella sezione Q&A.
2. **Recensioni**: il link diretto alla recensione via WhatsApp a ogni cliente soddisfatto, a fine pratica. Obiettivo: 100 recensioni entro giugno. Rispondere a tutte entro 48 ore.
3. **Email sul dominio**: `info@studiolegalepernorio.com` o `daniela@...` con Google Workspace o Zoho, da aggiornare poi su sito, scheda Google ed elenchi.
4. **Elenchi online con dati identici** (stesso nome, indirizzo e telefono, scritti allo stesso modo): Bing Places, Apple Business Connect, Pagine Gialle, Pagine Bianche, Cylex, Infobel, Hotfrog, Avvocato360, Avvocati.it, iCompetenti, Facebook Page.
5. **Social**: Instagram (e TikTok, se sostenibile) con 2 reel brevi a settimana tratti dalle guide; LinkedIn personale per i colleghi e le domiciliazioni.
6. **Link locali**: articoli o interviste su L'Informatore Vigevanese, La Provincia Pavese e Prima la Lomellina; incontri pubblici con il Comune, le associazioni e le scuole, con un link al sito.
7. **Google Ads locale (opzionale)**: campagna su "avvocato separazione Vigevano" e "avvocato divorzista Vigevano" in un raggio di 20 km, con un budget di prova di 10–15 €/giorno, mandando il traffico sulle pagine materia e su `/prenota`.
