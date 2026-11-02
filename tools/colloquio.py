# -*- coding: utf-8 -*-
"""Pagina /colloquio-online: richiesta di colloquio a distanza con allegati,
scelta della modalita' video e prova di videocamera e microfono."""

SLUG = "colloquio-online"
TITLE = "Colloquio online con l'avvocato · Videochiamata e documenti"
DESCRIPTION = "Consulenza legale a distanza con l'Avv. Daniela Pernorio: videochiamata dal browser o WhatsApp, invio dei documenti online, preventivo scritto. Da tutta Italia."
LABEL = "Colloquio a distanza"
H1 = "Colloquio online con l'avvocato"
LEAD = "Lo stesso colloquio che si fa in Studio, guardandosi in faccia, ma da casa o dall'ufficio. I documenti si inviano prima, così l'avvocato arriva alla videochiamata avendo già studiato il caso."

MATERIE = [
    "Separazione e divorzio", "Affidamento dei figli", "Unioni civili e convivenze", "Successioni ed eredità",
    "Amministrazione di sostegno", "Affitti e sfratti", "Usucapione, condominio, diritti reali",
    "Debiti, saldo e stralcio, pignoramenti", "Recupero crediti", "Contratti", "Incidenti e risarcimenti",
    "Multe e Codice della strada", "Lavoro", "Altro",
]

COME = """
<div class="card panel article rv">
<h2>Come funziona</h2>
<ol class="steps-online">
<li><b>Richiesta</b>: compili il modulo qui sotto, descriva la questione e alleghi i documenti principali (PDF o foto, fino a 8 MB in tutto).</li>
<li><b>Studio del caso</b>: l'avvocato legge i documenti prima del colloquio e la ricontatta per fissare giorno e ora.</li>
<li><b>Videochiamata</b>: dal browser con il link personale che riceve subito, oppure su WhatsApp video, oppure per telefono. Nessun programma da installare.</li>
<li><b>Riepilogo scritto</b>: dopo il colloquio riceve via email le strade possibili e il preventivo scritto, prima di iniziare qualsiasi attività.</li>
<li><b>Pratica condivisa</b>: aggiornamenti per email o PEC a ogni passaggio, documenti scambiati in formato digitale, firma anche a distanza.</li>
</ol>
<h2>Perché funziona</h2>
<ul>
<li><b>Trasparenza</b>: si parla guardandosi, come in Studio. Ogni passaggio e ogni costo è messo per iscritto.</li>
<li><b>Tempo</b>: niente spostamenti né parcheggio. Utile per chi lavora, per chi vive lontano da Vigevano, per i genitori con figli piccoli.</li>
<li><b>Riservatezza</b>: il link della videochiamata è personale e non è pubblicato da nessuna parte. Il colloquio non viene registrato.</li>
<li><b>Anche da lontano</b>: per le cause davanti ai Tribunali di Pavia, Milano e Novara lo Studio assiste anche clienti che vivono in altre città o all'estero.</li>
</ul>
<p>Preferisce venire in Studio? Nessun problema: il colloquio in presenza resta sempre possibile, in Via Egidio Sacchetti 14 a Vigevano.</p>
</div>
"""

TEST_AV = """
<div class="card panel rv tool" id="av">
<span class="label">Prima della videochiamata</span>
<h2 style="margin-top:10px">Prova videocamera e microfono</h2>
<p style="margin-top:10px">Un controllo di dieci secondi, direttamente qui. L'immagine e l'audio restano sul suo dispositivo: non vengono inviati a nessuno.</p>
<div class="av-box"><video id="av-v" playsinline muted></video><div class="av-ph" id="av-ph">Anteprima video</div></div>
<div class="av-meter" aria-hidden="true"><i id="av-l"></i></div>
<p class="note-s" id="av-s" aria-live="polite">Prema il pulsante e consenta l'accesso a videocamera e microfono.</p>
<div class="actions" style="margin-top:14px"><button class="btn btn-primary" type="button" id="av-go">Avvia la prova</button><button class="btn btn-ghost" type="button" id="av-stop" hidden>Interrompi</button></div>
</div>
"""


