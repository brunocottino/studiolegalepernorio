#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build del sito Studio Legale Pernorio.

Legge le pagine originali da src/, applica le correzioni SEO e tecniche,
genera le pagine nuove e scrive il sito pronto per Netlify in dist/.

Uso:  python3 tools/build.py
"""
import html
import json
import os
import re
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
import contenuti as C  # noqa: E402
import guide_nuove as G  # noqa: E402
import colloquio as CO  # noqa: E402
import agenti as AG  # noqa: E402
import fonti as FO  # noqa: E402
import ricerche as RI  # noqa: E402
import trovabile as TR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
STATIC = os.path.join(ROOT, "static")
DIST = os.path.join(ROOT, "dist")
FUNZIONI = os.path.join(ROOT, "functions")  # Netlify Functions generate (server MCP)
BASE = "https://studiolegalepernorio.com"
OGGI = date.today().isoformat()
WA = "https://wa.me/393333368757?text=Buongiorno%20Avvocato%2C%20vorrei%20fissare%20un%20appuntamento."

INSTAGRAM = "https://www.instagram.com/studio_legale_pernorio/"
ORARI_TXT = "Lun – Ven 9:00 – 19:00, su appuntamento"
ICO_IG = '<svg class="ico" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>'

FONT_PRELOAD = (
    '<link rel="preload" href="/fonts/inter-56724408-latin.woff2" as="font" type="font/woff2" crossorigin>'
    '<link rel="preload" href="/fonts/cormorant-garamond-2fed1d1b-latin.woff2" as="font" type="font/woff2" crossorigin>'
)

# Parole chiave per le pagine materia: slug -> forma usata in title e H1
MATERIE_KW = {
    "separazione-divorzio": "separazione e divorzio",
    "affidamento-minori": "affidamento dei figli",
    "unioni-civili": "unioni civili e convivenze",
    "successioni": "successioni ed eredità",
    "amministrazione-di-sostegno": "amministrazione di sostegno",
    "locazioni-comodato": "affitti e comodato",
    "sfratti": "sfratti",
    "usucapione-diritti-reali": "usucapione e diritti reali",
    "condominio": "condominio",
    "saldo-e-stralcio": "saldo e stralcio",
    "recupero-crediti": "recupero crediti",
    "crisi-impresa": "sovraindebitamento",
    "contratti": "contratti",
    "sinistri-responsabilita": "incidenti e risarcimenti",
    "codice-della-strada": "ricorsi contro le multe",
    "lavoro": "diritto del lavoro",
    "negoziazione-assistita": "negoziazione assistita",
    "mediazione-civile": "mediazione civile",
}

# Strumenti collegati a guide e materie
STRUMENTI_LINK = {
    "guida-successioni-autoliquidazione-imposta": 3,
    "guida-eredita-con-debiti": 3,
    "guida-testamento-olografo": 0,
    "attivita-successioni": 0,
    "guida-multa-autovelox-2026": 1,
    "attivita-codice-della-strada": 1,
    "guida-separazione-divorzio-unica-domanda": 2,
    "attivita-separazione-divorzio": 2,
    "guida-affidamento-figli-condiviso-esclusivo": 2,
}


def esc(s):
    return html.escape(s, quote=True)


def clean_url(name):
    """'studio.html' -> https://studiolegalepernorio.com/studio ; index -> /"""
    name = name[:-5] if name.endswith(".html") else name
    return BASE + "/" if name in ("", "index") else f"{BASE}/{name}"


def trim(s, n=158):
    if len(s) <= n:
        return s
    return s[: s.rfind(" ", 0, n - 1)].rstrip(",;:") + "…"


# ---------------------------------------------------------------------------
# Template e frammenti estratti dalle pagine esistenti
# ---------------------------------------------------------------------------

TPL = open(os.path.join(SRC, "guida-sfratto-per-morosita.html"), encoding="utf-8").read()
_PRATICA = open(os.path.join(SRC, "attivita-separazione-divorzio.html"), encoding="utf-8").read()

ICO_TEL = re.search(r'<svg class="ico"[^>]*><path d="M5 4h4[^"]*"/></svg>', TPL).group(0)
ICO_ARR = '<svg class="ico" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICO_WA = '<svg class="ico" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>'
ICO_TEL16 = ICO_TEL.replace('width="15" height="15"', 'width="16" height="16"')
CTA_SECTION = re.search(r'<section style="padding-top:0"><div class="wrap"><div class="cta-card rv">.*?</div></div></section>', _PRATICA, re.S).group(0)


def btn(cls, href, label, ico, ext=False):
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="btn {cls} " href="{href}"{tgt}>{label}<span class="bi">{ico}</span></a>'


BTN_CALL = btn("btn-primary", "tel:+390381386276", "Chiama", ICO_TEL16)
BTN_WA = btn("btn-ghost", WA, "WhatsApp", ICO_WA, True)


def breadcrumb_ld(items):
    el = []
    for i, (name, url) in enumerate(items, 1):
        d = {"@type": "ListItem", "position": i, "name": name}
        if url:
            d["item"] = url
        el.append(d)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def faq_html(faq):
    det = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    return f'<div class="card panel faq rv"><h2>Domande frequenti</h2>{det}<p class="note-s">Indicazioni generali, aggiornate a {C.AGGIORNATO}. Ogni caso va valutato sui documenti.</p></div>'


def faq_ld(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }


def pagina(slug, title, description, crumbs, label, h1, lead, body, aside, extra_ld=(), extra_after="", script=""):
    """Costruisce una pagina nuova con lo stesso layout delle guide."""
    url = clean_url(slug)
    s = TPL
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, flags=re.S)
    description = trim(description)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(description)}">', s)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(title)}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(description)}">', s)
    s = s.replace("aria-current='page' ", "")
    crumb_nav = "".join(f"<a href='{u.replace(BASE, '') or '/'}'>{esc(n)}</a>" for n, u in crumbs[:-1])
    crumb_nav += f'<span class="cur">{esc(crumbs[-1][0])}</span>'
    main = (
        "<main>" + ld(breadcrumb_ld(crumbs))
        + f'<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Percorso">{crumb_nav}</nav>'
        + f'<span class="label">{esc(label)}</span><h1>{esc(h1)}</h1><p class=lead>{esc(lead)}</p>'
        + f'<div class=actions>{BTN_CALL}{BTN_WA}</div></div></section>\n'
        + '<section style="padding-top:0"><div class="wrap area-layout">\n'
        + f"<div>{body}</div>\n"
        + f'<aside style="display:grid;gap:14px;margin-top:14px">{aside}</aside>\n'
        + "</div></section>\n" + extra_after + CTA_SECTION
        + "".join(ld(x) for x in extra_ld) + script + "</main>"
    )
    s = re.sub(r"<main>.*</main>", lambda m: main, s, flags=re.S)
    return s


def aside_std(materia=None, extra=""):
    out = ""
    if materia:
        out += f"<a class='card panel rv gcard' href='/{materia[0]}'><span class=\"label\">Competenza</span><b>{esc(materia[1])}</b><span class=\"note-s\">Cosa fa lo Studio →</span></a>"
    out += extra
    out += f'<div class="card panel rv"><span class="label">Ne vuole parlare?</span><div class="actions" style="margin-top:14px">{BTN_CALL}{BTN_WA}</div></div>'
    out += zone_card()
    return out


def zone_card():
    chips = "".join(f"<a class='chip' href='/{c['slug']}'>{esc(c['nome'])}</a>" for c in C.COMUNI)
    chips += f"<a class='chip' href='/{C.LOMELLINA['slug']}'>Tutta la Lomellina</a>"
    return f'<div class="card panel rv"><span class="label">Dove riceviamo clienti</span><div class="chips" style="margin-top:14px">{chips}</div></div>'


def strumenti_card(only=None):
    lst = C.STRUMENTI if only is None else [C.STRUMENTI[only]]
    out = ""
    for t in lst:
        out += f"<a class='card panel rv gcard' href='/{t['slug']}'><span class=\"label\">Strumento gratuito</span><b>{esc(t['titolo_breve'])}</b><span class=\"note-s\">{esc(t['intro'])} →</span></a>"
    return out


# ---------------------------------------------------------------------------
# Pagine nuove
# ---------------------------------------------------------------------------

def pagine_comuni():
    out = {}
    for c in C.COMUNI:
        nome = c["nome"]
        title = f"Avvocato per {nome} · Studio Legale Pernorio, Vigevano"
        desc = trim(f"Avvocato civilista per chi vive a {nome}: separazioni, figli, eredità, casa, debiti. Studio a Vigevano, {c['km']} da {nome}. Tribunale competente, costi e contatti.")
        temi = "".join(
            f"<li><a href='/{s}'><strong>{esc(n)}</strong></a>: {esc(d)}.</li>" for s, n, d in c["temi"]
        )
        body = (
            '<article class="card panel article rv">'
            f"<p>{c['intro']}</p>"
            f"<h2>Come raggiungere lo Studio da {esc(nome)}</h2>"
            f"<p>{c['percorso']} La distanza è di {c['km']}, {c['min']} in auto. Si riceve dal lunedì al venerdì, su appuntamento: conviene telefonare allo <a href=\"tel:+390381386276\">0381 386276</a> o scrivere su <a href=\"{WA}\" target=\"_blank\" rel=\"noopener\">WhatsApp</a>.</p>"
            f"<h2>Il tribunale competente per {esc(nome)}</h2>"
            f"<p>{c['tribunale']}</p>"
            f"<h2>Le questioni che seguiamo per chi vive a {esc(nome)}</h2>"
            f"<ul>{temi}</ul>"
            "<p>L'elenco completo è nella pagina delle <a href='/attivita'>competenze</a>: diciotto materie del diritto civile, dalla famiglia ai contratti.</p>"
            "<h2>Come funziona</h2>"
            "<ol><li><strong>Contatto</strong>: per telefono, WhatsApp o con il modulo, indicando brevemente la questione.</li>"
            "<li><strong>Primo colloquio</strong> in Studio, con i documenti: l'avvocato spiega le strade possibili, i tempi e i rischi.</li>"
            "<li><strong>Preventivo scritto</strong> prima di iniziare. Nessuna sorpresa: <a href='/costi-avvocato'>come si forma il costo</a>.</li></ol>"
            f'<p class="note-s">Studio Legale Pernorio, Avv. Daniela Pernorio, Via Egidio Sacchetti 14, 27029 Vigevano (PV). Aggiornato a {C.AGGIORNATO}.</p>'
            "</article>" + faq_html(c["faq"])
        )
        crumbs = [("Home", BASE + "/"), ("Dove operiamo", clean_url(C.LOMELLINA["slug"])), (nome, None)]
        page_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": clean_url(c["slug"]) + "#pagina",
            "url": clean_url(c["slug"]),
            "name": title,
            "about": {"@id": BASE + "/#studio"},
            "isPartOf": {"@id": BASE + "/#sito"},
            "inLanguage": "it-IT",
            "spatialCoverage": {"@type": "City", "name": nome},
        }
        out[c["slug"]] = pagina(
            c["slug"], title, desc, crumbs, f"Dove operiamo · {nome}", f"Avvocato per chi vive a {nome}",
            f"Lo Studio Legale Pernorio è a Vigevano, {c['km']} da {nome}. Famiglia, eredità, casa, debiti, lavoro: assistenza civile con un unico avvocato dal primo colloquio alla conclusione.",
            body, aside_std(extra=strumenti_card(2 if "separazione" in c["temi"][0][0] else 0)),
            extra_ld=[faq_ld(c["faq"]), page_ld],
        )
    return out


