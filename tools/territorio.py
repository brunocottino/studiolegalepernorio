# -*- coding: utf-8 -*-
"""Contenuto locale delle pagine per materia e collegamenti guide <-> materie.

Perché: nelle statistiche del 7-15 novembre 2026 Google porta quasi solo lettori
di guide (212 visite su 243), mentre le pagine "avvocato + materia a Vigevano"
ricevono 8 visite e stanno in seconda o terza pagina. Erano pagine brevi, senza
nulla di locale e senza collegamenti alle guide. Qui si aggiungono:

- LOCALE: per ogni materia, dove si svolge la pratica per chi vive a Vigevano e
  in Lomellina (ufficio competente, passaggi obbligati prima della causa);
- ANCORA: il testo del collegamento dalla guida alla pagina della materia,
  scritto come le persone cercano ("avvocato per ... a Vigevano");
- GUIDE_EXTRA: guide utili a una materia anche se nate sotto un'altra.

Regola: solo indicazioni generali verificabili sulla norma, senza importi né
promesse di risultato (Codice deontologico, artt. 17 e 35). I testi vanno
riletti dall'avvocata prima della pubblicazione.
"""

PAVIA = "<strong>Tribunale di Pavia</strong>"
VERIFICA = " Lo Studio verifica la competenza all'inizio della pratica."

