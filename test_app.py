"""Self-check : app.py sert des donnees valides depuis deals.db.

A lancer apres `python src/fetch_deals.py` (deals.db doit exister).
Usage : python test_app.py
"""
from app import app, load_deals


def main() -> None:
    deals = load_deals()
    assert len(deals) > 0, "aucun deal en base"
    assert all("title" in d and "sale_price" in d and "savings_pct" in d for d in deals), \
        "champs manquants sur au moins un deal"

    savings = [d["savings_pct"] for d in deals]
    assert savings == sorted(savings, reverse=True), "deals non tries par savings_pct decroissant"

    client = app.test_client()

    r = client.get("/")
    assert r.status_code == 200, f"/ a renvoye {r.status_code}"

    r2 = client.get("/api/deals")
    assert r2.status_code == 200, f"/api/deals a renvoye {r2.status_code}"
    data = r2.get_json()
    assert isinstance(data, list) and len(data) == len(deals), "/api/deals incoherent avec load_deals()"

    print(f"OK — {len(deals)} deals, / et /api/deals repondent correctement")


if __name__ == "__main__":
    main()
