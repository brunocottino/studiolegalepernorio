# -*- coding: utf-8 -*-
"""Farsi trovare: ricerca interna, glossario, feed, date stabili, segnali per motori e agenti.

- Ricerca nel sito (/cerca, /cerca.js) con SearchAction e OpenSearch: il sito si può
  interrogare dalla barra del browser e dagli assistenti.
- Glossario legale (/glossario-legale) con dati strutturati DefinedTermSet e fonti Normattiva.
- Feed Atom delle guide (/feed.xml).
- Date stabili: la data di modifica di una pagina cambia solo quando cambia il suo testo
  (registro in dati/date-pagine.json). Una sitemap con "oggi" su tutte le pagine a ogni
  build viene ignorata da Google.
- Sitemap con immagini, meta robots con anteprime estese, catalogo delle API (RFC 9727).
"""
import hashlib
import html
import json
import os
import re

import fonti as FO

BASE = "https://studiolegalepernorio.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(ROOT, "dati", "date-pagine.json")

ROBOTS_META = '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# Date stabili
# ---------------------------------------------------------------------------

def impronta(h):
    """Impronta del testo principale della pagina, senza le date che cambiano a ogni build."""
    m = re.search(r"<main>(.*)</main>", h, re.S)
    t = re.sub(r"<script.*?</script>", " ", m.group(1) if m else h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\d{2}/\d{2}/\d{4}", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return hashlib.sha1(t.encode("utf-8")).hexdigest()[:16]


def carica_registro():
    if os.path.exists(REGISTRO):
        with open(REGISTRO, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def salva_registro(reg):
    os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
    with open(REGISTRO, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, ensure_ascii=False, indent=0, sort_keys=True)
        fh.write("\n")


def date_pagina(reg, slug, h, oggi):
    """(pubblicata, modificata) della pagina; aggiorna il registro se il testo è cambiato."""
    imp = impronta(h)
    r = reg.get(slug)
    if r is None:
        r = reg[slug] = {"imp": imp, "pub": oggi, "mod": oggi}
    elif r["imp"] != imp:
        r["imp"], r["mod"] = imp, oggi
    return r["pub"], r["mod"]


def applica_date(h, oggi, pub, mod):
    h = h.replace(f'"dateModified": "{oggi}"', f'"dateModified": "{mod}"')
    return h.replace(f'"datePublished": "{oggi}"', f'"datePublished": "{pub}"')


# ---------------------------------------------------------------------------
# Glossario
# ---------------------------------------------------------------------------

DPR115 = "urn:nir:presidente.repubblica:decreto:2002-05-30;115"
CCII = "urn:nir:stato:decreto.legislativo:2019-01-12;14"
DLGS28 = "urn:nir:stato:decreto.legislativo:2010-03-04;28"
FO.ATTI.setdefault(DPR115, "D.P.R. 30 maggio 2002, n. 115 (Testo unico spese di giustizia)")
FO.ATTI.setdefault(CCII, "D.Lgs. 12 gennaio 2019, n. 14 (Codice della crisi d'impresa e dell'insolvenza)")

GLOSSARIO_SLUG = "glossario-legale"

# (id, termine, definizione, (etichetta fonte, atto, articolo), (pagina, testo del link))
GLOSSARIO = [
    ("accettazione-eredita", "Accettazione dell'eredità",
     "L'atto con cui chi è chiamato all'eredità diventa erede. Può essere espressa, con una dichiarazione scritta, oppure tacita, quando la persona compie atti che solo un erede potrebbe compiere. Il diritto di accettare si prescrive in dieci anni.",
     ("Artt. 474 e 480 c.c.", FO.CC, "474"), ("guida-eredita-con-debiti", "Eredità con debiti: cosa fare")),
    ("addebito", "Addebito della separazione",
     "La dichiarazione con cui il giudice, se gli viene chiesto, attribuisce la separazione al coniuge che ha violato i doveri del matrimonio. Chi subisce l'addebito perde il diritto all'assegno di mantenimento (restano solo gli alimenti, se è in stato di bisogno) e gran parte dei diritti sull'eredità dell'altro coniuge.",
     ("Art. 151 c.c.", FO.CC, "151"), ("attivita-separazione-divorzio", "Separazione e divorzio")),
    ("affidamento-condiviso", "Affidamento condiviso",
     "È la regola: i figli restano affidati a entrambi i genitori, che prendono insieme le decisioni più importanti su salute, scuola ed educazione. Non significa tempi uguali: di solito i figli abitano in prevalenza con uno dei due.",
     ("Art. 337-ter c.c.", FO.CC, "337ter"), ("guida-affidamento-figli-condiviso-esclusivo", "Affidamento condiviso o esclusivo")),
    ("affidamento-esclusivo", "Affidamento esclusivo",
     "È l'eccezione: il giudice affida i figli a un solo genitore quando l'affidamento all'altro è contrario all'interesse del minore. L'altro genitore conserva il diritto e il dovere di vigilare su istruzione, educazione e condizioni di vita dei figli.",
     ("Art. 337-quater c.c.", FO.CC, "337quater"), ("guida-affidamento-figli-condiviso-esclusivo", "Affidamento condiviso o esclusivo")),
    ("amministratore-di-sostegno", "Amministratore di sostegno",
     "La persona nominata dal giudice tutelare per assistere chi, per un'infermità o una menomazione fisica o psichica, non riesce a provvedere in tutto o in parte ai propri interessi. Il decreto di nomina indica gli atti che l'amministratore può compiere; per tutto il resto la persona conserva la propria capacità.",
     ("Art. 404 c.c.", FO.CC, "404"), ("guida-amministrazione-di-sostegno", "Amministrazione di sostegno: come funziona")),
    ("assegno-di-mantenimento", "Assegno di mantenimento",
     "La somma periodica che un genitore versa per i figli, oppure che un coniuge versa all'altro dopo la separazione quando questi non ha redditi adeguati. Per i figli si tiene conto delle loro esigenze, del tenore di vita, dei tempi passati con ciascun genitore e delle risorse di entrambi.",
     ("Artt. 156 e 337-ter c.c.", FO.CC, "337ter"), ("guida-assegno-mantenimento-figli", "Assegno per i figli: come si calcola")),
    ("assegno-divorzile", "Assegno divorzile",
     "L'assegno che, dopo il divorzio, può spettare all'ex coniuge che non ha mezzi adeguati e non può procurarseli per ragioni oggettive. Il giudice considera anche il contributo dato alla vita familiare e la durata del matrimonio. Si perde con le nuove nozze.",
     ("Art. 5 legge 898/1970", FO.L898, "5"), ("guida-divorzio-tempi", "Divorzio: tempi dopo la separazione")),
    ("beneficio-inventario", "Beneficio d'inventario",
     "Il modo di accettare l'eredità che tiene separato il patrimonio del defunto da quello dell'erede: l'erede risponde dei debiti ereditari solo entro il valore dei beni ricevuti. Si fa con una dichiarazione davanti al notaio o al cancelliere del tribunale, seguita dall'inventario.",
     ("Artt. 484 e 490 c.c.", FO.CC, "484"), ("guida-eredita-con-debiti", "Eredità con debiti: cosa fare")),
    ("caparra-confirmatoria", "Caparra confirmatoria",
     "La somma versata alla firma di un contratto a garanzia dell'impegno. Se non adempie chi l'ha versata, l'altra parte può recedere e trattenerla; se non adempie chi l'ha ricevuta, l'altra parte può recedere e chiedere il doppio.",
     ("Art. 1385 c.c.", FO.CC, "1385"), ("attivita-contratti", "Contratti e obbligazioni")),
    ("casa-familiare", "Casa familiare (assegnazione)",
     "La casa in cui la famiglia ha vissuto. Dopo la separazione il giudice ne assegna il godimento tenendo conto prima di tutto dell'interesse dei figli: di regola resta al genitore con cui i figli abitano, anche se non ne è proprietario.",
     ("Art. 337-sexies c.c.", FO.CC, "337sexies"), ("guida-casa-familiare-separazione", "Chi resta nella casa familiare")),
    ("collazione", "Collazione",
     "L'obbligo dei figli, dei loro discendenti e del coniuge che partecipano alla stessa eredità di rimettere nella massa da dividere le donazioni ricevute in vita dal defunto, salvo che questi li abbia dispensati.",
     ("Art. 737 c.c.", FO.CC, "737"), ("attivita-successioni", "Successioni ed eredità")),
    ("comodato", "Comodato",
     "Il contratto con cui una persona consegna a un'altra un bene, per esempio una casa, perché lo usi per un tempo o per uno scopo determinato, con l'obbligo di restituirlo. È gratuito: se c'è un corrispettivo si tratta di locazione.",
     ("Art. 1803 c.c.", FO.CC, "1803"), ("attivita-locazioni-comodato", "Locazioni e comodato")),
    ("contributo-unificato", "Contributo unificato",
     "La tassa dovuta allo Stato per iscrivere a ruolo una causa. L'importo dipende dal valore della lite e dal tipo di procedimento.",
     ("Art. 9 D.P.R. 115/2002", DPR115, "9"), ("costi-avvocato", "Quanto costa un avvocato")),
    ("convivenza-di-fatto", "Convivenza di fatto",
     "Il legame stabile tra due persone maggiorenni, unite da vincoli affettivi di coppia e di reciproca assistenza, che non sono sposate né unite civilmente. I conviventi possono regolare i rapporti economici con un contratto di convivenza.",
     ("Legge 76/2016, art. 1, commi 36 e seguenti", FO.L76, None), ("guida-fine-convivenza-diritti", "Fine della convivenza: cosa spetta")),
    ("decreto-ingiuntivo", "Decreto ingiuntivo",
     "L'ordine di pagamento che il giudice emette su richiesta del creditore che ha una prova scritta del credito, senza sentire prima il debitore. Dalla notifica il debitore ha di regola quaranta giorni per fare opposizione; se non la fa, il decreto diventa definitivo.",
     ("Artt. 633 e 641 c.p.c.", FO.CPC, "633"), ("attivita-recupero-crediti", "Recupero crediti")),
    ("delibera-condominiale", "Delibera condominiale (impugnazione)",
     "La decisione dell'assemblea di condominio. Chi era contrario, astenuto o assente può impugnarla davanti al giudice entro trenta giorni: dalla data dell'assemblea per i dissenzienti e gli astenuti, dalla comunicazione del verbale per gli assenti.",
     ("Art. 1137 c.c.", FO.CC, "1137"), ("guida-impugnare-delibera-condominiale", "Impugnare una delibera condominiale")),
    ("deposito-cauzionale", "Deposito cauzionale",
     "La somma che l'inquilino consegna al proprietario a garanzia degli obblighi del contratto di affitto. Non può superare tre mensilità del canone e produce interessi legali a favore dell'inquilino.",
     ("Art. 11 legge 392/1978", FO.L392, "11"), ("guida-deposito-cauzionale-affitto", "Deposito cauzionale: quando va restituito")),
    ("diffida", "Diffida (messa in mora)",
     "La richiesta scritta con cui si intima a qualcuno di adempiere, per esempio di pagare una somma. Costituisce in mora il debitore, da quel momento fa decorrere gli interessi di mora e interrompe la prescrizione.",
     ("Art. 1219 c.c.", FO.CC, "1219"), ("attivita-recupero-crediti", "Recupero crediti")),
    ("legato", "Legato",
     "La disposizione del testamento che attribuisce a una persona un bene o un diritto determinato, per esempio un immobile o una somma. Il legatario non è erede e, di regola, non risponde dei debiti del defunto.",
     ("Art. 588 c.c.", FO.CC, "588"), ("guida-testamento-olografo", "Testamento olografo: come farlo valido")),
    ("legittima", "Legittima (quota di)",
     "La parte di eredità che la legge riserva al coniuge, ai figli e, se mancano i figli, ai genitori, anche contro la volontà espressa nel testamento. Chi riceve meno di quanto gli spetta può agire in giudizio con l'azione di riduzione.",
     ("Art. 536 c.c.", FO.CC, "536"), ("attivita-successioni", "Successioni ed eredità")),
    ("mediazione-civile", "Mediazione civile",
     "Il tentativo di accordo davanti a un mediatore imparziale, con l'assistenza degli avvocati. In molte materie, tra cui condominio, diritti reali, divisioni, successioni, locazioni e contratti bancari, è obbligatorio tentarla prima di iniziare la causa.",
     ("Art. 5 D.Lgs. 28/2010", DLGS28, "5"), ("guida-negoziazione-assistita-o-mediazione", "Negoziazione assistita o mediazione")),
    ("negoziazione-assistita", "Negoziazione assistita",
     "L'accordo con cui le parti, assistite ciascuna dal proprio avvocato, si impegnano a cercare una soluzione senza andare in tribunale. L'accordo raggiunto vale come titolo esecutivo. Si può usare anche per separazione e divorzio consensuali.",
     ("Artt. 2 e 6 D.L. 132/2014", FO.DL132, "2"), ("guida-negoziazione-assistita-o-mediazione", "Negoziazione assistita o mediazione")),
    ("pignoramento", "Pignoramento",
     "L'atto che dà inizio all'esecuzione forzata: vincola beni del debitore, come immobili, conti correnti, stipendi o pensioni, perché il creditore possa soddisfarsi su di essi. Stipendi e pensioni si possono pignorare solo entro limiti fissati dalla legge.",
     ("Artt. 491 e 545 c.p.c.", FO.CPC, "491"), ("guida-pignoramento-stipendio-pensione", "Pignoramento di stipendio e pensione")),
    ("precetto", "Precetto",
     "L'intimazione formale a pagare, o a eseguire quanto dovuto, entro un termine non inferiore a dieci giorni, con l'avviso che in mancanza si procederà all'esecuzione forzata. Perde efficacia se l'esecuzione non inizia entro novanta giorni dalla notifica.",
     ("Artt. 480 e 481 c.p.c.", FO.CPC, "480"), ("attivita-recupero-crediti", "Recupero crediti")),
    ("preliminare", "Preliminare (compromesso)",
     "Il contratto con cui le parti si obbligano a firmare in seguito il contratto definitivo, per esempio la vendita di una casa. Deve avere la stessa forma del definitivo; se una parte poi si rifiuta di firmare, l'altra può chiedere al giudice una sentenza che ne produca gli effetti.",
     ("Artt. 1351 e 2932 c.c.", FO.CC, "1351"), ("attivita-contratti", "Contratti e obbligazioni")),
    ("prescrizione", "Prescrizione",
     "L'estinzione di un diritto che non viene esercitato per il tempo stabilito dalla legge. Il termine ordinario è di dieci anni; ce ne sono di più brevi, per esempio cinque anni per i canoni di affitto e per il risarcimento del danno da fatto illecito, due anni per i danni da circolazione dei veicoli.",
     ("Artt. 2934, 2946, 2947 e 2948 c.c.", FO.CC, "2946"), ("guida-prestito-tra-privati", "Prestito tra privati")),
    ("procura-alle-liti", "Procura alle liti",
     "L'atto con cui il cliente dà all'avvocato il potere di rappresentarlo in giudizio. Di solito è una scrittura firmata dal cliente, con la firma autenticata dall'avvocato stesso.",
     ("Art. 83 c.p.c.", FO.CPC, "83"), ("costi-avvocato", "Quanto costa un avvocato")),
    ("responsabilita-genitoriale", "Responsabilità genitoriale",
     "L'insieme dei diritti e dei doveri dei genitori verso i figli minorenni: cura, educazione, istruzione, amministrazione dei beni. Spetta a entrambi i genitori, che la esercitano di comune accordo, anche se non sono sposati o sono separati.",
     ("Art. 316 c.c.", FO.CC, "316"), ("attivita-affidamento-minori", "Affidamento dei figli")),
    ("rinuncia-eredita", "Rinuncia all'eredità",
     "La dichiarazione con cui il chiamato rifiuta l'eredità, resa davanti a un notaio o al cancelliere del tribunale del luogo in cui si è aperta la successione. Chi rinuncia è considerato come se non fosse mai stato chiamato e non risponde dei debiti del defunto.",
     ("Artt. 519 e 521 c.c.", FO.CC, "519"), ("guida-eredita-con-debiti", "Eredità con debiti: cosa fare")),
    ("saldo-e-stralcio", "Saldo e stralcio",
     "L'accordo con cui il creditore, per esempio una banca o una finanziaria, accetta una somma inferiore al dovuto e in cambio rinuncia al resto del credito. È una transazione: va messa per iscritto, con la liberatoria.",
     ("Art. 1965 c.c.", FO.CC, "1965"), ("guida-saldo-e-stralcio-banche-finanziarie", "Saldo e stralcio con banche e finanziarie")),
    ("separazione-consensuale", "Separazione consensuale",
     "La separazione chiesta dai coniugi d'accordo tra loro su figli, casa e questioni economiche. Si può ottenere con ricorso congiunto in tribunale, con la negoziazione assistita dagli avvocati oppure, in alcuni casi, davanti all'ufficiale di stato civile del Comune.",
     ("Art. 158 c.c.", FO.CC, "158"), ("guida-costo-separazione-consensuale", "Quanto costa una separazione consensuale")),
    ("separazione-giudiziale", "Separazione giudiziale",
     "La separazione chiesta al tribunale da un solo coniuge quando manca l'accordo. Presuppone fatti che rendono intollerabile la convivenza; il giudice decide su affidamento dei figli, mantenimento e casa familiare.",
     ("Art. 151 c.c.", FO.CC, "151"), ("guida-separazione-divorzio-unica-domanda", "Separazione e divorzio con un'unica domanda")),
    ("servitu", "Servitù",
     "Il peso imposto su un fondo a vantaggio di un altro fondo che appartiene a un proprietario diverso: per esempio il diritto di passare sul terreno del vicino per raggiungere la strada.",
     ("Art. 1027 c.c.", FO.CC, "1027"), ("attivita-usucapione-diritti-reali", "Usucapione e diritti reali")),
    ("sfratto-per-morosita", "Sfratto per morosità",
     "Il procedimento con cui il proprietario chiede al giudice di ordinare il rilascio dell'immobile perché l'inquilino non paga il canone. Negli affitti abitativi l'inquilino può chiedere in udienza un termine, detto di grazia, fino a novanta giorni per saldare il debito.",
     ("Art. 658 c.p.c. e art. 55 legge 392/1978", FO.CPC, "658"), ("guida-sfratto-per-morosita", "Sfratto per morosità: come funziona")),
    ("sovraindebitamento", "Sovraindebitamento",
     "La situazione di chi non riesce più a pagare i propri debiti e non può accedere alle procedure previste per le imprese maggiori: consumatori, professionisti, piccole imprese. La legge offre procedure per ristrutturare i debiti o liquidare il patrimonio e, alla fine, ottenere la liberazione dai debiti rimasti (esdebitazione).",
     ("Codice della crisi d'impresa, D.Lgs. 14/2019", CCII, None), ("attivita-crisi-impresa", "Sovraindebitamento e crisi d'impresa")),
    ("successione-legittima", "Successione legittima",
     "La successione regolata dalla legge quando manca un testamento, o quando il testamento non dispone di tutti i beni. Ereditano, in un ordine preciso, il coniuge, i figli, i genitori, i fratelli e gli altri parenti fino al sesto grado.",
     ("Art. 565 c.c.", FO.CC, "565"), ("strumento-calcolo-quote-eredita", "Calcolo delle quote di eredità")),
    ("testamento-olografo", "Testamento olografo",
     "Il testamento scritto per intero, datato e firmato di proprio pugno da chi lo fa. Non richiede notaio né testimoni, ma se manca la scrittura a mano o la firma è nullo.",
     ("Artt. 602 e 606 c.c.", FO.CC, "602"), ("guida-testamento-olografo", "Testamento olografo: come farlo valido")),
    ("titolo-esecutivo", "Titolo esecutivo",
     "Il documento che consente di avviare l'esecuzione forzata contro il debitore: per esempio una sentenza, un decreto ingiuntivo esecutivo, una cambiale, un atto notarile o un accordo di negoziazione assistita.",
     ("Art. 474 c.p.c.", FO.CPC, "474"), ("attivita-recupero-crediti", "Recupero crediti")),
    ("unione-civile", "Unione civile",
     "L'istituto che riconosce la coppia formata da due persone maggiorenni dello stesso sesso, con diritti e doveri in gran parte analoghi a quelli del matrimonio. Si scioglie senza passare dalla separazione.",
     ("Legge 76/2016, art. 1, commi 1-35", FO.L76, None), ("guida-scioglimento-unione-civile", "Scioglimento dell'unione civile")),
    ("usucapione", "Usucapione",
     "L'acquisto della proprietà di un bene per effetto del possesso continuato nel tempo, pacifico e pubblico. Per gli immobili servono di regola vent'anni; dieci se c'è buona fede e un titolo idoneo, trascritto nei registri immobiliari.",
     ("Artt. 1158 e 1159 c.c.", FO.CC, "1158"), ("guida-usucapione-quando-si-diventa-proprietari", "Usucapione: quando si diventa proprietari")),
]

GLOSSARIO_TITLE = "Glossario legale: i termini spiegati in parole semplici"
GLOSSARIO_DESC = ("Glossario dell'Avv. Daniela Pernorio, Vigevano: usucapione, legittima, addebito, decreto ingiuntivo, "
                  "precetto e altri termini di diritto civile spiegati in breve, con la fonte di legge.")


def _fonte(g):
    return FO.f(*g[3])


def glossario_body(aggiornato):
    lettere = sorted({g[1][0].upper() for g in GLOSSARIO})
    nav = "".join(f"<a class='chip' href='#lettera-{x.lower()}'>{x}</a>" for x in lettere)
    out = ('<article class="card panel article rv">'
           f"<p>{len(GLOSSARIO)} termini del diritto civile spiegati in poche righe, con l'articolo di legge e la pagina del sito che approfondisce. "
           "Serve a capire un atto ricevuto, una lettera dell'avvocato di controparte o una parola sentita in udienza.</p>"
           f'<nav class="chips" aria-label="Lettere" style="margin:14px 0 6px">{nav}</nav>')
    corrente = None
    for g in sorted(GLOSSARIO, key=lambda x: x[1].lower()):
        ident, termine, definizione, _, link = g
        f = _fonte(g)
        if termine[0].upper() != corrente:
            corrente = termine[0].upper()
            out += f'<h2 id="lettera-{corrente.lower()}">{corrente}</h2>'
        out += (f'<h3 id="{ident}">{esc(termine)}</h3><p>{esc(definizione)} '
                f'<span class="gl-f">Fonte: <a href="{esc(f["url"])}" target="_blank" rel="noopener">{esc(f["etichetta"])}</a>. '
                f"Approfondimento: <a href='/{link[0]}'>{esc(link[1])}</a>.</span></p>")
    out += (f'<p class="note-s">A cura dello Studio Legale Pernorio, <a href=\'/studio\'>Avv. Daniela Pernorio</a>, Vigevano. Aggiornato a {aggiornato}. '
            "Definizioni generali e semplificate: non sostituiscono un parere sul caso concreto.</p></article>")
    return out


def glossario_ld():
    url = f"{BASE}/{GLOSSARIO_SLUG}"
    return {
        "@context": "https://schema.org", "@type": "DefinedTermSet", "@id": url + "#glossario",
        "name": "Glossario legale dello Studio Legale Pernorio", "url": url, "inLanguage": "it-IT",
        "publisher": {"@id": BASE + "/#studio"}, "author": {"@id": BASE + "/#avvocato"},
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "@id": f"{url}#{g[0]}", "name": g[1], "description": g[2],
             "url": f"{url}#{g[0]}", "inDefinedTermSet": {"@id": url + "#glossario"}}
            for g in sorted(GLOSSARIO, key=lambda x: x[1].lower())
        ],
    }


