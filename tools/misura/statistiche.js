/* Pagina riservata /statistiche: legge /api/statistiche con la chiave nell'indirizzo (#k=...). */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var IA = ["ChatGPT", "Perplexity", "Gemini", "Claude", "Copilot", "Altre IA"];
  var CONTATTI = ["chiama", "whatsapp", "modulo", "email"];
  var NOMI = { chiama: "Chiama", whatsapp: "WhatsApp", modulo: "Moduli inviati", email: "Email" };
  var k = new URLSearchParams(location.hash.slice(1)).get("k") || "";
  try { if (k) localStorage.setItem("slp_k", k); else k = localStorage.getItem("slp_k") || ""; } catch (e) {}
  if (k) history.replaceState(null, "", location.pathname);
  var giorni = 30;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function conta(lista, chiave) {
    var m = {};
    lista.forEach(function (x) { var v = chiave(x); m[v] = (m[v] || 0) + 1; });
    return Object.keys(m).map(function (v) { return [v, m[v]]; }).sort(function (a, b) { return b[1] - a[1]; });
  }
  function tabella(righe, intest, vuoto) {
    if (!righe.length) return '<p class="vuoto">' + vuoto + "</p>";
    var max = Math.max.apply(null, righe.map(function (r) { return r[1]; }));
    return '<table><thead><tr><th>' + intest[0] + '</th><th class="n">' + intest[1] + "</th></tr></thead><tbody>" +
      righe.map(function (r) {
        return '<tr><td><span class="barra" style="--w:' + Math.round(r[1] / max * 100) + '%"></span>' + esc(r[0]) + '</td><td class="n">' + r[1] + "</td></tr>";
      }).join("") + "</tbody></table>";
  }
  function tile(n, et, nota) { return '<div class="tile"><b>' + n + "</b><span>" + et + "</span>" + (nota ? "<small>" + nota + "</small>" : "") + "</div>"; }

  function mostra(d) {
    var ev = d.eventi;
    var ing = ev.filter(function (x) { return x.e === "ingresso"; });
    var con = ev.filter(function (x) { return CONTATTI.indexOf(x.e) !== -1; });
    var bot = ev.filter(function (x) { return x.e === "bot"; });
    var ingIA = ing.filter(function (x) { return IA.indexOf(x.f) !== -1; });
    var conIA = con.filter(function (x) { return IA.indexOf(x.f) !== -1; });
    $("periodo").textContent = "Dal " + d.dal.split("-").reverse().join("/") + " a oggi (" + d.giorni + " giorni)";
    $("tiles").innerHTML =
      tile(ing.length, "visite entrate nel sito") +
      tile(ingIA.length, "arrivate da un'IA", ing.length ? Math.round(ingIA.length / ing.length * 100) + "% del totale" : "") +
      tile(con.length, "contatti dal sito", "Chiama, WhatsApp, moduli") +
      tile(bot.length, "letture di bot IA");
    $("fonti").innerHTML = tabella(conta(ing, function (x) { return x.f; }), ["Da dove arrivano", "Visite"], "Ancora nessuna visita registrata.");
    $("contatti").innerHTML = tabella(conta(con, function (x) { return NOMI[x.e] + " · da " + (x.f || "?"); }), ["Contatto e provenienza", "Clic"], "Ancora nessun clic su Chiama o WhatsApp.");
    $("paginaIA").innerHTML = tabella(conta(ingIA, function (x) { return x.f + " → " + x.p; }), ["IA e pagina d'ingresso", "Visite"], "Ancora nessuna visita da ChatGPT, Gemini, Perplexity, Claude o Copilot.") +
      (conIA.length ? '<p class="nota">Di cui contatti partiti da chi è arrivato da un\'IA: <b>' + conIA.length + "</b></p>" : "");
    $("bot").innerHTML = tabella(conta(bot, function (x) { return x.f; }), ["Bot", "Pagine lette"], "Ancora nessuna lettura registrata.");
    $("botPagine").innerHTML = tabella(conta(bot, function (x) { return x.p; }).slice(0, 15), ["Pagina", "Letture"], "—");
    // andamento giornaliero
    var g = {}, gIA = {};
    for (var i = 0; i < d.giorni; i++) {
      var dt = new Date(Date.now() - (d.giorni - 1 - i) * 864e5).toISOString().slice(0, 10);
      g[dt] = 0; gIA[dt] = 0;
    }
    ing.forEach(function (x) { var dt = x.t.slice(0, 10); if (dt in g) { g[dt]++; if (IA.indexOf(x.f) !== -1) gIA[dt]++; } });
    var vals = Object.keys(g), max = Math.max(1, Math.max.apply(null, vals.map(function (v) { return g[v]; })));
    $("giorni").innerHTML = vals.map(function (v) {
      return '<div class="col" title="' + v.split("-").reverse().join("/") + ": " + g[v] + " visite, " + gIA[v] + ' da IA"><i style="height:' + (g[v] / max * 100) + '%"><em style="height:' + (g[v] ? gIA[v] / g[v] * 100 : 0) + '%"></em></i></div>';
    }).join("");
    $("dati").hidden = false;
  }

  function carica() {
    if (!k) { $("stato").textContent = "Serve il link con la chiave."; return; }
    $("stato").textContent = "Carico…";
    fetch("/api/statistiche?giorni=" + giorni + "&k=" + encodeURIComponent(k), { cache: "no-store" })
      .then(function (r) { if (r.status === 403) throw new Error("Chiave non valida."); if (!r.ok) throw new Error("Errore " + r.status); return r.json(); })
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
