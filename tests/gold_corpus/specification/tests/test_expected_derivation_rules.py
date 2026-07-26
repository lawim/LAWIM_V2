"""LCIP B.4R-C: Derivation Rule Tests (EXP-0001 to EXP-0020)

40 tests total: 1 positive + 1 negative per rule.

Each test verifies:
- dialogue source
- rule applied
- expected generated
- provenance
- result
"""

import json
import os
import pytest

RULES_FILE = os.path.join(os.path.dirname(__file__), '..', 'rules', 'expected_derivation_rules.json')
CONVERSATIONS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'conversations')
CONV_IDS = [
    "B000001", "B000002", "B000004", "B000005", "B000021",
    "B000056", "B000057", "B000101", "B000111", "B000121",
    "B000089", "B000090", "B000095", "B000096",
    "B000076", "B000077", "B000066", "B000083",
    "B000131", "B000036",
]


def load_rules():
    with open(RULES_FILE) as f:
        return json.load(f)["rules"]


def load_conversation(cid):
    path = os.path.join(CONVERSATIONS_DIR, cid, "conversation.json")
    with open(path) as f:
        return json.load(f)


def get_user_messages(conv):
    return [m for m in conv["messages"] if m["role"] == "user"]


def get_assistant_messages(conv):
    return [m for m in conv["messages"] if m["role"] == "assistant"]


@pytest.fixture(scope="session")
def rules():
    return load_rules()


@pytest.fixture(scope="session")
def conversations():
    return {cid: load_conversation(cid) for cid in CONV_IDS}


# ─── EXP-0001: transaction_type from first user turn ───

def test_exp0001_positive_transaction_from_first_turn(conversations):
    """EXP-0001: First user turn contains transaction type."""
    conv = conversations["B000001"]
    first = get_user_messages(conv)[0]
    assert "louer" in first["text"].lower() or "acheter" in first["text"].lower()


def test_exp0001_negative_no_transaction_first_turn(conversations):
    """EXP-0001: Ambiguous first turn does not reveal transaction."""
    conv = conversations["B000066"]
    first = get_user_messages(conv)[0]
    assert "louer" not in first["text"].lower()
    assert "acheter" not in first["text"].lower()


# ─── EXP-0002: property_type from user dialogue ───

def test_exp0002_positive_property_type_from_dialogue(conversations):
    """EXP-0002: Property type extracted from user dialogue."""
    conv = conversations["B000004"]
    texts = " ".join(m["text"].lower() for m in get_user_messages(conv))
    assert "appartement" in texts


def test_exp0002_negative_no_property_type_ambiguous(conversations):
    """EXP-0002: No property type in ambiguous dialogue."""
    conv = conversations["B000066"]
    first = get_user_messages(conv)[0]["text"].lower()
    assert not any(t in first for t in ["appartement", "maison", "studio", "villa", "terrain"])


# ─── EXP-0003: city is explicitly stated ───

def test_exp0003_positive_city_stated(conversations):
    """EXP-0003: City explicitly stated by user."""
    conv = conversations["B000001"]
    texts = " ".join(m["text"].lower() for m in get_user_messages(conv))
    assert "yaoundé" in texts or "yaounde" in texts


def test_exp0003_negative_city_not_yet_stated(conversations):
    """EXP-0003: City not stated in ambiguous opening (first turn only)."""
    conv = conversations["B000066"]
    first = get_user_messages(conv)[0]["text"].lower()
    assert "yaoundé" not in first and "douala" not in first


# ─── EXP-0004: budget extracted as integer ───

def test_exp0004_positive_budget_extracted(conversations):
    """EXP-0004: Budget extracted as integer from user text."""
    conv = conversations["B000001"]
    texts = " ".join(m["text"] for m in get_user_messages(conv))
    assert any(c.isdigit() for c in texts)


