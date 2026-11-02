# Piano SEO – Studio Legale Pernorio (Vigevano)

Analisi del sito pubblicato studiolegalepernorio.com del 2 novembre 2026.

## Punto di partenza

Il sito è già sopra la media degli studi legali di zona: title e meta description scritte bene e localizzate ("Avvocato a Vigevano"), dati strutturati `LegalService` in JSON-LD, sitemap, robots.txt aperto anche ai motori di ricerca AI, 18 pagine sulle aree di attività, 10 guide pratiche, alt text su tutte le immagini, 64 recensioni Google con media 5,0. Non serve rifarlo da zero.

## 1. Correzioni urgenti (questa settimana)

1. **Conflitto www / senza www.** Tutti i tag `canonical` e tutta la sitemap puntano a `https://www.studiolegalepernorio.com/...`, ma il dominio `www` fa un redirect 301 verso `https://studiolegalepernorio.com/`. Google riceve così due segnali opposti: "la pagina giusta è la www" e "la www non esiste, vai sull'altra". Va scelta una sola versione (consigliata: quella senza www, perché è già quella primaria su Netlify) e allineati canonical, sitemap, JSON-LD (`url`, `image`) e Search Console.
2. **Doppio URL per pagina.** Ogni pagina risponde sia a `/studio` sia a `/studio.html`. Il canonical punta alla versione `.html`, ma i link interni usano spesso quella senza estensione. Uniformare i link interni e i canonical sulla stessa forma (consigliata quella senza `.html`) e impostare un redirect 301 dall'altra.
3. **Testo di anteprima visibile** nel modulo contatti: "Anteprima: nel sito pubblicato la richiesta arriva via email allo Studio." Va tolto, e va verificato che il modulo Netlify Forms consegni davvero le email.
4. **Email professionale.** Sostituire `daniela.pernorio@gmail.com` con `info@studiolegalepernorio.com` (o `daniela@...`) su sito, JSON-LD e scheda Google. Aumenta la fiducia e la coerenza dei dati.
5. **Search Console e Bing Webmaster Tools.** Verificare la proprietà del dominio, inviare la sitemap corretta, controllare pagine escluse e query di ricerca reali.

## 2. Scheda Google (Google Business Profile): la leva più forte

Per "avvocato Vigevano", "avvocato separazione Vigevano" e simili, Google mostra prima la mappa con 3 studi (il "local pack"). Lì contano la scheda Google, le recensioni e la vicinanza, più del sito.

- Categoria principale: **Avvocato**. Categorie secondarie: Avvocato divorzista, Avvocato di diritto di famiglia, Avvocato civilista, Studio legale.
- Servizi: inserirli tutti e 18, con una breve descrizione ciascuno.
- Orari precisi (non solo "su appuntamento"), foto dello studio, foto dell'avvocato.
- Un post a settimana (riprendendo una guida del sito).
- Sezione Domande e risposte compilata con le domande più frequenti.
- Recensioni: chiedere a ogni cliente soddisfatto a fine pratica, con un link diretto. Rispondere a tutte, senza mai citare dettagli della pratica (segreto professionale).
- NAP (nome, indirizzo, telefono) identico ovunque: sito, Google, Pagine Gialle, Apple Maps, Bing Places, elenchi forensi.

## 3. Pagine nuove sul sito (contenuti locali)

Oggi Vigevano è ben coperta. Mancano le pagine per i paesi vicini, da cui arriva gran parte della clientela:

