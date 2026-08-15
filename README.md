# Projet 03 — Suivi de prix de jeux vidéo + mini web app

> Suivre les prix et repérer les meilleures affaires demande de **collecter,
> structurer et visualiser** une donnée qui n'existe pas sous forme de dataset
> propre. Ce projet collecte des bons plans jeux, les stocke, et les expose dans une
> **web app** avec filtres réactifs et mise en avant des meilleures offres.

**👉 App en ligne : https://projet-03-scraper-prix-jeux-dashboard.onrender.com**
*(plan gratuit Render : le service s'endort après 15 min d'inactivité — la
première visite prend ~30-50 s pour se réveiller)*

Aperçu figé (secours) : https://claude.ai/code/artifact/d5f09fe5-d4a7-4c49-ab40-51487d80077c

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

## ☁️ Déployer (Render)

Le repo contient un **Blueprint** [`render.yaml`](render.yaml) : build =
`pip install -r requirements.txt && python src/fetch_deals.py` (régénère
`data/deals.db`, gitignoré, à chaque déploiement), start = `gunicorn app:app`.

1. Sur [render.com](https://render.com) → **New → Blueprint** → connecter ce repo GitHub.
   Render lit `render.yaml` et configure tout automatiquement (plan gratuit).
2. Une fois le service créé → **Settings → Deploy Hook**, copier l'URL.
3. Dans le repo GitHub → **Settings → Secrets and variables → Actions** → nouveau secret
   `RENDER_DEPLOY_HOOK_URL` avec cette URL.
4. Le workflow [`.github/workflows/refresh-deploy.yml`](.github/workflows/refresh-deploy.yml)
   déclenche un redeploy chaque jour à 6h UTC (+ bouton manuel dans l'onglet *Actions*) —
   chaque redeploy rejoue la collecte CheapShark, donc les prix se rafraîchissent.

*(Railway fonctionne aussi via le `Procfile` fourni, sans le Blueprint Render.)*

## 🗂️ Structure

```
projet-03-scraper-prix-jeux-dashboard/
├── app.py                 ← web app Flask (page + /api/deals)
├── src/fetch_deals.py     ← collecte CheapShark -> SQLite
├── templates/index.html   ← dashboard (filtres réactifs + Chart.js)
├── requirements.txt · Procfile · render.yaml
├── .github/workflows/refresh-deploy.yml  ← redeploy quotidien (rafraîchit les prix)
└── docs/ethique-scraping.md
```

## 💡 Insight

Le tri par réduction fait remonter les meilleures affaires du moment (dont des jeux
**gratuits à 100 %**) ; le filtre « réduction min » + « prix max » aide à repérer
la fenêtre d'achat idéale par boutique.

---

*Projet 03 du [Portfolio Data](../). Collecter → structurer → visualiser une donnée
qui n'existait pas, dans une petite app déployable.*
