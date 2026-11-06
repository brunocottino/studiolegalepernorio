#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit SEO, GEO e "agent experience" del sito generato in dist/.

Controlli ripresi e adattati da progetti open source studiati a novembre 2026:
- squirrelscan (regole Agent Experience, entity map, token weight, E-E-A-T)
- GEO Optimizer / geo-optimizer-skill (bot IA, llms.txt, Google AI readiness, WebMCP)
- claude-seo (local SEO: NAP, swap test anti pagine-doorway)
- WebMCP del W3C Web Machine Learning group (strumenti esposti agli agenti)

Lavora solo sui file di dist/, senza rete. Uso:
    python3 tools/build.py && python3 tools/audit.py   # scrive AUDIT.md
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
BASE = "https://studiolegalepernorio.com"

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Googlebot", "Google-Extended", "Bingbot", "Applebot",
           "Applebot-Extended", "DuckAssistBot", "meta-externalagent", "Amazonbot", "MistralAI-User"]

TEL = "+390381386276"


def leggi(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def testo_visibile(soup):
    s = BeautifulSoup(str(soup), "lxml")
    for t in s(["script", "style", "noscript", "template", "svg"]):
        t.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ")).strip()


def shingles(testo, k=5):
    w = re.findall(r"\w+", testo.lower())
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def ld_blocchi(soup):
    out = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string or "")
        except json.JSONDecodeError as e:
            out.append({"_errore": str(e)})
            continue
        stack = d if isinstance(d, list) else [d]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if "@graph" in x:
                    stack.extend(x["@graph"])
                    continue
                out.append(x)
            elif isinstance(x, list):
                stack.extend(x)
    return out


def tipi(o):
    t = o.get("@type", [])
    return set(t if isinstance(t, list) else [t])


