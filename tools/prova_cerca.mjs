// Prova della ricerca: domande scritte come le scriverebbe un cliente, e la pagina che deve uscire tra le prime tre.
// Uso: node tools/prova_cerca.mjs [-v]   (dopo python3 tools/build.py)
import { readFileSync } from 'node:fs';
const src = readFileSync(new URL('../dist/cerca.js', import.meta.url), 'utf8');
const creaMotore = new Function(src.slice(0, src.indexOf('(function(){')) + ';return creaMotore')();
const cerca = creaMotore(JSON.parse(readFileSync(new URL('../dist/cerca-testo.json', import.meta.url), 'utf8')));
const PROVE = [
 ['quanto costa separarsi', 'guida-costo-separazione-consensuale'],
 ['il padrone di casa non mi restituisce la caparra', 'guida-deposito-cauzionale-affitto'],
 ['mio padre è morto e aveva debiti', 'guida-eredita-con-debiti'],
 ['ho preso una multa con autovelox', 'guida-multa-autovelox-2026'],
 ['alimenti per i figli', 'guida-assegno-mantenimento-figli'],
 ['mi hanno licenziato', 'guida-licenziamento-cosa-fare'],
 ['possono pignorarmi la pensione', 'guida-pignoramento-stipendio-pensione'],
 ['inquilino non paga affitto', 'guida-sfratto-per-morosita'],
 ['dopo quanto tempo posso divorziare', 'guida-divorzio-tempi'],
 ['chi resta in casa dopo la separazione', 'guida-casa-familiare-separazione'],
 ['testamento scritto a mano', 'guida-testamento-olografo'],
 ['ho prestato soldi a un amico', 'guida-prestito-tra-privati'],
 ['incidente in macchina assicurazione non paga', 'guida-incidente-stradale-cosa-fare'],
 ['delibera assemblea condominio sbagliata', 'guida-impugnare-delibera-condominiale'],
 ['convivenza finita cosa mi spetta', 'guida-fine-convivenza-diritti'],
 ['madre anziana con demenza', 'amministrazione-di-sostegno'],
 ['debito con la finanziaria pagare meno', 'saldo-e-stralcio'],
 ['terreno usato da vent anni', 'usucapione'],
 ['quanto costa un avvocato', 'costi-avvocato'],
 ['colloquio in videochiamata', 'colloquio-online'],
 ['avvocato a Mortara', 'avvocato-mortara'],
 ['quote eredità senza testamento', 'strumento-calcolo-quote-eredita'],
 ['tasse sulla successione', 'successione'],
 ['affidamento condiviso', 'guida-affidamento-figli-condiviso-esclusivo'],
 ['il proprietario può entrare in casa mia', 'guida-diritti-inquilino'],
 ['mediazione o negoziazione assistita', 'guida-negoziazione-assistita-o-mediazione'],
 ['sciogliere unione civile', 'guida-scioglimento-unione-civile'],
 ['domiciliazione tribunale pavia', 'domiciliazioni'],
 ['orari dello studio', 'contatti'],
 ['documenti per la separazione', 'strumento-checklist-separazione'],
];
const v = process.argv.includes('-v'); let ok = 0; const male = [];
for (const [q, atteso] of PROVE) {
 const r = cerca(q, 3, 1), pos = r.findIndex(x => x.pagina.includes(atteso));
 if (pos >= 0) ok++; else male.push(q + ' -> ' + (r.map(x => x.pagina.split('/').pop()).join(', ') || 'nessun risultato'));
 if (v) console.log((pos >= 0 ? 'ok ' + (pos + 1) : 'NO  ') + ' ' + q + '  =>  ' + r.map(x => x.pagina.split('/').pop() + (x.sezione ? ' [' + x.sezione.slice(0, 40) + ']' : '')).join(' | '));
}
console.log(JSON.stringify({ prove: PROVE.length, riuscite: ok, fallite: male }));
