from lawim_runtime.intelligence.writing import AIResponseWriter, WriterValidator
from lawim_runtime.intelligence.writing.writer import AIResponseWriterRequest
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType
from lawim_runtime.interaction.response_writer import DeterministicResponseWriter


def test_writer_empty_plan():
    writer = AIResponseWriter()
    result = writer.write(AIResponseWriterRequest())
    assert result.success
    assert result.text == ""


def test_writer_fallback():
    writer = AIResponseWriter(deterministic_fallback=DeterministicResponseWriter())
    plan = InteractionResponsePlan(response_type=ResponseType.GREETING)
    result = writer.write(AIResponseWriterRequest(response_plan=plan))
    assert result.success
    assert result.fallback_used
    assert "Bonjour" in result.text


def test_writer_fallback_safe():
    writer = AIResponseWriter(deterministic_fallback=DeterministicResponseWriter())
    plan = InteractionResponsePlan(response_type=ResponseType.SAFE_FALLBACK)
    result = writer.write(AIResponseWriterRequest(response_plan=plan))
    assert result.success
    assert "difficult\u00e9" in result.text


def test_writer_validator():
    validator = WriterValidator()
    plan = InteractionResponsePlan(response_type=ResponseType.SUCCESS)
    result = validator.validate("Votre paiement a réussi", plan)
    assert not result.valid
    assert result.has_forbidden_claims

    result2 = validator.validate("Voici les résultats", plan)
    assert result2.valid
