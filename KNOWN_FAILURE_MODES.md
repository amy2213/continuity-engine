# Known Failure Modes

Continuity Engine is a rule-based research prototype. The patterns below are known or likely sources of misclassification.

## High-Risk Misclassification Areas

- Quoted speech where the writer reports another person's words
- Negated statements such as "I am not saying..."
- Sarcasm without explicit sarcasm markers
- Long passages containing multiple loop states
- Fictional, poetic, or highly metaphorical text
- Texts outside US-English idiom
- Multi-speaker dialogue or transcript excerpts
- Coercive or surveillance contexts, which are prohibited uses

## Why These Matter

The classifier detects surface language patterns. It does not reliably infer deep context, intent, culture, tone, or speaker boundaries.

## Current Handling

Known adversarial and regression cases live in `test_adversarial.json`. These tests verify that previously identified bugs remain fixed. They do not prove external validity.

## Required Future Work

- Add held-out samples not used during rule development
- Add human-coded disagreement examples
- Expand negation and quotation tests
- Track failures publicly instead of hiding them
