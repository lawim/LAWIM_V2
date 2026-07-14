from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DataCategory(str, Enum):
    CONTACT_INFO = "contact_info"
    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"
    PROPERTY_DETAILS = "property_details"
    BUDGET_INFO = "budget_info"
    PREFERENCES = "preferences"
    PROJECT_DETAILS = "project_details"
    DOSSIER_INFO = "dossier_info"


PRIVACY_LEVELS: dict[str, int] = {
    "public": 0,
    "consent_only": 1,
    "relationship_only": 2,
    "private": 3,
}


@dataclass
class PrivacyPolicy:
    data_category: DataCategory | None = None
    min_privacy_level: str = "consent_only"
    requires_consent: bool = True
    requires_relationship: bool = False
    description: str = ""

    def can_share(
        self,
        has_consent: bool = False,
        has_relationship: bool = False,
    ) -> bool:
        if self.min_privacy_level == "public":
            return True
        if self.min_privacy_level == "private":
            return False
        if self.min_privacy_level == "relationship_only":
            return has_relationship
        if self.min_privacy_level == "consent_only":
            return has_consent
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "data_category": self.data_category.value if self.data_category else None,
            "min_privacy_level": self.min_privacy_level,
            "requires_consent": self.requires_consent,
            "requires_relationship": self.requires_relationship,
            "description": self.description,
        }


DEFAULT_PRIVACY_POLICIES: dict[DataCategory, PrivacyPolicy] = {
    DataCategory.NAME: PrivacyPolicy(
        data_category=DataCategory.NAME,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Name shared after consent",
    ),
    DataCategory.PHONE: PrivacyPolicy(
        data_category=DataCategory.PHONE,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Phone number shared after consent",
    ),
    DataCategory.EMAIL: PrivacyPolicy(
        data_category=DataCategory.EMAIL,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Email shared after consent",
    ),
    DataCategory.ADDRESS: PrivacyPolicy(
        data_category=DataCategory.ADDRESS,
        min_privacy_level="relationship_only",
        requires_consent=True,
        requires_relationship=True,
        description="Address shared only after relationship is established",
    ),
    DataCategory.CONTACT_INFO: PrivacyPolicy(
        data_category=DataCategory.CONTACT_INFO,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Contact info shared after consent",
    ),
    DataCategory.PROPERTY_DETAILS: PrivacyPolicy(
        data_category=DataCategory.PROPERTY_DETAILS,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Property details shared after consent",
    ),
    DataCategory.BUDGET_INFO: PrivacyPolicy(
        data_category=DataCategory.BUDGET_INFO,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Budget information shared after consent",
    ),
    DataCategory.PREFERENCES: PrivacyPolicy(
        data_category=DataCategory.PREFERENCES,
        min_privacy_level="consent_only",
        requires_consent=True,
        description="Preferences shared after consent",
    ),
    DataCategory.PROJECT_DETAILS: PrivacyPolicy(
        data_category=DataCategory.PROJECT_DETAILS,
        min_privacy_level="relationship_only",
        requires_consent=True,
        requires_relationship=True,
        description="Project details shared only after relationship",
    ),
    DataCategory.DOSSIER_INFO: PrivacyPolicy(
        data_category=DataCategory.DOSSIER_INFO,
        min_privacy_level="private",
        requires_consent=True,
        requires_relationship=True,
        description="Dossier information is never shared with partners",
    ),
}


class PrivacyController:
    def __init__(
        self,
        policies: dict[DataCategory, PrivacyPolicy] | None = None,
    ):
        self.policies = policies or dict(DEFAULT_PRIVACY_POLICIES)

    def get_policy(self, category: DataCategory) -> PrivacyPolicy:
        return self.policies.get(category, DEFAULT_PRIVACY_POLICIES.get(
            category,
            PrivacyPolicy(
                data_category=category,
                min_privacy_level="private",
                requires_consent=True,
                description=f"No policy defined for {category.value}",
            ),
        ))

    def filter_shareable_data(
        self,
        data: dict[str, Any],
        has_consent: bool = False,
        has_relationship: bool = False,
    ) -> dict[str, Any]:
        shareable: dict[str, Any] = {}
        for key, value in data.items():
            try:
                category = DataCategory(key)
            except ValueError:
                shareable[key] = value
                continue

            policy = self.get_policy(category)
            if policy.can_share(
                has_consent=has_consent,
                has_relationship=has_relationship,
            ):
                shareable[key] = value

        return shareable

    def get_required_consent_categories(
        self,
        requested_categories: list[DataCategory],
    ) -> list[DataCategory]:
        return [
            cat for cat in requested_categories
            if self.get_policy(cat).requires_consent
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "policies": {
                cat.value: policy.to_dict()
                for cat, policy in self.policies.items()
            }
        }