def pagina_lomellina():
    L = C.LOMELLINA
    cards = "".join(
        f"<a class='card panel rv gcard' href='/{c['slug']}'><span class=\"label\">{esc(c['km'])} · {esc(c['min'])}</span><b>{esc(c['nome'])}</b><span class=\"note-s\">Tribunale, percorso, materie →</span></a>"
        for c in C.COMUNI
    )
    body = (
        '<article class="card panel article rv">'
        "<p>Lo Studio Legale Pernorio ha sede a Vigevano, in Via Egidio Sacchetti 14. Assiste clienti di tutta la Lomellina, da Mortara a Mede, da Garlasco a Robbio, e dell'Abbiatense, nelle questioni di diritto civile: famiglia, eredità, casa, debiti, contratti e lavoro.</p>"
        "<h2>Un solo tribunale per la Lomellina: Pavia</h2>"
        "<p>Dal 2013 il Tribunale di Vigevano è stato soppresso e il suo territorio accorpato al <strong>Tribunale di Pavia</strong>. Per chi vive a Vigevano, Mortara, Gambolò, Garlasco, Cassolnovo, Cilavegna, Robbio, Mede e negli altri comuni lomellini, le cause civili si svolgono quindi a Pavia. Lo Studio vi segue abitualmente le udienze, così il cliente si sposta solo quando la sua presenza è richiesta dal giudice.</p>"
        "<h2>Comuni in cui assistiamo clienti</h2>"
        "<p>Vigevano, Mortara, Gambolò, Garlasco, Cassolnovo, Cilavegna, Gravellona Lomellina, Parona, Robbio, Tromello, Dorno, Sannazzaro de' Burgondi, Mede, Sartirana Lomellina, e nell'Abbiatense Abbiategrasso, Ozzero, Morimondo e Cassinetta di Lugagnano.</p>"
        "<h2>Le materie</h2>"
        "<ul><li><a href='/diritto-di-famiglia'>Famiglia</a>: <a href='/attivita-separazione-divorzio'>separazione e divorzio</a>, <a href='/attivita-affidamento-minori'>affidamento dei figli</a>, <a href='/attivita-unioni-civili'>unioni civili e convivenze</a>.</li>"
        "<li>Eredità e persone fragili: <a href='/attivita-successioni'>successioni</a>, <a href='/attivita-amministrazione-di-sostegno'>amministrazione di sostegno</a>.</li>"
        "<li>Casa: <a href='/attivita-locazioni-comodato'>affitti e comodato</a>, <a href='/attivita-sfratti'>sfratti</a>, <a href='/attivita-usucapione-diritti-reali'>usucapione e diritti reali</a>, <a href='/attivita-condominio'>condominio</a>.</li>"
        "<li>Debiti e crediti: <a href='/attivita-saldo-e-stralcio'>saldo e stralcio</a>, <a href='/attivita-recupero-crediti'>recupero crediti</a>, <a href='/attivita-crisi-impresa'>sovraindebitamento</a>.</li>"
        "<li>Contratti, danni e lavoro: <a href='/attivita-contratti'>contratti</a>, <a href='/attivita-sinistri-responsabilita'>incidenti e risarcimenti</a>, <a href='/attivita-codice-della-strada'>multe</a>, <a href='/attivita-lavoro'>lavoro</a>.</li></ul>"
        "</article>"
        f'<div style="display:grid;gap:14px;margin-top:14px">{cards}</div>'
    )
    crumbs = [("Home", BASE + "/"), ("Dove operiamo", None)]
    return pagina(L["slug"], L["title"], L["description"], crumbs, "Dove operiamo", L["h1"], L["lead"], body, aside_std(extra=strumenti_card()))


def pagina_info(P, materia_aside=None):
    body = '<article class="card panel article rv">' + P["body"] + f'<p class="note-s">A cura dello Studio Legale Pernorio, Avv. Daniela Pernorio, Vigevano. Aggiornato a {C.AGGIORNATO}. Informazioni generali: non sostituiscono un parere sul caso concreto.</p></article>' + faq_html(P["faq"])
    crumbs = [("Home", BASE + "/"), (P["label"], None)]
    art = {
        "@context": "https://schema.org", "@type": "Article", "headline": P["h1"], "description": P["description"],
        "author": {"@id": BASE + "/#avvocato"}, "publisher": {"@id": BASE + "/#studio"},
        "datePublished": OGGI, "dateModified": OGGI, "inLanguage": "it-IT",
        "mainEntityOfPage": clean_url(P["slug"]), "image": BASE + "/img/og.jpg",
    }
    return pagina(P["slug"], P["title"], P["description"], crumbs, P["label"], P["h1"], P["lead"], body,
                  aside_std(materia_aside, extra=strumenti_card()), extra_ld=[faq_ld(P["faq"]), art])


# --- Strumenti ---------------------------------------------------------------

JS_EREDITA = r"""
<script>
(function(){
function g(a,b){while(b){var t=b;b=a%b;a=t}return a}
function F(n,d){var k=g(n,d)||1;return{n:n/k,d:d/k}}
function mul(a,b){return F(a.n*b.n,a.d*b.d)}function sub(a,b){return F(a.n*b.d-b.n*a.d,a.d*b.d)}
function div(a,k){return F(a.n,a.d*k)}function ge(a,b){return a.n*b.d>=b.n*a.d}
function quote(c,f,p,s){var r=[],rest,pt,gt;
 if(f>0){ if(c){ if(f===1){r.push(['Coniuge',F(1,2),1]);r.push(['Figlio',F(1,2),1]);} else {r.push(['Coniuge',F(1,3),1]);r.push(['Ciascun figlio',div(F(2,3),f),f]);} }
   else r.push([f===1?'Figlio':'Ciascun figlio',F(1,f),f]); return r;}
 if(c){ if(p+s===0){r.push(['Coniuge',F(1,1),1]);return r;}
   r.push(['Coniuge',F(2,3),1]); rest=F(1,3);
   if(s===0) r.push([p===1?'Genitore':'Ciascun genitore',div(rest,p),p]);
   else if(p===0) r.push([s===1?'Fratello o sorella':'Ciascun fratello o sorella',div(rest,s),s]);
   else { pt=mul(div(rest,p+s),F(p,1)); gt=ge(pt,F(1,4))?pt:F(1,4);
     r.push([p===1?'Genitore':'Ciascun genitore',div(gt,p),p]); r.push([s===1?'Fratello o sorella':'Ciascun fratello o sorella',div(sub(rest,gt),s),s]); }
   return r;}
 if(p+s===0) return r;
 if(s===0){r.push([p===1?'Genitore':'Ciascun genitore',F(1,p),p]);return r;}
 if(p===0){r.push([s===1?'Fratello o sorella':'Ciascun fratello o sorella',F(1,s),s]);return r;}
 pt=F(p,p+s); gt=ge(pt,F(1,2))?pt:F(1,2);
 r.push([p===1?'Genitore':'Ciascun genitore',div(gt,p),p]); r.push([s===1?'Fratello o sorella':'Ciascun fratello o sorella',div(sub(F(1,1),gt),s),s]); return r;}
window.__quote=quote;
var f=document.getElementById('qe');if(!f)return;
function eur(x){return x.toLocaleString('it-IT',{style:'currency',currency:'EUR',maximumFractionDigits:0})}
function run(){var c=f.coniuge.checked,fi=+f.figli.value||0,p=+f.genitori.value||0,s=+f.fratelli.value||0,v=parseFloat((f.valore.value||'').replace(/\./g,'').replace(',','.'))||0;
 var r=quote(c,fi,p,s),o=document.getElementById('qe-out');
 if(!r.length){o.innerHTML='<p>Senza coniuge, figli, genitori o fratelli l\'eredità va agli altri parenti fino al sesto grado e, in mancanza, allo Stato (artt. 572 e 586 c.c.). È un caso da valutare con un avvocato.</p>';return}
 var h='<table class="qt"><thead><tr><th>Erede</th><th>Quota</th><th>%</th>'+(v?'<th>Valore</th>':'')+'</tr></thead><tbody>';
 r.forEach(function(x){var q=x[1],pc=q.n/q.d;h+='<tr><td>'+x[0]+(x[2]>1?' ('+x[2]+')':'')+'</td><td>'+q.n+'/'+q.d+'</td><td>'+(pc*100).toLocaleString('it-IT',{maximumFractionDigits:2})+'%</td>'+(v?'<td>'+eur(v*pc)+'</td>':'')+'</tr>'});
 o.innerHTML=h+'</tbody></table>'}
f.addEventListener('input',run);f.addEventListener('change',run);run();
})();
</script>"""

JS_MULTA = r"""
<script>
(function(){
var f=document.getElementById('sm');if(!f)return;
function add(d,n){var x=new Date(d.getTime());x.setDate(x.getDate()+n);return x}
function fmt(d){return d.toLocaleDateString('it-IT',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}
function run(){var o=document.getElementById('sm-out'),v=f.data.value;if(!v){o.innerHTML='';return}
 var p=v.split('-'),d=new Date(+p[0],+p[1]-1,+p[2]),oggi=new Date();oggi.setHours(0,0,0,0);
 var rows=[['Pagamento con lo sconto del 30%',5,'Solo se il verbale lo prevede (non per le violazioni con confisca o sospensione della patente). Pagare significa rinunciare al ricorso.'],
 ['Ricorso al Giudice di Pace',30,'Si deposita presso il Giudice di Pace del luogo della violazione. Serve il contributo unificato.'],
 ['Pagamento in misura ridotta (minimo edittale)',60,'Dopo questa data l\'importo può salire fino alla metà del massimo previsto.'],
 ['Ricorso al Prefetto',60,'Gratuito. Se respinto, la sanzione può essere raddoppiata: valutare bene la scelta.']];
 var h='<table class="qt"><thead><tr><th>Cosa</th><th>Entro</th><th></th></tr></thead><tbody>';
 rows.forEach(function(r){var s=add(d,r[1]),late=s<oggi;h+='<tr'+(late?' class="late"':'')+'><td><b>'+r[0]+'</b><br><small>'+r[2]+'</small></td><td>'+fmt(s)+'</td><td>'+(late?'Scaduto':Math.round((s-oggi)/864e5)+' giorni')+'</td></tr>'});
 o.innerHTML=h+'</tbody></table>'}
f.addEventListener('input',run);run();
})();
</script>"""

JS_CHECK = r"""
<script>
(function(){
var K='slp-checklist-sep',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
var boxes=document.querySelectorAll('#ck input[type=checkbox]'),cnt=document.getElementById('ck-n');
function upd(){var n=0;boxes.forEach(function(b){if(b.checked)n++});if(cnt)cnt.textContent=n+' su '+boxes.length}
boxes.forEach(function(b){b.checked=!!st[b.id];b.addEventListener('change',function(){st[b.id]=b.checked;try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}upd()})});upd();
var p=document.getElementById('ck-print');if(p)p.addEventListener('click',function(){window.print()});
var r=document.getElementById('ck-reset');if(r)r.addEventListener('click',function(){st={};try{localStorage.removeItem(K)}catch(e){}boxes.forEach(function(b){b.checked=false});upd()});
})();
</script>"""


