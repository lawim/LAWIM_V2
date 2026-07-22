from __future__ import annotations
from .definitions import FieldDefinition, ValueType, MergeStrategy, ConflictStrategy
from .registry import FieldRegistry


def register_all_fields(registry: FieldRegistry) -> None:
    fields = [
        FieldDefinition(field_name="intent", canonical_name="intent", value_type=ValueType.STRING, required=True, priority=1, description="User's primary intent", merge_strategy=MergeStrategy.KEEP_EXISTING, conflict_strategy=ConflictStrategy.USE_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="transaction_type", canonical_name="transaction_type", aliases=("type_transaction",), value_type=ValueType.ENUM, required=True, priority=2, allowed_values=("RENT", "BUY", "SELL", "LIST", "PUBLISH"), description="Type of transaction", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="property_type", canonical_name="property_type", aliases=("type_bien", "bien"), value_type=ValueType.ENUM, required=True, priority=3, allowed_values=("APARTMENT", "STUDIO", "HOUSE", "VILLA", "LAND", "COMMERCIAL", "OFFICE", "WAREHOUSE"), description="Type of property", normalizer="property_type", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="city", canonical_name="city", aliases=("ville",), value_type=ValueType.STRING, required=True, priority=4, description="City of the property", normalizer="city", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE, minimum_confidence=0.6),
        FieldDefinition(field_name="district", canonical_name="district", aliases=("quartier", "neighborhood"), value_type=ValueType.STRING, required=False, priority=5, description="District or neighborhood", normalizer="district", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="districts", canonical_name="districts", aliases=("quartiers",), value_type=ValueType.LIST, required=False, priority=6, description="List of acceptable districts", merge_strategy=MergeStrategy.APPEND_UNIQUE),

        FieldDefinition(field_name="budget_min", canonical_name="budget_min", aliases=("budget minimum",), value_type=ValueType.MONEY, required=False, priority=10, description="Minimum budget", normalizer="money", merge_strategy=MergeStrategy.MAX_VALUE),
        FieldDefinition(field_name="budget_max", canonical_name="budget_max", aliases=("budget", "budget maximum"), value_type=ValueType.MONEY, required=True, priority=11, description="Maximum budget", normalizer="money", merge_strategy=MergeStrategy.MIN_VALUE, minimum_confidence=0.5),
        FieldDefinition(field_name="currency", canonical_name="currency", aliases=("devise",), value_type=ValueType.ENUM, required=True, priority=12, allowed_values=("XAF", "EUR", "USD"), default_value="XAF", description="Currency", merge_strategy=MergeStrategy.KEEP_EXISTING),

        FieldDefinition(field_name="bedrooms", canonical_name="bedrooms", aliases=("chambres", "bedroom_count", "nb_chambres"), value_type=ValueType.INTEGER, required=False, priority=20, description="Number of bedrooms", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="bathrooms", canonical_name="bathrooms", aliases=("salles de bain", "douches", "sdb"), value_type=ValueType.INTEGER, required=False, priority=21, description="Number of bathrooms", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="surface_min", canonical_name="surface_min", aliases=("surface minimum", "min surface"), value_type=ValueType.SURFACE, required=False, priority=22, description="Minimum surface area", normalizer="surface", merge_strategy=MergeStrategy.MAX_VALUE),
        FieldDefinition(field_name="surface_max", canonical_name="surface_max", aliases=("surface", "surface maximum"), value_type=ValueType.SURFACE, required=False, priority=23, description="Maximum surface area", normalizer="surface", merge_strategy=MergeStrategy.MIN_VALUE),
        FieldDefinition(field_name="furnished", canonical_name="furnished", aliases=("meubl\u00e9", "meuble"), value_type=ValueType.BOOLEAN, required=False, priority=24, description="Whether the property is furnished", normalizer="boolean", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="parking", canonical_name="parking", value_type=ValueType.BOOLEAN, required=False, priority=25, description="Parking availability", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="move_in_date", canonical_name="move_in_date", aliases=("date entr\u00e9e", "entry date", "emm\u00e9nagement"), value_type=ValueType.PERIOD, required=False, priority=30, description="Desired move-in date or period", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="visit_availability", canonical_name="visit_availability", aliases=("disponibilit\u00e9 visite", "visit date"), value_type=ValueType.PERIOD, required=False, priority=31, description="When the user is available for a visit", merge_strategy=MergeStrategy.REPLACE_IF_NEWER),
        FieldDefinition(field_name="urgency", canonical_name="urgency", aliases=("urgence",), value_type=ValueType.ENUM, required=False, priority=32, allowed_values=("LOW", "MEDIUM", "HIGH", "URGENT"), description="Urgency level", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="purchase_timeline", canonical_name="purchase_timeline", aliases=("d\u00e9lai achat",), value_type=ValueType.STRING, required=False, priority=33, description="Purchase timeline preference", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="lease_duration", canonical_name="lease_duration", aliases=("dur\u00e9e bail",), value_type=ValueType.STRING, required=False, priority=34, description="Lease duration preference", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="asking_price", canonical_name="asking_price", aliases=("prix demande", "prix vente"), value_type=ValueType.MONEY, required=False, priority=40, description="Asking price for sale", normalizer="money", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="occupancy_status", canonical_name="occupancy_status", aliases=("statut occupation",), value_type=ValueType.ENUM, required=False, priority=41, allowed_values=("OCCUPIED", "VACANT", "TENANTED"), description="Current occupancy status", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="property_condition", canonical_name="property_condition", aliases=("\u00e9tat bien",), value_type=ValueType.ENUM, required=False, priority=42, allowed_values=("NEW", "GOOD", "FAIR", "NEEDS_RENOVATION"), description="Property condition", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="media_available", canonical_name="media_available", value_type=ValueType.BOOLEAN, required=False, priority=43, description="Whether media/photos are available", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="sale_urgency", canonical_name="sale_urgency", aliases=("urgence vente",), value_type=ValueType.ENUM, required=False, priority=44, allowed_values=("LOW", "MEDIUM", "HIGH"), description="Sale urgency", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="land_area", canonical_name="land_area", aliases=("superficie terrain",), value_type=ValueType.SURFACE, required=False, priority=50, description="Land area in m\u00b2", normalizer="surface", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="land_use", canonical_name="land_use", aliases=("usage terrain",), value_type=ValueType.ENUM, required=False, priority=51, allowed_values=("RESIDENTIAL", "COMMERCIAL", "AGRICULTURAL", "MIXED"), description="Intended land use", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="ownership_document", canonical_name="ownership_document", aliases=("titre foncier", "document propri\u00e9t\u00e9"), value_type=ValueType.STRING, required=False, priority=52, description="Type of ownership document available", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="financing_required", canonical_name="financing_required", aliases=("financement",), value_type=ValueType.BOOLEAN, required=False, priority=53, description="Whether financing is needed", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="construction_type", canonical_name="construction_type", value_type=ValueType.ENUM, required=False, priority=60, allowed_values=("NEW", "EXTENSION", "RENOVATION"), description="Type of construction project", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="estimated_surface", canonical_name="estimated_surface", value_type=ValueType.SURFACE, required=False, priority=61, description="Estimated construction surface", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="floors", canonical_name="floors", value_type=ValueType.INTEGER, required=False, priority=62, description="Number of floors", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="construction_budget", canonical_name="construction_budget", value_type=ValueType.MONEY, required=False, priority=63, description="Construction budget", normalizer="money", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="desired_start_date", canonical_name="desired_start_date", value_type=ValueType.PERIOD, required=False, priority=64, description="Desired construction start date", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="desired_completion_date", canonical_name="desired_completion_date", value_type=ValueType.PERIOD, required=False, priority=65, description="Desired completion date", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="permit_status", canonical_name="permit_status", value_type=ValueType.ENUM, required=False, priority=66, allowed_values=("OBTAINED", "IN_PROGRESS", "NOT_STARTED"), description="Building permit status", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="investment_type", canonical_name="investment_type", value_type=ValueType.ENUM, required=False, priority=70, allowed_values=("PURCHASE", "CONSTRUCTION", "RENOVATION"), description="Type of investment", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="investment_budget", canonical_name="investment_budget", value_type=ValueType.MONEY, required=False, priority=71, description="Investment budget", normalizer="money", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="target_return", canonical_name="target_return", value_type=ValueType.STRING, required=False, priority=72, description="Target return expectation", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="investment_horizon", canonical_name="investment_horizon", aliases=("horizon",), value_type=ValueType.STRING, required=False, priority=73, description="Investment time horizon", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="risk_tolerance", canonical_name="risk_tolerance", value_type=ValueType.ENUM, required=False, priority=74, allowed_values=("LOW", "MEDIUM", "HIGH"), description="Risk tolerance", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="management_preference", canonical_name="management_preference", value_type=ValueType.STRING, required=False, priority=75, description="Property management preference", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),

        FieldDefinition(field_name="asset_type", canonical_name="asset_type", value_type=ValueType.ENUM, required=False, priority=80, allowed_values=("PROPERTY", "LAND", "CONSTRUCTION"), description="Type of asset to verify", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="verification_type", canonical_name="verification_type", value_type=ValueType.ENUM, required=False, priority=81, allowed_values=("TITLE", "OWNERSHIP", "CONFORMITY", "DEBT"), description="Type of verification", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="document_types", canonical_name="document_types", value_type=ValueType.LIST, required=False, priority=82, description="Required document types", merge_strategy=MergeStrategy.APPEND_UNIQUE),
        FieldDefinition(field_name="owner_identity_status", canonical_name="owner_identity_status", value_type=ValueType.ENUM, required=False, priority=83, allowed_values=("VERIFIED", "PENDING", "UNVERIFIED"), description="Owner identity verification status", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
        FieldDefinition(field_name="verification_urgency", canonical_name="verification_urgency", value_type=ValueType.ENUM, required=False, priority=84, allowed_values=("LOW", "MEDIUM", "HIGH", "URGENT"), description="Verification urgency", merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE),
    ]

    for field in fields:
        try:
            registry.register_field(field)
        except Exception:
            pass

    registry.register_profile_fields("RENTAL_SEARCH", ["intent", "transaction_type", "property_type", "city", "districts", "budget_min", "budget_max", "currency", "bedrooms", "bathrooms", "move_in_date", "furnished", "parking", "visit_availability", "lease_duration", "urgency"])
    registry.register_profile_fields("PURCHASE_SEARCH", ["intent", "transaction_type", "property_type", "city", "districts", "budget_min", "budget_max", "currency", "bedrooms", "bathrooms", "surface_min", "surface_max", "ownership_document", "financing_required", "purchase_timeline", "visit_availability", "urgency"])
    registry.register_profile_fields("SALE_PROJECT", ["property_type", "city", "district", "surface", "bedrooms", "bathrooms", "ownership_document", "asking_price", "currency", "occupancy_status", "property_condition", "media_available", "sale_urgency"])
    registry.register_profile_fields("LAND_PROJECT", ["city", "district", "land_area", "land_use", "ownership_document", "asking_price", "currency"])
    registry.register_profile_fields("CONSTRUCTION_PROJECT", ["city", "construction_type", "estimated_surface", "floors", "construction_budget", "currency", "desired_start_date", "desired_completion_date", "permit_status"])


def create_default_registry() -> FieldRegistry:
    registry = FieldRegistry()
    register_all_fields(registry)
    return registry
