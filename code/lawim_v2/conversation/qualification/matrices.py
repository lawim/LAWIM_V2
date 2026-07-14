from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SUPPORTED_TRANSACTION_TYPES = frozenset({
    "BUY", "SELL", "RENT", "RENT_OUT", "CONSTRUCT", "RENOVATE", "INVEST", "FIND",
})

SUPPORTED_PROPERTY_TYPES = frozenset({
    "APARTMENT", "STUDIO", "ROOM", "HOUSE", "VILLA", "COMMERCIAL", "LAND",
    "BUILDING", "PROPERTY",
})

ALLOWED_ACTIONS_VALUES = frozenset({
    "SEARCH", "MATCH", "RELATIONSHIP", "VISIT", "CONTACT", "HANDOVER", "INFORMATION",
})


@dataclass(frozen=True)
class QualificationMatrix:
    intent: str
    transaction_type: str
    property_type: str
    required_fields: list[str] = field(default_factory=list)
    recommended_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    field_priority: dict[str, int] = field(default_factory=dict)
    validation_rules: dict[str, str] = field(default_factory=dict)
    clarification_rules: dict[str, str] = field(default_factory=dict)
    readiness_threshold: float = 0.6
    allowed_actions: list[str] = field(default_factory=lambda: ["SEARCH", "MATCH", "RELATIONSHIP"])

    def __post_init__(self) -> None:
        _validate_matrix(self)

    @property
    def all_fields(self) -> list[str]:
        return self.required_fields + self.recommended_fields + self.optional_fields

    @property
    def total_field_count(self) -> int:
        return len(self.all_fields)

    def is_field_required(self, field: str) -> bool:
        return field in self.required_fields

    def is_field_recommended(self, field: str) -> bool:
        return field in self.recommended_fields

    def get_field_priority(self, field: str) -> int:
        return self.field_priority.get(field, 999)

    def get_validation_rule(self, field: str) -> str | None:
        return self.validation_rules.get(field)

    def get_clarification_rule(self, field: str) -> str | None:
        return self.clarification_rules.get(field)


def _validate_matrix(matrix: QualificationMatrix) -> None:
    if matrix.transaction_type not in SUPPORTED_TRANSACTION_TYPES:
        raise ValueError(f"Unsupported transaction_type: {matrix.transaction_type}")
    if matrix.property_type not in SUPPORTED_PROPERTY_TYPES:
        raise ValueError(f"Unsupported property_type: {matrix.property_type}")
    for action in matrix.allowed_actions:
        if action not in ALLOWED_ACTIONS_VALUES:
            raise ValueError(f"Unsupported allowed_action: {action}")
    if matrix.readiness_threshold < 0.0 or matrix.readiness_threshold > 1.0:
        raise ValueError("readiness_threshold must be between 0.0 and 1.0")
    if not (0.0 <= matrix.readiness_threshold <= 1.0):
        raise ValueError("readiness_threshold must be between 0.0 and 1.0")


# ---------------------------------------------------------------------------
# Rent parcours
# ---------------------------------------------------------------------------