- `avvocato-mortara`, `avvocato-gambolo`, `avvocato-garlasco`, `avvocato-cassolnovo`, `avvocato-cilavegna`, `avvocato-abbiategrasso`.
  Ciascuna con contenuto davvero diverso: distanza e tempi dallo studio, tribunale competente (Pavia per la Lomellina, Milano per l'Abbiatense), le materie più richieste, possibilità di colloquio online. Niente pagine fotocopia: Google le penalizza.
- Pagine "servizio + città" solo per i temi forti: **separazione Vigevano**, **divorzio Vigevano**, **affidamento figli Vigevano**, **successioni Vigevano**, **saldo e stralcio Vigevano**.
- Pagina **Costi e preventivo**: come si forma il compenso, cosa include il primo colloquio, gratuito patrocinio (reddito, procedura). È una delle ricerche più frequenti ("quanto costa una separazione").
- Pagina **Domande frequenti** arricchita con dati strutturati `FAQPage`.
- Biografia più ricca sulla pagina Lo Studio: anno di iscrizione all'Albo, formazione, corsi e specializzazioni, lingue, associazioni (es. AIAF, Camera civile). Google valuta molto l'esperienza dimostrata dell'autore nelle materie legali.
- Ogni guida firmata dall'avvocato, con data di aggiornamento e dati strutturati `Article` con autore.

## 4. Raggiungere i giovani

- **Instagram e TikTok** (o almeno Instagram): video brevi da 30–60 secondi tipo "Convivenza: cosa succede alla casa se ci lasciamo?", "Multa autovelox: quando si può contestare", "Affitto: il padrone di casa può entrare?". Ogni video rimanda alla guida sul sito.
- **WhatsApp** già presente: aggiungere un pulsante fisso su mobile.
- **Prenotazione online** del primo colloquio (anche in videochiamata) con un calendario tipo Calendly o Google Calendar.
- Temi che interessano i giovani: convivenze e unioni civili, affitti e caparre, contratti di lavoro e licenziamenti, incidenti stradali e multe, acquisto della prima casa.
- **LinkedIn** per l'avvocato: utile per la reputazione e per le domiciliazioni dai colleghi.

## 5. Un secondo sito?

Un secondo sito dello stesso studio, sugli stessi argomenti, **non conviene**: Google tende a mostrarne uno solo, i due siti si dividono la forza e le recensioni restano legate a una sola scheda. È molto meglio far crescere questo dominio.

Se si vuole un progetto in più, l'idea sensata è un **sito informativo tematico** con nome proprio, ad esempio una guida pratica su separazione e famiglia in Lomellina, oppure strumenti utili: calcolatore indicativo dell'assegno di mantenimento, calcolo della quota di legittima, checklist dei documenti per la separazione. Questi strumenti attirano link e visite e rimandano allo studio. Va fatto solo se c'è tempo di aggiornarlo con costanza.

## 6. Link e citazioni esterne

- Iscrizione a directory legali (Avvocati.it, Avvocato360, Pagine Gialle, Infobel, Cylex) con dati identici.
- Articoli o interviste su testate locali (L'Informatore Vigevanese, La Provincia Pavese, Prima la Lomellina).
- Incontri gratuiti con associazioni, scuole o Comune (es. "Diritti in famiglia"), con articolo sul sito dell'ente che linka lo studio.

## 7. Limiti deontologici (importante)

Il Codice deontologico forense (art. 17 e 35) consente pubblicità informativa ma vieta: superlativi e confronti ("il miglior avvocato", "il primo di Vigevano"), promesse di risultato, riferimenti a nomi di clienti, toni suggestivi. Tutti i testi, post e annunci devono restare informativi. Anche gli annunci a pagamento (Google Ads) sono ammessi solo con lo stesso tono.

## 8. Aspettative realistiche

Nessuno può garantire il primo posto in tutte le ricerche: dipende da Google, dalla posizione di chi cerca e dalla concorrenza. Con le correzioni tecniche, la scheda Google curata, le pagine locali e le recensioni costanti, l'obiettivo concreto è stare nei primi 3 della mappa per Vigevano e in prima pagina per i paesi vicini nel giro di 3–6 mesi.

## Ordine consigliato

1. Correzioni tecniche (sezione 1) – 1 giorno.
2. Scheda Google ottimizzata e campagna recensioni – 1 settimana.
3. Biografia arricchita, pagina costi, FAQ – 2 settimane.
4. Pagine per i paesi e "servizio + città" – 1 mese.
5. Instagram e prenotazione online – continuativo.
6. Eventuale sito/strumento tematico – dopo il punto 5.
