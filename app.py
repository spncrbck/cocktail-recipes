import json
import os
import sqlite3
from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "recipes.db")
RECIPES_PATH = os.path.join(os.path.dirname(__file__), "recipes.json")


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
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS recipes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            served       TEXT,
            glass        TEXT,
            garnish      TEXT,
            attribution  TEXT,
            special_tags TEXT,
            notes        TEXT
        );
        CREATE TABLE IF NOT EXISTS ingredients (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER REFERENCES recipes(id),
            item      TEXT NOT NULL,
            amount    REAL,
            unit      TEXT
        );
    """)
    if db.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0:
        with open(RECIPES_PATH) as f:
            seed = json.load(f)
        for drink in seed:
            cur = db.execute(
                """INSERT INTO recipes (name, served, glass, garnish, attribution, special_tags, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    drink["name"],
                    drink.get("served", ""),
                    drink.get("glass", ""),
                    json.dumps(drink.get("garnish", [])),
                    drink.get("attribution", ""),
                    json.dumps(drink.get("special_tags", [])),
                    drink.get("notes", ""),
                ),
            )
            for ing in drink["ingredients"]:
                db.execute(
                    "INSERT INTO ingredients (recipe_id, item, amount, unit) VALUES (?, ?, ?, ?)",
                    (cur.lastrowid, ing["item"], ing["amount"], ing["unit"]),
                )
        db.commit()


def recipe_row_to_dict(row, db):
    ingredients = db.execute(
        "SELECT item, amount, unit FROM ingredients WHERE recipe_id = ? ORDER BY id",
        (row["id"],),
    ).fetchall()
    return {
        "id": row["id"],
        "name": row["name"],
        "served": row["served"],
        "glass": row["glass"],
        "garnish": json.loads(row["garnish"] or "[]"),
        "attribution": row["attribution"],
        "special_tags": json.loads(row["special_tags"] or "[]"),
        "notes": row["notes"],
        "ingredients": [
            {"item": i["item"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients
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
            SELECT DISTINCT r.id, r.name, r.served, r.glass, r.garnish,
                            r.attribution, r.special_tags, r.notes
            FROM recipes r
            LEFT JOIN ingredients i ON i.recipe_id = r.id
            WHERE r.name LIKE ? OR i.item LIKE ?
            ORDER BY r.name
            """,
            (f"%{q}%", f"%{q}%"),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT id, name, served, glass, garnish, attribution, special_tags, notes FROM recipes ORDER BY name"
        ).fetchall()
    return jsonify([recipe_row_to_dict(row, db) for row in rows])


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