JS_IMPOSTA = """
<script>
(function(){
""" + AG.CALC_IMPOSTA_JS + r"""
var f=document.getElementById('is');if(!f)return;
function num(v){return parseFloat(String(v||'').replace(/\./g,'').replace(',','.'))||0}
function eur(x){return x.toLocaleString('it-IT',{style:'currency',currency:'EUR',maximumFractionDigits:0})}
function run(){var r=impostaSuccessione({quota:num(f.quota.value),rapporto:f.rapporto.value,disabile:f.disabile.checked,immobili:num(f.immobili.value),primaCasa:f.primaCasa.checked});
 var h='<table class="qt"><tbody><tr><td>Franchigia</td><td>'+eur(r.franchigia_euro)+'</td></tr><tr><td>Base imponibile</td><td>'+eur(r.base_imponibile_euro)+'</td></tr><tr><td>Aliquota</td><td>'+r.aliquota_percento+'%</td></tr><tr><td><b>Imposta di successione</b></td><td><b>'+eur(r.imposta_successione_euro)+'</b></td></tr>';
 if(r.imposte_ipotecaria_catastale){h+='<tr><td>Imposta ipotecaria (per l\'intera eredità)</td><td>'+eur(r.imposte_ipotecaria_catastale.ipotecaria_euro)+'</td></tr><tr><td>Imposta catastale (per l\'intera eredità)</td><td>'+eur(r.imposte_ipotecaria_catastale.catastale_euro)+'</td></tr>'}
 document.getElementById('is-out').innerHTML=h+'</tbody></table>'}
f.addEventListener('input',run);f.addEventListener('change',run);run();
})();
</script>"""


def pagine_strumenti():
    out = {}
    T = C.STRUMENTI
    crumbs_base = [("Home", BASE + "/"), ("Strumenti", clean_url("strumenti"))]

    # 1. Quote eredita
    t = T[0]
    body = (
        '<div class="card panel rv tool"><form id="qe" onsubmit="return false">'
        '<label class="tchk"><input type="checkbox" name="coniuge" checked> Il coniuge (o unito civilmente) è in vita</label>'
        '<div class="tgrid"><label>Figli<input type="number" name="figli" min="0" max="20" value="2" inputmode="numeric"></label>'
        '<label>Genitori in vita<select name="genitori"><option>0</option><option>1</option><option>2</option></select></label>'
        '<label>Fratelli e sorelle<input type="number" name="fratelli" min="0" max="20" value="0" inputmode="numeric"></label>'
        '<label>Valore dell\'eredità in € (facoltativo)<input type="text" name="valore" inputmode="decimal" placeholder="es. 200.000"></label></div>'
        '</form><div id="qe-out" aria-live="polite"></div></div>'
        '<article class="card panel article rv">'
        "<h2>Come funziona la successione senza testamento</h2>"
        "<p>Quando una persona muore senza testamento, la legge stabilisce chi eredita e in che misura (successione legittima, artt. 565 e seguenti del codice civile):</p>"
        "<ul><li><strong>Coniuge e un figlio</strong>: metà ciascuno.</li>"
        "<li><strong>Coniuge e due o più figli</strong>: un terzo al coniuge, due terzi divisi in parti uguali tra i figli.</li>"
        "<li><strong>Solo figli</strong>: tutto ai figli, in parti uguali.</li>"
        "<li><strong>Coniuge senza figli, con genitori e/o fratelli</strong>: due terzi al coniuge; il terzo restante a genitori e fratelli, con ai genitori almeno un quarto dell'intera eredità.</li>"
        "<li><strong>Solo genitori e fratelli</strong>: in parti uguali, ma ai genitori spetta almeno la metà.</li>"
        "<li><strong>Solo il coniuge</strong>: tutta l'eredità.</li></ul>"
        "<h2>Limiti del calcolo</h2>"
        "<p>Lo strumento non considera: figli premorti con discendenti (rappresentazione), fratelli unilaterali (ricevono metà della quota dei germani), ascendenti oltre i genitori, donazioni fatte in vita da imputare alla quota, debiti ereditari, separazione con addebito. Se c'è un <strong>testamento</strong> valgono altre regole: ai figli, al coniuge e in certi casi ai genitori spetta comunque una <strong>quota di legittima</strong> che il testamento non può ledere.</p>"
        "<p>Per una verifica sul caso concreto, o per la <a href='/guida-successioni-autoliquidazione-imposta'>dichiarazione di successione e l'imposta</a>, lo Studio è a disposizione.</p>"
        f'<p class="note-s">Strumento a scopo informativo, aggiornato a {C.AGGIORNATO}. Non sostituisce un parere legale.</p></article>'
    )
    out[t["slug"]] = pagina(t["slug"], t["title"], t["description"], crumbs_base + [(t["titolo_breve"], None)],
                            "Strumento gratuito · Successioni", "Calcolo delle quote di eredità senza testamento", t["lead"],
                            body, aside_std(t["materia"]), extra_ld=[tool_ld(t)], script=JS_EREDITA)

    # 2. Scadenze multa
    t = T[1]
    body = (
        '<div class="card panel rv tool"><form id="sm" onsubmit="return false">'
        '<label>Data di notifica o di contestazione del verbale<input type="date" name="data" required></label>'
        '</form><div id="sm-out" aria-live="polite"></div></div>'
        '<article class="card panel article rv">'
        "<h2>Le scadenze da ricordare</h2>"
        "<ul><li><strong>5 giorni</strong>: pagamento scontato del 30% sulla sanzione minima, quando previsto.</li>"
        "<li><strong>30 giorni</strong>: ricorso al Giudice di Pace del luogo in cui è stata commessa la violazione.</li>"
        "<li><strong>60 giorni</strong>: pagamento in misura ridotta oppure ricorso al Prefetto.</li></ul>"
        "<p>I termini decorrono dalla contestazione immediata o dalla notifica del verbale. Per la notifica a mezzo posta conta il giorno del ritiro o, in caso di compiuta giacenza, la data in cui la notifica si considera perfezionata. Se l'ultimo giorno è festivo, per il ricorso al Giudice di Pace la scadenza slitta al primo giorno non festivo.</p>"
        "<h2>Prefetto o Giudice di Pace?</h2>"
        "<p>Il ricorso al Prefetto è gratuito, ma se viene respinto la sanzione può arrivare al doppio del minimo. Quello al Giudice di Pace richiede il contributo unificato e consente una vera difesa in udienza. Le due strade sono alternative. Per gli autovelox, leggi la <a href='/guida-multa-autovelox-2026'>guida sulle multe da autovelox</a>.</p>"
        f'<p class="note-s">Strumento a scopo informativo, aggiornato a {C.AGGIORNATO}. Verificare sempre le indicazioni riportate sul verbale.</p></article>'
    )
    out[t["slug"]] = pagina(t["slug"], t["title"], t["description"], crumbs_base + [(t["titolo_breve"], None)],
                            "Strumento gratuito · Codice della strada", "Multa: entro quando pagare o fare ricorso", t["lead"],
                            body, aside_std(t["materia"]), extra_ld=[tool_ld(t)], script=JS_MULTA)

    # 3. Checklist separazione
    t = T[2]
    groups = ""
    k = 0
    for titolo, voci in C.CHECKLIST:
        items = ""
        for v in voci:
            k += 1
            items += f'<li><label><input type="checkbox" id="ck{k}"> <span>{esc(v)}</span></label></li>'
        groups += f"<h2>{esc(titolo)}</h2><ul class=\"cklist\">{items}</ul>"
    body = (
        f'<div class="card panel rv tool" id="ck"><p><b>Documenti raccolti: <span id="ck-n"></span></b></p>{groups}'
        '<div class="actions" style="margin-top:18px"><button class="btn btn-primary" type="button" id="ck-print">Stampa o salva PDF</button>'
        '<button class="btn btn-ghost" type="button" id="ck-reset">Azzera</button></div></div>'
        '<article class="card panel article rv"><h2>Perché preparare i documenti prima</h2>'
        "<p>Arrivare al primo colloquio con i documenti giusti permette all'avvocato di dare subito indicazioni concrete su mantenimento, casa familiare e tempi, e di stimare i costi con precisione. Non serve avere tutto: si parte da quello che c'è.</p>"
        "<p>Per capire le differenze tra separazione consensuale, giudiziale e con negoziazione assistita, e la possibilità di chiedere insieme separazione e divorzio, legga la <a href='/guida-separazione-divorzio-unica-domanda'>guida pratica</a>.</p>"
        f'<p class="note-s">Lo stato delle caselle resta salvato solo su questo dispositivo. Aggiornato a {C.AGGIORNATO}.</p></article>'
    )
    out[t["slug"]] = pagina(t["slug"], t["title"], t["description"], crumbs_base + [(t["titolo_breve"], None)],
                            "Strumento gratuito · Famiglia", "Checklist dei documenti per la separazione", t["lead"],
                            body, aside_std(t["materia"]), extra_ld=[tool_ld(t)], script=JS_CHECK)

    # 4. Imposta di successione
    t = T[3]
    body = (
        '<div class="card panel rv tool"><form id="is" onsubmit="return false">'
        '<div class="tgrid"><label>Valore della quota ricevuta (€)<input type="text" name="quota" inputmode="decimal" value="1.200.000"></label>'
        '<label>Chi riceve<select name="rapporto"><option value="coniuge">Coniuge, unito civilmente, figlio, genitore o altro parente in linea retta</option>'
        '<option value="fratello">Fratello o sorella</option><option value="parente">Altro parente fino al 4° grado o affine</option><option value="altri">Altra persona</option></select></label>'
        '<label>Valore catastale degli immobili dell\'eredità (€, facoltativo)<input type="text" name="immobili" inputmode="decimal" placeholder="es. 150.000"></label></div>'
        '<label class="tchk"><input type="checkbox" name="disabile"> L\'erede ha una disabilità grave (legge 104/1992)</label>'
        '<label class="tchk"><input type="checkbox" name="primaCasa"> Si chiede l\'agevolazione prima casa</label>'
        '</form><div id="is-out" aria-live="polite"></div></div>'
        '<article class="card panel article rv">'
        "<h2>Franchigie e aliquote</h2>"
        "<p>L'imposta si calcola <strong>per ciascun erede</strong>, sul valore della quota ricevuta che supera la franchigia (art. 7 del D.Lgs. 346/1990):</p>"
        "<ul><li><strong>Coniuge, unito civilmente e parenti in linea retta</strong> (figli, genitori, nipoti in linea retta): 4% oltre 1.000.000 € a testa.</li>"
        "<li><strong>Fratelli e sorelle</strong>: 6% oltre 100.000 € a testa.</li>"
        "<li><strong>Altri parenti fino al quarto grado e affini</strong>: 6% senza franchigia.</li>"
        "<li><strong>Tutti gli altri</strong>: 8% senza franchigia.</li>"
        "<li><strong>Erede con disabilità grave</strong>: franchigia di 1.500.000 €.</li></ul>"
        "<h2>Le imposte sugli immobili</h2>"
        "<p>Se nell'eredità ci sono immobili si pagano anche l'<strong>imposta ipotecaria</strong> (2%) e quella <strong>catastale</strong> (1%) sul valore catastale, con un minimo di 200 € ciascuna, una sola volta per immobile. Con l'agevolazione <strong>prima casa</strong>, se almeno un erede ne ha i requisiti, sono fisse: 200 € ciascuna. Per questo, anche quando l'imposta di successione è zero, con una casa nell'eredità qualcosa si paga quasi sempre.</p>"
        "<h2>Cosa il calcolo non considera</h2>"
        "<p>Debiti e spese deducibili, donazioni fatte in vita (che si sommano alla quota ai fini della franchigia), beni esenti come i titoli di Stato, imposta di bollo, tributi speciali e tassa ipotecaria. Dal 2025 l'imposta si autoliquida: lo spiega la <a href='/guida-successioni-autoliquidazione-imposta'>guida sulla dichiarazione di successione</a>. Per sapere chi eredita, c'è il <a href='/strumento-calcolo-quote-eredita'>calcolo delle quote</a>.</p>"
        f'<p class="note-s">Strumento a scopo informativo, aggiornato a {C.AGGIORNATO}. Fonte: <a href="https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1990-10-31;346" target="_blank" rel="noopener">D.Lgs. 346/1990 su Normattiva</a>.</p></article>'
    )
    out[t["slug"]] = pagina(t["slug"], t["title"], t["description"], crumbs_base + [(t["titolo_breve"], None)],
                            "Strumento gratuito · Successioni", "Calcolo dell'imposta di successione", t["lead"],
                            body, aside_std(t["materia"]), extra_ld=[tool_ld(t)], script=JS_IMPOSTA)

    # Indice strumenti
    cards = strumenti_card()
    body = ('<article class="card panel article rv"><p>Strumenti gratuiti preparati dallo Studio per orientarsi prima di parlare con un avvocato. Funzionano direttamente nel browser: i dati inseriti non vengono inviati né salvati dallo Studio.</p></article>'
            f'<div style="display:grid;gap:14px;margin-top:14px">{cards}</div>')
    out["strumenti"] = pagina("strumenti", "Strumenti legali gratuiti · Studio Legale Pernorio, Vigevano",
                              "Calcolo delle quote di eredità e dell'imposta di successione, scadenze di una multa, checklist per la separazione. Strumenti gratuiti dello Studio Legale Pernorio.",
                              [("Home", BASE + "/"), ("Strumenti", None)], "Strumenti gratuiti", "Strumenti legali gratuiti",
                              "Calcoli e checklist per orientarsi su eredità, imposte di successione, multe e separazione.", body, aside_std())
    return out


