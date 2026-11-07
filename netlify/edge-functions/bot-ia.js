// Conta le letture delle pagine da parte dei bot delle IA (non eseguono JavaScript,
// quindi solo il server li vede). Gira SOLO quando lo user-agent è di un bot IA:
// per le persone non viene nemmeno avviata. Non modifica la risposta.
const BOT = [
  ["GPTBot", "OpenAI (addestramento)"],
  ["OAI-SearchBot", "ChatGPT ricerca"],
  ["ChatGPT-User", "ChatGPT (su richiesta)"],
  ["ClaudeBot", "Claude (addestramento)"],
  ["Claude-SearchBot", "Claude ricerca"],
  ["Claude-User", "Claude (su richiesta)"],
  ["PerplexityBot", "Perplexity"],
  ["Perplexity-User", "Perplexity (su richiesta)"],
  ["Google-CloudVertexBot", "Gemini / Vertex"],
  ["GoogleOther", "Google IA"],
  ["Applebot-Extended", "Apple Intelligence"],
  ["Meta-ExternalAgent", "Meta AI"],
  ["meta-externalfetcher", "Meta AI (su richiesta)"],
  ["Amazonbot", "Amazon"],
  ["DuckAssistBot", "DuckDuckGo IA"],
  ["MistralAI-User", "Mistral"],
  ["Bytespider", "ByteDance"],
  ["CCBot", "Common Crawl"],
];
const RE = BOT.map(([k]) => k).join("|");

export default async (req, context) => {
  const ua = req.headers.get("user-agent") || "";
  const hit = BOT.find(([k]) => ua.toLowerCase().includes(k.toLowerCase()));
  if (!hit) return;
  const p = new URL(req.url).pathname;
  if (p.endsWith(".html")) return; // rimanda alla pagina senza .html, che viene contata lì
  context.waitUntil(
    fetch(new URL("/api/conta", req.url), {
      method: "POST",
      headers: { "content-type": "application/json", "x-misura": "edge" },
      body: JSON.stringify({ e: "bot", p, f: hit[1] }),
    }).catch(() => {})
  );
};

export const config = {
  path: "/*",
  excludedPath: ["/fonts/*", "/img/*", "/og/*", "/*.css", "/*.js", "/*.svg", "/*.webp", "/*.png", "/*.jpg", "/*.woff2", "/api/*", "/mcp"],
  header: { "user-agent": `(${RE})` },
  onError: "bypass",
};
