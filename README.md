# Continuity Engine

A rule-based narrative analysis prototype implementing the Mid-Process Identity Loop framework.

> **Core thesis:** Identity is continuity under revision.

**Frozen baseline:** v0.4.1-alpha  
**Active measurement layer:** v0.5 research implementation  
**Status:** Research prototype. Internal consistency verified. Human validation pending.  
**License:** MIT

https://amy2213.github.io/continuity-engine/

---

## What This Is

Continuity Engine classifies short text samples according to the Mid-Process Identity Loop, an original theoretical framework proposing that identity-relevant language can be analyzed along eight dimensions and mapped to one of eight loop states.

It analyzes language patterns related to self-reference, identity fixity, prediction, threat weighting, feedback integration, narrative flexibility, fragmentation, and updated continuity.

It is **not** a diagnostic, therapeutic, or psychological assessment tool. It does not measure personality, mental health, competence, or character. It classifies textual patterns.

The Mid-Process Identity Loop is an original framework by the author. It is not an established or externally validated psychological theory.

### Research governance

The repository separates four layers that must not be conflated:

- [`THEORY.md`](THEORY.md) — locked expanded theory baseline
- [`MEASUREMENT_SPEC.md`](MEASUREMENT_SPEC.md) — human constructs versus current machine observables
- [`QA_REPORT_2026-07-25.md`](QA_REPORT_2026-07-25.md) — full QA findings and issue ledger
- [`ROADMAP_V0_5.md`](ROADMAP_V0_5.md) — research and implementation sequence for v0.5

The original `continuity_engine.py` v0.4.1-alpha classifier remains the frozen operational baseline. The v0.5 implementation lives beside it in `continuity_engine_v05.py` so old and new behavior remain reproducible and directly comparable.

---

## Version Architecture

### v0.4.1-alpha — frozen baseline

`continuity_engine.py` preserves the original marker detection, scoring, classification cascade, and Revision Latency behavior used for the initial internal-consistency and regression results.

### v0.5 — active measurement layer

`continuity_engine_v05.py` begins the migration from proxy implementation behavior toward the locked measurement specification.

Current v0.5 corrections include:

- true first-person occurrence counting for Self-Reference Density
- self-reference density normalized per 100 words
- provisional density-based SR scoring with an explicit validation warning
- `classification_clarity` terminology instead of implying calibrated statistical confidence
- backward-compatible `confidence` alias
- corrected Revision Latency semantics
- `latency_to_adaptive` naming
- transition-count latency rather than one-based position
- recovery latency only when the sequence begins in a destabilized state
- normalized trajectory score
- explicit `starts_destabilized` output

Only Self-Reference Density has been migrated to a revised machine observable so far. The other seven dimensions still depend on v0.4.1 scoring logic until each construct is validated and migrated separately.

---

## How It Works

### v0.4.1 baseline pipeline

```text
Text input
  → Marker detection (regex pattern matching across 20+ categories)
  → Hinge classification (but-clauses, because-attribution)
  → Dimension scoring (8 scored dimensions, 0–3 scale)
  → Index calculation (rigidity, integration, threat-prediction, discernment)
  → Loop-state classification (rule-based cascade)
  → Optional: revision-latency analysis (multi-paragraph trajectories)
```

### Eight Scored Dimensions

| # | Dimension              | Abbreviation | What It Measures                         |
|---|------------------------|--------------|------------------------------------------|
| 1 | Self-Reference Density | SR           | First-person or self-modeling language   |
| 2 | Identity Fixity        | IF           | Fixed, permanent, or global self-claims  |
| 3 | Prediction             | PR           | Expectation and anticipation language    |
| 4 | Threat Weighting       | TH           | Perceived danger, rejection, or failure  |
| 5 | Feedback Integration   | FI           | Incorporation of external input          |
| 6 | Narrative Flexibility  | NF           | Openness, ambiguity tolerance, revision  |
| 7 | Fragmentation          | FR           | Competing self-models, internal splits   |
| 8 | Updated Continuity     | UC           | Explicit identity revision with thread   |

### Measurement warning

The frozen v0.4.1-alpha software scores many dimensions by counting distinct matched regex patterns and capping at 3. The human rubric defines 0–3 semantically as absent, weak/implied, clear, and dominant/load-bearing. These are not operationally equivalent scales.

v0.5 begins correcting this mismatch one construct at a time. Self-Reference Density now uses actual first-person occurrence density, but its score thresholds remain provisional until human validation establishes defensible anchors.

For the locked construct-to-machine specification and required corrections, see [`MEASUREMENT_SPEC.md`](MEASUREMENT_SPEC.md).

### Auxiliary Marker Categories

These categories influence scoring and classification but are not independently scored dimensions: bodily distress, sarcasm, rumination, boundary-setting, accountability, partial acceptance, context markers, weaponized evidence, ego-evidence ambiguity, third-person self-distance, feedback rejection, discernment, agency collapse, and unresolved resolution.