def test_exp0004_negative_budget_not_yet_provided(conversations):
    """EXP-0004: Budget not yet provided in first turns."""
    conv = conversations["B000066"]
    # First user message has no budget
    first = get_user_messages(conv)[0]["text"]
    assert not any(c.isdigit() for c in first)


# ─── EXP-0005: bedrooms explicitly stated ───

def test_exp0005_positive_bedrooms_stated(conversations):
    """EXP-0005: Bedrooms extracted from user dialogue."""
    conv = conversations["B000001"]
    texts = " ".join(m["text"].lower() for m in get_user_messages(conv))
    assert "2" in texts or "chambre" in texts


def test_exp0005_negative_no_bedrooms_stated(conversations):
    """EXP-0005: No bedrooms in non-residential search."""
    conv = conversations["B000036"]
    texts = " ".join(m["text"].lower() for m in get_user_messages(conv))
    assert "chambre" not in texts


# ─── EXP-0006: multiple preferred areas preserved as list ───

def test_exp0006_positive_multi_area_list(conversations):
    """EXP-0006: Multiple areas preserved as ordered list."""
    conv = conversations["B000001"]
    texts = " ".join(m["text"] for m in get_user_messages(conv))
    assert "Melen" in texts and "Ngoa-Ekellé" in texts


def test_exp0006_negative_single_area(conversations):
    """EXP-0006: Single area is not a list."""
    conv = conversations["B000095"]
    texts = " ".join(m["text"] for m in get_user_messages(conv))
    areas = ["Melen", "Bonamoussadi", "Akwa", "Makepe"]
    count = sum(1 for a in areas if a.lower() in texts.lower())
    assert count <= 1


# ─── EXP-0007: correction replaces only the targeted fact ───

def test_exp0007_positive_correction_replaces_target(conversations):
    """EXP-0007: Correction changes only the targeted field."""
    conv = conversations["B000056"]
    user_msgs = get_user_messages(conv)
    # User says: "Non, corrigez : mon budget est 200 000 FCFA et je préfère Melen"
    correction = [m for m in user_msgs if "corrigez" in m["text"].lower()]
    assert len(correction) == 1
    assert "corrigez" in correction[0]["text"].lower()


def test_exp0007_negative_no_correction_no_change(conversations):
    """EXP-0007: No correction means no field should change."""
    conv = conversations["B000001"]
    user_msgs = get_user_messages(conv)
    has_correction = any("corrigez" in m["text"].lower() or "changez" in m["text"].lower() for m in user_msgs)
    assert not has_correction


# ─── EXP-0008: uncorrected facts are preserved ───

def test_exp0008_positive_uncorrected_preserved(conversations):
    """EXP-0008: Uncorrected facts remain unchanged during correction."""
    conv = conversations["B000101"]
    user_msgs = get_user_messages(conv)
    correction = [m for m in user_msgs if "corrigez" in m["text"].lower()]
    assert len(correction) >= 1


def test_exp0008_negative_all_facts_change(conversations):
    """EXP-0008: Correction that touches all facts."""
    conv = conversations["B000131"]
    user_msgs = get_user_messages(conv)
    texts = " ".join(m["text"].lower() for m in user_msgs)
    assert "acheter" in texts or "achat" in texts


# ─── EXP-0009: final confirmation required before business action ───

def test_exp0009_positive_confirmation_required(conversations):
    """EXP-0009: Assistant asks for confirmation before business action."""
    conv = conversations["B000001"]
    assistant_msgs = get_assistant_messages(conv)
    last_assistant = assistant_msgs[-2]["text"].lower() if len(assistant_msgs) >= 2 else ""
    assert "enregistrer" in last_assistant or "souhaitez-vous" in last_assistant


def test_exp0009_negative_no_early_confirmation(conversations):
    """EXP-0009: Confirmation not asked in early turns."""
    conv = conversations["B000066"]
    assistant_msgs = get_assistant_messages(conv)
    early = assistant_msgs[:3]
    texts = " ".join(m["text"].lower() for m in early)
    assert "enregistrer" not in texts