def form_html(esc):
    opts = "".join(f"<option>{esc(m)}</option>" for m in MATERIE)
    return f"""
<div class="card panel rv tool" id="richiesta">
<span class="label">Richiesta di colloquio online</span>
<h2 style="margin-top:10px">Racconti la questione e alleghi i documenti</h2>
<form name="colloquio-online" id="co" method="POST" action="/grazie" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="colloquio-online">
<input type="hidden" name="link-video" id="co-room" value="">
<p class="hp"><label>Non compilare<input name="bot-field"></label></p>
<div class="tgrid">
<label>Nome e cognome<input type="text" name="nome" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Telefono<input type="tel" name="telefono" required autocomplete="tel"></label>
<label>Materia<select name="materia" required><option value="">Scegli…</option>{opts}</select></label>
</div>
<label>Di cosa si tratta<textarea name="descrizione" rows="5" required placeholder="Poche righe: cosa è successo, chi è coinvolto, cosa vorrebbe ottenere."></textarea></label>
<div class="tgrid">
<label>C'è una scadenza? (facoltativo)<input type="date" name="scadenza"></label>
<label>Come preferisce il colloquio<select name="modalita"><option>Videochiamata dal browser (link personale)</option><option>WhatsApp video</option><option>Telefono</option><option>In Studio a Vigevano</option></select></label>
</div>
<fieldset class="slots"><legend>Quando è disponibile</legend>
<label><input type="checkbox" name="disponibilita" value="Mattina 9-13"> Mattina</label>
<label><input type="checkbox" name="disponibilita" value="Pomeriggio 14-17"> Pomeriggio</label>
<label><input type="checkbox" name="disponibilita" value="Tardo pomeriggio 17-19"> Dopo il lavoro (17-19)</label>
</fieldset>
<div class="files">
<label>Documento 1<input type="file" name="documento1" accept=".pdf,.jpg,.jpeg,.png,.heic,.doc,.docx"></label>
<label>Documento 2<input type="file" name="documento2" accept=".pdf,.jpg,.jpeg,.png,.heic,.doc,.docx"></label>
<label>Documento 3<input type="file" name="documento3" accept=".pdf,.jpg,.jpeg,.png,.heic,.doc,.docx"></label>
<p class="note-s" id="co-size">Massimo 8 MB in totale. Altri documenti si possono inviare dopo, via email o PEC.</p>
</div>
<label class="consent"><input type="checkbox" name="privacy" required><span>Ho letto l'<a href='/privacy'>informativa privacy</a> e acconsento all'invio dei documenti allegati.</span></label>
<div class="actions"><button class="btn btn-primary" type="submit" id="co-send">Invia la richiesta</button></div>
<p class="note-s co-err" id="co-err" hidden></p>
</form>
<div id="co-ok" hidden>
<h2>Richiesta ricevuta</h2>
<p style="margin-top:10px">Grazie. L'avvocato leggerà la richiesta e i documenti e la ricontatterà per fissare giorno e ora del colloquio.</p>
<p style="margin-top:10px">Per avere una risposta più rapida può avvisare lo Studio anche su WhatsApp.</p><div class="actions" style="margin-top:12px"><a class="btn btn-primary" id="co-wa" href="https://wa.me/393333368757" target="_blank" rel="noopener">Avvisa su WhatsApp</a></div>
<div class="co-link" id="co-linkbox" hidden><span class="label">Il suo link personale per la videochiamata</span><a id="co-link" href="#" target="_blank" rel="noopener"></a><p class="note-s">Lo conservi: lo userà all'ora concordata. Funziona da computer e telefono, senza installare nulla. Se entra prima dell'avvocato, attenda qualche istante.</p><div class="actions"><button class="btn btn-ghost" type="button" id="co-copy">Copia il link</button></div></div>
</div>
</div>
"""