### Eight Loop States

| State                  | Description                                              |
|------------------------|----------------------------------------------------------|
| Flexible               | Adaptive processing without explicit identity revision   |
| Integrated             | Updated continuity with self-model revision              |
| Defensive              | External blame, dismissal, or feedback rejection         |
| Rigid                  | Fixed identity claims, fatalistic prediction             |
| Fragmented             | Competing self-models without resolution                 |
| Overloaded             | Agency, meaning, or action collapses                     |
| Stable/Neutral         | No meaningful identity activity                          |
| Mixed / Review Needed  | Ambiguous, sarcastic, or insufficient for classification |

These are classifications of textual processing configurations, not labels for people.

---

## Expanded Theory Baseline

The theory baseline formalizes identity as a continuity-constrained self-model that recursively incorporates new evidence.

A conceptual representation is:

```text
M_(t+1) = U(M_t, E_t, C_t)
```

where the revised self-model depends on the prior self-model, incoming evidence, and context.

The expanded theory introduces research constructs including:

- Revision Pressure
- Revision Capacity
- Evidence Weighting
- Revision Depth
- Revision Magnitude
- Continuity Preservation

It also introduces a transition-first hypothesis: the movement from one processing state to another may ultimately be more informative than isolated state classification.

These are theory constructs and research hypotheses. They are **not yet additional machine-scored dimensions**.

See [`THEORY.md`](THEORY.md) for the full locked formulation.

---

## File Structure

```text
continuity-engine/
├── continuity_engine.py              # frozen v0.4.1-alpha baseline classifier
├── continuity_engine_v05.py          # active v0.5 measurement layer
├── THEORY.md                         # locked expanded Mid-Process Identity Loop theory
├── MEASUREMENT_SPEC.md               # construct-to-machine operationalization specification
├── QA_REPORT_2026-07-25.md           # full QA issue ledger
├── ROADMAP_V0_5.md                   # validation-first v0.5 implementation roadmap
├── sample_texts.json                 # 60-sample labeled pilot dataset
├── test_adversarial.json             # 20-sample adversarial/edge-case regression set
├── run_verification.py               # verification runner
├── randomize_rater_packet.py         # seeded/blinded rater-packet generator
├── irr_calculator.py                 # inter-rater reliability calculator
├── methodology/
│   ├── irr_packet_v1_3.md            # rater instructions
│   ├── narrative_analysis_rubric_v1.md
│   └── revision_latency_v0_2.md
├── tests/
│   └── test_v05_measurement.py       # v0.5 measurement regression tests
├── outputs/                          # generated verification results and rater packets
└── docs/                             # documentation site files
```

---

## Documentation Site Files

Static documentation lives in [`docs/`](docs/). It contains `index.html` and a `loop-diagram.png` illustrating the Mid-Process Identity Loop. These files can be served as a GitHub Pages site.

---

## Quick Start

### Run existing verification workflows

```bash
# Run pilot verification (60 calibration samples)
python run_verification.py

# Run adversarial tests (20 edge cases)
python run_verification.py --dataset test_adversarial.json

# Exploration mode
python run_verification.py --dataset your_data.json --no-labels

# Generate blinded rater packet
python randomize_rater_packet.py

# Run all tests
python -m pytest tests/
```

### Use the frozen v0.4.1 baseline directly

```python
from continuity_engine import analyze_text

result = analyze_text("I was frustrated, but I can see why the change was needed.")

print(result.loop_state)
print(result.confidence)
print(result.explanation)
print(result.scores)
```

### Use the v0.5 measurement layer

```python
from continuity_engine_v05 import analyze_text_v05

result = analyze_text_v05("I thought I had failed, but now I can see another explanation.")

print(result.loop_state)
print(result.classification_clarity)
print(result.self_reference_count)
print(result.self_reference_density_per_100_words)
print(result.scores)
```

`classification_clarity` describes how directly the current rule set supports the assigned label. It is **not** a calibrated probability that the classification is correct.

---

## Revision Latency

The frozen v0.4.1 implementation remains available for reproducibility.

The v0.5 measurement layer corrects the main semantics identified in QA:

- `latency_to_adaptive` means transitions from an initially destabilized state to the first Flexible or Integrated state
- immediate adaptive recovery after the first state is counted as 1 transition, not position 2
- recovery latency is not reported when the sequence did not begin destabilized
- `latency_to_integrated` is separate from `latency_to_adaptive`
- `starts_destabilized` is explicit
- normalized trajectory score is reported in addition to raw trajectory score

The current document-analysis workflow still uses newline-separated paragraphs as practical analysis units. Paragraphs are formatting units, not a validated definition of narrative units. That remains an open research problem.

---

## IRR Calculator

After raters return completed CSVs as `coder_1.csv`, `coder_2.csv`, and `coder_3.csv`:

```bash
python irr_calculator.py
```

Writes `outputs/irr_summary.json` and `outputs/disagreement_review.csv`.