def glossario_indice():
    """Una voce dell'indice di ricerca per ogni termine."""
    url = f"{BASE}/{GLOSSARIO_SLUG}"
    return [{"t": g[1] + " · Glossario", "d": g[2], "k": "", "u": f"{url}#{g[0]}", "m": f"{url}.md", "c": "Glossario"}
            for g in GLOSSARIO]


# ---------------------------------------------------------------------------
# Ricerca nel sito
# ---------------------------------------------------------------------------

CERCA_SLUG = "cerca"

CATEGORIE = (("guida-", "Guida"), ("attivita-", "Competenza"), ("avvocato-", "Dove operiamo"), ("strumento-", "Strumento"))
CATEGORIE_PAGINA = {"guide": "Guide", "attivita": "Competenze", "strumenti": "Strumenti", "domande": "Domande frequenti",
                    "glossario-legale": "Glossario", "contatti": "Contatti", "studio": "Lo Studio", "costi-avvocato": "Costi",
                    "colloquio-online": "Colloquio online", "diritto-di-famiglia": "Competenza", "index": "Home"}


def categoria(slug):
    for pre, nome in CATEGORIE:
        if slug.startswith(pre):
            return nome
    return CATEGORIE_PAGINA.get(slug, "Pagina")


ICO_LENTE = '<svg class="ico" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def modulo_cerca(ident="sf", autofocus=False):
    """Modulo GET verso /cerca: funziona da ogni pagina, anche senza JavaScript fino alla pagina dei risultati."""
    return (f'<form class="sform" id="{ident}" action="/cerca" method="get" role="search" aria-label="Cerca nel sito">'
            f'<input type="search" name="q" id="{ident}-q" placeholder="Cerca: separazione, eredità, sfratto, multa…" '
            'aria-label="Cosa cerca" autocomplete="off" enterkeyhint="search" maxlength="80"'
            + (" autofocus" if autofocus else "") + ">"
            f'<button class="btn btn-primary" type="submit">Cerca<span class="bi">{ICO_LENTE}</span></button></form>')