LOCALE = {
    "separazione-divorzio": (
        f"<p>Per chi vive a Vigevano e in Lomellina il ricorso per separazione o divorzio si presenta, di regola, al {PAVIA}, "
        "competente per tutto il territorio dell'ex Tribunale di Vigevano. Lo Studio vi segue abitualmente le udienze.</p>"
        "<p>Con la <a href='/attivita-negoziazione-assistita'>negoziazione assistita</a> non ci sono udienze: gli incontri si tengono in Studio a Vigevano "
        "e l'accordo viene poi trasmesso alla Procura e al Comune. L'accordo davanti all'ufficiale di stato civile, quando la legge lo consente, "
        "si firma nel Comune di residenza di uno dei coniugi o in quello in cui il matrimonio è stato iscritto o trascritto.</p>"
    ),
    "affidamento-minori": (
        "<p>Per le decisioni su affidamento, collocamento e mantenimento è competente, di regola, il tribunale del luogo in cui il minore ha la residenza abituale. "
        f"Per i figli che vivono a Vigevano, Mortara, Gambolò, Garlasco e negli altri comuni della Lomellina è il {PAVIA}, "
        "sia quando i genitori sono sposati sia quando non lo sono. Lo Studio vi segue abitualmente le udienze.</p>"
        "<p>Quando i genitori raggiungono un accordo, lo si può formalizzare anche con la <a href='/attivita-negoziazione-assistita'>negoziazione assistita</a>, "
        "senza udienze: gli incontri si tengono in Studio a Vigevano.</p>"
    ),
    "unioni-civili": (
        "<p>Lo scioglimento dell'unione civile si chiede al tribunale oppure, se c'è accordo, con la negoziazione assistita o davanti all'ufficiale di stato civile. "
        f"Per chi vive a Vigevano e in Lomellina è competente, di regola, il {PAVIA}.</p>"
        "<p>Per porre fine a una convivenza di fatto non serve un procedimento in tribunale. Restano però da regolare la casa, i beni acquistati insieme e, "
        "se ci sono figli, affidamento e mantenimento: per questi ultimi è competente lo stesso Tribunale di Pavia.</p>"
    ),
    "successioni": (
        "<p>La successione si apre nel luogo dell'ultimo domicilio della persona defunta. Se viveva a Vigevano o in un comune della Lomellina, "
        f"per le cause tra eredi è competente il {PAVIA}. Nella cancelleria dello stesso tribunale si possono ricevere la rinuncia all'eredità "
        "e l'accettazione con beneficio d'inventario, in alternativa al notaio.</p>"
        "<p>La dichiarazione di successione si presenta invece all'Agenzia delle Entrate, di regola in via telematica. "
        "Prima di una causa di divisione ereditaria la legge impone un tentativo di <a href='/attivita-mediazione-civile'>mediazione</a>.</p>"
    ),
    "amministrazione-di-sostegno": (
        "<p>Il ricorso si presenta al giudice tutelare del luogo in cui la persona da assistere ha la residenza o il domicilio. "
        f"Per chi vive a Vigevano e in Lomellina è il giudice tutelare presso il {PAVIA}.</p>"
        "<p>Se la persona vive stabilmente in una casa di riposo o in un'altra struttura, può contare il luogo in cui si trova di fatto: "
        "lo Studio lo verifica prima di depositare il ricorso. Il giudice sente personalmente il beneficiario e, se questi non può spostarsi, si reca dove si trova.</p>"
    ),
    "locazioni-comodato": (
        "<p>Per le liti su affitti e comodato è competente il tribunale del luogo in cui si trova l'immobile. "
        f"Per case, negozi e capannoni a Vigevano e in Lomellina è il {PAVIA}.</p>"
        "<p>Prima della causa la legge impone, in materia di locazione e comodato, un tentativo di <a href='/attivita-mediazione-civile'>mediazione</a>. "
        "Molte questioni, come la restituzione del deposito o i lavori a carico del proprietario, si chiudono già con una diffida scritta dall'avvocato.</p>"
    ),
    "sfratti": (
        "<p>L'intimazione di sfratto si propone davanti al tribunale del luogo in cui si trova l'immobile. "
        f"Per gli immobili a Vigevano, Mortara, Garlasco, Gambolò e negli altri comuni lomellini è il {PAVIA}.</p>"
        "<p>Dopo la convalida, se l'inquilino non lascia l'immobile, il rilascio viene eseguito dall'ufficiale giudiziario. "
        "Lo Studio segue tutti i passaggi, dalla lettera di diffida alla riconsegna delle chiavi, e il recupero dei canoni non pagati.</p>"
    ),
    "usucapione-diritti-reali": (
        "<p>Le cause su proprietà, usucapione, confini e servitù si svolgono davanti al tribunale del luogo in cui si trova l'immobile. "
        f"Per terreni e fabbricati a Vigevano e in Lomellina è il {PAVIA}.</p>"
        "<p>Prima della causa è obbligatorio un tentativo di <a href='/attivita-mediazione-civile'>mediazione</a>. "
        "L'accordo di mediazione che accerta l'usucapione, con le firme autenticate, può essere trascritto nei registri immobiliari.</p>"
    ),
    "condominio": (
        "<p>Per impugnare una delibera o agire in una lite condominiale è competente il giudice del luogo in cui si trova l'edificio. "
        f"Per i condomini di Vigevano e della Lomellina è, secondo la materia e il valore, il Giudice di Pace o il {PAVIA}.</p>"
        "<p>Prima della causa è obbligatorio un tentativo di <a href='/attivita-mediazione-civile'>mediazione</a>. "
        "Le delibere annullabili vanno impugnate entro trenta giorni: conviene far vedere subito il verbale.</p>"
    ),
    "saldo-e-stralcio": (
        "<p>Il saldo e stralcio è una trattativa: non richiede un giudice. Lo Studio tratta per iscritto con la banca, la finanziaria "
        "o la società di recupero, ovunque abbiano sede, e il cliente viene in Studio a Vigevano solo per il colloquio e per la firma.</p>"
        f"<p>Se è già in corso un pignoramento dello stipendio, della pensione o del conto, la procedura si svolge di regola davanti al tribunale "
        f"del luogo in cui risiede il debitore: per chi vive a Vigevano e in Lomellina, il {PAVIA}.</p>"
    ),
    "recupero-crediti": (
        "<p>Il decreto ingiuntivo si chiede al Giudice di Pace o al tribunale, secondo il valore del credito e le regole sulla competenza. "
        f"Per i debitori che risiedono a Vigevano e in Lomellina il tribunale competente è il {PAVIA}: è lì che, di regola, si svolge anche "
        "il pignoramento dello stipendio, della pensione o del conto corrente.</p>"
        "<p>Lo Studio recupera crediti anche verso debitori di altre province: il deposito degli atti avviene in via telematica.</p>"
    ),
    "crisi-impresa": (
        "<p>Le procedure di sovraindebitamento si aprono davanti al tribunale del luogo in cui il debitore ha il centro dei propri interessi, "
        f"che per le persone fisiche coincide di regola con la residenza. Per chi vive a Vigevano e in Lomellina è il {PAVIA}.</p>"
        "<p>La domanda si presenta con l'assistenza di un Organismo di composizione della crisi (OCC), che redige la relazione richiesta dalla legge. "
        "Lo Studio prepara la documentazione e segue il rapporto con l'Organismo e con il tribunale.</p>"
    ),
    "contratti": (
        "<p>Molte liti sui contratti si chiudono prima della causa, con una diffida ben scritta o con la "
        "<a href='/attivita-negoziazione-assistita'>negoziazione assistita</a>, che in alcuni casi è obbligatoria.</p>"
        f"<p>Quando serve il giudice, la competenza dipende dal contratto, dal valore e dalla residenza delle parti: per chi vive o ha sede a Vigevano "
        f"e in Lomellina è spesso il {PAVIA}. Il contratto può però indicare un foro diverso: è una delle prime cose che lo Studio controlla.</p>"
    ),
    "sinistri-responsabilita": (
        "<p>Per i danni da incidente stradale la causa si può proporre, tra gli altri, davanti al giudice del luogo in cui è avvenuto il sinistro. "
        f"Per gli incidenti a Vigevano e in Lomellina è, secondo il valore, il Giudice di Pace o il {PAVIA}.</p>"
        "<p>Prima della causa la legge impone la richiesta di risarcimento all'assicurazione e, per i danni da circolazione di veicoli, "
        "la <a href='/attivita-negoziazione-assistita'>negoziazione assistita</a>. Spesso l'accordo si raggiunge in questa fase.</p>"
    ),
    "codice-della-strada": (
        "<p>Il ricorso si presenta al Prefetto o al Giudice di Pace del luogo in cui è stata commessa la violazione, non di quello in cui si abita. "
        "Per le multe prese a Vigevano e negli altri comuni della provincia di Pavia il Prefetto è quello di Pavia.</p>"
        "<p>La pratica si prepara in Studio a Vigevano, con il verbale e la prova della notifica. "
        "I termini sono brevi: lo <a href='/strumento-scadenze-multa'>strumento delle scadenze</a> calcola le date a partire dal giorno di notifica.</p>"
    ),
    "lavoro": (
        "<p>Le cause di lavoro si svolgono davanti al tribunale in funzione di giudice del lavoro. È competente il giudice del luogo in cui è sorto il rapporto "
        "oppure quello in cui si trova l'azienda o la sede a cui il lavoratore era addetto.</p>"
        f"<p>Per chi lavora a Vigevano e in Lomellina è di regola il {PAVIA}. Per chi lavora nel Milanese o nel Novarese può essere il Tribunale di Milano "
        "o quello di Novara, davanti ai quali lo Studio opera.</p>"
    ),
    "negoziazione-assistita": (
        "<p>Gli incontri si tengono in Studio a Vigevano o, se le parti sono d'accordo, a distanza. Non c'è un giudice e non ci sono udienze: "
        "l'accordo firmato dalle parti e dagli avvocati vale come titolo esecutivo.</p>"
        "<p>In materia di famiglia l'accordo viene trasmesso al Procuratore della Repubblica presso il tribunale competente, "
        f"che per Vigevano e la Lomellina è il {PAVIA}.</p>"
    ),
    "mediazione-civile": (
        "<p>La domanda di mediazione si presenta a un organismo che ha sede nel luogo del giudice competente per la causa. "
        f"Per le liti che spetterebbero al {PAVIA}, come quelle su immobili a Vigevano e in Lomellina, l'organismo va scelto in quel circondario.</p>"
        "<p>L'avvocato assiste la parte agli incontri, che possono svolgersi anche da remoto. Se si raggiunge l'accordo, il verbale vale come titolo esecutivo.</p>"
    ),
}