def tool_ld(t):
    return {
        "@context": "https://schema.org", "@type": "WebApplication", "name": t["titolo_breve"],
        "url": clean_url(t["slug"]), "description": t["description"], "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Web", "inLanguage": "it-IT", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "provider": {"@id": BASE + "/#studio"},
    }


def pagine_guide():
    out = {}
    for i, g in enumerate(G.GUIDE):
        url = clean_url(g["slug"])
        corpo = g["corpo"] + f'<p class="note-s">A cura dello Studio Legale Pernorio, <a href=\'/studio\'>Avv. Daniela Pernorio</a>, Vigevano. Aggiornato a {C.AGGIORNATO}. Informazioni generali: non sostituiscono un parere sul caso concreto.</p>'
        body = '<article class="card panel article rv">' + corpo + "</article>" + faq_html(g["faq"])
        altre = [x for x in G.GUIDE if x["slug"] != g["slug"] and x["cat"] == g["cat"]]
        altre += [x for x in G.GUIDE if x["slug"] != g["slug"] and x not in altre]
        chips = "".join(f"<a class='chip' href='/{x['slug']}'>{esc(x['titolo'])}</a>" for x in altre[:5])
        extra = ""
        tool = {"guida-costo-separazione-consensuale": 2, "guida-casa-familiare-separazione": 2, "guida-divorzio-tempi": 2,
                "guida-eredita-con-debiti": 0, "guida-testamento-olografo": 0}.get(g["slug"])
        if tool is not None:
            extra += strumenti_card(tool)
        extra += f'<div class="card panel rv"><span class="label">Altre guide</span><div class="chips" style="margin-top:14px">{chips}</div></div>'
        art = {
            "@context": "https://schema.org", "@type": "Article", "headline": g["titolo"], "description": g["sommario"],
            "inLanguage": "it-IT", "datePublished": OGGI, "dateModified": OGGI, "mainEntityOfPage": url,
            "image": BASE + "/img/og.jpg", "author": {"@id": BASE + "/#avvocato"}, "publisher": {"@id": BASE + "/#studio"},
            "articleSection": g["cat"],
        }
        crumbs = [("Home", BASE + "/"), ("Guide", clean_url("guide")), (g["cat"], None)]
        title = g["titolo"] + " · Avv. Daniela Pernorio, Vigevano"
        if len(title) > 70:
            title = g["titolo"] + " · Studio Pernorio"
        out[g["slug"]] = pagina(g["slug"], title, g["sommario"], crumbs, f"Guida · {g['cat']} · {g['min']} min di lettura",
                                g["titolo"], g["sommario"], body, aside_std(g["materia"], extra=extra), extra_ld=[faq_ld(g["faq"]), art])
    return out


def pagina_colloquio():
    body = CO.COME + CO.form_html(esc)
    aside = CO.TEST_AV + f'<div class="card panel rv"><span class="label">Preferisci parlarne subito?</span><div class="actions" style="margin-top:14px">{BTN_CALL}{BTN_WA}</div></div>' + zone_card()
    svc = {
        "@context": "https://schema.org", "@type": "Service", "name": "Colloquio legale online",
        "serviceType": "Consulenza legale a distanza in videochiamata", "provider": {"@id": BASE + "/#studio"},
        "areaServed": {"@type": "Country", "name": "Italia"}, "url": clean_url(CO.SLUG),
        "availableChannel": {"@type": "ServiceChannel", "serviceUrl": clean_url(CO.SLUG), "name": "Videochiamata, WhatsApp video, telefono"},
    }
    faq = [
        ("Serve installare un programma per la videochiamata?", "No. Il link personale si apre nel browser, da computer o telefono. In alternativa si può usare WhatsApp video o il telefono."),
        ("Come invio i documenti?", "Con il modulo di richiesta, fino a 8 MB in totale, e successivamente via email o PEC. L'avvocato li studia prima del colloquio."),
        ("Il colloquio online costa come quello in Studio?", "Sì, le condizioni sono le stesse e vengono comunicate al momento della conferma. Prima di iniziare qualsiasi attività si riceve un preventivo scritto."),
        ("Posso farmi assistere a distanza per tutta la pratica?", "In molti casi sì: documenti, firme, aggiornamenti e incontri si possono gestire online. Alcuni passaggi, come certe udienze, richiedono la presenza personale."),
    ]
    return pagina(CO.SLUG, CO.TITLE, CO.DESCRIPTION, [("Home", BASE + "/"), ("Contatti", clean_url("contatti")), ("Colloquio online", None)],
                  CO.LABEL, CO.H1, CO.LEAD, body + faq_html(faq), aside, extra_ld=[svc, faq_ld(faq)], script=CO.JS)


def pagina_glossario(esistenti):
    for g in TR.GLOSSARIO:
        assert g[4][0] in esistenti, f"Glossario: pagina inesistente {g[4][0]}"
    assert len({g[0] for g in TR.GLOSSARIO}) == len(TR.GLOSSARIO), "Glossario: id doppi"
    crumbs = [("Home", BASE + "/"), ("Guide", clean_url("guide")), ("Glossario", None)]
    return pagina(TR.GLOSSARIO_SLUG, TR.GLOSSARIO_TITLE, TR.GLOSSARIO_DESC, crumbs, "Glossario", "Glossario legale",
                  "Le parole che si incontrano in un atto, in una lettera o in udienza, spiegate in poche righe e con la fonte di legge.",
                  TR.glossario_body(C.AGGIORNATO), aside_std(extra=strumenti_card()), extra_ld=[TR.glossario_ld()])


def pagina_cerca():
    crumbs = [("Home", BASE + "/"), ("Cerca", None)]
    s = pagina(TR.CERCA_SLUG, "Cerca nel sito · Studio Legale Pernorio", "Cerca tra le guide, le competenze, il glossario e gli strumenti dello Studio Legale Pernorio di Vigevano.",
               crumbs, "Ricerca", "Cerca nel sito", "Guide, competenze, glossario e strumenti: scriva la parola che le interessa.",
               TR.cerca_body(), aside_std(), script='<script src="/cerca.js" defer></script>')
    s = s.replace(f"<div class=actions>{BTN_CALL}{BTN_WA}</div></div></section>", "</div></section>", 1)
    return s.replace(CTA_SECTION, "", 1)


def card_online():
    return ("<a class='card panel rv gcard' href='/colloquio-online'><span class=\"label\">Novità · Da casa</span>"
            "<b>Colloquio online con l'avvocato</b><span class=\"note-s\">Videochiamata, documenti inviati prima, riepilogo scritto →</span></a>")


def fix_indice_guide(s):
    cards = "".join(
        f"<a class='card glink' href='/{g['slug']}'><span class=\"label\">{esc(g['cat'])}</span><b>{esc(g['titolo'])}</b><span>{esc(g['sommario'])}</span></a>"
        for g in G.GUIDE
    )
    gloss = ("<a class='card glink' href='/glossario-legale'><span class=\"label\">Glossario</span><b>Le parole del diritto, in breve</b>"
             f"<span>{len(TR.GLOSSARIO)} termini spiegati in poche righe, dall'addebito all'usucapione, con la fonte di legge.</span></a>")
    s = s.replace('<div class="glist rv">', '<div class="glist rv">' + cards + gloss, 1)
    s = s.replace("</p></div></section>", "</p>" + TR.modulo_cerca() + "</div></section>", 1)
    s = s.replace("Informazioni generali, aggiornate a ottobre 2026.", f"Informazioni generali, aggiornate a {C.AGGIORNATO}.")
    return s


def fix_studio(s):
    s = s.replace("L'Avv. Daniela Pernorio è avvocato civilista, iscritta all'Ordine degli Avvocati di Pavia.",
                  "L'Avv. Daniela Pernorio è avvocato civilista, iscritta all'Ordine degli Avvocati di Pavia dal gennaio 2014.", 1)
    return s


def fix_orari_social(s):
    s = s.replace("Lun – Ven, su appuntamento", ORARI_TXT)
    s = s.replace("Via Egidio Sacchetti 14, Vigevano · Su appuntamento", "Via Egidio Sacchetti 14, Vigevano · Lun – Ven 9 – 19, su appuntamento")
    s = s.replace("Lo Studio riceve su appuntamento, dal lunedì al venerdì.", "Lo Studio riceve su appuntamento, dal lunedì al venerdì dalle 9:00 alle 19:00.")
    s = s.replace("Primo colloquio in Studio, dal lunedì al venerdì.", "Primo colloquio in Studio, dal lunedì al venerdì dalle 9 alle 19.")
    s = s.replace("<p style=\"margin-top:22px\">Avv. Daniela Pernorio<br>Ordine degli Avvocati di Pavia</p>",
                  "<p style=\"margin-top:22px\">Avv. Daniela Pernorio<br>Ordine degli Avvocati di Pavia dal 2014</p>")
    ig = f'<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram · @studio_legale_pernorio</a></li>'
    if INSTAGRAM not in s:
        s = s.replace('<li style="overflow-wrap:anywhere"><a href="mailto:daniela.pernorio@gmail.com">daniela.pernorio@gmail.com</a></li></ul>',
                      '<li style="overflow-wrap:anywhere"><a href="mailto:daniela.pernorio@gmail.com">daniela.pernorio@gmail.com</a></li>' + ig + "</ul>", 1)
    return s


# ---------------------------------------------------------------------------
# Correzioni applicate a tutte le pagine
# ---------------------------------------------------------------------------

def fix_urls(s):
    s = re.sub(r"https://www\.studiolegalepernorio\.com/([\w-]*)\.html", lambda m: clean_url(m.group(1)), s)
    s = s.replace("https://www.studiolegalepernorio.com", BASE)
    return s


