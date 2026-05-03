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

---

## File Structure

```
continuity-engine/
├── continuity_engine.py          # v0.4.1 classifier and Revision Latency tools
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

---

## Validation Status

The current pilot dataset (60 samples) achieves 100% classification accuracy. This is an **internal consistency result**, not external validation. The samples were hand-authored for calibration and used during rule development.

The adversarial test set (20 samples) achieves 100% accuracy against documented expected outcomes. These are **regression tests** — they verify that known bugs stay fixed and known edge cases are handled. They are not external validation. Some expected labels were chosen to match current classifier behavior at documented boundary cases rather than to stress-test the theory independently.

**What is proven:** The rules are internally consistent. The code runs end-to-end without errors. The classifier correctly processes the samples it was designed to handle.

**What is not proven:** That the classifier generalizes to unseen text. That human raters would agree with the labels. That the eight dimensions are valid constructs. That the tool works on real-world data.

**Next required steps:** Inter-rater reliability study with 3+ independent raters. Held-out evaluation on text not used during development. Cross-domain testing.

For planned validation work, see [Research Agenda](RESEARCH_AGENDA.md).

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
| Short-text optimized      | Designed for 1–5 sentence samples; longer text less tested    |
| Not diagnostic            | Labels describe text patterns, not people                     |
| Unpublished theory        | Mid-Process Identity Loop is an original, unvalidated framework |

For detailed edge cases, see [Known Failure Modes](KNOWN_FAILURE_MODES.md).

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

---

## Requirements

Python 3.8+. No external dependencies. Standard library only.
