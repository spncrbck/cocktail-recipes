# Cocktail Recipe Browser

A web app for browsing and searching cocktail recipes.

## Live App

**URL**: https://muddled.onrender.com

The app is hosted on Render and auto-deploys when changes are pushed to `master`.

## Features

- **Browse recipes** — View all cocktail recipes as cards with ingredients, garnish, serving style, and vessel
- **Live search** — Search by recipe name or ingredient name in real-time
- **Read-only** — The app is intentionally read-only; all recipe data is managed by editing `recipes.json`

## Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLite (auto-created from `recipes.json` on startup)
- **Frontend**: Vanilla HTML / CSS / JavaScript

## Data Schema

```
recipes:     id, name, garnish, served, vessel
ingredients: id, recipe_id, name, amount, unit
```

## Running Locally

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## Adding or Editing Recipes

All recipe data is stored in `recipes.json`. To add or edit a recipe:

1. Edit `recipes.json`
2. Commit and push to `master`
3. The app will automatically rebuild from the updated file

The SQLite database is ephemeral and is regenerated from `recipes.json` on every startup, so never edit it directly.

## Planned Features

- Bar inventory matcher — check off ingredients you have, see what you can make
- Missing ingredient suggestions — show drinks that are one ingredient away
- Random drink picker — surprise recipe button
- Filter by spirit, vessel, or serving style
- Ingredient substitution hints
- Print / export functionality
