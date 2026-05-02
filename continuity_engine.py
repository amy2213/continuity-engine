"""
Continuity Engine v0.4.1
Rule-based prototype for the Mid-Process Identity Loop narrative classifier.

This is a research prototype. It analyzes language patterns only and is not a
clinical or diagnostic tool. Do not use this tool to evaluate, rank, diagnose,
or profile individuals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

CANONICAL_STATES = [
    "Flexible",
    "Integrated",
    "Defensive",
    "Rigid",
    "Fragmented",
    "Overloaded",
    "Stable/Neutral",
    "Mixed / Review Needed",
]

DIMENSIONS = [
    "self_reference",
    "identity_fixity",
    "prediction",
    "threat",
    "feedback_integration",
    "narrative_flexibility",
    "fragmentation",
    "integration",
]

# Auxiliary marker categories influence dimension scores and classification
# but are not independently scored dimensions in the IRR rubric.
AUXILIARY_CATEGORIES = [
    "bodily_distress",
    "sarcasm",
    "rumination",
    "boundary",
    "accountability",
    "partial_acceptance",
    "context_markers",
    "weaponized_evidence",
    "ego_evidence_ambiguity",
    "third_person_self_distance",
    "feedback_rejection",
    "discernment",
    "agency_collapse",
    "unresolved_resolution",
]

MARKERS: Dict[str, List[str]] = {
    "self_reference": [
        r"\bi\b", r"\bme\b", r"\bmy\b", r"\bmyself\b", r"\bwho i am\b", r"\bmy story\b",
        r"\bsomeone like me\b", r"\bpeople like me\b",
    ],
    "third_person_self_distance": [
        r"\bsomeone like her\b", r"\bsomeone like him\b", r"\bsomeone like them\b",
        r"\ba person like her\b", r"\ba person like him\b", r"\ba person like that\b",
        r"\bshe tells herself\b", r"\bshe already knows\b", r"\bhe already knows\b",
        r"\bshe keeps\b", r"\bhe keeps\b", r"\bbefore she walks in\b", r"\bbefore he walks in\b",
        r"\bold version of me\b",
    ],
    "fixity": [
        r"\bi always\b", r"\bi never\b", r"\balways happens\b", r"\bthis always happens\b",
        r"\bthat's just who i am\b", r"\bthat is just who i am\b", r"\bi can't change\b", r"\bi cannot change\b",
        r"\bi'm broken\b", r"\bi am broken\b", r"\bi ruin every\w*\b", r"\bi ruin everything\b",
        r"\bi'm not capable\b", r"\bi am not capable\b", r"\bnothing ever works out\b", r"\bnothing ever changes\b", r"\bnothing changes\b",
        r"\bno matter what i do\b", r"\bjust the kind of person\b", r"\bthe kind of person\b",
        r"\bpeople like me\b", r"\bdo not get picked\b", r"\bno one takes .* seriously\b", r"\bpeople overlook my work\b",
        r"\bdoes not really change\b", r"\bpattern stays the same\b", r"\bpattern never changes\b",
        r"\balways been bad\b", r"\bnever get .* right\b", r"\bno point pretending i can change\b",
        r"\bnothing will ever change\b", r"\bwill never change\b",
    ],
    "prediction": [
        r"\bi knew\b", r"\balready knew\b", r"\bthis would happen\b", r"\bthis always happens\b", r"\bnext time\b",
        r"\bthey will\b", r"\bwill eventually\b", r"\bnothing will work\b", r"\bi expected\b", r"\bi assumed\b",
        r"\bi was afraid\b", r"\bi could tell\b", r"\bit was obvious\b", r"\bgoing to\b", r"\babout to\b", r"\bshould know better\b",
        r"\bbefore it started\b", r"\bbefore .* walks in\b", r"\beventually leave\b", r"\balways ends\b",
    ],
    "threat": [
        r"\bunsafe\b", r"\bnot safe\b", r"\bdangerous\b", r"\battacked\b", r"\brejected\b", r"\brejection\b",
        r"\bhumiliated\b", r"\btrapped\b", r"\bbetrayed\b", r"\bexposed\b", r"\bin trouble\b",
        r"\bagainst me\b", r"\bfailing\b", r"\bi am failing\b", r"\bi'm done\b", r"\bit's over\b", r"\bit is over\b",
        r"\blose everything\b", r"\bnothing ever works out\b", r"\btrap\b", r"\bdisaster\b", r"\bbreak me\b",
        r"\bthey will leave\b", r"\bpeople leave\b", r"\bgoing to leave me\b", r"\beventually leave\b",
        r"\bleave me\b", r"\bbe left out\b", r"\bleft out\b", r"\babandoned\b",
        r"\bmake me look bad\b", r"\btrying to trap me\b", r"\btoo sensitive\b", r"\bstupid\b",
    ],
    "feedback_integration": [
        r"\bi realized\b", r"\bi learned\b", r"\bi can see now\b", r"\bnow i can see\b", r"\bnow i understand\b",
        r"\bi understand\b", r"\bi had to reconsider\b", r"\bi reconsidered\b", r"\bi was wrong\b", r"\bpart of it was useful\b",
        r"\bpart of that was useful\b", r"\bpart of the message\b", r"\bsome of the criticism was fair\b",
        r"\bsome of it was fair\b", r"\bi can use\b", r"\bi can fix\b", r"\bi can correct\b", r"\bi can take what helps\b",
        r"\btake what helps\b", r"\bhelped me clarify\b", r"\bquestions helped me clarify\b", r"\bi can see why\b", r"\bi also think\b", r"\bi can understand why\b", r"\bi can also see\b",
        r"\bi do agree\b", r"\bi agree\b", r"\bi need to own\b", r"\bi can take responsibility\b", r"\bi take responsibility\b",
    ],
    "feedback_rejection": [
        r"\bthey don't get it\b", r"\bthey do not get it\b", r"\bclearly do not get it\b",
        r"\bthat doesn't count\b", r"\bthat does not count\b", r"\bi don't care what they said\b",
        r"\bi do not care what they said\b", r"\bi do not care how they interpreted\b", r"\bthey're just wrong\b",
        r"\bthey are just wrong\b", r"\bthey are wrong\b", r"\bthat proves nothing\b", r"\bi already know\b",
        r"\bnothing .* changes that\b", r"\bfeedback was useless\b", r"\bopinion matters\b", r"\btheir opinion matters\b",
        r"\bthat is ridiculous\b", r"\bshould be enough\b", r"\bthey are missing the point\b", r"\bthey .* missing the point\b",
    ],
    "flexibility": [
        r"\bpart of me\b", r"\banother part\b", r"\bat the same time\b", r"\bi used to think\b", r"\bbut now\b",
        r"\bboth things are true\b", r"\bboth things can be true\b", r"\bi can understand why\b", r"\bi can see why\b",
        r"\bit was more complicated\b", r"\bi'm still figuring\b", r"\bi may have misread\b", r"\bask a clearer question\b", r"\bbefore deciding what it meant\b", r"\bi can see another\b",
        r"\bpart of it did not apply\b", r"\bleave the rest\b", r"\blimited information\b", r"\bmissing context\b",
        r"\bwithout turning\b", r"\bwithout making\b", r"\bnot proof\b", r"\bcan also\b", r"\bi also\b",
        r"\bmaybe\b", r"\bi am not sure\b", r"\bi do not know yet\b", r"\bi'm not ready\b", r"\bi am not ready\b",
    ],
    "fragmentation": [
        r"\bi know .* but .* (feel|body|reacts|believe)\b", r"\bpart of me .* another part\b",
        r"\bi trust .* but .* leave\b", r"\bi am proud .* but .* fraud\b", r"\bi know i earned .* but\b",
        r"\bi do not care .* except\b", r"\bit does not matter .* but\b", r"\bi want .* but part of me\b",
        r"\bshe tells herself .* but\b", r"\bover it.* but\b", r"\bnot figured out\b", r"\bhave not figured out\b",
        r"\bi cannot tell which part\b", r"\bi don't know .* whether\b", r"\bi do not know .* whether\b",
        r"\bi am fine.*probably\b", r"\bi mean, probably\b", r"\bnot sure what i feel\b",
    ],
    "agency_collapse": [
        r"\bi can't think\b", r"\bi cannot think\b", r"\bi can't process\b", r"\bi cannot process\b",
        r"\bi don't know what .* do\b", r"\bi do not know what .* do\b", r"\bnothing makes sense\b", r"\bnothing fits\b",
        r"\bit is too much\b", r"\bi can't find the thread\b", r"\bi cannot find the thread\b", r"\bi cannot explain\b",
        r"\bi cannot .* organize\b", r"\bi feel like i am disappearing\b", r"\bone more thing will break me\b",
        r"\bcannot get a clean thought\b", r"\bclean thought .* stay still\b", r"\bi just want everything to stop\b",
    ],
    "integration": [
        r"\bit no longer defines me\b", r"\bno longer defines me\b", r"\bi am still me\b", r"\bchanged me .* did not erase me\b",
        r"\bdid not erase me\b", r"\bdid not lose myself\b", r"\bi did not lose myself\b", r"\bi revised myself\b",
        r"\bi revised the story\b", r"\bi can see the thread\b", r"\bmore accurate story\b", r"\bchoose differently now\b",
        r"\bdo not have to keep living\b", r"\bother explanations\b", r"\bnot proof that i am weak\b", r"\bdoes not mean i was worthless\b",
        r"\bdoes not mean .* stupid\b", r"\bnot define me\b", r"\bdoes not define me\b", r"\bwithout making it mean\b",
        r"\bwithout turning .* proof\b", r"\bbetter place to start\b", r"\bi have a more accurate story now\b", r"\bstaying honest with myself\b",
    ],
    "discernment": [
        r"\bnot accurate\b", r"\binaccurate\b", r"\bfactually wrong\b", r"\bdoes not support\b", r"\bthe data\b",
        r"\bthe facts\b", r"\bevidence\b", r"\bthat part .* true\b", r"\bmissing context\b", r"\blimited information\b",
        r"\bnot feedback\b", r"\bpart of it did not apply\b",
    ],
    "boundary": [
        r"\bi do not accept\b", r"\bi don't accept\b", r"\bnot feedback\b", r"\bwas not feedback\b", r"\bcalling me\b",
        r"\bwithout accepting disrespect\b", r"\bdisrespect\b", r"\bi can take responsibility\b", r"\bthat is not acceptable\b",
        r"\bboundary\b",
    ],
    "accountability": [
        r"\bi can take responsibility\b", r"\bi take responsibility\b", r"\bi need to own\b", r"\bi own that part\b",
        r"\bthat part is on me\b", r"\bi could have handled\b", r"\bi contributed\b", r"\bmy mistake\b",
        r"\bmaybe i could have\b", r"\bi avoided\b",
    ],
    "partial_acceptance": [
        r"\bpart of it was useful\b", r"\bpart of it applied\b", r"\bpart of it did not apply\b", r"\bsome of.* fair\b",
        r"\bi agree with part\b", r"\bi accept part\b", r"\bi can use part\b", r"\bi can take what helps\b",
        r"\bleave the rest\b", r"\bpart of the message\b", r"\bpart of what i meant\b",
    ],
    "context_markers": [
        r"\bwithout context\b", r"\bmissing context\b", r"\bout of context\b", r"\bgiven the constraints\b",
        r"\blimited information\b", r"\bat the time\b", r"\bunder those circumstances\b", r"\bcircumstances\b",
    ],
    "weaponized_evidence": [
        r"\bthe data proves they are\b", r"\bdata proves .* incompetent\b", r"\beveryone who disagrees\b",
        r"\banyone who disagrees\b", r"\btoo stupid to understand\b", r"\beither lying or\b",
        r"\bthey are incompetent\b", r"\btoo dumb to understand\b", r"\bonly an idiot\b",
    ],

    "ego_evidence_ambiguity": [
        r"\benjoying being right\b", r"\busing the facts cleanly\b", r"\bquestion whether i am using the facts\b", r"\busing the facts\b",
    ],
    "sarcasm": [
        r"\blove that for me\b", r"\bcompletely fine\b", r"\btotally fine\b", r"\bnothing says\b",
        r"\bsure,\s", r"\bsure\.\s", r"\bsure,?\s*because\b", r"\bsure,?\s*that\b",
        r"\bsure,?\s*great\b", r"\bobviously\b", r"\bpretending\b",
        r"\bemotional stability\b", r"\bstability like\b",
    ],
    "rumination": [
        r"\bchecking .* forty times\b", r"\brefreshing .* thirty times\b", r"\bcan't stop checking\b",
        r"\bcannot stop checking\b", r"\breplaying every word\b", r"\bcannot stop thinking\b", r"\bcan't stop thinking\b",
        r"\bkeep jumping\b", r"\bkeep testing\b",
    ],
    "bodily_distress": [
        r"\btight chest\b", r"\bchest is tight\b", r"\bjaw locked\b", r"\bjaw is not locked\b", r"\bjaw isn't locked\b",
        r"\bcan't breathe\b", r"\bcannot breathe\b", r"\bfrozen\b", r"\bshaking\b", r"\bheart racing\b",
        r"\bwired\b", r"\bnumb\b", r"\bexhausted\b", r"\bshutdown\b", r"\bbody still reacts\b", r"\bmy body\b",
    ],
    "unresolved_resolution": [
        r"\bhave not figured out\b", r"\bhaven't figured out\b", r"\bnot figured out\b", r"\bnot there yet\b",
        r"\bbody still reacts\b", r"\bstill reacts like\b", r"\bi do not know yet\b", r"\bi don't know yet\b",
        r"\bi am not ready\b", r"\bi'm not ready\b", r"\bnot sure\b",
    ],
}

@dataclass
class ScoreResult:
    text: str
    scores: Dict[str, int]
    indexes: Dict[str, float]
    markers: Dict[str, List[str]]
    hinge_results: Dict[str, Any]
    loop_state: str
    confidence: str
    explanation: str


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def cap_score(value: int, minimum: int = 0, maximum: int = 3) -> int:
    return max(minimum, min(maximum, value))


def find_markers(text: str) -> Dict[str, List[str]]:
    normalized = normalize_text(text)
    results: Dict[str, List[str]] = {}
    for category, patterns in MARKERS.items():
        matches = []
        for pattern in patterns:
            if re.search(pattern, normalized):
                matches.append(pattern)
        results[category] = matches
    return results


def marker_count(markers: Dict[str, List[str]], category: str) -> int:
    return len(markers.get(category, []))


def classify_but_hinges(text: str) -> List[str]:
    t = normalize_text(text)
    if " but " not in t:
        return []
    labels: List[str] = []
    if re.search(r"(used to think|changed|wrong|hurts?|failure|not the same).*but.*(now|no longer|did not lose|information|thread|revised)", t):
        labels.append("integrated_but")
    if re.search(r"(disagree|upset|frustrated|unfair|criticism|feedback|plan changed).*but.*(understand|useful|adjusted|learn|fix|clearer|work with)", t):
        labels.append("flexible_but")
    if re.search(r"(feedback|said|maybe|change my approach|avoiding).*but.*(wrong|ridiculous|caused|missing the point|trap|overreacting)", t):
        labels.append("defensive_but")
    if re.search(r"(safe|trust|proud|earned|care|matter|believe|over it|know).*but.*(body|feel|leave|fraud|waiting|cannot|can't|not figured|part of me|replaying|plans)", t):
        labels.append("fragmented_but")
    if re.search(r"(try|change|new words|dress it up).*but.*(nothing|never|pattern.*same|pattern never changes)", t):
        labels.append("rigid_but")
    if not labels:
        labels.append("unclassified_but")
    return labels


def classify_because_attribution(text: str) -> Dict[str, Any]:
    t = normalize_text(text)
    if " because " not in t:
        return {"because_attribution": [], "dominant_attribution": None, "attribution_modifier": "No Because Attribution"}
    patterns = {
        "evidence_based": [r"because .*data .*support", r"because .*data .*shows", r"because .*evidence", r"because .*facts", r"because .*not accurate", r"because .*not true"],
        "process_reflective": [r"because i was trying to protect", r"because i was reacting", r"because i misunderstood", r"because .*old pattern", r"because .*story i was used to", r"because .*easier than explaining"],
        "contextual": [r"because at the time", r"because .*limited information", r"because .*context", r"because .*constraints"],
        "external_blame": [r"because they do not understand", r"because they don't understand", r"because they are wrong", r"because they hate", r"because .*against me", r"because no one listens"],
        "fixed_self": [r"because i always", r"because .*broken", r"because .*who i am", r"because nothing changes", r"because i ruin", r"because people like me"],
        "threat_projection": [r"because .*leave", r"because .*not safe", r"because .*bad .*happen", r"because .*lose everything", r"because .*reject"],
    }
    detected = []
    for label, pats in patterns.items():
        if any(re.search(p, t) for p in pats):
            detected.append(label)
    if not detected:
        detected = ["unclassified"]
    priority = ["evidence_based", "process_reflective", "contextual", "fixed_self", "external_blame", "threat_projection", "unclassified"]
    dominant = next((p for p in priority if p in detected), "unclassified")
    modifier = {
        "evidence_based": "Evidence-Based Discernment",
        "process_reflective": "Process-Reflective Revision",
        "contextual": "Contextual Discernment",
        "external_blame": "Defensive Attribution",
        "fixed_self": "Fixed-Self Attribution",
        "threat_projection": "Threat-Projection Attribution",
        "unclassified": "Because Present / Review Needed",
    }.get(dominant, "Mixed Attribution / Review Needed")
    return {"because_attribution": detected, "dominant_attribution": dominant, "attribution_modifier": modifier}


def calculate_discernment_index(markers: Dict[str, List[str]], hinges: Dict[str, Any]) -> int:
    score = marker_count(markers, "discernment") + marker_count(markers, "partial_acceptance") + marker_count(markers, "context_markers")
    score -= marker_count(markers, "feedback_rejection")
    score -= 3 * marker_count(markers, "weaponized_evidence")
    dominant = hinges.get("because_attribution", {}).get("dominant_attribution")
    if dominant == "evidence_based": score += 2
    if dominant == "contextual": score += 1
    if dominant == "process_reflective": score += 1
    if dominant == "external_blame": score -= 2
    if dominant in {"fixed_self", "threat_projection"}: score -= 1
    return score


def score_dimensions(text: str, markers: Dict[str, List[str]], hinges: Dict[str, Any]) -> Dict[str, int]:
    scores = {dim: 0 for dim in DIMENSIONS}
    for dim, category in [
        ("self_reference", "self_reference"), ("identity_fixity", "fixity"), ("prediction", "prediction"),
        ("threat", "threat"), ("feedback_integration", "feedback_integration"),
        ("narrative_flexibility", "flexibility"), ("fragmentation", "fragmentation"),
        ("integration", "integration"),
    ]:
        scores[dim] = cap_score(marker_count(markers, category))

    if marker_count(markers, "third_person_self_distance"):
        scores["self_reference"] = max(scores["self_reference"], 2)
        scores["identity_fixity"] = max(scores["identity_fixity"], 1)
        scores["prediction"] = max(scores["prediction"], 1)

    if marker_count(markers, "agency_collapse"):
        scores["threat"] = max(scores["threat"], 2)
        scores["fragmentation"] = max(scores["fragmentation"], 2)

    # Auxiliary: bodily distress raises threat floor.
    if marker_count(markers, "bodily_distress"):
        scores["threat"] = max(scores["threat"], 1)
    # Auxiliary: rumination raises prediction and threat.
    if marker_count(markers, "rumination"):
        scores["prediction"] = max(scores["prediction"], 2)
        scores["threat"] = max(scores["threat"], 2)

    but = hinges.get("but", [])
    dominant = hinges.get("because_attribution", {}).get("dominant_attribution")

    if "integrated_but" in but:
        scores["narrative_flexibility"] = max(scores["narrative_flexibility"], 2)
        scores["integration"] = max(scores["integration"], 2)
    if "flexible_but" in but:
        scores["narrative_flexibility"] = max(scores["narrative_flexibility"], 2)
        scores["feedback_integration"] = max(scores["feedback_integration"], 2)
    if "defensive_but" in but:
        scores["feedback_integration"] = min(scores["feedback_integration"], 1)
        scores["narrative_flexibility"] = min(scores["narrative_flexibility"], 1)
    if "fragmented_but" in but:
        scores["fragmentation"] = max(scores["fragmentation"], 2)
    if "rigid_but" in but:
        scores["identity_fixity"] = max(scores["identity_fixity"], 2)
        scores["narrative_flexibility"] = min(scores["narrative_flexibility"], 1)

    if dominant == "evidence_based":
        scores["feedback_integration"] = max(scores["feedback_integration"], 2)
        scores["narrative_flexibility"] = max(scores["narrative_flexibility"], 2)
    elif dominant == "process_reflective":
        scores["feedback_integration"] = max(scores["feedback_integration"], 2)
        scores["narrative_flexibility"] = max(scores["narrative_flexibility"], 2)
        scores["integration"] = max(scores["integration"], 1)
    elif dominant == "contextual":
        scores["narrative_flexibility"] = max(scores["narrative_flexibility"], 2)
        scores["feedback_integration"] = max(scores["feedback_integration"], 1)
    elif dominant == "external_blame":
        scores["feedback_integration"] = min(scores["feedback_integration"], 1)
        scores["narrative_flexibility"] = min(scores["narrative_flexibility"], 1)
        scores["threat"] = max(scores["threat"], 2)
    elif dominant == "fixed_self":
        scores["identity_fixity"] = max(scores["identity_fixity"], 2)
        scores["prediction"] = max(scores["prediction"], 2)
        scores["narrative_flexibility"] = min(scores["narrative_flexibility"], 1)
    elif dominant == "threat_projection":
        scores["threat"] = max(scores["threat"], 2)
        scores["prediction"] = max(scores["prediction"], 2)

    # Old fixity under revision should not cap flexibility.
    revision_present = scores["integration"] >= 2 or dominant == "process_reflective" or "integrated_but" in but
    if scores["identity_fixity"] == 3 and not revision_present:
        scores["narrative_flexibility"] = min(scores["narrative_flexibility"], 1)

    return scores


def calculate_indexes(scores: Dict[str, int], markers: Dict[str, List[str]], hinges: Dict[str, Any]) -> Dict[str, float]:
    IF, TH, PR, NF = scores["identity_fixity"], scores["threat"], scores["prediction"], scores["narrative_flexibility"]
    FB, IN, FR = scores["feedback_integration"], scores["integration"], scores["fragmentation"]
    BD = cap_score(marker_count(markers, "bodily_distress"))  # auxiliary, not a scored dimension
    tpi = (PR + TH) * 1.5 if PR >= 2 and TH >= 2 else PR + TH
    return {
        "rigidity_index": IF + TH + PR - NF,
        "integration_index": FB + NF + IN - FR,
        "threat_prediction_index": tpi,
        "threat_prediction_with_body": tpi + BD,
        "revision_capacity_score": NF + FB + IN - IF,
        "fragmentation_load": FR,
        "discernment_index": calculate_discernment_index(markers, hinges),
    }


def classify_loop_state(text: str, scores: Dict[str, int], indexes: Dict[str, float], markers: Dict[str, List[str]], hinges: Dict[str, Any]) -> Tuple[str, str, str]:
    IF, TH, PR = scores["identity_fixity"], scores["threat"], scores["prediction"]
    FB, NF, FR, IN = scores["feedback_integration"], scores["narrative_flexibility"], scores["fragmentation"], scores["integration"]
    but = hinges.get("but", [])
    text_flags = {k: marker_count(markers, k) > 0 for k in MARKERS}
    dominant_because = hinges.get("because_attribution", {}).get("dominant_attribution")
    discernment_index = indexes.get("discernment_index", 0)
    normalized = normalize_text(text)

    # Sarcasm-growth collision: growth markers paired with dismissal, sarcasm,
    # or high fixity without flexibility suggest false integration.
    growth_present = marker_count(markers, "feedback_integration") > 0
    dismissal_present = marker_count(markers, "feedback_rejection") > 0
    sarcasm_present = text_flags.get("sarcasm", False)
    if growth_present and dismissal_present:
        return "Mixed / Review Needed", "Growth language co-occurs with dismissal, suggesting possible sarcasm or false integration.", "Medium"
    if growth_present and sarcasm_present:
        return "Mixed / Review Needed", "Growth language co-occurs with sarcasm markers, suggesting ironic framing.", "Medium"
    if growth_present and IF >= 2 and NF <= 1 and IN == 0:
        return "Mixed / Review Needed", "Growth language co-occurs with strong identity fixity and no flexibility or revision.", "Medium"

    # Mixed / Review high-priority ambiguity cases.
    if text_flags["sarcasm"] and (text_flags["bodily_distress"] or text_flags["rumination"]):
        return "Mixed / Review Needed", "Sarcasm co-occurs with bodily distress or rumination.", "Medium"
    if text_flags["weaponized_evidence"]:
        return "Defensive", "Evidence language is paired with global blame or contempt.", "High"
    if text_flags.get("ego_evidence_ambiguity"):
        return "Mixed / Review Needed", "Evidence language is paired with self-questioning about ego or motive.", "Medium"
    if re.search(r"\bi do not know yet\b|\bi don't know yet\b|\bi am not ready\b|\bi'm not ready\b|\bnot sure whether\b|\bi am not sure whether\b", normalized):
        pass
    # High-priority mixed uncertainty cases.
    if text_flags["sarcasm"] and text_flags["unresolved_resolution"]:
        return "Mixed / Review Needed", "Sarcasm or soft denial co-occurs with unresolved emotional meaning.", "Medium"
    if text_flags["unresolved_resolution"] and NF >= 2 and not text_flags["bodily_distress"]:
        return "Mixed / Review Needed", "The text is reflective but explicitly undecided or unresolved.", "Medium"

    # Boundary before defense.
    if text_flags["boundary"] and text_flags["accountability"]:
        return "Flexible", "Boundary-setting co-occurs with accountability.", "High"
    # Boundary without accountability or evidence is ambiguous, not neutral.
    if text_flags["boundary"] and not text_flags["accountability"] and discernment_index < 2:
        return "Mixed / Review Needed", "Boundary or rejection language is present without accountability, evidence, or enough context.", "Medium"

    # Defensive before rigid when outside blame or feedback rejection dominates.
    if dominant_because == "external_blame" or "defensive_but" in but:
        return "Defensive", "External blame or defensive hinge dominates.", "High"
    if marker_count(markers, "feedback_rejection") and discernment_index < 2 and FB <= 1 and NF <= 1 and IN == 0:
        return "Defensive", "The text rejects feedback through dismissal, blame, or low-discernment attribution.", "High"

    # Overload requires collapse or extreme threat-prediction/rumination.
    if text_flags["agency_collapse"] and TH >= 2 and IN <= 1:
        return "Overloaded", "Agency, meaning, or action collapses.", "High"
    if text_flags["rumination"] and TH >= 3 and PR >= 2 and IN == 0:
        return "Overloaded", "Threat-prediction and rumination dominate without resolution.", "High"

    # Unresolved body/model splits are fragmented, not integrated.
    if text_flags["unresolved_resolution"] and (FR >= 2 or text_flags["bodily_distress"]):
        return "Fragmented", "The text names a pattern but explicitly leaves it unresolved.", "High"
    if FR >= 2 and ("fragmented_but" in but or text_flags["fragmentation"] or text_flags["third_person_self_distance"]) and not text_flags["agency_collapse"]:
        return "Fragmented", "Competing self-models remain active without resolution.", "High"

    # Integrated requires explicit continuity/revision, or strong process-reflective revision.
    if IN >= 2 and (NF >= 2 or FB >= 2) and IF <= 1 and not text_flags["unresolved_resolution"]:
        return "Integrated", "The text shows updated continuity and self-model revision.", "High"
    if dominant_because == "process_reflective" and IN >= 1 and FB >= 2 and NF >= 2 and not text_flags["unresolved_resolution"]:
        return "Integrated", "Process-reflective attribution revises the self-model.", "High"
    if IN >= 3 and not text_flags["unresolved_resolution"]:
        return "Integrated", "The text contains strong updated-continuity markers.", "High"
    if IN >= 1 and NF >= 3 and not text_flags["unresolved_resolution"]:
        return "Integrated", "The text integrates competing truths into a revised starting point.", "Medium"

    # Third-person rigid mirror, unless explicit ambivalence softens it into Mixed.
    if text_flags["third_person_self_distance"] and NF >= 1 and IN == 0 and TH <= 1:
        return "Mixed / Review Needed", "Third-person self-distance is present but framed ambivalently.", "Medium"
    if text_flags["third_person_self_distance"] and IF >= 1 and PR >= 1 and NF <= 1 and IN <= 1:
        return "Rigid", "Third-person self-distance expresses fixed identity expectation.", "Medium"

    if IF >= 2 and NF <= 1 and IN <= 1 and FB <= 1:
        return "Rigid", "High identity fixity with low flexibility and integration.", "High"
    if IF >= 1 and PR >= 2 and NF <= 1 and IN == 0:
        return "Rigid", "Fixed expectation and prediction dominate without revision.", "High"
    if IF >= 1 and PR >= 1 and TH >= 1 and NF <= 1 and IN == 0:
        return "Rigid", "Fatalistic prediction and threat are generalized into a stable rule.", "Medium"

    if marker_count(markers, "feedback_rejection") and discernment_index >= 2 and (FB >= 2 or NF >= 2) and TH <= 2:
        return "Flexible", "The text rejects part of input through evidence-based discernment.", "Medium"

    if (NF >= 2 and FB >= 1 and IF <= 1 and FR <= 1 and IN < 2) or (FB >= 1 and TH <= 1 and IF <= 1 and FR == 0) or (NF >= 1 and TH <= 1 and IF <= 1 and FR == 0 and IN == 0):
        return "Flexible", "Adaptive flexibility without explicit identity revision.", "Medium"

    # Neutral if no meaningful identity activity.
    if sum(scores[d] for d in ["self_reference", "identity_fixity", "prediction", "threat", "feedback_integration", "narrative_flexibility", "fragmentation", "integration"]) <= 1:
        return "Stable/Neutral", "Objective or administrative text with no self-model activity.", "Medium"

    # Ambiguity patterns.
    if NF >= 2 and IN == 0 and (FR >= 1 or PR >= 1 or TH >= 1):
        return "Mixed / Review Needed", "Signals are reflective but unresolved or evenly balanced.", "Medium"

    return "Mixed / Review Needed", "Signals are mixed or insufficient for confident classification.", "Low"


def hooks_text(markers: Dict[str, List[str]]) -> str:
    """Deprecated. Retained only for backward compatibility. Do not use."""
    return " ".join(" ".join(v) for v in markers.values())


def analyze_text(text: str) -> ScoreResult:
    """Analyze a text sample and return dimension scores, indexes, and loop-state classification."""
    if not isinstance(text, str):
        raise TypeError(f"analyze_text expected a string, got {type(text).__name__}.")
    if not text.strip():
        raise ValueError("analyze_text received empty or whitespace-only text.")

    markers = find_markers(text)
    hinges = {
        "but": classify_but_hinges(text),
        "because_attribution": classify_because_attribution(text),
    }
    scores = score_dimensions(text, markers, hinges)
    indexes = calculate_indexes(scores, markers, hinges)
    loop_state, explanation, confidence = classify_loop_state(text, scores, indexes, markers, hinges)
    return ScoreResult(text=text, scores=scores, indexes=indexes, markers=markers, hinge_results=hinges, loop_state=loop_state, confidence=confidence, explanation=explanation)

# Revision Latency v0.2
DESTABILIZED_STATES = {"Overloaded", "Fragmented", "Rigid", "Defensive"}
ADAPTIVE_STATES = {"Flexible", "Integrated"}
STATE_VALUES = {"Overloaded": -3, "Fragmented": -2, "Rigid": -2, "Defensive": -2, "Mixed / Review Needed": -1, "Stable/Neutral": 0, "Flexible": 2, "Integrated": 3}


def calculate_recovery_stability(state_sequence: List[str]) -> float:
    first = next((i for i, s in enumerate(state_sequence) if s in ADAPTIVE_STATES), None)
    if first is None:
        return 0.0
    tail = state_sequence[first:]
    return sum(1 for s in tail if s in ADAPTIVE_STATES) / len(tail) if tail else 0.0


def calculate_revision_latency(state_sequence: List[str]) -> Dict[str, Any]:
    if not state_sequence:
        return {"latency_to_flexible": None, "latency_to_integrated": None, "stalled_state_count": 0, "no_resolution": True, "regression_count": 0, "final_state": None, "recovery_arc": "No Text", "trajectory_score": 0, "recovery_stability": 0.0, "state_sequence": []}
    starts_destabilized = state_sequence[0] in DESTABILIZED_STATES
    latency_to_flexible = next((i for i, s in enumerate(state_sequence, start=1) if s in ADAPTIVE_STATES), None)
    latency_to_integrated = next((i for i, s in enumerate(state_sequence, start=1) if s == "Integrated"), None)
    stalled = 0
    if starts_destabilized:
        for s in state_sequence:
            if s in ADAPTIVE_STATES:
                break
            stalled += 1
    no_resolution = starts_destabilized and latency_to_flexible is None
    regression_count = sum(1 for a, b in zip(state_sequence, state_sequence[1:]) if a in ADAPTIVE_STATES and b in DESTABILIZED_STATES)
    final_state = state_sequence[-1]
    if all(s == "Stable/Neutral" for s in state_sequence):
        arc = "Stable Neutral"
    elif regression_count:
        arc = "Regression After Recovery"
    elif no_resolution:
        arc = "No Resolution"
    elif latency_to_integrated is not None:
        arc = "Fast Integration" if latency_to_integrated <= 2 else "Gradual Integration"
    elif latency_to_flexible is not None:
        arc = "Fast Partial Recovery" if latency_to_flexible <= 2 else "Gradual Partial Recovery"
    else:
        arc = "Mixed / Unclear"
    return {"latency_to_flexible": latency_to_flexible, "latency_to_integrated": latency_to_integrated, "stalled_state_count": stalled, "no_resolution": no_resolution, "regression_count": regression_count, "final_state": final_state, "recovery_arc": arc, "trajectory_score": sum(STATE_VALUES.get(s, 0) for s in state_sequence), "recovery_stability": calculate_recovery_stability(state_sequence), "state_sequence": state_sequence}


def split_into_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in text.split("\n") if p.strip()]


def analyze_document(text: str) -> Dict[str, Any]:
    paragraphs = split_into_paragraphs(text)
    paragraph_results = []
    state_sequence = []
    for idx, paragraph in enumerate(paragraphs, 1):
        result = analyze_text(paragraph)
        state_sequence.append(result.loop_state)
        paragraph_results.append({"paragraph_number": idx, "text": paragraph, "loop_state": result.loop_state, "confidence": result.confidence, "scores": result.scores, "indexes": result.indexes, "explanation": result.explanation})
    return {"paragraph_results": paragraph_results, "state_sequence": state_sequence, "latency_metrics": calculate_revision_latency(state_sequence)}
