# -*- coding: utf-8 -*-
"""Migliorie guidate dalle ricerche reali di Google Search Console.

Fonte: export "Performance on Search" del 06/11/2026 (ultimi 3 mesi, web).
Per ogni pagina: le ricerche per cui compare già (impressioni) ma resta in
seconda-sesta pagina, o in prima pagina senza clic. Qui si aggiungono le
sezioni che rispondono proprio a quelle ricerche, le FAQ (con FAQPage) e
title/description più vicini a come le persone cercano.

Regola: solo informazioni generali verificabili sulla norma; niente numeri
inventati, niente promesse di risultato (Codice deontologico, artt. 17 e 35).
"""

AGGIORNATO = "novembre 2026"

# ---------------------------------------------------------------------------
# Title e description (entro 65 / 158 caratteri)
# ---------------------------------------------------------------------------

TITOLI = {
    # guide con molte impressioni e posizione 12-20
    "guida-saldo-e-stralcio-banche-finanziarie": "Saldo e stralcio: come funziona e quanto proporre alla banca",
    "guida-usucapione-quando-si-diventa-proprietari": "Usucapione di casa o terreno: quanti anni e come si ottiene",
    "guida-separazione-divorzio-unica-domanda": "Domanda di separazione e divorzio insieme: come funziona",
    # prima pagina ma zero clic: titolo più concreto
    "guida-amministrazione-di-sostegno": "Amministrazione di sostegno per un anziano: chi la chiede e come",
    "guida-sfratto-per-morosita": "Inquilino che non paga: come fare lo sfratto e quanto dura",
    "guida-affidamento-figli-condiviso-esclusivo": "Affidamento dei figli condiviso o esclusivo: come funziona",
    # pagine "avvocato + materia + Vigevano" in posizione 16-28
    "diritto-di-famiglia": "Avvocato diritto di famiglia a Vigevano: separazioni, figli",
    "attivita-separazione-divorzio": "Avvocato divorzista a Vigevano: separazione e divorzio",
    "attivita-successioni": "Avvocato eredità e testamenti a Vigevano · Studio Pernorio",
    "attivita-amministrazione-di-sostegno": "Avvocato amministrazione di sostegno a Vigevano",
}

DESCRIZIONI = {
    "guida-saldo-e-stralcio-banche-finanziarie": "Come funziona il saldo e stralcio con banca o finanziaria, anche dopo un decreto ingiuntivo o con mutuo e ipoteca: quanto proporre, liberatoria, CRIF.",
    "guida-usucapione-quando-si-diventa-proprietari": "Usucapione di una casa o di un terreno: 20, 10 o 5 anni, terreni agricoli, tasse pagate dal proprietario, cosa la interrompe e come farla riconoscere.",
    "guida-separazione-divorzio-unica-domanda": "Come presentare la domanda di separazione e divorzio, anche nello stesso ricorso: tempi, documenti da allegare, ricorso giudiziale o consensuale.",
    "guida-amministrazione-di-sostegno": "Per un genitore anziano o un familiare fragile: chi può chiedere l'amministrazione di sostegno, come si fa il ricorso al giudice tutelare, chi viene nominato.",
    "guida-sfratto-per-morosita": "Inquilino che non paga l'affitto: quando si può fare lo sfratto, i passaggi, il termine di grazia, i tempi e come recuperare i canoni arretrati.",
    "guida-affidamento-figli-condiviso-esclusivo": "Affidamento condiviso o esclusivo, per genitori sposati e non: le regole, quando un giudice lo esclude, il piano genitoriale e l'ascolto del figlio.",
    "diritto-di-famiglia": "Avvocato di diritto di famiglia a Vigevano: separazione, divorzio, affidamento e mantenimento dei figli, unioni civili. Avv. Daniela Pernorio.",
    "attivita-separazione-divorzio": "Avvocato divorzista a Vigevano: separazione consensuale o giudiziale, divorzio, assegni e casa familiare. Avv. Daniela Pernorio, preventivo scritto.",
    "attivita-amministrazione-di-sostegno": "Avvocato a Vigevano per l'amministrazione di sostegno di un anziano o di un familiare fragile: ricorso al giudice tutelare, rendiconti, autorizzazioni.",
    "attivita-successioni": "Avvocato a Vigevano per eredità, testamenti e donazioni: quote di legittima, divisioni tra eredi, impugnazione del testamento. Avv. Daniela Pernorio.",
}

