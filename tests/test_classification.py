"""Tests for loop-state classification. Each state has positive and negative cases."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from continuity_engine import analyze_text, CANONICAL_STATES


class TestInputValidation:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            analyze_text("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            analyze_text("   \n  ")

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            analyze_text(42)

    def test_none_raises(self):
        with pytest.raises(TypeError):
            analyze_text(None)


class TestFlexible:
    def test_basic_flexible(self):
        r = analyze_text("I was frustrated, but I can see why the change was needed. I adjusted.")
        assert r.loop_state == "Flexible"

    def test_boundary_with_accountability(self):
        r = analyze_text("I do not accept the way he spoke to me. Calling me lazy was not feedback, and I can take responsibility for missing the deadline without accepting disrespect.")
        assert r.loop_state == "Flexible"

    def test_flexible_should_not_be_integrated(self):
        """Flexible text without explicit identity revision should not be Integrated."""
        r = analyze_text("I disagree with their conclusion, but I do agree that the chart labels could be clearer. I can fix that part.")
        assert r.loop_state == "Flexible"
        assert r.loop_state != "Integrated"


class TestIntegrated:
    def test_basic_integrated(self):
        r = analyze_text("I used to believe that failure meant I was not capable. Now I can see it as information. It still hurts, but it no longer defines me.")
        assert r.loop_state == "Integrated"

    def test_revised_self(self):
        r = analyze_text("I am not the same person I was before this, but I can see the thread. I did not lose myself. I revised myself.")
        assert r.loop_state == "Integrated"

    def test_minimal_integration_marker_insufficient(self):
        """'I can see the thread' alone is not enough for Integrated."""
        r = analyze_text("I can see the thread.")
        assert r.loop_state != "Integrated"


class TestDefensive:
    def test_basic_defensive(self):
        r = analyze_text("They only criticized the project because they do not understand. I know the work was good.")
        assert r.loop_state == "Defensive"

    def test_weaponized_evidence(self):
        r = analyze_text("The data proves they are incompetent, and everyone who disagrees is either lying or too stupid.")
        assert r.loop_state == "Defensive"

    def test_defensive_not_flexible(self):
        r = analyze_text("I do not care how they interpreted it. I know what I meant, and that should be enough.")
        assert r.loop_state == "Defensive"


class TestRigid:
    def test_basic_rigid(self):
        r = analyze_text("This always happens to me. No matter what I do, people overlook my work. I am just the kind of person no one takes seriously.")
        assert r.loop_state == "Rigid"

    def test_third_person_rigid(self):
        r = analyze_text("Someone like her learns early not to expect much. She keeps showing up, but she already knows the room has made its decision before she walks in.")
        assert r.loop_state == "Rigid"


class TestFragmented:
    def test_basic_fragmented(self):
        r = analyze_text("I know I am safe, but my body does not believe it. I want to calm down, but part of me is still waiting for something bad to happen.")
        assert r.loop_state == "Fragmented"

    def test_trust_split(self):
        r = analyze_text("I trust her, but I also know she will eventually leave. I keep testing whether she means what she says.")
        assert r.loop_state == "Fragmented"


class TestOverloaded:
    def test_basic_overloaded(self):
        r = analyze_text("Everything is falling apart. I cannot think clearly, and I do not know what I am supposed to do next. One more thing will break me.")
        assert r.loop_state == "Overloaded"

    def test_agency_collapse(self):
        r = analyze_text("It is too much. I cannot explain it, fix it, or organize it. I feel like I am disappearing inside the noise.")
        assert r.loop_state == "Overloaded"


class TestStableNeutral:
    def test_basic_neutral(self):
        r = analyze_text("The meeting started at 9:00 a.m. The report was reviewed. Two errors were identified and the final version was submitted.")
        assert r.loop_state == "Stable/Neutral"

    def test_policy_language(self):
        r = analyze_text("The policy requires the form to be signed before reimbursement can be processed.")
        assert r.loop_state == "Stable/Neutral"

    def test_minimal_text(self):
        r = analyze_text("OK.")
        assert r.loop_state == "Stable/Neutral"


class TestMixedReviewNeeded:
    def test_ego_evidence_ambiguity(self):
        r = analyze_text("I know the data supports my conclusion, but I can also tell I am enjoying being right a little too much. That makes me question whether I am using the facts cleanly.")
        assert r.loop_state == "Mixed / Review Needed"

    def test_sarcasm_with_distress(self):
        r = analyze_text("I am fine. Completely fine. Nothing says stability like checking the same message forty times and pretending my jaw is not locked.")
        assert r.loop_state == "Mixed / Review Needed"


class TestSarcasmGrowthCollision:
    """Regression tests for the sarcasm-growth collision detector."""

    def test_growth_plus_dismissal(self):
        r = analyze_text("I learned so much from their brilliant feedback. I realized they are just wrong about everything.")
        assert r.loop_state == "Mixed / Review Needed"

    def test_growth_plus_sarcasm(self):
        r = analyze_text("Sure, I learned so much from their brilliant feedback.")
        assert r.loop_state == "Mixed / Review Needed"

    def test_growth_plus_high_fixity(self):
        r = analyze_text("I realized I am broken and nothing will ever change.")
        assert r.loop_state == "Mixed / Review Needed"

    def test_clean_growth_not_blocked(self):
        """Genuine growth without dismissal/sarcasm should still classify normally."""
        r = analyze_text("I realized part of it was useful and part of it did not apply. I can take what helps and leave the rest.")
        assert r.loop_state == "Flexible"


class TestDimensionOutput:
    def test_eight_dimensions_in_output(self):
        r = analyze_text("I was frustrated but I adjusted.")
        assert len(r.scores) == 8
        expected_keys = {"self_reference", "identity_fixity", "prediction", "threat",
                         "feedback_integration", "narrative_flexibility", "fragmentation", "integration"}
        assert set(r.scores.keys()) == expected_keys

    def test_no_bodily_distress_in_scores(self):
        """bodily_distress is auxiliary and should not appear in scored dimensions."""
        r = analyze_text("My chest is tight and I cannot breathe.")
        assert "bodily_distress" not in r.scores

    def test_all_states_are_canonical(self):
        r = analyze_text("Some text here.")
        assert r.loop_state in CANONICAL_STATES
