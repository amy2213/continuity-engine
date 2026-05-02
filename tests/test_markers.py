"""Tests for marker detection across all categories."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from continuity_engine import find_markers, marker_count


class TestFixityMarkers:
    def test_i_always_fires(self):
        m = find_markers("I always mess things up.")
        assert marker_count(m, "fixity") >= 1

    def test_i_am_broken_fires(self):
        m = find_markers("I am broken and nothing will fix me.")
        assert marker_count(m, "fixity") >= 1

    def test_nothing_will_ever_change_fires(self):
        m = find_markers("Nothing will ever change.")
        assert marker_count(m, "fixity") >= 1

    def test_policy_always_does_not_inflate(self):
        """Policy language should fire fixity weakly but not dominate."""
        m = find_markers("The team always reviews documentation.")
        # "always" alone should not fire identity-fixity patterns
        # that require first-person framing
        assert marker_count(m, "fixity") <= 1


class TestFeedbackIntegrationMarkers:
    def test_i_realized_fires(self):
        m = find_markers("I realized I was wrong about that.")
        assert marker_count(m, "feedback_integration") >= 1

    def test_i_learned_fires(self):
        m = find_markers("I learned a lot from the experience.")
        assert marker_count(m, "feedback_integration") >= 1

    def test_no_growth_in_neutral(self):
        m = find_markers("The meeting started at 9 a.m.")
        assert marker_count(m, "feedback_integration") == 0


class TestSarcasmMarkers:
    def test_sure_comma_fires(self):
        m = find_markers("Sure, that went well.")
        assert marker_count(m, "sarcasm") >= 1

    def test_completely_fine_fires(self):
        m = find_markers("I am completely fine.")
        assert marker_count(m, "sarcasm") >= 1

    def test_not_sure_does_not_fire(self):
        """Regression test: 'I am not sure' must not trigger sarcasm."""
        m = find_markers("I am not sure.")
        assert marker_count(m, "sarcasm") == 0

    def test_not_sure_whether_does_not_fire(self):
        m = find_markers("I am not sure whether to trust this.")
        assert marker_count(m, "sarcasm") == 0


class TestFeedbackRejectionMarkers:
    def test_they_are_just_wrong_fires(self):
        m = find_markers("They are just wrong about everything.")
        assert marker_count(m, "feedback_rejection") >= 1

    def test_neutral_does_not_fire(self):
        m = find_markers("The report was submitted on time.")
        assert marker_count(m, "feedback_rejection") == 0


class TestAgencyCollapseMarkers:
    def test_cannot_think_fires(self):
        m = find_markers("I cannot think clearly.")
        assert marker_count(m, "agency_collapse") >= 1

    def test_nothing_makes_sense_fires(self):
        m = find_markers("Nothing makes sense anymore.")
        assert marker_count(m, "agency_collapse") >= 1


class TestBodilyDistressMarkers:
    def test_tight_chest_fires(self):
        m = find_markers("My chest is tight and I cannot breathe.")
        assert marker_count(m, "bodily_distress") >= 1

    def test_neutral_does_not_fire(self):
        m = find_markers("The schedule was revised.")
        assert marker_count(m, "bodily_distress") == 0


class TestWeaponizedEvidenceMarkers:
    def test_data_proves_incompetent_fires(self):
        m = find_markers("The data proves they are incompetent.")
        assert marker_count(m, "weaponized_evidence") >= 1

    def test_clean_data_reference_does_not_fire(self):
        m = find_markers("The data supports the conclusion.")
        assert marker_count(m, "weaponized_evidence") == 0


class TestThirdPersonDistanceMarkers:
    def test_someone_like_her_fires(self):
        m = find_markers("Someone like her does not ask for help.")
        assert marker_count(m, "third_person_self_distance") >= 1

    def test_first_person_does_not_fire(self):
        m = find_markers("I do not ask for help.")
        assert marker_count(m, "third_person_self_distance") == 0