# ---------------------------------------------------------------------------
# Sezioni aggiunte alle guide (prima della firma)
# ---------------------------------------------------------------------------

SEZIONI = {
    "guida-saldo-e-stralcio-banche-finanziarie": """
<h2>Come funziona il saldo e stralcio, passo per passo</h2>
<ol>
<li><strong>Raccolta dei documenti</strong>: contratto, estratti conto, lettere ricevute, eventuale decreto ingiuntivo o atto di pignoramento.</li>
<li><strong>Verifiche</strong> su chi è oggi il creditore, prescrizione e importo, come indicato sopra.</li>
<li><strong>Proposta scritta</strong> al creditore, motivata, con la somma offerta e i tempi di pagamento.</li>
<li><strong>Accordo firmato</strong> con la rinuncia al residuo e le garanzie elencate sopra.</li>
<li><strong>Pagamento</strong> con mezzo tracciabile, solo dopo la firma, e poi <strong>liberatoria</strong>.</li>
</ol>

<h2>Quanto proporre</h2>
<p>Non esiste una percentuale fissa né una tabella ufficiale. La cifra che un creditore accetta dipende soprattutto da:</p>
<ul>
<li><strong>chi detiene il credito</strong>: la banca originaria tratta in modo diverso da una società che ha acquistato il credito in un pacchetto, spesso pagandolo una piccola parte del valore nominale;</li>
<li><strong>l'età del debito</strong> e il rischio di prescrizione;</li>
<li><strong>le garanzie</strong>: un'ipoteca o un garante solvibile riducono il margine di trattativa;</li>
<li><strong>la situazione del debitore</strong>: redditi, beni pignorabili, altri debiti. Una proposta sostenibile e documentata è più credibile di una cifra alta che poi non si riesce a pagare;</li>
<li><strong>pagamento in un'unica soluzione o a rate</strong>: di solito il pagamento immediato consente uno sconto maggiore.</li>
</ul>

<h2>Saldo e stralcio dopo un decreto ingiuntivo</h2>
<p>Il saldo e stralcio è possibile anche quando il creditore ha già ottenuto un decreto ingiuntivo. Il decreto però cambia i rapporti di forza: se non viene opposto entro <strong>40 giorni</strong> dalla notifica diventa definitivo e il creditore può pignorare stipendio, conto o beni.</p>
<p>Per questo, appena si riceve un decreto ingiuntivo, conviene far verificare subito se ci sono motivi di opposizione (prescrizione, importi non dovuti, credito non provato): sono anche gli argomenti migliori per trattare. Se c'è già un pignoramento, l'accordo deve prevedere la <strong>rinuncia alla procedura esecutiva</strong> e chiarire chi paga le spese legali maturate.</p>

<h2>Mutuo, ipoteca e cancellazione</h2>
<p>Con un mutuo garantito da ipoteca il creditore ha meno incentivo a fare sconti, perché può far vendere l'immobile all'asta. La trattativa resta però possibile, soprattutto quando il credito è stato ceduto o quando la vendita all'asta renderebbe meno del previsto.</p>
<p>Nell'accordo va scritto in modo espresso che, una volta pagata la somma concordata, il creditore presta il <strong>consenso alla cancellazione dell'ipoteca</strong>, con i tempi e con l'indicazione di chi sostiene le spese notarili. Senza questa clausola l'ipoteca resta iscritta anche dopo il pagamento.</p>

<h2>Centrale Rischi e CRIF dopo il saldo e stralcio</h2>
<p>Chiudere il debito non cancella subito le segnalazioni. La posizione viene aggiornata come chiusa, ma lo storico resta visibile per il periodo previsto dalle regole di ciascuna banca dati: la cosiddetta "riabilitazione" non è immediata. È importante che l'accordo obblighi il creditore ad aggiornare la segnalazione e che il debitore controlli, dopo qualche mese, la propria posizione in Centrale Rischi (Banca d'Italia) e nei sistemi di informazione creditizia come CRIF.</p>

<h2>La liberatoria</h2>
<p>La quietanza liberatoria è la prova che il debito è chiuso. Deve indicare il rapporto (numero del contratto o del finanziamento), la somma pagata, la dicitura <em>a saldo e stralcio di ogni pretesa</em> relativa a quel rapporto e la firma di chi ha il potere di rilasciarla. Va conservata senza limiti di tempo: i crediti vengono rivenduti, e capita che un nuovo acquirente torni a chiedere un debito già chiuso.</p>

<h2>Se la proposta viene rifiutata</h2>
<p>Un primo rifiuto è frequente e non chiude la trattativa. Si può riformulare la proposta (importo diverso, rate, acconto), far valere in modo più puntuale i punti deboli del credito o, se ci sono motivi fondati, contestarlo in giudizio. Quando i debiti sono più di uno, conviene valutare le procedure di sovraindebitamento descritte sopra.</p>

<h2>Prestito, finanziaria, fido, carta revolving</h2>
<p>Le regole sono le stesse per un prestito personale, una cessione del quinto, un fido di conto corrente o una carta revolving. Cambiano i documenti da esaminare e, a volte, i termini di prescrizione. Se il prestito è ancora in corso e regolare, prima di parlare di saldo e stralcio va considerata l'<strong>estinzione anticipata</strong>: nel credito ai consumatori il rimborso anticipato è sempre possibile, con riduzione degli interessi non ancora maturati e un eventuale indennizzo per la banca entro i limiti di legge (art. 125-sexies del Testo unico bancario); per i mutui sulla casa di abitazione non si pagano penali.</p>
""",

    "guida-usucapione-quando-si-diventa-proprietari": """
<h2>Usucapione di una casa</h2>
<p>Per una casa o un appartamento il termine è di regola di <strong>vent'anni</strong> di possesso. Il caso tipico è l'immobile di famiglia abitato da sempre da un parente senza che sia mai stato intestato, o con proprietari ormai irreperibili. Conta come ci si è comportati: pagare le spese, fare lavori, decidere dell'immobile come farebbe il proprietario. Chi abita la casa con il permesso del proprietario (ad esempio in comodato) è solo detentore e non usucapisce, finché non manifesta in modo chiaro al proprietario di volerla tenere per sé.</p>

<h2>Usucapione di un terreno</h2>
<p>Anche per un terreno il termine ordinario è di vent'anni. Le prove tipiche sono la coltivazione, le recinzioni, le piantumazioni, i lavori di manutenzione, la testimonianza di vicini e confinanti. Una semplice tolleranza del proprietario (lasciar passare, lasciar parcheggiare) non basta.</p>

<h2>Terreni agricoli: 15 anni o 5 anni</h2>
<p>Per i <strong>fondi rustici con annessi fabbricati</strong> il Codice prevede termini più brevi (art. 1159-bis c.c.):</p>
<ul>
<li><strong>15 anni</strong> di possesso per i fondi situati in comuni classificati montani;</li>
<li><strong>5 anni</strong> se il terreno è stato acquistato in buona fede da chi non era proprietario, con un titolo idoneo regolarmente trascritto.</li>
</ul>
<p>Le stesse regole valgono, fuori dai comuni montani, per i piccoli fondi rustici entro i limiti di reddito fissati dalla legge speciale (legge 346/1976), che prevede anche un procedimento semplificato davanti al Tribunale. Il termine di 5 anni, quindi, non si applica a chiunque coltivi un terreno: servono il titolo trascritto e la buona fede.</p>

<h2>Se il proprietario paga le tasse, l'usucapione si interrompe?</h2>
<p>No, di per sé. Secondo un orientamento costante della Corte di Cassazione, il pagamento delle imposte (IMU, tributi) da parte del proprietario non interrompe il possesso di chi sta usucapendo. Allo stesso modo, il fatto che sia il possessore a pagarle è un indizio utile, ma da solo non prova il possesso.</p>

<h2>Cosa interrompe l'usucapione</h2>
<ul>
<li>una <strong>domanda giudiziale</strong> del proprietario per riavere il bene;</li>
<li>il <strong>riconoscimento</strong> del diritto del proprietario da parte del possessore, ad esempio chiedendogli il permesso o proponendo di acquistare;</li>
<li>la <strong>perdita del possesso per oltre un anno</strong> (art. 1167 c.c.).</li>
</ul>
<p>Una semplice lettera di diffida o di messa in mora, invece, secondo la Cassazione non basta a interrompere il possesso.</p>

<h2>Usucapione tra eredi o comproprietari</h2>
<p>Chi è già comproprietario, ad esempio un coerede che abita da solo la casa dei genitori, non usucapisce solo perché la usa. Deve dimostrare di averla posseduta in modo esclusivo, impedendo agli altri di servirsene e comportandosi da unico proprietario, per tutto il tempo richiesto. È una prova più difficile, da valutare con attenzione prima di avviare una causa.</p>
""",

    "guida-separazione-divorzio-unica-domanda": """
<h2>Come si presenta la domanda di separazione o di divorzio</h2>
<p>Le strade sono tre, sia per la separazione sia per il divorzio:</p>
<ul>
<li><strong>ricorso al Tribunale</strong>: congiunto, se i coniugi sono d'accordo su tutto, oppure giudiziale, se l'accordo manca;</li>
<li><strong>negoziazione assistita</strong> da avvocati, quando c'è un accordo, senza udienze;</li>
<li><strong>davanti al sindaco</strong>, come ufficiale di stato civile, solo se non ci sono figli minori, maggiorenni non autosufficienti o con disabilità grave, e senza trasferimenti di beni.</li>
</ul>
<p>Il Tribunale competente è di regola quello del luogo in cui vivono abitualmente i figli minori; se non ci sono figli minori, quello di residenza del coniuge convenuto. Per chi vive a Vigevano e in Lomellina è il Tribunale di Pavia.</p>

<h2>Ricorso per divorzio giudiziale: cosa contiene</h2>
<p>Con il rito unico il ricorso deve essere completo fin dall'inizio: i fatti, le domande su figli, casa e assegni, le prove. Vanno allegati:</p>
<ul>
<li>le <strong>dichiarazioni dei redditi degli ultimi tre anni</strong>;</li>
<li>la documentazione su immobili, conti, investimenti e altri beni;</li>
<li>se ci sono figli minori, un <strong>piano genitoriale</strong> con la loro routine: scuola, attività, frequentazioni, vacanze.</li>
</ul>
<p>Le stesse regole valgono per il ricorso di separazione giudiziale. Il coniuge convenuto deve rispondere con un atto altrettanto completo, entro i termini fissati dal giudice.</p>

<h2>Documenti per la separazione consensuale</h2>
<p>Per un ricorso congiunto o una negoziazione assistita servono di solito: estratto dell'atto di matrimonio, certificati di residenza e stato di famiglia (o autocertificazione), dichiarazioni dei redditi, documenti su casa, mutuo e conti, e l'accordo su figli e mantenimento. Per prepararli senza dimenticare nulla c'è la <a href="/strumento-checklist-separazione">checklist per la separazione</a>, da spuntare o stampare.</p>

<h2>Quando si può chiedere il divorzio</h2>
<p>Dopo la separazione servono <strong>dodici mesi</strong> dalla prima udienza davanti al giudice nella separazione giudiziale, <strong>sei mesi</strong> nella separazione consensuale, anche se ottenuta con negoziazione assistita o in Comune. Con la domanda unica descritta sopra non serve aspettare per depositare: si deposita tutto insieme e il giudice esamina il divorzio quando i termini sono maturati.</p>
""",

    "guida-amministrazione-di-sostegno": """
<h2>Tutore o amministratore di sostegno per un anziano?</h2>
<p>Molti cercano un "tutore" per un genitore anziano. Oggi, nella grande maggioranza dei casi, la misura giusta è l'amministrazione di sostegno: è più flessibile e lascia alla persona tutta l'autonomia che può conservare. L'interdizione, con la nomina di un tutore, è ormai riservata ai casi in cui nessuna misura meno incisiva è sufficiente.</p>
""",
}

