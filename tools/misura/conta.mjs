// Funzione Netlify della misura senza cookie (copiata in functions/ da tools/build.py).
// POST /api/conta          registra un evento (ingresso, chiama, whatsapp, email, modulo, bot)
// GET  /api/statistiche?k= totali per fonte e per giorno, protetti da chiave
// Un blob per evento: nessun contatore da aggiornare, quindi nessuna scrittura persa.
import { getStore } from "@netlify/blobs";
import { createHash, randomUUID } from "node:crypto";

const HASH_CHIAVE = "__HASH_CHIAVE__";
const EVENTI = new Set(["ingresso", "chiama", "whatsapp", "email", "modulo", "bot"]);
const negozio = () => getStore({ name: "misura", consistency: "strong" });
const pulisci = (s, n) => String(s || "").replace(/[^\p{L}\p{N} ./_()-]/gu, "").slice(0, n);
const giorno = (d) => d.toISOString().slice(0, 10);

// Regione di chi visita, ricavata da Netlify dall'indirizzo IP al momento della richiesta.
// L'indirizzo IP non viene letto né conservato da questa funzione: resta solo il nome della regione.
const REGIONI = { 21: "Piemonte", 23: "Valle d'Aosta", 25: "Lombardia", 32: "Trentino-Alto Adige", 34: "Veneto", 36: "Friuli-Venezia Giulia",
  42: "Liguria", 45: "Emilia-Romagna", 52: "Toscana", 55: "Umbria", 57: "Marche", 62: "Lazio", 65: "Abruzzo", 67: "Molise", 72: "Campania",
  75: "Puglia", 77: "Basilicata", 78: "Calabria", 82: "Sicilia", 88: "Sardegna" };
const ZONA = new Set(["vigevano", "mortara", "gambolo", "garlasco", "cassolnovo", "cilavegna", "abbiategrasso", "parona", "robbio", "tromello",
  "dorno", "mede", "gravellona lomellina", "sannazzaro de burgondi", "sartirana lomellina", "ozzero", "morimondo", "cassinetta di lugagnano"]);
const piano = (s) => String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f']/g, "").trim();
export function zona(geo) {
  if (!geo || !geo.country || !geo.country.code) return "";
  if (geo.country.code !== "IT") return "Estero";
  const cod = String((geo.subdivision && geo.subdivision.code) || "").replace(/^IT-/, "");
  const reg = REGIONI[cod] || (geo.subdivision && geo.subdivision.name) || "Italia";
  if (reg !== "Lombardia") return reg;
  const c = piano(geo.city);
  if (ZONA.has(c)) return "Lombardia - Vigevano e Lomellina";
  if (c === "pavia") return "Lombardia - Pavia";
  return "Lombardia";
}

async function registra(req, context) {
  let d;
  try { d = JSON.parse(await req.text()); } catch { return new Response("", { status: 400 }); }
  if (!EVENTI.has(d.e)) return new Response("", { status: 400 });
  if (d.e === "bot" && req.headers.get("x-misura") !== "edge") return new Response("", { status: 403 });
  const ora = new Date();
  const ev = { e: d.e, p: pulisci(d.p, 120), f: pulisci(d.f, 40), t: ora.toISOString() };
  if (d.e !== "bot") {
    try { ev.z = pulisci(zona(context && context.geo), 40); } catch { ev.z = ""; }
    if (d.e !== "ingresso") ev.i = pulisci(d.i, 120);
  }
  // I dati stanno anche nella chiave: le statistiche si leggono con un solo elenco, senza aprire ogni evento
  const enc = encodeURIComponent;
  const chiave = `ev/${giorno(ora)}/${ora.getTime()}-${randomUUID().slice(0, 8)}~${enc(ev.e)}~${enc(ev.f)}~${enc(ev.p)}~${enc(ev.z || "")}~${enc(ev.i || "")}`;
  await negozio().setJSON(chiave.slice(0, 590), ev);
  return new Response(null, { status: 204 });
}

async function statistiche(url) {
  const k = url.searchParams.get("k") || "";
  if (createHash("sha256").update(k).digest("hex") !== HASH_CHIAVE) return new Response("Chiave non valida", { status: 403 });
  const giorni = Math.min(Math.max(parseInt(url.searchParams.get("giorni") || "30", 10) || 30, 1), 240);
  const st = negozio();
  const oggi = new Date();
  const date = [];
  for (let i = giorni - 1; i >= 0; i--) date.push(giorno(new Date(oggi.getTime() - i * 864e5)));
  const out = { giorni, dal: date[0], al: date[date.length - 1], eventi: [] };
  const leggi = async (g) => {
    const { blobs } = await st.list({ prefix: `ev/${g}/` });
    return Promise.all(blobs.map(async (b) => {
      const parti = b.key.split("/").pop().split("~");
      if (parti.length >= 4) {
        const dec = decodeURIComponent;
        // dal 15/11/2026 la chiave porta anche regione (z) e pagina d'ingresso (i); le chiavi più vecchie hanno 4 parti
        return { e: dec(parti[1]), f: dec(parti[2]), p: dec(parti[3]), z: dec(parti[4] || ""), i: dec(parti[5] || ""), t: new Date(+parti[0].split("-")[0]).toISOString() };
      }
      return st.get(b.key, { type: "json" }); // eventi salvati prima del 08/11/2026
    }));
  };
  for (let i = 0; i < date.length; i += 15) {
    const lotti = await Promise.all(date.slice(i, i + 15).map(leggi));
    for (const l of lotti) for (const ev of l) if (ev) out.eventi.push(ev);
  }
  return Response.json(out, { headers: { "cache-control": "no-store" } });
}

export default async (req, context) => {
  const url = new URL(req.url);
  if (req.method === "POST" && url.pathname === "/api/conta") return registra(req, context);
  if (req.method === "GET" && url.pathname === "/api/statistiche") return statistiche(url);
  return new Response("", { status: 405 });
};

export const config = { path: ["/api/conta", "/api/statistiche"] };
