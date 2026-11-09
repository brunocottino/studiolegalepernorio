// Pagine in Markdown per gli assistenti IA: se la richiesta chiede "Accept: text/markdown"
// (lo fanno Claude Code, alcuni agenti e i lettori automatici) risponde con la versione .md
// della pagina, molto più leggera dell'HTML. Gira SOLO per quelle richieste: i browser
// delle persone non mandano mai text/markdown. Se qualcosa non va, passa la pagina normale.
export default async (req) => {
  if (req.method !== "GET") return;
  const accept = (req.headers.get("accept") || "").toLowerCase();
  if (!accept.includes("text/markdown")) return;
  const url = new URL(req.url);
  const p = url.pathname.replace(/\/+$/, "");
  if (/\.[a-z0-9]+$/i.test(p)) return; // file con estensione: già serviti così come sono
  const md = new URL((p === "" ? "/index" : p) + ".md", url.origin);
  // Richiesta interna senza Accept e senza user-agent del bot: non riattiva le edge function
  const r = await fetch(md, { headers: { "x-markdown": "1" } });
  if (!r.ok || !(r.headers.get("content-type") || "").includes("markdown")) return;
  return new Response(r.body, {
    status: 200,
    headers: {
      "content-type": "text/markdown; charset=utf-8",
      "content-location": md.pathname,
      "vary": "Accept",
      "x-robots-tag": "noindex",
      "access-control-allow-origin": "*",
      "cache-control": "public, max-age=300",
    },
  });
};

export const config = {
  path: "/*",
  excludedPath: ["/fonts/*", "/img/*", "/og/*", "/api/*", "/mcp", "/statistiche*", "/.well-known/*"],
  header: { accept: "text/markdown" },
  onError: "bypass",
};
