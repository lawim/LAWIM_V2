from lawim_runtime.intelligence.evaluation import AIEvaluator, EvaluationCase, EvaluationCategory


def test_evaluator_empty():
    ev = AIEvaluator()
    summary = ev.summary()
    assert summary == {}


def test_evaluator_single_case():
    ev = AIEvaluator()
    ev.register_case(EvaluationCase(
        input_text="Je cherche un appartement",
        expected_intent="PROPERTY_SEARCH",
    ))

    def extractor(text):
        class MockResult:
            intent = "PROPERTY_SEARCH"
        return MockResult()

    results = ev.evaluate(extractor)
    assert len(results) == 1
    assert results[0].is_correct


def test_evaluator_summary():
    ev = AIEvaluator()
    ev.register_case(EvaluationCase(input_text="test1", expected_intent="A"))
    ev.register_case(EvaluationCase(input_text="test2", expected_intent="B"))

    calls = 0

    def extractor(text):
        nonlocal calls
        calls += 1
        class MockResult:
            intent = "A" if calls == 1 else "C"
        return MockResult()

    results = ev.evaluate(extractor)
    summary = ev.summary()
    assert summary["total_cases"] == 2
    assert summary["correct"] == 1
    assert summary["accuracy"] == 0.5
