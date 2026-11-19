/* Misura senza cookie dello Studio Legale Pernorio.
   Conta solo: da dove arriva chi entra nel sito (Google, ChatGPT, Gemini, ...)
   e i clic su Chiama, WhatsApp e invio dei moduli, con la pagina da cui la
   visita era entrata. Nessun identificativo,
   nessun cookie, nessun dato personale: solo totali giornalieri. */
(function () {
  if (navigator.webdriver || !navigator.sendBeacon) return;
  try { if (localStorage.getItem("slp_escludi") === "1") return; } catch (x) {} // dispositivo dello Studio
  var FONTI = [
    [/chatgpt\.com|chat\.openai\.com|openai/, "ChatGPT"],
    [/perplexity/, "Perplexity"],
    [/gemini\.google|bard\.google/, "Gemini"],
    [/claude\.ai|anthropic/, "Claude"],
    [/copilot\.microsoft|copilot\.cloud|edgeservices\.bing/, "Copilot"],
    [/deepseek|mistral|you\.com|meta\.ai|grok|x\.ai|phind|kagi/, "Altre IA"],
    [/^gbp$|business\.google|maps\.google|google\.[a-z.]+\/maps/, "Scheda Google"],
    [/google\./, "Google"],
    [/bing\./, "Bing"],
    [/duckduckgo|ecosia|yahoo|qwant|brave/, "Altri motori"],
    [/instagram/, "Instagram"],
    [/facebook|fb\.com|whatsapp|linkedin|t\.co$|tiktok/, "Social"],
    [/dequo|lawzana|virgilio|paginebianche|paginegialle|avvocati|ordineavvocati/, "Elenchi"]
  ];
  function fonte() {
    var q = new URLSearchParams(location.search);
    var u = (q.get("utm_source") || "").toLowerCase();
    var r = "";
    try { r = document.referrer ? new URL(document.referrer).hostname.toLowerCase() : ""; } catch (e) {}
    if (r === location.hostname) return null; // navigazione interna
    var t = u || r;
    if (!t) return "Diretto o app";
    for (var i = 0; i < FONTI.length; i++) if (FONTI[i][0].test(t)) return FONTI[i][1];
    return "Altri siti";
  }
  function invia(e, f) {
    try {
      navigator.sendBeacon("/api/conta", JSON.stringify({ e: e, p: location.pathname, f: f || "", i: e === "ingresso" ? "" : ing }));
    } catch (x) {}
  }
  var f = fonte(), mem = null, ing = ""; // ing: pagina da cui è entrata la visita
  try { mem = sessionStorage.getItem("slp_fonte"); ing = sessionStorage.getItem("slp_ingresso") || ""; } catch (x) {}
  if (f) {
    ing = location.pathname;
    invia("ingresso", f);
    try { sessionStorage.setItem("slp_fonte", f); sessionStorage.setItem("slp_ingresso", ing); } catch (x) {}
  } else {
    f = mem || "Sconosciuta";
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href]");
    if (!a) return;
    var h = a.getAttribute("href");
    if (/^tel:/.test(h)) invia("chiama", f);
    else if (/wa\.me|whatsapp/.test(h)) invia("whatsapp", f);
    else if (/^mailto:/.test(h)) invia("email", f);
    else if (/google\.[a-z.]+\/maps\/dir/.test(h)) invia("indicazioni", f);
  }, true);
  document.addEventListener("submit", function () { invia("modulo", f); }, true);

  // Messaggio sulla distanza dallo Studio, dove la pagina lo prevede (data-dove).
  // La posizione è quella approssimata della connessione: si usa solo per questo testo e non viene registrata.
  var box = document.querySelectorAll("[data-dove]");
  if (box.length && window.fetch) {
    fetch("/api/dove", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : {}; }).then(function (d) {
      var t = "";
      if (d.vigevano) t = "È a Vigevano: lo Studio è in Via Egidio Sacchetti 14, vicino al centro storico. <a href=\"https://www.google.com/maps/dir/?api=1&destination=Via+Egidio+Sacchetti+14%2C+27029+Vigevano+PV\" target=\"_blank\" rel=\"noopener\">Indicazioni stradali</a>";
      else if (d.comune && location.pathname !== d.comune.url) t = "Da " + d.comune.nome + " allo Studio: " + d.comune.min + " in auto. <a href=\"" + d.comune.url + "\">Avvocato per chi vive a " + d.comune.nome + "</a>";
      else if (d.comune) t = "";
      else if (d.fascia === "Entro 22 km") t = "È a meno di mezz'ora dallo Studio, a Vigevano. <a href=\"/contatti\">Come arrivare e orari</a>";
      else if (d.fascia) t = "Non abita vicino a Vigevano? Il primo colloquio si può fare online, in videochiamata, con i documenti inviati prima. <a href=\"/colloquio-online\">Colloquio online</a>";
      if (!t) return;
      for (var i = 0; i < box.length; i++) { box[i].innerHTML = t; box[i].hidden = false; }
    }).catch(function () {});
  }
})();