# Titolo della sezione locale: "<materia> a Vigevano e in Lomellina"
TITOLO_LOCALE = {
    "separazione-divorzio": "Separazione e divorzio a Vigevano e in Lomellina: dove si presenta il ricorso",
    "affidamento-minori": "Affidamento dei figli a Vigevano e in Lomellina: quale tribunale decide",
    "unioni-civili": "Unioni civili e convivenze a Vigevano e in Lomellina",
    "successioni": "Eredità e successioni a Vigevano e in Lomellina: a chi rivolgersi",
    "amministrazione-di-sostegno": "Amministrazione di sostegno a Vigevano e in Lomellina: dove si presenta il ricorso",
    "locazioni-comodato": "Affitti e comodato a Vigevano e in Lomellina: dove si discute la lite",
    "sfratti": "Sfratto a Vigevano e in Lomellina: quale tribunale e quali passaggi",
    "usucapione-diritti-reali": "Usucapione, confini e servitù a Vigevano e in Lomellina",
    "condominio": "Liti di condominio a Vigevano e in Lomellina: giudice e mediazione",
    "saldo-e-stralcio": "Saldo e stralcio per chi vive a Vigevano e in Lomellina",
    "recupero-crediti": "Recupero crediti a Vigevano e in Lomellina: giudice competente",
    "crisi-impresa": "Sovraindebitamento a Vigevano e in Lomellina: dove si presenta la domanda",
    "contratti": "Contratti e liti contrattuali a Vigevano e in Lomellina",
    "sinistri-responsabilita": "Incidenti e risarcimenti a Vigevano e in Lomellina",
    "codice-della-strada": "Ricorso contro una multa presa a Vigevano o in provincia di Pavia",
    "lavoro": "Cause di lavoro a Vigevano e in Lomellina: quale tribunale",
    "negoziazione-assistita": "Negoziazione assistita a Vigevano: come si svolge",
    "mediazione-civile": "Mediazione civile a Vigevano e in Lomellina: dove si svolge",
}

# Testo del collegamento dalla guida alla pagina della materia
ANCORA = {
    "attivita-separazione-divorzio": "avvocato divorzista a Vigevano",
    "attivita-affidamento-minori": "avvocato per l'affidamento dei figli a Vigevano",
    "attivita-unioni-civili": "avvocato per unioni civili e convivenze a Vigevano",
    "attivita-successioni": "avvocato per eredità e testamenti a Vigevano",
    "attivita-amministrazione-di-sostegno": "avvocato per l'amministrazione di sostegno a Vigevano",
    "attivita-locazioni-comodato": "avvocato per affitti e locazioni a Vigevano",
    "attivita-sfratti": "avvocato per sfratti a Vigevano",
    "attivita-usucapione-diritti-reali": "avvocato per usucapione e diritti reali a Vigevano",
    "attivita-condominio": "avvocato per il condominio a Vigevano",
    "attivita-saldo-e-stralcio": "avvocato per saldo e stralcio a Vigevano",
    "attivita-recupero-crediti": "avvocato per il recupero crediti a Vigevano",
    "attivita-crisi-impresa": "avvocato per il sovraindebitamento a Vigevano",
    "attivita-contratti": "avvocato per contratti a Vigevano",
    "attivita-sinistri-responsabilita": "avvocato per incidenti e risarcimenti a Vigevano",
    "attivita-codice-della-strada": "avvocato per ricorsi contro le multe a Vigevano",
    "attivita-lavoro": "avvocato del lavoro a Vigevano",
    "attivita-negoziazione-assistita": "avvocato per la negoziazione assistita a Vigevano",
    "attivita-mediazione-civile": "avvocato per la mediazione civile a Vigevano",
}

