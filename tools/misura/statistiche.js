/* Pagina riservata /statistiche: confronta il periodo scelto con quello precedente
   e dice in alto se stiamo migliorando e dove. Chiave nell'indirizzo (#k=...). */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var INIZIO = "2026-11-06T17:50:00Z"; // prima di quest'ora: solo prove tecniche
  var IA = ["ChatGPT", "Perplexity", "Gemini", "Claude", "Copilot", "Altre IA"];
  var CONTATTI = ["chiama", "whatsapp", "modulo", "email", "indicazioni"];
  var ZONA = "Entro 22 km";
  var PAGINE = "__PAGINE__"; // indirizzi veri del sito, scritti dalla build: servono a scartare gli scanner
  var CONTROLLI = ["/robots.txt", "/sitemap.xml"];
  var NOMI = { chiama: "Chiama", whatsapp: "WhatsApp", modulo: "Modulo inviato", email: "Email", indicazioni: "Indicazioni stradali" };
  var k = new URLSearchParams(location.hash.slice(1)).get("k") || "";
  try { if (k) localStorage.setItem("slp_k", k); else k = localStorage.getItem("slp_k") || ""; } catch (e) {}
  if (k) history.replaceState(null, "", location.pathname);
  var giorni = 7;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function data(iso) { return iso.slice(0, 10).split("-").reverse().join("/"); }
  function pag(p) { return p === "/" ? "Home" : p.replace(/^\//, "").replace(/-/g, " "); }
  function tipo(p) {
    if (p === "/") return "Home";
    if (/^\/guida-/.test(p) || p === "/guide" || p === "/domande") return "Guide";
    if (/^\/attivita/.test(p) || p === "/diritto-di-famiglia") return "Pagine per materia (avvocato + materia)";
    if (/^\/avvocato-/.test(p)) return "Pagine dei comuni";
    if (/^\/strument/.test(p)) return "Strumenti";
    if (/^\/(contatti|studio|costi-avvocato|colloquio-online|domiciliazioni)$/.test(p)) return "Studio, costi e contatti";
    return "Altro";
  }
  function locale(x) { return /^\/(attivita|avvocato-)/.test(x.p) || x.p === "/diritto-di-famiglia"; }
  function vera(p) { return typeof PAGINE === "string" || PAGINE.indexOf(p) !== -1; }
  function conta(lista, chiave) {
    var m = {};
    lista.forEach(function (x) { var v = chiave(x); m[v] = (m[v] || 0) + 1; });
    return m;
  }
  function ordina(m) { return Object.keys(m).map(function (v) { return [v, m[v]]; }).sort(function (a, b) { return b[1] - a[1]; }); }
  function tabella(righe, intest, vuoto) {
    if (!righe.length) return '<p class="vuoto">' + vuoto + "</p>";
    var max = Math.max.apply(null, righe.map(function (r) { return r[1]; }));
    return "<table><thead><tr><th>" + intest[0] + '</th><th class="n">' + intest[1] + "</th></tr></thead><tbody>" +
      righe.map(function (r) {
        return '<tr><td><span class="barra" style="--w:' + Math.round(r[1] / max * 100) + '%"></span>' + esc(r[0]) + '</td><td class="n">' + r[1] + "</td></tr>";
      }).join("") + "</tbody></table>";
  }
  function delta(ora, prima, completo) {
    if (!completo) return '<span class="delta fermo">confronto dal ' + data(new Date(Date.parse(INIZIO) + 2 * giorni * 864e5).toISOString()) + "</span>";
    var d = ora - prima;
    if (d === 0) return '<span class="delta fermo">= come prima (' + prima + ")</span>";
    var pct = prima ? " (" + (d > 0 ? "+" : "") + Math.round(d / prima * 100) + "%)" : "";
    return '<span class="delta ' + (d > 0 ? "su" : "giu") + '">' + (d > 0 ? "▲ +" : "▼ ") + d + pct + " · prima " + prima + "</span>";
  }
  function pl(n, uno, piu) { return n + " " + (n === 1 ? uno : piu); }
  function escludi() {
    var on = false;
    try { on = localStorage.getItem("slp_escludi") === "1"; } catch (e) {}
    $("escludi").innerHTML = on
      ? "Le visite da questo dispositivo <b>non vengono contate</b>. <button type=\"button\" id=\"btnEsc\">Torna a contarle</button>"
      : "Le visite da questo dispositivo vengono contate. Se è il telefono o il computer dello Studio, conviene escluderlo: <button type=\"button\" id=\"btnEsc\">Non contare le mie visite</button>";
    $("btnEsc").onclick = function () { try { if (on) localStorage.removeItem("slp_escludi"); else localStorage.setItem("slp_escludi", "1"); } catch (e) {} escludi(); };
  }
  function tile(n, et, dl) { return '<div class="tile"><b>' + n + "</b><span>" + et + "</span>" + dl + "</div>"; }

  function misure(ev) {
    var ing = ev.filter(function (x) { return x.e === "ingresso"; });
    var con = ev.filter(function (x) { return CONTATTI.indexOf(x.e) !== -1; });
    return {
      ing: ing, con: con,
      // letture vere: pagine che esistono, senza i controlli di robots e sitemap e senza gli scanner
      bot: ev.filter(function (x) { return x.e === "bot" && CONTROLLI.indexOf(x.p) === -1 && vera(x.p); }),
      botCtl: ev.filter(function (x) { return x.e === "bot" && CONTROLLI.indexOf(x.p) !== -1; }),
      botFinti: ev.filter(function (x) { return x.e === "bot" && CONTROLLI.indexOf(x.p) === -1 && !vera(x.p); }),
      locali: ing.filter(locale),
      conD: ing.filter(function (x) { return x.d; }),
      zona: ing.filter(function (x) { return x.d === ZONA; }),
      conZonaC: con.filter(function (x) { return x.d === ZONA; }),
      indic: con.filter(function (x) { return x.e === "indicazioni"; }),
      conZona: ing.filter(function (x) { return x.z; }),
      ia: ing.filter(function (x) { return IA.indexOf(x.f) !== -1; }),
      google: ing.filter(function (x) { return x.f === "Google" || x.f === "Scheda Google"; }),
      tel: con.filter(function (x) { return x.e === "chiama" || x.e === "whatsapp"; })
    };
  }
  function movimenti(oraM, primaM) {
    var tutti = {}, out = [];
    Object.keys(oraM).concat(Object.keys(primaM)).forEach(function (x) { tutti[x] = 1; });
    Object.keys(tutti).forEach(function (x) { out.push([x, (oraM[x] || 0) - (primaM[x] || 0), oraM[x] || 0, primaM[x] || 0]); });
    return out;
  }

  function mostra(d) {
    var fine = Date.now(), taglio = fine - giorni * 864e5;
    var ev = d.eventi.filter(function (x) {
      return x.t >= INIZIO && x.f !== "Verifica tecnica" && x.p.indexOf("/__") !== 0 && !(x.e === "bot" && /\.html$/.test(x.p));
    });
    var ora = ev.filter(function (x) { return Date.parse(x.t) >= taglio; });
    var prima = ev.filter(function (x) { return Date.parse(x.t) < taglio; });
    var completo = Date.parse(INIZIO) <= fine - 2 * giorni * 864e5;
    var A = misure(ora), P = misure(prima);

    $("periodo").textContent = "Ultimi " + giorni + " giorni (dal " + data(new Date(taglio).toISOString()) + ") confrontati con i " + giorni + " giorni prima. Misura attiva dal 06/11/2026.";

    // Verdetto
    var dPers = A.ing.length - P.ing.length, dCon = A.con.length - P.con.length;
    var cls, tit, righe = [];
    if (!completo) {
      cls = ""; tit = "Raccolta dati in corso";
      righe.push("La misura è attiva dal 6 novembre: il primo confronto completo su " + giorni + " giorni sarà possibile dal " + data(new Date(Date.parse(INIZIO) + 2 * giorni * 864e5).toISOString()) + ".");
    } else {
      var base = Math.max(P.ing.length, 1), pct = dPers / base;
      if ((pct >= 0.1 && dCon >= 0) || (dCon > 0 && pct > -0.1)) { cls = "su"; tit = "Stiamo migliorando"; }
      else if (pct <= -0.1 || dCon < 0) { cls = "giu"; tit = "Stiamo calando"; }
      else { cls = ""; tit = "Stabile"; }
      righe.push("Visite di persone: <b>" + A.ing.length + "</b> contro " + P.ing.length + " del periodo prima.");
      righe.push("Contatti dal sito (Chiama, WhatsApp, moduli, email): <b>" + A.con.length + "</b> contro " + P.con.length + ".");
      if (A.ing.length + P.ing.length < 20) righe.push("Numeri ancora piccoli: bastano poche visite per spostare le percentuali.");
    }
    var top = ordina(conta(A.ing, function (x) { return x.f; }))[0];
    righe.push("Nel periodo: " + pl(A.ing.length, "visita", "visite") + ", " + A.google.length + " da Google, " + A.ia.length + " dalle IA, " + pl(A.con.length, "contatto", "contatti") +
      (A.ing.length ? " (" + Math.round(A.con.length / A.ing.length * 100) + "% delle visite diventa un contatto)." : "."));
    if (top) righe.push("La fonte principale è <b>" + esc(top[0]) + "</b> con " + top[1] + " visite.");
    if (A.conD.length) righe.push("<b>Visite entro 22 km dallo Studio: " + A.zona.length + "</b> su " + A.conD.length + " con posizione nota (" + Math.round(A.zona.length / A.conD.length * 100) +
      "%). Contatti da chi è in zona: <b>" + A.conZonaC.length + "</b>. È l'obiettivo principale.");
    else righe.push("La distanza dallo Studio viene misurata dalla prossima pubblicazione: il dato apparirà con le visite successive.");
    righe.push("Ingressi sulle pagine locali (materie e comuni): <b>" + A.locali.length + "</b> su " + A.ing.length + ". È il numero che deve crescere: sono le ricerche di chi cerca un avvocato in zona.");
    if (A.conZona.length) {
      var lomb = A.conZona.filter(function (x) { return /^Lombardia/.test(x.z); }).length;
      var zonaSt = A.conZona.filter(function (x) { return /Vigevano|Pavia/.test(x.z); }).length;
      righe.push("Visite dalla Lombardia: <b>" + Math.round(lomb / A.conZona.length * 100) + "%</b> (" + lomb + " su " + A.conZona.length + " con regione nota), di cui " + zonaSt + " da Vigevano, Lomellina o Pavia.");
    }
    if (!A.ia.length && A.bot.length) righe.push("Le IA leggono il sito (" + A.bot.length + " letture di pagine vere) ma non mandano ancora persone.");
    $("verdetto").className = "verdetto " + cls;
    $("verdetto").innerHTML = '<span class="label">Il verdetto</span><p class="v-tit">' + tit + "</p><ul><li>" + righe.join("</li><li>") + "</li></ul>";

    $("tiles").innerHTML =
      tile(A.zona.length, "visite entro 22 km dallo Studio", delta(A.zona.length, P.zona.length, completo && P.conD.length > 0)) +
      tile(A.conZonaC.length, "contatti da chi è entro 22 km", delta(A.conZonaC.length, P.conZonaC.length, completo && P.conD.length > 0)) +
      tile(A.indic.length, "richieste di indicazioni stradali", delta(A.indic.length, P.indic.length, completo)) +
      tile(A.ing.length, "visite di persone", delta(A.ing.length, P.ing.length, completo)) +
      tile(A.con.length, "contatti dal sito", delta(A.con.length, P.con.length, completo)) +
      tile(A.google.length, "da Google e scheda Google", delta(A.google.length, P.google.length, completo)) +
      tile(A.ia.length, "da ChatGPT, Gemini e altre IA", delta(A.ia.length, P.ia.length, completo)) +
      tile(A.tel.length, "tocchi su Chiama o WhatsApp", delta(A.tel.length, P.tel.length, completo)) +
      tile(A.ing.length ? Math.round(A.con.length / A.ing.length * 100) + "%" : "–", "visite che diventano contatto", "") +
      tile(A.locali.length, "ingressi su pagine locali (materie e comuni)", delta(A.locali.length, P.locali.length, completo)) +
      tile(A.bot.length, "pagine lette dai bot IA", delta(A.bot.length, P.bot.length, completo)) +
      tile(Object.keys(conta(A.bot, function (x) { return x.f; })).length, "IA diverse che leggono il sito", "");

    // Dove cresce / cala: fonti, pagine d'ingresso, bot
    var mov = []
      .concat(movimenti(conta(A.ing, function (x) { return x.f; }), conta(P.ing, function (x) { return x.f; })).map(function (r) { return ["Visite da " + r[0]].concat(r.slice(1)); }))
      .concat(movimenti(conta(A.ing, function (x) { return x.p; }), conta(P.ing, function (x) { return x.p; })).map(function (r) { return ["Ingressi su «" + pag(r[0]) + "»"].concat(r.slice(1)); }))
      .concat(movimenti(conta(A.con, function (x) { return NOMI[x.e]; }), conta(P.con, function (x) { return NOMI[x.e]; })).map(function (r) { return ["Contatti " + r[0]].concat(r.slice(1)); }))
      .concat(movimenti(conta(A.bot, function (x) { return x.f; }), conta(P.bot, function (x) { return x.f; })).map(function (r) { return ["Letture bot " + r[0]].concat(r.slice(1)); }));
    function lista(arr, vuoto) {
      if (!arr.length) return '<p class="vuoto">' + vuoto + "</p>";
      return "<ul>" + arr.slice(0, 6).map(function (r) {
        return "<li>" + esc(r[0]) + ': <span class="delta ' + (r[1] > 0 ? "su" : "giu") + '">' + (r[1] > 0 ? "+" : "") + r[1] + "</span> <span class=\"nota\">(" + r[2] + " ora, " + r[3] + " prima)</span></li>";
      }).join("") + "</ul>";
    }
    var su = mov.filter(function (r) { return r[1] > 0; }).sort(function (a, b) { return b[1] - a[1]; });
    var giu = mov.filter(function (r) { return r[1] < 0; }).sort(function (a, b) { return a[1] - b[1]; });
    if (!completo) {
      $("cresce").innerHTML = lista(su, "Ancora niente da confrontare.") + '<p class="nota">Confronto parziale: il periodo precedente è iniziato prima della misura.</p>';
      $("cala").innerHTML = '<p class="vuoto">Si potrà dire dal ' + data(new Date(Date.parse(INIZIO) + 2 * giorni * 864e5).toISOString()) + ".</p>";
    } else {
      $("cresce").innerHTML = lista(su, "Nessuna crescita rispetto al periodo prima.");
      $("cala").innerHTML = lista(giu, "Nessun calo rispetto al periodo prima.");
    }

    // Andamento
    var g = {}, gIA = {};
    for (var i = 0; i < giorni; i++) { var dt = new Date(fine - (giorni - 1 - i) * 864e5).toISOString().slice(0, 10); g[dt] = 0; gIA[dt] = 0; }
    A.ing.forEach(function (x) { var dt = x.t.slice(0, 10); if (dt in g) { g[dt]++; if (IA.indexOf(x.f) !== -1) gIA[dt]++; } });
    var vals = Object.keys(g), max = Math.max(1, Math.max.apply(null, vals.map(function (v) { return g[v]; })));
    $("giorni").innerHTML = vals.map(function (v) {
      return '<div class="col" title="' + data(v) + ": " + g[v] + " visite, " + gIA[v] + ' da IA"><i style="height:' + (g[v] / max * 100) + '%"><em style="height:' + (g[v] ? gIA[v] / g[v] * 100 : 0) + '%"></em></i></div>';
    }).join("");

    $("fonti").innerHTML = tabella(ordina(conta(A.ing, function (x) { return x.f; })), ["Provenienza", "Visite"], "Nessuna visita nel periodo.");
    $("contatti").innerHTML = tabella(ordina(conta(A.con, function (x) { return NOMI[x.e] + " · da " + (x.f || "?"); })), ["Contatto e provenienza", "Clic"], "Nessun clic su Chiama, WhatsApp, email o moduli nel periodo.");
    $("pagine").innerHTML = tabella(ordina(conta(A.ing, function (x) { return pag(x.p); })).slice(0, 12), ["Pagina", "Ingressi"], "Nessun ingresso nel periodo.");
    $("pagineContatti").innerHTML = tabella(ordina(conta(A.con, function (x) { return pag(x.p); })), ["Pagina", "Contatti"], "Nessun contatto nel periodo.");
    $("paginaIA").innerHTML = tabella(ordina(conta(A.ia, function (x) { return x.f + " → " + pag(x.p); })), ["IA e pagina d'ingresso", "Visite"], "Nessuna visita da ChatGPT, Gemini, Perplexity, Claude o Copilot nel periodo.");
    $("fasce").innerHTML = A.conD.length
      ? tabella(ordina(conta(A.conD, function (x) { return x.d; })), ["Distanza dallo Studio", "Visite"], "—") +
        tabella(ordina(conta(A.zona, function (x) { return tipo(x.p); })), ["Chi è entro 22 km entra da", "Visite"], "Nessuna visita dalla zona nel periodo.")
      : '<p class="vuoto">Misurata dalla prossima pubblicazione: ancora nessun dato nel periodo.</p>';
    $("tipi").innerHTML = tabella(ordina(conta(A.ing, function (x) { return tipo(x.p); })), ["Tipo di pagina d'ingresso", "Visite"], "Nessuna visita nel periodo.");
    $("regioni").innerHTML = A.conZona.length
      ? tabella(ordina(conta(A.conZona, function (x) { return x.z; })).slice(0, 10), ["Regione", "Visite"], "—")
      : '<p class="vuoto">La regione viene registrata dalla pubblicazione del 15/11/2026 in poi: ancora nessun dato nel periodo.</p>';
    var conIng = A.con.filter(function (x) { return x.i; });
    $("contattiIngresso").innerHTML = conIng.length
      ? tabella(ordina(conta(conIng, function (x) { return pag(x.i) + (x.z ? " · " + x.z : ""); })), ["Pagina da cui era entrato chi ha contattato", "Contatti"], "—")
      : '<p class="vuoto">Registrata dalla pubblicazione del 15/11/2026 in poi: ancora nessun contatto con questo dato.</p>';
    $("botNota").textContent = "Contate solo le letture di pagine che esistono. Esclusi nel periodo: " + A.botFinti.length +
      " tentativi su indirizzi inesistenti (programmi che cercano password fingendosi bot delle IA) e " + A.botCtl.length + " semplici controlli di robots e sitemap.";
    $("bot").innerHTML = tabella(ordina(conta(A.bot, function (x) { return x.f; })), ["Bot", "Letture"], "Nessuna lettura nel periodo.");
    $("botPagine").innerHTML = tabella(ordina(conta(A.bot, function (x) { return pag(x.p); })).slice(0, 12), ["Pagina", "Letture"], "—");
    escludi();
    $("dati").hidden = false;
  }

  function carica() {
    if (!k) { $("stato").textContent = "Serve il link con la chiave."; return; }
    $("stato").textContent = "Carico…";
    fetch("/api/statistiche?giorni=" + giorni * 2 + "&k=" + encodeURIComponent(k), { cache: "no-store" })
      .then(function (r) { if (r.status === 403) throw new Error("Chiave non valida."); if (!r.ok) throw new Error("Errore " + r.status + ": riprovare tra poco."); return r.json(); })
      .then(function (d) { $("stato").textContent = ""; mostra(d); })
      .catch(function (e) { $("stato").textContent = e.message; });
  }
  document.querySelectorAll("[data-giorni]").forEach(function (b) {
    b.addEventListener("click", function () {
      giorni = +b.getAttribute("data-giorni");
      document.querySelectorAll("[data-giorni]").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      carica();
    });
  });
  carica();
})();