def fix_ld(s):
    def repl(m):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        items = data if isinstance(data, list) else [data]
        for it in items:
            t = it.get("@type")
            if t == "LegalService":
                it["@id"] = BASE + "/#studio"
                it["url"] = BASE + "/"
                it.setdefault("logo", BASE + "/img/icon-512.png")
                it["image"] = [BASE + "/img/og.jpg", BASE + "/img/ingresso.webp", BASE + "/img/studio-vetrata.webp"]
                it["openingHoursSpecification"] = [{
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "opens": "09:00", "closes": "19:00",
                }]
                it["sameAs"] = list(dict.fromkeys((it.get("sameAs") or []) + [INSTAGRAM]))
                it.setdefault("hasOfferCatalog", {
                    "@type": "OfferCatalog", "name": "Aree di attività",
                    "itemListElement": [
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": clean_url("attivita-" + k)}}
                        for k, n in [(k, v[0].upper() + v[1:]) for k, v in MATERIE_KW.items()]
                    ],
                })
                f = it.get("founder")
                if isinstance(f, dict):
                    f["@id"] = BASE + "/#avvocato"
                    f.setdefault("url", clean_url("studio"))
                    f.setdefault("image", BASE + "/img/ritratto-viso.webp")
                    f.setdefault("worksFor", {"@id": BASE + "/#studio"})
                    f["hasCredential"] = {"@type": "EducationalOccupationalCredential", "credentialCategory": "Iscrizione all'Albo degli Avvocati",
                                          "recognizedBy": {"@type": "Organization", "name": "Ordine degli Avvocati di Pavia"}, "dateCreated": "2014-01"}
            elif t == "ProfilePage" and isinstance(it.get("mainEntity"), dict):
                pe = it["mainEntity"]
                pe["@id"] = BASE + "/#avvocato"
                pe["sameAs"] = [INSTAGRAM]
                pe["hasCredential"] = {"@type": "EducationalOccupationalCredential", "credentialCategory": "Iscrizione all'Albo degli Avvocati",
                                       "recognizedBy": {"@type": "Organization", "name": "Ordine degli Avvocati di Pavia"}, "dateCreated": "2014-01"}
                pe["worksFor"] = {"@id": BASE + "/#studio"}
            elif t == "WebSite":
                it["@id"] = BASE + "/#sito"
                it["publisher"] = {"@id": BASE + "/#studio"}
                it["potentialAction"] = TR.search_action()
            elif t == "Article":
                it["author"] = {"@type": "Person", "@id": BASE + "/#avvocato", "name": "Avv. Daniela Pernorio", "url": clean_url("studio")}
                it["publisher"] = {"@id": BASE + "/#studio"}
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, s, flags=re.S)


def fix_head(s, slug, noindex=False):
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">', "", s)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>', "", s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">', FONT_PRELOAD, s)
    s = s.replace('href="style.css"', 'href="/style.css"').replace('href="favicon.svg"', 'href="/favicon.svg"')
    s = s.replace('href="img/apple-touch-icon.png"', 'href="/img/apple-touch-icon.png"').replace('href="site.webmanifest"', 'href="/site.webmanifest"')
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    url = clean_url(slug)
    extra = ""
    if 'property="og:url"' not in s:
        extra += f'<meta property="og:url" content="{url}">'
    if 'property="og:type"' not in s:
        extra += f'<meta property="og:type" content="{"article" if slug.startswith("guida-") else "website"}">'
    if 'property="og:site_name"' not in s:
        extra += '<meta property="og:site_name" content="Studio Legale Pernorio">'
    if 'name="twitter:card"' not in s:
        extra += '<meta name="twitter:card" content="summary_large_image">'
    if noindex and 'name="robots"' not in s:
        extra += '<meta name="robots" content="noindex, follow">'
    elif not noindex and 'name="robots"' not in s:
        extra += TR.ROBOTS_META
    extra += TR.HEAD_LINKS
    s = s.replace("<link rel=\"icon\"", extra + "\n<link rel=\"icon\"", 1)
    del title
    return s


def fix_nav(s):
    # Aggiunge "Guide" al menu principale e a quello mobile
    if "href='/guide'>Guide</a><a href='/contatti'>" not in s:
        s = s.replace("<a href='/contatti'>Contatti</a></nav>", "<a href='/guide'>Guide</a><a href='/contatti'>Contatti</a></nav>", 1)
        s = s.replace("<a aria-current='page' href='/contatti'>Contatti</a></nav>", "<a href='/guide'>Guide</a><a aria-current='page' href='/contatti'>Contatti</a></nav>", 1)
        arr = re.search(r'<span class="arr">.*?</span>', s, re.S)
        if arr:
            s = re.sub(r"(<nav aria-label=\"Menu\">.*?)(<a (?:aria-current='page' )?href='/contatti'>Contatti)",
                       lambda m: m.group(1) + f"<a href='/guide'>Guide{arr.group(0)}</a>" + m.group(2), s, count=1, flags=re.S)
    return s


def fix_footer(s):
    extra = "<li><a href='/strumenti'>Strumenti gratuiti</a></li><li><a href='/costi-avvocato'>Costi e preventivo</a></li><li><a href='/colloquio-online'>Colloquio online</a></li><li><a href='/glossario-legale'>Glossario legale</a></li><li><a href='/cerca'>Cerca nel sito</a></li>"
    s = s.replace("<li><a href='/domande'>Domande frequenti</a></li>", "<li><a href='/domande'>Domande frequenti</a></li>" + extra, 1)
    zone = " · ".join(f"<a href='/{c['slug']}'>{esc(c['nome'])}</a>" for c in C.COMUNI)
    blocco = f'<div class="fzones"><span>Dove operiamo:</span> <a href=\'/\'>Vigevano</a> · {zone} · <a href=\'/{C.LOMELLINA["slug"]}\'>Lomellina</a></div>\n'
    s = s.replace('<div class="legal">', blocco + '<div class="legal">', 1)
    return s


def fix_pratica(s, key):
    kw = MATERIE_KW[key]
    h1_orig = re.search(r"<h1>(.*?)</h1>", s).group(1)
    titolo = f"Avvocato per {kw} a Vigevano · Avv. Daniela Pernorio"
    if len(titolo) > 66:
        titolo = f"Avvocato per {kw} a Vigevano · Studio Pernorio"
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(titolo)}</title>", s)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(titolo)}">', s)
    desc_orig = html.unescape(re.search(r'<meta name="description" content="([^"]*)">', s).group(1))
    desc_orig = desc_orig.split(" Studio Legale Pernorio")[0].strip()
    desc = trim(f"Avvocato a Vigevano per {kw}. {desc_orig} Avv. Daniela Pernorio, Tribunale di Pavia: primo colloquio su appuntamento, preventivo scritto.")
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">', s)
    s = s.replace(f"<h1>{h1_orig}</h1>", f"<h1>{h1_orig}<span class=\"h1s\">Avvocato a Vigevano e in Lomellina</span></h1>", 1)

    chips = "".join(f"<a class='chip' href='/{c['slug']}'>{esc(c['nome'])}</a>" for c in C.COMUNI)
    pannello = (
        '<div class="card panel rv"><h2>Come lavora lo Studio</h2>'
        '<ul class="ticks"><li><span><b>Primo colloquio</b> in Studio a Vigevano, con i documenti: le strade possibili, i tempi, i rischi.</span></li>'
        '<li><span><b>Preventivo scritto</b> prima di iniziare. <a href="/costi-avvocato">Come si forma il costo</a>.</span></li>'
        '<li><span><b>Anche a distanza</b>: <a href="/colloquio-online">colloquio online</a> in videochiamata, con i documenti inviati prima.</span></li>'
        "<li><span><b>Un solo avvocato</b> segue la pratica dall'inizio alla fine, con aggiornamenti scritti a ogni passaggio.</span></li>"
        '<li><span><b>Accordo prima della causa</b>, quando è possibile: <a href="/attivita-negoziazione-assistita">negoziazione assistita</a> e <a href="/attivita-mediazione-civile">mediazione</a>.</span></li></ul>'
        f'<h3 style="margin-top:22px">Per chi vive in Lomellina e nell\'Abbiatense</h3><div class="chips" style="margin-top:12px">{chips}</div></div>\n'
    )
    if key == "separazione-divorzio":
        pannello = (
            '<div class="card panel article rv">'
            "<h2>Separazione consensuale o giudiziale?</h2>"
            "<p>La <strong>separazione consensuale</strong> presuppone un accordo tra i coniugi su figli, mantenimento e casa. Si può ottenere in tre modi: con ricorso congiunto al Tribunale di Pavia, con la <a href='/attivita-negoziazione-assistita'>negoziazione assistita</a> (un avvocato per ciascun coniuge, senza udienze) oppure, se non ci sono figli minori, non autosufficienti o con disabilità grave e non ci sono trasferimenti di beni, davanti all'ufficiale di stato civile del Comune.</p>"
            "<p>La <strong>separazione giudiziale</strong> si chiede quando l'accordo non c'è. Il giudice decide su affidamento, mantenimento e assegnazione della casa familiare, se necessario dopo un'istruttoria. Dura di più e costa di più: per questo lo Studio cerca sempre prima un accordo, senza rinunciare a tutelare il cliente.</p>"
            "<h2>Casa familiare e mantenimento</h2>"
            "<p>La casa familiare viene assegnata di regola al genitore con cui i figli vivono prevalentemente, indipendentemente da chi ne è proprietario. L'assegno per i figli tiene conto delle loro esigenze, del tenore di vita, dei tempi di permanenza presso ciascun genitore e dei redditi di entrambi. L'assegno per il coniuge spetta solo a chi non ha redditi adeguati.</p>"
            "<h2>Da dove partire</h2>"
            "<p>Prima del colloquio è utile raccogliere i documenti principali con la <a href='/strumento-checklist-separazione'>checklist per la separazione</a>, da spuntare o stampare. Per i costi, vedere <a href='/costi-avvocato'>quanto costa una separazione</a>.</p>"
            "</div>\n" + pannello
        )
    idx = s.find("</div>\n<aside")
    if idx != -1:
        s = s[:idx] + pannello + s[idx:]
    tool = STRUMENTI_LINK.get("attivita-" + key)
    if tool is not None:
        s = s.replace('<aside style="display:grid;gap:14px;margin-top:14px">\n', '<aside style="display:grid;gap:14px;margin-top:14px">\n' + strumenti_card(tool), 1)
    return s


def fix_guida(s, slug):
    tool = STRUMENTI_LINK.get(slug)
    if tool is not None:
        s = s.replace('<aside style="display:grid;gap:14px;margin-top:14px">\n', '<aside style="display:grid;gap:14px;margin-top:14px">\n' + strumenti_card(tool), 1)
    s = s.replace("<p class=\"note-s\">A cura dello Studio Legale Pernorio, Avv. Daniela Pernorio, Vigevano.",
                  "<p class=\"note-s\">A cura dello Studio Legale Pernorio, <a href='/studio'>Avv. Daniela Pernorio</a>, Vigevano.", 1)
    return s


HOME_DESC = "Avv. Daniela Pernorio, avvocato civilista a Vigevano (PV): separazioni e divorzi, affidamento dei figli, eredità, sfratti, debiti con banche. Tribunale di Pavia."


