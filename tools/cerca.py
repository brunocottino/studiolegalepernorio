# -*- coding: utf-8 -*-
"""Ricerca sul testo completo del sito, uguale per persone e assistenti IA.

Un solo indice (/cerca-testo.json) e un solo motore (MOTORE_JS) usati da:
- la pagina /cerca del sito (file /cerca.js);
- l'API pubblica /api/cerca?q=... (Netlify Function, JSON o Markdown);
- il server MCP (/mcp): cerca_nel_sito, search e fetch;
- lo strumento WebMCP cerca-nel-sito (che chiama l'API).

L'indice è fatto di passaggi: ogni sezione (h2) e ogni domanda frequente è un
risultato a sé, con il suo testo e il collegamento al punto esatto della pagina.
Così chi cerca "padrone di casa non restituisce la caparra" arriva al paragrafo
giusto, e un assistente IA riceve già la risposta con l'URL da citare.
"""
import json
import re
import unicodedata

BASE = "https://studiolegalepernorio.com"

# Titoli di sezione che non sono contenuto (riquadri ripetuti su ogni pagina)
SEZIONI_ESCLUSE = {"parliamo della sua questione.", "fonti normative", "guide correlate", "altre guide"}
RIGHE_ESCLUSE = {"il suo caso", "altre guide", "ne vuole parlare?", "dove riceviamo clienti", "su appuntamento",
                 "domande frequenti", "come lavora lo studio"}
INIZI_ESCLUSI = ("oppure chiami lo", "a cura dello studio", "indicazioni generali", "primo colloquio in studio",
                 "[competenza**", "[strumento gratuito**", "guida · ", "[guida**")

# Pagine indice o di servizio: nella ricerca compaiono solo con titolo e descrizione
SOLO_TITOLO = {"guide", "strumenti", "attivita", "privacy", "cookie"}

# Parole di tutti i giorni e termini giuridici equivalenti: chi cerca "alimenti"
# trova "mantenimento", chi cerca "padrone di casa" trova "locatore".
SINONIMI = [
    ["affitto", "locazione", "pigione", "canone"],
    ["inquilino", "conduttore", "affittuario"],
    ["padrone", "proprietario", "locatore"],
    ["caparra", "cauzione", "deposito"],
    ["alimenti", "mantenimento"],
    ["eredita", "successione", "erede", "ereditare", "lascito"],
    ["multa", "verbale", "sanzione", "contravvenzione"],
    ["autovelox", "velocita", "tutor"],
    ["licenziamento", "licenziato", "licenziare"],
    ["incidente", "sinistro", "tamponamento"],
    ["costo", "prezzo", "tariffa", "parcella", "onorario", "compenso", "preventivo", "spesa", "pagare"],
    ["banca", "finanziaria", "prestito", "finanziamento", "mutuo"],
    ["debito", "insoluto", "rata", "arretrato"],
    ["convivente", "convivenza", "compagno", "compagna"],
    ["marito", "moglie", "coniuge"],
    ["figlio", "minore", "bambino"],
    ["anziano", "fragile", "demenza", "alzheimer", "incapace", "sostegno", "badante", "tutore"],
    ["sfratto", "sfrattare", "morosita", "moroso"],
    ["avvocato", "legale"],
    ["casa", "immobile", "abitazione", "appartamento"],
    ["vicino", "confinante", "confine"],
    ["soldi", "denaro", "somma", "credito"],
    ["lasciarsi", "separazione", "separarsi"],
    ["stipendio", "busta", "retribuzione", "salario"],
    ["tempo", "durata", "termine", "mese", "scadenza"],
    ["online", "videochiamata", "distanza"],
    ["gratis", "gratuito"],
    ["assicurazione", "risarcimento", "danno"],
    ["assemblea", "delibera", "condominio", "amministratore"],
    ["pignoramento", "pignorare", "esecuzione"],
    ["testamento", "olografo", "legittima"],
    ["affidamento", "collocamento", "visita"],
    ["orario", "apertura", "appuntamento", "contatti", "telefono", "indirizzo", "ricevimento"],
    ["sciogliere", "scioglimento"],
]

