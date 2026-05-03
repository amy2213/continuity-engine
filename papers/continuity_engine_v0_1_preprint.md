# Continuity Engine v0.4.1-alpha: A Rule-Based Prototype for Operationalizing the Mid-Process Identity Loop

**Amy Laird**  
ORCID: [0009-0001-5479-0007](https://orcid.org/0009-0001-5479-0007)

Version: 0.1 preprint-style draft
Repository: [amy2213/continuity-engine](https://github.com/amy2213/continuity-engine)
Documentation: [amy2213.github.io/continuity-engine](https://amy2213.github.io/continuity-engine/)
Software version: 0.4.1-alpha
License: MIT

---

## Abstract

This paper introduces **Continuity Engine v0.4.1-alpha**, a rule-based narrative-analysis prototype that operationalizes the **Mid-Process Identity Loop**, an original conceptual framework for analyzing identity-continuity language. The framework proposes that identity-relevant narrative patterns can be examined through recursive interaction among self-reference, fixed identity claims, prediction, threat weighting, feedback integration, narrative flexibility, fragmentation, and updated continuity. The software prototype maps short text samples onto eight scored dimensions and eight loop-state labels through transparent marker detection, hinge classification, index calculation, and rule-based classification.

The current implementation demonstrates internal consistency and regression stability, not external validation. The repository reports 60/60 accuracy on a synthetic pilot calibration set and 20/20 accuracy on an adversarial regression set, while explicitly identifying both as internal and regression results rather than evidence of generalization. A separate known-weakness stress set documents current limitations in negation, quoted speech, fictional narration, multi-speaker transcripts, subtle sarcasm, and bodily-distress counterframing. The project also includes an inter-rater reliability packet, randomization tools, and an IRR calculator for future human validation.

Continuity Engine is not a diagnostic, therapeutic, or psychological assessment instrument. It classifies textual patterns, not people. This paper presents the model, implementation architecture, current testing status, known limitations, ethics boundaries, and the plan for future empirical work.

---

## 1. Introduction

Narrative self-understanding is often treated as though identity were a stable inner object that language merely describes. The **Mid-Process Identity Loop** starts from a different premise: identity is better understood as continuity under revision. In this view, identity is not a fixed essence but a recursive process in which perception, memory, prediction, bodily state, social feedback, and narrative interpretation continuously update the self-model.

Continuity Engine was built to test whether this conceptual model can be operationalized as a transparent coding system. Rather than attempting to infer hidden psychological states, the prototype analyzes explicit textual patterns: first-person self-reference, fixed self-claims, prediction language, threat framing, feedback integration, narrative flexibility, unresolved splits, and continuity-preserving revision.

The repository frames the project as a rule-based narrative analysis prototype, not a diagnostic or psychological assessment tool. It states that the framework is original and not externally validated, and that the software classifies text patterns rather than mental health, competence, or character.

This paper therefore has a narrow purpose: to document the theoretical model, software implementation, internal test status, known failure modes, and the plan for future human-rater studies.

---

## 2. Theoretical Background

The Mid-Process Identity Loop proposes that identity-relevant language can be analyzed as a dynamic process of self-model maintenance and revision. A person encounters an event, interprets it through perception and memory, compares it against an existing self-model, assigns meaning, experiences emotional or bodily response, and either updates or defends the current narrative structure.

The theory does not assume that every self-related statement reflects deep psychological truth. Instead, it treats language as evidence of local narrative organization. Some text shows flexible processing. Some shows defensive dismissal. Some shows fixed identity claims. Some shows fragmentation between competing self-models. Some shows explicit revision that preserves continuity.

This distinction matters because the software does not claim access to the writer's inner state. It detects patterns in written text.

**Core thesis:** Identity is continuity under revision.

---

## 3. The Mid-Process Identity Loop

### Figure 1. Mid-Process Identity Loop

```
External Event / Input
        │
        ▼
   Perception
        │
        ▼
Comparison with Current Self-Model
        │
        ▼
  Meaning Assignment
        │
        ▼
Emotional / Bodily State
        │
        ▼
 Narrative Response
        │
        ▼
Revision, Defense, Fragmentation, or Collapse
        │
        ▼
 Updated Self-Model
        │
        └───────────────────────────────┐
                                        │
        ┌───────────────────────────────┘
        │
        ▼
   (Next event enters revised loop)
```

**Figure 1 note.** The loop is recursive. Each update changes the interpretive conditions for the next event. The arrow returning from Updated Self-Model to the next cycle represents the continuity mechanism: the revised model becomes the baseline for subsequent processing.

---

## 4. Operationalization in Continuity Engine

Continuity Engine operationalizes the Mid-Process Identity Loop as a rule-based classifier. The processing pipeline proceeds through text input, marker detection, hinge classification, dimension scoring, index calculation, loop-state classification, and optional revision-latency analysis for multi-paragraph trajectories.

Here, "operationalizes" means converting the framework into an explicit, auditable coding prototype, not that the framework has been psychometrically validated.

### Figure 2. Continuity Engine Pipeline

```
Text Input
     │
     ▼
Regex Marker Detection
  (20+ marker categories)
     │
     ▼
Hinge Classification
  ├── but-clauses
  └── because-attribution
     │
     ▼
Eight-Dimension Scoring
  (0–3 scale per dimension)
     │
     ▼
Index Calculation
  ├── rigidity index
  ├── integration index
  ├── threat-prediction index
  └── discernment index
     │
     ▼
Rule-Based Cascade
     │
     ▼
Loop-State Output
  (one of eight canonical states)
```

**Figure 2 note.** The prototype is intentionally transparent. It uses explicit regex patterns and rule-based logic rather than a learned or black-box model. Every classification decision is traceable to specific markers, scores, and cascade rules.

---

## 5. Eight Scored Dimensions

The engine scores each text sample across eight dimensions on a 0–3 scale. These dimensions are coding categories for text patterns. They are not personality traits, psychological constructs, or diagnostic indicators.

| Dimension              | Abbr. | Core Question                                              | High-Score Signal                             |
| ---------------------- | :---: | ---------------------------------------------------------- | --------------------------------------------- |
| Self-Reference Density |  SR   | How much does the text refer to the self?                  | Repeated self-modeling language                |
| Identity Fixity        |  IF   | Does the text express fixed self-claims?                   | Permanent or global self-characterizations     |
| Prediction             |  PR   | Does the text anticipate or pre-load outcomes?             | Expectation and pre-loaded-outcome language    |
| Threat Weighting       |  TH   | Is meaning organized around danger, rejection, or failure? | Danger, rejection, or catastrophic framing     |
| Feedback Integration   |  FI   | Does the text incorporate external input?                  | Acknowledgment or use of outside perspective   |
| Narrative Flexibility  |  NF   | Does the text hold ambiguity or multiple perspectives?     | Tolerance for complexity or both-and framing   |
| Fragmentation          |  FR   | Are competing self-models active and unresolved?           | Unresolved split between body, thought, action |
| Updated Continuity     |  UC   | Does the text revise identity while preserving a thread?   | Explicit revision with maintained self-thread  |

### Figure 3. Eight-Dimension Matrix

```
SR  Self-Reference Density    →  self-model presence
IF  Identity Fixity           →  permanence / fixed claims
PR  Prediction                →  expected-outcome language
TH  Threat Weighting          →  danger / rejection framing
FI  Feedback Integration      →  use of external input
NF  Narrative Flexibility     →  ambiguity / multiple perspectives
FR  Fragmentation             →  unresolved internal split
UC  Updated Continuity        →  revision while preserving self-thread
```

**Figure 3 note.** The dimensions are text-level coding categories. They describe what the text does, not who the writer is.

### Behavioral Anchors

The inter-rater reliability packet (v1.3) expands these dimensions with behavioral anchors on the 0–3 scale, where 0 indicates absence of relevant markers, 1 indicates weak or implied presence, 2 indicates clear and noticeable presence, and 3 indicates the dimension is dominant and load-bearing in the text.

These anchors are intended to support future inter-rater reliability testing; they are not yet evidence that raters will agree.

### Auxiliary Marker Categories

Beyond the eight scored dimensions, the engine detects auxiliary marker categories that influence scoring and classification but are not independently scored. These include bodily distress, sarcasm, rumination, boundary-setting, accountability, partial acceptance, context markers, weaponized evidence, ego-evidence ambiguity, third-person self-distance, feedback rejection, discernment, agency collapse, and unresolved resolution.

---

## 6. Loop-State Classification Architecture

The classifier assigns one of eight canonical loop states through a rule-based cascade. The eight states are:

1. **Flexible** — Adaptive processing without explicit identity revision.
2. **Integrated** — Updated continuity with self-model revision.
3. **Defensive** — External blame, dismissal, or feedback rejection.
4. **Rigid** — Fixed identity claims or fatalistic prediction.
5. **Fragmented** — Competing self-models without resolution.
6. **Overloaded** — Agency, meaning, or action collapse.
7. **Stable/Neutral** — No meaningful identity-relevant activity.
8. **Mixed / Review Needed** — Ambiguous, sarcastic, or insufficient signals for confident classification.

### Cascade Logic

The cascade gives priority to ambiguity and collision cases before ordinary classification. Several architectural decisions reflect the theory's core distinctions:

**Ambiguity routing.** Growth language paired with dismissal, sarcasm, or high identity fixity routes to Mixed / Review Needed rather than Flexible or Integrated. This prevents false-positive classification of superficially positive text.

**Boundary handling.** Boundary-setting is handled separately from defensiveness. Boundary language combined with accountability routes to Flexible. Boundary language without accountability or sufficient context routes to Mixed / Review Needed.

**Overloaded conditions.** Overloaded classification requires agency collapse or high rumination combined with elevated threat-prediction conditions.

**Fragmented conditions.** Fragmented classification requires active unresolved self-model splits, not merely the co-presence of competing signals.

**Integrated conditions.** Integrated classification requires explicit updated-continuity markers or process-reflective revision language.

### Tie-Breaker Rules

The IRR packet provides human raters with tie-breaker rules for common confusion pairs: Flexible vs. Integrated, Defensive vs. Flexible, Fragmented vs. Integrated, Fragmented vs. Overloaded, and Rigid vs. Defensive. These rules are designed to improve coding consistency and to surface the classification boundaries that are most likely to produce disagreement.

---

## 7. Software Artifact and Repository Structure

The repository contains the following major components:

- **`continuity_engine.py`** — v0.4.1 classifier with marker detection, dimension scoring, index calculation, cascade classification, and revision-latency tools.
- **`sample_texts.json`** — 60-sample labeled pilot dataset used during rule development and calibration.
- **`test_adversarial.json`** — 20-sample adversarial and edge-case regression test set.
- **`test_known_weaknesses.json`** — 12-sample exploratory stress set, explicitly marked as not a validation dataset.
- **`run_verification.py`** — Verification runner supporting dataset selection and label-free exploration mode.
- **`randomize_rater_packet.py`** — Seeded, blinded rater-packet generator with master key.
- **`irr_calculator.py`** — Inter-rater reliability calculator supporting primary-state agreement, pairwise agreement, Cohen's kappa, Fleiss' kappa, dimension agreement, coder severity reports, and disagreement summaries.
- **`methodology/`** — Rater instructions (IRR packet v1.3), narrative analysis rubric, and revision-latency documentation.
- **`tests/`** — Unit and regression tests for markers, hinges, classification, adversarial cases, known-weakness documentation, randomization, and IRR calculation.
- **`outputs/`** — Generated verification results, exploratory known-weakness results, and rater packet templates.
- **`docs/`** — GitHub Pages documentation site.
- **`CITATION.cff`** — Citation metadata including title, author, version, date, license, repository URL, documentation URL, abstract, and keywords.
- **`KNOWN_FAILURE_MODES.md`** — Documented high-risk misclassification areas.
- **`RESEARCH_AGENDA.md`** — Planned empirical questions, minimum validation study design, and explicit not-yet-claimed list.
- **`heldout_samples_template.json`** — Template for future held-out samples, with instructions not to tune rules against it and to have human raters assign expected labels before classifier comparison.

The GitHub Actions CI workflow runs tests on Python 3.8, 3.11, and 3.12 and installs dependencies before executing `pytest`.

The runtime engine uses the Python standard library only. Development and CI testing use pytest.

---

## 8. Internal Consistency and Regression Testing

The current repository reports 60/60 accuracy on the pilot dataset and 20/20 accuracy on the adversarial regression set.

**What these numbers represent.** The pilot result is an **internal consistency** check. The 60 samples were hand-authored for calibration and used during rule development. They confirm that the implemented rules produce the intended classifications on the samples they were designed to handle.

The adversarial result is a **regression stability** check. The 20 samples verify that previously identified bugs remain fixed and that known edge cases continue to be handled as documented.

**What these numbers do not represent.** Neither result constitutes external validation. The numbers do not demonstrate generalization to unseen text, agreement with human raters, construct validity of the eight dimensions, or real-world performance.

### Figure 4. Validation Status Ladder

```
CURRENT STATUS
  ✓  Internal consistency on synthetic pilot samples (60/60)
  ✓  Regression stability on adversarial edge cases (20/20)
  ✓  Known weaknesses documented (12 exploratory stress cases)
  ✓  CI test workflow passing (Python 3.8, 3.11, 3.12)

NEXT STEPS
  →  Human inter-rater reliability study
  →  Held-out text evaluation
  →  Cross-domain testing
  →  Disagreement analysis

NOT YET CLAIMED
  ✗  External validation
  ✗  Construct validity
  ✗  Predictive validity
  ✗  Clinical usefulness
  ✗  Population generalization
```

**Figure 4 note.** The project is currently a test bench for a theory, not evidence that the theory is validated.

---

## 9. Known Failure Modes

The repository documents known failure modes explicitly. High-risk misclassification areas include:

- **Quoted speech** — The classifier may attribute another speaker's words to the narrator.
- **Negated statements** — Phrases such as "I am not saying..." may be partially pattern-matched as affirmative.
- **Sarcasm without markers** — Sarcasm that lacks explicit textual cues is not reliably detected.
- **Multi-state passages** — Long text containing signals for multiple loop states may receive a single label that does not capture the full trajectory.
- **Fictional or poetic text** — First-person fictional narration is not reliably distinguished from self-report.
- **Non-US-English idiom** — Marker patterns are US-English dominant.
- **Multi-speaker dialogue** — Transcript-style text with multiple speakers complicates attribution.
- **Coercive or surveillance contexts** — These are prohibited uses, but the classifier cannot detect or refuse them automatically.

These failure modes matter because the classifier detects surface language patterns. It does not reliably infer deep context, intent, culture, tone, or speaker boundaries.

### Known-Weakness Exploratory Set

A separate 12-sample stress set documents the classifier's current behavior on deliberately difficult cases. It is explicitly marked `exploratory_not_validation` with `accuracy_is_not_asserted: true`. The set currently matches 6 of 12 desired labels. Because the set was designed to expose difficult boundary cases rather than estimate performance, the 6/12 match count should be read as a failure-map summary, not as an accuracy metric.

Notable mismatches include a negated contempt phrase classified as Defensive instead of Flexible, quoted fixity from another speaker classified as Mixed / Review Needed instead of Integrated, and bodily distress with cognitive counterframing classified as Flexible instead of Fragmented.

These failures are not defects in the paper's argument. They are evidence that the project documents its limitations rather than concealing them.

---

## 10. Ethics and Use Boundaries

Continuity Engine must not be used to evaluate, rank, punish, diagnose, or profile individuals.

The tool classifies language patterns in text. It does not assess a writer's mental health, character, competence, or worth. Classifications describe textual patterns, not people.

### Acceptable Use

- The writer's own text, for personal reflection.
- Anonymized text, for research purposes with appropriate safeguards.
- Consented text, with documented informed consent.
- Research coding, as a pre-classification or hypothesis-generation tool.

### Unacceptable Use

- Evaluating employees, students, or patients based on loop-state classifications.
- Using labels to characterize individuals.
- Surveillance or coercive monitoring of writing.
- Clinical use, diagnosis, or treatment planning.

### Safer Label Language

For any public-facing or user-facing application, internal labels should be softened to reduce potential stigma:

| Internal Label | Suggested Public Label |
|----------------|------------------------|
| Defensive      | Protective Pattern     |
| Rigid          | Fixed Pattern          |
| Fragmented     | Split Pattern          |
| Overloaded     | Overwhelm Pattern      |
| Flexible       | Adaptive Pattern       |
| Integrated     | Integrated Pattern     |

---

## 11. Human Validation Plan

The repository includes tools for future human validation.

### Rater Materials

The IRR packet (v1.3) provides raters with scoring instructions, behavioral anchors for all eight dimensions, loop-state definitions, tie-breaker rules for common confusion pairs, confidence-level guidance, worked examples, and a calibration protocol. The packet instructs raters to code the text, not the subtext, and to treat scores as coding judgments rather than moral evaluations.

### Blinding and Randomization

The rater-packet generator creates blinded sample IDs using a seeded shuffle and produces a master key for de-identification after coding.

### Agreement Statistics

The IRR calculator computes primary-state agreement, pairwise agreement, Cohen's kappa (for two-coder pairs), Fleiss' kappa (for three or more coders), dimension agreement within ±1, coder severity reports, and disagreement summaries.

### Minimum Study Design

The research agenda specifies the following minimum next validation study:

- Recruit at least three independent raters.
- Use 30–60 samples not used during rule development.
- Run a calibration round followed by a blind coding round.
- Calculate Fleiss' kappa for primary state.
- Calculate pairwise Cohen's kappa.
- Calculate dimension agreement within ±1.
- Publish disagreement patterns.

The held-out sample template reinforces that future held-out samples must not be used for rule tuning and that expected labels should be assigned by human raters before classifier comparison.

---

## 12. Research Agenda

The current project supports several empirical questions, as documented in the repository's research agenda:

1. Can independent human raters apply the eight-dimension rubric consistently?
2. Do human-coded primary loop states agree above chance?
3. Which dimensions show the highest and lowest inter-rater agreement?
4. Does the classifier agree with human raters on held-out text?
5. Which loop states are most frequently confused?
6. Does the framework generalize across writing genres?
7. Do revision-latency patterns show meaningful trajectory differences in multi-paragraph text?

These are open empirical questions. They are not rhetorical predictions of success.

---

## 13. Limitations

Continuity Engine has several important limitations.

**Rule-based architecture.** The classifier cannot reliably infer deep context, speaker intent, cultural background, tone, or complex pragmatics. It operates on surface-level text patterns.

**Synthetic pilot dataset.** The 60 pilot samples were hand-authored during development. They demonstrate internal consistency but cannot establish generalization to unseen or real-world text.

**Adversarial dataset as regression test.** The 20 adversarial samples verify known bug fixes and documented edge cases. They do not constitute an independent validity test. Some expected labels were chosen to match current classifier behavior at documented boundary cases.

**Unresolved known weaknesses.** The 12-sample stress set demonstrates that negation, quotation, fiction, transcript structure, subtle sarcasm, and bodily counterframing are not fully handled. Six of twelve cases do not match desired labels.

**Original and unpublished framework.** The Mid-Process Identity Loop is an original framework by the author. It is not an established or externally validated theory. No peer-reviewed literature currently supports or critiques it.

**English-only.** Marker patterns are US-English dominant. Performance on other English varieties or other languages is untested.

**Short-text optimization.** The engine is designed for 1–5 sentence samples. Behavior on longer text is less tested.

These limitations do not invalidate the prototype. They define the boundary between a credible test bench and an overclaimed instrument.

---

## 14. Not Yet Claimed

This project does not yet claim:

- External validation.
- Construct validity.
- Diagnostic authority.
- Clinical usefulness.
- Personality assessment.
- Predictive validity.
- Population generalization.
- Real-world performance.
- Reliable classification across domains.
- Measurement of people.

The project currently claims only that the rule system is internally consistent on its designed pilot set, stable against its adversarial regression suite, transparent enough for critique, and structured for future human validation.

---

## 15. Conclusion

Continuity Engine v0.4.1-alpha demonstrates that the Mid-Process Identity Loop can be operationalized as a transparent rule-based narrative coding prototype. The current implementation maps short text samples across eight scored dimensions and eight loop states, supports revision-latency analysis, provides pilot and adversarial regression checks, documents known failure modes, and includes tools for human inter-rater validation.

The project's value at this stage is not that it confirms the theory. It does not. Its value is that it converts an abstract conceptual model into a testable software artifact with explicit assumptions, reproducible rules, documented failure modes, and a clear pathway toward empirical evaluation.

The next necessary step is not further rule tuning. It is human validation: independent raters, blinded samples, agreement statistics, disagreement analysis, and held-out comparison. Only then can the framework begin moving from prototype toward an empirically evaluated coding instrument.

Until then, Continuity Engine should be understood as a research prototype for textual pattern classification, not as a validated psychological tool.

---

## Repository and Software Citation

Amy Laird. **Continuity Engine: A Rule-Based Narrative Analysis Framework.** Version 0.4.1-alpha. 2026. MIT License.

- Repository: https://github.com/amy2213/continuity-engine
- Documentation: https://amy2213.github.io/continuity-engine/
- Citation metadata: `CITATION.cff`

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

## Overclaim Audit

The following risk terms were audited across this paper. Each use is documented below.

| Risk Term             | Occurrences | Context of Use                                                                 |
|-----------------------|:-----------:|--------------------------------------------------------------------------------|
| validated             |      ✓      | Used only in negated or bounded form: "not externally validated," "not validated" |
| proven                |      —      | Not used                                                                        |
| diagnostic            |      ✓      | Used only in negated safety language: "not a diagnostic ... instrument"          |
| diagnosis             |      ✓      | Used only in prohibited-use context: "Clinical use, diagnosis, or treatment"    |
| detects identity      |      —      | Not used                                                                        |
| measures mental health|      —      | Not used                                                                        |
| predicts              |      —      | Not used as a capability claim                                                  |
| predictive            |      ✓      | Used only in "not yet claimed" list: "Predictive validity"                      |
| generalizes           |      ✓      | Used only in bounded/negative form: "cannot establish generalization"           |
| clinical              |      ✓      | Used only in prohibited or not-yet-claimed contexts                             |
| personality           |      ✓      | Used only in not-yet-claimed list: "Personality assessment"                     |
| assessment            |      ✓      | Used only in negated safety language: "not a psychological assessment instrument"|

**Audit result.** No unbounded capability claims were found. All flagged terms appear in negated, bounded, or explicitly not-yet-claimed contexts only.
