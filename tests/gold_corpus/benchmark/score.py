"""Gold Corpus scoring engine.

Score categories:
  - Conversation Score: structural integrity + schema compliance
  - Memory Score: slots retained across turns
  - Qualification Score: correct status detection
  - Business Score: correct business action
  - Runtime Score: correct engine + services
  - Language Score: correct language + identity
  - Channel Score: correct channel behaviour

Each score is a float in [0.0, 1.0].
Global Score is the weighted average of all category scores.
"""


WEIGHTS = {
    "conversation": 0.15,
    "memory": 0.15,
    "qualification": 0.15,
    "business": 0.15,
    "runtime": 0.15,
    "language": 0.10,
    "channel": 0.05,
    "intent": 0.10,
}


def compute_conversation_score(pass_count: int, total_count: int) -> float:
    if total_count == 0:
        return 1.0
    return pass_count / total_count


def compute_memory_score(retained_slots: list, expected_slots: list) -> float:
    if not expected_slots:
        return 1.0
    if not retained_slots:
        return 0.0
    matched = sum(1 for s in expected_slots if s in retained_slots)
    return matched / len(expected_slots)


def compute_qualification_score(actual_status: str, expected_status: str) -> float:
    return 1.0 if actual_status == expected_status else 0.0


def compute_business_score(actual_action: str, expected_action: str) -> float:
    return 1.0 if actual_action == expected_action else 0.0


def compute_runtime_score(actual_engine: str, expected_engine: str,
                          actual_services: list, expected_services: list) -> float:
    score = 0.0
    count = 0
    if expected_engine:
        count += 1
        score += 1.0 if actual_engine == expected_engine else 0.0
    if expected_services:
        count += 1
        if actual_services:
            matched = sum(1 for s in expected_services if s in actual_services)
            score += matched / len(expected_services) if expected_services else 1.0
        else:
            score += 0.0
    return score / count if count > 0 else 1.0


def compute_language_score(actual_lang: str, expected_lang: str,
                           actual_identity: str, expected_identity: str) -> float:
    score = 0.0
    count = 0
    if expected_lang:
        count += 1
        score += 1.0 if actual_lang == expected_lang else 0.0
    if expected_identity:
        count += 1
        score += 1.0 if expected_identity in (actual_identity or "") else 0.0
    return score / count if count > 0 else 1.0


def compute_channel_score(actual_channel: str, expected_channel: str) -> float:
    return 1.0 if actual_channel == expected_channel else 0.0


def compute_intent_score(actual_intent: str, expected_intent: str) -> float:
    return 1.0 if actual_intent == expected_intent else 0.0


def compute_global_score(scores: dict) -> float:
    total_weight = 0.0
    weighted_sum = 0.0
    for category, score in scores.items():
        weight = WEIGHTS.get(category, 0.05)
        if score is not None:
            weighted_sum += weight * score
            total_weight += weight
    if total_weight == 0:
        return 0.0
    return weighted_sum / total_weight


def compute_all_scores(
    conversation_pass: int, conversation_total: int,
    retained_slots: list, expected_slots: list,
    actual_status: str, expected_status: str,
    actual_action: str, expected_action: str,
    actual_engine: str, expected_engine: str,
    actual_services: list, expected_services: list,
    actual_lang: str, expected_lang: str,
    actual_identity: str, expected_identity: str,
    actual_channel: str, expected_channel: str,
    actual_intent: str, expected_intent: str,
) -> dict:
    scores = {
        "conversation": compute_conversation_score(conversation_pass, conversation_total),
        "memory": compute_memory_score(retained_slots, expected_slots),
        "qualification": compute_qualification_score(actual_status, expected_status),
        "business": compute_business_score(actual_action, expected_action),
        "runtime": compute_runtime_score(actual_engine, expected_engine, actual_services, expected_services),
        "language": compute_language_score(actual_lang, expected_lang, actual_identity, expected_identity),
        "channel": compute_channel_score(actual_channel, expected_channel),
        "intent": compute_intent_score(actual_intent, expected_intent),
    }
    scores["global"] = compute_global_score(scores)
    return scores
