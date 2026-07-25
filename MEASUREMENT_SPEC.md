# Continuity Engine Measurement Specification

## Purpose

This document separates the Mid-Process Identity Loop constructs from the current software observables used to approximate them.

The human construct definition is authoritative. Machine features are implementation hypotheses and may be changed when evidence shows they do not adequately represent the construct.

## Locked principle

> Do not simplify the theory to match the current classifier. Improve the classifier to better approximate the theory.

## Construct-to-machine map

| Construct | Human definition | Current machine approximation | Known issue | Next action |
|---|---|---|---|---|
| Self-Reference Density | Degree to which the self is the subject of the text | Count of distinct matching self-reference regex patterns, capped at 3 | Not true density; repeated occurrences of the same marker are collapsed | Count occurrences and normalize by token count |
| Identity Fixity | Degree of fixed, global, or permanent self-model claims | Count of distinct fixity regex patterns, capped at 3 | Marker diversity is not semantic dominance | Develop anchored features for globality, permanence, and self-reference scope |
| Prediction | Degree to which outcomes are preloaded or anticipated | Count of prediction marker types plus hinge modifiers | Does not distinguish mild expectation from load-bearing prediction reliably | Add intensity and scope features |
| Threat Weighting | Degree to which meaning is organized around danger, rejection, failure, or loss | Threat marker counts plus auxiliary floors | Literal threat terms can fire outside identity context | Add identity relevance and attribution scope |
| Feedback Integration | Degree to which external input is incorporated or used | Integration marker counts plus hinge modifiers | Surface acknowledgment may be mistaken for genuine incorporation | Require evidence of use, revision, or partial acceptance where possible |
| Narrative Flexibility | Capacity to hold ambiguity, complexity, or multiple perspectives | Flexibility markers and hinge modifiers | Distinct phrases are not equivalent to sustained flexibility | Add clause-level and passage-level structure features |
| Fragmentation | Unresolved competition between incompatible self-models | Fragmentation markers, bodily split markers, hinge logic | Ordinary contradiction may be confused with unresolved model competition | Require unresolved competing models, not contradiction alone |
| Updated Continuity | Explicit self-model revision with preserved self-thread | Integration markers and rule cascade | Currently mixes revision and continuity into one score | Separate Revision Magnitude and Continuity Preservation experimentally |

## Scoring problem in v0.4.1-alpha

The current engine mostly uses this pattern:

1. detect whether each regex appears,
2. count matching regex patterns,
3. cap the count at 3.

The human rubric instead defines scores semantically:

- 0: absent
- 1: weak or implied
- 2: clear
- 3: dominant or load-bearing

These are not equivalent scales.

A future version must not interpret numeric agreement between the two systems as construct agreement until their operational definitions are aligned.

## Proposed next-generation feature families

### 1. Frequency

How often a construct-relevant expression occurs.

Example for self-reference:

SelfReferenceDensity = self_reference_occurrences / token_count

### 2. Scope

Whether a marker applies to:
- the writer,
- another person,
- quoted speech,
- a hypothetical person,
- a team or institution.

### 3. Intensity

Whether language is mild, clear, global, permanent, catastrophic, or dominant.

### 4. Structural centrality

Whether a construct is incidental or organizes the passage.

### 5. Resolution status

Whether a conflict is:
- unresolved,
- partially resolved,
- fully revised,
- merely acknowledged.

### 6. Temporal direction

Whether a statement refers to:
- prior self-model,
- current self-model,
- anticipated future self-model.

This is especially important for Updated Continuity.

## Confidence terminology

The current `High`, `Medium`, and `Low` values are rule-derived clarity labels, not calibrated probabilities.

Until empirical calibration exists, public and research documentation should interpret these as:

- High = strong rule clarity
- Medium = moderate rule clarity
- Low = ambiguous rule evidence

Preferred future field name: `classification_clarity`.

## State precedence specification requirement

The rule cascade order encodes theoretical assumptions. Future versions must document why one state takes precedence over another in collision cases.

Priority decisions to formalize include:

- Defensive vs Rigid
- Fragmented vs Integrated
- Overloaded vs Fragmented
- Flexible vs Integrated
- Boundary vs Defensive
- Mixed vs any confident classification

## Revision Latency measurement corrections

The current implementation uses paragraph positions. Future work should distinguish:

- `latency_to_adaptive`: first Flexible or Integrated state after destabilization
- `latency_to_integrated`: first Integrated state after destabilization
- transition count: number of transitions elapsed, where immediate adaptation after the starting unit has latency 0
- unit definition: paragraph is currently a formatting proxy, not a theoretically validated narrative unit

Trajectory score should be reported both raw and normalized by number of units.

## Candidate future constructs

The following are theory variables, not yet machine dimensions:

- Revision Pressure
- Revision Capacity
- Evidence Weighting
- Revision Depth
- Revision Magnitude
- Continuity Preservation

They must not be converted into regex categories without a construct definition and validation plan.

## Validation rule

Human coding reliability must be tested before engine agreement is treated as meaningful.

The minimum sequence is:

1. validate human rubric reliability,
2. refine constructs from disagreement,
3. freeze a human-coded held-out set,
4. evaluate the engine against that frozen set,
5. perform ablation and cross-domain testing.