STOP = ("a ad al allo ai agli alla alle anche avere c che chi ci cio come con cosa cui da dal dallo dai dagli dalla dalle "
        "de dei del dello degli della delle di e ed essere fa fare ha hanno ho i il in io l la le lei lo loro lui ma me mi mia "
        "mio ne nei nel nello negli nella nelle no noi non o od per piu po puo quale quali quando quanto quella quelle "
        "quelli quello questa queste questi questo se sei si sia sono su sua sue sui sul sullo sugli sulla sulle suo suoi "
        "ti tra tu tua tuo un una uno va vi voi vorrei devo posso serve bisogna").split()


def _piano(t):
    """Markdown -> testo semplice."""
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("**", "").replace("→", " ")
    t = re.sub(r"(?m)^\s*(?:[-*]|\d+\.)\s+", "", t)
    t = re.sub(r"(?m)^\|[-| ]+\|$", "", t).replace("|", " ")
    return re.sub(r"\s+", " ", t).strip()


def ancora(testo):
    """Identificativo di una sezione (id dell'h2), uguale in HTML e nell'indice."""
    t = unicodedata.normalize("NFD", _piano(testo).lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60].strip("-")


def tipo_di(slug):
    if slug.startswith("guida-"):
        return "Guida"
    if slug.startswith("attivita-") or slug in ("diritto-di-famiglia", "domiciliazioni"):
        return "Competenza"
    if slug.startswith("avvocato-"):
        return "Zona"
    if slug.startswith("strumento-"):
        return "Strumento"
    if slug == "domande":
        return "Domande"
    return "Studio"


def passaggi(md):
    """Divide il Markdown di una pagina in passaggi: [titolo sezione, ancora, testo, è_faq]."""
    corpo = md.split("---", 2)[2] if md.startswith("---") else md
    corpo = corpo.rsplit("\n---\n", 1)[0]
    out, sez, anc, buf, salta = [], "", "", [], False

    def chiudi():
        testo = " ".join(buf).strip()
        del buf[:]
        if len(testo) < 60:
            return
        # sezioni lunghe: pezzi da circa 900 caratteri, tagliati a fine frase
        while len(testo) > 1300:
            i = testo.rfind(". ", 500, 950)
            i = i + 1 if i > 0 else 900
            out.append([sez, anc, testo[:i].strip(), 0])
            testo = testo[i:].strip()
        out.append([sez, anc, testo, 0])

    blocchi = [b.strip() for b in corpo.split("\n\n") if b.strip()]
    i = 0
    while i < len(blocchi):
        b = blocchi[i]
        i += 1
        m = re.match(r"^(#{1,2}) (.+)$", b)
        if m:
            chiudi()
            titolo = _piano(m.group(2))
            salta = titolo.lower() in SEZIONI_ESCLUSE
            sez, anc = ("", "") if m.group(1) == "#" else (titolo, ancora(titolo))
            continue
        if salta:
            continue
        low = b.lower()
        if low in RIGHE_ESCLUSE or low.startswith(INIZI_ESCLUSI):
            continue
        faq = re.match(r"^\*\*(.+?\?)\*\*\s*(.*)$", b, re.S)
        if faq and (faq.group(2).strip() or i < len(blocchi)):
            risposta = faq.group(2).strip()
            if not risposta:
                risposta = blocchi[i]
                i += 1
            out.append([_piano(faq.group(1)), anc, _piano(risposta), 1])
            continue
        if b.startswith("### "):
            b = b[4:] + "."
        t = _piano(b)
        if t:
            buf.append(t)
    chiudi()
    return out


def indice(pagine_md, meta):
    """pagine_md: {slug: markdown}; meta: {slug: (titolo, descrizione)} -> indice compatto."""
    docs, pas = [], []
    for slug in pagine_md:
        t, d = meta[slug]
        url = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
        docs.append([url, re.sub(r"\s*·.*$", "", t), d, tipo_di(slug)])
        if slug in SOLO_TITOLO:
            pas.append([len(docs) - 1, "", "", d, 0])
            continue
        for sez, anc, testo, faq in passaggi(pagine_md[slug]):
            pas.append([len(docs) - 1, sez, anc, testo, faq])
    return {"d": docs, "p": pas}