def fix_home(s):
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{HOME_DESC}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{HOME_DESC}">', s, count=1)
    s = s.replace('<p class="sub">Avv. Daniela Pernorio</p>', '<p class="sub">Avv. Daniela Pernorio, avvocato a Vigevano</p>', 1)
    s = s.replace('imagesrcset="img/ritratto-daniela-900.webp 900w, img/ritratto-daniela.webp 1600w"',
                  'imagesrcset="img/ritratto-daniela-900.webp 900w, img/ritratto-daniela.webp 793w"')
    chips = "".join(f"<a class='chip' href='/{c['slug']}'>{esc(c['nome'])}</a>" for c in C.COMUNI)
    sez = (
        '<section><div class="wrap"><div class="sec-head rv"><span class="label">Strumenti e territorio</span><h2>Prima di chiamare</h2></div>'
        f'<div class="tools-grid">{card_online()}{strumenti_card()}'
        f'<a class="card panel rv gcard" href="/costi-avvocato"><span class="label">Trasparenza</span><b>Quanto costa un avvocato</b><span class="note-s">Preventivo scritto, voci di costo, spese vive →</span></a>'
        "</div>"
        f'<div class="card panel rv" style="margin-top:14px"><span class="label">Dove operiamo</span><p style="margin-top:10px">Lo Studio riceve a Vigevano e assiste clienti di tutta la Lomellina e dell\'Abbiatense.</p><div class="chips" style="margin-top:14px">{chips}<a class=\'chip\' href=\'/{C.LOMELLINA["slug"]}\'>Tutta la Lomellina</a></div></div>'
        "</div></section>\n"
    )
    # Inserita prima della sezione "Guide pratiche", altrimenti in fondo al main
    m = re.search(r'<section[^>]*>(?:(?!<section).)*?Guide pratiche', s, re.S)
    if m:
        s = s[: m.start()] + sez + s[m.start():]
    else:
        s = s.replace("</main>", sez + "</main>", 1)
    return s


def fix_contatti(s):
    s = s.replace('<aside', '<aside', 1)
    m = re.search(r'<div class="card panel rv"><form', s)
    if m:
        s = s[:m.start()] + '<div style="margin-bottom:14px">' + card_online() + '</div>' + s[m.start():]
    s = s.replace('<p class="ok" hidden>Anteprima: nel sito pubblicato la richiesta arriva via email allo Studio.</p>\n', "")
    s = s.replace('<p class="ok" hidden>Anteprima: nel sito pubblicato la richiesta arriva via email allo Studio.</p>', "")
    s = s.replace("<form action='grazie' class='cf' id='cf' method='POST' name='contatti'>",
                  "<form action='/grazie' class='cf' id='cf' method='POST' name='contatti' data-netlify='true' netlify-honeypot='bot-field'>")
    return s


MISURA_TXT = ("<p><b>Misura delle visite, senza cookie.</b> Il sito conta in forma aggregata da dove arrivano le visite "
              "(per esempio Google, la scheda Google dello Studio, ChatGPT o altri assistenti IA) e quante volte vengono toccati i pulsanti "
              "Chiama, WhatsApp e invio dei moduli. Per ogni evento registra solo il tipo, la pagina, la provenienza e l'ora: nessun cookie, "
              "nessun indirizzo IP, nessun identificativo del dispositivo. La provenienza resta nel browser solo per la durata della visita "
              "(sessionStorage) e si cancella chiudendo la scheda. I dati sono conservati su Netlify, Inc. e servono solo allo Studio "
              "per capire quali pagine sono utili. Conta inoltre, lato server, le letture delle pagine da parte dei programmi automatici "
              "delle intelligenze artificiali.</p>\n")


def fix_privacy(s):
    add = ("<p><b>Colloqui a distanza.</b> Con il modulo di richiesta di colloquio online si possono inviare documenti, conservati "
           "dal fornitore del modulo (Netlify, Inc.) per il tempo necessario a gestire la richiesta e poi trasferiti nel fascicolo dello Studio. "
           "Le videochiamate si svolgono, a scelta del cliente, tramite Jitsi Meet (8x8, Inc.) con un link personale non pubblicato, "
           "WhatsApp o telefono. I colloqui non vengono registrati. La prova di videocamera e microfono presente sul sito funziona solo nel browser "
           "e non trasmette immagini né audio.</p>\n"
           "<p><b>Calcolatori e strumenti per assistenti IA.</b> I calcolatori del sito funzionano nel browser e non inviano allo Studio i dati inseriti. "
           "Il servizio per assistenti IA all'indirizzo /mcp e gli strumenti WebMCP restituiscono solo informazioni pubbliche e calcoli: "
           "non chiedono e non conservano dati personali, salvo i normali registri tecnici del fornitore di hosting (Netlify, Inc.). "
           "La funzione che prepara una richiesta di contatto si limita a precompilare il modulo nel browser: l'invio resta sempre una scelta della persona.</p>\n")
    return s.replace("<p><b>Diritti.</b>", add + MISURA_TXT + "<p><b>Diritti.</b>", 1)


def fix_cookie(s):
    s = s.replace("<p>Il sito non usa cookie di profilazione né strumenti di statistica.",
                  "<p>Il sito non usa cookie, né di profilazione né di statistica. Per sapere da dove arrivano le visite usa una misura "
                  "propria senza cookie, descritta nell'<a href='/privacy'>informativa privacy</a>.", 1)
    return s.replace(
        "I caratteri tipografici sono forniti dal servizio Google Fonts: per scaricarli il browser si collega ai server di Google, che ricevono l'indirizzo IP del visitatore.",
        "I caratteri tipografici sono ospitati direttamente sul sito: il browser non si collega a servizi esterni per scaricarli.",
    )


CSS_EXTRA = """
/* --- aggiunte SEO/UX novembre 2026 --- */
.article > h2:first-child{margin-top:0}
.ticks a{text-decoration:underline;text-underline-offset:3px}
h1 .h1s{display:block;margin-top:.5em;font-family:var(--body);font-size:.95rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500;color:var(--graphite)}
footer .fzones{margin-top:28px;font-size:.8rem;line-height:1.9;color:color-mix(in srgb,var(--on-dark) 70%,transparent)}
footer .fzones a{text-decoration:underline;text-underline-offset:3px}
footer .fzones span{text-transform:uppercase;letter-spacing:.16em;font-size:.66rem;margin-right:6px}
.tools-grid{display:grid;gap:14px}
@media (min-width:760px){.tools-grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.tool form{display:grid;gap:16px}
.tool label{display:grid;gap:6px;font-size:.9rem;font-weight:500}
.tool input[type=number],.tool input[type=text],.tool input[type=date],.tool select{font:inherit;padding:12px 14px;border:1px solid color-mix(in srgb,var(--ink) 22%,transparent);border-radius:12px;background:var(--paper);color:var(--ink);min-height:48px;width:100%;box-sizing:border-box}
.tool .tgrid{display:grid;gap:14px}
@media (min-width:600px){.tool .tgrid{grid-template-columns:1fr 1fr}}
.tool .tchk{display:flex;align-items:center;gap:10px;grid-template-columns:none}
.tool input[type=checkbox]{width:20px;height:20px;accent-color:var(--ink)}
.qt{width:100%;border-collapse:collapse;margin-top:18px;font-size:.92rem}
.qt th,.qt td{text-align:left;padding:10px 8px;border-bottom:1px solid color-mix(in srgb,var(--ink) 12%,transparent);vertical-align:top}
.qt th{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500}
.qt small{color:var(--graphite)}
.qt tr.late td{opacity:.55;text-decoration:line-through}
.cklist{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:10px}
.cklist label{display:flex;gap:12px;align-items:flex-start;font-weight:400}
.cklist input{flex:none;margin-top:3px}
.tool h2{font-size:1.5rem;margin-top:22px}
@media print{header.top,.sheet,footer,.dock,aside,.phero .actions,.cta-card,#ck .actions{display:none!important}.tool{box-shadow:none;border:0}}
"""


CSS_EXTRA += """
.article .caso{margin:30px 0;padding:22px 22px 18px;border-radius:18px;background:color-mix(in srgb,var(--forest) 7%,var(--card));border:1px solid color-mix(in srgb,var(--forest) 22%,transparent)}
.article .caso .caso-q{font-family:var(--display);font-size:1.45rem;line-height:1.3;margin:8px 0 6px;color:var(--ink)}
.article .caso p{margin:0 0 10px}
.article .caso .actions{margin:14px 0 10px}
"""


def build_css():
    fonts = open(os.path.join(STATIC, "fonts", "fonts.css"), encoding="utf-8").read()
    css = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
    return fonts + "\n" + css + CSS_EXTRA + CO.CSS + TR.CSS


# ---------------------------------------------------------------------------
# Agenti IA: grafo delle entità, versione Markdown, WebMCP (vedi tools/agenti.py)
# ---------------------------------------------------------------------------

def dati_studio():
    return {
        "nome": "Studio Legale Pernorio",
        "avvocato": "Avv. Daniela Pernorio, avvocato civilista iscritta all'Ordine degli Avvocati di Pavia dal 2014",
        "indirizzo": "Via Egidio Sacchetti 14, 27029 Vigevano (PV), Italia",
        "telefono": "+39 0381 386276",
        "whatsapp": "https://wa.me/393333368757",
        "instagram": INSTAGRAM,
        "orari": ORARI_TXT,
        "tribunali": ["Pavia", "Milano", "Novara"],
        "primo_colloquio": "In Studio a Vigevano oppure online in videochiamata, su appuntamento; preventivo scritto prima di iniziare.",
        "contatti": clean_url("contatti"),
        "colloquio_online": clean_url(CO.SLUG),
        "costi": clean_url("costi-avvocato"),
        "materie": [{"nome": v[0].upper() + v[1:], "url": clean_url("attivita-" + k)} for k, v in MATERIE_KW.items()],
        "comuni_serviti": [{"nome": "Vigevano", "url": BASE + "/"}] + [
            {"nome": c["nome"], "distanza": c["km"], "url": clean_url(c["slug"])} for c in C.COMUNI],
        "avvertenza": "Informazioni generali: ogni caso va valutato sui documenti con l'avvocato.",
    }


TITOLI_NUOVI = {
    "guida-eredita-con-debiti": "Eredità con debiti: rinuncia o beneficio d'inventario · Vigevano",
    "guida-usucapione-quando-si-diventa-proprietari": "Usucapione: quando si diventa proprietari · Studio Pernorio",
}

DESC_NUOVE = {
    "index": "Avv. Daniela Pernorio, avvocato civilista a Vigevano (PV): separazioni e divorzi, figli, eredità, sfratti, debiti con banche. Tribunale di Pavia.",
    "diritto-di-famiglia": "Separazione, divorzio, affidamento e mantenimento dei figli, unioni civili e convivenze: l'Avv. Daniela Pernorio a Vigevano, Tribunale di Pavia.",
    "guide": "Guide pratiche dell'Avv. Daniela Pernorio su famiglia, eredità, casa, debiti, lavoro e multe: risposte chiare, fonti di legge e casi frequenti.",
    "cookie": "Informativa cookie dello Studio Legale Pernorio di Vigevano: nessun cookie, nessuna profilazione; le visite sono contate in forma aggregata.",
    "privacy": "Informativa privacy dello Studio Legale Pernorio, Vigevano: quali dati raccoglie il sito con i moduli di contatto, perché e per quanto tempo.",
    "attivita": "Le 18 materie dell'Avv. Daniela Pernorio, avvocato civilista a Vigevano: famiglia e figli, eredità, casa e affitti, debiti, contratti, incidenti, lavoro.",
    "domiciliazioni": "Domiciliazioni e sostituzioni d'udienza per colleghi avvocati presso i Tribunali di Pavia, Milano e Novara e il Giudice di Pace di Vigevano.",
}

TITOLI_NUOVI.update(RI.TITOLI)
DESC_NUOVE.update(RI.DESCRIZIONI)

