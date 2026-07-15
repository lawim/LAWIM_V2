from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .actor import ActorType


class PrivacyLevel(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


@dataclass(frozen=True)
class VisualRole:
    actor_type: ActorType
    code: str
    label_fr: str
    label_en: str
    emoji: str
    display_format: str
    color: str = ""
    privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    mask_phone: bool = True
    mask_email: bool = True
    sort_order: int = 99

    def format_display(self, name: str = "") -> str:
        if name:
            return f"{self.emoji} {self.display_format.replace('{name}', name)}"
        return f"{self.emoji} {self.label_fr}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_type": self.actor_type.value,
            "code": self.code,
            "label_fr": self.label_fr,
            "label_en": self.label_en,
            "emoji": self.emoji,
            "display_format": self.display_format,
            "color": self.color,
            "privacy_level": self.privacy_level.value,
            "mask_phone": self.mask_phone,
            "mask_email": self.mask_email,
        }


_CATALOG: list[VisualRole] = [
    VisualRole(ActorType.AI_ASSISTANT, "AI", "LAWIM AI", "LAWIM AI",
               "\U0001f916", "{name}", color="#6366f1", sort_order=1),
    VisualRole(ActorType.LAWIM_STAFF, "STAFF", "LAWIM ({name})", "LAWIM ({name})",
               "\U0001f9d1\U0000200d\U0001f4bc", "LAWIM ({name})", color="#4f46e5", sort_order=2),
    VisualRole(ActorType.USER, "USER", "Utilisateur", "User",
               "\U0001f464", "Utilisateur", sort_order=10),
    VisualRole(ActorType.OWNER, "OWNER", "Propriétaire", "Owner",
               "\U0001f3e0", "Propriétaire ({name})", sort_order=11),
    VisualRole(ActorType.BUYER, "BUYER", "Acheteur", "Buyer",
               "\U0001f3e1", "Acheteur ({name})", sort_order=12),
    VisualRole(ActorType.TENANT, "TENANT", "Locataire", "Tenant",
               "\U0001f3e2", "Locataire ({name})", sort_order=13),
    VisualRole(ActorType.REAL_ESTATE_AGENT, "AGENT", "Agent immobilier", "Real estate agent",
               "\U0001f3e0", "Agent immobilier ({name})", color="#059669", sort_order=20),
    VisualRole(ActorType.AGENCY, "AGENCY", "Agence", "Agency",
               "\U0001f3e2", "Agence ({name})", color="#0d9488", sort_order=21),
    VisualRole(ActorType.ARCHITECT, "ARCHITECT", "Architecte", "Architect",
               "\U0001f4d0", "Architecte ({name})", color="#7c3aed", sort_order=30),
    VisualRole(ActorType.ENGINEER, "ENGINEER", "Ingénieur", "Engineer",
               "\U0001f477", "Ingénieur ({name})", color="#2563eb", sort_order=31),
    VisualRole(ActorType.TECHNICIAN, "TECH", "Technicien", "Technician",
               "\U0001f527", "Technicien ({name})", sort_order=32),
    VisualRole(ActorType.NOTARY, "NOTARY", "Notaire", "Notary",
               "\u2696\ufe0f", "Notaire ({name})", color="#9333ea", sort_order=33),
    VisualRole(ActorType.INVESTOR, "INVESTOR", "Investisseur", "Investor",
               "\U0001f4b0", "Investisseur ({name})", sort_order=34),
    VisualRole(ActorType.PARTNER, "PARTNER", "Partenaire", "Partner",
               "\U0001f91d", "Partenaire ({name})", sort_order=40),
    VisualRole(ActorType.SYSTEM, "SYSTEM", "Système", "System",
               "\u2699\ufe0f", "Système ({name})", privacy_level=PrivacyLevel.INTERNAL, sort_order=99),
]

_BY_TYPE: dict[ActorType, VisualRole] = {r.actor_type: r for r in _CATALOG}


class VisualRoleRegistry:
    def get(self, actor_type: ActorType) -> VisualRole:
        return _BY_TYPE.get(actor_type, _BY_TYPE[ActorType.USER])

    def list_all(self) -> list[VisualRole]:
        return list(_CATALOG)

    def count(self) -> int:
        return len(_CATALOG)

    def to_dict_list(self) -> list[dict[str, Any]]:
        return [r.to_dict() for r in _CATALOG]


visual_role_registry = VisualRoleRegistry()