FAQ = {
    "guida-saldo-e-stralcio-banche-finanziarie": [
        ("Quanto si può proporre in un saldo e stralcio?",
         "Non c'è una percentuale fissa. Dipende da chi detiene il credito (banca o società che lo ha acquistato), dall'età del debito, dalle garanzie e dalla capacità di pagamento del debitore. Una proposta sostenibile e motivata è più efficace di una cifra alta che non si riesce a pagare."),
        ("Si può fare il saldo e stralcio dopo un decreto ingiuntivo?",
         "Sì. Ma il decreto non opposto entro 40 giorni dalla notifica diventa definitivo e permette il pignoramento: conviene far valutare subito se ci sono motivi di opposizione, che sono anche argomenti per trattare."),
        ("Dopo il saldo e stralcio l'ipoteca viene cancellata?",
         "Solo se il creditore presta il consenso alla cancellazione. Per questo l'accordo deve prevederlo espressamente, con i tempi e l'indicazione di chi paga le spese notarili."),
        ("Il saldo e stralcio cancella la segnalazione in Centrale Rischi o CRIF?",
         "Non subito. La posizione viene aggiornata come chiusa, ma lo storico resta visibile per il periodo previsto dalle regole di ciascuna banca dati. L'accordo deve obbligare il creditore ad aggiornare la segnalazione."),
        ("Cosa deve contenere la liberatoria?",
         "Il riferimento al contratto, la somma pagata, la formula a saldo e stralcio di ogni pretesa relativa a quel rapporto e la firma di chi può rilasciarla. Va conservata senza limiti di tempo."),
        ("Posso estinguere un prestito in anticipo senza penali?",
         "Nel credito ai consumatori il rimborso anticipato è sempre possibile, con riduzione degli interessi futuri; la banca può chiedere un indennizzo solo entro i limiti dell'art. 125-sexies del Testo unico bancario. Per i mutui sulla casa di abitazione non sono dovute penali."),
    ],
    "guida-usucapione-quando-si-diventa-proprietari": [
        ("Quanti anni servono per l'usucapione di una casa?",
         "Di regola vent'anni di possesso continuo, pacifico e pubblico. Dieci anni se la casa è stata acquistata in buona fede da chi non era proprietario, con un titolo idoneo trascritto."),
        ("Un terreno agricolo si può usucapire in 5 anni?",
         "Solo per i fondi rustici con annessi fabbricati e solo se il terreno è stato acquistato in buona fede, con un titolo idoneo regolarmente trascritto (art. 1159-bis c.c.). Senza titolo il termine è di 15 anni per i fondi rustici nei comuni montani e per i piccoli fondi entro i limiti di reddito della legge 346/1976; negli altri casi è di 20 anni."),
        ("Se il proprietario paga l'IMU, l'usucapione si interrompe?",
         "No. Secondo la Cassazione il pagamento delle imposte da parte del proprietario non interrompe il possesso altrui. Lo interrompono una domanda giudiziale, il riconoscimento del diritto del proprietario o la perdita del possesso per oltre un anno."),
        ("Un coerede può usucapire la casa dei genitori?",
         "Sì, ma deve dimostrare di averla posseduta in modo esclusivo, impedendo agli altri coeredi di usarla, per tutto il tempo richiesto. Usarla da solo con la tolleranza degli altri non basta."),
        ("Serve una causa per ottenere l'usucapione?",
         "Non sempre. Se tutti gli interessati sono d'accordo, l'usucapione può essere accertata con un accordo in mediazione trascritto nei registri immobiliari. Altrimenti serve una causa, preceduta dal tentativo obbligatorio di mediazione."),
    ],
    "guida-separazione-divorzio-unica-domanda": [
        ("Come si presenta la domanda di divorzio?",
         "Con ricorso al Tribunale (congiunto o giudiziale), con la negoziazione assistita da avvocati oppure, in assenza di figli minori o non autosufficienti e di trasferimenti di beni, davanti al sindaco come ufficiale di stato civile."),
        ("Quali documenti servono per il ricorso di separazione o divorzio?",
         "Le dichiarazioni dei redditi degli ultimi tre anni, la documentazione su immobili, conti e investimenti e, se ci sono figli minori, un piano genitoriale. Per la consensuale anche l'accordo su figli, casa e mantenimento."),
        ("Dopo quanto tempo dalla separazione si può divorziare?",
         "Dodici mesi dalla prima udienza nella separazione giudiziale, sei mesi nella consensuale, anche se ottenuta con negoziazione assistita o in Comune."),
        ("Si possono chiedere separazione e divorzio nello stesso ricorso?",
         "Sì. Dalla Riforma Cartabia la domanda di divorzio può essere proposta insieme a quella di separazione; la Cassazione (sent. 28727/2023) lo ha ammesso anche per il ricorso congiunto. Il giudice esamina il divorzio quando i termini sono maturati."),
    ],
    "guida-amministrazione-di-sostegno": [
        ("Per un genitore anziano serve un tutore o un amministratore di sostegno?",
         "Di regola un amministratore di sostegno: è la misura più flessibile e lascia alla persona l'autonomia che può conservare. L'interdizione con nomina di un tutore è oggi residuale."),
        ("Dove si presenta il ricorso?",
         "Al Giudice Tutelare del Tribunale del luogo in cui la persona vive, con la certificazione medica e l'indicazione dei familiari. Per chi vive a Vigevano e in Lomellina è il Tribunale di Pavia."),
        ("Chi può chiedere l'amministrazione di sostegno?",
         "La persona interessata, il coniuge o il convivente stabile, i parenti entro il quarto grado, gli affini entro il secondo, il tutore o curatore e il Pubblico Ministero."),
    ],
    "guida-sfratto-per-morosita": [
        ("Dopo quanto tempo di mancato pagamento si può fare lo sfratto?",
         "Nelle locazioni abitative quando il canone non è pagato decorsi venti giorni dalla scadenza, oppure quando gli oneri accessori non pagati superano due mensilità del canone."),
        ("L'inquilino può evitare lo sfratto pagando?",
         "Nelle locazioni abitative può chiedere all'udienza un termine di grazia, fino a novanta giorni, per pagare canoni, spese e interessi. Se paga entro il termine, lo sfratto non viene convalidato."),
        ("Insieme allo sfratto si recuperano gli affitti arretrati?",
         "Sì: si può chiedere al giudice un decreto ingiuntivo per i canoni scaduti e per quelli che maturano fino al rilascio, utile per pignorare stipendio, conto o altri beni dell'inquilino."),
    ],
}

