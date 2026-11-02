# -*- coding: utf-8 -*-
"""Contenuti delle pagine nuove del sito Studio Legale Pernorio.

Ogni pagina e' un dizionario con slug, title, description, h1, label, lead,
corpo HTML dell'articolo, FAQ e colonna laterale. Il build le impagina con
lo stesso layout delle pagine esistenti.
"""

AGGIORNATO = "novembre 2026"

# Comuni serviti -------------------------------------------------------------

COMUNI = [
    {
        "slug": "avvocato-mortara",
        "nome": "Mortara",
        "km": "circa 13 km",
        "min": "circa 20 minuti",
        "percorso": "Da Mortara si arriva a Vigevano percorrendo la strada provinciale verso nord-est, attraverso la campagna della Lomellina. Lo Studio è in Via Egidio Sacchetti 14, a pochi minuti a piedi dal centro storico e da Piazza Ducale.",
        "intro": "Mortara è il secondo centro della Lomellina e molti suoi abitanti hanno a Vigevano il lavoro, la scuola dei figli o i servizi di riferimento. Lo Studio Legale Pernorio assiste clienti di Mortara e dei comuni vicini nelle questioni di diritto civile, con un rapporto diretto con l'avvocato dal primo colloquio alla conclusione della pratica.",
        "tribunale": "Per chi risiede a Mortara è competente il <strong>Tribunale di Pavia</strong>, come per tutta la Lomellina dopo la soppressione del Tribunale di Vigevano nel 2013. Lo Studio segue abitualmente le udienze a Pavia: il cliente non deve spostarsi, salvo quando la sua presenza è richiesta dal giudice.",
        "temi": [
            ("attivita-successioni", "Successioni ed eredità", "divisioni di case e terreni agricoli tra coeredi, testamenti, quote di legittima"),
            ("attivita-usucapione-diritti-reali", "Usucapione e diritti reali", "confini, servitù di passaggio, fondi e cascine possedute da decenni"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-locazioni-comodato", "Locazioni e comodato", "contratti di affitto, canoni non pagati, restituzione dell'immobile"),
            ("attivita-saldo-e-stralcio", "Saldo e stralcio", "debiti con banche e finanziarie da chiudere con una somma ridotta"),
        ],
        "faq": [
            ("Devo andare a Pavia per la mia causa se abito a Mortara?", "Di regola no. Le udienze sono seguite dall'avvocato; la presenza della parte è necessaria solo in alcuni momenti, per esempio nell'udienza di comparizione dei coniugi in una separazione. In quei casi lo Studio la prepara e la accompagna."),
            ("Posso avere il primo colloquio senza venire a Vigevano?", "Sì: lo Studio offre il colloquio online, in videochiamata dal browser o su WhatsApp, con i documenti inviati prima tramite il sito. Chi preferisce può venire in Studio, su appuntamento."),
            ("Lo Studio segue anche questioni su terreni e cascine?", "Sì: usucapione, servitù, confini, divisioni ereditarie di fondi agricoli e comproprietà sono materie che lo Studio tratta regolarmente."),
        ],
    },
    {
        "slug": "avvocato-gambolo",
        "nome": "Gambolò",
        "km": "circa 8 km",
        "min": "circa 12 minuti",
        "percorso": "Gambolò confina con Vigevano: lo Studio, in Via Egidio Sacchetti 14, si raggiunge in pochi minuti d'auto.",
        "intro": "Per chi vive a Gambolò, Remondò o Belcreda, Vigevano è la città di riferimento a pochi chilometri. Lo Studio Legale Pernorio assiste i cittadini di Gambolò nelle questioni familiari, patrimoniali e nei rapporti con banche e finanziarie, con un preventivo scritto prima di iniziare.",
        "tribunale": "Gambolò rientra nel circondario del <strong>Tribunale di Pavia</strong>. È lo stesso tribunale competente per Vigevano: lo Studio vi segue abitualmente le udienze.",
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "consensuale, giudiziale, con negoziazione assistita"),
            ("attivita-affidamento-minori", "Affidamento dei figli", "tempi di permanenza, scuola, mantenimento, anche tra genitori non sposati"),
            ("attivita-condominio", "Condominio e liti tra vicini", "delibere, spese, immissioni e distanze"),
            ("attivita-recupero-crediti", "Recupero crediti", "diffide, decreti ingiuntivi, pignoramenti"),
            ("attivita-sinistri-responsabilita", "Incidenti e risarcimenti", "sinistri stradali e danni alla persona"),
        ],
        "faq": [
            ("Quanto costa rivolgersi allo Studio da Gambolò?", "Il costo non dipende da dove abita il cliente: prima di iniziare lo Studio consegna un preventivo scritto. Le voci che lo compongono sono spiegate nella pagina sui costi."),
            ("Posso fissare un appuntamento in giornata?", "Dipende dagli impegni in tribunale. Per le urgenze, per esempio un atto notificato con una scadenza vicina, conviene telefonare o scrivere su WhatsApp indicando la data di notifica."),
            ("Per una separazione devo cambiare tribunale se ci siamo sposati altrove?", "No: conta la residenza dei coniugi, non il luogo del matrimonio. Se entrambi vivono a Gambolò è competente il Tribunale di Pavia."),
        ],
    },
    {
        "slug": "avvocato-garlasco",
        "nome": "Garlasco",
        "km": "circa 20 km",
        "min": "circa 25 minuti",
        "percorso": "Da Garlasco si raggiunge Vigevano passando per Gambolò. Lo Studio è in Via Egidio Sacchetti 14, vicino al centro storico.",
        "intro": "Garlasco, Dorno, Tromello e Alagna guardano tanto a Pavia quanto a Vigevano. Lo Studio Legale Pernorio, con sede a Vigevano e attività quotidiana al Tribunale di Pavia, è un riferimento comodo per entrambe le direzioni: colloqui in Studio a Vigevano, udienze a Pavia.",
        "tribunale": "Per Garlasco è competente il <strong>Tribunale di Pavia</strong>. Chi abita qui ha quindi un vantaggio pratico: l'avvocato che lo segue è lo stesso che frequenta abitualmente quel tribunale e le sue sezioni, compresa la volontaria giurisdizione per amministrazioni di sostegno e successioni.",
        "temi": [
            ("attivita-amministrazione-di-sostegno", "Amministrazione di sostegno", "tutela di un genitore anziano o di un familiare fragile"),
            ("attivita-successioni", "Successioni ed eredità", "dichiarazione di successione, divisioni, accettazione con beneficio d'inventario"),
            ("attivita-sfratti", "Sfratti", "morosità e finita locazione"),
            ("attivita-lavoro", "Diritto del lavoro", "licenziamenti, retribuzioni non pagate, TFR"),
            ("attivita-crisi-impresa", "Sovraindebitamento", "procedure per privati e piccole imprese in difficoltà"),
        ],
        "faq": [
            ("Per un'amministrazione di sostegno a quale tribunale ci si rivolge da Garlasco?", "Al giudice tutelare del Tribunale di Pavia, competente per il luogo in cui la persona da tutelare ha residenza o domicilio."),
            ("Lo Studio è lontano da Garlasco?", "Circa venti minuti d'auto. Molte attività, come lo scambio di documenti e gli aggiornamenti sulla pratica, si svolgono anche per email e WhatsApp, senza bisogno di spostarsi."),
            ("Si può chiudere una lite senza andare in tribunale?", "Spesso sì: con la negoziazione assistita o la mediazione si arriva a un accordo che ha valore di titolo esecutivo. Lo Studio valuta sempre prima questa strada."),
        ],
    },
    {
        "slug": "avvocato-cassolnovo",
        "nome": "Cassolnovo",
        "km": "circa 8 km",
        "min": "circa 12 minuti",
        "percorso": "Cassolnovo e Villanova sono a nord di Vigevano, lungo il Ticino e al confine con il Piemonte. Lo Studio si raggiunge in una decina di minuti d'auto.",
        "intro": "Cassolnovo è un comune di confine: molti residenti lavorano in Piemonte o a Milano, e capita che una stessa questione coinvolga più tribunali. Lo Studio Legale Pernorio lavora davanti ai Tribunali di Pavia, Milano e Novara e può seguire la pratica anche quando una delle parti vive dall'altra parte del Ticino.",
        "tribunale": "Per chi risiede a Cassolnovo è competente il <strong>Tribunale di Pavia</strong>. Se la controparte, un datore di lavoro o un immobile si trovano in provincia di Novara o di Milano, può essere competente un altro tribunale: lo Studio lo verifica all'inizio, perché un errore sulla competenza fa perdere tempo e denaro.",
        "temi": [
            ("attivita-lavoro", "Diritto del lavoro", "anche con datori di lavoro in Piemonte o in Lombardia"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "anche quando i coniugi vivono in province diverse"),
            ("attivita-contratti", "Contratti", "compravendite, preliminari, appalti e scritture private"),
            ("attivita-codice-della-strada", "Ricorsi contro le multe", "autovelox, ZTL, sospensioni della patente"),
            ("attivita-saldo-e-stralcio", "Saldo e stralcio", "chiusura di debiti con banche e finanziarie"),
        ],
        "faq": [
            ("La mia ex moglie vive in provincia di Novara: quale tribunale decide?", "Dipende dal tipo di procedimento e da dove vivono i figli. Per le questioni sui figli minori conta di regola la loro residenza abituale. Lo Studio individua il tribunale competente nel primo colloquio."),
            ("Lo Studio segue cause anche a Novara?", "Sì, lo Studio opera anche davanti al Tribunale di Novara e al Tribunale di Milano."),
            ("Ho ricevuto una multa da un comune piemontese: posso fare ricorso da qui?", "Sì. Il ricorso al Prefetto o al Giudice di Pace è legato al luogo della violazione, ma la pratica si prepara in Studio. Attenzione ai termini: 60 giorni per il Prefetto, 30 per il Giudice di Pace."),
        ],
    },
    {
        "slug": "avvocato-cilavegna",
        "nome": "Cilavegna",
        "km": "circa 13 km",
        "min": "circa 18 minuti",
        "percorso": "Cilavegna si trova a ovest di Vigevano, verso Gravellona Lomellina e Robbio. Lo Studio, in Via Egidio Sacchetti 14, si raggiunge in meno di venti minuti.",
        "intro": "Per chi vive a Cilavegna, Gravellona Lomellina, Parona o Robbio, lo Studio Legale Pernorio offre assistenza civile completa a Vigevano: famiglia, casa, debiti, contratti, lavoro. Ogni pratica è seguita personalmente dall'avvocato.",
        "tribunale": "Cilavegna fa parte del circondario del <strong>Tribunale di Pavia</strong>. Le udienze sono seguite dallo Studio; il cliente viene informato per iscritto di ogni passaggio.",
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "consensuale o giudiziale, assegni e casa familiare"),
            ("attivita-unioni-civili", "Unioni civili e convivenze", "scioglimento, contratti di convivenza, diritti del convivente"),
            ("attivita-successioni", "Successioni ed eredità", "testamenti, legittima, divisioni"),
            ("attivita-recupero-crediti", "Recupero crediti", "fatture non pagate, decreti ingiuntivi"),
            ("attivita-negoziazione-assistita", "Negoziazione assistita", "accordi firmati dagli avvocati, senza udienze"),
        ],
        "faq": [
            ("Quanto dura una separazione consensuale?", "Con un accordo già definito, pochi mesi. Con la negoziazione assistita, dalla firma dell'accordo al nulla osta del Pubblico Ministero passano di solito alcune settimane."),
            ("Che documenti devo portare al primo colloquio?", "Dipende dalla materia. Per una separazione è utile la checklist dei documenti presente tra gli strumenti del sito, da stampare o spuntare dal telefono."),
            ("Posso pagare l'avvocato a rate?", "Le modalità di pagamento si concordano nel preventivo scritto, prima di iniziare."),
        ],
    },
    {
        "slug": "avvocato-abbiategrasso",
        "nome": "Abbiategrasso",
        "km": "circa 13 km",
        "min": "circa 20 minuti",
        "percorso": "Da Abbiategrasso si raggiunge Vigevano attraversando il Ticino. Lo Studio si trova in Via Egidio Sacchetti 14, vicino al centro storico.",
        "intro": "Abbiategrasso e l'Abbiatense sono legati a Vigevano da sempre: per lavoro, scuola, famiglia. Lo Studio Legale Pernorio assiste clienti di Abbiategrasso, Ozzero, Morimondo, Cassinetta di Lugagnano e dei comuni vicini, con la comodità di uno studio a venti minuti e l'esperienza sui tribunali di Pavia e Milano.",
        "tribunale": "La competenza per i comuni dell'Abbiatense non è uniforme: storicamente una parte era nel circondario del Tribunale di Vigevano, oggi accorpato a <strong>Pavia</strong>, mentre altri comuni fanno capo al <strong>Tribunale di Milano</strong>. Lo Studio opera in entrambi e verifica il tribunale competente per il singolo comune e il tipo di causa all'inizio della pratica.",
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "davanti al Tribunale di Pavia o di Milano"),
            ("attivita-affidamento-minori", "Affidamento dei figli", "anche tra genitori non sposati"),
            ("attivita-locazioni-comodato", "Affitti e comodato", "contratti, canoni, depositi cauzionali"),
            ("attivita-lavoro", "Diritto del lavoro", "licenziamenti, differenze retributive, TFR"),
            ("attivita-sinistri-responsabilita", "Incidenti e risarcimenti", "sinistri stradali, responsabilità professionale e medica"),
        ],
        "faq": [
            ("Abito ad Abbiategrasso: la mia causa va a Pavia o a Milano?", "Dipende dal comune esatto e dalla materia. Lo Studio lo verifica nel primo colloquio e segue le udienze in entrambi i tribunali."),
            ("Perché rivolgersi a uno studio di Vigevano e non di Milano?", "Per la vicinanza e il rapporto diretto: venti minuti d'auto, appuntamenti in tempi brevi, un unico avvocato che segue la pratica dall'inizio alla fine."),
            ("Lo Studio fa domiciliazioni per colleghi di Milano?", "Sì, lo Studio offre domiciliazioni e sostituzioni d'udienza presso i Tribunali di Pavia, Milano e Novara."),
        ],
    },
]

