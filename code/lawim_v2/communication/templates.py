from __future__ import annotations

from .engines import CommunicationPlatformEngine


class TemplatesModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().template

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_notification_template(**kwargs)

    def list_templates(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_notification_templates(**kwargs)

    def render(self, *, template_id: int, variables: dict[str, object]) -> dict[str, object]:
        row = self.repository.get_notification_template(template_id)
        rendered = self.engine.render(
            template=str(row.get("body") or ""),
            variables=variables,
        )
        subject = self.engine.render(
            template=str(row.get("subject") or ""),
            variables=variables,
        )
        return {"subject": subject, "body": rendered, "template_id": template_id}
