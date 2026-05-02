import csv
import json
import math
from collections import Counter, defaultdict
from itertools import combinations

DIMENSIONS = ["SR", "IF", "PR", "TH", "FI", "NF", "FR", "UC"]
CANONICAL_STATES = ["Flexible", "Integrated", "Defensive", "Rigid", "Fragmented", "Overloaded", "Stable/Neutral", "Mixed / Review Needed"]
STATE_NORMALIZATION = {
    "Flexible": "Flexible", "Integrated": "Integrated", "Defensive": "Defensive", "Rigid": "Rigid",
    "Fragmented": "Fragmented", "Overloaded": "Overloaded", "Stable/Neutral": "Stable/Neutral",
    "Stable / Neutral": "Stable/Neutral", "Mixed": "Mixed / Review Needed", "Mixed/Review": "Mixed / Review Needed",
    "Mixed / Review": "Mixed / Review Needed", "Mixed / Review Needed": "Mixed / Review Needed"
}


def normalize_state(value):
    return STATE_NORMALIZATION.get((value or "").strip(), (value or "").strip())


def load_coder_csv(path, coder_id):
    rows = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = ["sample_id", *DIMENSIONS, "primary_state"]
        missing = [c for c in required if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path} missing columns: {missing}")
        for row in reader:
            sid = row["sample_id"].strip()
            parsed = {
                "coder_id": coder_id,
                "sample_id": sid,
                "primary_state": normalize_state(row.get("primary_state", "")),
                "secondary_state": normalize_state(row.get("secondary_state", "")),
                "confidence": row.get("confidence", "").strip(),
                "notes": row.get("notes", "").strip(),
            }
            for dim in DIMENSIONS:
                try:
                    parsed[dim] = int(row[dim])
                except Exception:
                    parsed[dim] = None
            rows[sid] = parsed
    return rows


def load_all_coders(coder_files):
    return {coder_id: load_coder_csv(path, coder_id) for coder_id, path in coder_files.items()}


def get_common_sample_ids(coder_data):
    return sorted(set.intersection(*[set(samples) for samples in coder_data.values()]))


def percent_agreement_primary_state(coder_data, sample_ids):
    return sum(1 for sid in sample_ids if len({coder_data[c][sid]["primary_state"] for c in coder_data}) == 1) / len(sample_ids) if sample_ids else 0


def pairwise_percent_agreement_primary_state(coder_data, sample_ids):
    out = {}
    for a, b in combinations(coder_data.keys(), 2):
        out[(a, b)] = sum(1 for sid in sample_ids if coder_data[a][sid]["primary_state"] == coder_data[b][sid]["primary_state"]) / len(sample_ids) if sample_ids else 0
    return out


def dimension_agreement_within_one(coder_data, sample_ids):
    out = {}
    for dim in DIMENSIONS:
        total = agree = 0
        for sid in sample_ids:
            scores = [coder_data[c][sid][dim] for c in coder_data]
            if any(v is None for v in scores):
                continue
            total += 1
            agree += int(max(scores) - min(scores) <= 1)
        out[dim] = agree / total if total else 0
    return out


def dimension_exact_agreement(coder_data, sample_ids):
    out = {}
    for dim in DIMENSIONS:
        total = agree = 0
        for sid in sample_ids:
            scores = [coder_data[c][sid][dim] for c in coder_data]
            if any(v is None for v in scores):
                continue
            total += 1
            agree += int(len(set(scores)) == 1)
        out[dim] = agree / total if total else 0
    return out


def cohen_kappa(labels_a, labels_b, categories):
    if len(labels_a) != len(labels_b):
        raise ValueError("Label lists must have same length")
    n = len(labels_a)
    if not n:
        return 0.0
    po = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n
    ca, cb = Counter(labels_a), Counter(labels_b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in categories)
    return 1.0 if math.isclose(1 - pe, 0) else (po - pe) / (1 - pe)


