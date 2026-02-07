from pydantic import ValidationError
from .schema import Recipe

def _format_pydantic_errors(e: ValidationError) -> str:
    parts: list[str] = []
    for err in e.errors():
        loc = ".".join(str(x) for x in err.get("loc", []))
        msg = err.get("msg", "invalid")
        parts.append(f"{loc}: {msg}" if loc else msg)
    return "; ".join(parts)

def validate_recipe(recipe: dict) -> dict:
    try:
        parsed = Recipe.model_validate(recipe)
        return parsed.model_dump()
    except ValidationError as e:
        raise ValueError(f"Invalid recipe: {_format_pydantic_errors(e)}")