# Fonti normative aggiunte dopo l'analisi delle ricerche
FO.ATTI.setdefault("urn:nir:stato:decreto.legislativo:1993-09-01;385", "D.Lgs. 1 settembre 1993, n. 385 (Testo unico bancario)")
_ATTO = {"cc": FO.CC, "cpc": FO.CPC, "tub": "urn:nir:stato:decreto.legislativo:1993-09-01;385"}
for _slug, _lst in RI.FONTI_EXTRA.items():
    _gia = {x["urn"] for x in FO.FONTI.get(_slug, [])}
    for _et, _a, _art in _lst:
        _f = FO.f(_et, _ATTO[_a], _art)
        if _f["urn"] not in _gia:
            FO.FONTI.setdefault(_slug, []).append(_f)


# Navigazione istantanea: il browser precarica la pagina quando il dito o il mouse
# si avvicina al link (Speculation Rules, Chrome/Edge; ignorato dagli altri browser).
SPECULATION = ('<script type="speculationrules">' + json.dumps({"prefetch": [{"where": {"and": [
    {"href_matches": "/*"}, {"not": {"href_matches": "/grazie"}}, {"not": {"href_matches": "/*.md"}},
    {"not": {"selector_matches": "[target=_blank]"}}]}, "eagerness": "moderate"}]}) + "</script>")


CORRELATE = {}
STOP = set("della delle degli dello dalla dalle sono come cosa quando quanto anche più può deve fare essere stato alla allo agli alle nella nelle negli nel con per tra fra che non una uno gli dei del dal sul sulla questo questa studio pernorio avvocato vigevano guida guide".split())


def calcola_correlate(pagine):
    """Per ogni guida, le 3 guide più vicine per contenuto (Jaccard sulle parole)."""
    def parole(h):
        m = re.search(r"<main>(.*)</main>", h, re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", m.group(1) if m else h, flags=re.S)))
        return {w for w in re.findall(r"[a-zàèéìòù]{5,}", t.lower()) if w not in STOP}
    g = {k: parole(v) for k, v in pagine.items() if k.startswith("guida-")}
    df = {}
    for ws in g.values():
        for w in ws:
            df[w] = df.get(w, 0) + 1
    comuni = {w for w, n in df.items() if n > len(g) * 0.2}  # parole troppo diffuse: non distinguono il tema
    g = {k: ws - comuni for k, ws in g.items()}
    titoli = {k: html.unescape(re.search(r"<h1[^>]*>(.*?)</h1>", v, re.S).group(1)) for k, v in pagine.items() if k in g}
    for a in g:
        sim = sorted(((len(g[a] & g[b]) / max(1, len(g[a] | g[b])), b) for b in g if b != a), reverse=True)[:3]
        CORRELATE[a] = [(b, re.sub(r"<[^>]+>", "", titoli[b]).strip()) for _, b in sim]


TEL_TXT = "0381 386276"


def cta_guida(s, slug):
    """Pulsanti in testa alla guida e riquadro 'il suo caso' a metà articolo."""
    if not slug.startswith("guida-") or slug == "guida-domiciliazioni-tribunale-pavia":
        return s
    # pulsanti nell'intestazione, se mancano (guide originali)
    m = re.search(r'(<section class="phero">.*?<p class=lead>.*?</p>)(</div></section>)', s, re.S)
    if m and "class=actions" not in m.group(1):
        s = s.replace(m.group(0), m.group(1) + f"<div class=actions>{BTN_CALL}{BTN_WA}</div>" + m.group(2), 1)
    a = s.find('<article class="card panel article')
    if a == -1:
        return s
    dom, testo = RI.CTA.get(slug, RI.CTA_DEFAULT)
    box = (
        '<aside class="caso" aria-label="Parlarne con lo Studio">'
        f'<span class="label">Il suo caso</span><p class="caso-q">{esc(dom)}</p><p>{esc(testo)}</p>'
        f'<div class="actions">{BTN_CALL}{BTN_WA}</div>'
        f'<p class="note-s">Oppure chiami lo <a href="tel:+390381386276">{TEL_TXT}</a> · {ORARI_TXT} · '
        '<a href="/colloquio-online">colloquio anche online</a></p></aside>\n'
    )
    fine = s.find("</article>", a)
    pos = [m.start() for m in re.finditer(r"<h2[ >]", s[a:fine])]
    i = a + pos[2] if len(pos) >= 3 else (a + pos[-1] if pos else s.rfind('<p class="note-s">A cura', a, fine))
    if i < a:
        return s
    return s[:i] + box + s[i:]


def applica_ricerche(s, slug):
    """Sezioni, FAQ e date aggiornate per le pagine viste in Search Console (tools/ricerche.py)."""
    if slug in RI.TITOLI:
        s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(RI.TITOLI[slug])}">', s, count=1)
    sez = RI.SEZIONI.get(slug)
    faq = RI.FAQ.get(slug)
    if not (sez or faq) or "</article>" not in s:
        return s
    firma = '<p class="note-s">A cura dello Studio Legale Pernorio'
    if sez:
        i = s.rfind(firma)
        i = i if i != -1 else s.rfind("</article>")
        s = s[:i] + sez.strip() + "\n" + s[i:]
    s = re.sub(r"(Aggiornato a )ottobre 2026", r"\g<1>" + RI.AGGIORNATO, s)
    s = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{OGGI}"', s)
    if faq:
        det = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
        box = (f'<div class="card panel faq rv" style="margin-top:14px"><h2>Domande frequenti</h2>{det}</div>' + ld(faq_ld(faq)))
        i = s.rfind("</article>") + len("</article>")
        s = s[:i] + box + s[i:]
    return s


def redirects(tutte):
    """301 da /pagina.html a /pagina (Search Console vede entrambe) e dai vecchi indirizzi."""
    righe = ["", "# Generato da tools/build.py: una sola versione per pagina, senza .html"]
    for vecchio, nuovo in RI.VECCHI_URL.items():
        righe.append(f"{vecchio}  {nuovo}  301!")
    for slug in sorted(tutte):
        if slug in ("index", "404"):
            continue
        righe.append(f"/{slug}.html  /{slug}  301!")
    return "\n".join(righe) + "\n"


def titolo_corto(t, n=65):
    """Title entro n caratteri (Google taglia oltre ~600 px): si accorcia la firma, mai il tema."""
    base = t.split(" · ")[0]
    if len(t) <= n:
        return t
    for suff in (" · Studio Pernorio, Vigevano", " · Studio Pernorio", " · Vigevano", ""):
        if "Vigevano" in base and "Vigevano" in suff:
            continue
        if len(base + suff) <= n:
            return base + suff
    return base


def fix_agenti(s, slug):
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if m:
        nuovo = esc(TITOLI_NUOVI.get(slug) or titolo_corto(html.unescape(m.group(1).strip())))
        s = s.replace(m.group(0), f"<title>{nuovo}</title>", 1)
    if slug in CORRELATE and "</article>" in s:
        li = "".join(f"<li><a href='/{b}'>{esc(t)}</a></li>" for b, t in CORRELATE[slug])
        i = s.rfind("</article>") + len("</article>")
        s = s[:i] + f'<div class="card panel rv" style="margin-top:14px"><h2>Guide correlate</h2><ul>{li}</ul></div>' + s[i:]
    if slug in DESC_NUOVE:
        d = esc(DESC_NUOVE[slug])
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{d}">', s, count=1)
        s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{d}">', s, count=1)
    title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip())
    m = re.search(r'<meta name="description" content="([^"]*)">', s)
    desc = html.unescape(m.group(1)) if m else ""
    url = clean_url(slug)

    fonti = FO.FONTI.get(slug, [])

    def bc(mm):
        d = json.loads(mm.group(1))
        if isinstance(d, dict) and d.get("@type") == "BreadcrumbList":
            d["@id"] = url + "#percorso"
        if isinstance(d, dict) and d.get("@type") == "Article" and fonti:
            d["citation"] = [{"@type": "Legislation", "name": x["etichetta"], "legislationIdentifier": x["urn"],
                              "url": x["url"], "isPartOf": {"@type": "Legislation", "name": FO.ATTI[x["atto"]]},
                              "legislationJurisdiction": "IT"} for x in fonti]
        return ld(d)
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', bc, s, flags=re.S)
    if fonti and "</article>" in s:
        li = "".join(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["etichetta"])}</a></li>' for x in fonti)
        box = ('<div class="card panel rv fonti" style="margin-top:14px"><h2>Fonti normative</h2>'
               f'<ul>{li}</ul><p class="note-s">Testi ufficiali su Normattiva, la banca dati pubblica della normativa italiana. Collegamenti controllati il {OGGI[8:10]}/{OGGI[5:7]}/{OGGI[:4]}.</p></div>')
        i = s.rfind("</article>") + len("</article>")
        s = s[:i] + box + s[i:]
    nodi = []
    if url + "#pagina" not in s:
        n = AG.nodo_pagina(slug, title, desc, OGGI)
        if url + "#percorso" not in s:
            del n["breadcrumb"]
        nodi.append(n)
    if slug.startswith("attivita-"):
        kw = MATERIE_KW[slug[len("attivita-"):]]
        nodi.append(AG.nodo_servizio(slug, "Avvocato per " + kw, url))
    if os.path.exists(os.path.join(STATIC, "og", slug + ".jpg")):
        img = f"{BASE}/og/{slug}.jpg"
        s = re.sub(r'<meta property="og:image" content="[^"]*">', "", s)
        s = re.sub(r'<meta name="twitter:image" content="[^"]*">', "", s)
        s = s.replace('<link rel="icon"', f'<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(title)}"><meta name="twitter:image" content="{img}">\n<link rel="icon"', 1)
        if nodi:
            nodi[0]["primaryImageOfPage"] = {"@type": "ImageObject", "url": img, "width": 1200, "height": 630}
    if nodi:
        s = s.replace("</body>", "".join(ld(n) for n in nodi) + "\n</body>", 1)
    testa = f'<link rel="alternate" type="text/markdown" href="{AG.md_di(slug)}" title="Versione Markdown per assistenti IA">'
    s = s.replace('<link rel="manifest"', testa + '<link rel="manifest"', 1)
    s = s.replace("</body>", '<script src="/agenti.js" defer></script><script src="/conta.js" defer></script>\n' + SPECULATION + "\n</body>", 1)
    if slug == "contatti":
        s = AG.modulo_webmcp(s)
    return s


