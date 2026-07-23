from lawim_runtime.interaction.persistence.repositories import (
    InMemorySessionRepository,
    InMemoryChannelIdentityRepository,
    InMemoryDeduplicationRepository,
    InMemoryDeliveryRepository,
    InMemoryDivergenceRepository,
)
from lawim_runtime.interaction.session import InteractionSession
from lawim_runtime.interaction.delivery import DeliveryResult, DeliveryStatus


def test_session_repository_save_and_get():
    repo = InMemorySessionRepository()
    session = InteractionSession(user_id="user-001", channel="whatsapp")
    repo.save(session)
    fetched = repo.get(session.session_id)
    assert fetched is not None
    assert fetched.user_id == "user-001"


def test_session_repository_list_by_user():
    repo = InMemorySessionRepository()
    s1 = InteractionSession(user_id="user-001", channel="whatsapp")
    s2 = InteractionSession(user_id="user-001", channel="telegram")
    s3 = InteractionSession(user_id="user-002", channel="whatsapp")
    repo.save(s1)
    repo.save(s2)
    repo.save(s3)
    sessions = repo.list_by_user("user-001")
    assert len(sessions) == 2


def test_channel_identity_repository():
    repo = InMemoryChannelIdentityRepository()
    repo.save("whatsapp", "+237600000", "user-001")
    repo.save("telegram", "12345", "user-001")
    assert repo.resolve("whatsapp", "+237600000") == "user-001"
    assert repo.resolve("telegram", "12345") == "user-001"
    assert repo.resolve("whatsapp", "unknown") is None
    channels = repo.list_channels_for_user("user-001")
    assert len(channels) == 2


def test_deduplication_repository():
    repo = InMemoryDeduplicationRepository()
    assert not repo.is_duplicate("whatsapp:msg-001")
    repo.mark_seen("whatsapp:msg-001")
    assert repo.is_duplicate("whatsapp:msg-001")
    assert not repo.is_duplicate("telegram:msg-001")


def test_delivery_repository():
    repo = InMemoryDeliveryRepository()
    r1 = DeliveryResult(delivery_id="del-001", status=DeliveryStatus.SENT, correlation_id="corr-001")
    r2 = DeliveryResult(delivery_id="del-002", status=DeliveryStatus.FAILED, correlation_id="corr-001")
    repo.save(r1)
    repo.save(r2)
    assert repo.get("del-001") is not None
    results = repo.list_by_correlation("corr-001")
    assert len(results) == 2


def test_divergence_repository():
    repo = InMemoryDivergenceRepository()

    class DummyRecord:
        def __init__(self, correlation_id: str, field: str):
            self.correlation_id = correlation_id
            self.field = field

    r1 = DummyRecord("corr-001", "identity")
    r2 = DummyRecord("corr-001", "project")
    repo.save(r1)
    repo.save(r2)
    assert repo.count() == 2
    listed = repo.list_by_correlation("corr-001")
    assert len(listed) == 2
    assert repo.list_by_correlation("corr-999") == []