# ---------------------------------------------------------------------------
# Motore di ricerca (JavaScript, lo stesso codice nel browser e nelle funzioni)
# BM25 sui passaggi, radici delle parole italiane, sinonimi, peso al titolo.
# ---------------------------------------------------------------------------

MOTORE_JS = r"""function creaMotore(IX){
 var STOP={},SIN={},P=[],DF={},N=IX.p.length,media=0;
 __STOP__.forEach(function(w){STOP[w]=1});
 function norm(s){return String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
 function radice(w){if(/^\d+$/.test(w))return w;if(w.length>4)w=w.replace(/[aeiou]+$/,'');w=w.replace(/([cg])h$/,'$1');return w.slice(0,6)}
 function parole(s){return norm(s).split(/[^a-z0-9]+/).filter(function(w){return w.length>1&&!STOP[w]}).map(radice)}
 __SIN__.forEach(function(g){var r=g.map(radice);r.forEach(function(a){SIN[a]=SIN[a]||{};r.forEach(function(b){if(a!==b)SIN[a][b]=1})})});
 function conta(tf,lista,peso){lista.forEach(function(w){tf[w]=(tf[w]||0)+peso})}
 var TD=IX.d.map(function(d){return{t:parole(d[1]),d:parole(d[2])}});
 IX.p.forEach(function(p,i){var tf={},tx=parole(p[3]);conta(tf,tx,1);conta(tf,parole(p[1]),p[4]?2:3);conta(tf,TD[p[0]].t,2);conta(tf,TD[p[0]].d,.5);
  P[i]={tf:tf,n:tx.length+8};media+=P[i].n;for(var w in tf)DF[w]=(DF[w]||0)+1});
 media=media/(N||1);
 var PRIORE={Guida:1.12,Competenza:1.1,Domande:1.05,Strumento:1.05,Zona:.75,Studio:1};
 function idf(w){var n=DF[w]||0;return Math.log(1+(N-n+.5)/(n+.5))}
 function estratto(testo,q){if(testo.length<=300)return testo;var fr=testo.replace(/([.!?])\s+(?=[A-ZÀ-Ý«"])/g,'$1\n').split('\n'),best=0,bs=-1;
  fr.forEach(function(f,i){var s=0,ws=parole(f);q.forEach(function(w){if(ws.indexOf(w)>=0)s++});if(s>bs){bs=s;best=i}});
  var o=fr[best].trim(),k=best+1;while(k<fr.length&&(o+' '+fr[k]).length<300){o+=' '+fr[k].trim();k++}
  if(o.length>320)o=o.slice(0,300).replace(/\s+\S*$/,'')+'…';return(best>0?'… ':'')+o}
 function cerca(domanda,n,perPagina,soglia){var q=[],visti={};parole(domanda).forEach(function(w){if(!visti[w]){visti[w]=1;q.push(w)}});
  if(!q.length)return[];var frase=norm(domanda).replace(/[^a-z0-9]+/g,' ').trim(),ris=[];
  for(var i=0;i<N;i++){var p=P[i],s=0,trovate=0;
   for(var j=0;j<q.length;j++){var w=q[j],f=p.tf[w]||0,peso=1,best=0;
    if(f)best=idf(w)*f*2.2/(f+1.2*(.65+.35*p.n/media));
    for(var x in SIN[w]||{}){var g=p.tf[x]||0;if(g){var v=.55*idf(x)*g*2.2/(g+1.2*(.65+.35*p.n/media));if(v>best)best=v}}
    if(best){s+=best*peso;trovate++}}
   if(!s||(q.length>2&&trovate*2<q.length))continue;s*=Math.pow(trovate/q.length,1.6);
   var r=IX.p[i],d=IX.d[r[0]];
   if(q.length>1&&norm(r[1]+' '+r[3]).replace(/[^a-z0-9]+/g,' ').indexOf(frase)>=0)s*=1.5;
   var tt=TD[r[0]].t,nt=0;q.forEach(function(w){if(tt.indexOf(w)>=0)nt++;else for(var y in SIN[w]||{})if(tt.indexOf(y)>=0){nt+=.8;break}});if(nt>=q.length-.45)s*=1.6;else if(q.length>2&&nt>=q.length-1.2)s*=1.2;
   s*=PRIORE[d[3]]||1;
   ris.push({i:i,s:s})}
  ris.sort(function(a,b){return b.s-a.s});
  var out=[],perDoc={},testi={},max=perPagina||2;n=n||8;
  for(var k=0;k<ris.length&&out.length<n;k++){var r2=IX.p[ris[k].i],d2=IX.d[r2[0]];
   if(ris[k].s<ris[0].s*(soglia||.28))break;
   if(testi[r2[3]])continue;testi[r2[3]]=1;
   perDoc[r2[0]]=(perDoc[r2[0]]||0)+1;if(perDoc[r2[0]]>max)continue;
   out.push({titolo:d2[1],tipo:d2[3],sezione:r2[1]||'',domanda_frequente:!!r2[4],estratto:estratto(r2[3],q),testo:r2[3],
    url:d2[0]+(r2[2]?'#'+r2[2]:''),pagina:d2[0],markdown:(d2[0].slice(-1)==='/'?d2[0]+'index':d2[0])+'.md',punteggio:Math.round(ris[k].s*100)/100})}
  return out}
 cerca.radici=function(s){return parole(s)};cerca.radice=function(w){return radice(norm(w))};
 return cerca}"""


