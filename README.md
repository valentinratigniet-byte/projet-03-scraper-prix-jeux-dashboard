# Projet 03 — Suivi de prix de jeux vidéo + mini web app

> Suivre les prix et repérer les meilleures affaires demande de **collecter,
> structurer et visualiser** une donnée qui n'existe pas sous forme de dataset
> propre. Ce projet collecte des bons plans jeux, les stocke, et les expose dans une
> **web app** avec filtres réactifs et mise en avant des meilleures offres.

**👉 Aperçu interactif : https://claude.ai/code/artifact/d5f09fe5-d4a7-4c49-ab40-51487d80077c**
*(données réelles figées ; la vraie app Flask se rafraîchit et se déploie)*

## 🧩 Ce que fait le projet

1. **Collecte** ([`src/fetch_deals.py`](src/fetch_deals.py)) — API publique **CheapShark**
   (bons plans multi-boutiques, sans clé). Choix **éthique** vs scraping fragile —
   voir [docs/ethique-scraping.md](docs/ethique-scraping.md).
2. **Stockage** — **SQLite** (`data/deals.db`), rejouable et planifiable.
3. **Web app** ([`app.py`](app.py) + Flask) — page avec **filtres réactifs**
   (recherche, prix max, réduction min, boutique), **KPIs**, graphique par boutique
   (Chart.js), et cartes d'offres avec **jeux gratuits mis en avant**.

Identité visuelle « Petrol & Ambre », cohérente avec le portfolio.

## 🚀 Lancer en local

```bash
pip install -r requirements.txt
python src/fetch_deals.py     # collecte -> data/deals.db (~160 offres)
python app.py                 # -> http://localhost:5000
```

## ☁️ Déployer (Render / Railway)

Le projet est prêt à déployer (`Procfile` + `gunicorn`) :

```
web: gunicorn app:app
```

- **Render** : nouveau *Web Service* depuis le repo → build `pip install -r requirements.txt`,
  start `gunicorn app:app`.
- Prévoir une tâche planifiée (cron) qui rejoue `python src/fetch_deals.py` pour
  rafraîchir les prix (1×/jour suffit).

## 🗂️ Structure

```
projet-03-scraper-prix-jeux-dashboard/
├── app.py                 ← web app Flask (page + /api/deals)
├── src/fetch_deals.py     ← collecte CheapShark -> SQLite
├── templates/index.html   ← dashboard (filtres réactifs + Chart.js)
├── requirements.txt · Procfile
└── docs/ethique-scraping.md
```

## 💡 Insight

Le tri par réduction fait remonter les meilleures affaires du moment (dont des jeux
**gratuits à 100 %**) ; le filtre « réduction min » + « prix max » aide à repérer
la fenêtre d'achat idéale par boutique.

---

*Projet 03 du [Portfolio Data](../). Collecter → structurer → visualiser une donnée
qui n'existait pas, dans une petite app déployable.*
