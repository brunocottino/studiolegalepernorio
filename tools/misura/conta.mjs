// Funzione Netlify della misura senza cookie (copiata in functions/ da tools/build.py).
// POST /api/conta          registra un evento (ingresso, chiama, whatsapp, email, modulo, bot)
// GET  /api/statistiche?k= totali per fonte e per giorno, protetti da chiave
// Un blob per evento: nessun contatore da aggiornare, quindi nessuna scrittura persa.
import { getStore } from "@netlify/blobs";
import { createHash, randomUUID } from "node:crypto";

const HASH_CHIAVE = "__HASH_CHIAVE__";
const EVENTI = new Set(["ingresso", "chiama", "whatsapp", "email", "modulo", "bot"]);
const negozio = () => getStore({ name: "misura", consistency: "strong" });
const pulisci = (s, n) => String(s || "").replace(/[^\p{L}\p{N} ./_-]/gu, "").slice(0, n);
const giorno = (d) => d.toISOString().slice(0, 10);

async function registra(req) {
  let d;
  try { d = JSON.parse(await req.text()); } catch { return new Response("", { status: 400 }); }
  if (!EVENTI.has(d.e)) return new Response("", { status: 400 });
  if (d.e === "bot" && req.headers.get("x-misura") !== "edge") return new Response("", { status: 403 });
  const ora = new Date();
  const ev = { e: d.e, p: pulisci(d.p, 120), f: pulisci(d.f, 40), t: ora.toISOString() };
  await negozio().setJSON(`ev/${giorno(ora)}/${ora.getTime()}-${randomUUID().slice(0, 8)}`, ev);
  return new Response("", { status: 204 });
}

async function statistiche(url) {
  const k = url.searchParams.get("k") || "";
  if (createHash("sha256").update(k).digest("hex") !== HASH_CHIAVE) return new Response("Chiave non valida", { status: 403 });
  const giorni = Math.min(Math.max(parseInt(url.searchParams.get("giorni") || "30", 10) || 30, 1), 120);
  const st = negozio();
  const oggi = new Date();
  const out = { giorni, dal: null, eventi: [] };
  for (let i = giorni - 1; i >= 0; i--) {
    const g = giorno(new Date(oggi.getTime() - i * 864e5));
    if (!out.dal) out.dal = g;
    const { blobs } = await st.list({ prefix: `ev/${g}/` });
    const lotti = await Promise.all(blobs.map((b) => st.get(b.key, { type: "json" })));
    for (const ev of lotti) if (ev) out.eventi.push(ev);
  }
  return Response.json(out, { headers: { "cache-control": "no-store" } });
}

export default async (req) => {
  const url = new URL(req.url);
  if (req.method === "POST" && url.pathname === "/api/conta") return registra(req);
  if (req.method === "GET" && url.pathname === "/api/statistiche") return statistiche(url);
  return new Response("", { status: 405 });
};

export const config = { path: ["/api/conta", "/api/statistiche"] };
