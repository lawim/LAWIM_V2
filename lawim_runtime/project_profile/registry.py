from __future__ import annotations
from typing import Any
from .definitions import FieldDefinition
from ..runtime.errors import RuntimeError


class FieldRegistryError(RuntimeError):
    pass


class FieldAlreadyExistsError(FieldRegistryError):
    pass


class FieldNotFoundError(FieldRegistryError):
    pass


class FieldRegistry:
    def __init__(self) -> None:
        self._fields: dict[str, FieldDefinition] = {}
        self._alias_map: dict[str, str] = {}
        self._profile_fields: dict[str, set[str]] = {}

    def register_field(self, field: FieldDefinition, profile_types: tuple[str, ...] = ()) -> None:
        if field.field_name in self._fields:
            raise FieldAlreadyExistsError(f"Field '{field.field_name}' already registered")
        self._fields[field.field_name] = field
        for alias in field.aliases:
            self._alias_map[alias.lower()] = field.field_name
        for pt in profile_types:
            if pt not in self._profile_fields:
                self._profile_fields[pt] = set()
            self._profile_fields[pt].add(field.field_name)

    def get_field(self, name: str) -> FieldDefinition:
        if name in self._fields:
            return self._fields[name]
        resolved = self._alias_map.get(name.lower())
        if resolved and resolved in self._fields:
            return self._fields[resolved]
        raise FieldNotFoundError(f"Field '{name}' not found")

    def has_field(self, name: str) -> bool:
        return name in self._fields or name.lower() in self._alias_map

    def list_fields(self) -> list[FieldDefinition]:
        return list(self._fields.values())

    def list_required_fields(self, profile_type: str = "") -> list[FieldDefinition]:
        fields = self._fields_for_profile(profile_type)
        return [f for f in fields if f.required]

    def list_fields_by_profile(self, profile_type: str) -> list[FieldDefinition]:
        return self._fields_for_profile(profile_type)

    def resolve_alias(self, alias: str) -> str | None:
        return self._alias_map.get(alias.lower())

    def register_profile_fields(self, profile_type: str, field_names: list[str]) -> None:
        self._profile_fields[profile_type] = set(field_names)

    def _fields_for_profile(self, profile_type: str) -> list[FieldDefinition]:
        if not profile_type:
            return list(self._fields.values())
        names = self._profile_fields.get(profile_type, set())
        return [self._fields[n] for n in names if n in self._fields]
