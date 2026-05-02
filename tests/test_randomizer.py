"""Tests for randomize_rater_packet.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from randomize_rater_packet import (
    load_samples, stratified_shuffle, create_rater_and_master_tables,
    check_randomization, RANDOM_SEED, MAX_SAME_STATE_IN_ROW,
)


class TestStratifiedShuffle:
    def setup_method(self):
        self.samples = load_samples()
        self.randomized = stratified_shuffle(self.samples)

    def test_all_samples_preserved(self):
        assert len(self.randomized) == len(self.samples)

    def test_no_duplicates(self):
        ids = [s["sample_id"] for s in self.randomized]
        assert len(ids) == len(set(ids))

    def test_no_three_in_a_row(self):
        for i in range(len(self.randomized) - 2):
            window = self.randomized[i:i+3]
            states = [s["expected_loop_state"] for s in window]
            assert len(set(states)) > 1, f"Three in a row at index {i}: {states}"

    def test_deterministic_with_seed(self):
        """Same seed should produce same order."""
        r1 = stratified_shuffle(self.samples, seed=RANDOM_SEED)
        r2 = stratified_shuffle(self.samples, seed=RANDOM_SEED)
        assert [s["sample_id"] for s in r1] == [s["sample_id"] for s in r2]


class TestBlinding:
    def setup_method(self):
        samples = load_samples()
        randomized = stratified_shuffle(samples)
        self.rater_packet, self.master_key = create_rater_and_master_tables(randomized)

    def test_rater_packet_has_no_labels(self):
        for item in self.rater_packet:
            assert "expected_loop_state" not in item
            assert "original_id" not in item

    def test_rater_ids_are_blinded(self):
        for item in self.rater_packet:
            assert item["sample_id"].startswith("S-")
            assert not item["sample_id"].startswith("FLEX")
            assert not item["sample_id"].startswith("INT")

    def test_master_key_has_labels(self):
        for item in self.master_key:
            assert "expected_loop_state" in item
            assert "original_id" in item

    def test_master_key_matches_rater_packet(self):
        rater_ids = [r["sample_id"] for r in self.rater_packet]
        master_ids = [m["sample_id"] for m in self.master_key]
        assert rater_ids == master_ids

    def test_check_randomization_clean(self):
        problems = check_randomization(self.master_key)
        assert len(problems) == 0
