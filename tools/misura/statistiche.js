/* Pagina riservata /statistiche: confronta il periodo scelto con quello precedente
   e dice in alto se stiamo migliorando e dove. Chiave nell'indirizzo (#k=...). */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var INIZIO = "2026-11-06T17:50:00Z"; // prima di quest'ora: solo prove tecniche
  var IA = ["ChatGPT", "Perplexity", "Gemini", "Claude", "Copilot", "Altre IA"];
  var CONTATTI = ["chiama", "whatsapp", "modulo", "email"];
  var NOMI = { chiama: "Chiama", whatsapp: "WhatsApp", modulo: "Modulo inviato", email: "Email" };
  var k = new URLSearchParams(location.hash.slice(1)).get("k") || "";
  try { if (k) localStorage.setItem("slp_k", k); else k = localStorage.getItem("slp_k") || ""; } catch (e) {}
  if (k) history.replaceState(null, "", location.pathname);
  var giorni = 7;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function data(iso) { return iso.slice(0, 10).split("-").reverse().join("/"); }
  function pag(p) { return p === "/" ? "Home" : p.replace(/^\//, "").replace(/-/g, " "); }
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
      bot: ev.filter(function (x) { return x.e === "bot"; }),
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
    if (!A.ia.length && A.bot.length) righe.push("Le IA leggono il sito (" + A.bot.length + " letture dei loro bot) ma non mandano ancora persone.");
    $("verdetto").className = "verdetto " + cls;
    $("verdetto").innerHTML = '<span class="label">Il verdetto</span><p class="v-tit">' + tit + "</p><ul><li>" + righe.join("</li><li>") + "</li></ul>";

    $("tiles").innerHTML =
      tile(A.ing.length, "visite di persone", delta(A.ing.length, P.ing.length, completo)) +
      tile(A.con.length, "contatti dal sito", delta(A.con.length, P.con.length, completo)) +
      tile(A.google.length, "da Google e scheda Google", delta(A.google.length, P.google.length, completo)) +
      tile(A.ia.length, "da ChatGPT, Gemini e altre IA", delta(A.ia.length, P.ia.length, completo)) +
      tile(A.tel.length, "tocchi su Chiama o WhatsApp", delta(A.tel.length, P.tel.length, completo)) +
      tile(A.ing.length ? Math.round(A.con.length / A.ing.length * 100) + "%" : "–", "visite che diventano contatto", "") +
      tile(A.bot.length, "letture dei bot IA", delta(A.bot.length, P.bot.length, completo)) +
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
