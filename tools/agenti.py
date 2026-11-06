# -*- coding: utf-8 -*-
"""Il sito letto e usato dagli agenti IA (ChatGPT, Claude, Gemini, Perplexity, Copilot).

Idee riprese da progetti open source studiati a novembre 2026:
- WebMCP (W3C Web Machine Learning CG): la pagina espone "strumenti" che l'agente
  integrato nel browser può chiamare (Chrome 149 e Edge 150 in origin trial,
  ChatGPT Desktop, Brave Leo). Qui: /agenti.js e gli attributi toolname sul modulo.
- squirrelscan, regola ax/markdown-response: una versione Markdown di ogni pagina
  (/pagina.md), segnalata con <link rel="alternate" type="text/markdown">.
- squirrelscan, entity map: un solo grafo di identità (@id) su tutte le pagine.
- robots.txt con Content-Signal (search, ai-input, ai-train).
"""
import json
import re

from bs4 import BeautifulSoup, NavigableString

BASE = "https://studiolegalepernorio.com"


def url_di(slug):
    return BASE + "/" if slug == "index" else f"{BASE}/{slug}"


def md_di(slug):
    return "/index.md" if slug == "index" else f"/{slug}.md"


# ---------------------------------------------------------------------------
# Versione Markdown delle pagine
# ---------------------------------------------------------------------------

def _inline(el):
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(re.sub(r"\s+", " ", str(c)))
        elif c.name in ("script", "style", "svg", "noscript", "button", "input", "select", "textarea"):
            continue
        elif c.name == "a":
            t = _inline(c).strip()
            href = c.get("href", "")
            if href.startswith("/"):
                href = BASE + href
            out.append(f"[{t}]({href})" if t and href and not href.startswith("#") else t)
        elif c.name in ("strong", "b"):
            t = _inline(c).strip()
            out.append(f"**{t}**" if t else "")
        elif c.name in ("em", "i"):
            t = _inline(c).strip()
            out.append(f"*{t}*" if t else "")
        elif c.name == "span" and "h1s" in (c.get("class") or []):
            out.append(" · " + _inline(c).strip())
        elif c.name == "br":
            out.append("\n")
        else:
            out.append(_inline(c))
    return "".join(out)