# Fonti normative in più (si aggiungono a tools/fonti.py)
FONTI_EXTRA = {
    "guida-usucapione-quando-si-diventa-proprietari": [
        ("Art. 1159-bis c.c., usucapione speciale dei fondi rustici", "cc", "1159bis"),
        ("Art. 1165 c.c., applicazione delle norme sulla prescrizione", "cc", "1165"),
        ("Art. 1167 c.c., interruzione per perdita del possesso", "cc", "1167"),
    ],
    "guida-saldo-e-stralcio-banche-finanziarie": [
        ("Art. 2882 c.c., cancellazione dell'ipoteca", "cc", "2882"),
        ("Art. 125-sexies Testo unico bancario, rimborso anticipato", "tub", "125sexies"),
        ("Art. 645 c.p.c., opposizione al decreto ingiuntivo", "cpc", "645"),
    ],
}

# Redirect di vecchi indirizzi visti in Search Console che oggi non esistono
VECCHI_URL = {
    "/contact.html": "/contatti",
    "/contact": "/contatti",
    "/news.html": "/guide",
    "/news": "/guide",
    "/index.html": "/",
}

# ---------------------------------------------------------------------------
# Inviti a chiamare dentro le guide
# ---------------------------------------------------------------------------
# Chi legge una guida ha un problema concreto. Il riquadro compare a metà
# articolo, dove il lettore ha capito il tema ma non ha ancora finito di leggere,
# e parla della sua situazione. Toni informativi, nessuna promessa di risultato.
# Formato: slug -> (domanda, testo)

