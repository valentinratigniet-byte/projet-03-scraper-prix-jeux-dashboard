"""
Collecte des bons plans jeux vidéo depuis l'API CheapShark (gratuite, sans clé)
et stockage dans SQLite. Alternative éthique au scraping : source structurée,
respectueuse des conditions d'usage (User-Agent, pas de surcharge).

Usage : python src/fetch_deals.py
"""
import json
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://www.cheapshark.com/api/1.0"
DB = Path(__file__).resolve().parent.parent / "data" / "deals.db"
PAGES = 3          # 3 x 60 = ~180 deals
PAGE_SIZE = 60
HEADERS = {"User-Agent": "portfolio-data-game-deals/1.0"}


def _get(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch() -> list[dict]:
    stores = {s["storeID"]: s["storeName"] for s in _get(f"{API}/stores")}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    deals = []
    for page in range(PAGES):
        batch = _get(f"{API}/deals?pageSize={PAGE_SIZE}&pageNumber={page}&sortBy=Savings&onSale=1")
        for d in batch:
            deals.append({
                "deal_id": d["dealID"],
                "title": d["title"],
                "store": stores.get(d["storeID"], f"Store {d['storeID']}"),
                "sale_price": float(d["salePrice"]),
                "normal_price": float(d["normalPrice"]),
                "savings_pct": round(float(d["savings"]), 1),
                "metacritic": int(d["metacriticScore"] or 0),
                "steam_rating": int(d["steamRatingPercent"] or 0),
                "url": f"https://www.cheapshark.com/redirect?dealID={d['dealID']}",
                "fetched_at": now,
            })
    # déduplication par titre (garder la meilleure réduction)
    best = {}
    for d in deals:
        k = d["title"].lower()
        if k not in best or d["savings_pct"] > best[k]["savings_pct"]:
            best[k] = d
    return list(best.values())


def store(deals: list[dict]) -> None:
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            deal_id TEXT PRIMARY KEY, title TEXT, store TEXT,
            sale_price REAL, normal_price REAL, savings_pct REAL,
            metacritic INTEGER, steam_rating INTEGER, url TEXT, fetched_at TEXT
        )""")
    con.execute("DELETE FROM deals")
    con.executemany(
        "INSERT OR REPLACE INTO deals VALUES "
        "(:deal_id,:title,:store,:sale_price,:normal_price,:savings_pct,"
        ":metacritic,:steam_rating,:url,:fetched_at)", deals)
    con.commit()
    con.close()


def main() -> None:
    deals = fetch()
    store(deals)
    print(f"{len(deals)} bons plans stockés dans {DB.name}")
    free = sum(1 for d in deals if d["sale_price"] == 0)
    print(f"  dont {free} gratuits (100 %) · {len({d['store'] for d in deals})} boutiques")


if __name__ == "__main__":
    main()
