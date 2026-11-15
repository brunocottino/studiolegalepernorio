// Chi chiede una pagina con "Accept: text/markdown" (assistenti e agenti IA) riceve
// la versione Markdown già pronta (/pagina.md) allo stesso indirizzo.
// Gira SOLO quando la richiesta contiene quell'intestazione: i browser delle persone
// non la mandano mai, quindi per loro non viene nemmeno avviata.
export default async (req) => {
  if (req.method !== "GET") return;
  const accept = (req.headers.get("accept") || "").toLowerCase();
  const md = accept.indexOf("text/markdown"), html = accept.indexOf("text/html");
  if (md < 0 || (html >= 0 && html < md)) return; // preferisce l'HTML
  const u = new URL(req.url);
  const p = u.pathname.replace(/\.html$/, "").replace(/\/+$/, "") || "/index";
  if (/\.[a-z0-9]+$/i.test(p)) return; // file (immagini, .md, .json): nessun intervento
  const r = await fetch(new URL(p + ".md", u.origin), { headers: { accept: "*/*" } });
  if (!r.ok || !(r.headers.get("content-type") || "").includes("markdown")) return;
  return new Response(r.body, {
    status: 200,
    headers: {
      "content-type": "text/markdown; charset=utf-8",
      "vary": "Accept",
      "x-robots-tag": "noindex",
      "access-control-allow-origin": "*",
      "link": `<${u.origin}${u.pathname}>; rel="canonical"`,
      "cache-control": "public, max-age=600",
    },
  });
};

export const config = {
  path: "/*",
  excludedPath: ["/fonts/*", "/img/*", "/og/*", "/api/*", "/mcp", "/statistiche*", "/*.md", "/*.css", "/*.js", "/*.json", "/*.txt", "/*.xml"],
  header: { accept: "text/markdown" },
  onError: "bypass",
};
