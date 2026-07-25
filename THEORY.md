# Mid-Process Identity Loop

## Locked theory baseline

**Status:** Theory baseline for Continuity Engine v0.4.1-alpha and successor research versions.

**Core thesis:** Identity is continuity under revision.

Continuity Engine treats identity-relevant language as evidence of a local processing configuration, not as a fixed description of a person. The framework is not diagnostic and does not claim access to hidden mental states.

## Core model

Identity is modeled as a continuously updated self-model that predicts, interprets, and incorporates experience while preserving enough continuity for the system to remain recognizably the same self across time.

Let the self-model at time t be M_t, incoming evidence be E_t, and contextual conditions be C_t.

M_(t+1) = U(M_t, E_t, C_t)

The revision process can be represented conceptually as balancing two pressures:

1. improving correspondence with new evidence, and
2. preserving continuity with the prior self-model.

A useful theoretical representation is:

M_(t+1) = argmin_M [PredictionError(M, E_t) + lambda * ContinuityLoss(M, M_t)]

This equation is conceptual, not empirically estimated in the current system.

## Continuity-revision tradeoff

The framework proposes two broad failure modes.

### Excessive continuity

The current self-model is preserved despite contradictory evidence.

Likely configurations include:
- Rigid
- Defensive
- prediction lock
- evidence discounting

### Excessive revision without successful continuity preservation

Incoming evidence destabilizes the self-model faster than it can be reconciled.

Likely configurations include:
- Fragmented
- Overloaded
- unresolved model competition
- temporary loss of coherent agency

Adaptive identity processing occurs between these extremes.

## State definitions as processing configurations

### Stable/Neutral

No meaningful identity-relevant revision pressure is visible in the text.

### Flexible

New evidence is accommodated without structural self-model revision.

The current model remains substantially intact while interpretation, strategy, or perspective changes.

### Integrated

The self-model is structurally revised while continuity is preserved.

The writer is not simply changing an opinion. The text shows an updated self-understanding while retaining a recognizable thread between prior and revised self-models.

### Defensive

Incoming evidence is rejected, discounted, externalized, or reinterpreted primarily in a way that protects the current self-model from revision.

Defensive is a processing configuration, not a moral label.

### Rigid

The prior self-model dominates interpretation so strongly that new evidence has little capacity to update it.

Rigid differs from Defensive. Defensive processing rejects or attacks evidence. Rigid processing preloads what evidence is allowed to mean.

### Fragmented

Two or more incompatible self-models remain simultaneously active without a successful mechanism for adjudication or integration.

Fragmentation is not ordinary contradiction. Humans can hold competing thoughts without fragmentation. The defining feature is unresolved model competition.

### Overloaded

Revision demand exceeds available processing capacity. The system temporarily loses sufficient capacity for coherent reconciliation, planning, meaning-making, or action.

### Mixed / Review Needed

Available textual evidence is ambiguous, conflicting, sarcastic, attribution-sensitive, too sparse, or otherwise insufficient for a defensible single-state classification.

## Expanded theoretical constructs

These are now part of the theory baseline but are not yet required machine-scored dimensions.

### Revision Pressure

The pressure placed on the current self-model by incoming evidence.

Conceptually:

RevisionPressure = EvidenceConflict * EvidenceWeight

### Revision Capacity

The system's demonstrated capacity to hold complexity, incorporate feedback, preserve agency, and update interpretation.

Candidate contributors include:
- narrative flexibility
- feedback integration
- ambiguity tolerance
- contextual discernment
- preserved agency

### Evidence Weighting

The epistemic influence given to incoming information.

Threat, source credibility, context, prior prediction, and self-model protection may alter the effective weight of evidence.

### Revision Depth

Not all revisions are identity revisions.

A useful hierarchy is:

0. factual revision
1. interpretation revision
2. strategy revision
3. self-model revision
4. identity-architecture revision

### Revision Magnitude

How much the self-model changes between states.

### Continuity Preservation

How strongly the revised self-model remains connected to the prior self-model.

Integration is expected to involve both meaningful revision and preserved continuity.

## Updated Continuity as a possible outcome variable

The current eight-dimension architecture treats Updated Continuity as a peer dimension. The expanded theory introduces a competing hypothesis:

> Updated Continuity may be better modeled as an outcome produced by the interaction of revision pressure, evidence weighting, fixity, revision capacity, and continuity preservation.

This is not yet locked as the final measurement architecture. It is a primary empirical question for the next research phase.

## Transition-first hypothesis

The current engine classifies text states. The theory predicts that transitions may ultimately be more informative than isolated states.

The preferred future unit of analysis is therefore not only S_t, but:

S_t -> S_(t+1)

Examples include:
- Rigid -> Flexible
- Defensive -> Integrated
- Fragmented -> Flexible
- Flexible -> Defensive
- Integrated -> Fragmented

A process theory should be evaluated on trajectories, not only snapshots.

## Falsifiable predictions

1. Higher Identity Fixity should predict longer revision latency after contradictory evidence.
2. Higher Narrative Flexibility should predict lower persistence of Rigid and Defensive configurations.
3. High Revision Pressure combined with low Revision Capacity should increase Fragmented or Overloaded trajectories.
4. Feedback Integration alone should not be sufficient for Integrated classification without self-model revision and continuity preservation.
5. Integrated passages should contain more explicit temporal self-linking than Flexible passages.
6. Defensive and Rigid states should differ in attribution structure: Defensive should externalize conflict more often, while Rigid should generalize conflict into stable expectations more often.
7. Integrated processing should reduce subsequent prediction extremity more than Flexible processing, if measured longitudinally.

## Ethics boundary

All states belong to the text-processing episode, not the person.

The framework must not be used to rank, diagnose, punish, profile, or characterize individuals.

## Research rule

The theory may be revised by evidence.

The software must not silently redefine the theory simply because a regex implementation behaves a certain way.