JS = r"""
<script>
(function(){
/* Link video personale */
var room='StudioLegalePernorio-'+Array.from(crypto.getRandomValues(new Uint8Array(9))).map(function(b){return'abcdefghjkmnpqrstuvwxyz23456789'[b%31]}).join('');
var url='https://meet.jit.si/'+room+'#config.prejoinConfig.enabled=true';
var rf=document.getElementById('co-room');if(rf)rf.value=url;
var f=document.getElementById('co');
if(f){
 var MAX=8*1024*1024,sz=document.getElementById('co-size');
 function tot(){var t=0;f.querySelectorAll('input[type=file]').forEach(function(i){if(i.files[0])t+=i.files[0].size});return t}
 f.addEventListener('change',function(e){if(e.target.type!=='file')return;var t=tot();sz.textContent=(t/1048576).toFixed(1).replace('.',',')+' MB su 8 MB'+(t>MAX?' – troppo grandi: tolga un documento e lo invii dopo via email.':'');sz.classList.toggle('co-err',t>MAX)});
 f.addEventListener('submit',function(e){
  if(!window.fetch||!window.FormData)return;
  e.preventDefault();var err=document.getElementById('co-err');err.hidden=true;
  if(tot()>MAX){err.textContent='Gli allegati superano 8 MB.';err.hidden=false;return}
  var b=document.getElementById('co-send');b.disabled=true;b.firstChild.textContent='Invio in corso…';
  fetch('/',{method:'POST',body:new FormData(f)}).then(function(r){if(!r.ok)throw 0;
   f.hidden=true;var ok=document.getElementById('co-ok');ok.hidden=false;
   if(f.modalita.value.indexOf('browser')>-1){var a=document.getElementById('co-link');a.href=url;a.textContent=url.split('#')[0];document.getElementById('co-linkbox').hidden=false}
   var w=document.getElementById('co-wa');if(w)w.href='https://wa.me/393333368757?text='+encodeURIComponent('Buongiorno Avvocato, ho appena inviato dal sito una richiesta di colloquio online. '+f.nome.value+' ('+f.materia.value+')');
   ok.scrollIntoView({behavior:'smooth',block:'start'});
  }).catch(function(){b.disabled=false;b.firstChild.textContent='Invia la richiesta';err.textContent='Invio non riuscito. Riprovi, oppure scriva su WhatsApp o chiami lo 0381 386276.';err.hidden=false});
 });
 var cp=document.getElementById('co-copy');if(cp)cp.addEventListener('click',function(){try{navigator.clipboard.writeText(url.split('#')[0]);cp.firstChild.textContent='Copiato'}catch(e){}});
}
/* Prova videocamera e microfono */
var go=document.getElementById('av-go'),st=document.getElementById('av-stop'),v=document.getElementById('av-v'),s=document.getElementById('av-s'),lv=document.getElementById('av-l'),ph=document.getElementById('av-ph');
var stream=null,ctx=null,raf=0;
function stop(){if(stream)stream.getTracks().forEach(function(t){t.stop()});stream=null;if(ctx)ctx.close();ctx=null;cancelAnimationFrame(raf);lv.style.width='0';v.srcObject=null;ph.hidden=false;st.hidden=true;go.hidden=false}
if(go){go.addEventListener('click',function(){
 if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){s.textContent='Questo browser non consente la prova: usi Chrome, Safari, Edge o Firefox aggiornati.';return}
 navigator.mediaDevices.getUserMedia({video:true,audio:true}).then(function(m){
  stream=m;v.srcObject=m;v.play();ph.hidden=true;go.hidden=true;st.hidden=false;
  s.textContent='Videocamera attiva. Parli: se la barra si muove, il microfono funziona.';
  try{ctx=new (window.AudioContext||window.webkitAudioContext)();var an=ctx.createAnalyser();an.fftSize=512;ctx.createMediaStreamSource(m).connect(an);var d=new Uint8Array(an.fftSize),heard=false;
   (function loop(){an.getByteTimeDomainData(d);var p=0;for(var i=0;i<d.length;i++){var x=Math.abs(d[i]-128);if(x>p)p=x}var pc=Math.min(100,p/64*100);lv.style.width=pc+'%';if(pc>25&&!heard){heard=true;s.textContent='Tutto funziona: videocamera e microfono pronti per il colloquio.'}raf=requestAnimationFrame(loop)})();}catch(e){}
 }).catch(function(e){s.textContent=(e&&e.name==='NotAllowedError')?'Accesso negato. Consenta videocamera e microfono dalle impostazioni del browser e riprovi.':'Nessuna videocamera o microfono trovati.'})
});st.addEventListener('click',function(){stop();s.textContent='Prova interrotta.'})}
})();
</script>"""

CSS = """
.steps-online{padding-left:1.3em}.steps-online li+li{margin-top:.6em}
.tool textarea{font:inherit;padding:12px 14px;border:1px solid color-mix(in srgb,var(--ink) 22%,transparent);border-radius:12px;background:var(--paper);color:var(--ink);width:100%;box-sizing:border-box;resize:vertical}
.tool input[type=email],.tool input[type=tel]{font:inherit;padding:12px 14px;border:1px solid color-mix(in srgb,var(--ink) 22%,transparent);border-radius:12px;background:var(--paper);color:var(--ink);min-height:48px;width:100%;box-sizing:border-box}
.tool input[type=file]{font:inherit;font-size:.85rem;padding:10px;border:1px dashed color-mix(in srgb,var(--ink) 30%,transparent);border-radius:12px;width:100%;box-sizing:border-box;background:var(--paper)}
.tool fieldset.slots{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:10px 18px}
.tool fieldset.slots legend{font-size:.9rem;font-weight:500;margin-bottom:8px;padding:0}
.tool fieldset.slots label{display:flex;gap:8px;align-items:center;font-weight:400}
.tool .files{display:grid;gap:10px}
.tool .consent{display:flex;gap:10px;align-items:flex-start;font-weight:400}
.tool .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.tool [hidden]{display:none!important}
.co-err{color:#9b2c2c}
.co-link{margin-top:18px;padding:16px;border-radius:14px;background:color-mix(in srgb,var(--ink) 5%,transparent);display:grid;gap:8px}
.co-link a{font-weight:500;overflow-wrap:anywhere;text-decoration:underline}
.av-box{position:relative;margin-top:16px;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#1d241f}
.av-box video{width:100%;height:100%;object-fit:cover;transform:scaleX(-1)}
.av-ph{position:absolute;inset:0;display:grid;place-items:center;color:#cfd6d0;font-size:.9rem}
.av-meter{margin-top:12px;height:8px;border-radius:99px;background:color-mix(in srgb,var(--ink) 10%,transparent);overflow:hidden}
.av-meter i{display:block;height:100%;width:0;background:var(--forest);transition:width .08s}
"""
