import json
import os
import sqlite3
from flask import Flask, g, jsonify, render_template, request, abort

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
            garnish      TEXT,
            served       TEXT,
            vessel       TEXT,
            flavor_tags  TEXT,
            flavor_desc  TEXT
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
        with open(RECIPES_PATH) as f:
            seed = json.load(f)
        for drink in seed:
            tags = json.dumps(drink.get("flavor_tags", []))
            cur = db.execute(
                "INSERT INTO recipes (name, garnish, served, vessel, flavor_tags, flavor_desc) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    drink["name"],
                    drink.get("garnish", ""),
                    drink.get("served", ""),
                    drink.get("vessel", ""),
                    tags,
                    drink.get("flavor_description", ""),
                ),
            )
            for ing in drink.get("ingredients", []):
                db.execute(
                    "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
                    (cur.lastrowid, ing["name"], ing["amount"], ing["unit"]),
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
        "flavor_tags": json.loads(row["flavor_tags"] or "[]"),
        "flavor_description": row["flavor_desc"] or "",
        "ingredients": [
            {"name": i["name"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients
        ],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    db = get_db()
    row = db.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    if row is None:
        abort(404)
    recipe = recipe_row_to_dict(row, db)
    return render_template("recipe.html", recipe=recipe)


@app.route("/api/recipes")
def list_recipes():
    db = get_db()
    q = request.args.get("q", "").strip()
    if q:
        rows = db.execute(
            """
            SELECT DISTINCT r.id, r.name, r.garnish, r.served, r.vessel, r.flavor_tags, r.flavor_desc
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


@app.route("/api/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
    db = get_db()
    row = db.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    if row is None:
        abort(404)
    return jsonify(recipe_row_to_dict(row, db))


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