SUGGERITE = ["separazione", "assegno per i figli", "eredità con debiti", "testamento", "sfratto", "affitto",
             "pignoramento", "saldo e stralcio", "multa autovelox", "usucapione", "licenziamento", "costi"]


def cerca_body():
    chips = "".join(f"<a class='chip' href='/cerca?q={esc(x.replace(' ', '+'))}'>{esc(x)}</a>" for x in SUGGERITE)
    return ('<div class="card panel rv">' + modulo_cerca("sf")
            + '<p class="note-s" id="sn" aria-live="polite" style="margin-top:14px">Scriva una o più parole: la ricerca guarda tra guide, competenze, glossario, strumenti e pagine dei comuni.</p>'
            + f'<div class="chips" id="sc" style="margin-top:14px">{chips}</div></div>'
            + '<div class="glist" id="sr" style="margin-top:14px"></div>'
            + "<noscript><div class=\"card panel\" style=\"margin-top:14px\"><p>La ricerca richiede JavaScript. In alternativa: <a href='/guide'>tutte le guide</a>, "
              "<a href='/attivita'>le competenze</a>, <a href='/glossario-legale'>il glossario</a>.</p></div></noscript>")


CERCA_JS = r"""/* Studio Legale Pernorio · ricerca nel sito. Gira nel browser sull'indice /cerca.json: ciò che si scrive non viene inviato né salvato. */
(function(){
var f=document.getElementById('sf'),i=document.getElementById('sf-q'),o=document.getElementById('sr'),n=document.getElementById('sn'),c=document.getElementById('sc');
if(!f||!i||!o)return;
var IX=null,T0=document.title,tm;
var STOP={il:1,lo:1,la:1,le:1,gli:1,un:1,una:1,uno:1,di:1,del:1,della:1,dei:1,delle:1,da:1,dal:1,in:1,con:1,su:1,per:1,tra:1,fra:1,che:1,chi:1,cosa:1,come:1,quando:1,quanto:1,mi:1,si:1,se:1,non:1,ho:1,ha:1,posso:1,devo:1,fare:1,mio:1,mia:1,al:1,alla:1,ad:1,ed:1,nel:1,nella:1,sono:1,essere:1,puo:1,fa:1,fare:1,mio:1,mia:1,miei:1,suo:1,sua:1,ci:1,ne:1,ma:1,anche:1,vuole:1,voglio:1,serve:1};
var SIN={affitto:['locazion','inquilin','canon'],affitti:['locazion','inquilin'],padrone:['proprietar','locator'],casa:['immobil','abitazion'],multa:['verbal','sanzion','autovelox'],multe:['verbal','sanzion','autovelox'],
eredita:['succession','ered'],eredi:['succession','ered'],debiti:['debit','saldo','sovraindebit'],debito:['debit','saldo','sovraindebit'],banca:['banc','finanziar'],incidente:['sinistr','risarciment'],
licenziato:['licenziament'],licenziata:['licenziament'],lavoro:['lavor','licenziament'],bambini:['figl','minor'],bambino:['figl','minor'],figli:['figl','minor'],mantenimento:['manteniment','assegn'],alimenti:['manteniment','assegn'],
divorzio:['divorz','separazion'],divorziare:['divorz'],separarsi:['separazion'],separarmi:['separazion'],convivente:['convivenz'],compagno:['convivenz'],compagna:['convivenz'],soldi:['prestit','credit'],
prezzo:['cost','preventiv'],costo:['cost','preventiv'],costa:['cost','preventiv'],tariffa:['cost','preventiv'],parcella:['cost','preventiv'],onorario:['cost','preventiv'],
vicino:['condomin','confin','servit'],vicini:['condomin','confin','servit'],terreno:['usucapion','confin','fond'],nonno:['amministrazion','sostegn'],anziano:['amministrazion','sostegn'],
video:['online','videochiam'],videochiamata:['online'],telefono:['contatt'],orari:['contatt'],indirizzo:['contatt'],dove:['contatt','comun'],sfrattare:['sfratt'],moroso:['morosit','sfratt'],
cartella:['debit','pignorament'],stipendio:['pignorament','stipend'],pensione:['pignorament','pension'],testamento:['testament','legittim'],notaio:['testament','succession'],compromesso:['preliminar','contratt']};
function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function radice(w){return w.length>4?w.replace(/(e|i|a|o)$/,'').replace(/(h)$/,''):w}
function parole(s){return norm(s).split(/[^a-z0-9]+/).filter(Boolean)}
function prepara(ix){ix.forEach(function(p){p._t=parole(p.t.split(' · ')[0]);p._d=parole(p.d);p._k=parole(p.k)});return ix}
function carica(){if(IX)return Promise.resolve(IX);return fetch('/cerca.json').then(function(r){return r.json()}).then(function(j){IX=prepara(j);return IX})}
function ha(lista,r){for(var k=0;k<lista.length;k++)if(lista[k].indexOf(r)===0)return true;return false}
function cerca(ix,q){
 var ter=parole(q).filter(function(w){return w.length>1&&!STOP[w]}).map(function(w){return [radice(w)].concat(SIN[w]||[])});
 if(!ter.length)return null;
 var out=[];
 ix.forEach(function(p){var s=0,m=0;
  ter.forEach(function(vs){var best=0;vs.forEach(function(r,j){var v=ha(p._t,r)?6:ha(p._d,r)?3:ha(p._k,r)?1:0;if(j>0)v=v*0.6;if(v>best)best=v});if(best){m++;s+=best}});
  if(m&&m>=(ter.length>2?ter.length-1:ter.length))out.push({p:p,s:s+m*10+(p.c==='Guida'?0.5:0)})});
 out.sort(function(a,b){return b.s-a.s});return out.slice(0,24).map(function(x){return x.p})}
function el(t,cls,txt){var e=document.createElement(t);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
function mostra(q,res){
 o.textContent='';
 if(res===null){n.textContent='Scriva una o più parole: la ricerca guarda tra guide, competenze, glossario, strumenti e pagine dei comuni.';if(c)c.hidden=false;document.title=T0;return}
 document.title='"'+q+'" · Cerca · Studio Legale Pernorio';
 if(!res.length){n.textContent='Nessun risultato per "'+q+'". Provi con una parola più generale, oppure chiami lo Studio allo 0381 386276: la sua questione potrebbe comunque rientrare tra quelle seguite.';if(c)c.hidden=false;return}
 n.textContent=res.length===1?'1 risultato per "'+q+'"':res.length+' risultati per "'+q+'"';if(c)c.hidden=true;
 res.forEach(function(p){var a=el('a','card glink');a.href=p.u.replace(/^https?:\/\/[^/]+/,'')||'/';
  a.appendChild(el('span','label',p.c||'Pagina'));a.appendChild(el('b',null,p.t.split(' · ')[0]));a.appendChild(el('span',null,p.d));o.appendChild(a)})}
function vai(push){var q=i.value.trim();
 try{var u=new URL(location.href);if(q)u.searchParams.set('q',q);else u.searchParams.delete('q');history[push?'pushState':'replaceState'](null,'',u)}catch(e){}
 if(!q){mostra('',null);return}
 carica().then(function(ix){if(i.value.trim()===q)mostra(q,cerca(ix,q))}).catch(function(){n.textContent='La ricerca non è disponibile in questo momento. Può consultare le guide dal menu.'})}
f.addEventListener('submit',function(e){e.preventDefault();vai(true);i.blur()});
i.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(function(){vai(false)},160)});
addEventListener('popstate',leggi);
function leggi(){var q='';try{q=new URLSearchParams(location.search).get('q')||''}catch(e){}i.value=q;if(q)vai(false);else{mostra('',null);if(innerWidth>900)i.focus()}}
leggi();
})();
"""


