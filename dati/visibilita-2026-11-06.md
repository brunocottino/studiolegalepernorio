# Misura della visibilità: 6 novembre 2026 (punto di partenza)

Motore: la ricerca web di Claude (Anthropic). Ho fatto domande da cliente senza nominare lo Studio, più due ricerche per nome.

| Domanda | Studio citato? | Chi viene citato al suo posto |
|---|---|---|
| avvocato separazione Vigevano | No | dequo.it (Avv. Adriana Ciappa), virgilio.it (elenco di 84 studi), Studio Lenchi |
| avvocato divorzista Lomellina | No | Avv. Liliana L'Aurora (Lomello), dequo.it |
| avvocato successioni eredità Vigevano | No | dequo.it (Avv. Valentina Contini, Avv. Adriana Ciappa), Di Caro, Pirani, Sisaro |
| avvocato civilista Mortara | No | Nessun avvocato di Mortara: "nessun avvocato civilista trovato" |
| avvocato sfratto morosità Vigevano | No | Guide generiche (money.it, condominioweb, dequo) |
| Studio Legale Pernorio Vigevano | Solo tramite lawzana.com | La scheda Lawzana descrive lo Studio come "civile e penale" |
| "Pernorio" avvocato Daniela (ricerca estesa) | Sì | Il sito (home, 3 guide), Virgilio e Pagine Bianche ("Avvocato pernorio daniela"), elenco dell'Ordine di Pavia (iscrizione 22/01/2014) |

## Cosa significa

1. Il sito è indicizzato, ma per le domande generiche le IA citano **gli elenchi** (Dequo, Virgilio, Lawzana), non i siti degli studi. È lo stesso schema dei dati Yext (42% delle citazioni viene dagli elenchi).
2. **Dequo** è la fonte più citata per Vigevano e lo Studio non c'è. Iscriversi è la prima mossa: https://www.dequo.it/area-personale/registrazione-avvocato
3. **Lawzana** ha dati sbagliati ("civile e penale") e va corretta o rivendicata.
4. **Virgilio e Pagine Bianche** hanno il nome scritto "Avvocato pernorio daniela", senza la parola "Studio Legale" e forse senza il sito. Va uniformato ai dati canonici di `ELENCHI.md`.
5. **Mortara**: l'IA dice che "non c'è nessun avvocato civilista". È lo spazio libero più evidente, e la pagina `/avvocato-mortara` lo copre già. Il 6/11 l'ho segnalata a IndexNow, insieme alle altre 65 pagine.

Da ripetere ogni mese con le stesse domande. Con le chiavi API c'è anche `tools/visibilita_ia.py`.
