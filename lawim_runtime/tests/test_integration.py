from ..events.base import RuntimeEvent
from ..events.bus import EventBus
from ..project.model import ProjectRuntime
from ..project.status import ProjectStatus
from ..project.timeline import Timeline, TimelineEntry
from ..registry.registry import RuntimeRegistry
from ..registry.engine import EngineBase
from ..scheduler.scheduler import RuntimeScheduler
from ..persistence.persistence import RuntimePersistence
from ..telemetry.audit import RuntimeAudit
from ..telemetry.metrics import RuntimeMetrics
from ..runtime.director import RuntimeDirector
from ..api.api import RuntimeAPI
from ..services.conversation_adapter import ConversationRuntimeAdapter
from ..services.runtime_facade import RuntimeFacade


class _MemoryPersistence(RuntimePersistence):
    def __init__(self):
        self.projects: dict[str, ProjectRuntime] = {}
        self.events: list[RuntimeEvent] = []

    def save_project(self, p):
        self.projects[p.project_id] = p

    def load_project(self, pid):
        return self.projects.get(pid)

    def save_event(self, e):
        self.events.append(e)

    def load_events(self, pid):
        return [e for e in self.events if e.project_id == pid]

    def save_timeline_entry(self, e):
        pass


class _TestEngine(EngineBase):
    def __init__(self, name="test"):
        self._name = name

    def name(self):
        return self._name

    def can_handle(self, e):
        return True

    def execute(self, project, event):
        if project is None:
            project = ProjectRuntime()
        if event.event_type == "PROJECT_CREATED":
            project.project_type = event.payload.get(
                "project_type", project.project_type
            )
            project.owner = event.actor
            project.status = ProjectStatus.ACTIVE
        return project


class _QualifyingEngine(EngineBase):
    def name(self):
        return "qualifier"

    def can_handle(self, e):
        return e.event_type == "QUALIFY"

    def execute(self, project, event):
        if project is not None:
            project.qualification = event.payload
            project.status = ProjectStatus.QUALIFYING
        return project


def test_full_pipeline():
    bus = EventBus()
    reg = RuntimeRegistry()
    reg.register("test", _TestEngine())
    sched = RuntimeScheduler()
    sched.set_order(["test"])
    persistence = _MemoryPersistence()
    timeline = Timeline()
    audit = RuntimeAudit()
    metrics = RuntimeMetrics()
    director = RuntimeDirector(bus, reg, sched, persistence, timeline, audit, metrics)
    api = RuntimeAPI(director)

    result = api.create_project(project_type="RENT", owner="user1")
    assert result["project"]["project_type"] == "RENT"
    assert result["project"]["owner"] == "user1"
    assert result["project"]["status"] == "ACTIVE"

    pid = result["project"]["project_id"]
    loaded = persistence.load_project(pid)
    assert loaded is not None
    assert loaded.owner == "user1"


def test_event_replay():
    bus = EventBus()
    events = []
    bus.subscribe("TEST", lambda e: events.append(e))
    e1 = RuntimeEvent(
        event_type="TEST", project_id="p1", payload={"step": 1}
    )
    e2 = RuntimeEvent(
        event_type="TEST", project_id="p1", payload={"step": 2}
    )
    bus.publish(e1)
    bus.publish(e2)
    assert len(events) == 2
    history = bus.replay()
    assert history[0].payload["step"] == 1


def test_runtime_metrics_tracking():
    bus = EventBus()
    reg = RuntimeRegistry()
    reg.register("test", _TestEngine("test"))
    sched = RuntimeScheduler()
    sched.set_order(["test"])
    persistence = _MemoryPersistence()
    timeline = Timeline()
    audit = RuntimeAudit()
    metrics = RuntimeMetrics()
    director = RuntimeDirector(bus, reg, sched, persistence, timeline, audit, metrics)
    api = RuntimeAPI(director)

    api.create_project(project_type="BUY", owner="user2")
    summary = metrics.get_summary()
    assert summary["total_events"] >= 1


