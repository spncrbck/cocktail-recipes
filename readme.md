# Cocktail Recipe Database

An AI-first cocktail database and assistant bartender, powered by Claude Code.

There is no application code — Claude Code is the interface. Recipes are stored in `data/recipes.json` and Claude Code can add, search, filter, and suggest recipes in natural language.

### What you can ask

- "Add a recipe for a Negroni"
- "What can I make with gin, lemon juice, and simple syrup?"
- "Show me all stirred whiskey cocktails"
- "Give me a random cocktail"
- "Look up the Manhattan recipe"

See `CLAUDE.md` for the full schema and conventions.

### Features

- Stores drink name, ingredients with amounts and units, garnish, serving style, and vessel
- Search by ingredient, name, tag, or serving style
- Filter by available bar ingredients
- Randomize for a surprise recipe