def opensearch():
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">\n'
            "<ShortName>Studio Pernorio</ShortName>\n"
            "<LongName>Studio Legale Pernorio, Vigevano</LongName>\n"
            "<Description>Cerca tra le guide legali, il glossario e le competenze dello Studio Legale Pernorio di Vigevano</Description>\n"
            "<InputEncoding>UTF-8</InputEncoding>\n<Language>it-IT</Language>\n"
            f'<Image width="192" height="192" type="image/png">{BASE}/img/icon-192.png</Image>\n'
            f'<Url type="text/html" method="get" template="{BASE}/cerca?q={{searchTerms}}"/>\n'
            f'<Url type="application/opensearchdescription+xml" rel="self" template="{BASE}/opensearch.xml"/>\n'
            "</OpenSearchDescription>\n")


def search_action():
    return {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": BASE + "/cerca?q={search_term_string}"},
            "query-input": "required name=search_term_string"}


HEAD_LINKS = ('<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Studio Legale Pernorio">'
              '<link rel="alternate" type="application/atom+xml" href="/feed.xml" title="Guide dello Studio Legale Pernorio">')


# ---------------------------------------------------------------------------
# Feed Atom e sitemap
# ---------------------------------------------------------------------------

def feed_atom(voci):
    """voci: elenco di dict con url, titolo, sommario, pub, mod, cat."""
    voci = sorted(voci, key=lambda v: (v["mod"], v["pub"], v["titolo"]), reverse=True)
    agg = max(v["mod"] for v in voci)
    x = html.escape
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="it">',
           "<title>Studio Legale Pernorio · Guide pratiche</title>",
           "<subtitle>Guide di diritto civile dell'Avv. Daniela Pernorio, Vigevano: famiglia, eredità, casa, debiti, lavoro</subtitle>",
           f'<link rel="self" type="application/atom+xml" href="{BASE}/feed.xml"/>',
           f'<link rel="alternate" type="text/html" href="{BASE}/guide"/>',
           f"<id>{BASE}/feed.xml</id>", f"<updated>{agg}T08:00:00+01:00</updated>",
           f"<icon>{BASE}/img/icon-192.png</icon>",
           f"<author><name>Avv. Daniela Pernorio</name><uri>{BASE}/studio</uri></author>",
           "<rights>Studio Legale Pernorio, Vigevano</rights>"]
    for v in voci:
        out.append("<entry>"
                   f"<title>{x(v['titolo'])}</title>"
                   f'<link rel="alternate" type="text/html" href="{v["url"]}"/>'
                   f"<id>{v['url']}</id>"
                   f"<published>{v['pub']}T08:00:00+01:00</published><updated>{v['mod']}T08:00:00+01:00</updated>"
                   f'<category term="{x(v["cat"], quote=True)}"/>'
                   f"<summary>{x(v['sommario'])}</summary>"
                   "</entry>")
    out.append("</feed>")
    return "\n".join(out) + "\n"


