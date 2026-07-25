from continuity_engine_v05 import (
    analyze_text_v05,
    calculate_revision_latency_v05,
    calculate_self_reference_features,
    self_reference_score_v05,
)


def test_self_reference_counts_occurrences_not_pattern_types():
    text = "I thought I failed because I believed I was wrong and I kept blaming myself."
    features = calculate_self_reference_features(text)
    assert features["self_reference_occurrences"] >= 5
    assert features["self_reference_density_per_100_words"] > 0


def test_self_reference_score_increases_with_density():
    low = self_reference_score_v05("I submitted the report.")
    high = self_reference_score_v05("I thought I failed because I believed I was wrong and I kept blaming myself.")
    assert high > low


def test_v05_exposes_classification_clarity_and_compatibility_alias():
    result = analyze_text_v05("I was frustrated, but I can see why the change was needed.")
    assert result.classification_clarity in {"High", "Medium", "Low"}
    assert result.confidence == result.classification_clarity
    assert "self_reference_density_per_100_words" in result.measurement_features


def test_latency_to_adaptive_counts_transitions():
    metrics = calculate_revision_latency_v05(["Rigid", "Flexible"])
    assert metrics["starts_destabilized"] is True
    assert metrics["latency_to_adaptive"] == 1
    assert metrics["latency_to_flexible"] == 1


def test_immediate_adaptive_sequence_is_not_recovery():
    metrics = calculate_revision_latency_v05(["Flexible", "Integrated"])
    assert metrics["starts_destabilized"] is False
    assert metrics["latency_to_adaptive"] is None
    assert metrics["latency_to_integrated"] is None
    assert metrics["recovery_arc"] == "No Initial Destabilization"


def test_empty_sequence_is_not_no_resolution():
    metrics = calculate_revision_latency_v05([])
    assert metrics["no_resolution"] is False
    assert metrics["recovery_arc"] == "No Text"


def test_normalized_trajectory_is_length_adjusted():
    short = calculate_revision_latency_v05(["Rigid", "Integrated"])
    repeated = calculate_revision_latency_v05(["Rigid", "Integrated", "Rigid", "Integrated"])
    assert short["normalized_trajectory_score"] == repeated["normalized_trajectory_score"]


def test_no_resolution_requires_initial_destabilization():
    destabilized = calculate_revision_latency_v05(["Rigid", "Mixed / Review Needed"])
    neutral = calculate_revision_latency_v05(["Stable/Neutral", "Mixed / Review Needed"])
    assert destabilized["no_resolution"] is True
    assert neutral["no_resolution"] is False