def main():
    if not os.path.isdir(DIST):
        sys.exit("dist/ mancante: lanciare prima python3 tools/build.py")
    problemi = defaultdict(list)   # severità -> elenco
    info = []

    def p(sev, msg):
        problemi[sev].append(msg)

    pagine = {fn[:-5]: leggi(os.path.join(DIST, fn)) for fn in sorted(os.listdir(DIST)) if fn.endswith(".html")}
    indicizzabili = {k for k, v in pagine.items() if 'name="robots" content="noindex' not in v}
    titoli, descr, testi = {}, {}, {}
    link_in = Counter()
    entita = defaultdict(set)      # @id -> pagine
    ratio = {}

    for slug, h in pagine.items():
        soup = BeautifulSoup(h, "lxml")
        url = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
        t = soup.title.string.strip() if soup.title and soup.title.string else ""
        d = (soup.find("meta", attrs={"name": "description"}) or {}).get("content", "")
        titoli[slug], descr[slug] = t, d
        txt = testo_visibile(soup.body or soup)
        testi[slug] = txt
        ratio[slug] = len(txt.encode()) / max(1, len(h.encode()))
        if slug not in indicizzabili:
            continue
        # Core SEO
        if not 25 <= len(t) <= 65:
            p("avviso", f"`{slug}`: title di {len(t)} caratteri (ideale 25-65)")
        if not 70 <= len(d) <= 160:
            p("avviso", f"`{slug}`: description di {len(d)} caratteri (ideale 70-160)")
        h1 = soup.find_all("h1")
        if len(h1) != 1:
            p("errore", f"`{slug}`: {len(h1)} H1")
        can = soup.find("link", rel="canonical")
        if not can or can.get("href") != url:
            p("errore", f"`{slug}`: canonical {can.get('href') if can else 'assente'} invece di {url}")
        if soup.find("html").get("lang") != "it":
            p("errore", f"`{slug}`: lang diverso da it")
        # Google AI: nessuna restrizione di snippet
        rob = (soup.find("meta", attrs={"name": "robots"}) or {}).get("content", "")
        if "nosnippet" in rob or "max-snippet:0" in rob:
            p("errore", f"`{slug}`: snippet bloccati, la pagina non può essere citata in AI Overviews")
        # Immagini
        for img in soup.find_all("img"):
            if img.get("alt") is None:
                p("avviso", f"`{slug}`: immagine senza alt ({img.get('src')})")
            if not (img.get("width") and img.get("height")):
                p("info", f"`{slug}`: immagine senza width/height ({img.get('src')}), rischio CLS")
        # Link interni
        for a in soup.find_all("a", href=True):
            hr = a["href"].split("#")[0].split("?")[0]
            if hr.startswith(BASE):
                hr = hr[len(BASE):]
            if not hr.startswith("/") or hr.startswith("//"):
                continue
            target = hr.strip("/") or "index"
            if target.endswith(".html"):
                p("avviso", f"`{slug}`: link interno con .html ({hr})")
                target = target[:-5]
            if os.path.splitext(target)[1]:
                if not os.path.exists(os.path.join(DIST, target)):
                    p("errore", f"`{slug}`: file collegato inesistente {hr}")
                continue
            if target not in pagine:
                p("errore", f"`{slug}`: link rotto {hr}")
            elif target != slug:
                link_in[target] += 1
        # Dati strutturati
        for o in ld_blocchi(soup):
            if "_errore" in o:
                p("errore", f"`{slug}`: JSON-LD non valido ({o['_errore']})")
                continue
            if o.get("@id"):
                entita[o["@id"]].add(slug)
            ty = tipi(o)
            if ty & {"Article", "BlogPosting"}:
                for campo in ("headline", "author", "datePublished", "dateModified"):
                    if not o.get(campo):
                        p("avviso", f"`{slug}`: Article senza {campo}")
            if "FAQPage" in ty:
                n = len(o.get("mainEntity", []))
                if n == 0:
                    p("errore", f"`{slug}`: FAQPage vuota")
        # E-E-A-T sulle guide: firma e data visibili
        if slug.startswith("guida-"):
            if "Pernorio" not in txt:
                p("avviso", f"`{slug}`: guida senza firma dell'avvocato visibile")
            if not re.search(r"aggiornat[oa]", txt, re.I):
                p("avviso", f"`{slug}`: guida senza data di aggiornamento visibile")
        # NAP visibile
        if TEL not in h.replace(" ", ""):
            p("info", f"`{slug}`: numero di telefono non presente in un link tel:")
        # Agent experience
        if not soup.find("link", attrs={"type": "text/markdown"}):
            p("info", f"`{slug}`: nessuna versione Markdown segnalata (rel=alternate type=text/markdown)")
        if ratio[slug] < 0.15:
            p("info", f"`{slug}`: testo visibile al {ratio[slug]:.0%} dell'HTML (token weight)")

    # Duplicati
    for nome, mappa in (("title", titoli), ("description", descr)):
        c = Counter(v for k, v in mappa.items() if k in indicizzabili)
        for v, n in c.items():
            if n > 1:
                p("errore", f"{nome} duplicato su {n} pagine: «{v[:70]}»")
    # Pagine orfane
    for slug in sorted(indicizzabili - {"index"}):
        if link_in[slug] == 0:
            p("avviso", f"`{slug}`: pagina orfana (nessun link interno)")
        elif link_in[slug] == 1:
            info.append(f"`{slug}` ha un solo link interno in entrata")
    # Swap test (claude-seo): pagine dei comuni troppo simili = rischio doorway
    comuni = [s for s in indicizzabili if s.startswith("avvocato-")]
    sh = {s: shingles(testi[s]) for s in comuni}
    simili = []
    for a, b in combinations(sorted(comuni), 2):
        j = len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b]))
        simili.append((j, a, b))
        if j > 0.5:
            p("avviso", f"`{a}` e `{b}` simili al {j:.0%}: rischio pagine doorway")
    if simili:
        j, a, b = max(simili)
        info.append(f"Pagine dei comuni: somiglianza massima {j:.0%} ({a} / {b}); soglia di allarme 50%")
    # Entity map (squirrelscan): una sola identità per lo Studio
    if entita:
        rif = {k: sum(1 for h in pagine.values() if f'"{k}"' in h) for k in (BASE + "/#studio", BASE + "/#avvocato", BASE + "/#sito")}
        per_pagina = sum(1 for k in entita if k.endswith("#pagina"))
        info.append("Grafo delle entità: " + ", ".join(f"{k.replace(BASE, '')} citato in {n} pagine" for k, n in rif.items())
                    + f"; {per_pagina} pagine con nodo WebPage proprio")
    else:
        p("avviso", "Nessun @id nei dati strutturati: lo Studio rischia di apparire come entità diverse su ogni pagina")
    # File di sito
    robots = leggi(os.path.join(DIST, "robots.txt"))
    mancanti = [b for b in AI_BOTS if b.lower() not in robots.lower()]
    if re.search(r"User-agent: \*\s*\nAllow: /", robots):
        info.append("robots.txt: `User-agent: *` consente tutto; bot IA non citati esplicitamente: " + (", ".join(mancanti) or "nessuno"))
    if "Content-Signal" not in robots:
        p("info", "robots.txt senza Content-Signal (politica per scopo: search, ai-input, ai-train)")
    for fn in ("llms.txt", "llms-full.txt", "sitemap.xml"):
        if not os.path.exists(os.path.join(DIST, fn)):
            p("errore", f"{fn} mancante")
    llms = leggi(os.path.join(DIST, "llms.txt"))
    if not llms.startswith("# ") or "\n> " not in llms:
        p("avviso", "llms.txt non segue il formato (titolo H1 + riassunto in blockquote)")
    sm = leggi(os.path.join(DIST, "sitemap.xml"))
    for slug in indicizzabili:
        u = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
        if f"<loc>{u}</loc>" not in sm:
            p("errore", f"`{slug}` assente dalla sitemap")
    # WebMCP
    js = [f for f in os.listdir(DIST) if f.endswith(".js")]
    if not any("modelContext" in leggi(os.path.join(DIST, f)) for f in js):
        p("info", "Nessuno strumento WebMCP (document.modelContext.registerTool) per gli agenti nel browser")
    if not any("toolname=" in h for h in pagine.values()):
        p("info", "Nessun modulo con attributi WebMCP dichiarativi (toolname, tooldescription)")
    tw = sorted(ratio.items(), key=lambda x: x[1])[:3]
    info.append("Token weight più basso: " + ", ".join(f"{k} {v:.0%}" for k, v in tw))

    # Report
    righe = ["# Audit del sito (dist/)", "", f"Pagine HTML: {len(pagine)}, indicizzabili: {len(indicizzabili)}.", ""]
    for sev in ("errore", "avviso", "info"):
        lst = problemi.get(sev, [])
        righe.append(f"## {sev.capitalize()} ({len(lst)})")
        righe.append("")
        righe += [f"- {x}" for x in lst[:80]] or ["- Nessuno"]
        if len(lst) > 80:
            righe.append(f"- … altri {len(lst) - 80}")
        righe.append("")
    righe += ["## Note", ""] + [f"- {x}" for x in info]
    out = "\n".join(righe) + "\n"
    with open(os.path.join(ROOT, "AUDIT.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"Errori {len(problemi['errore'])}, avvisi {len(problemi['avviso'])}, info {len(problemi['info'])} -> AUDIT.md")
    return 1 if problemi["errore"] else 0


if __name__ == "__main__":
    sys.exit(main())
