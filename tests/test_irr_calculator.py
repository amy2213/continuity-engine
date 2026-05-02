"""Tests for irr_calculator.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from irr_calculator import (
    normalize_state, cohen_kappa, fleiss_kappa,
    percent_agreement_primary_state, CANONICAL_STATES,
)


class TestNormalizeState:
    def test_canonical_passthrough(self):
        assert normalize_state("Flexible") == "Flexible"
        assert normalize_state("Mixed / Review Needed") == "Mixed / Review Needed"

    def test_common_variants(self):
        assert normalize_state("Stable / Neutral") == "Stable/Neutral"
        assert normalize_state("Mixed") == "Mixed / Review Needed"
        assert normalize_state("Mixed/Review") == "Mixed / Review Needed"
        assert normalize_state("Mixed / Review") == "Mixed / Review Needed"

    def test_whitespace_handling(self):
        assert normalize_state("  Flexible  ") == "Flexible"

    def test_none_handling(self):
        assert normalize_state(None) == ""

    def test_unknown_passthrough(self):
        assert normalize_state("Something Else") == "Something Else"


class TestCohenKappa:
    def test_perfect_agreement(self):
        labels = ["Flexible", "Rigid", "Defensive"]
        k = cohen_kappa(labels, labels, CANONICAL_STATES)
        assert math.isclose(k, 1.0)

    def test_no_agreement(self):
        a = ["Flexible", "Flexible", "Flexible"]
        b = ["Rigid", "Rigid", "Rigid"]
        k = cohen_kappa(a, b, CANONICAL_STATES)
        assert k < 0.01  # should be near 0 or negative

    def test_partial_agreement(self):
        a = ["Flexible", "Rigid", "Defensive", "Integrated"]
        b = ["Flexible", "Rigid", "Flexible", "Integrated"]
        k = cohen_kappa(a, b, CANONICAL_STATES)
        assert 0.0 < k < 1.0

    def test_empty_raises_or_returns_zero(self):
        k = cohen_kappa([], [], CANONICAL_STATES)
        assert k == 0.0

    def test_mismatched_lengths_raises(self):
        import pytest
        with pytest.raises(ValueError):
            cohen_kappa(["Flexible"], ["Flexible", "Rigid"], CANONICAL_STATES)


class TestFleissKappa:
    def test_returns_none_for_two_raters(self):
        """Fleiss requires 3+ raters."""
        coder_data = {
            "c1": {"s1": {"primary_state": "Flexible"}},
            "c2": {"s1": {"primary_state": "Flexible"}},
        }
        k = fleiss_kappa(coder_data, ["s1"])
        assert k is None

    def test_perfect_agreement_three_raters(self):
        coder_data = {
            "c1": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
            "c2": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
            "c3": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
        }
        k = fleiss_kappa(coder_data, ["s1", "s2"])
        assert math.isclose(k, 1.0)


class TestPercentAgreement:
    def test_full_agreement(self):
        coder_data = {
            "c1": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
            "c2": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
        }
        pa = percent_agreement_primary_state(coder_data, ["s1", "s2"])
        assert math.isclose(pa, 1.0)

    def test_no_agreement(self):
        coder_data = {
            "c1": {"s1": {"primary_state": "Flexible"}, "s2": {"primary_state": "Rigid"}},
            "c2": {"s1": {"primary_state": "Rigid"}, "s2": {"primary_state": "Flexible"}},
        }
        pa = percent_agreement_primary_state(coder_data, ["s1", "s2"])
        assert math.isclose(pa, 0.0)