def motore_js():
    return (MOTORE_JS.replace("__STOP__", json.dumps(STOP)).replace("__SIN__", json.dumps(SINONIMI)))


# ---------------------------------------------------------------------------
# Pagina /cerca del sito
# ---------------------------------------------------------------------------

ESEMPI = ["quanto costa separarsi", "il padrone di casa non restituisce la caparra", "eredità con debiti",
          "multa autovelox ricorso", "assegno per i figli", "pignoramento dello stipendio", "licenziamento",
          "colloquio online"]

ICO_LENTE = ('<svg class="ico" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
             '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>')


def modulo(valore="", autofocus=False, ident="cerca-q"):
    """Casella di ricerca: funziona anche senza JavaScript (porta a /cerca?q=...)."""
    return (f'<form class="cerca-f" action="/cerca" method="get" role="search">'
            f'<label class="sr" for="{ident}">Cerca nel sito</label>'
            f'<input id="{ident}" name="q" type="search" placeholder="Es. eredità con debiti" '
            f'autocomplete="off" enterkeyhint="search" maxlength="120" value="{valore}"{" autofocus" if autofocus else ""}>'
            f'<button class="btn btn-primary" type="submit" aria-label="Cerca">{ICO_LENTE}<span>Cerca</span></button></form>')


def corpo_pagina():
    chips = "".join(f"<a href='/cerca?q={e.replace(' ', '+')}'>{e}</a>" for e in ESEMPI)
    return (modulo(autofocus=True)
            + '<p class="cerca-stato" id="cerca-stato" role="status" aria-live="polite"></p>'
            + '<div id="cerca-r" class="cerca-r"></div>'
            + f'<div id="cerca-esempi" class="cerca-esempi"><span class="label">Ricerche frequenti</span><div class="cerca-chips">{chips}</div></div>'
            + '<noscript><p>Per cercare serve JavaScript. In alternativa può consultare le <a href="/guide">guide</a>, '
              'le <a href="/domande">domande frequenti</a> o le <a href="/attivita">competenze</a>.</p></noscript>')