# Seconda materia collegata dalla guida, quando la guida serve a due pratiche diverse
SECONDA_MATERIA = {
    "guida-sfratto-per-morosita": "attivita-sfratti",
    "guida-pignoramento-stipendio-pensione": "attivita-recupero-crediti",
    "guida-prestito-tra-privati": "attivita-contratti",
    "guida-negoziazione-assistita-o-mediazione": "attivita-mediazione-civile",
    "guida-casa-familiare-separazione": "attivita-affidamento-minori",
    "guida-saldo-e-stralcio-banche-finanziarie": "attivita-crisi-impresa",
    "guida-eredita-con-debiti": "attivita-saldo-e-stralcio",
}

# Messaggio WhatsApp già scritto, diverso per ogni pagina: chi scrive non deve spiegare da capo
WA_MATERIA = "Buongiorno Avvocato, vorrei fissare un appuntamento per una questione di {kw}."
WA_GUIDA = "Buongiorno Avvocato, ho letto sul sito la guida «{titolo}» e vorrei fissare un appuntamento."
WA_COMUNE = "Buongiorno Avvocato, scrivo da {nome} e vorrei fissare un appuntamento."


# ---------------------------------------------------------------------------
# Comuni entro 22 km di strada dallo Studio (calcolo del 19/11/2026)
# Distanze e tempi: percorso stradale più rapido da Via Egidio Sacchetti 14
# (OpenStreetMap / OSRM), arrotondati. Tribunale: provincia di Pavia e
# Abbiatense -> Pavia (ex circondario di Vigevano; il Presidente del Tribunale
# di Pavia coordina anche il Giudice di Pace di Abbiategrasso, tabelle 2020-2022);
# provincia di Novara -> Novara.
# ---------------------------------------------------------------------------

# distanze corrette delle pagine già esistenti
DISTANZE = {
    "avvocato-mortara": ("circa 12 km", "circa 15 minuti", 12.3),
    "avvocato-gambolo": ("circa 7 km", "circa 10 minuti", 7.5),
    "avvocato-garlasco": ("circa 17 km", "circa 20 minuti", 17.2),
    "avvocato-cassolnovo": ("circa 7 km", "circa 10 minuti", 7.2),
    "avvocato-cilavegna": ("circa 11 km", "circa 15 minuti", 10.8),
    "avvocato-abbiategrasso": ("circa 14 km", "circa 20 minuti", 14.0),
}

PERCORSI = {
    "avvocato-mortara": "Da Mortara si arriva a Vigevano con la statale 494 Vigevanese, che entra in città da Viale dell'Agricoltura e Corso Torino.",
    "avvocato-gambolo": "Da Gambolò si arriva a Vigevano con la provinciale 183, che entra in città da Corso Genova.",
    "avvocato-garlasco": "Da Garlasco si arriva a Vigevano con la provinciale 206, quasi tutta in rettilineo, che entra in città da Corso Pavia.",
    "avvocato-cassolnovo": "Da Cassolnovo si arriva a Vigevano con la provinciale 206, che entra in città da Corso Novara.",
    "avvocato-cilavegna": "Da Cilavegna si arriva a Vigevano passando per Gravellona Lomellina, sulla provinciale 192, che entra in città da Via Gravellona.",
    "avvocato-abbiategrasso": "Da Abbiategrasso si arriva a Vigevano con la statale 494 Vigevanese, attraversando il Ticino, ed entrando in città da Corso Milano.",
}

TRIBUNALE_ABBIATEGRASSO = (
    "Abbiategrasso è in provincia di Milano, ma per la giustizia civile fa parte del circondario del <strong>Tribunale di Pavia</strong>, "
    "che ha raccolto il territorio dell'ex Tribunale di Vigevano. Anche l'ufficio del Giudice di Pace di Abbiategrasso dipende dal Tribunale di Pavia. "
    "Molti pensano di doversi rivolgere a Milano: per le cause legate alla residenza o agli immobili ad Abbiategrasso non è così. "
    "Se la controparte o l'immobile sono altrove, la competenza può cambiare: lo Studio lo verifica all'inizio."
)

_PAVIA_STD = ("Lo Studio segue abitualmente le udienze a Pavia: il cliente si sposta solo quando il giudice chiede la sua presenza, "
              "e riceve per iscritto un aggiornamento dopo ogni passaggio.")

_NOVARA = ("Trovandosi in provincia di Novara, per le cause legate alla residenza o agli immobili a {nome} è competente, di regola, il "
           "<strong>Tribunale di Novara</strong>, non quello di Pavia. Lo Studio opera anche a Novara: un avvocato può assistere il cliente "
           "davanti a qualsiasi tribunale italiano e gli atti si depositano in via telematica. Per chi vive a {nome} cambia quindi solo il luogo delle udienze, "
           "non la possibilità di farsi seguire da uno studio di Vigevano, a {km}.")

