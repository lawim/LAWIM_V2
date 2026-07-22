from ..events.base import RuntimeEvent
from ..registry.registry import RuntimeRegistry
from ..registry.engine import EngineBase
from ..scheduler.scheduler import RuntimeScheduler


def test_scheduler_execution_order():
    reg = RuntimeRegistry()
    order = []

    class E1(EngineBase):
        def name(self):
            return "e1"

        def can_handle(self, e):
            return True

        def execute(self, p, e):
            order.append("e1")
            return p

    class E2(EngineBase):
        def name(self):
            return "e2"

        def can_handle(self, e):
            return True

        def execute(self, p, e):
            order.append("e2")
            return p

    reg.register("e1", E1())
    reg.register("e2", E2())
    sched = RuntimeScheduler()
    sched.set_order(["e1", "e2"])
    sched.execute(None, RuntimeEvent(event_type="TEST"), reg)
    assert order == ["e1", "e2"]


def test_scheduler_skips_unregistered():
    reg = RuntimeRegistry()
    order = []

    class E3(EngineBase):
        def name(self):
            return "e3"

        def can_handle(self, e):
            return True

        def execute(self, p, e):
            order.append("e3")
            return p

    reg.register("e3", E3())
    sched = RuntimeScheduler()
    sched.set_order(["nonexistent", "e3"])
    sched.execute(None, RuntimeEvent(event_type="TEST"), reg)
    assert order == ["e3"]
