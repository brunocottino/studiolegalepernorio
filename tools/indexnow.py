#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avvisa Bing, Yandex, Seznam, Naver (e chi aderisce a IndexNow) degli URL cambiati.

Da lanciare SOLO dopo la pubblicazione su Netlify, quando i nuovi URL sono online.
Bing alimenta anche Copilot e la ricerca di ChatGPT: un avviso immediato accorcia
i tempi di indicizzazione da giorni a ore.

Uso:
    python3 tools/indexnow.py            # tutti gli URL della sitemap in dist/
    python3 tools/indexnow.py --prova    # mostra cosa invierebbe, senza inviare
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "studiolegalepernorio.com"


def main():
    chiavi = [f for f in os.listdir(os.path.join(ROOT, "static", "root")) if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
    if not chiavi:
        sys.exit("Chiave IndexNow non trovata in static/root/")
    key = chiavi[0][:-4]
    sm = open(os.path.join(ROOT, "dist", "sitemap.xml"), encoding="utf-8").read()
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    corpo = {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}
    print(f"{len(urls)} URL, chiave {key}")
    if "--prova" in sys.argv:
        print("\n".join(urls[:10]) + ("\n…" if len(urls) > 10 else ""))
        return
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(corpo).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print("Risposta IndexNow:", r.status, "(200 o 202 = ricevuto)")


if __name__ == "__main__":
    main()