COMUNI_NUOVI = [
    {
        "slug": "avvocato-trecate", "nome": "Trecate", "km": "circa 19 km", "min": "circa 25 minuti", "km_n": 19.4,
        "intro": "Trecate, con oltre ventimila abitanti, è il centro più grande dell'Ovest Ticino novarese ed è legata a Vigevano da strade, lavoro e servizi. "
                 "Lo Studio Legale Pernorio assiste chi vive a Trecate nelle questioni di diritto civile, con un unico avvocato dal primo colloquio alla conclusione.",
        "percorso": "Da Trecate si arriva a Vigevano passando per Cerano: si prende la provinciale 4 Ovest Ticino e poi la provinciale 206, che entra in città da Corso Novara.",
        "tribunale": _NOVARA,
        "temi": [
            ("attivita-lavoro", "Diritto del lavoro", "licenziamenti, differenze retributive, TFR non pagato, anche per chi lavora nelle aziende della zona industriale"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni, anche davanti al Tribunale di Novara"),
            ("attivita-sinistri-responsabilita", "Incidenti e risarcimenti", "danni da incidenti stradali e trattative con le assicurazioni"),
            ("attivita-locazioni-comodato", "Affitti e comodato", "contratti, canoni non pagati, deposito cauzionale"),
            ("attivita-recupero-crediti", "Recupero crediti", "fatture e prestiti non pagati, decreti ingiuntivi e pignoramenti"),
        ],
        "faq": [
            ("Abito a Trecate: posso farmi seguire da un avvocato di Vigevano se la causa è a Novara?",
             "Sì. L'avvocato può assistere il cliente davanti a qualsiasi tribunale italiano, e lo Studio opera anche al Tribunale di Novara. Gli atti si depositano in via telematica e alle udienze va l'avvocato."),
            ("Per una separazione chi vive a Trecate va al tribunale di Novara?",
             "Di regola sì, se i coniugi e i figli vivono a Trecate. Con la negoziazione assistita, invece, non ci sono udienze: gli incontri si tengono in Studio a Vigevano o a distanza."),
            ("Quanto ci vuole per arrivare allo Studio da Trecate?",
             "Circa 25 minuti in auto, passando per Cerano. Il primo colloquio si può fare anche online, in videochiamata, con i documenti inviati prima."),
        ],
    },
    {
        "slug": "avvocato-cerano", "nome": "Cerano", "km": "circa 14 km", "min": "circa 17 minuti", "km_n": 14.0,
        "intro": "Cerano è il comune novarese più vicino a Vigevano: molte famiglie hanno qui la casa e a Vigevano il lavoro, le scuole o i parenti. "
                 "Lo Studio Legale Pernorio assiste chi vive a Cerano nelle questioni di diritto civile, dalla famiglia alla casa ai debiti.",
        "percorso": "Da Cerano si arriva a Vigevano con la provinciale 4 Ovest Ticino e poi con la provinciale 206, che entra in città da Corso Novara.",
        "tribunale": _NOVARA,
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali e giudiziali, casa familiare, assegni"),
            ("attivita-affidamento-minori", "Affidamento dei figli", "calendario di visita, mantenimento, genitori non sposati"),
            ("attivita-successioni", "Successioni ed eredità", "divisioni tra eredi, testamenti, quote di legittima"),
            ("attivita-saldo-e-stralcio", "Saldo e stralcio", "debiti con banche e finanziarie da chiudere con una somma ridotta"),
            ("attivita-codice-della-strada", "Ricorsi contro le multe", "verbali e autovelox, ricorso al Prefetto o al Giudice di Pace"),
        ],
        "faq": [
            ("Sono di Cerano: il tribunale per me è Novara o Pavia?",
             "Per le cause legate alla residenza o a immobili a Cerano è di regola Novara. Lo Studio verifica la competenza all'inizio e opera in entrambi i tribunali."),
            ("Ho preso una multa a Vigevano ma abito a Cerano: dove faccio ricorso?",
             "Il ricorso si presenta al Prefetto o al Giudice di Pace del luogo della violazione: per una multa presa a Vigevano, quindi, quelli competenti per Vigevano, non per Cerano."),
            ("Posso fare il primo colloquio senza venire a Vigevano?",
             "Sì: lo Studio offre il colloquio online, in videochiamata o su WhatsApp, con i documenti inviati prima dal sito."),
        ],
    },
    {
        "slug": "avvocato-motta-visconti", "nome": "Motta Visconti", "km": "circa 23 km", "min": "circa 30 minuti", "km_n": 22.9,
        "intro": "Motta Visconti è in provincia di Milano, sulla riva sinistra del Ticino, ma per la giustizia civile guarda a Pavia, come il resto dell'Abbiatense. "
                 "Lo Studio Legale Pernorio assiste chi vive a Motta Visconti nelle questioni di diritto civile, con un unico avvocato dal primo colloquio alla conclusione.",
        "percorso": "Da Motta Visconti si arriva a Vigevano risalendo verso Abbiategrasso sulla statale 526 e prendendo poi la statale 494 Vigevanese, che attraversa il Ticino ed entra in città da Corso Milano.",
        "tribunale": "Pur essendo in provincia di Milano, Motta Visconti rientra nel circondario del <strong>Tribunale di Pavia</strong>, che ha raccolto il territorio dell'ex Tribunale di Vigevano: "
                     "è a Pavia, per esempio, che si svolgono le esecuzioni sugli immobili che si trovano qui. " + _PAVIA_STD,
        "temi": [
            ("attivita-usucapione-diritti-reali", "Usucapione e diritti reali", "confini, servitù, case e terreni posseduti da decenni"),
            ("attivita-successioni", "Successioni ed eredità", "divisioni di case e terreni tra coeredi, testamenti"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-recupero-crediti", "Recupero crediti", "pignoramenti e opposizioni, anche su immobili"),
            ("attivita-condominio", "Condominio", "delibere, spese, liti tra vicini"),
        ],
        "faq": [
            ("Motta Visconti è in provincia di Milano: la mia causa si fa a Milano?",
             "Di regola no: Motta Visconti, come l'Abbiatense, rientra nel circondario del Tribunale di Pavia. Se la controparte o l'immobile sono altrove la competenza può cambiare, e lo Studio lo verifica all'inizio."),
            ("Devo andare a Pavia per le udienze?",
             "Di regola no: alle udienze va l'avvocato. La presenza della parte serve solo in alcuni momenti, che lo Studio prepara e accompagna."),
            ("Posso evitare il viaggio per il primo colloquio?",
             "Sì: il primo colloquio si può fare online, in videochiamata o su WhatsApp, con i documenti inviati prima dal sito."),
        ],
    },
    {
        "slug": "avvocato-robecco-sul-naviglio", "nome": "Robecco sul Naviglio", "km": "circa 18 km", "min": "circa 25 minuti", "km_n": 18.2,
        "intro": "Robecco sul Naviglio, tra Magenta e Abbiategrasso, è in provincia di Milano ma per la giustizia civile fa capo a Pavia. "
                 "Lo Studio Legale Pernorio assiste chi vive a Robecco e nelle sue frazioni nelle questioni di diritto civile, dalla famiglia alla casa ai debiti.",
        "percorso": "Da Robecco si scende verso Abbiategrasso sulla statale 526 e si prende la statale 494 Vigevanese, che attraversa il Ticino ed entra a Vigevano da Corso Milano.",
        "tribunale": "Robecco sul Naviglio rientra nel circondario del <strong>Tribunale di Pavia</strong>, come gli altri comuni dell'ex circondario di Vigevano in provincia di Milano: "
                     "è a Pavia, per esempio, che si svolgono le esecuzioni sugli immobili che si trovano qui. " + _PAVIA_STD,
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-successioni", "Successioni ed eredità", "testamenti, quote di legittima, divisioni tra eredi"),
            ("attivita-locazioni-comodato", "Affitti e comodato", "contratti, canoni non pagati, restituzione dell'immobile"),
            ("attivita-contratti", "Contratti", "preliminari di compravendita, appalti e lavori in casa"),
            ("attivita-lavoro", "Diritto del lavoro", "licenziamenti e retribuzioni non pagate"),
        ],
        "faq": [
            ("Abito a Robecco sul Naviglio: il tribunale è Milano o Pavia?",
             "Per le cause legate alla residenza o agli immobili a Robecco è di regola il Tribunale di Pavia. Per le cause di lavoro conta invece il luogo in cui si lavora, che può portare a Milano: lo Studio opera in entrambi."),
            ("Quanto dista lo Studio da Robecco?",
             "Circa 18 km, 25 minuti in auto passando per Abbiategrasso. Il primo colloquio si può fare anche online."),
            ("Lo Studio segue anche questioni di lavoro?",
             "Sì: licenziamenti, retribuzioni e TFR non pagati, sia in Lomellina sia nel Milanese."),
        ],
    },
    {
        "slug": "avvocato-tromello", "nome": "Tromello", "km": "circa 13 km", "min": "circa 17 minuti", "km_n": 12.9,
        "intro": "Tromello è un comune agricolo della Lomellina orientale, a metà strada tra Vigevano e Garlasco. "
                 "Lo Studio Legale Pernorio assiste chi vive a Tromello e nelle sue cascine nelle questioni di diritto civile, con particolare attenzione a terreni, eredità e confini.",
        "percorso": "Da Tromello si arriva a Vigevano passando per Gambolò, sulle provinciali 183 e 183 dir, ed entrando in città da Corso Genova.",
        "tribunale": "Tromello fa parte del circondario del <strong>Tribunale di Pavia</strong>, che dal 2013 comprende tutta la Lomellina. " + _PAVIA_STD,
        "temi": [
            ("attivita-usucapione-diritti-reali", "Usucapione e diritti reali", "confini tra fondi, servitù di passaggio e d'acqua, terreni posseduti da decenni"),
            ("attivita-successioni", "Successioni ed eredità", "divisione di terreni agricoli e cascine tra coeredi"),
            ("attivita-contratti", "Contratti", "affitti di fondi rustici, compravendite, scritture private"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-amministrazione-di-sostegno", "Amministrazione di sostegno", "per un genitore anziano che non riesce più a gestire i propri beni"),
        ],
        "faq": [
            ("Lo Studio segue questioni su terreni agricoli e confini?",
             "Sì: usucapione, servitù di passaggio e di acquedotto, confini e divisioni ereditarie di fondi sono materie che lo Studio tratta regolarmente. Prima della causa è obbligatoria la mediazione, che spesso chiude la lite."),
            ("Devo andare a Pavia per la causa?",
             "Di regola no: alle udienze va l'avvocato. La presenza della parte serve solo in alcuni momenti, che lo Studio prepara e accompagna."),
            ("Come si fissa il primo colloquio?",
             "Per telefono, WhatsApp o con il modulo del sito. Il colloquio si tiene in Studio a Vigevano, a circa 17 minuti da Tromello, oppure online."),
        ],
    },
    {
        "slug": "avvocato-gravellona-lomellina", "nome": "Gravellona Lomellina", "km": "circa 8 km", "min": "circa 11 minuti", "km_n": 8.1,
        "intro": "Gravellona Lomellina è tra i comuni più vicini a Vigevano: la provinciale che la collega alla città arriva a pochi minuti dallo Studio. "
                 "Lo Studio Legale Pernorio assiste chi vive a Gravellona nelle questioni di diritto civile, con un rapporto diretto con l'avvocato.",
        "percorso": "Da Gravellona si arriva a Vigevano con la provinciale 192, che entra in città da Corso Europa e Via Gravellona.",
        "tribunale": "Gravellona Lomellina rientra nel circondario del <strong>Tribunale di Pavia</strong>, competente per tutta la Lomellina. " + _PAVIA_STD,
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-affidamento-minori", "Affidamento dei figli", "calendario di visita e mantenimento"),
            ("attivita-successioni", "Successioni ed eredità", "testamenti, quote di legittima, rinuncia all'eredità"),
            ("attivita-condominio", "Condominio", "delibere, spese, liti tra vicini"),
            ("attivita-saldo-e-stralcio", "Saldo e stralcio", "debiti con banche e finanziarie"),
        ],
        "faq": [
            ("Quanto dista lo Studio da Gravellona Lomellina?",
             "Circa 8 km, una decina di minuti in auto lungo la provinciale 192. Si riceve su appuntamento dal lunedì al venerdì."),
            ("Per una rinuncia all'eredità devo andare a Pavia?",
             "La rinuncia si fa con dichiarazione a un notaio oppure alla cancelleria del Tribunale di Pavia. Prima conviene un parere: alcuni comportamenti valgono come accettazione."),
            ("Cosa porto al primo colloquio?",
             "I documenti che riguardano la questione: atti ricevuti, contratti, lettere, messaggi. Per una separazione c'è una checklist da stampare o spuntare dal telefono tra gli strumenti del sito."),
        ],
    },
    {
        "slug": "avvocato-parona", "nome": "Parona", "km": "circa 10 km", "min": "circa 11 minuti", "km_n": 9.5,
        "intro": "Parona si trova sulla statale Vigevanese, tra Vigevano e Mortara, e per molti suoi abitanti Vigevano è la città di riferimento. "
                 "Lo Studio Legale Pernorio assiste chi vive a Parona nelle questioni di diritto civile, dalla famiglia agli affitti ai debiti.",
        "percorso": "Da Parona si arriva a Vigevano con la statale 494 Vigevanese, che entra in città da Viale dell'Agricoltura e Corso Torino.",
        "tribunale": "Parona fa parte del circondario del <strong>Tribunale di Pavia</strong>, competente per tutta la Lomellina. " + _PAVIA_STD,
        "temi": [
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-locazioni-comodato", "Affitti e comodato", "contratti, canoni non pagati, deposito cauzionale"),
            ("attivita-sfratti", "Sfratti", "inquilino che non paga, finita locazione"),
            ("attivita-lavoro", "Diritto del lavoro", "licenziamenti e retribuzioni non pagate"),
            ("attivita-recupero-crediti", "Recupero crediti", "diffide, decreti ingiuntivi, pignoramenti"),
        ],
        "faq": [
            ("Quanto ci vuole da Parona allo Studio?",
             "Circa 11 minuti in auto lungo la statale Vigevanese. Il colloquio si può fare anche online, in videochiamata."),
            ("Ho un inquilino che non paga: quanto dura uno sfratto?",
             "Dipende da come si comporta l'inquilino e dai tempi dell'ufficiale giudiziario. Il primo passo è una diffida scritta; poi l'intimazione di sfratto al Tribunale di Pavia."),
            ("Devo andare a Pavia per le udienze?",
             "Di regola no: alle udienze va l'avvocato, che informa il cliente per iscritto di ogni passaggio."),
        ],
    },
    {
        "slug": "avvocato-gropello-cairoli", "nome": "Gropello Cairoli", "km": "circa 21 km", "min": "circa 26 minuti", "km_n": 21.3,
        "intro": "Gropello Cairoli è nella Lomellina orientale, tra Garlasco e il Ticino, a una ventina di minuti da Vigevano. "
                 "Lo Studio Legale Pernorio assiste chi vive a Gropello nelle questioni di diritto civile, dalla famiglia alla casa alle eredità.",
        "percorso": "Da Gropello si raggiunge Garlasco con la provinciale 206 dir e da lì Vigevano con la provinciale 206, entrando in città da Corso Pavia.",
        "tribunale": "Gropello Cairoli fa parte del circondario del <strong>Tribunale di Pavia</strong>, che dista poco più di venti chilometri. " + _PAVIA_STD,
        "temi": [
            ("attivita-successioni", "Successioni ed eredità", "divisioni tra coeredi, testamenti, quote di legittima"),
            ("attivita-amministrazione-di-sostegno", "Amministrazione di sostegno", "per un familiare anziano o fragile"),
            ("attivita-usucapione-diritti-reali", "Usucapione e diritti reali", "confini, servitù, terreni"),
            ("attivita-separazione-divorzio", "Separazione e divorzio", "accordi consensuali, casa familiare, assegni"),
            ("attivita-crisi-impresa", "Sovraindebitamento", "debiti non più sostenibili, per privati e piccole imprese"),
        ],
        "faq": [
            ("Gropello è vicino a Pavia: perché uno studio di Vigevano?",
             "Il tribunale è comunque Pavia, dove lo Studio segue abitualmente le udienze. Conta di più avere un avvocato che segua la pratica dall'inizio alla fine e risponda in fretta: il primo colloquio si può fare anche online."),
            ("Come si chiede l'amministrazione di sostegno per un genitore?",
             "Con un ricorso al giudice tutelare del luogo in cui la persona vive, per Gropello quello del Tribunale di Pavia. Il giudice sente la persona e nomina l'amministratore, spesso un familiare."),
            ("Quanto ci vuole per arrivare allo Studio?",
             "Circa 26 minuti in auto, passando per Garlasco."),
        ],
    },
]

