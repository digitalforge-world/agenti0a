#!/usr/bin/env python3
"""CLI simple d'analyse d'entreprise (business, économique, digital)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read().decode("utf-8", errors="ignore")


def ddg_search(query: str, limit: int = 8) -> list[SearchResult]:
    encoded = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={encoded}"
    html = fetch(url)

    pattern = re.compile(
        r'<a[^>]*class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>.*?'
        r'<a[^>]*class="result__snippet"[^>]*>(?P<snippet>.*?)</a>',
        re.DOTALL,
    )

    results: list[SearchResult] = []
    for m in pattern.finditer(html):
        raw_url = unescape(re.sub(r"<.*?>", "", m.group("href"))).strip()
        title = unescape(re.sub(r"<.*?>", "", m.group("title"))).strip()
        snippet = unescape(re.sub(r"<.*?>", "", m.group("snippet"))).strip()

        parsed = urllib.parse.urlparse(raw_url)
        if parsed.netloc == "duckduckgo.com" and parsed.path == "/l/":
            qs = urllib.parse.parse_qs(parsed.query)
            if "uddg" in qs:
                raw_url = qs["uddg"][0]

        if raw_url.startswith("http"):
            results.append(SearchResult(title=title, url=raw_url, snippet=snippet))

        if len(results) >= limit:
            break

    return results


def dedupe_results(results: list[SearchResult]) -> list[SearchResult]:
    seen: set[str] = set()
    unique: list[SearchResult] = []
    for r in results:
        key = r.url.split("?")[0].rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    return unique


def extract_contacts(text: str) -> dict[str, list[str]]:
    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
    phones = sorted(
        set(
            p.strip()
            for p in re.findall(r"(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}", text)
            if len(re.sub(r"\D", "", p)) >= 8
        )
    )
    socials = sorted(
        set(
            s
            for s in re.findall(r"https?://(?:www\.)?(?:linkedin|twitter|x|facebook|instagram|youtube)\.com/[^\s)\]>'\"]+", text, re.I)
        )
    )
    return {"emails": emails[:15], "phones": phones[:15], "socials": socials[:20]}


def infer_business_points(results: list[SearchResult]) -> list[str]:
    points: list[str] = []
    corpus = " ".join([f"{r.title} {r.snippet}" for r in results]).lower()

    rules = [
        ("saas", "L'entreprise semble avoir une composante SaaS / logiciel."),
        ("e-commerce", "Le modèle e-commerce semble important dans la génération de revenus."),
        ("funding", "Des signaux de financement/levée de fonds sont présents dans les sources."),
        ("growth", "Les sources mentionnent des éléments de croissance ou d'expansion."),
        ("partnership", "Des partenariats stratégiques sont mentionnés publiquement."),
        ("ai", "La dimension data/IA semble présente dans la proposition de valeur."),
    ]
    for token, msg in rules:
        if token in corpus:
            points.append(msg)

    if not points:
        points.append("Les signaux business sont partiels : approfondir avec rapports officiels et page investisseurs.")
    return points


def score_section(results: list[SearchResult], contacts: dict[str, list[str]]) -> dict[str, int]:
    n = len(results)
    digital = min(5, 2 + (1 if contacts["socials"] else 0) + (1 if n >= 8 else 0))
    economic = min(5, 2 + (1 if any("investor" in (r.url + r.title).lower() for r in results) else 0) + (1 if n >= 6 else 0))
    commercial = min(5, 2 + (1 if any("pricing" in (r.url + r.snippet).lower() for r in results) else 0) + (1 if n >= 5 else 0))
    execution = min(5, 2 + (1 if any("careers" in (r.url + r.title).lower() for r in results) else 0) + (1 if n >= 7 else 0))
    return {
        "sante_economique": economic,
        "maturite_digitale": digital,
        "efficacite_commerciale": commercial,
        "capacite_execution": execution,
    }


def build_report(company: str, country: str, results: list[SearchResult]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    contacts = extract_contacts("\n".join([f"{r.title}\n{r.snippet}\n{r.url}" for r in results]))
    scores = score_section(results, contacts)
    points = infer_business_points(results)

    recs = [
        ("0-90 jours", "Mettre en place un tableau de bord KPI (CA, marge, CAC, conversion).", "CA mensuel, marge brute, taux conversion"),
        ("0-90 jours", "Auditer le tunnel digital (SEO, landing pages, formulaires de contact).", "Trafic organique, leads qualifiés"),
        ("3-12 mois", "Structurer une stratégie de contenu orientée différenciation sectorielle.", "Part de voix, MQL, engagement social"),
        ("3-12 mois", "Déployer CRM + automatisations marketing/vente.", "Cycle de vente, taux de closing"),
        ("12+ mois", "Lancer un plan d'expansion géographique/segmentaire basé sur données.", "Nouveaux revenus par segment"),
    ]

    top_sources = "\n".join([f"- {r.title} — {r.url}" for r in results]) or "- Aucune source trouvée"
    emails = "\n".join([f"- {e}" for e in contacts["emails"]]) or "- Non trouvé"
    phones = "\n".join([f"- {p}" for p in contacts["phones"]]) or "- Non trouvé"
    socials = "\n".join([f"- {s}" for s in contacts["socials"]]) or "- Non trouvé"

    rec_lines = "\n".join([f"- **{horizon}**: {action} *(KPI: {kpi})*" for horizon, action, kpi in recs])
    bp_lines = "\n".join([f"- {p}" for p in points])

    return textwrap.dedent(
        f"""
        # Rapport entreprise: {company}
        _Date d'analyse: {timestamp}_

        ## 1) Résumé exécutif
        Cette analyse synthétise les informations publiques trouvées pour **{company}** ({country}).
        Le rapport met l'accent sur les axes business, économiques et digitaux, puis propose un plan d'amélioration priorisé.

        ## 2) Fiche entreprise
        - Nom recherché: {company}
        - Pays cible: {country}
        - Nombre de sources analysées: {len(results)}

        ## 3) Analyse business
        {bp_lines}

        ## 4) Analyse économique (indications)
        - Santé économique (1-5): **{scores['sante_economique']}**
        - Efficacité commerciale (1-5): **{scores['efficacite_commerciale']}**
        - Capacité d'exécution (1-5): **{scores['capacite_execution']}**
        - Note: ces scores sont indicatifs et doivent être validés avec des documents financiers officiels.

        ## 5) Diagnostic digital
        - Maturité digitale (1-5): **{scores['maturite_digitale']}**
        - Présence sociale détectée: {"oui" if contacts['socials'] else "limitée/non détectée"}

        ## 6) Recommandations prioritaires
        {rec_lines}

        ## 7) Contacts publics détectés
        ### Emails
        {emails}

        ### Téléphones
        {phones}

        ### Réseaux sociaux
        {socials}

        ## 8) Sources
        {top_sources}
        """
    ).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyse publique d'une entreprise et génération d'un rapport Markdown.")
    parser.add_argument("company", help="Nom de l'entreprise à analyser")
    parser.add_argument("--country", default="France", help="Pays principal (défaut: France)")
    parser.add_argument("--max-results", type=int, default=10, help="Nombre max de résultats web")
    parser.add_argument("--output", default="rapport_entreprise.md", help="Fichier Markdown de sortie")
    parser.add_argument("--json", action="store_true", help="Sauvegarder aussi les résultats bruts en JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queries = [
        f"{args.company} official site",
        f"{args.company} investors revenue growth",
        f"{args.company} linkedin",
        f"{args.company} contact email phone",
        f"{args.company} digital strategy ecommerce",
    ]

    all_results: list[SearchResult] = []
    for q in queries:
        try:
            all_results.extend(ddg_search(q, limit=max(3, args.max_results // 2)))
        except Exception as exc:
            print(f"[warn] recherche échouée pour '{q}': {exc}", file=sys.stderr)

    results = dedupe_results(all_results)[: args.max_results]
    report = build_report(args.company, args.country, results)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    if args.json:
        payload = [r.__dict__ for r in results]
        with open(args.output.replace(".md", ".json"), "w", encoding="utf-8") as jf:
            json.dump(payload, jf, ensure_ascii=False, indent=2)

    print(f"Rapport généré: {args.output}")
    print(f"Sources exploitées: {len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
