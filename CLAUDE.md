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
1. Check each ingredient against the canonical list below. If any ingredient is missing, add it to the appropriate category first.
2. Append a new entry to the `recipes` array in `data/recipes.json`, using canonical ingredient names exactly as they appear in the list.

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
- **Always use canonical ingredient names** (see list below). If a recipe calls for something not on the list, add it to the appropriate category before adding the recipe.

## Canonical Ingredients

When adding recipes, ingredient `name` values must match this list exactly. This ensures consistent search and filtering.

### Spirits

**Vodka**
- `vodka`

**Gin**
- `gin`
- `sloe gin`

**Rum**
- `white rum`
- `dark rum`
- `aged rum`
- `overproof rum`
- `spiced rum`
- `cachaça`

**Tequila & Mezcal**
- `blanco tequila`
- `reposado tequila`
- `añejo tequila`
- `mezcal`

**Whiskey**
- `bourbon`
- `rye whiskey`
- `scotch whisky`
- `Irish whiskey`
- `Japanese whisky`

**Brandy**
- `brandy`
- `cognac`
- `calvados`
- `pisco`
- `Armagnac`

**Other Spirits**
- `absinthe`
- `aquavit`
- `grappa`

### Liqueurs & Modifiers

**Orange**
- `triple sec`
- `Cointreau`
- `Grand Marnier`
- `curaçao`

**Bitter & Aperitivo**
- `Campari`
- `Aperol`
- `Cynar`
- `Fernet-Branca`
- `Amaro Nonino`
- `Amaro Montenegro`
- `klosterbitter liqueur`

**Vermouth & Aromatized Wine**
- `sweet vermouth`
- `dry vermouth`
- `bianco vermouth`
- `Lillet Blanc`
- `Cocchi Americano`
- `Cocchi di Torino`

**Herbal & Floral**
- `green Chartreuse`
- `yellow Chartreuse`
- `Bénédictine`
- `Drambuie`
- `St-Germain`
- `elderflower liqueur`

**Cherry & Nut**
- `maraschino liqueur`
- `Amaretto`
- `Frangelico`

**Coffee & Chocolate**
- `Kahlúa`
- `coffee liqueur`
- `dark crème de cacao`
- `white crème de cacao`

**Cream**
- `Irish cream liqueur`

**Other Liqueurs**
- `green crème de menthe`
- `white crème de menthe`
- `crème de violette`
- `crème de cassis`
- `Midori`
- `falernum`
- `Licor 43`

### Bitters

- `Angostura bitters`
- `Peychaud's bitters`
- `orange bitters`
- `mole bitters`
- `celery bitters`
- `grapefruit bitters`
- `cocoa bitters`

### Juices

- `lime juice`
- `lemon juice`
- `orange juice`
- `grapefruit juice`
- `pineapple juice`
- `cranberry juice`
- `apple juice`
- `pomegranate juice`
- `passion fruit juice`
- `tomato juice`

### Syrups & Sweeteners

- `simple syrup`
- `rich simple syrup`
- `demerara syrup`
- `honey syrup`
- `agave syrup`
- `grenadine`
- `orgeat`
- `passion fruit syrup`
- `raspberry syrup`
- `cinnamon syrup`
- `ginger syrup`

### Mixers & Sodas

- `ginger beer`
- `ginger ale`
- `tonic water`
- `club soda`
- `sparkling water`
- `cola`
- `lemon-lime soda`
- `Champagne`
- `prosecco`
- `dry sparkling wine`

### Dairy & Eggs

- `heavy cream`
- `whole milk`
- `coconut cream`
- `coconut milk`
- `egg white`
- `whole egg`

### Fresh & Produce

- `fresh mint`
- `fresh basil`
- `fresh thyme`
- `fresh ginger`
- `cucumber`
- `jalapeño`
- `muddled lime`
- `muddled lemon`

### Salty & Savory

- `olive brine`
- `hot sauce`
- `Worcestershire sauce`
- `horseradish`