PAGINA_JS = r"""/* Studio Legale Pernorio · ricerca nel sito. Tutto avviene nel browser: la domanda non viene inviata né registrata. */
__MOTORE__
(function(){
var f=document.querySelector('main form.cerca-f'),q=document.getElementById('cerca-q'),out=document.getElementById('cerca-r'),
 stato=document.getElementById('cerca-stato'),esempi=document.getElementById('cerca-esempi');
if(!f||!out||!q)return;
var motore=null,attesa=null,t=null;
function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
function evidenzia(nodo,testo,rad){testo.split(/([A-Za-zÀ-ÿ0-9]+)/).forEach(function(pz,i){
 if(i%2&&pz.length>1&&rad.indexOf(motore.radice(pz))>=0)nodo.appendChild(el('mark',null,pz));else nodo.appendChild(document.createTextNode(pz))})}
function carica(){if(motore)return Promise.resolve();if(!attesa)attesa=fetch('/cerca-testo.json').then(function(r){return r.json()}).then(function(ix){motore=creaMotore(ix)});return attesa}
function mostra(){var d=q.value.trim();
 try{history.replaceState(null,'',d?'/cerca?q='+encodeURIComponent(d).replace(/%20/g,'+'):'/cerca')}catch(e){}
 if(d.length<2){out.textContent='';stato.textContent='';esempi.hidden=false;return}
 carica().then(function(){var r=motore(d,10),rad=motore.radici(d);out.textContent='';esempi.hidden=r.length>0;
  if(!r.length){stato.textContent='Nessun risultato per questa ricerca. Provi con altre parole, oppure ci scriva o ci chiami: 0381 386276.';
   var a=el('div','actions');var c=el('a','btn btn-primary','Chiama lo Studio');c.href='tel:+390381386276';var s=el('a','btn btn-ghost','Scriva la sua domanda');s.href='/contatti#scrivi';a.appendChild(c);a.appendChild(s);out.appendChild(a);return}
  stato.textContent=r.length===1?'1 risultato':r.length+' risultati';
  r.forEach(function(x){var a=el('a','card ris');a.href=x.url.replace(/^https?:\/\/[^/]+/,'');
   a.appendChild(el('span','label',x.domanda_frequente?x.tipo+' · Domanda frequente':x.tipo));
   var h=el('h2');evidenzia(h,x.domanda_frequente?x.sezione:x.titolo,rad);a.appendChild(h);
   if(x.sezione&&!x.domanda_frequente)a.appendChild(el('p','ris-sez',x.sezione));
   var p=el('p','ris-txt');evidenzia(p,x.estratto,rad);a.appendChild(p);
   if(x.domanda_frequente)a.appendChild(el('p','ris-sez','Da: '+x.titolo));
   out.appendChild(a)})}).catch(function(){stato.textContent='La ricerca non è disponibile in questo momento. Può chiamarci allo 0381 386276.'})}
f.addEventListener('submit',function(e){e.preventDefault();mostra();q.blur()});
q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(mostra,180)});
q.addEventListener('focus',carica);
var iniziale=new URLSearchParams(location.search).get('q');if(iniziale){q.value=iniziale;mostra()}
})();
"""


def pagina_js():
    return PAGINA_JS.replace("__MOTORE__", motore_js())


CSS = """
/* --- ricerca nel sito --- */
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.cerca-f{display:flex;gap:10px;align-items:stretch;margin:6px 0 4px;max-width:720px}
.cerca-f input{flex:1;min-width:0;font:inherit;padding:14px 18px;border:1px solid color-mix(in srgb,var(--ink) 24%,transparent);border-radius:999px;background:var(--card,var(--paper));color:var(--ink);min-height:52px;box-sizing:border-box}
.cerca-f input:focus-visible{outline:2px solid var(--forest);outline-offset:2px}
.cerca-f .btn{flex:none;gap:8px}
@media (max-width:520px){.cerca-f .btn span{display:none}.cerca-f .btn{padding-inline:18px}.cerca-f input{font-size:16px}}
.phero .cerca-f{margin-top:22px}
.cerca-stato{margin:18px 0 0;font-size:.9rem;color:var(--graphite);min-height:1.4em}
.cerca-r{display:grid;gap:12px;margin-top:10px}
.cerca-r .ris{display:block;padding:20px 22px;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}
.cerca-r .ris:hover{transform:translateY(-2px)}
.cerca-r .ris h2{font-size:1.35rem;line-height:1.25;margin:6px 0 4px}
.cerca-r .ris-sez{margin:0 0 6px;font-size:.82rem;letter-spacing:.04em;color:var(--graphite)}
.cerca-r .ris-txt{margin:0 0 4px;font-size:.95rem;line-height:1.6}
.cerca-r mark{background:color-mix(in srgb,var(--brass) 30%,transparent);color:inherit;border-radius:3px;padding:0 2px}
.cerca-r .actions{margin-top:6px}
.cerca-esempi{margin-top:26px}
.cerca-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.cerca-chips a{padding:9px 16px;border-radius:999px;border:1px solid color-mix(in srgb,var(--ink) 18%,transparent);font-size:.9rem;text-decoration:none}
.cerca-chips a:hover{border-color:var(--ink)}
:target{scroll-margin-top:96px}
"""


