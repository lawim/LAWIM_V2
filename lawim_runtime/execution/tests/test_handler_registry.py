from __future__ import annotations

import pytest

from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.registry import (
    ActionHandlerRegistry,
    HandlerAlreadyRegisteredError,
    HandlerNotFoundError,
    HandlerRegistryError,
)


class _TestHandler(ActionHandler):
    handler_name = "test_handler"
    supported_actions = ["action_1", "action_2"]
    version = "1.0.0"

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context):
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        return {"result": "ok"}

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {"compensated": True}


class _HandlerNoName(ActionHandler):
    handler_name = ""
    supported_actions = ["action_3"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        return {}

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {}


class TestActionHandlerRegistry:
    def test_register_handler(self):
        registry = ActionHandlerRegistry()
        handler = _TestHandler()
        registry.register_handler(handler)
        assert registry.count() == 1

    def test_resolve_handler_by_action(self):
        registry = ActionHandlerRegistry()
        handler = _TestHandler()
        registry.register_handler(handler)
        resolved = registry.resolve_handler("action_1")
        assert resolved is handler

    def test_resolve_handler_not_found(self):
        registry = ActionHandlerRegistry()
        with pytest.raises(HandlerNotFoundError):
            registry.resolve_handler("unknown_action")

    def test_register_duplicate_handler_raises(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        with pytest.raises(HandlerAlreadyRegisteredError):
            registry.register_handler(_TestHandler())

    def test_register_duplicate_action_raises(self):
        registry = ActionHandlerRegistry()
        class _OtherHandler(ActionHandler):
            handler_name = "other"
            supported_actions = ["action_1"]
            def can_handle(self, action_code): return True
            def validate(self, context): return []
            def prepare(self, context): return {}
            def execute(self, context): return {}
            def verify(self, context, raw_result): return True
            def compensate(self, context, result): return {}

        registry.register_handler(_TestHandler())
        with pytest.raises(HandlerAlreadyRegisteredError):
            registry.register_handler(_OtherHandler())

    def test_unregister_handler(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        registry.unregister_handler("test_handler")
        assert registry.count() == 0

    def test_unregister_nonexistent_raises(self):
        registry = ActionHandlerRegistry()
        with pytest.raises(HandlerNotFoundError):
            registry.unregister_handler("ghost")

    def test_has_handler_for(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        assert registry.has_handler_for("action_1") is True
        assert registry.has_handler_for("unknown") is False

    def test_list_handlers(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        handlers = registry.list_handlers()
        assert len(handlers) == 1

    def test_list_actions(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        actions = registry.list_actions()
        assert "action_1" in actions
        assert "action_2" in actions

    def test_validate_registry_clean(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        assert registry.validate_registry() == []

    def test_handler_no_supported_actions(self):
        class _NoActionsHandler(ActionHandler):
            handler_name = "no_actions"
            supported_actions = []
            def can_handle(self, action_code): return False
            def validate(self, context): return []
            def prepare(self, context): return {}
            def execute(self, context): return {}
            def verify(self, context, raw_result): return True
            def compensate(self, context, result): return {}
        registry = ActionHandlerRegistry()
        registry.register_handler(_NoActionsHandler())
        errors = registry.validate_registry()
        assert len(errors) >= 1
