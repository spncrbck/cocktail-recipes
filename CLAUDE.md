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

## Recipe JSON Schema

`recipes.json` is the source of truth. Each recipe object must have all of these keys:

```json
{
  "name": "Title Case string",
  "ingredients": [{ "amount": 1.5, "unit": "oz", "item": "ingredient name" }],
  "served": "string",
  "glass": "string",
  "garnish": ["string"],
  "attribution": "string",
  "special_tags": ["string"],
  "notes": "string"
}
```

### Field rules

- **name** — Title-case. Infer if unclear.
- **ingredients.amount** — Always a decimal: `1.5`, `0.75`, `0.5`. For barspoon / splash / dash / rinse use `1`.
- **ingredients.unit** — `oz`, `dash`, `splash`, `barspoon`, `rinse`, `drop`, or `""`. Convert volume to oz where possible.
- **ingredients.item** — Clean and generic: `"lemon juice"` not `"fresh-squeezed lemon juice"`. Drop brand when it's just a common style (Bombay → `"gin"`, Bacardi → `"white rum"`). Keep brand when it defines the ingredient: `"Lillet Blanc"`, `"Aperol"`, `"Campari"`, `"Fernet-Branca"`, `"Velvet Falernum"`.
- **served** — `neat` / `on the rocks` / `up` / `built` / `shaken` / `stirred` / `blended` / `shot`. Chain if needed: `"shaken, up"`. Infer from drink style if unstated (sours → `"shaken, up"`, highballs → `"built, on the rocks"`, spirit-forward → `"stirred, up"`).
- **glass** — lowercase: `highball`, `rocks`, `martini`, `coupe`, `nick & nora`, `collins`, `flute`, `mule mug`, `snifter`, `hurricane`, `wine`, `pint`, `shot`, `tiki`, `unknown`.
- **garnish** — array, `[]` if none. Garnish = placed on top/rim, not mixed in.
- **attribution** — exact source string or `""`. Instagram format: `"IG @username"`.
- **special_tags** — array of short tag strings. Reserved: `"inferred"` (any amounts were guessed). Others as appropriate: `"spicy"`, `"low-abv"`, `"frozen"`, `"brunch"`, etc.
- **notes** — only if critical (rimming instructions, layering order, specific ice type); else `""`.

Unknown or missing fields → `""` or `[]`. Never omit a key.

### Parsing conventions (when adding recipes from photos or menus)

- Visible text beats visual inference — infer intelligently when content is cut off or incomplete.
- Merge duplicate ingredients by summing amounts.
- If amounts are missing (e.g. restaurant menu photo), make reasonable professional guesses and add `"inferred"` to `special_tags`.
- Multiple recipes in one input → all go into one JSON array.

## Database Schema

The SQLite DB is rebuilt from `recipes.json` on every start. Never edit it directly.

```
recipes:     id, name, served, glass, garnish (JSON array), attribution, special_tags (JSON array), notes
ingredients: id, recipe_id, item, amount, unit
```

## Running Locally

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## Current Features (MVP)

- Browse all recipes as cards
- Live search by recipe name or ingredient name
- Ingredient list, garnish, serving style, and glass shown per card

## Planned Features

- **Bar inventory matcher** — check off ingredients you have, get a list of what you can make
- **"Missing one ingredient" suggestions** — show near-matches with one ingredient missing
- **Random drink picker** — shake button that surfaces a random recipe
- **Filter by spirit** — narrow by base spirit (vodka, gin, whiskey, rum, etc.)
- **Filter by glass / serving style** — e.g., show only "stirred, up" drinks or highball drinks
- **Ingredient substitution hints** — e.g., "can use lemon juice instead of lime juice"
- **Print / export** — printable recipe card layout
