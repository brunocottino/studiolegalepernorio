# -*- coding: utf-8 -*-
"""Fonti normative delle guide, con link permanenti a Normattiva (URN:NIR).

Perché: lo studio GEO di Princeton (KDD 2024) mostra che le pagine che citano
fonti precise vengono riprese più spesso nelle risposte dei motori IA. Per un
contenuto legale (YMYL) è anche il segnale di affidabilità più forte.
Ogni link usa il risolutore ufficiale https://www.normattiva.it/uri-res/N2Ls?<URN>,
verificato con tools/fonti.py --verifica.
"""
import sys
import time
import urllib.request

R = "https://www.normattiva.it/uri-res/N2Ls?"
CC = "urn:nir:stato:codice.civile:1942-03-16;262"
CPC = "urn:nir:stato:codice.procedura.civile:1940-10-28;1443"
CDS = "urn:nir:stato:decreto.legislativo:1992-04-30;285"
L392 = "urn:nir:stato:legge:1978-07-27;392"
L898 = "urn:nir:stato:legge:1970-12-01;898"
L76 = "urn:nir:stato:legge:2016-05-20;76"
DL132 = "urn:nir:stato:decreto.legge:2014-09-12;132"

ATTI = {  # URN dell'atto -> nome per esteso (per i dati strutturati)
    CC: "Codice civile (R.D. 16 marzo 1942, n. 262)",
    CPC: "Codice di procedura civile (R.D. 28 ottobre 1940, n. 1443)",
    CDS: "Codice della strada (D.Lgs. 30 aprile 1992, n. 285)",
    L392: "Legge 27 luglio 1978, n. 392 (equo canone)",
    L898: "Legge 1 dicembre 1970, n. 898 (divorzio)",
    L76: "Legge 20 maggio 2016, n. 76 (unioni civili e convivenze)",
    DL132: "D.L. 12 settembre 2014, n. 132 (negoziazione assistita)",
    "urn:nir:stato:legge:2004-01-09;6": "Legge 9 gennaio 2004, n. 6 (amministrazione di sostegno)",
    "urn:nir:stato:legge:1998-12-09;431": "Legge 9 dicembre 1998, n. 431 (locazioni abitative)",
    "urn:nir:stato:legge:1966-07-15;604": "Legge 15 luglio 1966, n. 604 (licenziamenti individuali)",
    "urn:nir:stato:decreto.legislativo:2015-03-04;23": "D.Lgs. 4 marzo 2015, n. 23 (tutele crescenti)",
    "urn:nir:stato:decreto.legislativo:2005-09-07;209": "D.Lgs. 7 settembre 2005, n. 209 (Codice delle assicurazioni private)",
    "urn:nir:stato:decreto.legislativo:2010-03-04;28": "D.Lgs. 4 marzo 2010, n. 28 (mediazione civile)",
    "urn:nir:stato:decreto.legislativo:1990-10-31;346": "D.Lgs. 31 ottobre 1990, n. 346 (Testo unico imposta di successione)",
    "urn:nir:stato:decreto.legislativo:2012-09-07;155": "D.Lgs. 7 settembre 2012, n. 155 (geografia giudiziaria)",
}


def f(etichetta, atto, art=None):
    urn = atto + (f"~art{art}" if art else "")
    return {"etichetta": etichetta, "urn": urn, "atto": atto, "url": R + urn}