# ---------------------------------------------------------------------------
# API pubblica /api/cerca (Netlify Function): per assistenti IA e GPT personalizzati
# ---------------------------------------------------------------------------

CONTA_JS = r"""const AGENTI = [['ChatGPT-User','ChatGPT (su richiesta)'],['OAI-SearchBot','ChatGPT ricerca'],['GPTBot','OpenAI (addestramento)'],['openai','ChatGPT (connettore)'],['Claude-User','Claude (su richiesta)'],['Claude-SearchBot','Claude ricerca'],['ClaudeBot','Claude (addestramento)'],['claude','Claude (connettore)'],['anthropic','Claude (connettore)'],['Perplexity','Perplexity'],['Gemini','Gemini'],['Google','Google IA'],['Copilot','Copilot'],['Mistral','Mistral'],['Mozilla','Agente nel browser']];
// Conta l'uso da parte degli assistenti IA (solo quale assistente e quale servizio: mai il testo della domanda)
function contaUso(req, context, servizio){try{const ua=(req.headers.get('user-agent')||'').toLowerCase(),h=AGENTI.find(([k])=>ua.includes(k.toLowerCase()));
 const p=fetch(new URL('/api/conta',req.url),{method:'POST',headers:{'content-type':'application/json','x-misura':'edge'},body:JSON.stringify({e:'bot',p:servizio,f:h?h[1]:'Altro agente'})}).catch(()=>{});
 if(context&&context.waitUntil)context.waitUntil(p)}catch(e){}}
"""

API_JS = r"""// Generato da tools/build.py: non modificare a mano.
// Ricerca pubblica sul testo del sito. Sola lettura, nessun dato registrato.
const IX = __INDICE__;
__MOTORE__
const cerca = creaMotore(IX);
const H = {'Access-Control-Allow-Origin':'*','Cache-Control':'public, max-age=3600','X-Robots-Tag':'noindex'};
const STUDIO = {nome:'Studio Legale Pernorio',avvocato:'Avv. Daniela Pernorio',indirizzo:'Via Egidio Sacchetti 14, 27029 Vigevano (PV)',telefono:'+39 0381 386276',contatti:'__BASE__/contatti'};
__CONTA__const NOTA = 'Informazioni generali a cura dello Studio Legale Pernorio di Vigevano: ogni caso va valutato sui documenti con l\'avvocato. Citare la pagina di origine.';
export default async (req, context) => {
 if (req.method === 'OPTIONS') return new Response(null,{status:204,headers:{...H,'Access-Control-Allow-Methods':'GET, OPTIONS'}});
 const u = new URL(req.url), q = (u.searchParams.get('q') || u.searchParams.get('domanda') || '').slice(0,200).trim();
 const n = Math.min(Math.max(parseInt(u.searchParams.get('n'),10) || 6, 1), 12);
 const md = u.searchParams.get('formato') === 'md' || /text\/markdown/.test(req.headers.get('accept') || '');
 if (!q) return new Response(JSON.stringify({errore:'Indicare la domanda nel parametro q.',esempio:'__BASE__/api/cerca?q=eredita+con+debiti',parametri:{q:'domanda in italiano',n:'numero di risultati (1-12, predefinito 6)',formato:'json (predefinito) oppure md'}}),{status:400,headers:{...H,'Content-Type':'application/json; charset=utf-8'}});
 contaUso(req, context, '/api/cerca');
 const r = cerca(q, n, 2, .15).map(({punteggio, estratto, ...x}) => x);
 if (md) {
  let t = '# Ricerca nel sito dello Studio Legale Pernorio: ' + q + '\n\n';
  t += r.length ? r.map((x,i) => '## ' + (i+1) + '. ' + x.titolo + (x.sezione ? ' · ' + x.sezione : '') + '\n\n' + x.testo + '\n\nFonte: ' + x.url).join('\n\n') : 'Nessun risultato. Elenco delle pagine: __BASE__/llms.txt';
  t += '\n\n---\n\n' + NOTA + '\n' + STUDIO.nome + ', ' + STUDIO.indirizzo + ', tel. ' + STUDIO.telefono + ', ' + STUDIO.contatti + '\n';
  return new Response(t,{headers:{...H,'Content-Type':'text/markdown; charset=utf-8'}});
 }
 return new Response(JSON.stringify({domanda:q,risultati:r,studio:STUDIO,nota:NOTA}),{headers:{...H,'Content-Type':'application/json; charset=utf-8'}});
};
export const config = { path: '/api/cerca' };
"""


