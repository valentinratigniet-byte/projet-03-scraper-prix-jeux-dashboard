"""
Mini web app Flask — dashboard des bons plans jeux vidéo.
Sert la page (filtres réactifs + Chart.js) et une API JSON.
Lancer : python app.py  ->  http://localhost:5000
"""
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template

DB = Path(__file__).resolve().parent / "data" / "deals.db"
app = Flask(__name__)


def load_deals() -> list[dict]:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    deals = [dict(r) for r in con.execute(
        "SELECT * FROM deals ORDER BY savings_pct DESC")]
    con.close()
    return deals


@app.route("/")
def index():
    deals = load_deals()
    return render_template("index.html", deals=deals)


@app.route("/api/deals")
def api_deals():
    return jsonify(load_deals())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
