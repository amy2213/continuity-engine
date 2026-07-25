# Continuity Engine v0.5 Research and Implementation Roadmap

## Objective

Move Continuity Engine from a coherent rule-based prototype toward a defensible measurement instrument without erasing the v0.4.1-alpha baseline.

## Governing rule

Do not optimize the engine against every known example until it reproduces expected labels perfectly. Preserve independent challenge and held-out data.

# Phase 0: Baseline freeze

**Status:** Required before implementation changes.

- Preserve v0.4.1-alpha code behavior as the historical baseline.
- Preserve `sample_texts.json` as calibration/internal-consistency data.
- Preserve `test_adversarial.json` as regression data.
- Preserve the known-weakness corpus as a challenge set.
- Record theory and measurement changes separately from code changes.

Exit condition: baseline artifacts are identifiable and no future validation dataset has been used for rule tuning.

# Phase 1: Construct alignment

## 1.1 Build construct-to-feature specification

For every dimension, document:
- construct definition,
- human anchors,
- machine observables,
- scope rules,
- intensity rules,
- temporal interpretation,
- known ambiguity.

## 1.2 Correct Self-Reference Density

Replace distinct-marker counting as the main SR signal with occurrence-based density normalized by text length.

## 1.3 Separate semantic intensity from marker count

Develop interpretable features for:
- globality,
- permanence,
- repetition,
- structural centrality,
- unresolved status.

Exit condition: machine features can be explicitly mapped to human rubric anchors without claiming that simple marker diversity equals semantic dominance.

# Phase 2: Scope and attribution handling

## 2.1 Negation scope

Prevent content under explicit negation from automatically firing affirmative construct markers.

## 2.2 Quotation scope

Distinguish narrator statements from quoted speech.

## 2.3 Speaker attribution

Flag multi-speaker and transcript structures for special handling or review.

## 2.4 Prior-belief attribution

Allow old beliefs quoted during revision to be represented separately from current beliefs.

Exit condition: challenge cases for negation, quotations, and speaker attribution are materially improved without tuning away independent failures.

# Phase 3: State architecture formalization

## 3.1 State-precedence matrix

Document pairwise precedence and tie-break logic.

## 3.2 Rule clarity

Rename or reinterpret current confidence as `classification_clarity`.

## 3.3 Explanation trace

Ensure each output can report:
- decisive markers,
- decisive hinge logic,
- decisive score conditions,
- cascade rule used.

Exit condition: every classification is traceable to an explicit documented theoretical decision.

# Phase 4: Revision Latency correction

## 4.1 Rename adaptive metric

Use `latency_to_adaptive` for first Flexible or Integrated state.

## 4.2 Separate position from transitions

Report:
- first adaptive unit position,
- transitions elapsed after destabilization.

## 4.3 Recovery requires destabilization

Do not label general first-adaptive position as recovery latency when no destabilized starting condition exists.

## 4.4 Normalize trajectory score

Report raw and per-unit normalized trajectory scores.

## 4.5 Research narrative units

Paragraphs remain an implementation proxy until a narrative unit is empirically defined.

Exit condition: trajectory metrics have unambiguous names and comparable interpretations across text lengths.

# Phase 5: IRR hardening

## 5.1 Strict input validation

Reject:
- unknown primary states,
- unknown secondary states,
- noninteger dimension values,
- scores outside 0-3,
- duplicate sample IDs.

## 5.2 Missingness audit

Before IRR calculations, report:
- expected sample count,
- missing IDs by coder,
- extra IDs by coder,
- common IDs,
- excluded IDs.

## 5.3 Reliability statistics

Retain:
- percent agreement,
- Cohen's kappa,
- Fleiss' kappa,
- exact dimension agreement,
- within-one agreement.

Add or evaluate:
- weighted Cohen's kappa for ordinal dimensions,
- Krippendorff's alpha for ordinal ratings.

Exit condition: malformed coder data cannot silently improve reliability results.

# Phase 6: Human validation before classifier validation

## 6.1 Calibration

Use independent raters and the locked rubric.

## 6.2 Blind coding

Use unseen samples not authored to demonstrate existing engine states.

## 6.3 Disagreement analysis

Treat disagreement as construct information, not merely coder error.

## 6.4 Rubric revision

Revise the rubric if needed before creating a gold set.

Exit condition: human reliability is characterized with transparent disagreement patterns.

# Phase 7: Frozen held-out engine evaluation

Create a held-out corpus whose labels are assigned before the engine sees it.

Report:
- confusion matrix,
- macro F1,
- balanced accuracy,
- per-state precision,
- per-state recall,
- performance by text domain,
- performance by classification clarity.

Do not headline simple accuracy alone.

# Phase 8: Ablation and theory testing

Test whether each major architecture component contributes:
- hinge logic,
- auxiliary markers,
- discernment,
- state precedence,
- threat modifiers,
- scope preprocessing.

Evaluate expanded theory predictions involving:
- Revision Pressure,
- Revision Capacity,
- Continuity Preservation,
- Revision Depth,
- transition trajectories.

# Phase 9: Cross-domain testing

Evaluate separately across writing domains before making population or genre-general claims.

No clinical, employment, education, surveillance, or coercive use is permitted.

# v0.5 definition of done

v0.5 should not mean "more regexes."

A defensible v0.5 should mean:

1. clearer construct-to-machine mapping,
2. corrected density and trajectory semantics,
3. scope-aware negation/quotation handling,
4. hardened IRR tooling,
5. explicit state-precedence governance,
6. preservation of untouched held-out validation data,
7. no expansion of claims beyond available evidence.