def test_conversation_adapter():
    bus = EventBus()
    received = []
    bus.subscribe("CONVERSATION_MESSAGE_RECEIVED", lambda e: received.append(e))
    bus.subscribe("CONVERSATION_INTENT_DETECTED", lambda e: received.append(e))
    bus.subscribe("CONVERSATION_SLOT_UPDATED", lambda e: received.append(e))
    bus.subscribe("QUALIFICATION_READY", lambda e: received.append(e))

    adapter = ConversationRuntimeAdapter(bus)
    adapter.on_message_received("p1", "user1", "Bonjour", "whatsapp")
    adapter.on_intent_detected("p1", "user1", "rental_search", 0.95)
    adapter.on_slot_updated("p1", "user1", "city", "Douala")
    adapter.on_qualification_ready(
        "p1", "user1", {"budget": 180000, "bedrooms": 2}
    )

    assert len(received) == 4
    assert received[0].payload["message"] == "Bonjour"
    assert received[0].source == "whatsapp"
    assert received[1].payload["intent"] == "rental_search"
    assert received[1].payload["confidence"] == 0.95
    assert received[2].payload["field"] == "city"
    assert received[2].payload["value"] == "Douala"
    assert received[3].payload["budget"] == 180000


def test_runtime_facade_health():
    bus = EventBus()
    reg = RuntimeRegistry()
    reg.register("test", _TestEngine("test"))
    sched = RuntimeScheduler()
    sched.set_order(["test"])
    persistence = _MemoryPersistence()
    timeline = Timeline()
    audit = RuntimeAudit()
    metrics = RuntimeMetrics()
    director = RuntimeDirector(bus, reg, sched, persistence, timeline, audit, metrics)
    facade = RuntimeFacade(director)

    health = facade.health()
    assert health["status"] == "ok"
    assert health["runtime"] == "LROS"
    assert health["version"] == "3.0.0-alpha"


def test_runtime_facade_process_event():
    bus = EventBus()
    reg = RuntimeRegistry()
    reg.register("test", _TestEngine("test"))
    sched = RuntimeScheduler()
    sched.set_order(["test"])
    persistence = _MemoryPersistence()
    timeline = Timeline()
    audit = RuntimeAudit()
    metrics = RuntimeMetrics()
    director = RuntimeDirector(bus, reg, sched, persistence, timeline, audit, metrics)
    facade = RuntimeFacade(director)

    result = facade.process_event(
        "PROJECT_CREATED",
        project_id="",
        actor="facade_user",
        project_type="SELL",
    )
    assert result["project"]["project_type"] == "SELL"
    assert result["project"]["owner"] == "facade_user"


def test_multiple_engine_pipeline():
    bus = EventBus()
    reg = RuntimeRegistry()
    test_engine = _TestEngine("creator")
    qual_engine = _QualifyingEngine()
    reg.register("creator", test_engine)
    reg.register("qualifier", qual_engine)
    sched = RuntimeScheduler()
    sched.set_order(["creator", "qualifier"])
    persistence = _MemoryPersistence()
    timeline = Timeline()
    audit = RuntimeAudit()
    metrics = RuntimeMetrics()
    director = RuntimeDirector(bus, reg, sched, persistence, timeline, audit, metrics)
    api = RuntimeAPI(director)

    result = api.create_project(project_type="RENT", owner="multi_user")
    pid = result["project"]["project_id"]

    qual_event = RuntimeEvent(
        event_type="QUALIFY",
        project_id=pid,
        actor="system",
        source="test",
        payload={"budget": 200000, "bedrooms": 3},
    )
    qual_result = api.handle_event(qual_event)
    assert qual_result["project"]["status"] == "QUALIFYING"
    assert qual_result["project"]["qualification"]["budget"] == 200000
