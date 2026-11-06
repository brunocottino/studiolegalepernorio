#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misura se gli assistenti IA nominano lo Studio quando un cliente chiede un avvocato.

Idea ripresa da elmo, GetCito e Sanrovax/ai-visibility-checker: si fanno le
stesse domande "da cliente" (senza mai nominare lo Studio) a più motori con
ricerca web attiva, e si conta in quante risposte compare lo Studio. Ogni motore
cita fonti diverse (bassa sovrapposizione), quindi si misura motore per motore.

Usa solo le chiavi presenti nell'ambiente; senza chiavi mostra le domande.
    GEMINI_API_KEY      Gemini con Google Search (il più vicino agli AI Overviews)
    OPENAI_API_KEY      OpenAI Responses con web_search
    PERPLEXITY_API_KEY  Perplexity Sonar
    ANTHROPIC_API_KEY   Claude con web_search
Modelli modificabili con GEMINI_MODEL, OPENAI_MODEL, PERPLEXITY_MODEL, ANTHROPIC_MODEL.

Uso:
    python3 tools/visibilita_ia.py --prova     # solo l'elenco delle domande
    python3 tools/visibilita_ia.py             # esegue e aggiunge una riga a dati/visibilita-ia.csv
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOMI = ("pernorio", "studiolegalepernorio")

DOMANDE = [
    "Mi serve un avvocato per una separazione a Vigevano, chi mi consigli?",
    "Avvocato divorzista in Lomellina: quali studi ci sono?",
    "Chi è un buon avvocato per l'affidamento dei figli in provincia di Pavia, zona Vigevano?",
    "Devo fare una successione a Vigevano, mi serve un avvocato: a chi posso rivolgermi?",
    "Avvocato per sfratto per morosità a Vigevano",
    "Ho debiti con una finanziaria e vorrei fare un saldo e stralcio, avvocato vicino a Mortara?",
    "Avvocato civilista a Garlasco o vicino",
    "Avvocato a Gambolò per una questione di eredità",
    "Avvocato per amministrazione di sostegno a Vigevano",
    "Studio legale a Cassolnovo o Cilavegna per questioni di famiglia",
    "Avvocato per ricorso contro una multa autovelox in Lomellina",
    "Chi fa domiciliazioni al Tribunale di Pavia?",
    "Avvocato per unioni civili e convivenze vicino ad Abbiategrasso",
    "Quanto costa un avvocato per una separazione consensuale a Vigevano?",
    "Avvocato che fa colloqui online per diritto di famiglia in Lombardia",
]


def _post(url, corpo, headers):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def gemini(q):
    m = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
              {"contents": [{"parts": [{"text": q}]}], "tools": [{"google_search": {}}]},
              {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    return json.dumps(d, ensure_ascii=False)


def openai(q):
    d = _post("https://api.openai.com/v1/responses",
              {"model": os.environ.get("OPENAI_MODEL", "gpt-4.1"), "tools": [{"type": "web_search"}], "input": q},
              {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
    return json.dumps(d, ensure_ascii=False)


def perplexity(q):
    d = _post("https://api.perplexity.ai/chat/completions",
              {"model": os.environ.get("PERPLEXITY_MODEL", "sonar"), "messages": [{"role": "user", "content": q}]},
              {"Authorization": "Bearer " + os.environ["PERPLEXITY_API_KEY"]})
    return json.dumps(d, ensure_ascii=False)


def claude(q):
    d = _post("https://api.anthropic.com/v1/messages",
              {"model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"), "max_tokens": 1500,
               "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
               "messages": [{"role": "user", "content": q}]},
              {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
    return json.dumps(d, ensure_ascii=False)


MOTORI = {"gemini": ("GEMINI_API_KEY", gemini), "openai": ("OPENAI_API_KEY", openai),
          "perplexity": ("PERPLEXITY_API_KEY", perplexity), "claude": ("ANTHROPIC_API_KEY", claude)}


def main():
    if "--prova" in sys.argv:
        print("\n".join(f"{i:2}. {q}" for i, q in enumerate(DOMANDE, 1)))
        return
    attivi = {n: f for n, (k, f) in MOTORI.items() if os.environ.get(k)}
    if not attivi:
        sys.exit("Nessuna chiave API nell'ambiente: vedere l'intestazione del file.")
    os.makedirs(os.path.join(ROOT, "dati"), exist_ok=True)
    out = os.path.join(ROOT, "dati", "visibilita-ia.csv")
    nuovo = not os.path.exists(out)
    with open(out, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if nuovo:
            w.writerow(["data", "motore", "domanda", "studio_citato"])
        for nome, fn in attivi.items():
            ok = 0
            for q in DOMANDE:
                try:
                    testo = fn(q).lower()
                    hit = any(n in testo for n in NOMI)
                except Exception as e:  # noqa: BLE001
                    print(f"  {nome}: errore su «{q[:40]}…»: {e}")
                    continue
                ok += hit
                w.writerow([date.today().isoformat(), nome, q, int(hit)])
            print(f"{nome}: Studio citato in {ok} risposte su {len(DOMANDE)}")


if __name__ == "__main__":
    main()
