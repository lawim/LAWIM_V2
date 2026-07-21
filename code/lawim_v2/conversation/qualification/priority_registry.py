from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QualificationJourneyDefinition:
    intent_code: str
    journey_code: str
    required_slots: list[str] = field(default_factory=list)
    conditional_slots: list[dict] = field(default_factory=list)
    optional_slots: list[str] = field(default_factory=list)
    priority_order: list[str] = field(default_factory=list)
    completion_rule: str = "all_essential_filled"
    next_action: str = ""
    language_catalog: dict = field(default_factory=dict)


@dataclass
class QualificationSlotDefinition:
    slot_code: str
    category: str = "SECONDARY"
    data_type: str = "string"
    priority: int = 999
    depends_on: list[str] = field(default_factory=list)
    skip_when: dict = field(default_factory=dict)
    validation_rule: str = ""
    question_key: str = ""
    clarification_key: str = ""


class QualificationPriorityRegistry:
    def __init__(self) -> None:
        self._journeys: dict[str, QualificationJourneyDefinition] = {}
        self._slots: dict[str, QualificationSlotDefinition] = {}
        self._init_defaults()

    def _init_defaults(self) -> None:
        self._register_all_slots()
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="search_rental",
                journey_code="SEARCH_RENTAL",
                required_slots=[
                    "transaction_type", "property_type", "city", "budget_xaf",
                ],
                conditional_slots=[
                    {
                        "slot": "district",
                        "depends_on": "city",
                        "skip_when": {},
                    },
                    {
                        "slot": "bedrooms",
                        "depends_on": "property_type",
                        "skip_when": {"property_type": "studio"},
                    },
                    {
                        "slot": "bathrooms",
                        "depends_on": "property_type",
                        "skip_when": {"property_type": "studio"},
                    },
                    {
                        "slot": "kitchens",
                        "depends_on": "property_type",
                        "skip_when": {"property_type": "studio"},
                    },
                ],
                optional_slots=["furnished", "move_in_date", "other_requirements"],
                priority_order=[
                    "transaction_type", "property_type", "city", "district",
                    "budget_xaf", "bedrooms", "bathrooms", "kitchens",
                    "furnished", "move_in_date", "other_requirements",
                ],
                completion_rule="all_essential_filled",
                next_action="search",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="search_purchase",
                journey_code="SEARCH_PURCHASE",
                required_slots=[
                    "property_type", "city", "budget_xaf",
                ],
                conditional_slots=[
                    {
                        "slot": "district",
                        "depends_on": "city",
                        "skip_when": {},
                    },
                ],
                optional_slots=[
                    "bedrooms", "bathrooms", "kitchens",
                    "financing_mode", "title_requirements",
                    "other_requirements",
                ],
                priority_order=[
                    "property_type", "city", "district", "budget_xaf",
                    "bedrooms", "bathrooms", "kitchens",
                    "financing_mode", "title_requirements",
                    "other_requirements",
                ],
                completion_rule="all_essential_filled",
                next_action="search",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="search_land",
                journey_code="SEARCH_LAND",
                required_slots=[
                    "transaction_type", "city", "surface_m2", "budget_xaf",
                ],
                conditional_slots=[
                    {
                        "slot": "district",
                        "depends_on": "city",
                        "skip_when": {},
                    },
                ],
                optional_slots=[
                    "intended_use", "title_status", "accessibility",
                    "utilities", "other_requirements",
                ],
                priority_order=[
                    "transaction_type", "city", "district", "intended_use",
                    "surface_m2", "budget_xaf", "title_status",
                    "accessibility", "utilities", "other_requirements",
                ],
                completion_rule="all_essential_filled",
                next_action="search",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="sell_property",
                journey_code="SELL_PROPERTY",
                required_slots=[
                    "actor_role", "property_type", "city", "ownership_status",
                    "surface_m2", "asking_price",
                ],
                conditional_slots=[
                    {
                        "slot": "district",
                        "depends_on": "city",
                        "skip_when": {},
                    },
                ],
                optional_slots=[
                    "documents_available", "occupancy_status",
                    "inspection_availability",
                ],
                priority_order=[
                    "actor_role", "property_type", "city", "district",
                    "ownership_status", "documents_available", "surface_m2",
                    "asking_price", "occupancy_status",
                    "inspection_availability",
                ],
                completion_rule="all_essential_filled",
                next_action="publish",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="rent_out_property",
                journey_code="RENT_OUT_PROPERTY",
                required_slots=[
                    "actor_role", "property_type", "city", "ownership_status",
                    "monthly_rent",
                ],
                conditional_slots=[
                    {
                        "slot": "district",
                        "depends_on": "city",
                        "skip_when": {},
                    },
                ],
                optional_slots=[
                    "documents_available", "furnished", "charges",
                    "availability_date", "inspection_availability",
                ],
                priority_order=[
                    "actor_role", "property_type", "city", "district",
                    "ownership_status", "documents_available", "furnished",
                    "monthly_rent", "charges", "availability_date",
                    "inspection_availability",
                ],
                completion_rule="all_essential_filled",
                next_action="publish",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="publish_listing",
                journey_code="PUBLISH_LISTING",
                required_slots=[
                    "actor_role", "transaction_type", "property_type",
                    "location", "price", "description", "documents",
                    "media", "consent",
                ],
                conditional_slots=[],
                optional_slots=["availability"],
                priority_order=[
                    "actor_role", "transaction_type", "property_type",
                    "location", "price", "description", "documents",
                    "media", "availability", "consent",
                ],
                completion_rule="all_consent_given",
                next_action="publish",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="property_visit",
                journey_code="PROPERTY_VISIT",
                required_slots=[
                    "property_reference", "preferred_date", "confirmation",
                ],
                conditional_slots=[],
                optional_slots=[
                    "preferred_time_window", "contact_channel",
                    "attendee_count",
                ],
                priority_order=[
                    "property_reference", "preferred_date",
                    "preferred_time_window", "contact_channel",
                    "attendee_count", "confirmation",
                ],
                completion_rule="all_confirmed",
                next_action="schedule",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="document_assistance",
                journey_code="DOCUMENT_ASSISTANCE",
                required_slots=[
                    "document_type", "property_reference",
                    "document_owner", "requested_action", "consent",
                ],
                conditional_slots=[],
                optional_slots=["document_availability"],
                priority_order=[
                    "document_type", "property_reference", "document_owner",
                    "requested_action", "document_availability", "consent",
                ],
                completion_rule="all_essential_filled",
                next_action="process",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="construction_service",
                journey_code="CONSTRUCTION_SERVICE",
                required_slots=[
                    "service_type", "project_location", "property_type",
                    "scope", "budget_range",
                ],
                conditional_slots=[],
                optional_slots=[
                    "project_stage", "timeline", "documents_available",
                    "preferred_contact",
                ],
                priority_order=[
                    "service_type", "project_location", "property_type",
                    "project_stage", "scope", "budget_range", "timeline",
                    "documents_available", "preferred_contact",
                ],
                completion_rule="all_essential_filled",
                next_action="match",
            )
        )
        self._register_journey(
            QualificationJourneyDefinition(
                intent_code="professional_service",
                journey_code="PROFESSIONAL_SERVICE",
                required_slots=[
                    "service_type", "project_location", "property_type",
                    "scope",
                ],
                conditional_slots=[],
                optional_slots=[
                    "project_stage", "timeline", "preferred_contact",
                ],
                priority_order=[
                    "service_type", "project_location", "property_type",
                    "project_stage", "scope", "timeline",
                    "preferred_contact",
                ],
                completion_rule="all_essential_filled",
                next_action="match",
            )
        )

    def _register_all_slots(self) -> None:
        slots: list[QualificationSlotDefinition] = [
            QualificationSlotDefinition(
                slot_code="transaction_type",
                category="ESSENTIAL",
                data_type="string",
                priority=1,
                depends_on=[],
                skip_when={},
                validation_rule="known_transaction_type",
                question_key="qualification.transaction_type",
                clarification_key="qualification.clarify.transaction_type",
            ),
            QualificationSlotDefinition(
                slot_code="property_type",
                category="ESSENTIAL",
                data_type="string",
                priority=2,
                depends_on=[],
                skip_when={},
                validation_rule="known_property_type",
                question_key="qualification.property_type",
                clarification_key="qualification.clarify.property_type",
            ),
            QualificationSlotDefinition(
                slot_code="city",
                category="ESSENTIAL",
                data_type="string",
                priority=3,
                depends_on=[],
                skip_when={},
                validation_rule="known_city",
                question_key="qualification.city",
                clarification_key="qualification.clarify.city",
            ),
            QualificationSlotDefinition(
                slot_code="district",
                category="CONDITIONAL",
                data_type="string",
                priority=4,
                depends_on=["city"],
                skip_when={},
                validation_rule="known_district",
                question_key="qualification.district",
                clarification_key="qualification.clarify.district",
            ),
            QualificationSlotDefinition(
                slot_code="budget_xaf",
                category="ESSENTIAL",
                data_type="integer",
                priority=5,
                depends_on=[],
                skip_when={},
                validation_rule="positive_integer",
                question_key="qualification.budget",
                clarification_key="qualification.clarify.budget",
            ),
            QualificationSlotDefinition(
                slot_code="bedrooms",
                category="CONDITIONAL",
                data_type="integer",
                priority=6,
                depends_on=["property_type"],
                skip_when={"property_type": "studio"},
                validation_rule="non_negative_integer",
                question_key="qualification.bedrooms",
                clarification_key="qualification.clarify.bedrooms",
            ),
            QualificationSlotDefinition(
                slot_code="bathrooms",
                category="CONDITIONAL",
                data_type="integer",
                priority=7,
                depends_on=["property_type"],
                skip_when={"property_type": "studio"},
                validation_rule="non_negative_integer",
                question_key="qualification.bathrooms",
                clarification_key="qualification.clarify.bathrooms",
            ),
            QualificationSlotDefinition(
                slot_code="kitchens",
                category="CONDITIONAL",
                data_type="integer",
                priority=8,
                depends_on=["property_type"],
                skip_when={"property_type": "studio"},
                validation_rule="non_negative_integer",
                question_key="qualification.kitchens",
                clarification_key="qualification.clarify.kitchens",
            ),
            QualificationSlotDefinition(
                slot_code="furnished",
                category="SECONDARY",
                data_type="boolean",
                priority=9,
                depends_on=[],
                skip_when={},
                validation_rule="boolean",
                question_key="qualification.furnished",
                clarification_key="qualification.clarify.furnished",
            ),
            QualificationSlotDefinition(
                slot_code="move_in_date",
                category="SECONDARY",
                data_type="string",
                priority=10,
                depends_on=[],
                skip_when={},
                validation_rule="date_string",
                question_key="qualification.move_in_date",
                clarification_key="qualification.clarify.move_in_date",
            ),
            QualificationSlotDefinition(
                slot_code="other_requirements",
                category="OPTIONAL_USER_REQUIREMENT",
                data_type="string",
                priority=11,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.other_requirements",
                clarification_key="",
            ),
            QualificationSlotDefinition(
                slot_code="intended_use",
                category="SECONDARY",
                data_type="string",
                priority=12,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.intended_use",
                clarification_key="qualification.clarify.intended_use",
            ),
            QualificationSlotDefinition(
                slot_code="surface_m2",
                category="ESSENTIAL",
                data_type="number",
                priority=13,
                depends_on=[],
                skip_when={},
                validation_rule="positive_number",
                question_key="qualification.surface",
                clarification_key="qualification.clarify.surface",
            ),
            QualificationSlotDefinition(
                slot_code="title_status",
                category="SECONDARY",
                data_type="string",
                priority=14,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.title_status",
                clarification_key="qualification.clarify.title_status",
            ),
            QualificationSlotDefinition(
                slot_code="accessibility",
                category="SECONDARY",
                data_type="string",
                priority=15,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.accessibility",
                clarification_key="qualification.clarify.accessibility",
            ),
            QualificationSlotDefinition(
                slot_code="utilities",
                category="SECONDARY",
                data_type="string",
                priority=16,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.utilities",
                clarification_key="qualification.clarify.utilities",
            ),
            QualificationSlotDefinition(
                slot_code="financing_mode",
                category="SECONDARY",
                data_type="string",
                priority=17,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.financing_mode",
                clarification_key="qualification.clarify.financing_mode",
            ),
            QualificationSlotDefinition(
                slot_code="title_requirements",
                category="SECONDARY",
                data_type="string",
                priority=18,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.title_requirements",
                clarification_key="qualification.clarify.title_requirements",
            ),
            QualificationSlotDefinition(
                slot_code="actor_role",
                category="ESSENTIAL",
                data_type="string",
                priority=19,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.actor_role",
                clarification_key="qualification.clarify.actor_role",
            ),
            QualificationSlotDefinition(
                slot_code="ownership_status",
                category="ESSENTIAL",
                data_type="string",
                priority=20,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.ownership_status",
                clarification_key="qualification.clarify.ownership_status",
            ),
            QualificationSlotDefinition(
                slot_code="documents_available",
                category="SECONDARY",
                data_type="string",
                priority=21,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.documents_available",
                clarification_key="qualification.clarify.documents_available",
            ),
            QualificationSlotDefinition(
                slot_code="asking_price",
                category="ESSENTIAL",
                data_type="integer",
                priority=22,
                depends_on=[],
                skip_when={},
                validation_rule="positive_integer",
                question_key="qualification.asking_price",
                clarification_key="qualification.clarify.asking_price",
            ),
            QualificationSlotDefinition(
                slot_code="occupancy_status",
                category="SECONDARY",
                data_type="string",
                priority=23,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.occupancy_status",
                clarification_key="qualification.clarify.occupancy_status",
            ),
            QualificationSlotDefinition(
                slot_code="inspection_availability",
                category="SECONDARY",
                data_type="string",
                priority=24,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.inspection_availability",
                clarification_key="",
            ),
            QualificationSlotDefinition(
                slot_code="monthly_rent",
                category="ESSENTIAL",
                data_type="integer",
                priority=25,
                depends_on=[],
                skip_when={},
                validation_rule="positive_integer",
                question_key="qualification.monthly_rent",
                clarification_key="qualification.clarify.monthly_rent",
            ),
            QualificationSlotDefinition(
                slot_code="charges",
                category="SECONDARY",
                data_type="integer",
                priority=26,
                depends_on=[],
                skip_when={},
                validation_rule="non_negative_integer",
                question_key="qualification.charges",
                clarification_key="qualification.clarify.charges",
            ),
            QualificationSlotDefinition(
                slot_code="availability_date",
                category="SECONDARY",
                data_type="string",
                priority=27,
                depends_on=[],
                skip_when={},
                validation_rule="date_string",
                question_key="qualification.availability_date",
                clarification_key="qualification.clarify.availability_date",
            ),
            QualificationSlotDefinition(
                slot_code="location",
                category="ESSENTIAL",
                data_type="string",
                priority=28,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.location",
                clarification_key="qualification.clarify.location",
            ),
            QualificationSlotDefinition(
                slot_code="price",
                category="ESSENTIAL",
                data_type="integer",
                priority=29,
                depends_on=[],
                skip_when={},
                validation_rule="positive_integer",
                question_key="qualification.price",
                clarification_key="qualification.clarify.price",
            ),
            QualificationSlotDefinition(
                slot_code="description",
                category="ESSENTIAL",
                data_type="string",
                priority=30,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.description",
                clarification_key="qualification.clarify.description",
            ),
            QualificationSlotDefinition(
                slot_code="documents",
                category="ESSENTIAL",
                data_type="string",
                priority=31,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.documents",
                clarification_key="qualification.clarify.documents",
            ),
            QualificationSlotDefinition(
                slot_code="media",
                category="ESSENTIAL",
                data_type="string",
                priority=32,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.media",
                clarification_key="qualification.clarify.media",
            ),
            QualificationSlotDefinition(
                slot_code="availability",
                category="SECONDARY",
                data_type="string",
                priority=33,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.availability",
                clarification_key="qualification.clarify.availability",
            ),
            QualificationSlotDefinition(
                slot_code="consent",
                category="ESSENTIAL",
                data_type="boolean",
                priority=34,
                depends_on=[],
                skip_when={},
                validation_rule="boolean",
                question_key="qualification.consent",
                clarification_key="qualification.clarify.consent",
            ),
            QualificationSlotDefinition(
                slot_code="property_reference",
                category="ESSENTIAL",
                data_type="string",
                priority=35,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.property_reference",
                clarification_key="qualification.clarify.property_reference",
            ),
            QualificationSlotDefinition(
                slot_code="preferred_date",
                category="ESSENTIAL",
                data_type="string",
                priority=36,
                depends_on=[],
                skip_when={},
                validation_rule="date_string",
                question_key="qualification.preferred_date",
                clarification_key="qualification.clarify.preferred_date",
            ),
            QualificationSlotDefinition(
                slot_code="preferred_time_window",
                category="SECONDARY",
                data_type="string",
                priority=37,
                depends_on=["preferred_date"],
                skip_when={},
                validation_rule="",
                question_key="qualification.preferred_time_window",
                clarification_key="qualification.clarify.preferred_time_window",
            ),
            QualificationSlotDefinition(
                slot_code="contact_channel",
                category="SECONDARY",
                data_type="string",
                priority=38,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.contact_channel",
                clarification_key="qualification.clarify.contact_channel",
            ),
            QualificationSlotDefinition(
                slot_code="attendee_count",
                category="SECONDARY",
                data_type="integer",
                priority=39,
                depends_on=[],
                skip_when={},
                validation_rule="positive_integer",
                question_key="qualification.attendee_count",
                clarification_key="qualification.clarify.attendee_count",
            ),
            QualificationSlotDefinition(
                slot_code="confirmation",
                category="ESSENTIAL",
                data_type="boolean",
                priority=40,
                depends_on=[],
                skip_when={},
                validation_rule="boolean",
                question_key="qualification.confirmation",
                clarification_key="qualification.clarify.confirmation",
            ),
            QualificationSlotDefinition(
                slot_code="document_type",
                category="ESSENTIAL",
                data_type="string",
                priority=41,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.document_type",
                clarification_key="qualification.clarify.document_type",
            ),
            QualificationSlotDefinition(
                slot_code="document_owner",
                category="ESSENTIAL",
                data_type="string",
                priority=42,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.document_owner",
                clarification_key="qualification.clarify.document_owner",
            ),
            QualificationSlotDefinition(
                slot_code="requested_action",
                category="ESSENTIAL",
                data_type="string",
                priority=43,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.requested_action",
                clarification_key="qualification.clarify.requested_action",
            ),
            QualificationSlotDefinition(
                slot_code="document_availability",
                category="SECONDARY",
                data_type="string",
                priority=44,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.document_availability",
                clarification_key="qualification.clarify.document_availability",
            ),
            QualificationSlotDefinition(
                slot_code="service_type",
                category="ESSENTIAL",
                data_type="string",
                priority=45,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.service_type",
                clarification_key="qualification.clarify.service_type",
            ),
            QualificationSlotDefinition(
                slot_code="project_location",
                category="ESSENTIAL",
                data_type="string",
                priority=46,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.project_location",
                clarification_key="qualification.clarify.project_location",
            ),
            QualificationSlotDefinition(
                slot_code="project_stage",
                category="SECONDARY",
                data_type="string",
                priority=47,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.project_stage",
                clarification_key="qualification.clarify.project_stage",
            ),
            QualificationSlotDefinition(
                slot_code="scope",
                category="ESSENTIAL",
                data_type="string",
                priority=48,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.scope",
                clarification_key="qualification.clarify.scope",
            ),
            QualificationSlotDefinition(
                slot_code="budget_range",
                category="ESSENTIAL",
                data_type="string",
                priority=49,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.budget_range",
                clarification_key="qualification.clarify.budget_range",
            ),
            QualificationSlotDefinition(
                slot_code="timeline",
                category="SECONDARY",
                data_type="string",
                priority=50,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.timeline",
                clarification_key="qualification.clarify.timeline",
            ),
            QualificationSlotDefinition(
                slot_code="preferred_contact",
                category="SECONDARY",
                data_type="string",
                priority=51,
                depends_on=[],
                skip_when={},
                validation_rule="",
                question_key="qualification.preferred_contact",
                clarification_key="qualification.clarify.preferred_contact",
            ),
        ]
        for slot in slots:
            self._slots[slot.slot_code] = slot

    def _register_journey(self, journey: QualificationJourneyDefinition) -> None:
        for slot_code in journey.priority_order:
            if slot_code not in self._slots:
                raise ValueError(
                    f"Journey '{journey.journey_code}' references unknown slot "
                    f"'{slot_code}'. Register the slot definition first."
                )
        for existing in self._journeys.values():
            if isinstance(existing, QualificationJourneyDefinition):
                if existing.journey_code == journey.journey_code:
                    raise ValueError(
                        f"Duplicate journey code: {journey.journey_code}"
                    )
        self._journeys[journey.intent_code] = journey
        self._journeys[journey.journey_code] = journey

    def get_journey(
        self, intent_code: str
    ) -> QualificationJourneyDefinition | None:
        return self._journeys.get(intent_code)

    def get_slot(
        self, slot_code: str
    ) -> QualificationSlotDefinition | None:
        return self._slots.get(slot_code)

    def resolve_priority(
        self,
        journey: QualificationJourneyDefinition,
        known_slots: dict[str, Any],
    ) -> str | None:
        for slot_code in journey.priority_order:
            if slot_code in known_slots:
                continue
            slot_def = self._slots.get(slot_code)
            if slot_def is None:
                continue
            if slot_def.skip_when:
                skip = False
                for field, value in slot_def.skip_when.items():
                    if field in known_slots and known_slots[field] == value:
                        skip = True
                        break
                if skip:
                    continue
            deps_met = all(
                dep in known_slots for dep in slot_def.depends_on
            )
            if not deps_met:
                continue
            return slot_code
        return None

    def resolve_all_missing(
        self,
        journey: QualificationJourneyDefinition,
        known_slots: dict[str, Any],
    ) -> list[str]:
        missing: list[str] = []
        for slot_code in journey.priority_order:
            if slot_code in known_slots:
                continue
            slot_def = self._slots.get(slot_code)
            if slot_def is None:
                continue
            if slot_def.skip_when:
                skip = False
                for field, value in slot_def.skip_when.items():
                    if field in known_slots and known_slots[field] == value:
                        skip = True
                        break
                if skip:
                    continue
            deps_met = all(
                dep in known_slots for dep in slot_def.depends_on
            )
            if not deps_met:
                continue
            missing.append(slot_code)
        return missing

    def validate_dependencies(self) -> list[str]:
        issues: list[str] = []
        slot_codes = set(self._slots.keys())
        for journey in self._journeys.values():
            for slot_code in journey.priority_order:
                slot_def = self._slots.get(slot_code)
                if slot_def is None:
                    issues.append(
                        f"Journey '{journey.journey_code}': slot '{slot_code}' "
                        f"not found in slot definitions"
                    )
                    continue
                for dep in slot_def.depends_on:
                    if dep not in slot_codes:
                        issues.append(
                            f"Slot '{slot_code}' depends on unknown slot '{dep}'"
                        )
                    if dep not in journey.priority_order:
                        issues.append(
                            f"Journey '{journey.journey_code}': "
                            f"dependency '{dep}' of slot '{slot_code}' is not "
                            f"in the priority_order"
                        )
                if slot_def.skip_when:
                    for field in slot_def.skip_when:
                        if field not in slot_codes:
                            issues.append(
                                f"Slot '{slot_code}' skip_when references "
                                f"unknown slot '{field}'"
                            )
        if not self._journeys:
            issues.append("No journeys registered")
        journey_count = len(set(j.journey_code for j in self._journeys.values()))
        if journey_count == 0:
            issues.append("No journeys registered")
        return issues

    def all_journeys(self) -> list[QualificationJourneyDefinition]:
        seen: set[str] = set()
        result: list[QualificationJourneyDefinition] = []
        for j in self._journeys.values():
            if j.journey_code not in seen:
                seen.add(j.journey_code)
                result.append(j)
        return result

    def all_slots(self) -> list[QualificationSlotDefinition]:
        return list(self._slots.values())

    def count_journeys(self) -> int:
        return len(set(j.journey_code for j in self._journeys.values()))

    def count_slots(self) -> int:
        return len(self._slots)