CTA = {
    "guida-saldo-e-stralcio-banche-finanziarie": ("Ha ricevuto una lettera da una banca, una finanziaria o una società di recupero?", "Prima di rispondere o di pagare, conviene far controllare il debito: chi lo chiede, se è prescritto, se l'importo è giusto. Se è arrivato un decreto ingiuntivo, ci sono 40 giorni per opporsi."),
    "guida-usucapione-quando-si-diventa-proprietari": ("Usa da anni una casa o un terreno che non è intestato a lei?", "Con le visure e qualche documento si può capire in un colloquio se ci sono i requisiti e quale strada è più rapida: accordo in mediazione o causa."),
    "guida-separazione-divorzio-unica-domanda": ("State pensando a separazione o divorzio?", "In un primo colloquio si capisce quale strada è possibile nel vostro caso (consensuale, giudiziale, negoziazione assistita), con tempi e costi messi per iscritto prima di iniziare."),
    "guida-amministrazione-di-sostegno": ("Un genitore o un familiare non riesce più a gestire pagamenti e pratiche?", "Lo Studio prepara il ricorso al Giudice Tutelare di Pavia e segue l'amministratore nei rendiconti e nelle autorizzazioni. Se il familiare non può spostarsi, si parte da un colloquio con lei."),
    "guida-sfratto-per-morosita": ("L'inquilino non paga?", "Ogni mese di attesa è un canone in più da recuperare. Con il contratto e l'elenco dei mancati pagamenti si valuta subito se e come procedere."),
    "guida-affidamento-figli-condiviso-esclusivo": ("Dovete decidere come organizzare la vita dei figli?", "Un colloquio aiuta a capire cosa è ragionevole chiedere, come scrivere un piano genitoriale che funzioni e quando ha senso andare dal giudice."),
    "guida-assegno-mantenimento-figli": ("Deve fissare o rivedere un assegno di mantenimento?", "Con i redditi delle due parti e le spese dei figli si può stimare un importo ragionevole e capire se c'è spazio per un accordo."),
    "guida-casa-familiare-separazione": ("Vi state separando e c'è una casa di mezzo?", "Proprietà, mutuo e figli cambiano le risposte. Con l'atto di acquisto e il mutuo si valutano le soluzioni possibili prima di firmare qualsiasi accordo."),
    "guida-costo-separazione-consensuale": ("Vuole sapere quanto costerebbe la sua separazione?", "Lo Studio fa un preventivo scritto dopo il primo colloquio, prima di iniziare. Nessuna sorpresa sui costi."),
    "guida-divorzio-tempi": ("Siete separati e volete divorziare?", "Basta la sentenza o l'accordo di separazione per verificare se i termini sono maturati e quale strada è più rapida."),
    "guida-fine-convivenza-diritti": ("La convivenza è finita e non sapete come dividere casa, spese e figli?", "In un colloquio si chiarisce cosa spetta a ciascuno e come mettere l'accordo per iscritto."),
    "guida-scioglimento-unione-civile": ("Volete sciogliere l'unione civile?", "Si può fare anche senza tribunale, se c'è accordo. In un colloquio si sceglie la strada più semplice per il vostro caso."),
    "guida-eredita-con-debiti": ("È morto un familiare e teme che ci siano debiti?", "Prima di compiere qualsiasi atto sull'eredità conviene un parere: alcuni comportamenti valgono come accettazione e fanno rispondere dei debiti."),
    "guida-testamento-olografo": ("Vuole fare testamento o ha trovato un testamento da verificare?", "Un controllo prima evita molte liti dopo: requisiti, quote di legittima, pubblicazione dal notaio."),
    "guida-successioni-autoliquidazione-imposta": ("Deve presentare una dichiarazione di successione?", "Con l'elenco dei beni e degli eredi si capisce cosa va dichiarato, quanto si paga e se ci sono questioni da risolvere tra eredi."),
    "guida-deposito-cauzionale-affitto": ("Il proprietario non le restituisce il deposito cauzionale?", "Con il contratto e il verbale di riconsegna si valuta se le trattenute sono legittime e come chiedere la restituzione."),
    "guida-diritti-inquilino": ("Ha un problema con il proprietario di casa?", "Contratto alla mano, in un colloquio si chiarisce cosa può pretendere e come farlo per iscritto."),
    "guida-impugnare-delibera-condominiale": ("Vuole contestare una delibera del condominio?", "I termini sono brevi: 30 giorni. Conviene far vedere subito il verbale."),
    "guida-incidente-stradale-cosa-fare": ("Ha avuto un incidente e l'assicurazione non risponde o offre poco?", "Con il CID, le foto e i referti medici si valuta se l'offerta è congrua e come chiedere il risarcimento completo."),
    "guida-licenziamento-cosa-fare": ("Ha ricevuto una lettera di licenziamento?", "Ci sono 60 giorni per impugnarlo. Porti la lettera e il contratto: in un colloquio si capisce se ci sono margini."),
    "guida-multa-autovelox-2026": ("Ha ricevuto una multa e pensa di contestarla?", "I termini sono brevi: 30 giorni per il Giudice di Pace, 60 per il Prefetto. Con il verbale si valuta subito se il ricorso ha senso."),
    "guida-pignoramento-stipendio-pensione": ("Le è arrivato un pignoramento o un atto di precetto?", "Con l'atto ricevuto si verifica se gli importi e i limiti di legge sono rispettati e se c'è spazio per un accordo con il creditore."),
    "guida-prestito-tra-privati": ("Ha prestato soldi e non le vengono restituiti?", "Bonifici, messaggi e scritture possono bastare come prova. In un colloquio si valuta la strada più rapida per recuperarli."),
    "guida-negoziazione-assistita-o-mediazione": ("Vuole chiudere una lite senza una causa?", "In un colloquio si sceglie lo strumento giusto, mediazione o negoziazione assistita, e si prepara la proposta."),
}
CTA_DEFAULT = ("Ha una situazione simile?", "Ne parli con l'avvocato: in un primo colloquio si capiscono le strade possibili, i tempi e i costi, messi per iscritto prima di iniziare.")
