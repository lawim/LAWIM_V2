from lawim_runtime.intelligence.safety import ResponseValidator, ForbiddenClaimDetector, RedactionPolicy
from lawim_runtime.intelligence.safety.validation import FORBIDDEN_CLAIMS
from lawim_runtime.intelligence.safety.redaction import redact_sensitive_text


def test_response_validator():
    validator = ResponseValidator()
    result = validator.validate("Bonjour, voici les informations")
    assert result.valid

    result2 = validator.validate("Votre paiement a réussi")
    assert not result2.valid
    assert result2.has_forbidden_claims


def test_forbidden_claim_detector():
    detector = ForbiddenClaimDetector()
    matches = detector.detect("Votre paiement a réussi")
    assert len(matches) >= 1

    matches2 = detector.detect("Bonjour, je cherche un appartement")
    assert len(matches2) == 0


def test_redaction():
    redacted = redact_sensitive_text("Mon email est test@example.com")
    assert "[REDACTED_EMAIL]" in redacted
    assert "test@example.com" not in redacted

    redacted2 = redact_sensitive_text("Mon numéro est +237600000000")
    assert "[REDACTED_PHONE]" in redacted2

    redacted3 = redact_sensitive_text("texte normal sans secret")
    assert redacted3 == "texte normal sans secret"


def test_redaction_policy():
    policy = RedactionPolicy(enabled=False)
    text = "test@example.com"
    assert policy.redact(text) == text

    policy.enabled = True
    assert "[REDACTED_EMAIL]" in policy.redact(text)
