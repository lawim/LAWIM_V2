from ..events.base import RuntimeEvent
from ..events.bus import EventBus
from ..events.project import ProjectEvent
from ..events.conversation import ConversationEvent
from ..events.qualification import QualificationEvent


def test_event_creation():
    e = RuntimeEvent(event_type="TEST", project_id="p1", actor="tester")
    assert e.event_id
    assert e.event_type == "TEST"
    assert e.project_id == "p1"
    assert e.actor == "tester"
    assert e.version == 1
    assert e.timestamp


def test_event_immutable():
    e = RuntimeEvent(event_type="TEST", project_id="p1")
    try:
        e.event_type = "CHANGED"
        assert False, "Should be frozen"
    except Exception:
        pass


def test_event_bus_publish():
    bus = EventBus()
    received = []
    bus.subscribe("TEST_EVENT", lambda e: received.append(e))
    e = RuntimeEvent(event_type="TEST_EVENT", project_id="p1")
    bus.publish(e)
    assert len(received) == 1
    assert received[0].event_id == e.event_id


def test_event_bus_unsubscribe():
    bus = EventBus()
    received = []
    def handler(e):
        received.append(e)
    bus.subscribe("TEST", handler)
    bus.unsubscribe("TEST", handler)
    bus.publish(RuntimeEvent(event_type="TEST"))
    assert len(received) == 0


def test_event_bus_replay():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type="A"))
    bus.publish(RuntimeEvent(event_type="B"))
    bus.publish(RuntimeEvent(event_type="C"))
    history = bus.replay()
    assert len(history) == 3
    partial = bus.replay(from_index=1)
    assert len(partial) == 2
    assert partial[0].event_type == "B"


def test_event_bus_multiple_handlers():
    bus = EventBus()
    results = []
    bus.subscribe("E", lambda e: results.append("h1"))
    bus.subscribe("E", lambda e: results.append("h2"))
    bus.publish(RuntimeEvent(event_type="E"))
    assert len(results) == 2


def test_typed_events():
    project = ProjectEvent(
        event_type="PROJECT_CREATED",
        project_id="p1",
        payload={"type": "BUY"},
    )
    assert project.project_id == "p1"

    conv = ConversationEvent(
        event_type="CONVERSATION_MESSAGE_RECEIVED",
        project_id="p1",
        payload={"message": "Bonjour"},
    )
    assert conv.payload["message"] == "Bonjour"

    qual = QualificationEvent(
        event_type="QUALIFICATION_UPDATED",
        project_id="p1",
        payload={"budget": 100000},
    )
    assert qual.payload["budget"] == 100000