### Required Coder CSV Columns

```text
sample_id,SR,IF,PR,TH,FI,NF,FR,UC,primary_state,secondary_state,confidence,notes
```

The current IRR tooling remains part of the research prototype. The QA report identifies required input-hardening work before formal validation, including strict state validation, range checks, duplicate-ID detection, explicit missingness reporting, and stronger ordinal reliability statistics.

---

## Validation Status

The frozen v0.4.1 pilot dataset (60 samples) achieves 100% classification accuracy. This is an **internal consistency result**, not external validation. The samples were hand-authored for calibration and used during rule development.

The adversarial test set (20 samples) achieves 100% accuracy against documented expected outcomes. These are **regression tests**. They verify that known bugs stay fixed and known edge cases are handled. They are not external validation.

The v0.5 implementation has dedicated regression tests and passed the repository CI matrix on Python 3.8, 3.11, and 3.12 at merge time. This confirms implementation consistency, not construct validity or generalization.

**What is currently supported:**

- the rules are internally consistent on their designed calibration samples
- regression behavior is stable on the documented adversarial cases
- v0.5 measurement corrections execute successfully across the CI matrix
- old and new implementations remain reproducible side by side

**What is not proven:**

- generalization to unseen real-world text
- agreement with independent human raters
- construct validity of the eight dimensions
- validity of provisional v0.5 SR thresholds
- real-world predictive power
- clinical usefulness
- population generalization

**Next required sequence:** Human construct reliability → construct refinement → frozen human-coded held-out set → engine evaluation → ablation → cross-domain testing.

For planned validation work, see [`RESEARCH_AGENDA.md`](RESEARCH_AGENDA.md) and [`ROADMAP_V0_5.md`](ROADMAP_V0_5.md).

---

## Limitations

| Limitation | Explanation |
|---|---|
| Rule-based | Cannot infer deep context, intent, or meaning reliably |
| English-only | Markers are US-English dominant |
| Synthetic pilot dataset | Does not demonstrate generalization |
| Sarcasm weakness | Only surface sarcasm patterns detected |
| Negation weakness | Limited negation handling; context-dependent |
| Speaker attribution | Quoted speech and multi-speaker text remain high-risk cases |
| Partial measurement migration | Only SR has been migrated to a revised v0.5 observable so far |
| Provisional SR thresholds | Density thresholds are not yet human-validated |
| Short-text optimized | Designed primarily for short reflective samples |
| Paragraph trajectory proxy | Paragraphs are formatting units, not validated narrative units |
| Not diagnostic | Labels describe text patterns, not people |
| Unpublished theory | Mid-Process Identity Loop is original and unvalidated |

For detailed edge cases, see [`KNOWN_FAILURE_MODES.md`](KNOWN_FAILURE_MODES.md) and [`QA_REPORT_2026-07-25.md`](QA_REPORT_2026-07-25.md).

---

## Ethics and Usage Policy

**Do not use this tool to evaluate, rank, punish, diagnose, or profile individuals.**

This tool classifies language patterns in text. It does not assess the writer's mental health, character, competence, or worth. Classifications describe textual patterns, not people.

### Acceptable Use

- Your own writing, for personal reflection
- Anonymized text, for research purposes
- Consented text, with appropriate safeguards
- Research coding, as a pre-classification or hypothesis-generation tool

### Unacceptable Use

- Evaluating employees, students, or patients based on loop-state classifications
- Using labels such as Defensive, Rigid, or Overloaded to characterize individuals
- Surveillance or coercive monitoring of writing
- Clinical diagnosis or treatment planning

### Safer Label Language

| Internal Label | Suggested Public Label |
|----------------|------------------------|
| Defensive      | Protective Pattern     |
| Rigid          | Fixed Pattern          |
| Fragmented     | Split Pattern          |
| Overloaded     | Overwhelm Pattern      |
| Flexible       | Adaptive Pattern       |
| Integrated     | Integrated Pattern     |

---

## Citation

The repository citation currently refers to the frozen v0.4.1-alpha software baseline. The v0.5 measurement layer is an active research implementation and should not yet be presented as a separately validated release.

```bibtex
@software{continuity_engine,
  title   = {Continuity Engine: A Rule-Based Narrative Analysis Framework},
  author  = {Laird, Amy},
  year    = {2026},
  version = {0.4.1-alpha},
  url     = {https://github.com/amy2213/continuity-engine},
  note    = {Research prototype. Mid-Process Identity Loop is an original framework.}
}
```

---

## Contributing

Contributions welcome, especially:

- real-world text samples that are anonymized and consented
- adversarial test cases that expose failure modes
- translations or adaptations of marker sets for other languages
- independent rater data for IRR validation
- bug reports and edge-case documentation

Please do not submit changes that expand validation claims beyond the evidence currently available or tune the known-weakness challenge set into another artificial 100% result.

---

## Requirements

Python 3.8+. No external runtime dependencies. Standard library only.
