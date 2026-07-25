"""
Continuity Engine v0.5 experimental measurement layer.

This module preserves continuity_engine.py (v0.4.1-alpha) as the frozen
research baseline while implementing selected measurement corrections from
MEASUREMENT_SPEC.md and QA_REPORT_2026-07-25.md.

It is still a research prototype. It classifies textual patterns, not people,
and is not a diagnostic or psychological assessment instrument.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

from continuity_engine import (
    ADAPTIVE_STATES,
    DESTABILIZED_STATES,
    STATE_VALUES,
    ScoreResult,
    calculate_indexes,
    calculate_recovery_stability,
    classify_because_attribution,
    classify_but_hinges,
    classify_loop_state,
    find_markers,
    marker_count,
    normalize_text,
    score_dimensions,
)


@dataclass
class V05ScoreResult:
    """v0.5 result with clearer semantics for rule-derived certainty."""

    text: str
    scores: Dict[str, int]
    indexes: Dict[str, float]
    markers: Dict[str, List[str]]
    hinge_results: Dict[str, Any]
    loop_state: str
    classification_clarity: str
    explanation: str
    measurement_features: Dict[str, Any]

    @property
    def confidence(self) -> str:
        """Backward-compatible alias. Not statistical confidence."""
        return self.classification_clarity


SELF_REFERENCE_PATTERN = re.compile(r"\b(i|me|my|mine|myself)\b", re.IGNORECASE)
WORD_PATTERN = re.compile(r"\b[\w']+\b")


def calculate_self_reference_features(text: str) -> Dict[str, float]:
    """Measure actual first-person occurrence density rather than marker diversity.

    Density is occurrences per 100 word tokens. The current thresholds are
    provisional machine operationalizations and must be validated against the
    human rubric before being treated as construct-valid cut points.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    words = WORD_PATTERN.findall(text)
    occurrences = SELF_REFERENCE_PATTERN.findall(text)
    word_count = len(words)
    occurrence_count = len(occurrences)
    density_per_100 = (occurrence_count / word_count * 100.0) if word_count else 0.0

    return {
        "word_count": word_count,
        "self_reference_occurrences": occurrence_count,
        "self_reference_density_per_100_words": density_per_100,
    }


def self_reference_score_v05(text: str, third_person_self_distance: bool = False) -> int:
    """Provisional 0-3 machine score for Self-Reference Density.

    Unlike v0.4.1, this uses actual occurrence density rather than the number of
    distinct regex patterns that happened to match.
    """
    features = calculate_self_reference_features(text)
    count = int(features["self_reference_occurrences"])
    density = float(features["self_reference_density_per_100_words"])

    if count == 0:
        score = 0
    elif count == 1 and density < 10:
        score = 1
    elif count <= 3 or density < 20:
        score = 2
    else:
        score = 3

    # Preserve the existing framework's explicit third-person self-distance
    # treatment while keeping it visible as a separate machine rule.
    if third_person_self_distance:
        score = max(score, 2)

    return score


def score_dimensions_v05(
    text: str,
    markers: Dict[str, List[str]],
    hinges: Dict[str, Any],
) -> Dict[str, int]:
    """Apply the frozen v0.4.1 scoring logic, then correct SR measurement.

    Other dimensions remain v0.4.1 operationalizations until separately
    validated and migrated. This incremental approach prevents a theory change,
    feature rewrite, and classifier rewrite from being confounded in one step.
    """
    scores = score_dimensions(text, markers, hinges)
    scores["self_reference"] = self_reference_score_v05(
        text,
        third_person_self_distance=marker_count(markers, "third_person_self_distance") > 0,
    )
    return scores


def analyze_text_v05(text: str) -> V05ScoreResult:
    """Analyze text using the v0.5 experimental measurement layer."""
    if not isinstance(text, str):
        raise TypeError(f"analyze_text_v05 expected a string, got {type(text).__name__}.")
    if not text.strip():
        raise ValueError("analyze_text_v05 received empty or whitespace-only text.")

    markers = find_markers(text)
    hinges = {
        "but": classify_but_hinges(text),
        "because_attribution": classify_because_attribution(text),
    }
    scores = score_dimensions_v05(text, markers, hinges)
    indexes = calculate_indexes(scores, markers, hinges)
    loop_state, explanation, rule_clarity = classify_loop_state(
        text, scores, indexes, markers, hinges
    )

    features = calculate_self_reference_features(text)
    features["self_reference_score_v05"] = scores["self_reference"]

    return V05ScoreResult(
        text=text,
        scores=scores,
        indexes=indexes,
        markers=markers,
        hinge_results=hinges,
        loop_state=loop_state,
        classification_clarity=rule_clarity,
        explanation=explanation,
        measurement_features=features,
    )


