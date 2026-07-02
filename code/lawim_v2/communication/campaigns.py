from __future__ import annotations

from .engines import CommunicationPlatformEngine


class CampaignsModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().campaign

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_campaign(**kwargs)

    def list_campaigns(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_campaigns(**kwargs)

    def execute(self, campaign_id: int) -> dict[str, object]:
        return self.repository.execute_campaign(campaign_id)

    def pause(self, campaign_id: int) -> dict[str, object]:
        return self.repository.update_campaign(campaign_id, campaign_status="paused")

    def resume(self, campaign_id: int) -> dict[str, object]:
        return self.repository.update_campaign(campaign_id, campaign_status="running")