LOMELLINA = {
    "slug": "avvocato-lomellina",
    "title": "Avvocato in Lomellina · Studio Legale Pernorio, Vigevano",
    "description": "Avvocato civilista per Vigevano e la Lomellina: Mortara, Gambolò, Garlasco, Cassolnovo, Cilavegna, Robbio, Mede. Famiglia, eredità, casa, debiti. Tribunale di Pavia.",
    "h1": "Avvocato in Lomellina",
    "lead": "Lo Studio ha sede a Vigevano e assiste clienti di tutta la Lomellina e dell'Abbiatense, davanti ai Tribunali di Pavia, Milano e Novara.",
}

# Pagina costi ---------------------------------------------------------------

COSTI = {
    "slug": "costi-avvocato",
    "title": "Quanto costa un avvocato a Vigevano · Preventivo scritto",
    "description": "Come si calcola il compenso dell'avvocato, cosa include il preventivo scritto, spese vive e contributo unificato. Separazione, sfratto, recupero crediti: le voci di costo spiegate.",
    "label": "Costi e preventivo",
    "h1": "Quanto costa un avvocato",
    "lead": "Prima di iniziare lo Studio consegna un preventivo scritto. Qui spieghiamo da cosa dipende il costo di una pratica e quali spese si aggiungono al compenso.",
    "body": """
<p><strong>In sintesi:</strong> il compenso si concorda prima di iniziare, per iscritto. Dipende dal valore della pratica, dalla sua complessità e dalle fasi effettivamente svolte. A parte si pagano le spese vive (contributo unificato, notifiche, marche) e, se dovuti, IVA e contributo alla Cassa Forense.</p>

<h2>Il preventivo scritto</h2>
<p>La legge impone all'avvocato di comunicare al cliente, in forma scritta, la prevedibile misura del costo della prestazione, distinguendo tra oneri, spese e compenso. Lo Studio lo fa sempre, prima di iniziare: il cliente sa in anticipo quanto spenderà e quando.</p>
<p>Il preventivo indica:</p>
<ul>
<li>il <strong>compenso</strong> dell'avvocato, a forfait o per fasi;</li>
<li>le <strong>spese vive</strong> prevedibili, come contributo unificato, notifiche e copie;</li>
<li>gli <strong>oneri accessori</strong>: rimborso forfettario, contributo previdenziale (4%) e IVA, quando dovuta;</li>
<li>le <strong>modalità di pagamento</strong> concordate.</li>
</ul>

<h2>Come si calcola il compenso</h2>
<p>Il riferimento sono i parametri forensi del Ministero della Giustizia (D.M. 55/2014, aggiornato dal D.M. 147/2022). I parametri dividono ogni causa in fasi: studio della controversia, fase introduttiva, fase istruttoria e di trattazione, fase decisionale. Per ogni fase indicano un valore medio che varia in base al <strong>valore della causa</strong>.</p>
<p>Avvocato e cliente possono concordare un compenso diverso, purché proporzionato all'attività. Nelle pratiche stragiudiziali, come una diffida, una trattativa o un saldo e stralcio, si concorda spesso un importo fisso o una percentuale sul risultato economico ottenuto.</p>

<h2>Le spese vive più comuni</h2>
<ul>
<li><strong>Contributo unificato</strong>: la tassa per iscrivere una causa a ruolo. Varia in base al tipo e al valore del procedimento. Per la separazione consensuale e il divorzio congiunto è in misura fissa e contenuta.</li>
<li><strong>Marca da bollo</strong> per diritti forfettari e copie.</li>
<li><strong>Notifiche</strong> tramite ufficiale giudiziario o PEC.</li>
<li><strong>Consulenti</strong>: consulente tecnico, commercialista, perito, quando la pratica li richiede.</li>
<li><strong>Mediazione obbligatoria</strong>: le spese dell'organismo di mediazione, nelle materie in cui è condizione per fare causa.</li>
</ul>

<h2>Da cosa dipende il costo, materia per materia</h2>
<h3>Separazione e divorzio</h3>
<p>Una separazione consensuale o un divorzio congiunto costano molto meno di una procedura giudiziale, perché le fasi sono poche e l'accordo è già definito. Con la <a href="/attivita-negoziazione-assistita">negoziazione assistita</a> ciascun coniuge ha il proprio avvocato. La procedura giudiziale costa di più perché richiede istruttoria, udienze e talvolta una consulenza tecnica sui figli.</p>
<h3>Sfratto per morosità</h3>
<p>Se l'inquilino non si oppone, la procedura si chiude con la convalida e i costi restano contenuti. Se si oppone, diventa una causa ordinaria. Le spese legali possono essere poste a carico dell'inquilino moroso.</p>
<h3>Recupero crediti</h3>
<p>Diffida e decreto ingiuntivo hanno costi prevedibili. In caso di condanna le spese liquidate dal giudice sono a carico del debitore, ma il cliente le anticipa e le recupera solo se il debitore è solvibile.</p>
<h3>Saldo e stralcio</h3>
<p>Spesso il compenso si collega al risparmio ottenuto: una parte fissa più una percentuale sulla riduzione del debito. Tutto è indicato nel preventivo.</p>

<h2>Chi paga le spese se vinco la causa?</h2>
<p>Di regola il giudice condanna la parte che perde a rimborsare le spese legali dell'altra, nella misura che liquida secondo i parametri. Il giudice può però compensarle, in tutto o in parte, per esempio se la questione era nuova o incerta. Nelle cause di famiglia la compensazione è frequente.</p>

<h2>Il primo colloquio</h2>
<p>Al primo colloquio l'avvocato ascolta la situazione, esamina i documenti e spiega le possibili strade, con tempi e costi di ciascuna. Le condizioni del primo colloquio vengono comunicate al momento della prenotazione.</p>
""",
    "faq": [
        ("Il preventivo è obbligatorio?", "Sì: l'avvocato deve rendere nota al cliente, in forma scritta o digitale, la prevedibile misura del costo della prestazione, distinguendo oneri, spese e compenso."),
        ("Posso pagare a rate?", "Le modalità di pagamento si concordano nel preventivo. Per le pratiche lunghe il pagamento è in genere distribuito per fasi."),
        ("Se perdo la causa devo pagare anche l'avvocato dell'altra parte?", "Può succedere: di regola chi perde rimborsa le spese legali alla controparte, salvo che il giudice le compensi. Il rischio viene valutato con il cliente prima di iniziare."),
    ],
}