RENT_STUDIO = QualificationMatrix(
    intent="rent_studio",
    transaction_type="RENT",
    property_type="STUDIO",
    required_fields=["city", "budget_max"],
    recommended_fields=["surface_sqm", "deadline"],
    optional_fields=["furnished", "parking", "contact_phone"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "furnished": 5, "parking": 6, "contact_phone": 7},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

RENT_ROOM = QualificationMatrix(
    intent="rent_room",
    transaction_type="RENT",
    property_type="ROOM",
    required_fields=["city", "budget_max"],
    recommended_fields=["deadline"],
    optional_fields=["furnished", "parking", "contact_phone"],
    field_priority={"city": 1, "budget_max": 2, "deadline": 3, "furnished": 4, "parking": 5, "contact_phone": 6},
    validation_rules={"budget_max": "positive_integer", "city": "known_city"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

RENT_APARTMENT = QualificationMatrix(
    intent="rent_apartment",
    transaction_type="RENT",
    property_type="APARTMENT",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "floor", "furnished", "parking"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "floor": 7, "furnished": 8, "parking": 9},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

RENT_HOUSE = QualificationMatrix(
    intent="rent_house",
    transaction_type="RENT",
    property_type="HOUSE",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "garden"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "garden": 9},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

RENT_VILLA = QualificationMatrix(
    intent="rent_villa",
    transaction_type="RENT",
    property_type="VILLA",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "pool", "garden"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "pool": 9, "garden": 10},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

RENT_COMMERCIAL = QualificationMatrix(
    intent="rent_commercial",
    transaction_type="RENT",
    property_type="COMMERCIAL",
    required_fields=["city", "budget_max", "surface_sqm"],
    recommended_fields=["deadline", "property_condition"],
    optional_fields=["parking", "contact_phone", "furnished"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "property_condition": 5, "parking": 6, "contact_phone": 7, "furnished": 8},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

# ---------------------------------------------------------------------------
# Buy parcours
# ---------------------------------------------------------------------------

BUY_LAND = QualificationMatrix(
    intent="buy_land",
    transaction_type="BUY",
    property_type="LAND",
    required_fields=["city", "budget_max", "surface_sqm"],
    recommended_fields=["deadline", "zone_type"],
    optional_fields=["contact_phone", "electricity_access", "water_access", "road_access"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "zone_type": 5, "contact_phone": 6, "electricity_access": 7, "water_access": 8, "road_access": 9},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

BUY_HOUSE = QualificationMatrix(
    intent="buy_house",
    transaction_type="BUY",
    property_type="HOUSE",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "garden", "pool", "construction_year"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "garden": 9, "pool": 10, "construction_year": 11},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

BUY_APARTMENT = QualificationMatrix(
    intent="buy_apartment",
    transaction_type="BUY",
    property_type="APARTMENT",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "floor", "furnished", "parking", "construction_year"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "floor": 7, "furnished": 8, "parking": 9, "construction_year": 10},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

BUY_VILLA = QualificationMatrix(
    intent="buy_villa",
    transaction_type="BUY",
    property_type="VILLA",
    required_fields=["city", "budget_max"],
    recommended_fields=["bedroom_count", "surface_sqm", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "pool", "garden", "construction_year"],
    field_priority={"city": 1, "budget_max": 2, "bedroom_count": 3, "surface_sqm": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "pool": 9, "garden": 10, "construction_year": 11},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "bedroom_count": "non_negative_integer", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "bedroom_count": "ask_bedroom_count", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

BUY_COMMERCIAL = QualificationMatrix(
    intent="buy_commercial",
    transaction_type="BUY",
    property_type="COMMERCIAL",
    required_fields=["city", "budget_max", "surface_sqm"],
    recommended_fields=["deadline", "property_condition"],
    optional_fields=["parking", "contact_phone", "floor"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "property_condition": 5, "parking": 6, "contact_phone": 7, "floor": 8},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

BUY_BUILDING = QualificationMatrix(
    intent="buy_building",
    transaction_type="BUY",
    property_type="BUILDING",
    required_fields=["city", "budget_max", "surface_sqm"],
    recommended_fields=["deadline", "floor_count", "construction_year"],
    optional_fields=["parking", "contact_phone", "elevator"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "floor_count": 5, "construction_year": 6, "parking": 7, "contact_phone": 8, "elevator": 9},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number", "floor_count": "non_negative_integer"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface", "floor_count": "ask_floor_count"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

# ---------------------------------------------------------------------------
# Sell parcours
# ---------------------------------------------------------------------------

SELL_LAND = QualificationMatrix(
    intent="sell_land",
    transaction_type="SELL",
    property_type="LAND",
    required_fields=["city", "surface_sqm"],
    recommended_fields=["expected_price", "deadline", "zone_type"],
    optional_fields=["contact_phone", "electricity_access", "water_access", "road_access", "title_deed"],
    field_priority={"city": 1, "surface_sqm": 2, "expected_price": 3, "deadline": 4, "zone_type": 5, "contact_phone": 6, "electricity_access": 7, "water_access": 8, "road_access": 9, "title_deed": 10},
    validation_rules={"city": "known_city", "surface_sqm": "positive_number", "expected_price": "positive_integer"},
    clarification_rules={"city": "ask_city", "surface_sqm": "ask_surface", "expected_price": "ask_expected_price"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

SELL_HOUSE = QualificationMatrix(
    intent="sell_house",
    transaction_type="SELL",
    property_type="HOUSE",
    required_fields=["city", "surface_sqm"],
    recommended_fields=["expected_price", "bedroom_count", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "garden", "pool", "construction_year", "title_deed"],
    field_priority={"city": 1, "surface_sqm": 2, "expected_price": 3, "bedroom_count": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "garden": 9, "pool": 10, "construction_year": 11, "title_deed": 12},
    validation_rules={"city": "known_city", "surface_sqm": "positive_number", "expected_price": "positive_integer", "bedroom_count": "non_negative_integer"},
    clarification_rules={"city": "ask_city", "surface_sqm": "ask_surface", "expected_price": "ask_expected_price", "bedroom_count": "ask_bedroom_count"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

SELL_APARTMENT = QualificationMatrix(
    intent="sell_apartment",
    transaction_type="SELL",
    property_type="APARTMENT",
    required_fields=["city", "surface_sqm"],
    recommended_fields=["expected_price", "bedroom_count", "deadline"],
    optional_fields=["bathroom_count", "floor", "furnished", "parking", "construction_year", "title_deed"],
    field_priority={"city": 1, "surface_sqm": 2, "expected_price": 3, "bedroom_count": 4, "deadline": 5, "bathroom_count": 6, "floor": 7, "furnished": 8, "parking": 9, "construction_year": 10, "title_deed": 11},
    validation_rules={"city": "known_city", "surface_sqm": "positive_number", "expected_price": "positive_integer", "bedroom_count": "non_negative_integer"},
    clarification_rules={"city": "ask_city", "surface_sqm": "ask_surface", "expected_price": "ask_expected_price", "bedroom_count": "ask_bedroom_count"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

SELL_PROPERTY = QualificationMatrix(
    intent="sell_property",
    transaction_type="SELL",
    property_type="PROPERTY",
    required_fields=["city", "surface_sqm", "property_type_detail"],
    recommended_fields=["expected_price", "bedroom_count", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "construction_year", "title_deed"],
    field_priority={"city": 1, "surface_sqm": 2, "property_type_detail": 3, "expected_price": 4, "bedroom_count": 5, "deadline": 6, "bathroom_count": 7, "furnished": 8, "parking": 9, "construction_year": 10, "title_deed": 11},
    validation_rules={"city": "known_city", "surface_sqm": "positive_number", "expected_price": "positive_integer", "bedroom_count": "non_negative_integer"},
    clarification_rules={"city": "ask_city", "surface_sqm": "ask_surface", "expected_price": "ask_expected_price"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

# ---------------------------------------------------------------------------
# Rent out (mettre en location)
# ---------------------------------------------------------------------------

RENT_OUT = QualificationMatrix(
    intent="rent_out",
    transaction_type="RENT_OUT",
    property_type="PROPERTY",
    required_fields=["city", "surface_sqm"],
    recommended_fields=["expected_rent", "bedroom_count", "deadline"],
    optional_fields=["bathroom_count", "furnished", "parking", "availability_date", "contact_phone"],
    field_priority={"city": 1, "surface_sqm": 2, "expected_rent": 3, "bedroom_count": 4, "deadline": 5, "bathroom_count": 6, "furnished": 7, "parking": 8, "availability_date": 9, "contact_phone": 10},
    validation_rules={"city": "known_city", "surface_sqm": "positive_number", "expected_rent": "positive_integer", "bedroom_count": "non_negative_integer"},
    clarification_rules={"city": "ask_city", "surface_sqm": "ask_surface", "expected_rent": "ask_expected_rent"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP"],
)

# ---------------------------------------------------------------------------
# Construct / Renovate / Invest
# ---------------------------------------------------------------------------

CONSTRUCT = QualificationMatrix(
    intent="construct",
    transaction_type="CONSTRUCT",
    property_type="PROPERTY",
    required_fields=["city", "budget_max", "surface_sqm"],
    recommended_fields=["deadline", "property_type_detail"],
    optional_fields=["bedroom_count", "bathroom_count", "floor_count", "contact_phone", "architect_required"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "property_type_detail": 5, "bedroom_count": 6, "bathroom_count": 7, "floor_count": 8, "contact_phone": 9, "architect_required": 10},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

RENOVATE = QualificationMatrix(
    intent="renovate",
    transaction_type="RENOVATE",
    property_type="PROPERTY",
    required_fields=["city", "budget_max"],
    recommended_fields=["surface_sqm", "deadline", "property_type_detail"],
    optional_fields=["renovation_type", "contact_phone", "urgent"],
    field_priority={"city": 1, "budget_max": 2, "surface_sqm": 3, "deadline": 4, "property_type_detail": 5, "renovation_type": 6, "contact_phone": 7, "urgent": 8},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "surface_sqm": "positive_number"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "surface_sqm": "ask_surface"},
    readiness_threshold=0.6,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

INVEST = QualificationMatrix(
    intent="invest",
    transaction_type="INVEST",
    property_type="PROPERTY",
    required_fields=["city", "budget_max"],
    recommended_fields=["expected_roi", "deadline", "property_type_detail"],
    optional_fields=["surface_sqm", "contact_phone", "risk_profile", "investment_horizon"],
    field_priority={"city": 1, "budget_max": 2, "expected_roi": 3, "deadline": 4, "property_type_detail": 5, "surface_sqm": 6, "contact_phone": 7, "risk_profile": 8, "investment_horizon": 9},
    validation_rules={"budget_max": "positive_integer", "city": "known_city", "expected_roi": "percentage"},
    clarification_rules={"city": "ask_city", "budget_max": "ask_budget", "expected_roi": "ask_expected_roi"},
    readiness_threshold=0.5,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "INFORMATION"],
)

# ---------------------------------------------------------------------------
# Find professional parcours
# ---------------------------------------------------------------------------

FIND_ARCHITECT = QualificationMatrix(
    intent="find_architect",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline", "budget_max"],
    optional_fields=["contact_phone", "project_description", "language"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "budget_max": 4, "contact_phone": 5, "project_description": 6, "language": 7},
    validation_rules={"city": "known_city", "budget_max": "positive_integer"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty", "deadline": "ask_deadline"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_ENGINEER = QualificationMatrix(
    intent="find_engineer",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline", "budget_max"],
    optional_fields=["contact_phone", "project_description", "language"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "budget_max": 4, "contact_phone": 5, "project_description": 6, "language": 7},
    validation_rules={"city": "known_city", "budget_max": "positive_integer"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty", "deadline": "ask_deadline"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_TECHNICIAN = QualificationMatrix(
    intent="find_technician",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline", "budget_max"],
    optional_fields=["contact_phone", "project_description", "language"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "budget_max": 4, "contact_phone": 5, "project_description": 6, "language": 7},
    validation_rules={"city": "known_city", "budget_max": "positive_integer"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty", "deadline": "ask_deadline"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_NOTARY = QualificationMatrix(
    intent="find_notary",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["deadline", "service_type"],
    optional_fields=["contact_phone", "language", "budget_max"],
    field_priority={"city": 1, "deadline": 2, "service_type": 3, "contact_phone": 4, "language": 5, "budget_max": 6},
    validation_rules={"city": "known_city"},
    clarification_rules={"city": "ask_city", "service_type": "ask_service_type"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_AGENT = QualificationMatrix(
    intent="find_agent",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline"],
    optional_fields=["contact_phone", "language", "budget_max", "experience_years"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "contact_phone": 4, "language": 5, "budget_max": 6, "experience_years": 7},
    validation_rules={"city": "known_city"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_CONTRACTOR = QualificationMatrix(
    intent="find_contractor",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline", "budget_max"],
    optional_fields=["contact_phone", "project_description", "language", "project_scale"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "budget_max": 4, "contact_phone": 5, "project_description": 6, "language": 7, "project_scale": 8},
    validation_rules={"city": "known_city", "budget_max": "positive_integer"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty", "deadline": "ask_deadline"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

FIND_LAWYER = QualificationMatrix(
    intent="find_lawyer",
    transaction_type="FIND",
    property_type="PROPERTY",
    required_fields=["city"],
    recommended_fields=["specialty", "deadline"],
    optional_fields=["contact_phone", "language", "budget_max", "experience_years"],
    field_priority={"city": 1, "specialty": 2, "deadline": 3, "contact_phone": 4, "language": 5, "budget_max": 6, "experience_years": 7},
    validation_rules={"city": "known_city"},
    clarification_rules={"city": "ask_city", "specialty": "ask_specialty"},
    readiness_threshold=0.4,
    allowed_actions=["SEARCH", "MATCH", "RELATIONSHIP", "CONTACT"],
)

# ---------------------------------------------------------------------------
# Master list and index
# ---------------------------------------------------------------------------

ALL_MATRICES: list[QualificationMatrix] = [
    RENT_STUDIO,
    RENT_ROOM,
    RENT_APARTMENT,
    RENT_HOUSE,
    RENT_VILLA,
    RENT_COMMERCIAL,
    BUY_LAND,
    BUY_HOUSE,
    BUY_APARTMENT,
    BUY_VILLA,
    BUY_COMMERCIAL,
    BUY_BUILDING,
    SELL_LAND,
    SELL_HOUSE,
    SELL_APARTMENT,
    SELL_PROPERTY,
    RENT_OUT,
    CONSTRUCT,
    RENOVATE,
    INVEST,
    FIND_ARCHITECT,
    FIND_ENGINEER,
    FIND_TECHNICIAN,
    FIND_NOTARY,
    FIND_AGENT,
    FIND_CONTRACTOR,
    FIND_LAWYER,
]

MATRIX_INDEX: dict[str, list[QualificationMatrix]] = {}
for _m in ALL_MATRICES:
    MATRIX_INDEX.setdefault(_m.intent, []).append(_m)


def get_matrix(intent: str, transaction_type: str | None = None, property_type: str | None = None) -> QualificationMatrix | None:
    candidates = MATRIX_INDEX.get(intent, [])
    if not candidates:
        return None
    if transaction_type is None and property_type is None:
        return candidates[0]
    for m in candidates:
        if transaction_type is not None and m.transaction_type != transaction_type:
            continue
        if property_type is not None and m.property_type != property_type:
            continue
        return m
    return None


def get_next_field(matrix: QualificationMatrix, known_facts: dict[str, Any]) -> str | None:
    all_ordered = sorted(matrix.all_fields, key=lambda f: matrix.get_field_priority(f))
    for field in all_ordered:
        if field not in known_facts:
            return field
    return None


def get_readiness_score(matrix: QualificationMatrix, known_facts: dict[str, Any]) -> float:
    if not matrix.total_field_count:
        return 0.0
    required_known = sum(1 for f in matrix.required_fields if f in known_facts)
    recommended_known = sum(1 for f in matrix.recommended_fields if f in known_facts)
    optional_known = sum(1 for f in matrix.optional_fields if f in known_facts)
    total_required = len(matrix.required_fields)
    total_recommended = len(matrix.recommended_fields)
    total_optional = len(matrix.optional_fields)
    required_weight = 3.0
    recommended_weight = 1.5
    optional_weight = 0.5
    total_possible = (total_required * required_weight) + (total_recommended * recommended_weight) + (total_optional * optional_weight)
    if total_possible == 0:
        return 1.0
    actual = (required_known * required_weight) + (recommended_known * recommended_weight) + (optional_known * optional_weight)
    score = actual / total_possible
    if total_required > 0:
        required_ratio = required_known / total_required
        if required_ratio < 0.5:
            score *= required_ratio * 2
    return min(max(score, 0.0), 1.0)