def _blocchi(el, out):
    for c in el.children:
        if isinstance(c, NavigableString):
            t = str(c).strip()
            if t:
                out.append(t)
            continue
        n = c.name
        if n in ("script", "style", "svg", "noscript", "form", "button", "template", "img", "picture", "nav"):
            continue
        if c.get("class") and set(c.get("class")) & {"actions", "hp", "crumbs", "chips"}:
            continue
        if n in ("h1", "h2", "h3", "h4"):
            t = _inline(c).strip()
            if t:
                out.append("#" * int(n[1]) + " " + t)
        elif n == "p":
            t = _inline(c).strip()
            if t:
                out.append(t)
        elif n in ("ul", "ol"):
            righe = []
            for i, li in enumerate(c.find_all("li", recursive=False), 1):
                t = _inline(li).strip()
                if t:
                    righe.append(("- " if n == "ul" else f"{i}. ") + t)
            if righe:
                out.append("\n".join(righe))
        elif n == "details":
            s = c.find("summary")
            q = _inline(s).strip() if s else ""
            if s:
                s.extract()
            a = re.sub(r"\s+", " ", c.get_text(" ")).strip()
            if q:
                out.append(f"**{q}**\n\n{a}")
        elif n == "table":
            rows = [[_inline(td).strip().replace("|", "/") for td in tr.find_all(["th", "td"])] for tr in c.find_all("tr")]
            rows = [r for r in rows if r]
            if rows:
                w = max(len(r) for r in rows)
                rows = [r + [""] * (w - len(r)) for r in rows]
                out.append("\n".join(["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w] + ["| " + " | ".join(r) + " |" for r in rows[1:]]))
        elif n == "a" and c.get("href"):
            t = _inline(c).strip()
            if t:
                href = c["href"]
                out.append(f"[{t}]({BASE + href if href.startswith('/') else href})")
        elif n in ("blockquote",):
            out.append("> " + _inline(c).strip())
        else:
            _blocchi(c, out)


def pagina_md(slug, html_txt, oggi):
    soup = BeautifulSoup(html_txt, "lxml")
    title = soup.title.get_text().strip() if soup.title else slug
    desc = (soup.find("meta", attrs={"name": "description"}) or {}).get("content", "")
    main = soup.find("main") or soup.body
    out = []
    _blocchi(main, out)
    corpo = "\n\n".join(x for x in out if x.strip())
    corpo = re.sub(r"[ \t]+\n", "\n", corpo)
    corpo = re.sub(r"\n{3,}", "\n\n", corpo)
    testa = (
        f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\n"
        f"url: {url_di(slug)}\n"
        f"description: {json.dumps(desc, ensure_ascii=False)}\n"
        f"updated: {oggi}\n"
        "author: Avv. Daniela Pernorio, Studio Legale Pernorio, Vigevano (PV)\n---\n\n"
    )
    piede = (
        "\n\n---\n\nStudio Legale Pernorio · Avv. Daniela Pernorio · Via Egidio Sacchetti 14, 27029 Vigevano (PV) · "
        "Tel. +39 0381 386276 · WhatsApp +39 333 336 8757 · Lun–Ven 9:00–19:00 su appuntamento · "
        f"{BASE}/contatti\n\nIndicazioni generali: ogni caso va valutato sui documenti con l'avvocato.\n"
    )
    return testa + corpo + piede


# ---------------------------------------------------------------------------
# Grafo delle entità: ogni pagina dichiara chi è e a chi appartiene
# ---------------------------------------------------------------------------

TIPO_PAGINA = {
    "contatti": "ContactPage",
    "studio": "AboutPage",
    "guide": "CollectionPage",
    "attivita": "CollectionPage",
    "strumenti": "CollectionPage",
}


def nodo_pagina(slug, title, desc, oggi):
    """WebPage collegata al sito (#sito) e allo Studio (#studio), con data di modifica."""
    url = url_di(slug)
    n = {
        "@context": "https://schema.org",
        "@type": TIPO_PAGINA.get(slug, "WebPage"),
        "@id": url + "#pagina",
        "url": url,
        "name": title,
        "description": desc,
        "inLanguage": "it-IT",
        "isPartOf": {"@id": BASE + "/#sito"},
        "about": {"@id": BASE + "/#studio"},
        "publisher": {"@id": BASE + "/#studio"},
        "dateModified": oggi,
        "breadcrumb": {"@id": url + "#percorso"},
    }
    if slug.startswith(("guida-", "attivita-")) or slug in ("costi-avvocato",):
        n["author"] = {"@id": BASE + "/#avvocato"}
    return n


def nodo_servizio(slug, nome, url_pagina):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": url_pagina + "#servizio",
        "name": nome,
        "serviceType": nome,
        "url": url_pagina,
        "provider": {"@id": BASE + "/#studio"},
        "areaServed": [{"@type": "City", "name": c} for c in
                       ("Vigevano", "Mortara", "Gambolò", "Garlasco", "Cassolnovo", "Cilavegna", "Abbiategrasso")]
                      + [{"@type": "AdministrativeArea", "name": "Lomellina"}],
        "availableChannel": [
            {"@type": "ServiceChannel", "name": "In Studio a Vigevano", "serviceLocation": {"@id": BASE + "/#studio"}},
            {"@type": "ServiceChannel", "name": "Colloquio online", "serviceUrl": BASE + "/colloquio-online"},
        ],
    }


# ---------------------------------------------------------------------------
# WebMCP: strumenti per gli agenti IA nel browser
# ---------------------------------------------------------------------------

AGENTI_JS = r"""/* Studio Legale Pernorio · strumenti WebMCP per agenti IA nel browser.
   Spec: https://github.com/webmachinelearning/webmcp  ·  Nessun dato viene inviato senza il click della persona. */
(function(){
var mc=document.modelContext||navigator.modelContext;
if(!mc||typeof mc.registerTool!=='function')return;
var INDICE=null;
function indice(){if(INDICE)return Promise.resolve(INDICE);return fetch('/cerca.json').then(function(r){return r.json()}).then(function(j){INDICE=j;return j})}
function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
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
var STUDIO=__STUDIO__;
__IMPOSTA__
var tools=[
{name:'informazioni-studio',
 description:"Restituisce i dati dello Studio Legale Pernorio (Avv. Daniela Pernorio, avvocato civilista a Vigevano, Pavia): indirizzo, telefono, WhatsApp, email, orari, materie trattate, comuni serviti, tribunali, modalità del primo colloquio e del preventivo.",
 inputSchema:{type:'object',properties:{}},
 annotations:{readOnlyHint:true},
 execute:function(){return STUDIO}},
{name:'cerca-nel-sito',
 description:"Cerca tra le guide pratiche, le competenze, le pagine per comune e gli strumenti del sito dello Studio Legale Pernorio. Restituisce titolo, descrizione, indirizzo della pagina e della sua versione Markdown.",
 inputSchema:{type:'object',properties:{domanda:{type:'string',description:"Argomento o domanda in italiano, ad esempio 'separazione con figli' o 'multa autovelox'."}},required:['domanda']},
 annotations:{readOnlyHint:true},
 execute:function(a){var q=norm(a&&a.domanda).split(/\W+/).filter(function(w){return w.length>2});
  return indice().then(function(ix){return ix.map(function(p){var t=norm(p.t+' '+p.d+' '+p.k),s=0;q.forEach(function(w){if(t.indexOf(w)>=0)s+=norm(p.t).indexOf(w)>=0?3:1});return{p:p,s:s}})
   .filter(function(x){return x.s>0}).sort(function(a,b){return b.s-a.s}).slice(0,6).map(function(x){return{titolo:x.p.t,descrizione:x.p.d,url:x.p.u,markdown:x.p.m}})})}},
{name:'calcola-quote-eredita',
 description:"Calcola le quote di eredità in assenza di testamento (successione legittima, artt. 566-585 del codice civile italiano) in base a coniuge, figli, genitori e fratelli del defunto. Indicativo: non considera rappresentazione, ascendenti diversi dai genitori, fratelli unilaterali o testamenti.",
 inputSchema:{type:'object',properties:{
  coniuge:{type:'boolean',description:'Il defunto lascia un coniuge o unito civilmente.'},
  figli:{type:'integer',minimum:0,description:'Numero di figli.'},
  genitori:{type:'integer',minimum:0,maximum:2,description:'Genitori viventi (0-2), rilevano solo senza figli.'},
  fratelli:{type:'integer',minimum:0,description:'Fratelli e sorelle, rilevano solo senza figli.'},
  valore:{type:'number',minimum:0,description:"Valore dell'eredità in euro, facoltativo."}},required:['coniuge','figli']},
 annotations:{readOnlyHint:true},
 execute:function(a){var r=quote(!!a.coniuge,a.figli|0,a.genitori|0,a.fratelli|0),v=+a.valore||0;
  if(!r.length)return{quote:[],nota:"Senza coniuge, figli, genitori o fratelli l'eredità va agli altri parenti fino al sesto grado e poi allo Stato (artt. 572 e 586 c.c.)."};
  return{quote:r.map(function(x){var pc=x[1].n/x[1].d;var o={erede:x[0],persone:x[2],quota:x[1].n+'/'+x[1].d,percentuale:Math.round(pc*10000)/100};if(v)o.valore_euro=Math.round(v*pc);return o}),
   nota:'Calcolo indicativo. Strumento completo: '+location.origin+'/strumento-calcolo-quote-eredita . Per un parere: Studio Legale Pernorio, 0381 386276.'}}},
__IMPOSTA_TOOL__,
{name:'scadenze-multa',
 description:"Dato il giorno di notifica di una multa stradale italiana, calcola le scadenze: pagamento scontato del 30% (5 giorni), ricorso al Giudice di Pace (30 giorni), pagamento in misura ridotta e ricorso al Prefetto (60 giorni).",
 inputSchema:{type:'object',properties:{notifica:{type:'string',format:'date',description:'Data di notifica o contestazione, formato AAAA-MM-GG.'}},required:['notifica']},
 annotations:{readOnlyHint:true},
 execute:function(a){var p=String(a.notifica||'').split('-');if(p.length!==3)return{errore:'Data nel formato AAAA-MM-GG'};
  var d=new Date(+p[0],+p[1]-1,+p[2]);function z(n){return (n<10?'0':'')+n}function add(n){var x=new Date(d.getTime());x.setDate(x.getDate()+n);return x.getFullYear()+'-'+z(x.getMonth()+1)+'-'+z(x.getDate())}
  return{scadenze:[{cosa:'Pagamento con sconto del 30% (se previsto dal verbale)',entro:add(5)},{cosa:'Ricorso al Giudice di Pace',entro:add(30)},{cosa:'Pagamento in misura ridotta',entro:add(60)},{cosa:'Ricorso al Prefetto (gratuito, rischio raddoppio)',entro:add(60)}],
   nota:'Indicativo: i termini possono cambiare per notifiche via PEC, residenti all\'estero o verbali particolari. Guida: '+location.origin+'/guida-multa-autovelox-2026'}}},
{name:'prepara-richiesta-allo-studio',
 description:"Prepara una richiesta di contatto allo Studio Legale Pernorio compilando il modulo della pagina Contatti. Non invia nulla: la persona rilegge, accetta l'informativa privacy e preme Invia.",
 inputSchema:{type:'object',properties:{
  nome:{type:'string',description:'Nome e cognome.'},email:{type:'string',description:'Email per la risposta.'},
  telefono:{type:'string',description:'Telefono, facoltativo.'},messaggio:{type:'string',description:'Breve descrizione della questione legale, senza dati sensibili non necessari.'}},required:['nome','messaggio']},
 execute:function(a){try{sessionStorage.setItem('slp-bozza',JSON.stringify(a||{}))}catch(e){}
  if(!document.getElementById('cf')){location.href='/contatti#cf';return{stato:'Apro la pagina Contatti con il modulo precompilato: la persona deve rileggere, spuntare la privacy e premere Invia.'}}
  riempi();return{stato:'Modulo precompilato. La persona deve rileggere, spuntare la privacy e premere Invia.'}}}
];
function riempi(){var f=document.getElementById('cf');if(!f)return;var b;try{b=JSON.parse(sessionStorage.getItem('slp-bozza')||'null')}catch(e){}
 if(!b)return;['nome','email','telefono','messaggio'].forEach(function(k){if(b[k]&&f.elements[k])f.elements[k].value=b[k]});
 try{sessionStorage.removeItem('slp-bozza')}catch(e){}var p=f.elements.privacy;if(p)p.focus()}
riempi();
tools.forEach(function(t){try{var r=mc.registerTool(t);if(r&&r.catch)r.catch(function(){})}catch(e){}});
})();
"""


def agenti_js(studio):
    return (AGENTI_JS.replace("__STUDIO__", json.dumps(studio, ensure_ascii=False))
            .replace("__IMPOSTA_TOOL__", IMPOSTA_TOOL_JS).replace("__IMPOSTA__", CALC_IMPOSTA_JS))


def modulo_webmcp(s):
    """Attributi WebMCP dichiarativi sul modulo contatti (senza invio automatico)."""
    s = s.replace("<form action='/grazie' class='cf' id='cf' method='POST' name='contatti'",
                  "<form action='/grazie' class='cf' id='cf' method='POST' name='contatti' toolname='richiesta-contatto-studio' "
                  "tooldescription=\"Invia una richiesta di primo contatto allo Studio Legale Pernorio di Vigevano. La persona deve accettare l'informativa privacy.\"", 1)
    for nome, d in (("nome", "Nome e cognome di chi scrive"), ("email", "Email per la risposta"),
                    ("telefono", "Telefono, facoltativo"), ("messaggio", "Breve descrizione della questione legale")):
        s = re.sub(rf'(<(?:input|textarea) id="cf-[a-z]+" name="{nome}")', rf'\1 toolparamdescription="{d}"', s, count=1)
    return s


ROBOTS = """# Studio Legale Pernorio · politica per motori di ricerca e assistenti IA
# Content-Signal: search = risultati e citazioni, ai-input = risposte IA in tempo reale, ai-train = addestramento
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

User-agent: Googlebot
User-agent: Bingbot
User-agent: Applebot
User-agent: DuckDuckBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: ClaudeBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: DuckAssistBot
User-agent: meta-externalagent
User-agent: Amazonbot
User-agent: MistralAI-User
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

Sitemap: https://studiolegalepernorio.com/sitemap.xml
"""


# ---------------------------------------------------------------------------
# Calcolo dell'imposta di successione (D.Lgs. 346/1990, art. 7; artt. 10 e 13
# per le imposte ipotecaria e catastale). Stesse regole per pagina, WebMCP e MCP.
# ---------------------------------------------------------------------------

CALC_IMPOSTA_JS = r"""function impostaSuccessione(a){
 var R={coniuge:{n:'Coniuge, unito civilmente o parente in linea retta (figli, genitori, nipoti in linea retta)',al:0.04,fr:1000000},
  fratello:{n:'Fratello o sorella',al:0.06,fr:100000},
  parente:{n:'Altro parente fino al 4° grado o affine (linea retta, o collaterale fino al 3° grado)',al:0.06,fr:0},
  altri:{n:'Altra persona',al:0.08,fr:0}};
 var r=R[a.rapporto]||R.altri,q=Math.max(0,+a.quota||0),fr=a.disabile?1500000:r.fr,base=Math.max(0,q-fr),imp=Math.round(base*r.al);
 var im=Math.max(0,+a.immobili||0),ipo=0,cat=0;
 if(im>0){if(a.primaCasa){ipo=200;cat=200}else{ipo=Math.max(200,Math.round(im*0.02));cat=Math.max(200,Math.round(im*0.01))}}
 return{erede:r.n,quota_euro:q,franchigia_euro:fr,base_imponibile_euro:base,aliquota_percento:r.al*100,imposta_successione_euro:imp,
  imposte_ipotecaria_catastale:im>0?{ipotecaria_euro:ipo,catastale_euro:cat,nota:a.primaCasa?'Agevolazione prima casa: imposte fisse di 200 euro ciascuna.':'2% e 1% del valore catastale, minimo 200 euro ciascuna. Si pagano una volta per immobile, non per ogni erede.'}:null,
  nota:'Calcolo indicativo (D.Lgs. 346/1990). Non considera passività deducibili, donazioni precedenti, beni esenti (es. titoli di Stato), bollo, tributi speciali e tassa ipotecaria.'}}"""


IMPOSTA_TOOL_JS = r"""{name:'calcola-imposta-successione',
 description:"Calcola l'imposta di successione italiana dovuta da un erede (aliquote 4%, 6%, 8% e franchigie da 1.000.000 o 100.000 euro, 1.500.000 per persone con disabilità grave) e le imposte ipotecaria e catastale sugli immobili, anche con agevolazione prima casa.",
 inputSchema:{type:'object',properties:{
  quota:{type:'number',minimum:0,description:"Valore in euro della quota ricevuta dall'erede."},
  rapporto:{type:'string',enum:['coniuge','fratello','parente','altri'],description:"coniuge = coniuge, unito civilmente o parente in linea retta; fratello = fratello o sorella; parente = altri parenti fino al 4° grado e affini; altri = nessun legame."},
  disabile:{type:'boolean',description:"Erede con disabilità grave (legge 104/1992)."},
  immobili:{type:'number',minimum:0,description:"Valore catastale complessivo degli immobili dell'eredità, facoltativo."},
  primaCasa:{type:'boolean',description:"Si chiede l'agevolazione prima casa."}},required:['quota','rapporto']},
 annotations:{readOnlyHint:true},
 execute:function(a){return impostaSuccessione(a||{})}}"""


# ---------------------------------------------------------------------------
# Server MCP pubblico (Model Context Protocol, trasporto Streamable HTTP senza
# sessione) come Netlify Function su /mcp. Permette di aggiungere lo Studio come
# "connettore" in ChatGPT, Claude e negli altri client MCP. Solo lettura: non
# riceve dati personali e non invia nulla allo Studio.
# ---------------------------------------------------------------------------

MCP_JS = r"""// Generato da tools/build.py: non modificare a mano.
const STUDIO = __STUDIO__;
const INDICE = __INDICE__;
const VERSIONI = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"];
__QUOTE__
__IMPOSTA__
function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function z(n){return (n<10?'0':'')+n}
const TOOLS = [
 {name:'informazioni_studio',title:'Informazioni sullo Studio Legale Pernorio',
  description:"Dati dello Studio Legale Pernorio, Avv. Daniela Pernorio, avvocato civilista a Vigevano (Pavia, Lombardia): indirizzo, telefono, WhatsApp, orari, materie, comuni serviti, tribunali, primo colloquio e preventivo.",
  inputSchema:{type:'object',properties:{}},annotations:{readOnlyHint:true,openWorldHint:false},
  run:()=>STUDIO},
 {name:'cerca_nel_sito',title:'Cerca nelle guide dello Studio',
  description:"Cerca tra guide legali pratiche, competenze, pagine per comune (Vigevano, Mortara, Gambolò, Garlasco, Cassolnovo, Cilavegna, Abbiategrasso, Lomellina) e strumenti dello Studio Legale Pernorio. Restituisce titolo, descrizione e URL.",
  inputSchema:{type:'object',properties:{domanda:{type:'string',description:"Argomento in italiano, es. 'affidamento figli' o 'sfratto per morosità'."}},required:['domanda']},
  annotations:{readOnlyHint:true,openWorldHint:false},
  run:(a)=>{const q=norm(a.domanda).split(/\W+/).filter(w=>w.length>2);
   return INDICE.map(p=>{const t=norm(p.t+' '+p.d+' '+p.k);let s=0;q.forEach(w=>{if(t.includes(w))s+=norm(p.t).includes(w)?3:1});return{p,s}})
    .filter(x=>x.s>0).sort((a,b)=>b.s-a.s).slice(0,8).map(x=>({titolo:x.p.t,descrizione:x.p.d,url:x.p.u,markdown:x.p.m}))}},
 {name:'leggi_pagina',title:'Leggi una pagina del sito',
  description:"Restituisce il testo completo in Markdown di una pagina del sito dello Studio Legale Pernorio, dato il suo URL o il suo nome (es. 'guida-divorzio-tempi').",
  inputSchema:{type:'object',properties:{pagina:{type:'string',description:"URL o nome della pagina, ottenuto da cerca_nel_sito."}},required:['pagina']},
  annotations:{readOnlyHint:true,openWorldHint:false},
  run:async(a,origin)=>{let p=String(a.pagina||'').replace(/^https?:\/\/[^/]+/,'').replace(/^\/+|\.md$|\.html$/g,'')||'index';
   if(!INDICE.some(x=>x.m.endsWith('/'+p+'.md')))return{errore:'Pagina non trovata. Usare cerca_nel_sito.'};
   const r=await fetch(origin+'/'+p+'.md');return{url:'__BASE__/'+(p==='index'?'':p),testo:await r.text()}}},
 {name:'calcola_quote_eredita',title:'Quote di eredità senza testamento',
  description:"Quote di eredità nella successione legittima italiana (artt. 565-586 codice civile) tra coniuge, figli, genitori e fratelli. Indicativo.",
  inputSchema:{type:'object',properties:{coniuge:{type:'boolean'},figli:{type:'integer',minimum:0},genitori:{type:'integer',minimum:0,maximum:2},fratelli:{type:'integer',minimum:0},valore:{type:'number',minimum:0,description:'Valore in euro, facoltativo'}},required:['coniuge','figli']},
  annotations:{readOnlyHint:true,openWorldHint:false},
  run:(a)=>{const r=quote(!!a.coniuge,a.figli|0,a.genitori|0,a.fratelli|0),v=+a.valore||0;
   if(!r.length)return{quote:[],nota:"Senza coniuge, figli, genitori o fratelli ereditano gli altri parenti fino al sesto grado e poi lo Stato."};
   return{quote:r.map(x=>{const pc=x[1].n/x[1].d,o={erede:x[0],persone:x[2],quota:x[1].n+'/'+x[1].d,percentuale:Math.round(pc*1e4)/100};if(v)o.valore_euro=Math.round(v*pc);return o}),
    nota:'Indicativo. Per un parere: Studio Legale Pernorio, Vigevano, tel. 0381 386276.'}}},
 {name:'calcola_imposta_successione',title:'Imposta di successione',
  description:"Imposta di successione italiana per un erede (franchigie 1.000.000 / 100.000 / 1.500.000 euro, aliquote 4-6-8%) e imposte ipotecaria e catastale, anche con prima casa.",
  inputSchema:{type:'object',properties:{quota:{type:'number',minimum:0},rapporto:{type:'string',enum:['coniuge','fratello','parente','altri']},disabile:{type:'boolean'},immobili:{type:'number',minimum:0},primaCasa:{type:'boolean'}},required:['quota','rapporto']},
  annotations:{readOnlyHint:true,openWorldHint:false},
  run:(a)=>impostaSuccessione(a)},
 {name:'scadenze_multa',title:'Scadenze di una multa stradale',
  description:"Dalla data di notifica di una multa stradale italiana: scadenze per lo sconto del 30% (5 giorni), il ricorso al Giudice di Pace (30), il pagamento ridotto e il ricorso al Prefetto (60).",
  inputSchema:{type:'object',properties:{notifica:{type:'string',description:'Data AAAA-MM-GG'}},required:['notifica']},
  annotations:{readOnlyHint:true,openWorldHint:false},
  run:(a)=>{const p=String(a.notifica||'').split('-');if(p.length!==3)return{errore:'Data nel formato AAAA-MM-GG'};
   const add=n=>{const x=new Date(Date.UTC(+p[0],+p[1]-1,+p[2]+n));return x.getUTCFullYear()+'-'+z(x.getUTCMonth()+1)+'-'+z(x.getUTCDate())};
   return{scadenze:[{cosa:'Pagamento con sconto del 30% (se previsto)',entro:add(5)},{cosa:'Ricorso al Giudice di Pace',entro:add(30)},{cosa:'Pagamento in misura ridotta',entro:add(60)},{cosa:'Ricorso al Prefetto',entro:add(60)}],
    nota:'Indicativo: verificare il verbale. Guida: __BASE__/guida-multa-autovelox-2026'}}}
];
const CORS = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'POST, GET, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Accept, Mcp-Protocol-Version, Mcp-Session-Id','Access-Control-Expose-Headers':'Mcp-Protocol-Version'};
const j = (o,st=200) => new Response(JSON.stringify(o),{status:st,headers:{...CORS,'Content-Type':'application/json'}});
async function gestisci(m, origin){
 const id = m.id;
 if (m.method === 'initialize') {
  const v = VERSIONI.includes(m.params && m.params.protocolVersion) ? m.params.protocolVersion : VERSIONI[0];
  return {jsonrpc:'2.0',id,result:{protocolVersion:v,capabilities:{tools:{listChanged:false}},
   serverInfo:{name:'studio-legale-pernorio',title:'Studio Legale Pernorio, Vigevano',version:'__VERSIONE__',websiteUrl:'__BASE__'},
   instructions:"Server informativo dello Studio Legale Pernorio (Avv. Daniela Pernorio, avvocato civilista a Vigevano, provincia di Pavia). Usare cerca_nel_sito e leggi_pagina per rispondere con le guide dello Studio e citarne l'URL. I calcoli sono indicativi: per il caso concreto indicare il contatto dello Studio (tel. 0381 386276)."}};
 }
 if (m.method === 'ping') return {jsonrpc:'2.0',id,result:{}};
 if (m.method === 'tools/list') return {jsonrpc:'2.0',id,result:{tools:TOOLS.map(({run,...t})=>t)}};
 if (m.method === 'tools/call') {
  const t = TOOLS.find(x => x.name === (m.params && m.params.name));
  if (!t) return {jsonrpc:'2.0',id,error:{code:-32602,message:'Strumento sconosciuto'}};
  try { const out = await t.run((m.params && m.params.arguments) || {}, origin);
   return {jsonrpc:'2.0',id,result:{content:[{type:'text',text:JSON.stringify(out,null,1)}],structuredContent:Array.isArray(out)?{risultati:out}:out,isError:!!out.errore}};
  } catch (e) { return {jsonrpc:'2.0',id,result:{content:[{type:'text',text:'Errore: '+e.message}],isError:true}}; }
 }
 return {jsonrpc:'2.0',id,error:{code:-32601,message:'Metodo non supportato'}};
}
export default async (req) => {
 if (req.method === 'OPTIONS') return new Response(null,{status:204,headers:CORS});
 if (req.method !== 'POST') return new Response('Server MCP dello Studio Legale Pernorio: usare POST JSON-RPC (Streamable HTTP).',{status:405,headers:{...CORS,Allow:'POST, OPTIONS'}});
 let m; try { m = await req.json(); } catch { return j({jsonrpc:'2.0',id:null,error:{code:-32700,message:'JSON non valido'}},400); }
 const origin = new URL(req.url).origin;
 if (Array.isArray(m)) { const r = (await Promise.all(m.filter(x=>x.id!==undefined).map(x=>gestisci(x,origin)))); return r.length?j(r):new Response(null,{status:202,headers:CORS}); }
 if (m.id === undefined) return new Response(null,{status:202,headers:CORS});
 return j(await gestisci(m, origin));
};
export const config = { path: '/mcp' };
"""

QUOTE_JS = r"""function g(a,b){while(b){var t=b;b=a%b;a=t}return a}
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
 r.push([p===1?'Genitore':'Ciascun genitore',div(gt,p),p]); r.push([s===1?'Fratello o sorella':'Ciascun fratello o sorella',div(sub(F(1,1),gt),s),s]); return r;}"""


def mcp_function(studio, indice, versione):
    return (MCP_JS.replace("__STUDIO__", json.dumps(studio, ensure_ascii=False))
            .replace("__INDICE__", json.dumps(indice, ensure_ascii=False))
            .replace("__QUOTE__", QUOTE_JS).replace("__IMPOSTA__", CALC_IMPOSTA_JS)
            .replace("__BASE__", BASE).replace("__VERSIONE__", versione))


def server_card(versione):
    """Scheda di scoperta del server MCP (proposta SEP-1649, /.well-known/mcp/server-card.json)."""
    return {
        "$schema": "https://static.modelcontextprotocol.io/schemas/mcp-server-card/v1.json",
        "name": "it.studiolegalepernorio/sito",
        "title": "Studio Legale Pernorio, Vigevano",
        "description": "Guide legali pratiche, calcolo quote di eredità e imposta di successione, scadenze delle multe e contatti dello Studio Legale Pernorio, avvocato civilista a Vigevano (Pavia).",
        "version": versione,
        "websiteUrl": BASE,
        "remotes": [{"type": "streamable-http", "url": BASE + "/mcp"}],
        "capabilities": {"tools": {"listChanged": False}},
        "authentication": {"required": False},
        "tools": ["informazioni_studio", "cerca_nel_sito", "leggi_pagina", "calcola_quote_eredita",
                  "calcola_imposta_successione", "scadenze_multa"],
    }
