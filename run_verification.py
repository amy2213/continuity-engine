import csv
import json
from collections import Counter, defaultdict
from continuity_engine import analyze_text, CANONICAL_STATES


def load_samples(path="sample_texts.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["samples"]


def assign_failure_type(expected, predicted):
    if expected == predicted:
        return ""
    return {
        "Flexible": "False Flexible",
        "Integrated": "False Integrated",
        "Defensive": "False Defensive",
        "Rigid": "False Rigid",
        "Fragmented": "False Fragmented",
        "Overloaded": "False Overloaded",
        "Stable/Neutral": "False Stable",
        "Mixed / Review Needed": "False Mixed",
    }.get(predicted, "Unclassified Error")


def run_dataset_verification(samples):
    results = []
    for sample in samples:
        result = analyze_text(sample["text"])
        expected = sample["expected_loop_state"]
        predicted = result.loop_state
        match = expected == predicted
        results.append({
            "sample_id": sample["sample_id"],
            "expected": expected,
            "predicted": predicted,
            "match": match,
            "confidence": result.confidence,
            "explanation": result.explanation,
            "failure_type": assign_failure_type(expected, predicted),
            "rigidity_index": result.indexes.get("rigidity_index"),
            "integration_index": result.indexes.get("integration_index"),
            "discernment_index": result.indexes.get("discernment_index"),
            "threat_prediction_index": result.indexes.get("threat_prediction_index"),
            "scores": json.dumps(result.scores),
        })
    return results


def summarize(results):
    correct = sum(1 for r in results if r["match"])
    total = len(results)
    return correct, total, correct / total if total else 0


def accuracy_by_state(results):
    totals = defaultdict(int); corrects = defaultdict(int)
    for r in results:
        totals[r["expected"]] += 1
        if r["match"]:
            corrects[r["expected"]] += 1
    return [{"state": s, "correct": corrects[s], "total": totals[s], "accuracy": corrects[s] / totals[s] if totals[s] else 0} for s in CANONICAL_STATES]


def confusion_matrix(results):
    matrix = {e: {p: 0 for p in CANONICAL_STATES} for e in CANONICAL_STATES}
    for r in results:
        if r["expected"] in matrix and r["predicted"] in matrix[r["expected"]]:
            matrix[r["expected"]][r["predicted"]] += 1
    return matrix


def save_results(results, path="outputs/verification_results.csv"):
    fieldnames = ["sample_id", "expected", "predicted", "match", "confidence", "failure_type", "explanation", "rigidity_index", "integration_index", "discernment_index", "threat_prediction_index", "scores"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(results)


def save_summary(results, path="outputs/verification_summary.json"):
    correct, total, accuracy = summarize(results)
    failures = defaultdict(list)
    for r in results:
        if not r["match"]:
            failures[r["failure_type"]].append(r["sample_id"])
    summary = {
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "accuracy_by_state": accuracy_by_state(results),
        "confusion_matrix": confusion_matrix(results),
        "failure_taxonomy": dict(failures),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Continuity Engine verification.")
    parser.add_argument("--dataset", default="sample_texts.json", help="Path to labeled JSON dataset.")
    parser.add_argument("--no-labels", action="store_true", help="Exploration mode: classify without expected labels.")
    args = parser.parse_args()

    samples = load_samples(args.dataset)

    if args.no_labels:
        print(f"Exploration mode: classifying {len(samples)} samples from {args.dataset}\n")
        for sample in samples:
            result = analyze_text(sample["text"])
            print(f"{sample['sample_id']}: {result.loop_state} ({result.confidence})")
            print(f"  {result.explanation}")
            print(f"  scores: {json.dumps(result.scores)}")
            print()
    else:
        results = run_dataset_verification(samples)
        dataset_tag = args.dataset.replace(".json", "").replace("/", "_")
        results_path = f"outputs/verification_results_{dataset_tag}.csv"
        summary_path = f"outputs/verification_summary_{dataset_tag}.json"
        save_results(results, path=results_path)
        summary = save_summary(results, path=summary_path)
        print(f"Dataset: {args.dataset}")
        print(f"Overall Accuracy: {summary['correct']} / {summary['total']} = {summary['accuracy']:.2%}")
        print("Accuracy by State:")
        for row in summary["accuracy_by_state"]:
            if row["total"] > 0:
                print(f"- {row['state']}: {row['correct']} / {row['total']} = {row['accuracy']:.2%}")
        if summary["failure_taxonomy"]:
            print("Failures:")
            for ftype, ids in summary["failure_taxonomy"].items():
                print(f"- {ftype}: {len(ids)} | {', '.join(ids)}")
        else:
            print("No failures.")
