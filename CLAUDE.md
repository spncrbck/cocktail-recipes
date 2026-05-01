# Cocktail Recipe Database

This repo is an AI-first cocktail database. There is no application code — Claude Code is the interface. All recipes live in `data/recipes.json`.

## Schema

Each recipe in the `recipes` array follows this structure:

```json
{
  "name": "string — title-cased drink name",
  "ingredients": [
    {
      "name": "string — ingredient name, lowercase",
      "amount": "number",
      "unit": "string — see units below"
    }
  ],
  "garnish": "string — garnish description, or null if none",
  "served": "string — see serving styles below",
  "vessel": "string — glass or drinkware, lowercase",
  "tags": ["array of lowercase strings — see tagging conventions below"]
}
```

### Units
- `oz` — fluid ounces (standard for spirits, mixers, juices)
- `dash` — dashes (bitters)
- `barspoon` — barspoons (modifiers, syrups in small amounts)
- `tsp` — teaspoons
- `tbsp` — tablespoons
- `splash` — splashes (approximate, use sparingly)
- `whole` — whole items (e.g. an egg)

### Serving Styles
- `over ice` — built or poured over ice in the glass
- `up` — chilled and strained, served without ice
- `neat` — room temperature, no ice, no dilution
- `on the rocks` — spirit over a large ice cube
- `blended` — blended with ice

### Tagging Conventions
Tags are used for filtering and discovery. Apply all that fit:

**Base spirit:** `vodka`, `gin`, `rum`, `tequila`, `mezcal`, `whiskey`, `bourbon`, `rye`, `scotch`, `brandy`, `cognac`, `amaro`, `wine`, `beer`, `non-alcoholic`

**Style:** `classic`, `modern`, `tropical`, `tiki`, `sour`, `stirred`, `highball`, `shot`, `punch`, `low-abv`

**Flavor profile:** `refreshing`, `citrusy`, `bitter`, `sweet`, `smoky`, `spicy`, `herbal`, `creamy`, `fruity`, `rich`

**Season/occasion:** `summer`, `winter`, `holiday`, `brunch`, `digestif`, `aperitif`

## Common Tasks

### Add a recipe
Append a new entry to the `recipes` array in `data/recipes.json`, following the schema above. Use existing recipes as reference for formatting.

### Search by ingredient
Read `data/recipes.json` and filter recipes whose `ingredients` array contains a matching `name`.

### Find drinks for a given bar (available ingredients)
Given a list of ingredients, find all recipes where every ingredient `name` is in the provided list.

### Look up by name
Find the recipe object where `name` matches (case-insensitive).

### Randomize
Pick a random entry from the `recipes` array.

### Filter by tag
Find all recipes whose `tags` array includes the specified tag.

## Conventions
- Ingredient names are lowercase (`rye whiskey`, not `Rye Whiskey`)
- Recipe names are title-cased (`Whiskey Sour`, not `whiskey sour`)
- Keep `amount` as a number, not a string (`1.5` not `"1.5"`)
- Prefer `oz` over other units when possible for consistency
- When a recipe has no garnish, set `"garnish": null`
- The `recipes` array is not sorted — new recipes are appended
