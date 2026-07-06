import json
from pathlib import Path
from typing import Any

from src.detector import detect_prompt_injection_llm


def evaluate_detector(path: str = "data/eval_cases.json") -> dict[str, Any]:
    cases = json.loads(Path(path).read_text())

    tp = fp = tn = fn = 0
    rows = []

    for case in cases:
        result = detect_prompt_injection_llm(
            user_task=case["user_task"],
            external_content=case["external_content"]
        )

        expected = case["label"] == "injection"
        predicted = result.is_prompt_injection

        if predicted and expected:
            tp += 1
        elif predicted and not expected:
            fp += 1
        elif not predicted and not expected:
            tn += 1
        elif not predicted and expected:
            fn += 1

        rows.append(
            {
                "id": case["id"],
                "category": case["category"],
                "expected": case["label"],
                "predicted": "injection" if predicted else "clean",
                "confidence": result.confidence,
                "risk_level": result.risk_level,
                "attack_type": result.attack_type,
                "recommended_action": result.recommended_action,
                "reasoning_summary": result.reasoning_summary
            }
        )

    total = len(cases)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    accuracy = (tp + tn) / total if total else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

    return {
        "summary": {
            "total": total,
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn,
            "accuracy": round(accuracy, 3),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3)
        },
        "rows": rows
    }


def save_report(
    results: dict[str, Any],
    output_path: str = "reports/detector_results.json"
) -> None:
    Path(output_path).write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    results = evaluate_detector()
    save_report(results)
    print(json.dumps(results["summary"], indent=2))
    print("\nSaved full report to reports/detector_results.json")