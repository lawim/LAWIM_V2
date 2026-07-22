from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .models import HandoverData, LeadData, OpportunityData


class CRMRepository(ABC):

    @abstractmethod
    def save_lead(self, lead: LeadData) -> None:
        ...

    @abstractmethod
    def get_lead_by_project(self, project_id: str) -> LeadData | None:
        ...

    @abstractmethod
    def save_opportunity(self, opportunity: OpportunityData) -> None:
        ...

    @abstractmethod
    def save_handover(self, handover: HandoverData) -> None:
        ...

    @abstractmethod
    def list_active_leads(self) -> list[LeadData]:
        ...

    @abstractmethod
    def list_handovers(self) -> list[HandoverData]:
        ...


class InMemoryCRMRepository(CRMRepository):

    def __init__(self) -> None:
        self._leads: dict[str, LeadData] = {}
        self._opportunities: dict[str, OpportunityData] = {}
        self._handovers: dict[str, HandoverData] = {}

    def save_lead(self, lead: LeadData) -> None:
        self._leads[lead.lead_id] = lead

    def get_lead_by_project(self, project_id: str) -> LeadData | None:
        for lead in self._leads.values():
            if lead.project_id == project_id:
                return lead
        return None

    def save_opportunity(self, opportunity: OpportunityData) -> None:
        self._opportunities[opportunity.opportunity_id] = opportunity

    def save_handover(self, handover: HandoverData) -> None:
        self._handovers[handover.handover_id] = handover

    def list_active_leads(self) -> list[LeadData]:
        return [lead for lead in self._leads.values() if lead.status not in ("closed", "lost")]

    def list_handovers(self) -> list[HandoverData]:
        return list(self._handovers.values())
