import json
import re
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """
    Extract the first JSON object from model output.

    This lets the app survive if the model accidentally wraps JSON in prose
    or Markdown code fences.
    """
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text.strip()).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output.")

    parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON is not an object.")

    return parsed