# Strumenti ------------------------------------------------------------------

STRUMENTI = [
    {
        "slug": "strumento-calcolo-quote-eredita",
        "titolo_breve": "Calcolo quote di eredità",
        "title": "Calcolo quote di eredità senza testamento · Strumento gratuito",
        "description": "Calcola come si divide un'eredità senza testamento tra coniuge, figli, genitori e fratelli secondo il codice civile (artt. 565-586). Gratuito, immediato.",
        "lead": "Chi eredita e quanto, quando non c'è un testamento. Inserisca i familiari in vita e lo strumento applica le regole del codice civile.",
        "intro": "Calcola la successione legittima (artt. 565-586 c.c.) tra coniuge, figli, genitori e fratelli.",
        "materia": ("attivita-successioni", "Successioni ed eredità"),
    },
    {
        "slug": "strumento-scadenze-multa",
        "titolo_breve": "Scadenze di una multa",
        "title": "Multa: entro quando pagare o fare ricorso · Calcolo scadenze",
        "description": "Inserisci la data di notifica del verbale e scopri le scadenze: sconto del 30% in 5 giorni, pagamento in 60 giorni, ricorso al Prefetto (60) o al Giudice di Pace (30).",
        "lead": "Dalla data di notifica del verbale, le scadenze per pagare con lo sconto, pagare in misura ridotta o fare ricorso.",
        "intro": "Sconto del 30%, pagamento in misura ridotta, ricorso al Prefetto o al Giudice di Pace: tutte le date.",
        "materia": ("attivita-codice-della-strada", "Ricorsi al Codice della strada"),
    },
    {
        "slug": "strumento-checklist-separazione",
        "titolo_breve": "Checklist documenti per la separazione",
        "title": "Documenti per la separazione: checklist da stampare",
        "description": "Tutti i documenti da preparare per una separazione o un divorzio: stato civile, redditi, casa, figli, conti. Checklist gratuita da spuntare o stampare.",
        "lead": "I documenti da raccogliere prima del primo colloquio per una separazione o un divorzio. Li spunti man mano: la lista resta salvata su questo dispositivo.",
        "intro": "Tutti i documenti da raccogliere prima del colloquio, da spuntare o stampare.",
        "materia": ("attivita-separazione-divorzio", "Separazione e divorzio"),
    },
]

