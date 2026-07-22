from __future__ import annotations


class ProgressiveWizardDecisionAdapter:
    def to_next_field(
        self,
        missing_fields: list[str],
        priority_map: dict[str, int],
    ) -> str | None:
        if not missing_fields:
            return None
        return min(missing_fields, key=lambda f: priority_map.get(f, 999))
