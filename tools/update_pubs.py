#!/usr/bin/env python3
"""PubMed'den yeni yayın adaylarını bulur ve pubs.js'ye eklemek üzere hazırlar.

Kullanım:
  python3 tools/update_pubs.py                 # son 2 yılı tarar, adayları pubs-candidates.json'a yazar ve özetler
  python3 tools/update_pubs.py --since 2020    # taramayı 2020'den başlatır
  python3 tools/update_pubs.py --apply         # pubs-candidates.json'daki "keep": true kayıtları pubs.js'ye ekler
  python3 tools/update_pubs.py --email siz@istanbul.edu.tr --api-key ...   # NCBI kibar kullanım (isteğe bağlı)

Akış: her ekip üyesi için PubMed'de yazar adı + "Istanbul" adres araması yapılır (E-utilities esearch),
pubs.js'de olmayan PMID'ler efetch ile çekilir, adaylar adres özetiyle birlikte pubs-candidates.json'a yazılır.
Adaş yazarları ayıklamak için dosyayı gözden geçirip uygun kayıtlarda "keep": true yapın, sonra --apply ile ekleyin.
jif, aynı dergideki mevcut kayıtlardan alınır; dergi listede yoksa 0 yazılır ve uyarı verilir (elle doldurun).
Gereksinim yok (standart kütüphane). Ağ erişimi gerekir.
"""
import argparse, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBS_PATH = os.path.join(ROOT, "pubs.js")
CAND_PATH = os.path.join(ROOT, "pubs-candidates.json")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Ekip üyeleri: sitedeki ad -> PubMed yazar biçimleri (soyad + baş harfler; Türkçe harfler ASCII'ye çevrilir)
MEMBERS = {
    "Filiz Akyüz": ["Akyuz F"],
    "Fatih Beşışık": ["Besisik F", "Besisik SF"],
    "Kadir Demir": ["Demir K"],
    "Bilger Çavuş": ["Cavus B"],
    "Besim Fazıl Ağargün": ["Agargun BF", "Agargun B"],
    "Ege Akcasu": ["Akcasu E"],
    "Ersel Bilgin": ["Bilgin E"],
    "Asım Gurbanov": ["Gurbanov A"],
    "Nijat Nasirov": ["Nasirov N"],
    "Sabuhi Mammadov": ["Mammadov S"],
    "Pelin Telli": ["Telli P"],
}
AFFIL_HINTS = ["istanbul university", "istanbul faculty of medicine", "istanbul tip", "istanbul üniversitesi", "capa", "çapa"]


def ascii_fold(s):
    s = s.replace("ı", "i").replace("İ", "I")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def load_pubs():
    s = open(PUBS_PATH, encoding="utf-8").read()
    head = s[:s.index("[")]
    body = json.loads(s[s.index("["):s.rindex("]") + 1])
    return head, body


def save_pubs(head, pubs):
    out = head + json.dumps(pubs, ensure_ascii=False, indent=0).replace("\n]", "\n]") + ";\n"
    open(PUBS_PATH, "w", encoding="utf-8").write(out)


def get(url, params, retries=3):
    q = urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            with urllib.request.urlopen(url + "?" + q, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def esearch(term, mindate, common):
    params = dict(db="pubmed", term=term, retmax=500, retmode="json", mindate=str(mindate), maxdate="3000", datetype="pdat", **common)
    data = json.loads(get(EUTILS + "esearch.fcgi", params))
    return data.get("esearchresult", {}).get("idlist", [])


def efetch(pmids, common):
    out = []
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i + 100]
        xml = get(EUTILS + "efetch.fcgi", dict(db="pubmed", id=",".join(chunk), retmode="xml", **common))
        out.extend(parse_pubmed_xml(xml))
        time.sleep(0.4)
    return out


def pub_type(types):
    t = " ".join(types).lower()
    if "case reports" in t:
        return "Case"
    if "review" in t or "meta-analysis" in t or "systematic" in t:
        return "Review"
    if "letter" in t or "comment" in t or "editorial" in t:
        return "Letter"
    return "Article"


def parse_pubmed_xml(xml):
    """PubmedArticleSet XML -> kayıt sözlükleri (pmid, doi, title, journal, year, authors, type, affiliations, author_list)."""
    root = ET.fromstring(xml)
    recs = []
    for art in root.iter("PubmedArticle"):
        pmid = (art.findtext("MedlineCitation/PMID") or "").strip()
        a = art.find("MedlineCitation/Article")
        if a is None:
            continue
        title = "".join(a.find("ArticleTitle").itertext()).strip().rstrip(".") if a.find("ArticleTitle") is not None else ""
        journal = (a.findtext("Journal/ISOAbbreviation") or a.findtext("Journal/Title") or "").strip()
        year = a.findtext("Journal/JournalIssue/PubDate/Year") or a.findtext("Journal/JournalIssue/PubDate/MedlineDate", "")[:4]
        year = int(year) if year and year.isdigit() else 0
        doi = ""
        for idn in art.iter("ArticleId"):
            if idn.get("IdType") == "doi":
                doi = (idn.text or "").strip()
        authors, affs = [], []
        for au in a.iter("Author"):
            ln, ini = au.findtext("LastName"), au.findtext("Initials")
            if ln:
                authors.append(f"{ln} {ini}".strip() if ini else ln)
            for af in au.iter("Affiliation"):
                if af.text:
                    affs.append(af.text.strip())
        types = [pt.text or "" for pt in a.iter("PublicationType")]
        recs.append({"pmid": pmid, "doi": doi, "title": title, "journal": journal, "year": year, "author_list": authors,
                     "type": pub_type(types), "affiliations": affs})
    return recs


def author_string(author_list):
    if len(author_list) <= 3:
        return ", ".join(author_list)
    return ", ".join(author_list[:3]) + ", et al."


def match_members(author_list):
    found = []
    folded = [ascii_fold(x).lower() for x in author_list]
    for name, forms in MEMBERS.items():
        for f in forms:
            if ascii_fold(f).lower() in folded:
                found.append(name)
                break
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=int, help="tarama başlangıç yılı (varsayılan: pubs.js'deki son yıl - 1)")
    ap.add_argument("--apply", action="store_true", help="pubs-candidates.json'daki keep=true kayıtları pubs.js'ye ekle")
    ap.add_argument("--email", default="bfagargun@istanbul.edu.tr")
    ap.add_argument("--api-key", default=os.environ.get("NCBI_API_KEY", ""))
    args = ap.parse_args()
    head, pubs = load_pubs()
    known = {p["pmid"] for p in pubs}
    jif_by_journal = {}
    for p in pubs:
        jif_by_journal.setdefault(p["journal"].lower(), p.get("jif", 0))

    if args.apply:
        cands = json.load(open(CAND_PATH, encoding="utf-8"))
        added = 0
        for c in cands:
            if not c.get("keep") or c["pmid"] in known:
                continue
            rec = {k: c[k] for k in ["pmid", "doi", "title", "journal", "year", "jif", "members", "authors", "type"]}
            pubs.append(rec)
            known.add(c["pmid"])
            added += 1
        save_pubs(head, pubs)
        print(f"{added} kayıt eklendi; toplam {len(pubs)}. Ana sayfadaki yayın sayısını ve index.html'deki 'Yayınlar (n)' değerlerini kontrol edin.")
        return

    since = args.since or (max(p["year"] for p in pubs) - 1)
    common = {"tool": "capagastro-site", "email": args.email}
    if args.api_key:
        common["api_key"] = args.api_key
    new_ids = {}
    for name, forms in MEMBERS.items():
        term = "(" + " OR ".join(f'"{f}"[Author]' for f in forms) + ") AND Istanbul[Affiliation]"
        ids = esearch(term, since, common)
        fresh = [i for i in ids if i not in known]
        for i in fresh:
            new_ids.setdefault(i, set()).add(name)
        print(f"{name}: {len(ids)} sonuç, {len(fresh)} yeni")
        time.sleep(0.4)
    if not new_ids:
        print("Yeni aday yok.")
        return
    recs = efetch(sorted(new_ids), common)
    cands = []
    for r in recs:
        members = match_members(r["author_list"]) or sorted(new_ids.get(r["pmid"], []))
        affil_ok = any(h in " ".join(r["affiliations"]).lower() for h in AFFIL_HINTS)
        jif = jif_by_journal.get(r["journal"].lower(), 0)
        cands.append({
            "keep": bool(affil_ok),
            "pmid": r["pmid"], "doi": r["doi"], "title": r["title"], "journal": r["journal"], "year": r["year"],
            "jif": jif, "members": members, "authors": author_string(r["author_list"]), "type": r["type"],
            "affiliation_hint": affil_ok, "affiliations": r["affiliations"][:3],
            "note": ("" if jif else "jif bilinmiyor, elle doldurun. ") + ("" if affil_ok else "Adres İstanbul ünitesini göstermiyor; adaş olabilir.")
        })
    cands.sort(key=lambda c: (-c["year"], c["journal"]))
    json.dump(cands, open(CAND_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(cands)} aday yazıldı: {CAND_PATH}")
    for c in cands:
        flag = "+" if c["keep"] else "?"
        print(f" {flag} {c['pmid']} {c['year']} {c['journal']}: {c['title'][:70]} [{', '.join(c['members'])}]{' | ' + c['note'] if c['note'] else ''}")
    print("\nGözden geçirip uygun kayıtlarda keep: true bırakın, sonra: python3 tools/update_pubs.py --apply")


if __name__ == "__main__":
    main()
