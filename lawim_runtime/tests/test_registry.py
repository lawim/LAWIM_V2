from ..registry.registry import RuntimeRegistry
from ..registry.engine import EngineBase
from ..runtime.errors import EngineNotFoundError
from ..events.base import RuntimeEvent
from ..project.model import ProjectRuntime


class _DummyEngine(EngineBase):
    def name(self):
        return "dummy"

    def can_handle(self, event):
        return True

    def execute(self, project, event):
        return project


def test_register_and_get():
    reg = RuntimeRegistry()
    engine = _DummyEngine()
    reg.register("dummy", engine)
    assert reg.get("dummy") is engine


def test_engine_not_found():
    reg = RuntimeRegistry()
    try:
        reg.get("nonexistent")
        assert False
    except EngineNotFoundError:
        pass


def test_list_engines():
    reg = RuntimeRegistry()
    reg.register("a", _DummyEngine())
    reg.register("b", _DummyEngine())
    assert set(reg.list()) == {"a", "b"}