def api_function(ix):
    return (API_JS.replace("__INDICE__", json.dumps(ix, ensure_ascii=False, separators=(",", ":")))
            .replace("__MOTORE__", motore_js()).replace("__CONTA__", CONTA_JS).replace("__BASE__", BASE))


def openapi(versione):
    """Descrizione OpenAPI dell'API di ricerca: serve per collegarla a un GPT personalizzato o a un agente."""
    ris = {"type": "object", "properties": {
        "titolo": {"type": "string"}, "tipo": {"type": "string"}, "sezione": {"type": "string"},
        "domanda_frequente": {"type": "boolean"}, "testo": {"type": "string", "description": "Testo del passaggio trovato"},
        "url": {"type": "string", "description": "Indirizzo da citare, con il punto esatto della pagina"},
        "pagina": {"type": "string"}, "markdown": {"type": "string", "description": "Versione Markdown dell'intera pagina"}}}
    return {
        "openapi": "3.1.0",
        "info": {"title": "Studio Legale Pernorio · ricerca nel sito", "version": versione,
                 "description": "Ricerca sul testo completo delle guide legali, delle competenze e delle domande frequenti dello Studio Legale Pernorio (Avv. Daniela Pernorio, avvocato civilista a Vigevano, Pavia). Sola lettura, senza registrazione.",
                 "contact": {"name": "Studio Legale Pernorio", "url": BASE + "/contatti"}},
        "servers": [{"url": BASE}],
        "paths": {"/api/cerca": {"get": {
            "operationId": "cercaNelSito", "summary": "Cerca nel sito dello Studio Legale Pernorio",
            "parameters": [
                {"name": "q", "in": "query", "required": True, "schema": {"type": "string"}, "description": "Domanda o argomento in italiano, ad esempio 'eredità con debiti'"},
                {"name": "n", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 12, "default": 6}, "description": "Numero di risultati"},
                {"name": "formato", "in": "query", "schema": {"type": "string", "enum": ["json", "md"], "default": "json"}, "description": "json oppure md (testo Markdown)"}],
            "responses": {"200": {"description": "Passaggi trovati, dal più pertinente", "content": {"application/json": {"schema": {"type": "object", "properties": {
                "domanda": {"type": "string"}, "risultati": {"type": "array", "items": ris},
                "studio": {"type": "object"}, "nota": {"type": "string"}}}}}}}}}},
    }


OPENSEARCH = f"""<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
<ShortName>Studio Pernorio</ShortName>
<Description>Cerca nelle guide legali dello Studio Legale Pernorio, Vigevano</Description>
<InputEncoding>UTF-8</InputEncoding>
<Language>it-IT</Language>
<Image width="32" height="32" type="image/svg+xml">{BASE}/favicon.svg</Image>
<Url type="text/html" template="{BASE}/cerca?q={{searchTerms}}"/>
<Url type="application/json" template="{BASE}/api/cerca?q={{searchTerms}}"/>
</OpenSearchDescription>
"""
