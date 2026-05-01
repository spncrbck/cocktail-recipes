# Cocktail Recipe App

A web app for browsing and querying cocktail recipes.

## What We're Building

A Flask + SQLite web app to search, browse, and eventually manage cocktail recipes.
The original project started as a Python CLI script with hardcoded recipes — this
web app replaces that with a proper persistent store and browser-based UI.

## Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLite (`recipes.db`, auto-created on first run)
- **Frontend**: Vanilla HTML / CSS / JavaScript (no framework)

## Data Schema

```
recipes:     id, name, garnish, served, vessel
ingredients: id, recipe_id, name, amount, unit
```

Ingredients use a flat row-per-ingredient model (name, amount, unit) rather than
the original parallel-array approach, making queries straightforward.

## Running Locally

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## Current Features (MVP)

- Browse all recipes as cards
- Live search by recipe name or ingredient name
- Ingredient list, garnish, serving style, and vessel shown per card

## Planned Features

- **Add recipe form** — UI to submit new recipes without touching the DB directly
- **Bar inventory matcher** — check off ingredients you have, get a list of what you can make
- **"Missing one ingredient" suggestions** — show near-matches with one ingredient missing
- **Random drink picker** — shake button that surfaces a random recipe
- **Filter by spirit** — narrow by base spirit (vodka, gin, whiskey, rum, etc.)
- **Filter by vessel / serving style** — e.g., show only "neat" drinks or highball drinks
- **Edit and delete recipes** — full CRUD via the UI
- **Ingredient substitution hints** — e.g., "can use lemon juice instead of lime juice"
- **Print / export** — printable recipe card layout
