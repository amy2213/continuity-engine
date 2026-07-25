# Continuity Engine

A rule-based narrative analysis prototype implementing the Mid-Process Identity Loop framework.

> **Core thesis:** Identity is continuity under revision.

**Version:** 0.4.1-alpha  
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

The repository now separates four layers that must not be conflated:

- [`THEORY.md`](THEORY.md) — locked expanded theory baseline
- [`MEASUREMENT_SPEC.md`](MEASUREMENT_SPEC.md) — human constructs versus current machine observables
- [`QA_REPORT_2026-07-25.md`](QA_REPORT_2026-07-25.md) — full QA findings and issue ledger
- [`ROADMAP_V0_5.md`](ROADMAP_V0_5.md) — research and implementation sequence for v0.5

The v0.4.1-alpha classifier remains the operational baseline. The new theory documents do **not** retroactively claim that the current implementation already measures every expanded construct.

---

## How It Works

```
Text input
  → Marker detection (regex pattern matching across 20+ categories)
  → Hinge classification (but-clauses, because-attribution)
  → Dimension scoring (8 scored dimensions, 0–3 scale)
  → Index calculation (rigidity, integration, threat-prediction, discernment)
  → Loop-state classification (rule-based cascade)
  → Optional: revision-latency analysis (multi-paragraph trajectories)
```

### Eight Scored Dimensions

| # | Dimension              | Abbreviation | What It Measures                        |
|---|------------------------|--------------|------------------------------------------|
| 1 | Self-Reference Density | SR           | First-person or self-modeling language    |
| 2 | Identity Fixity        | IF           | Fixed, permanent, or global self-claims  |
| 3 | Prediction             | PR           | Expectation and anticipation language    |
| 4 | Threat Weighting       | TH           | Perceived danger, rejection, or failure  |
| 5 | Feedback Integration   | FI           | Incorporation of external input          |
| 6 | Narrative Flexibility  | NF           | Openness, ambiguity tolerance, revision  |
| 7 | Fragmentation          | FR           | Competing self-models, internal splits   |
| 8 | Updated Continuity     | UC           | Explicit identity revision with thread   |

### Measurement warning

The current v0.4.1-alpha software scores many dimensions by counting distinct matched regex patterns and capping at 3. The human rubric defines 0–3 semantically as absent, weak/implied, clear, and dominant/load-bearing. These are not yet operationally equivalent scales.

For the locked construct-to-machine specification and required corrections, see [`MEASUREMENT_SPEC.md`](MEASUREMENT_SPEC.md).

### Auxiliary Marker Categories

These categories influence scoring and classification but are not independently scored dimensions: bodily distress, sarcasm, rumination, boundary-setting, accountability, partial acceptance, context markers, weaponized evidence, ego-evidence ambiguity, third-person self-distance, feedback rejection, discernment, agency collapse, and unresolved resolution.

### Eight Loop States

| State                  | Description                                             |
|------------------------|---------------------------------------------------------|
| Flexible               | Adaptive processing without explicit identity revision  |
| Integrated             | Updated continuity with self-model revision             |
| Defensive              | External blame, dismissal, or feedback rejection        |
| Rigid                  | Fixed identity claims, fatalistic prediction            |
| Fragmented             | Competing self-models without resolution                |
| Overloaded             | Agency, meaning, or action collapses                    |
| Stable/Neutral         | No meaningful identity activity                         |
| Mixed / Review Needed  | Ambiguous, sarcastic, or insufficient for classification|

These are classifications of textual processing configurations, not labels for people.

---

## Expanded Theory Baseline

The theory baseline now formalizes identity as a continuity-constrained self-model that recursively incorporates new evidence.

A conceptual representation is:

```
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

```
continuity-engine/
├── continuity_engine.py          # v0.4.1 classifier and Revision Latency tools
├── THEORY.md                     # locked expanded Mid-Process Identity Loop theory
├── MEASUREMENT_SPEC.md           # construct-to-machine operationalization specification
├── QA_REPORT_2026-07-25.md       # full QA issue ledger
├── ROADMAP_V0_5.md               # validation-first v0.5 implementation roadmap
├── sample_texts.json             # 60-sample labeled pilot dataset
├── test_adversarial.json         # 20-sample adversarial/edge-case test set
├── run_verification.py           # Verification runner (supports --dataset, --no-labels)
├── randomize_rater_packet.py     # Seeded/blinded rater-packet generator
├── irr_calculator.py             # Inter-rater reliability calculator
├── methodology/
│   ├── irr_packet_v1_3.md        # Rater instructions (v1.3)
│   ├── narrative_analysis_rubric_v1.md
│   └── revision_latency_v0_2.md
├── tests/                        # Unit and regression tests
├── outputs/                      # Generated verification results, rater packets
└── docs/                         # Documentation site files (index.html, loop-diagram.png)
```

---

## Documentation Site Files

Static documentation lives in [`docs/`](docs/). It contains `index.html` and a `loop-diagram.png` illustrating the Mid-Process Identity Loop. These files can be served as a GitHub Pages site (Settings → Pages → branch `main`, folder `/docs`).

---

## Quick Start

```bash
# Run pilot verification (60 calibration samples)
python run_verification.py