def calculate_revision_latency_v05(state_sequence: List[str]) -> Dict[str, Any]:
    """Corrected Revision Latency semantics for v0.5.

    Changes from v0.4.1:
    - `latency_to_adaptive` correctly names the first Flexible OR Integrated state.
    - Latency counts transitions elapsed from the starting unit, so immediate
      adaptation is zero rather than one.
    - Recovery latency is only defined when the sequence starts destabilized.
    - `latency_to_integrated` is likewise a transition count and only represents
      recovery when starting destabilized.
    - Adds normalized trajectory score for cross-document comparability.
    - Retains deprecated `latency_to_flexible` as an alias for compatibility.
    """
    if not state_sequence:
        return {
            "latency_to_adaptive": None,
            "latency_to_flexible": None,
            "latency_to_integrated": None,
            "stalled_state_count": 0,
            "no_resolution": False,
            "regression_count": 0,
            "final_state": None,
            "recovery_arc": "No Text",
            "trajectory_score": 0,
            "normalized_trajectory_score": 0.0,
            "recovery_stability": 0.0,
            "starts_destabilized": False,
            "state_sequence": [],
        }

    starts_destabilized = state_sequence[0] in DESTABILIZED_STATES

    adaptive_index = next(
        (i for i, state in enumerate(state_sequence) if state in ADAPTIVE_STATES),
        None,
    )
    integrated_index = next(
        (i for i, state in enumerate(state_sequence) if state == "Integrated"),
        None,
    )

    latency_to_adaptive = adaptive_index if starts_destabilized else None
    latency_to_integrated = integrated_index if starts_destabilized else None

    stalled = 0
    if starts_destabilized:
        for state in state_sequence:
            if state in ADAPTIVE_STATES:
                break
            stalled += 1

    no_resolution = starts_destabilized and latency_to_adaptive is None
    regression_count = sum(
        1
        for previous, current in zip(state_sequence, state_sequence[1:])
        if previous in ADAPTIVE_STATES and current in DESTABILIZED_STATES
    )

    if all(state == "Stable/Neutral" for state in state_sequence):
        arc = "Stable Neutral"
    elif regression_count:
        arc = "Regression After Recovery"
    elif no_resolution:
        arc = "No Resolution"
    elif starts_destabilized and latency_to_integrated is not None:
        arc = "Fast Integration" if latency_to_integrated <= 1 else "Gradual Integration"
    elif starts_destabilized and latency_to_adaptive is not None:
        arc = "Fast Partial Recovery" if latency_to_adaptive <= 1 else "Gradual Partial Recovery"
    elif not starts_destabilized:
        arc = "No Initial Destabilization"
    else:
        arc = "Mixed / Unclear"

    trajectory_score = sum(STATE_VALUES.get(state, 0) for state in state_sequence)
    normalized_trajectory = trajectory_score / len(state_sequence)

    return {
        "latency_to_adaptive": latency_to_adaptive,
        # Deprecated compatibility alias. The v0.4.1 field never meant
        # specifically Flexible; it meant the first adaptive state.
        "latency_to_flexible": latency_to_adaptive,
        "latency_to_integrated": latency_to_integrated,
        "stalled_state_count": stalled,
        "no_resolution": no_resolution,
        "regression_count": regression_count,
        "final_state": state_sequence[-1],
        "recovery_arc": arc,
        "trajectory_score": trajectory_score,
        "normalized_trajectory_score": normalized_trajectory,
        "recovery_stability": calculate_recovery_stability(state_sequence),
        "starts_destabilized": starts_destabilized,
        "state_sequence": state_sequence,
    }


def analyze_document_v05(text: str) -> Dict[str, Any]:
    """Analyze newline-separated units with corrected v0.5 latency metrics.

    Paragraphs remain a provisional narrative-unit proxy. THEORY.md and
    MEASUREMENT_SPEC.md explicitly identify narrative-unit definition as future
    construct work.
    """
    if not isinstance(text, str):
        raise TypeError(f"analyze_document_v05 expected a string, got {type(text).__name__}.")

    paragraphs = [paragraph.strip() for paragraph in text.split("\n") if paragraph.strip()]
    paragraph_results = []
    state_sequence: List[str] = []

    for number, paragraph in enumerate(paragraphs, start=1):
        result = analyze_text_v05(paragraph)
        state_sequence.append(result.loop_state)
        paragraph_results.append(
            {
                "paragraph_number": number,
                "text": paragraph,
                "loop_state": result.loop_state,
                "classification_clarity": result.classification_clarity,
                "confidence": result.confidence,
                "scores": result.scores,
                "indexes": result.indexes,
                "measurement_features": result.measurement_features,
                "explanation": result.explanation,
            }
        )

    return {
        "paragraph_results": paragraph_results,
        "state_sequence": state_sequence,
        "latency_metrics": calculate_revision_latency_v05(state_sequence),
    }
