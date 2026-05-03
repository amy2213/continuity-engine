import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from continuity_engine import analyze_text, CANONICAL_STATES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEAKNESS_PATH = os.path.join(ROOT, "test_known_weaknesses.json")
OUTPUT_PATH = os.path.join(ROOT, "outputs", "known_weaknesses_results.json")


def load_samples():
    with open(WEAKNESS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["samples"]


def test_known_weaknesses_run_without_error():
    samples = load_samples()
    results = []

    for sample in samples:
        result = analyze_text(sample["text"])
        assert result.loop_state in CANONICAL_STATES

        results.append({
            "sample_id": sample["sample_id"],
            "risk_type": sample["risk_type"],
            "expected_loop_state": sample["expected_loop_state"],
            "predicted_loop_state": result.loop_state,
            "confidence": result.confidence,
            "matches_expected": result.loop_state == sample["expected_loop_state"],
            "explanation": result.explanation,
            "scores": result.scores,
            "indexes": result.indexes,
            "notes": sample.get("notes", "")
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "dataset_name": "continuity_engine_known_weaknesses_v0_1",
            "status": "exploratory_not_validation",
            "accuracy_is_not_asserted": True,
            "results": results
        }, f, indent=2)

    assert os.path.exists(OUTPUT_PATH)


def test_known_weaknesses_file_has_minimum_samples():
    assert len(load_samples()) >= 12