# Run adversarial tests (20 edge cases)
python run_verification.py --dataset test_adversarial.json

# Exploration mode (classify without expected labels)
python run_verification.py --dataset your_data.json --no-labels

# Generate blinded rater packet
python randomize_rater_packet.py

# Run unit tests
python -m pytest tests/
```

### Using the Engine Directly

```python
from continuity_engine import analyze_text

result = analyze_text("I was frustrated, but I can see why the change was needed.")

print(result.loop_state)    # "Flexible"
print(result.confidence)    # "Medium"
print(result.explanation)   # "Adaptive flexibility without explicit identity revision."
print(result.scores)        # {"self_reference": 1, "identity_fixity": 0, ...}
```

### Multi-Paragraph Analysis

```python
from continuity_engine import analyze_document

doc = analyze_document("Paragraph one.\nParagraph two.\nParagraph three.")

print(doc["state_sequence"])
print(doc["latency_metrics"]["recovery_arc"])
```

The current Revision Latency implementation treats newline-separated paragraphs as analysis units. This is a practical proxy, not a validated definition of a narrative unit. The v0.5 roadmap includes correcting terminology and trajectory semantics.

---

## IRR Calculator

After raters return completed CSVs as `coder_1.csv`, `coder_2.csv`, and `coder_3.csv`:

```bash
python irr_calculator.py
```

Writes `outputs/irr_summary.json` and `outputs/disagreement_review.csv`.

### Required Coder CSV Columns

```
sample_id,SR,IF,PR,TH,FI,NF,FR,UC,primary_state,secondary_state,confidence,notes
```

The current IRR tooling is part of the research prototype. The QA report identifies required input-hardening work before formal validation, including strict state validation, range checks, duplicate-ID detection, and explicit missingness reporting.

---

## Validation Status

The current pilot dataset (60 samples) achieves 100% classification accuracy. This is an **internal consistency result**, not external validation. The samples were hand-authored for calibration and used during rule development.

The adversarial test set (20 samples) achieves 100% accuracy against documented expected outcomes. These are **regression tests** — they verify that known bugs stay fixed and known edge cases are handled. They are not external validation. Some expected labels were chosen to match current classifier behavior at documented boundary cases rather than to stress-test the theory independently.

**What is proven:** The rules are internally consistent. The code runs end-to-end without errors. The classifier correctly processes the samples it was designed to handle.

**What is not proven:** That the classifier generalizes to unseen text. That human raters would agree with the labels. That the eight dimensions are valid constructs. That the tool works on real-world data.

**Next required sequence:** Human construct reliability → construct refinement → frozen human-coded held-out set → engine evaluation → ablation → cross-domain testing.

For planned validation work, see [`RESEARCH_AGENDA.md`](RESEARCH_AGENDA.md) and [`ROADMAP_V0_5.md`](ROADMAP_V0_5.md).

A held-out sample template is included for future validation design, but it does not contain validation data.

---

## Limitations

| Limitation                | Explanation                                                   |
|---------------------------|---------------------------------------------------------------|
| Rule-based                | Cannot infer deep context, intent, or meaning reliably        |
| English-only              | Markers are US-English dominant                               |
| Synthetic pilot dataset   | Does not demonstrate generalization                           |
| Sarcasm weakness          | Only surface sarcasm patterns detected                        |
| Negation weakness         | Limited negation handling; context-dependent                  |
| Speaker attribution       | Quoted speech and multi-speaker text remain high-risk cases   |
| Measurement alignment     | Machine score counts do not yet fully match human semantic anchors |
| Short-text optimized      | Designed for 1–5 sentence samples; longer text less tested    |
| Paragraph trajectory proxy| Paragraphs are formatting units, not validated narrative units |
| Not diagnostic            | Labels describe text patterns, not people                     |
| Unpublished theory        | Mid-Process Identity Loop is an original, unvalidated framework |

For detailed edge cases, see [`KNOWN_FAILURE_MODES.md`](KNOWN_FAILURE_MODES.md) and the dated QA report.

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
- Using labels ("Defensive," "Rigid," "Overloaded") to characterize individuals
- Surveillance or coercive monitoring of writing
- Clinical diagnosis or treatment planning

### Safer Label Language

For any public-facing or user-facing application, consider mapping internal labels:

| Internal Label | Suggested Public Label |
|----------------|----------------------|
| Defensive      | Protective Pattern   |
| Rigid          | Fixed Pattern        |
| Fragmented     | Split Pattern        |
| Overloaded     | Overwhelm Pattern    |
| Flexible       | Adaptive Pattern     |
| Integrated     | Integrated Pattern   |

---

## Citation

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

- Real-world text samples (anonymized, with consent)
- Adversarial test cases that expose failure modes
- Translations or adaptations of marker sets for other languages
- Independent rater data for IRR validation
- Bug reports and edge-case documentation

Please do not submit changes that expand validation claims beyond the evidence currently available.

---

## Requirements

Python 3.8+. No external runtime dependencies. Standard library only.