def immagini_pagina(slug, h, ha_og):
    """Immagini da dichiarare nella sitemap: anteprima della pagina e fotografie del contenuto."""
    imgs = [f"{BASE}/og/{slug}.jpg"] if ha_og else []
    m = re.search(r"<main>(.*)</main>", h, re.S)
    for src in re.findall(r'<img[^>]+src="([^"]+\.webp)"', m.group(1) if m else ""):
        u = BASE + "/" + src.lstrip("/")
        if u not in imgs:
            imgs.append(u)
    return imgs[:6]


def sitemap(righe):
    """righe: (url, mod, priorità, immagini)."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for url, mod, prio, imgs in righe:
        im = "".join(f"<image:image><image:loc>{u}</image:loc></image:image>" for u in imgs)
        out.append(f"<url><loc>{url}</loc><lastmod>{mod}</lastmod><priority>{prio}</priority>{im}</url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Catalogo delle API per gli agenti (RFC 9727, /.well-known/api-catalog)
# ---------------------------------------------------------------------------

def api_catalog():
    return {"linkset": [
        {"anchor": BASE + "/mcp",
         "service-desc": [{"href": BASE + "/.well-known/mcp/server-card.json", "type": "application/json"}],
         "service-doc": [{"href": BASE + "/llms.txt", "type": "text/plain"}]},
        {"anchor": BASE + "/cerca.json",
         "service-doc": [{"href": BASE + "/llms.txt", "type": "text/plain"}],
         "item": [{"href": BASE + "/feed.xml", "type": "application/atom+xml"},
                  {"href": BASE + "/sitemap.xml", "type": "application/xml"},
                  {"href": BASE + "/llms-full.txt", "type": "text/plain"}]},
    ]}


HEADERS = """
# Ricerca, feed e scoperta per agenti (generato da tools/build.py)
/opensearch.xml
  Content-Type: application/opensearchdescription+xml; charset=utf-8
  Cache-Control: public, max-age=86400

