# Analyse Entreprise CLI

Application CLI qui génère un **rapport business / économique / digital** à partir du nom d'une entreprise, en se basant sur des informations publiques trouvées sur internet.

## Prérequis

- Python 3.10+
- Accès internet

## Exécution rapide

```bash
python app.py "Nom Entreprise"
```

Exemple:

```bash
python app.py "Airbnb" --country "États-Unis" --max-results 12 --output rapport_airbnb.md --json
```

## Options

- `--country` : pays principal (défaut: `France`)
- `--max-results` : nombre maximal de résultats web retenus
- `--output` : chemin du fichier markdown généré
- `--json` : sauvegarde aussi les résultats bruts dans un fichier JSON

## Fichier généré

Par défaut, l'application crée `rapport_entreprise.md` avec:

- résumé exécutif
- analyse business
- diagnostic économique indicatif
- analyse digitale
- recommandations prioritaires
- contacts publics détectés (emails, téléphones, réseaux sociaux)
- liste des sources

## Limites importantes

- Les données financières sont indicatives si les rapports officiels ne sont pas trouvés.
- Toujours valider les informations critiques avec les sources primaires (rapport annuel, site investisseurs, autorités de régulation).
