from __future__ import annotations
from typing import Any

from ..runtime.errors import RuntimeError
from .handler import ActionHandler


class HandlerRegistryError(RuntimeError):
    pass


class HandlerNotFoundError(HandlerRegistryError):
    pass


class HandlerAlreadyRegisteredError(HandlerRegistryError):
    pass


class ActionHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, ActionHandler] = {}
        self._action_map: dict[str, str] = {}

    def register_handler(self, handler: ActionHandler) -> None:
        name = handler.handler_name
        if not name:
            raise HandlerRegistryError("Handler must have a non-empty handler_name")
        if name in self._handlers:
            raise HandlerAlreadyRegisteredError(
                f"Handler '{name}' already registered"
            )
        self._handlers[name] = handler
        for action_code in handler.supported_actions:
            existing = self._action_map.get(action_code)
            if existing is not None:
                raise HandlerAlreadyRegisteredError(
                    f"Action '{action_code}' already handled by '{existing}', cannot register '{name}'"
                )
            self._action_map[action_code] = name

    def unregister_handler(self, name: str) -> None:
        handler = self._handlers.pop(name, None)
        if handler is None:
            raise HandlerNotFoundError(f"Handler '{name}' not found")
        for action_code in handler.supported_actions:
            self._action_map.pop(action_code, None)

    def resolve_handler(self, action_code: str) -> ActionHandler:
        handler_name = self._action_map.get(action_code)
        if handler_name is None:
            for handler in self._handlers.values():
                if handler.can_handle(action_code):
                    self._action_map[action_code] = handler.handler_name
                    return handler
            raise HandlerNotFoundError(
                f"No handler found for action '{action_code}'"
            )
        handler = self._handlers.get(handler_name)
        if handler is None:
            raise HandlerNotFoundError(
                f"Handler '{handler_name}' for action '{action_code}' not found in registry"
            )
        return handler

    def has_handler_for(self, action_code: str) -> bool:
        try:
            self.resolve_handler(action_code)
            return True
        except HandlerNotFoundError:
            return False

    def list_handlers(self) -> list[ActionHandler]:
        return list(self._handlers.values())

    def list_actions(self) -> list[str]:
        return list(self._action_map.keys())

    def validate_registry(self) -> list[str]:
        errors: list[str] = []
        for name, handler in self._handlers.items():
            if not handler.supported_actions:
                errors.append(f"Handler '{name}' has no supported_actions")
            for action_code in handler.supported_actions:
                mapped = self._action_map.get(action_code)
                if mapped != name:
                    errors.append(
                        f"Action '{action_code}' mapped to '{mapped}' but owned by '{name}'"
                    )
        return errors

    def count(self) -> int:
        return len(self._handlers)