FONTI = {
    "guida-affidamento-figli-condiviso-esclusivo": [
        f("Art. 337-ter c.c., provvedimenti riguardo ai figli", CC, "337ter"),
        f("Art. 337-quater c.c., affidamento a un solo genitore", CC, "337quater"),
        f("Art. 337-sexies c.c., assegnazione della casa familiare", CC, "337sexies"),
    ],
    "guida-amministrazione-di-sostegno": [
        f("Art. 404 c.c., amministrazione di sostegno", CC, "404"),
        f("Art. 407 c.c., procedimento", CC, "407"),
        f("Legge 6/2004", "urn:nir:stato:legge:2004-01-09;6"),
    ],
    "guida-assegno-mantenimento-figli": [
        f("Art. 337-ter c.c., mantenimento dei figli", CC, "337ter"),
        f("Art. 337-septies c.c., figli maggiorenni", CC, "337septies"),
        f("Art. 316-bis c.c., concorso negli oneri", CC, "316bis"),
    ],
    "guida-casa-familiare-separazione": [
        f("Art. 337-sexies c.c., assegnazione della casa familiare", CC, "337sexies"),
        f("Art. 337-ter c.c., provvedimenti riguardo ai figli", CC, "337ter"),
    ],
    "guida-costo-separazione-consensuale": [
        f("Art. 6 D.L. 132/2014, negoziazione assistita per separazione e divorzio", DL132, "6"),
        f("Art. 12 D.L. 132/2014, separazione davanti al sindaco", DL132, "12"),
        f("Art. 158 c.c., separazione consensuale", CC, "158"),
    ],
    "guida-fine-convivenza-diritti": [
        f("Legge 76/2016, art. 1 commi 36-65 (convivenze di fatto)", L76, "1"),
        f("Art. 337-ter c.c., figli di genitori non sposati", CC, "337ter"),
    ],
    "guida-divorzio-tempi": [
        f("Art. 3 Legge 898/1970, casi e termini del divorzio", L898, "3"),
        f("Art. 5 Legge 898/1970, assegno divorzile", L898, "5"),
        f("Art. 6 D.L. 132/2014, divorzio con negoziazione assistita", DL132, "6"),
    ],
    "guida-eredita-con-debiti": [
        f("Art. 470 c.c., accettazione con beneficio d'inventario", CC, "470"),
        f("Art. 485 c.c., erede nel possesso dei beni", CC, "485"),
        f("Art. 519 c.c., rinunzia all'eredità", CC, "519"),
        f("Art. 480 c.c., prescrizione del diritto di accettare", CC, "480"),
    ],
    "guida-testamento-olografo": [
        f("Art. 602 c.c., testamento olografo", CC, "602"),
        f("Art. 620 c.c., pubblicazione del testamento olografo", CC, "620"),
        f("Art. 536 c.c., legittimari", CC, "536"),
    ],
    "guida-deposito-cauzionale-affitto": [
        f("Art. 11 Legge 392/1978, deposito cauzionale", L392, "11"),
        f("Art. 1590 c.c., restituzione della cosa locata", CC, "1590"),
    ],
    "guida-diritti-inquilino": [
        f("Art. 1575 c.c., obblighi del locatore", CC, "1575"),
        f("Art. 1576 c.c., riparazioni", CC, "1576"),
        f("Art. 1609 c.c., piccole riparazioni a carico dell'inquilino", CC, "1609"),
        f("Legge 431/1998, locazioni abitative", "urn:nir:stato:legge:1998-12-09;431"),
    ],
    "guida-licenziamento-cosa-fare": [
        f("Art. 6 Legge 604/1966, termini di impugnazione", "urn:nir:stato:legge:1966-07-15;604", "6"),
        f("D.Lgs. 23/2015, contratto a tutele crescenti", "urn:nir:stato:decreto.legislativo:2015-03-04;23"),
        f("Art. 2119 c.c., giusta causa", CC, "2119"),
    ],
    "guida-incidente-stradale-cosa-fare": [
        f("Art. 2054 c.c., circolazione dei veicoli", CC, "2054"),
        f("Art. 148 Codice delle assicurazioni, procedura di risarcimento", "urn:nir:stato:decreto.legislativo:2005-09-07;209", "148"),
        f("Art. 149 Codice delle assicurazioni, indennizzo diretto", "urn:nir:stato:decreto.legislativo:2005-09-07;209", "149"),
    ],
    "guida-prestito-tra-privati": [
        f("Art. 1813 c.c., mutuo", CC, "1813"),
        f("Art. 1815 c.c., interessi", CC, "1815"),
        f("Art. 2946 c.c., prescrizione ordinaria", CC, "2946"),
    ],
    "guida-impugnare-delibera-condominiale": [
        f("Art. 1137 c.c., impugnazione delle deliberazioni", CC, "1137"),
        f("Art. 1136 c.c., costituzione dell'assemblea e validità delle deliberazioni", CC, "1136"),
        f("D.Lgs. 28/2010, mediazione obbligatoria in condominio", "urn:nir:stato:decreto.legislativo:2010-03-04;28", "5"),
    ],
    "guida-pignoramento-stipendio-pensione": [
        f("Art. 545 c.p.c., crediti impignorabili", CPC, "545"),
        f("Art. 543 c.p.c., pignoramento presso terzi", CPC, "543"),
    ],
    "guida-domiciliazioni-tribunale-pavia": [
        f("D.Lgs. 155/2012, soppressione del Tribunale di Vigevano", "urn:nir:stato:decreto.legislativo:2012-09-07;155"),
    ],
    "guida-multa-autovelox-2026": [
        f("Art. 142 Codice della strada, limiti di velocità", CDS, "142"),
        f("Art. 202 Codice della strada, pagamento in misura ridotta", CDS, "202"),
        f("Art. 203 Codice della strada, ricorso al Prefetto", CDS, "203"),
        f("Art. 204-bis Codice della strada, ricorso al Giudice di Pace", CDS, "204bis"),
    ],
    "guida-negoziazione-assistita-o-mediazione": [
        f("Art. 2 D.L. 132/2014, convenzione di negoziazione assistita", DL132, "2"),
        f("Art. 3 D.L. 132/2014, negoziazione obbligatoria", DL132, "3"),
        f("Art. 5 D.Lgs. 28/2010, mediazione obbligatoria", "urn:nir:stato:decreto.legislativo:2010-03-04;28", "5"),
    ],
    "guida-saldo-e-stralcio-banche-finanziarie": [
        f("Art. 1965 c.c., transazione", CC, "1965"),
        f("Art. 1236 c.c., remissione del debito", CC, "1236"),
    ],
    "guida-scioglimento-unione-civile": [
        f("Legge 76/2016, art. 1 commi 22-26 (scioglimento)", L76, "1"),
        f("Art. 3 Legge 898/1970, richiamato per le unioni civili", L898, "3"),
    ],
    "guida-separazione-divorzio-unica-domanda": [
        f("Codice di procedura civile, rito unico per famiglia (artt. 473-bis e seguenti)", CPC),
        f("Art. 3 Legge 898/1970, termini per il divorzio", L898, "3"),
    ],
    "guida-sfratto-per-morosita": [
        f("Art. 658 c.p.c., intimazione di sfratto per morosità", CPC, "658"),
        f("Art. 55 Legge 392/1978, termine di grazia", L392, "55"),
        f("Art. 5 Legge 392/1978, inadempimento del conduttore", L392, "5"),
    ],
    "guida-successioni-autoliquidazione-imposta": [
        f("D.Lgs. 346/1990, Testo unico dell'imposta di successione", "urn:nir:stato:decreto.legislativo:1990-10-31;346"),
        f("Artt. 565 e seguenti c.c., successione legittima", CC, "565"),
    ],
    "guida-usucapione-quando-si-diventa-proprietari": [
        f("Art. 1158 c.c., usucapione ventennale", CC, "1158"),
        f("Art. 1159 c.c., usucapione decennale", CC, "1159"),
        f("Art. 1140 c.c., possesso", CC, "1140"),
    ],
}


def verifica():
    atti = sorted({x["atto"] for v in FONTI.values() for x in v})
    ok = True
    for a in atti:
        for tentativo in range(3):
            try:
                with urllib.request.urlopen(R + a, timeout=30) as r:
                    t = r.read().decode("utf-8", "ignore")
                break
            except Exception as e:  # noqa: BLE001
                t = ""
                err = e
                time.sleep(3)
        import re
        m = re.search(r"<title>(.*?)</title>", t, re.S)
        titolo = m.group(1).strip() if m else f"ERRORE {err}"
        buono = m and "Normattiva" in titolo and "errore" not in titolo.lower()
        ok &= bool(buono)
        print(("OK  " if buono else "NO  ") + a + "  ->  " + titolo)
        time.sleep(1.5)
    return ok


if __name__ == "__main__" and "--verifica" in sys.argv:
    sys.exit(0 if verifica() else 1)
