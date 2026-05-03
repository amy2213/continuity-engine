# Research Agenda

Continuity Engine currently demonstrates internal consistency and regression stability. It does not yet demonstrate external validity.

## Current Status

- 60-sample synthetic pilot dataset
- 20-sample adversarial regression dataset
- Unit tests for markers, hinges, classification, randomization, IRR calculation, and adversarial cases
- Human validation pending

## Next Empirical Questions

1. Can independent human raters apply the eight-dimension rubric consistently?
2. Do human-coded primary loop states agree above chance?
3. Which dimensions show the highest and lowest agreement?
4. Does the classifier agree with human raters on held-out text?
5. Which states are most frequently confused?
6. Does the framework generalize across writing genres?
7. Do revision-latency patterns show meaningful trajectory differences in multi-paragraph text?

## Minimum Validation Study

- Recruit at least 3 independent raters
- Use 30-60 samples not used to build the rules
- Run one calibration round
- Run one blind coding round
- Calculate Fleiss' kappa for primary state
- Calculate pairwise Cohen's kappa
- Calculate dimension agreement within ±1
- Publish disagreement patterns

## Minimum Reporting Standard

Report:
- dataset source
- anonymization and consent status
- number of raters
- calibration procedure
- primary-state agreement
- dimension agreement
- confusion matrix
- known failure modes
- examples of disagreement

## Do Not Claim Yet

Do not claim:
- external validation
- psychological diagnosis
- clinical usefulness
- personality assessment
- real-world predictive power
- generalization across populations
