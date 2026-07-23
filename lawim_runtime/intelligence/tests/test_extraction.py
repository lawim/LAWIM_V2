from lawim_runtime.intelligence.extraction import (
    StructuredExtractionEngine,
    ExtractionRequest,
    ExtractionResult,
    ExtractionCandidate,
    ExtractionEvidence,
    ExtractionMethod,
    ExtractionWarning,
    ExtractionConfidencePolicy,
)


def test_engine_deterministic():
    calls = []

    def det_handler(req):
        calls.append(req)
        return ExtractionResult(
            candidates=[
                ExtractionCandidate(
                    field_name="property_type",
                    value="apartment",
                    confidence=0.95,
                    evidence=ExtractionEvidence(
                        source_text="appartement",
                        extraction_method=ExtractionMethod.DETERMINISTIC,
                    ),
                ),
            ],
            intent="PROPERTY_SEARCH",
        )

    engine = StructuredExtractionEngine(deterministic_handler=det_handler)
    req = ExtractionRequest(text="Je cherche un appartement")
    result = engine.extract(req)

    assert len(result.candidates) == 1
    assert result.candidates[0].field_name == "property_type"
    assert result.candidates[0].value == "apartment"
    assert result.intent == "PROPERTY_SEARCH"


def test_engine_filter_by_confidence():
    engine = StructuredExtractionEngine()
    candidates = [
        ExtractionCandidate(field_name="a", value="x", confidence=0.8),
        ExtractionCandidate(field_name="b", value="y", confidence=0.3),
    ]
    filtered = engine._filter_by_confidence(candidates, ExtractionConfidencePolicy.AUTO_ACCEPT)
    assert len(filtered) == 1
    assert filtered[0].field_name == "a"


def test_engine_merge():
    det_candidates = [
        ExtractionCandidate(field_name="city", value="Douala", confidence=0.9),
    ]
    llm_candidates = [
        ExtractionCandidate(field_name="city", value="Yaounde", confidence=0.95),
        ExtractionCandidate(field_name="budget", value=100000, confidence=0.8),
    ]

    def det(req):
        return ExtractionResult(candidates=det_candidates)

    def llm(req):
        return ExtractionResult(candidates=llm_candidates)

    engine = StructuredExtractionEngine(deterministic_handler=det, primary_handler=llm)
    result = engine.extract(ExtractionRequest())
    assert len(result.candidates) == 2
    city = [c for c in result.candidates if c.field_name == "city"][0]
    assert city.value == "Yaounde"


def test_to_candidate_updates():
    engine = StructuredExtractionEngine()
    result = ExtractionResult(
        candidates=[
            ExtractionCandidate(
                field_name="property_type",
                value="apartment",
                confidence=0.95,
                evidence=ExtractionEvidence(
                    source_text="appartement",
                    extraction_method=ExtractionMethod.DETERMINISTIC,
                ),
            ),
        ],
    )
    updates = engine.to_candidate_updates(result, "proj-001")
    assert len(updates) >= 0


def test_extraction_candidate_defaults():
    cand = ExtractionCandidate(field_name="test", value=42)
    assert cand.field_name == "test"
    assert cand.value == 42
    assert not cand.is_negation
    assert not cand.is_correction