CHECKLIST = [
    ("Stato civile e famiglia", [
        "Estratto per riassunto dell'atto di matrimonio (dal Comune in cui ci si è sposati)",
        "Certificato di residenza e stato di famiglia di entrambi i coniugi",
        "Documento d'identità e codice fiscale",
        "Eventuale convenzione di separazione dei beni o fondo patrimoniale",
        "Per il divorzio: copia del verbale di separazione omologato o della sentenza",
    ]),
    ("Redditi e lavoro", [
        "Dichiarazioni dei redditi degli ultimi tre anni (730 o Redditi PF) di entrambi",
        "Ultime buste paga o, per autonomi, ultimi bilanci o fatturato",
        "CU di pensioni, indennità e altri redditi",
        "Estratti dei conti correnti e dei depositi titoli degli ultimi 12 mesi",
    ]),
    ("Casa e patrimonio", [
        "Atto di acquisto o visura catastale della casa familiare",
        "Contratto di mutuo e piano di ammortamento, oppure contratto di affitto",
        "Elenco di altri immobili, auto e beni di valore, con intestatari",
        "Finanziamenti e prestiti in corso, con le rate mensili",
    ]),
    ("Figli", [
        "Certificati di nascita o stato di famiglia con i figli",
        "Spese ordinarie mensili per i figli (scuola, mensa, trasporti, attività)",
        "Spese straordinarie degli ultimi anni (mediche, dentistiche, viaggi di studio)",
        "Orari di lavoro dei genitori e organizzazione attuale della settimana",
    ]),
    ("Altro", [
        "Eventuali accordi già discussi tra i coniugi, anche informali",
        "Comunicazioni rilevanti (messaggi, email) conservate in copia",
        "Provvedimenti precedenti del tribunale, se esistono",
    ]),
]
