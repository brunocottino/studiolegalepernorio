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