def pairwise_cohen_kappas(coder_data, sample_ids):
    out = {}
    for a, b in combinations(coder_data.keys(), 2):
        out[(a, b)] = cohen_kappa([coder_data[a][sid]["primary_state"] for sid in sample_ids], [coder_data[b][sid]["primary_state"] for sid in sample_ids], CANONICAL_STATES)
    return out


def fleiss_kappa(coder_data, sample_ids, categories=CANONICAL_STATES):
    coder_ids = list(coder_data)
    n_raters = len(coder_ids)
    if n_raters < 3:
        return None
    n_items = len(sample_ids)
    matrix = []
    for sid in sample_ids:
        counts = Counter(coder_data[c][sid]["primary_state"] for c in coder_ids)
        matrix.append([counts[cat] for cat in categories])
    p_i = [(sum(v*v for v in row) - n_raters) / (n_raters * (n_raters - 1)) for row in matrix]
    p_bar = sum(p_i) / n_items if n_items else 0
    total_ratings = n_items * n_raters
    p_j = [sum(row[j] for row in matrix) / total_ratings for j in range(len(categories))]
    pe = sum(v*v for v in p_j)
    return 1.0 if math.isclose(1 - pe, 0) else (p_bar - pe) / (1 - pe)


def disagreement_report(coder_data, sample_ids):
    report = []
    for sid in sample_ids:
        labels = {c: coder_data[c][sid]["primary_state"] for c in coder_data}
        if len(set(labels.values())) > 1:
            report.append({
                "sample_id": sid,
                "primary_state_labels": labels,
                "notes": {c: coder_data[c][sid].get("notes", "") for c in coder_data}
            })
    return report


def coder_severity_report(coder_data, sample_ids):
    out = {}
    for c in coder_data:
        dim_means = {}
        for dim in DIMENSIONS:
            values = [coder_data[c][sid][dim] for sid in sample_ids if coder_data[c][sid][dim] is not None]
            dim_means[dim] = sum(values) / len(values) if values else 0
        out[c] = dim_means
    return out


def save_disagreement_csv(disagreements, path="outputs/disagreement_review.csv"):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id", "coder_labels", "coder_notes"])
        writer.writeheader()
        for item in disagreements:
            writer.writerow({
                "sample_id": item["sample_id"],
                "coder_labels": " | ".join(f"{c}: {v}" for c, v in item["primary_state_labels"].items()),
                "coder_notes": " | ".join(f"{c}: {v}" for c, v in item["notes"].items())
            })


def save_irr_summary(coder_data, path="outputs/irr_summary.json"):
    sample_ids = get_common_sample_ids(coder_data)
    disagreements = disagreement_report(coder_data, sample_ids)
    summary = {
        "coders": list(coder_data.keys()),
        "common_sample_count": len(sample_ids),
        "primary_state_full_agreement": percent_agreement_primary_state(coder_data, sample_ids),
        "pairwise_percent_agreement": {f"{a}_vs_{b}": v for (a,b), v in pairwise_percent_agreement_primary_state(coder_data, sample_ids).items()},
        "pairwise_cohen_kappa": {f"{a}_vs_{b}": v for (a,b), v in pairwise_cohen_kappas(coder_data, sample_ids).items()},
        "fleiss_kappa": fleiss_kappa(coder_data, sample_ids),
        "dimension_agreement_within_one": dimension_agreement_within_one(coder_data, sample_ids),
        "dimension_exact_agreement": dimension_exact_agreement(coder_data, sample_ids),
        "coder_severity_report": coder_severity_report(coder_data, sample_ids),
        "disagreement_count": len(disagreements),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    save_disagreement_csv(disagreements)
    return summary


if __name__ == "__main__":
    coder_files = {"coder_1": "coder_1.csv", "coder_2": "coder_2.csv", "coder_3": "coder_3.csv"}
    coder_data = load_all_coders(coder_files)
    summary = save_irr_summary(coder_data)
    print(json.dumps(summary, indent=2))
