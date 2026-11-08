/* Misura senza cookie dello Studio Legale Pernorio.
   Conta solo: da dove arriva chi entra nel sito (Google, ChatGPT, Gemini, ...)
   e i clic su Chiama, WhatsApp e invio dei moduli. Nessun identificativo,
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
      navigator.sendBeacon("/api/conta", JSON.stringify({ e: e, p: location.pathname, f: f || "" }));
    } catch (x) {}
  }
  var f = fonte(), mem = null;
  try { mem = sessionStorage.getItem("slp_fonte"); } catch (x) {}
  if (f) {
    invia("ingresso", f);
    try { sessionStorage.setItem("slp_fonte", f); } catch (x) {}
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
  }, true);
  document.addEventListener("submit", function () { invia("modulo", f); }, true);
})();
