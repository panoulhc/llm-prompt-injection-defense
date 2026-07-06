from src.json_utils import extract_json_object


def test_extract_plain_json():
    text = '{"passed": true, "confidence": 0.9}'
    parsed = extract_json_object(text)

    assert parsed["passed"] is True
    assert parsed["confidence"] == 0.9


def test_extract_markdown_json():
    text = """```json
{"passed": false, "confidence": 1.0}
```"""
    parsed = extract_json_object(text)

    assert parsed["passed"] is False
    assert parsed["confidence"] == 1.0


def test_extract_json_from_prose():
    text = 'Here is the result: {"passed": true, "confidence": 0.7}'
    parsed = extract_json_object(text)

    assert parsed["passed"] is True
    assert parsed["confidence"] == 0.7