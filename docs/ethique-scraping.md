# Note sur l'éthique de la collecte

Collecter une donnée qui n'existe pas sous forme de dataset propre est courant en
data — mais doit se faire **de façon responsable**.

## Choix : API plutôt que scraping

Ce projet utilise l'**API publique CheapShark** (agrégateur de bons plans jeux)
plutôt que de scraper un site marchand. C'est le bon réflexe quand une API existe :

- **Légal & stable** : usage prévu par le fournisseur, format structuré (JSON),
  pas de contournement de conditions d'utilisation.
- **Robuste** : pas de casse au moindre changement de HTML.
- **Respectueux** : pas de charge inutile sur un site tiers.

## Si l'on devait scraper (règles appliquées)

En l'absence d'API, un scraping éthique respecte :

1. **`robots.txt`** — vérifier les chemins autorisés/interdits avant toute requête.
2. **Conditions d'utilisation** du site (certains interdisent explicitement le scraping).
3. **User-Agent identifiable** — ne pas se faire passer pour un navigateur anonyme.
4. **Débit maîtrisé** — délais entre requêtes, pas de parallélisme agressif (ne pas
   surcharger le serveur).
5. **Données personnelles** — ne jamais collecter de données perso ; se limiter aux
   informations publiques et factuelles (ici : titres, prix, réductions).
6. **Cache & fraîcheur** — rafraîchir raisonnablement (ex. 1×/jour), pas en continu.

## Rafraîchissement

La collecte (`src/fetch_deals.py`) est **rejouable** et pensée pour une exécution
planifiée (cron / tâche planifiée) — typiquement une fois par jour, suffisant pour
un suivi de prix.
