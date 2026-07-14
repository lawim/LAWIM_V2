from __future__ import annotations

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as mdto
from .engines import MarketplacePlatformEngine


class PartnerService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = MarketplacePlatformEngine()

    def list_registrations(self, *, status: str | None = None) -> list[dict[str, object]]:
        return self.repository.list_marketplace_partner_registrations(status=status)

    def get_registration(self, registration_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_partner_registration(registration_id)

    def create_registration(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_partner_registration(**kwargs)

    def approve_registration(self, registration_id: int, *, reviewer_id: int | None = None) -> dict[str, object]:
        return self.repository.approve_marketplace_partner_registration(registration_id, reviewer_id=reviewer_id)

    def qualify(self, registration_id: int) -> dict[str, object]:
        reg = self.repository.get_marketplace_partner_registration(registration_id)
        partner = None
        if reg.get("partner_profile_id"):
            partner = self.repository.one(
                "SELECT * FROM partner_profiles WHERE id = ?",
                (int(reg["partner_profile_id"]),),
            )
        return self.engine.partner_qualification.evaluate(registration=reg, partner=dict(partner) if partner else None)


class ProviderService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_providers(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_providers(**kwargs)

    def get_provider(self, provider_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_provider(provider_id)

    def get_bundle(self, provider_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_provider_bundle(provider_id)

    def create_provider(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_provider(**kwargs)

    def update_provider(self, provider_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.update_marketplace_provider(provider_id, **kwargs)


class CatalogService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = MarketplacePlatformEngine()

    def list_categories(self) -> list[dict[str, object]]:
        return self.repository.list_marketplace_catalog_categories()

    def list_items(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_catalog_items(**kwargs)

    def get_item(self, item_id: int) -> dict[str, object]:
        item = self.repository.get_marketplace_catalog_item(item_id)
        service = None
        if item.get("service_catalog_id"):
            try:
                service = self.repository.get_service_catalog_item(int(item["service_catalog_id"]))
            except Exception:
                service = None
        return self.engine.catalog.enrich_item(item=item, service_catalog=service)

    def create_item(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_catalog_item(**kwargs)


class RequestService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_requests(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_requests(**kwargs)

    def get_request(self, request_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_request(request_id)

    def create_request(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_request(**kwargs)

    def update_request(self, request_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.update_marketplace_request(request_id, **kwargs)

    def add_document(self, request_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.add_marketplace_request_document(request_id, **kwargs)


class QuoteService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = MarketplacePlatformEngine()

    def list_quotes(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_quotes(**kwargs)

    def get_quote(self, quote_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_quote(quote_id)

    def create_quote(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_quote(**kwargs)

    def send_quote(self, quote_id: int) -> dict[str, object]:
        return self.repository.send_marketplace_quote(quote_id)

    def accept_quote(self, quote_id: int) -> dict[str, object]:
        return self.repository.accept_marketplace_quote(quote_id)

    def validate_quote(self, quote_id: int) -> dict[str, object]:
        quote = self.repository.get_marketplace_quote(quote_id)
        return self.engine.quotes.validate_quote(quote=quote, lines=list(quote.get("lines") or []))


class ContractService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_contracts(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_contracts(**kwargs)

    def get_contract(self, contract_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_contract(contract_id)

    def create_from_quote(self, quote_id: int) -> dict[str, object]:
        return self.repository.create_marketplace_contract(quote_id=quote_id)

    def activate(self, contract_id: int) -> dict[str, object]:
        return self.repository.activate_marketplace_contract(contract_id)


class MissionService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_missions(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_missions(**kwargs)

    def get_mission(self, mission_id: int) -> dict[str, object]:
        return self.repository.get_marketplace_mission(mission_id)

    def update_mission(self, mission_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.update_marketplace_mission(mission_id, **kwargs)

    def add_deliverable(self, mission_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.add_marketplace_mission_deliverable(mission_id, **kwargs)


class ReviewService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_reviews(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_reviews(**kwargs)

    def create_review(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_review(**kwargs)

    def publish_review(self, review_id: int) -> dict[str, object]:
        return self.repository.publish_marketplace_review(review_id)

    def reputation(self, provider_id: int) -> dict[str, int]:
        return self.repository.get_marketplace_reputation(provider_id)


class RecommendationService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = MarketplacePlatformEngine()

    def list_recommendations(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_ai_recommendations(**kwargs)


class CommissionService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def compute(self, contract_id: int) -> dict[str, object]:
        return self.repository.compute_marketplace_commission(contract_id)

    def list_commissions(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_commissions(**kwargs)


class SubscriptionService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_plans(self) -> list[dict[str, object]]:
        return self.repository.list_marketplace_subscription_plans()

    def list_subscriptions(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_subscriptions(**kwargs)

    def subscribe(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_marketplace_subscription(**kwargs)


class DisputeService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_disputes(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_marketplace_disputes(**kwargs)

    def open_dispute(self, **kwargs: object) -> dict[str, object]:
        return self.repository.open_marketplace_dispute(**kwargs)

    def add_message(self, dispute_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.add_marketplace_dispute_message(dispute_id, **kwargs)

    def resolve(self, dispute_id: int, *, resolution: str) -> dict[str, object]:
        return self.repository.resolve_marketplace_dispute(dispute_id, resolution=resolution)


class AnalyticsService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def analytics(self) -> dict[str, object]:
        return self.repository.marketplace_analytics()

    def dashboard(self) -> dict[str, object]:
        return self.repository.marketplace_dashboard()

    def stats(self) -> dict[str, object]:
        return self.repository.marketplace_stats()

    def snapshot(self) -> dict[str, object]:
        return self.repository.snapshot_marketplace_analytics()


class MarketplaceService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy
        self.engine = MarketplacePlatformEngine()
        self.partners = PartnerService(repository)
        self.providers = ProviderService(repository)
        self.catalog = CatalogService(repository)
        self.requests = RequestService(repository)
        self.quotes = QuoteService(repository)
        self.contracts = ContractService(repository)
        self.missions = MissionService(repository)
        self.reviews = ReviewService(repository)
        self.recommendations = RecommendationService(repository)
        self.commissions = CommissionService(repository)
        self.subscriptions = SubscriptionService(repository)
        self.disputes = DisputeService(repository)
        self.analytics_service = AnalyticsService(repository)

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    # --- Partner registrations ---

    def list_partner_registrations(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_partner_list")
        METRICS.increment("partner_list")
        return {
            "registrations": [
                mdto.partner_registration_dto(r) for r in self.partners.list_registrations(status=status)
            ]
        }

    def create_partner_registration(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        reg = self.partners.create_registration(
            applicant_name=str(body["applicant_name"]),
            applicant_email=str(body.get("applicant_email") or ""),
            applicant_phone=str(body.get("applicant_phone") or ""),
            provider_type=str(body.get("provider_type") or "company"),
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
            service_categories=list(body.get("service_categories") or []),
        )
        METRICS.increment("marketplace_partner_created")
        METRICS.increment("partner_created")
        return {"registration": mdto.partner_registration_dto(reg)}

    def approve_partner_registration(self, *, actor: dict[str, object], registration_id: int) -> dict[str, object]:
        self._require_admin(actor)
        reviewer_id = int(actor["id"]) if actor.get("id") is not None else None
        reg = self.partners.approve_registration(registration_id, reviewer_id=reviewer_id)
        METRICS.increment("partner_approved")
        return {"registration": mdto.partner_registration_dto(reg)}

    def qualify_partner_registration(self, *, actor: dict[str, object], registration_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"qualification": self.partners.qualify(registration_id)}

    # --- Providers ---

    def list_providers(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_provider_list")
        METRICS.increment("provider_list")
        return {"providers": [mdto.provider_dto(r) for r in self.providers.list_providers(status=status)]}

    def get_provider(self, *, actor: dict[str, object], provider_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("provider_detail")
        return mdto.provider_bundle_dto(self.providers.get_bundle(provider_id))

    def create_provider(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        provider = self.providers.create_provider(
            partner_profile_id=int(body["partner_profile_id"]),
            provider_type=str(body.get("provider_type") or "company"),
            headline=str(body.get("headline") or ""),
            bio=str(body.get("bio") or ""),
        )
        METRICS.increment("marketplace_provider_created")
        METRICS.increment("provider_created")
        return {"provider": mdto.provider_dto(provider)}

    def update_provider(self, *, actor: dict[str, object], provider_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        provider = self.providers.update_provider(provider_id, **body)
        METRICS.increment("provider_updated")
        return {"provider": mdto.provider_dto(provider)}

    def provider_availability(self, *, actor: dict[str, object], provider_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"availability": [mdto.availability_dto(r) for r in self.repository.list_marketplace_availability(provider_id)]}

    def set_provider_availability(self, *, actor: dict[str, object], provider_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        slot = self.repository.set_marketplace_availability(
            provider_id,
            day_of_week=int(body["day_of_week"]),
            start_time=str(body.get("start_time") or "08:00"),
            end_time=str(body.get("end_time") or "18:00"),
        )
        return {"availability": mdto.availability_dto(slot)}

    def provider_portfolio(self, *, actor: dict[str, object], provider_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"portfolio": [mdto.portfolio_item_dto(r) for r in self.repository.list_marketplace_portfolio(provider_id)]}

    # --- Catalog ---

    def list_catalog_categories(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("catalog_list")
        return {"categories": [mdto.catalog_category_dto(r) for r in self.catalog.list_categories()]}

    def list_catalog_items(self, *, actor: dict[str, object], category: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_catalog_list")
        METRICS.increment("catalog_list")
        return {"items": [mdto.catalog_item_dto(r) for r in self.catalog.list_items(category=category, status="active")]}

    def get_catalog_item(self, *, actor: dict[str, object], item_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("catalog_detail")
        return {"item": mdto.catalog_item_dto(self.catalog.get_item(item_id))}

    def create_catalog_item(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        item = self.catalog.create_item(
            category_id=int(body["category_id"]),
            title=str(body["title"]),
            description=str(body.get("description") or ""),
            category=str(body.get("category") or "other"),
            service_catalog_id=int(body["service_catalog_id"]) if body.get("service_catalog_id") is not None else None,
            provider_profile_id=int(body["provider_profile_id"]) if body.get("provider_profile_id") is not None else None,
            price_min=int(body["price_min"]) if body.get("price_min") is not None else None,
            price_max=int(body["price_max"]) if body.get("price_max") is not None else None,
        )
        METRICS.increment("catalog_item_created")
        return {"item": mdto.catalog_item_dto(item)}

    # --- Service requests ---

    def list_requests(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_request_list")
        METRICS.increment("request_list")
        return {"requests": [mdto.service_request_dto(r) for r in self.requests.list_requests(status=status)]}

    def get_request(self, *, actor: dict[str, object], request_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("request_detail")
        return {"request": mdto.service_request_dto(self.requests.get_request(request_id))}

    def create_request(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        project_id = int(body["project_id"]) if body.get("project_id") is not None else None
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        req = self.requests.create_request(
            title=str(body["title"]),
            description=str(body.get("description") or ""),
            category=str(body.get("category") or "other"),
            city=str(body.get("city") or ""),
            region=str(body.get("region") or ""),
            budget_min=int(body["budget_min"]) if body.get("budget_min") is not None else None,
            budget_max=int(body["budget_max"]) if body.get("budget_max") is not None else None,
            user_id=user_id,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            project_id=project_id,
            property_id=int(body["property_id"]) if body.get("property_id") is not None else None,
            catalog_item_id=int(body["catalog_item_id"]) if body.get("catalog_item_id") is not None else None,
            status=str(body.get("status") or "submitted"),
            criteria=dict(body.get("criteria") or {}),
        )
        METRICS.increment("marketplace_request_created")
        METRICS.increment("request_created")
        METRICS.increment("service_request_created")
        return {"request": mdto.service_request_dto(req)}

    def update_request(self, *, actor: dict[str, object], request_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        req = self.requests.update_request(request_id, **body)
        METRICS.increment("request_updated")
        return {"request": mdto.service_request_dto(req)}

    # --- Quotes ---

    def list_quotes(self, *, actor: dict[str, object], request_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("quote_list")
        return {"quotes": [mdto.quote_dto(r) for r in self.quotes.list_quotes(request_id=request_id)]}

    def create_quote(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        quote = self.quotes.create_quote(
            request_id=int(body["request_id"]),
            provider_profile_id=int(body["provider_profile_id"]),
            lines=list(body.get("lines") or []),
            notes=str(body.get("notes") or ""),
        )
        METRICS.increment("marketplace_quote_created")
        METRICS.increment("quote_created")
        return {"quote": mdto.quote_dto(quote)}

    def send_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        self._require_auth(actor)
        quote = self.quotes.send_quote(quote_id)
        METRICS.increment("quote_sent")
        return {"quote": mdto.quote_dto(quote)}

    def accept_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        self._require_auth(actor)
        quote = self.quotes.accept_quote(quote_id)
        METRICS.increment("quote_accepted")
        return {"quote": mdto.quote_dto(quote)}

    # --- Contracts ---

    def list_contracts(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("contract_list")
        return {"contracts": [mdto.contract_dto(r) for r in self.contracts.list_contracts(status=status)]}

    def create_contract(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        contract = self.contracts.create_from_quote(int(body["quote_id"]))
        METRICS.increment("marketplace_contract_created")
        METRICS.increment("contract_created")
        return {"contract": mdto.contract_dto(contract)}

    def activate_contract(self, *, actor: dict[str, object], contract_id: int) -> dict[str, object]:
        self._require_auth(actor)
        contract = self.contracts.activate(contract_id)
        METRICS.increment("contract_activated")
        return {"contract": mdto.contract_dto(contract)}

    def prepare_payment(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        prep = self.repository.prepare_marketplace_payment(
            amount=int(body["amount"]),
            payment_method=str(body.get("payment_method") or "mobile_money"),
            contract_id=int(body["contract_id"]) if body.get("contract_id") is not None else None,
            subscription_id=int(body["subscription_id"]) if body.get("subscription_id") is not None else None,
        )
        return {"payment_preparation": mdto.payment_preparation_dto(prep)}

    # --- Missions ---

    def list_missions(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("mission_list")
        return {"missions": [mdto.mission_dto(r) for r in self.missions.list_missions(status=status)]}

    def get_mission(self, *, actor: dict[str, object], mission_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("mission_detail")
        return {"mission": mdto.mission_dto(self.missions.get_mission(mission_id))}

    def update_mission(self, *, actor: dict[str, object], mission_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        mission = self.missions.update_mission(mission_id, **body)
        METRICS.increment("mission_updated")
        return {"mission": mdto.mission_dto(mission)}

    # --- Reviews ---

    def list_reviews(self, *, actor: dict[str, object], provider_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("review_list")
        return {"reviews": [mdto.review_dto(r) for r in self.reviews.list_reviews(provider_id=provider_id, status="published")]}

    def create_review(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        review = self.reviews.create_review(
            provider_profile_id=int(body["provider_profile_id"]),
            rating=int(body.get("rating") or 5),
            title=str(body.get("title") or ""),
            body=str(body.get("body") or ""),
            mission_id=int(body["mission_id"]) if body.get("mission_id") is not None else None,
            user_id=user_id,
        )
        METRICS.increment("marketplace_review_created")
        METRICS.increment("review_created")
        METRICS.increment("rating_submitted")
        return {"review": mdto.review_dto(review)}

    def provider_reputation(self, *, actor: dict[str, object], provider_id: int) -> dict[str, object]:
        self._require_auth(actor)
        scores = self.reviews.reputation(provider_id)
        METRICS.increment("reputation_computed")
        return mdto.reputation_dto(scores)

    # --- Recommendations ---

    def list_recommendations(self, *, actor: dict[str, object], request_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("recommendation_list")
        return {
            "recommendations": [
                mdto.ai_recommendation_dto(r) for r in self.recommendations.list_recommendations(request_id=request_id)
            ]
        }

    # --- Commissions ---

    def list_commissions(self, *, actor: dict[str, object], contract_id: int | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("commission_list")
        return {"commissions": [mdto.commission_dto(r) for r in self.commissions.list_commissions(contract_id=contract_id)]}

    # --- Subscriptions ---

    def list_subscription_plans(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("subscription_plan_list")
        return {"plans": [mdto.subscription_plan_dto(r) for r in self.subscriptions.list_plans()]}

    def subscribe(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        sub = self.subscriptions.subscribe(
            plan_id=int(body["plan_id"]),
            provider_profile_id=int(body["provider_profile_id"]) if body.get("provider_profile_id") is not None else None,
            user_id=user_id,
        )
        METRICS.increment("marketplace_subscription_created")
        METRICS.increment("subscription_created")
        return {"subscription": mdto.subscription_dto(sub)}

    # --- Disputes ---

    def list_disputes(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("dispute_list")
        return {"disputes": [mdto.dispute_dto(r) for r in self.disputes.list_disputes(status=status)]}

    def open_dispute(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        dispute = self.disputes.open_dispute(
            contract_id=int(body["contract_id"]),
            reason=str(body.get("reason") or ""),
            mission_id=int(body["mission_id"]) if body.get("mission_id") is not None else None,
            opened_by_user_id=user_id,
        )
        METRICS.increment("marketplace_dispute_opened")
        METRICS.increment("dispute_opened")
        return {"dispute": mdto.dispute_dto(dispute)}

    def resolve_dispute(self, *, actor: dict[str, object], dispute_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        dispute = self.disputes.resolve(dispute_id, resolution=str(body.get("resolution") or ""))
        METRICS.increment("dispute_resolved")
        return {"dispute": mdto.dispute_dto(dispute)}

    # --- Analytics / Dashboard ---

    def analytics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_analytics")
        METRICS.increment("analytics_view")
        return mdto.analytics_dto(self.analytics_service.analytics())

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_dashboard")
        return mdto.dashboard_dto(self.analytics_service.dashboard())

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("marketplace_stats")
        return {"stats": self.analytics_service.stats()}

    def integration_sources(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        if actor is not None:
            self._require_auth(actor)
        return {"sources": self.engine.integration_sources(), "integrations": self.repository.marketplace_integrations()}

    def seed_catalog(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        self.repository.seed_marketplace_catalog()
        METRICS.increment("marketplace_catalog_seeded")
        return {"seeded": True}