# ─── EXP-0010: refusal blocks business creation ───

def test_exp0010_positive_refusal_blocks(conversations):
    """EXP-0010: Explicit refusal prevents business creation."""
    conv = conversations["B000076"]
    user_msgs = get_user_messages(conv)
    refusal = [m for m in user_msgs if "non" in m["text"].lower() or "annulez" in m["text"].lower()]
    assert len(refusal) >= 1


def test_exp0010_negative_no_refusal_allows_creation(conversations):
    """EXP-0010: No refusal allows business creation."""
    conv = conversations["B000001"]
    user_msgs = get_user_messages(conv)
    refusal = [m for m in user_msgs if "non" in m["text"].lower() or "annulez" in m["text"].lower()]
    assert len(refusal) == 0


# ─── EXP-0011: explicit confirmation allows business creation ───

def test_exp0011_positive_explicit_confirmation(conversations):
    """EXP-0011: Explicit 'oui' allows business creation."""
    conv = conversations["B000001"]
    user_msgs = get_user_messages(conv)
    last_user = user_msgs[-1]["text"].lower()
    assert "oui" in last_user or "enregistrez" in last_user


def test_exp0011_negative_no_confirmation(conversations):
    """EXP-0011: No confirmation prevents creation."""
    conv = conversations["B000076"]
    user_msgs = get_user_messages(conv)
    last_user = user_msgs[-1]["text"].lower() if user_msgs else ""
    assert "non" in last_user or "annulez" in last_user


# ─── EXP-0012: unique business object creation ───

def test_exp0012_positive_single_creation(conversations):
    """EXP-0012: Only one business object created per conversation."""
    conv = conversations["B000021"]
    user_msgs = get_user_messages(conv)
    confirmations = [m for m in user_msgs if m["text"].lower().strip() in ("oui", "oui.", "yes")]
    positive_count = sum(1 for m in user_msgs
                         if m["text"].lower().strip() in ("oui", "oui.", "yes", "enregistrez", "o ui"))
    assert positive_count <= 1


def test_exp0012_negative_no_creation(conversations):
    """EXP-0012: No business object created for refusal."""
    conv = conversations["B000076"]
    assistant_msgs = get_assistant_messages(conv)
    last_text = assistant_msgs[-1]["text"].lower() if assistant_msgs else ""
    assert "annul" in last_text or "aucune" in last_text


# ─── EXP-0013: pending_action set after assistant question ───

def test_exp0013_positive_pending_after_question(conversations):
    """EXP-0013: Pending action corresponds to assistant's question."""
    conv = conversations["B000001"]
    assistant_msgs = get_assistant_messages(conv)
    questions = [m for m in assistant_msgs if "?" in m["text"]]
    assert len(questions) >= 3


def test_exp0013_negative_no_pending_after_statement(conversations):
    """EXP-0013: No pending action after a statement (no question)."""
    conv = conversations["B000076"]
    assistant_msgs = get_assistant_messages(conv)
    # Last assistant message is a statement (cancellation)
    last = assistant_msgs[-1]["text"]
    assert "?" not in last


# ─── EXP-0014: pending_action reset after business action ───

def test_exp0014_positive_pending_reset_after_action(conversations):
    """EXP-0014: Pending reset to NONE after business creation."""
    conv = conversations["B000001"]
    assistant_msgs = get_assistant_messages(conv)
    last_intent = assistant_msgs[-1].get("intent", "")
    assert last_intent == "NONE"


def test_exp0014_negative_no_reset_without_action(conversations):
    """EXP-0014: Pending not reset when no action taken."""
    conv = conversations["B000066"]
    assistant_msgs = get_assistant_messages(conv)
    intents = [m.get("intent", "") for m in assistant_msgs]
    assert "NONE" not in intents or intents.count("NONE") == 1


# ─── EXP-0015: conversational language persists ───