/feed.xml
  Content-Type: application/atom+xml; charset=utf-8
  Access-Control-Allow-Origin: *
  Cache-Control: public, max-age=3600

/cerca.js
  Cache-Control: public, max-age=3600

/.well-known/api-catalog
  Content-Type: application/linkset+json; charset=utf-8
  Access-Control-Allow-Origin: *

/
  Link: </llms.txt>; rel="describedby"; type="text/plain", </sitemap.xml>; rel="sitemap"; type="application/xml", </feed.xml>; rel="alternate"; type="application/atom+xml", </.well-known/api-catalog>; rel="api-catalog", </index.md>; rel="alternate"; type="text/markdown"
"""

CSS = """
/* --- ricerca e glossario --- */
.sform{display:flex;gap:10px;align-items:stretch}
.sform input[type=search]{flex:1;min-width:0;font:inherit;font-size:1rem;padding:13px 16px;border:1px solid var(--rule);border-radius:var(--r-sm);background:var(--paper);color:var(--ink);min-height:50px;-webkit-appearance:none;appearance:none}
.sform input[type=search]:focus{outline:none;border-color:var(--forest);box-shadow:0 0 0 3px color-mix(in srgb,var(--forest) 15%,transparent)}
.sform .btn{flex:none}
#sc[hidden]{display:none}
.phero .sform{margin-top:22px;max-width:620px}
@media (max-width:480px){.sform .btn{padding-inline:16px}}
.article h3[id]{scroll-margin-top:96px}.article h2[id]{scroll-margin-top:96px}
.article .gl-f{display:block;margin-top:6px;font-size:.84rem;color:var(--graphite)}
.article h3:target{background:color-mix(in srgb,var(--forest) 9%,transparent);box-shadow:0 0 0 8px color-mix(in srgb,var(--forest) 9%,transparent);border-radius:4px}
"""
