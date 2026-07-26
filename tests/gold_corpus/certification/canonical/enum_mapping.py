"""Canonical enum mappings — explicit conversion tables for all enum fields."""

# Intent mapping
INTENT_MAP = {
    "search_property": "property_search",
    "property_search": "property_search",
    "rental_search": "property_search",
    "purchase_search": "property_search",
    "SEARCH_PROPERTY": "property_search",
    "visit_scheduling": "visit_scheduling",
    "visit_request": "visit_scheduling",
    "create_case": "create_case",
    "case_creation": "create_case",
}

# Phase/status mapping
PHASE_MAP = {
    "initial": "initial",
    "STARTED": "initial",
    "in_progress": "qualifying",
    "QUALIFYING": "qualifying",
    "qualified": "qualified",
    "READY_FOR_ACTION": "qualified",
    "unqualified": "unqualified",
    "completed": "completed",
    "ACTION_COMPLETED": "completed",
    "handover": "handover",
    "error": "error",
}

# Pending user action mapping
PENDING_ACTION_MAP = {
    "NONE": "none",
    "ASK_BUDGET": "ask_budget",
    "ASK_BEDROOMS": "ask_bedrooms",
    "ASK_AREAS": "ask_areas",
    "ASK_CITY": "ask_city",
    "ASK_PROPERTY_TYPE": "ask_property_type",
    "ASK_TRANSACTION": "ask_transaction",
    "ASK_MOVE_IN_DATE": "ask_move_in_date",
    "CONFIRM_FIELD_VALUE": "confirm_field_value",
    "CONFIRM_QUALIFICATION": "confirm_qualification",
    "CONFIRM_CREATION": "confirm_creation",
    "search": "search",
    "CREATE_SEARCH_REQUEST": "create_search_request",
    "search_request_created": "create_search_request",
}

# Business action mapping
BUSINESS_ACTION_MAP = {
    "none": "none",
    "NONE": "none",
    "search": "search",
    "create_search_request": "create_search_request",
    "CREATE_SEARCH_REQUEST": "create_search_request",
    "qualify": "qualify",
    "qualification": "qualify",
    "cancel": "cancel",
    "create": "create",
    "schedule_visit": "schedule_visit",
    "visit_scheduling": "schedule_visit",
}

# Language mapping
LANGUAGE_MAP = {
    "fr": "fr",
    "en": "en",
    "pcm": "pcm",
    "english": "en",
    "francais": "fr",
}

# Question semantic types
QUESTION_TYPE_MAP = {
    "ask_budget": "ASK_BUDGET",
    "ask_bedrooms": "ASK_BEDROOMS",
    "ask_areas": "ASK_AREAS",
    "ask_city": "ASK_CITY",
    "ask_property_type": "ASK_PROPERTY_TYPE",
    "ask_transaction": "ASK_TRANSACTION",
    "ask_move_in_date": "ASK_MOVE_IN_DATE",
    "confirm_field": "CONFIRM_FIELD",
    "confirm_qualification": "CONFIRM_QUALIFICATION",
    "confirm_creation": "CONFIRM_CREATION",
    "clarify": "CLARIFY",
    "acknowledge": "ACKNOWLEDGE",
}


def map_value(mapping: dict, source_value: str, default: str = "unknown") -> str:
    """Map a value through an explicit mapping table."""
    if source_value is None:
        return default
    return mapping.get(str(source_value), default)
