#!/usr/bin/env python3
"""
Parse cocktail recipes from images, PDFs, or text into JSON.

Usage:
    python parse_recipe.py photo.png
    python parse_recipe.py menu.jpg menu2.png
    python parse_recipe.py recipe.pdf -o my_recipes.json
    echo "2oz gin, 1oz lime, 0.75oz simple syrup" | python parse_recipe.py
    python parse_recipe.py photo.png --add          # also append to recipes.json
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import anthropic

SYSTEM_PROMPT = """You are a cocktail recipe parser. Parse all cocktail content from the provided input into clean JSON.

Output a JSON array — one object per recipe — following this schema exactly:

{
  "name": "string",
  "ingredients": [{ "amount": number, "unit": "string", "item": "string" }],
  "served": "string",
  "glass": "string",
  "garnish": ["string"],
  "attribution": "string",
  "special_tags": ["string"],
  "notes": "string"
}

FIELD RULES:

name — Title-case. Infer from context if unclear.

amount — Always a decimal number: 1.5, 0.75, 0.5, 0.25. Barspoon/splash/dash/rinse are units, not amounts — set amount to 1 for those. If amounts are missing (e.g. a restaurant menu photo), make reasonable professional guesses and add "inferred" to special_tags.

unit — Use: oz, dash, splash, barspoon, rinse, drop, or "" (empty string for garnish/rimming items). Convert everything possible to oz (e.g. 1 jigger = 1.5 oz, 1 pony = 1 oz, 1 cup = 8 oz).

item — Simple and clean. "lemon juice" not "fresh-squeezed lemon juice". "simple syrup" not "1:1 cane sugar syrup". "egg white" not "one fresh egg white".

brand specificity — Drop brand if it's just a common style: Bombay → "gin", Bacardi → "white rum", Smirnoff → "vodka". Keep brand if it defines the ingredient type: "Lillet Blanc", "Aperol", "Campari", "Fernet-Branca", "Velvet Falernum", "Luxardo maraschino liqueur", "Cointreau", "Chartreuse".

served — One or more of: neat / on the rocks / up / built / shaken / stirred / blended / shot. Chain if needed: "shaken, up". Infer from drink style if not stated: sours → "shaken, up", highballs → "built, on the rocks", spirit-forward → "stirred, up".

glass — Lowercase: highball, rocks, martini, coupe, nick & nora, collins, flute, mule mug, snifter, hurricane, wine, pint, shot, tiki, unknown.

garnish — Array of strings. [] if none. Garnish = placed on top/rim, not mixed in. Citrus expressed over drink is still a garnish.

attribution — Exact source string, or "". For Instagram use: "IG @username".

special_tags — Array of short strings. Reserved: "inferred" (any amounts were guessed). Add others as appropriate: "spicy", "low-abv", "frozen", "brunch", "tropical", "classic", "tiki", "aperitivo".

notes — Only if critical: rimming instructions, specific layering order, required ice type, technique details. "" otherwise.

PARSING RULES:

- Visible text beats visual inference. Infer intelligently when content is cut off or incomplete.
- Merge duplicate ingredients — sum amounts.
- Multiple recipes in one input → all go into the JSON array.
- Unknown or missing fields → "" or [], never omit the key.
- Output ONLY the JSON array. No markdown fences, no preamble, no explanation."""

IMAGE_MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def build_content(inputs: list[str], stdin_text: str | None) -> list[dict]:
    content = []

    for inp in inputs:
        path = Path(inp)
        if not path.exists():
            print(f"Warning: {inp} not found, skipping", file=sys.stderr)
            continue

        ext = path.suffix.lower()

        if ext in IMAGE_MEDIA_TYPES:
            data = base64.standard_b64encode(path.read_bytes()).decode()
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": IMAGE_MEDIA_TYPES[ext],
                    "data": data,
                },
            })
        elif ext == ".pdf":
            data = base64.standard_b64encode(path.read_bytes()).decode()
            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": data,
                },
            })
        else:
            try:
                text = path.read_text(encoding="utf-8")
                content.append({"type": "text", "text": f"[{path.name}]\n{text}"})
            except Exception as e:
                print(f"Warning: could not read {inp}: {e}", file=sys.stderr)

    if stdin_text:
        content.append({"type": "text", "text": stdin_text})

    return content


def call_claude(content: list[dict], client: anthropic.Anthropic) -> str:
    content_with_instruction = content + [
        {
            "type": "text",
            "text": "Parse all cocktail recipes from the provided content. Return only the JSON array.",
        }
    ]

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content_with_instruction}],
    )

    return next(b.text for b in response.content if b.type == "text")


def extract_json(raw: str) -> list[dict]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        end = next((i for i in range(len(lines) - 1, 0, -1) if lines[i].strip() == "```"), len(lines))
        cleaned = "\n".join(lines[1:end])
    result = json.loads(cleaned)
    return result if isinstance(result, list) else [result]


def recipes_to_app_format(recipes: list[dict]) -> list[dict]:
    """Convert parsed schema to recipes.json schema for --add."""
    converted = []
    for r in recipes:
        garnish_list = r.get("garnish", [])
        garnish_str = ", ".join(garnish_list) if garnish_list else ""
        ingredients = [
            {"name": ing["item"], "amount": ing["amount"], "unit": ing["unit"]}
            for ing in r.get("ingredients", [])
        ]
        converted.append({
            "name": r.get("name", "Unknown"),
            "garnish": garnish_str,
            "served": r.get("served", ""),
            "vessel": r.get("glass", "unknown"),
            "ingredients": ingredients,
        })
    return converted


def print_synopsis(recipes: list[dict], out_path: Path) -> None:
    print(f"\nSaved: {out_path}")
    print(f"Recipes: {len(recipes)}")
    for r in recipes:
        name = r.get("name", "Unknown")
        tags = r.get("special_tags", [])
        notes = r.get("notes", "")
        inferred = "inferred" in tags
        other_tags = [t for t in tags if t != "inferred"]

        flags = []
        if inferred:
            flags.append("amounts inferred")
        if other_tags:
            flags.append(", ".join(other_tags))
        if notes:
            flags.append(f"note: {notes}")

        flag_str = f"  [{'; '.join(flags)}]" if flags else ""
        print(f"  - {name}{flag_str}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse cocktail recipes from images, PDFs, or text into JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.strip(),
    )
    parser.add_argument("inputs", nargs="*", help="Image, PDF, or text files to parse")
    parser.add_argument("-o", "--output", help="Output JSON file (default: parsed_recipes.json)")
    parser.add_argument(
        "--add",
        action="store_true",
        help="Also append parsed recipes to recipes.json in app format",
    )
    args = parser.parse_args()

    stdin_text = None
    if not sys.stdin.isatty():
        stdin_text = sys.stdin.read().strip() or None

    if not args.inputs and not stdin_text:
        parser.print_help()
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("Parsing...", file=sys.stderr)
    content = build_content(args.inputs, stdin_text)

    if not content:
        print("Error: no readable content found", file=sys.stderr)
        sys.exit(1)

    raw = call_claude(content, client)

    try:
        recipes = extract_json(raw)
    except json.JSONDecodeError as e:
        print(f"Error: could not parse response as JSON: {e}", file=sys.stderr)
        print(f"Raw response:\n{raw}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out_path = Path(args.output)
    elif args.inputs and len(args.inputs) == 1:
        stem = Path(args.inputs[0]).stem
        out_path = Path(f"{stem}_parsed.json")
    else:
        out_path = Path("parsed_recipes.json")

    out_path.write_text(json.dumps(recipes, indent=2))
    print_synopsis(recipes, out_path)

    if args.add:
        recipes_json = Path(__file__).parent / "recipes.json"
        existing = json.loads(recipes_json.read_text())
        converted = recipes_to_app_format(recipes)
        existing.extend(converted)
        recipes_json.write_text(json.dumps(existing, indent=2))
        names = [r["name"] for r in converted]
        print(f"\nAdded to recipes.json: {', '.join(names)}")
        print("Restart the app (or it will reload on next deploy) to see the new recipes.")


if __name__ == "__main__":
    main()