def csp(tutte):
    """Content-Security-Policy rigorosa: solo script del sito e script interni elencati per hash."""
    import base64
    import hashlib
    hs = set()
    for h in tutte.values():
        for m in re.finditer(r'<script(?: type="speculationrules")?>(.*?)</script>', h, re.S):
            hs.add("'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode()).digest()).decode() + "'")
    handler = "'sha256-" + base64.b64encode(hashlib.sha256(b"return false").digest()).decode() + "'"
    return "; ".join([
        "default-src 'self'",
        "script-src 'self' " + " ".join(sorted(hs)) + " 'unsafe-hashes' " + handler,
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: blob:",
        "font-src 'self'",
        "connect-src 'self'",
        "media-src 'self' blob: mediastream:",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'self'",
        "upgrade-insecure-requests",
    ])


def scrivi_agenti(tutte, indicizzabili, date):
    """File per agenti: Markdown di ogni pagina, indice di ricerca, agenti.js, robots.txt."""
    indice = []
    for slug in indicizzabili:
        s = tutte[slug]
        with open(os.path.join(DIST, AG.md_di(slug).lstrip("/")), "w", encoding="utf-8") as fh:
            fh.write(AG.pagina_md(slug, s, date[slug][1]))
        t = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip())
        m = re.search(r'<meta name="description" content="([^"]*)">', s)
        h2 = " ".join(html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S))
        faqs = " ".join(html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<summary>(.*?)</summary>", s, re.S))
        indice.append({"t": t, "d": html.unescape(m.group(1)) if m else "", "k": (h2 + " " + faqs)[:900], "u": clean_url(slug), "m": BASE + AG.md_di(slug), "c": TR.categoria(slug)})
    indice += TR.glossario_indice()
    with open(os.path.join(DIST, "cerca.json"), "w", encoding="utf-8") as fh:
        json.dump(indice, fh, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(DIST, "agenti.js"), "w", encoding="utf-8") as fh:
        fh.write(AG.agenti_js(dati_studio()))
    # Server MCP (Netlify Function) e scheda di scoperta
    versione = OGGI.replace("-", ".")
    os.makedirs(FUNZIONI, exist_ok=True)
    with open(os.path.join(FUNZIONI, "mcp.mjs"), "w", encoding="utf-8") as fh:
        fh.write(AG.mcp_function(dati_studio(), indice, versione))
    wk = os.path.join(DIST, ".well-known", "mcp")
    os.makedirs(wk, exist_ok=True)
    with open(os.path.join(wk, "server-card.json"), "w", encoding="utf-8") as fh:
        json.dump(AG.server_card(versione), fh, ensure_ascii=False, indent=1)
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(AG.ROBOTS)


# ---------------------------------------------------------------------------

NON_INDICIZZATE = ("404", "grazie", TR.CERCA_SLUG)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)
    shutil.copytree(os.path.join(STATIC, "fonts"), os.path.join(DIST, "fonts"))
    if os.path.isdir(os.path.join(STATIC, "og")):
        shutil.copytree(os.path.join(STATIC, "og"), os.path.join(DIST, "og"))
    for fn in os.listdir(os.path.join(STATIC, "root")):
        shutil.copy(os.path.join(STATIC, "root", fn), os.path.join(DIST, fn))
    os.remove(os.path.join(DIST, "fonts", "fonts.css"))
    with open(os.path.join(DIST, "style.css"), "w", encoding="utf-8") as fh:
        fh.write(build_css())

    pagine = {}
    for fn in sorted(os.listdir(SRC)):
        if fn.endswith(".html"):
            pagine[fn[:-5]] = open(os.path.join(SRC, fn), encoding="utf-8").read()

    nuove = {}
    nuove.update(pagine_comuni())
    nuove[C.LOMELLINA["slug"]] = pagina_lomellina()
    nuove[C.COSTI["slug"]] = pagina_info(C.COSTI)
    nuove.update(pagine_strumenti())
    nuove.update(pagine_guide())
    nuove[CO.SLUG] = pagina_colloquio()
    nuove[TR.GLOSSARIO_SLUG] = pagina_glossario(set(pagine) | set(nuove))
    nuove[TR.CERCA_SLUG] = pagina_cerca()
    registro = TR.carica_registro()
    date = {}

    calcola_correlate({**pagine, **nuove})
    tutte = {}
    for slug, s in list(pagine.items()) + list(nuove.items()):
        if slug.startswith("attivita-"):
            s = fix_pratica(s, slug[len("attivita-"):])
        elif slug.startswith("guida-"):
            s = fix_guida(s, slug)
        elif slug == "index":
            s = fix_home(s)
        elif slug == "contatti":
            s = fix_contatti(s)
        elif slug == "cookie":
            s = fix_cookie(s)
        elif slug == "privacy":
            s = fix_privacy(s)
        elif slug == "guide":
            s = fix_indice_guide(s)
        elif slug == "studio":
            s = fix_studio(s)
        s = applica_ricerche(s, slug)
        s = cta_guida(s, slug)
        s = fix_orari_social(s)
        s = fix_urls(s)
        s = fix_ld(s)
        if slug == "404":
            s = s.replace("<div class=actions>", TR.modulo_cerca() + '<div class=actions style="margin-top:18px">', 1)
        s = fix_head(s, slug, noindex=slug in NON_INDICIZZATE)
        s = fix_nav(s)
        s = fix_footer(s)
        if slug not in NON_INDICIZZATE:
            s = fix_agenti(s, slug)
            date[slug] = TR.date_pagina(registro, slug, s, OGGI)
            s = TR.applica_date(s, OGGI, *date[slug])
        tutte[slug] = s
        with open(os.path.join(DIST, slug + ".html"), "w", encoding="utf-8") as fh:
            fh.write(s)

    # Sitemap: la data cambia solo quando cambia il testo della pagina (dati/date-pagine.json)
    TR.salva_registro(registro)
    esclusi = set(NON_INDICIZZATE)
    prio = {"index": "1.0", "attivita": "0.9", "contatti": "0.9", "studio": "0.8"}
    urls = []
    for slug in sorted(tutte, key=lambda x: (x != "index", x)):
        if slug in esclusi:
            continue
        p = prio.get(slug, "0.8" if slug.startswith(("attivita-", "avvocato-")) else "0.7")
        ha_og = os.path.exists(os.path.join(STATIC, "og", slug + ".jpg"))
        urls.append((clean_url(slug), date[slug][1], p, TR.immagini_pagina(slug, tutte[slug], ha_og)))
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(TR.sitemap(urls))

    # Feed Atom delle guide, ricerca nel sito, OpenSearch, catalogo delle API
    voci = []
    for slug in sorted(tutte):
        if not slug.startswith("guida-"):
            continue
        h = tutte[slug]
        cat = re.search(r'<span class="label">Guida · ([^·<]+)', h)
        voci.append({"url": clean_url(slug), "pub": date[slug][0], "mod": date[slug][1],
                     "titolo": html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1))).strip(),
                     "sommario": html.unescape(re.search(r'<meta name="description" content="([^"]*)">', h).group(1)),
                     "cat": html.unescape(cat.group(1)).strip() if cat else "Guide"})
    for fn, testo in (("feed.xml", TR.feed_atom(voci)), ("opensearch.xml", TR.opensearch()), ("cerca.js", TR.CERCA_JS)):
        with open(os.path.join(DIST, fn), "w", encoding="utf-8") as fh:
            fh.write(testo)
    os.makedirs(os.path.join(DIST, ".well-known"), exist_ok=True)
    with open(os.path.join(DIST, ".well-known", "api-catalog"), "w", encoding="utf-8") as fh:
        json.dump(TR.api_catalog(), fh, ensure_ascii=False, indent=1)

    # robots.txt, Markdown, indice di ricerca e WebMCP
    scrivi_agenti(tutte, [x for x in tutte if x not in esclusi], date)

    # llms.txt e llms-full.txt
    for fn in ("llms.txt", "llms-full.txt"):
        t = fix_urls(open(os.path.join(SRC, fn), encoding="utf-8").read())
        if fn == "llms.txt":
            t = t.rstrip() + "\n\n## Dove operiamo\n\n"
            t += "".join(f"- [Avvocato per {c['nome']}]({clean_url(c['slug'])}): {c['km']} dallo Studio, tribunale competente e materie\n" for c in C.COMUNI)
            t += f"- [Avvocato in Lomellina]({clean_url(C.LOMELLINA['slug'])}): tutti i comuni serviti\n"
            t += "\n## Costi e strumenti\n\n"
            t += f"- [Quanto costa un avvocato]({clean_url('costi-avvocato')}): preventivo scritto, parametri, spese vive\n"
            t += f"\n## Colloquio online\n\n- [Colloquio online con l'avvocato]({clean_url(CO.SLUG)}): videochiamata dal browser o WhatsApp, invio documenti, riepilogo e preventivo scritto\n"
            t += "\n## Nuove guide\n\n" + "".join(f"- [{g['titolo']}]({clean_url(g['slug'])}): {g['sommario']}\n" for g in G.GUIDE)
            t += f"- [Glossario legale]({clean_url(TR.GLOSSARIO_SLUG)}): {len(TR.GLOSSARIO)} termini di diritto civile spiegati in breve, con la fonte di legge\n"
            t += "\n## Strumenti\n\n"
            t += "".join(f"- [{x['titolo_breve']}]({clean_url(x['slug'])}): {x['intro']}\n" for x in C.STRUMENTI)
            t += ("\n## Per agenti e assistenti IA\n\n"
                  f"- Ogni pagina ha una versione Markdown: aggiungere .md all'indirizzo (es. {BASE}/attivita-separazione-divorzio.md, home: {BASE}/index.md)\n"
                  f"- Con l'intestazione HTTP Accept: text/markdown ogni pagina risponde direttamente in Markdown\n"
                  f"- [Feed Atom delle guide]({BASE}/feed.xml), con data di pubblicazione e di ultimo aggiornamento\n"
                  f"- Ricerca: {BASE}/cerca?q=parola (pagina per le persone); descrizione OpenSearch: {BASE}/opensearch.xml; catalogo: {BASE}/.well-known/api-catalog\n"
                  f"- [Indice di ricerca JSON]({BASE}/cerca.json): titolo, descrizione, URL e versione Markdown di ogni pagina\n"
                  f"- Server MCP pubblico, senza registrazione: {BASE}/mcp (Streamable HTTP; scheda: {BASE}/.well-known/mcp/server-card.json)\n"
                  "- Strumenti WebMCP nel browser (document.modelContext): informazioni-studio, cerca-nel-sito, calcola-quote-eredita, calcola-imposta-successione, scadenze-multa, prepara-richiesta-allo-studio (non invia nulla senza il click della persona)\n")
        with open(os.path.join(DIST, fn), "w", encoding="utf-8") as fh:
            fh.write(t)

    # site.webmanifest con percorsi assoluti
    m = open(os.path.join(SRC, "site.webmanifest"), encoding="utf-8").read().replace('"img/', '"/img/')
    with open(os.path.join(DIST, "site.webmanifest"), "w", encoding="utf-8") as fh:
        fh.write(m)

    # Misura senza cookie: script, pagina riservata e funzione
    MIS = os.path.join(ROOT, "tools", "misura")
    for fn in ("conta.js", "statistiche.js", "statistiche.html"):
        shutil.copy(os.path.join(MIS, fn), os.path.join(DIST, fn))
    hash_chiave = open(os.path.join(MIS, "chiave.sha256")).read().strip()
    with open(os.path.join(FUNZIONI, "conta.mjs"), "w", encoding="utf-8") as fh:
        fh.write(open(os.path.join(MIS, "conta.mjs"), encoding="utf-8").read().replace("__HASH_CHIAVE__", hash_chiave))

    # Redirect e header Netlify
    shutil.copy(os.path.join(ROOT, "netlify", "_redirects"), os.path.join(DIST, "_redirects"))
    with open(os.path.join(DIST, "_redirects"), "a", encoding="utf-8") as fh:
        fh.write(redirects(tutte))
    shutil.copy(os.path.join(ROOT, "netlify", "_headers"), os.path.join(DIST, "_headers"))
    with open(os.path.join(DIST, "_headers"), "a", encoding="utf-8") as fh:
        fh.write("\n# Generato da tools/build.py\n/*\n  Content-Security-Policy: " + csp(tutte) + "\n")
        fh.write("\n/statistiche*\n  X-Robots-Tag: noindex, nofollow\n  Cache-Control: no-store\n")
        fh.write(TR.HEADERS)
    shutil.copy(os.path.join(ROOT, "netlify", "netlify.toml"), os.path.join(DIST, "netlify.toml"))

    print(f"Build completato: {len(tutte)} pagine ({len(nuove)} nuove), {len(urls)} URL in sitemap -> {DIST}")


if __name__ == "__main__":
    main()
