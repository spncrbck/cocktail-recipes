import os
import sqlite3
from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "recipes.db")

SEED_RECIPES = [
    {
        "name": "Moscow Mule",
        "garnish": "lime wedge",
        "served": "over ice",
        "vessel": "copper mug",
        "ingredients": [("vodka", 2, "oz"), ("ginger beer", 4, "oz"), ("lime juice", 0.5, "oz")],
    },
    {
        "name": "Gin and Tonic",
        "garnish": "lime wedge",
        "served": "over ice",
        "vessel": "highball glass",
        "ingredients": [("gin", 2, "oz"), ("tonic water", 4, "oz"), ("lime juice", 0.5, "oz")],
    },
    {
        "name": "Manhattan",
        "garnish": "cherry",
        "served": "neat",
        "vessel": "coupe",
        "ingredients": [
            ("rye whiskey", 2, "oz"),
            ("sweet vermouth", 1, "oz"),
            ("angostura bitters", 2, "dash"),
        ],
    },
]


def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(_):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS recipes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                garnish TEXT,
                served  TEXT,
                vessel  TEXT
            );
            CREATE TABLE IF NOT EXISTS ingredients (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER REFERENCES recipes(id),
                name      TEXT NOT NULL,
                amount    REAL,
                unit      TEXT
            );
        """)
        if db.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0:
            for drink in SEED_RECIPES:
                cur = db.execute(
                    "INSERT INTO recipes (name, garnish, served, vessel) VALUES (?, ?, ?, ?)",
                    (drink["name"], drink["garnish"], drink["served"], drink["vessel"]),
                )
                for name, amount, unit in drink["ingredients"]:
                    db.execute(
                        "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
                        (cur.lastrowid, name, amount, unit),
                    )
            db.commit()


def recipe_row_to_dict(row, db):
    ingredients = db.execute(
        "SELECT name, amount, unit FROM ingredients WHERE recipe_id = ? ORDER BY id",
        (row["id"],),
    ).fetchall()
    return {
        "id": row["id"],
        "name": row["name"],
        "garnish": row["garnish"],
        "served": row["served"],
        "vessel": row["vessel"],
        "ingredients": [
            {"name": i["name"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients
        ],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recipes")
def list_recipes():
    db = get_db()
    q = request.args.get("q", "").strip()
    if q:
        rows = db.execute(
            """
            SELECT DISTINCT r.id, r.name, r.garnish, r.served, r.vessel
            FROM recipes r
            LEFT JOIN ingredients i ON i.recipe_id = r.id
            WHERE r.name LIKE ? OR i.name LIKE ?
            ORDER BY r.name
            """,
            (f"%{q}%", f"%{q}%"),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM recipes ORDER BY name").fetchall()
    return jsonify([recipe_row_to_dict(row, db) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
