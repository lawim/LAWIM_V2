from lawim_runtime.interaction.orchestrator import InteractionOrchestrator
from lawim_runtime.interaction.envelope import InteractionEnvelope, MessageType
from lawim_runtime.interaction.identity import IdentityResolver
from lawim_runtime.interaction.session import SessionManager
from lawim_runtime.interaction.delivery import DeliveryManager


def test_orchestrator_processes_envelope():
    orch = InteractionOrchestrator()
    env = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-001",
        external_user_id="+237600000",
        raw_sender="+237600000",
        raw_content="Je cherche un appartement",
        message_type=MessageType.TEXT,
    )
    result = orch.process(env)
    assert result.envelope is not None
    assert result.context is not None
    assert result.response_plan is not None
    assert result.error == ""


def test_orchestrator_duplicate_message():
    orch = InteractionOrchestrator()
    env = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="dup-001",
        external_user_id="+237600000",
        raw_sender="+237600000",
        raw_content="hello",
    )
    r1 = orch.process(env)
    assert r1.error == ""

    r2 = orch.process(env)
    assert r2.response_plan is not None
    assert r2.response_plan.is_empty() or "duplicate" in str(r2.warnings)


def test_orchestrator_empty_content():
    orch = InteractionOrchestrator()
    env = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-002",
        external_user_id="+237600000",
        raw_sender="+237600000",
        raw_content="",
    )
    result = orch.process(env)
    assert result.response_plan is not None


def test_orchestrator_identity_resolution():
    resolver = IdentityResolver()
    resolver.link_channel_to_user("user-001", "whatsapp", "+237600000")
    orch = InteractionOrchestrator(identity_resolver=resolver)
    env = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-003",
        external_user_id="+237600000",
        raw_sender="+237600000",
        raw_content="test",
    )
    result = orch.process(env)
    assert result.context is not None
    assert result.context.user_id == "user-001"


def test_orchestrator_session_continuity():
    resolver = IdentityResolver()
    resolver.link_channel_to_user("user-001", "whatsapp", "+237600001")
    orch = InteractionOrchestrator(identity_resolver=resolver)

    env1 = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-004",
        external_user_id="+237600001",
        raw_sender="+237600001",
        raw_content="first message",
    )
    r1 = orch.process(env1)
    session_id_1 = r1.context.session_id if r1.context else ""

    env2 = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-005",
        external_user_id="+237600001",
        raw_sender="+237600001",
        raw_content="second message",
    )
    r2 = orch.process(env2)
    session_id_2 = r2.context.session_id if r2.context else ""
    assert session_id_1 == session_id_2
