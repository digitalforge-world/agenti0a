---
name: analyse-entreprise
description: Recherche et synthèse d'informations publiques sur une entreprise (activité, modèle business, performances économiques, maturité digitale, concurrence, signaux de risque et opportunités) avec production d'un rapport structuré et de recommandations actionnables. Utiliser ce skill quand l'utilisateur fournit un nom d'entreprise et demande une analyse détaillée orientée business/économie/stratégie digitale, y compris les contacts publics (email, téléphone, réseaux sociaux, site officiel).
---

# Analyse Entreprise

## Objectif

Produire un rapport clair, vérifiable et orienté décision pour une entreprise donnée, en privilégiant les sources officielles et récentes.

## Workflow opérationnel

1. **Cadrer la demande**
   - Confirmer le nom exact de l'entreprise et le pays principal d'activité.
   - Vérifier si l'utilisateur veut une analyse globale ou un focus (finance, marketing digital, expansion, etc.).

2. **Collecter les données web**
   - Prioriser : site officiel, rapports annuels/financiers, registres publics, presse économique reconnue.
   - Compléter avec : profils sociaux officiels, pages investisseurs, base d'emploi/carrières, partenaires.
   - Capturer systématiquement la date de chaque source.

3. **Extraire les informations clés**
   - **Identité** : nom légal, siège, secteur, produits/services, zones géographiques.
   - **Business** : proposition de valeur, segments clients, pricing, canaux, partenariats.
   - **Économie/finance** : CA, croissance, marge (si disponible), levées, dettes, rentabilité, tendances.
   - **Digital** : e-commerce, SEO, présence sociale, acquisition, UX, automation, data/IA.
   - **Marché** : concurrence, positionnement, menaces externes, régulation.
   - **Contacts publics** : email(s), téléphone(s), formulaire de contact, réseaux sociaux officiels.

4. **Évaluer et noter**
   - Utiliser une échelle simple (1-5) sur : santé économique, maturité digitale, efficacité commerciale, capacité d'exécution.
   - Justifier chaque note avec faits + sources.

5. **Rédiger les recommandations**
   - Produire au moins 10 recommandations priorisées :
     - 0-90 jours (quick wins)
     - 3-12 mois (chantiers structurants)
     - 12+ mois (avantages durables)
   - Pour chaque recommandation : impact attendu, effort estimé, risque principal, KPI de suivi.

## Format de sortie (obligatoire)

Suivre strictement cette structure :

1. **Résumé exécutif (8-12 lignes)**
2. **Fiche entreprise**
3. **Analyse business détaillée**
4. **Analyse économique et financière**
5. **Diagnostic digital**
6. **SWOT synthétique**
7. **Plan d'amélioration priorisé** (tableau impact/effort)
8. **Contacts publics et réseaux sociaux**
9. **Sources utilisées** (URL + date)

## Qualité et fiabilité

- Toujours distinguer clairement : **fait vérifié** vs **inférence**.
- Ne jamais inventer de chiffre financier.
- Si une donnée est introuvable, écrire explicitement : "Non publié / non trouvé dans les sources consultées".
- Préférer des sources de moins de 12 mois pour l'actualité économique.

## Conformité

- N'inclure que des données de contact **publiquement disponibles**.
- Ne pas fournir de données personnelles non publiques.
- En cas de doute, garder uniquement les coordonnées génériques de l'entreprise.

## Ressources

- Utiliser `references/report-template.md` comme canevas de rapport final.
- Utiliser `references/research-checklist.md` pour ne manquer aucun angle d'analyse.
