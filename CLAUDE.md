# Cocktail Recipe App

A web app for browsing and querying cocktail recipes.

## What We're Building

A Flask + SQLite web app to search, browse, and eventually manage cocktail recipes.
The original project started as a Python CLI script with hardcoded recipes — this
web app replaces that with a proper persistent store and browser-based UI.

## Live App

**URL**: https://cocktail-recipes-pr3g.onrender.com
**Host**: Render (free tier web service)

Auto-deploys when commits are pushed to `master`. There is no manual deploy step.

## Read-Only App

The live app is intentionally read-only. Users cannot add, edit, or delete recipes
through the UI. All recipe changes are made by editing `recipes.json` and pushing
to master. Do not implement write functionality (forms, API POST/DELETE routes,
etc.) unless explicitly asked.

## Adding or Editing Recipes

`recipes.json` is the source of truth for all recipe data. The SQLite database
(`recipes.db`) is ephemeral — it is rebuilt from `recipes.json` on every deploy
and every time the app starts locally. Never edit the DB directly; changes will
be lost on the next restart.

To add or edit a recipe: update `recipes.json`, commit, and push to `master`.
Render will auto-deploy within a minute or two and the change will be live.

## Branch Strategy

Push directly to `master` for recipe additions and small changes. Use a feature
branch for anything that touches `app.py`, `templates/`, or `static/` — i.e.
changes that affect app behavior or appearance.

## Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLite (`recipes.db`, auto-created on first run, ephemeral on Render)
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

- **Bar inventory matcher** — check off ingredients you have, get a list of what you can make
- **"Missing one ingredient" suggestions** — show near-matches with one ingredient missing
- **Random drink picker** — shake button that surfaces a random recipe
- **Filter by spirit** — narrow by base spirit (vodka, gin, whiskey, rum, etc.)
- **Filter by vessel / serving style** — e.g., show only "neat" drinks or highball drinks
- **Ingredient substitution hints** — e.g., "can use lemon juice instead of lime juice"
- **Print / export** — printable recipe card layout
