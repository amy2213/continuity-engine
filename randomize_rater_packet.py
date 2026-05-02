import csv
import json
import random
from collections import defaultdict

RANDOM_SEED = 2213
MAX_SAME_STATE_IN_ROW = 2


def load_samples(path="sample_texts.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["samples"]


def group_by_state(samples):
    groups = defaultdict(list)
    for sample in samples:
        groups[sample["expected_loop_state"]].append(sample)
    return groups


def too_many_same_state(candidate, output, max_same=2):
    if len(output) < max_same:
        return False
    state = candidate["expected_loop_state"]
    return all(item["expected_loop_state"] == state for item in output[-max_same:])


def stratified_shuffle(samples, seed=RANDOM_SEED, max_same_state_in_row=MAX_SAME_STATE_IN_ROW):
    random.seed(seed)
    groups = group_by_state(samples)
    for state in groups:
        random.shuffle(groups[state])
    output = []
    remaining = sum(len(items) for items in groups.values())
    while remaining > 0:
        available_states = [state for state, items in groups.items() if items]
        random.shuffle(available_states)
        placed = False
        for state in available_states:
            candidate = groups[state][0]
            if not too_many_same_state(candidate, output, max_same_state_in_row):
                output.append(groups[state].pop(0))
                remaining -= 1
                placed = True
                break
        if not placed:
            state = available_states[0]
            output.append(groups[state].pop(0))
            remaining -= 1
    return output


def create_rater_and_master_tables(samples):
    rater_packet, master_key = [], []
    for index, sample in enumerate(samples, start=1):
        blinded_id = f"S-{index:03d}"
        rater_packet.append({"sample_id": blinded_id, "text": sample["text"]})
        master_key.append({
            "sample_id": blinded_id,
            "original_id": sample["sample_id"],
            "expected_loop_state": sample["expected_loop_state"],
        })
    return rater_packet, master_key


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(rows, path, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def check_randomization(master_key):
    problems = []
    for i in range(len(master_key) - 2):
        window = master_key[i:i+3]
        states = [item["expected_loop_state"] for item in window]
        if len(set(states)) == 1:
            problems.append({"start": window[0]["sample_id"], "end": window[-1]["sample_id"], "state": states[0]})
    return problems


if __name__ == "__main__":
    samples = load_samples()
    randomized = stratified_shuffle(samples)
    rater_packet, master_key = create_rater_and_master_tables(randomized)
    save_json({"dataset_name": "continuity_engine_unlabeled_rater_packet_v1", "random_seed": RANDOM_SEED, "samples": rater_packet}, "outputs/unlabeled_rater_packet.json")
    save_json({"dataset_name": "continuity_engine_master_key_v1", "random_seed": RANDOM_SEED, "samples": master_key}, "outputs/master_key_internal.json")
    save_csv(rater_packet, "outputs/unlabeled_rater_packet.csv", ["sample_id", "text"])
    save_csv(master_key, "outputs/master_key_internal.csv", ["sample_id", "original_id", "expected_loop_state"])
    problems = check_randomization(master_key)
    print("Created rater packet and master key.")
    print(f"Randomization problems: {len(problems)}")
