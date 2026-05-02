"""Tests for but-hinge and because-attribution classifiers."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from continuity_engine import classify_but_hinges, classify_because_attribution


class TestButHinges:
    def test_integrated_but(self):
        labels = classify_but_hinges("I was wrong about that, but I can see the thread now.")
        assert "integrated_but" in labels

    def test_flexible_but(self):
        labels = classify_but_hinges("I was upset, but I can understand why they did it.")
        assert "flexible_but" in labels

    def test_defensive_but(self):
        labels = classify_but_hinges("Maybe I could change my approach, but they are missing the point.")
        assert "defensive_but" in labels

    def test_fragmented_but(self):
        labels = classify_but_hinges("I trust her, but I keep testing whether she will leave.")
        assert "fragmented_but" in labels

    def test_rigid_but(self):
        labels = classify_but_hinges("I try new words, but the pattern never changes.")
        assert "rigid_but" in labels

    def test_no_but_returns_empty(self):
        labels = classify_but_hinges("I am doing fine today.")
        assert labels == []

    def test_neutral_but_is_unclassified(self):
        labels = classify_but_hinges("I like pizza, but I prefer pasta.")
        assert "unclassified_but" in labels


class TestBecauseAttribution:
    def test_evidence_based(self):
        result = classify_because_attribution("I disagreed because the data does not support it.")
        assert result["dominant_attribution"] == "evidence_based"

    def test_process_reflective(self):
        result = classify_because_attribution("I reacted because I was trying to protect myself.")
        assert result["dominant_attribution"] == "process_reflective"

    def test_external_blame(self):
        result = classify_because_attribution("It failed because they do not understand.")
        assert result["dominant_attribution"] == "external_blame"

    def test_fixed_self(self):
        result = classify_because_attribution("It happened because I always do this.")
        assert result["dominant_attribution"] == "fixed_self"

    def test_threat_projection(self):
        result = classify_because_attribution("I panicked because they will leave.")
        assert result["dominant_attribution"] == "threat_projection"

    def test_no_because(self):
        result = classify_because_attribution("I am fine today.")
        assert result["dominant_attribution"] is None
        assert result["attribution_modifier"] == "No Because Attribution"