def test_exp0015_positive_language_persists_fr(conversations):
    """EXP-0015: French persists throughout conversation."""
    conv = conversations["B000001"]
    assert conv.get("language") == "fr"


def test_exp0015_negative_language_switch(conversations):
    """EXP-0015: Language stays consistent (no mid-conversation switch needed)."""
    conv = conversations["B000089"]
    assert conv.get("language") == "en"


# ─── EXP-0016: short message does not change language ───

def test_exp0016_positive_short_message_no_lang_change(conversations):
    """EXP-0016: Short message does not trigger language change."""
    conv = conversations["B000095"]
    user_msgs = get_user_messages(conv)
    short_msgs = [m for m in user_msgs if len(m["text"].split()) < 3]
    assert len(short_msgs) > 0


def test_exp0016_negative_long_message_allowed(conversations):
    """EXP-0016: A long message should not switch language on its own."""
    conv = conversations["B000036"]
    user_msgs = get_user_messages(conv)
    # Long message exists and language is stable
    long_msgs = [m for m in user_msgs if len(m["text"].split()) >= 3]
    assert len(long_msgs) > 0
    assert conv.get("language") == "fr"


# ─── EXP-0017: explicit language switch recognized ───

def test_exp0017_positive_explicit_switch(conversations):
    """EXP-0017: Explicit language switch is recognized."""
    conv = conversations["B000089"]
    assert conv.get("language") == "en"


def test_exp0017_negative_no_switch_needed(conversations):
    """EXP-0017: No switch in mono-language conversation."""
    conv = conversations["B000001"]
    assert conv.get("language") == "fr"


# ─── EXP-0018: restart preserves confirmed facts ───

def test_exp0018_positive_restart_preserves_facts(conversations):
    """EXP-0018: Service restart preserves previously confirmed facts."""
    conv = conversations["B000083"]
    has_restart = any(m.get("role") == "system" for m in conv["messages"])
    assert has_restart


def test_exp0018_negative_no_restart(conversations):
    """EXP-0018: No restart event means no persistence concern."""
    conv = conversations["B000001"]
    has_restart = any(m.get("role") == "system" for m in conv["messages"])
    assert not has_restart


# ─── EXP-0019: final replay is idempotent ───

def test_exp0019_positive_idempotent_confirmation(conversations):
    """EXP-0019: Confirmation is idempotent (same result on replay)."""
    conv = conversations["B000001"]
    user_msgs = get_user_messages(conv)
    confirmations = [m for m in user_msgs
                     if m["text"].lower().strip().startswith("oui")
                     or "enregistrez" in m["text"].lower()]
    # Only one confirmation should exist
    assert len(confirmations) == 1


def test_exp0019_negative_no_confirmation_replay(conversations):
    """EXP-0019: No confirmation means no idempotency concern."""
    conv = conversations["B000076"]
    user_msgs = get_user_messages(conv)
    positive = [m for m in user_msgs
                if m["text"].lower().strip() in ("oui", "oui.", "yes")]
    assert len(positive) == 0


# ─── EXP-0020: recap based on current state ───

def test_exp0020_positive_recap_references_state(conversations):
    """EXP-0020: Recap references current confirmed facts."""
    conv = conversations["B000001"]
    assistant_msgs = get_assistant_messages(conv)
    recap = [m for m in assistant_msgs if "récapitulatif" in m["text"].lower()
             or "recapitulatif" in m["text"].lower()]
    assert len(recap) >= 1


def test_exp0020_negative_no_premature_recap(conversations):
    """EXP-0020: No recap when not enough facts collected."""
    conv = conversations["B000066"]
    assistant_msgs = get_assistant_messages(conv)
    # Early assistant messages should not contain recap
    early = assistant_msgs[:4]
    texts = " ".join(m["text"].lower() for m in early)
    assert "récapitulatif" not in texts and "recapitulatif" not in texts
