from lawim_runtime.interaction.divergence import InteractionDivergenceAnalyzer


def test_no_divergence():
    analyzer = InteractionDivergenceAnalyzer()
    v2 = {"resolved_identity": "user-001", "next_action": "ASK_MISSING_FIELD"}
    v3 = {"resolved_identity": "user-001", "next_action": "ASK_MISSING_FIELD"}
    divergences = analyzer.compare("int-001", "corr-1", "whatsapp", v2, v3)
    assert len(divergences) == 0


def test_divergence_detected():
    analyzer = InteractionDivergenceAnalyzer()
    v2 = {"next_action": "START_MATCHING", "handover": False}
    v3 = {"next_action": "ASK_MISSING_FIELD", "handover": False}
    divergences = analyzer.compare("int-001", "corr-1", "whatsapp", v2, v3)
    assert len(divergences) >= 1


def test_handover_divergence():
    analyzer = InteractionDivergenceAnalyzer()
    v2 = {"handover": False}
    v3 = {"handover": True}
    divergences = analyzer.compare("int-001", "corr-1", "whatsapp", v2, v3)
    handover_div = [d for d in divergences if d.field_name == "handover"]
    assert len(handover_div) == 1
    assert handover_div[0].v2_value is False
    assert handover_div[0].v3_value is True


def test_count():
    analyzer = InteractionDivergenceAnalyzer()
    assert analyzer.count() == 0
    analyzer.record_divergence("int-001", "corr-1", "whatsapp", "intent", "search", "greeting")
    assert analyzer.count() == 1
