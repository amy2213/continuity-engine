"""Adversarial regression tests loaded from test_adversarial.json."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from continuity_engine import analyze_text

ADVERSARIAL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "test_adversarial.json"
)


def load_adversarial():
    with open(ADVERSARIAL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["samples"]


@pytest.fixture
def adversarial_samples():
    return load_adversarial()


class TestAdversarialDataset:
    def test_all_adversarial_samples_pass(self, adversarial_samples):
        failures = []
        for sample in adversarial_samples:
            result = analyze_text(sample["text"])
            if result.loop_state != sample["expected_loop_state"]:
                failures.append(
                    f"{sample['sample_id']}: expected {sample['expected_loop_state']}, "
                    f"got {result.loop_state} — {sample.get('notes', '')}"
                )
        if failures:
            pytest.fail("Adversarial failures:\n" + "\n".join(failures))

    def test_adversarial_file_exists(self):
        assert os.path.exists(ADVERSARIAL_PATH)

    def test_adversarial_has_minimum_samples(self, adversarial_samples):
        assert len(adversarial_samples) >= 20


class TestPilotDataset:
    """Ensure pilot dataset still passes after code changes."""

    def test_pilot_60_samples_pass(self):
        pilot_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sample_texts.json"
        )
        with open(pilot_path, "r", encoding="utf-8") as f:
            samples = json.load(f)["samples"]

        failures = []
        for sample in samples:
            result = analyze_text(sample["text"])
            if result.loop_state != sample["expected_loop_state"]:
                failures.append(
                    f"{sample['sample_id']}: expected {sample['expected_loop_state']}, "
                    f"got {result.loop_state}"
                )
        assert len(failures) == 0, f"Pilot regressions:\n" + "\n".join(failures)