FAQ_ABBIATEGRASSO = ("Abito ad Abbiategrasso: la mia causa va a Pavia o a Milano?",
                     "Per le cause legate alla residenza o agli immobili ad Abbiategrasso è di regola il Tribunale di Pavia, che ha raccolto l'ex circondario di Vigevano. "
                     "Per le cause di lavoro conta invece il luogo in cui si lavora, che può portare a Milano. Lo Studio segue le udienze in entrambi i tribunali.")


def applica_comuni(C):
    """Distanze verificate, Abbiategrasso aggiornata, comuni nuovi; elenco ordinato per distanza."""
    for c in C.COMUNI:
        if c["slug"] in DISTANZE:
            c["km"], c["min"], c["km_n"] = DISTANZE[c["slug"]]
            c["percorso"] = PERCORSI[c["slug"]] + " Lo Studio è in Via Egidio Sacchetti 14, vicino al centro storico."
        if c["slug"] == "avvocato-abbiategrasso":
            c["tribunale"] = TRIBUNALE_ABBIATEGRASSO
            c["faq"] = [FAQ_ABBIATEGRASSO if q.startswith("Abito ad Abbiategrasso") else (q, a) for q, a in c["faq"]]
    gia = {c["slug"] for c in C.COMUNI}
    for c in COMUNI_NUOVI:
        if c["slug"] not in gia:
            c = dict(c)
            c["percorso"] += " Lo Studio è in Via Egidio Sacchetti 14, vicino al centro storico."
            c["tribunale"] = c["tribunale"].format(nome=c["nome"], km=c["km"])
            C.COMUNI.append(c)
    C.COMUNI.sort(key=lambda c: c["km_n"])


