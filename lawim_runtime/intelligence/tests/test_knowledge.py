from lawim_runtime.intelligence.knowledge import KnowledgeGateway, KnowledgeQuery, KnowledgeResult, KnowledgeSource, TrustLevel, AnswerStatus


def test_gateway_no_sources():
    gw = KnowledgeGateway()
    q = KnowledgeQuery(text="test query")
    result = gw.query(q)
    assert result.status == AnswerStatus.NO_RELEVANT_SOURCE


def test_gateway_with_sources():
    class MockKnowledge:
        def query(self, text):
            return [KnowledgeSource(source_id="src-001", title="Test Source", trust_level=TrustLevel.VERIFIED_INTERNAL)]

    gw = KnowledgeGateway(knowledge_service=MockKnowledge())
    q = KnowledgeQuery(text="test")
    result = gw.query(q)
    assert result.status == AnswerStatus.ANSWER_SUPPORTED
    assert len(result.sources) > 0


def test_knowledge_source_defaults():
    src = KnowledgeSource(source_id="src-001")
    assert src.trust_level == TrustLevel.UNVERIFIED
    assert src.language == "fr"