# Ingresso per problema in home: come le persone descrivono la propria situazione
PROBLEMI = [
    ("Mi sto separando", "Separazione consensuale o giudiziale, divorzio, casa e assegni", "attivita-separazione-divorzio"),
    ("Figli: affidamento e mantenimento", "Calendario di visita, mantenimento, genitori non sposati", "attivita-affidamento-minori"),
    ("È morto un familiare", "Eredità, testamento, debiti del defunto, divisione tra eredi", "attivita-successioni"),
    ("Un genitore non riesce più a gestirsi", "Amministrazione di sostegno: chi la chiede e come", "attivita-amministrazione-di-sostegno"),
    ("L'inquilino non paga", "Diffida, sfratto per morosità, recupero dei canoni", "attivita-sfratti"),
    ("Ho debiti con banche o finanziarie", "Saldo e stralcio, pignoramento, sovraindebitamento", "attivita-saldo-e-stralcio"),
    ("Mi devono dei soldi", "Prestiti e fatture non pagati, decreto ingiuntivo", "attivita-recupero-crediti"),
    ("Lavoro: licenziamento o stipendio", "Impugnare un licenziamento, retribuzioni e TFR non pagati", "attivita-lavoro"),
    ("Incidente o multa da contestare", "Risarcimento dall'assicurazione, ricorso contro il verbale", "attivita-sinistri-responsabilita"),
]
