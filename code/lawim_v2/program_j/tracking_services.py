from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any

from .tracking_models import (
    AttributionModel,
    AttributionTouchpoint,
    CampaignStatus,
    ConversionEvent,
    ExternalCampaign,
    ExternalChannelCode,
    ExternalPublication,
    LeadAttribution,
    LeadSource,
    PublicationStatus,
    RedirectLog,
    TouchpointType,
    channel_code_from_source,
    generate_tracking_code,
    parse_tracking_code,
)


class TrackingResolutionService:
    def validate_tracking_code(self, code: str) -> bool:
        if not code:
            return False
        return bool(re.match(r"^[A-Z]{2}-LAWIM-\d{6}-\d{4}-\d{2}-\d{3}$", code))

    def parse(self, code: str) -> dict[str, Any] | None:
        return parse_tracking_code(code)

    def resolve_publication(self, code: str, publications: list[ExternalPublication]) -> ExternalPublication | None:
        parsed = self.parse(code)
        if parsed is None:
            return None
        pub_id = parsed["publication_id"]
        for p in publications:
            pd = getattr(p, "publication_id", None)
            if pd is not None:
                try:
                    if int(pd) == pub_id:
                        return p
                except (ValueError, TypeError):
                    continue
        return None

    def resolve_campaign(self, code: str, publications: list[ExternalPublication],
                          campaigns: list[ExternalCampaign]) -> ExternalCampaign | None:
        pub = self.resolve_publication(code, publications)
        if pub is None or not pub.campaign_id:
            return None
        for c in campaigns:
            if c.campaign_id == pub.campaign_id:
                return c
        return None

    def generate(self, channel: str, publication_seq: int, sequence: int = 1) -> str:
        try:
            code = ExternalChannelCode(channel).value
        except ValueError:
            code = channel_code_from_source(channel).value
        return generate_tracking_code(code, publication_seq, sequence=sequence)


class TouchpointIngestionService:
    def create_deduplication_key(self, touchpoint_type: str, subject_id: str,
                                  occurred_at: str, channel: str) -> str:
        raw = f"{touchpoint_type}:{subject_id}:{occurred_at}:{channel}"
        import hashlib
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def normalize_redirect(self, redirect: RedirectLog) -> AttributionTouchpoint:
        now = datetime.now(timezone.utc).isoformat()
        return AttributionTouchpoint(
            touchpoint_id=str(uuid.uuid4()),
            subject_id=redirect.anonymous_subject_id or str(redirect.user_id or ""),
            user_id=redirect.user_id,
            anonymous_session_id=redirect.session_id,
            conversation_id=redirect.conversation_id,
            channel=ExternalChannelCode.OTHER.value,
            tracking_code=redirect.tracking_code,
            touchpoint_type=TouchpointType.REDIRECT,
            occurred_at=redirect.occurred_at or now,
            correlation_id=redirect.correlation_id,
            deduplication_key=self.create_deduplication_key("REDIRECT",
                redirect.anonymous_subject_id or str(redirect.user_id or ""),
                redirect.occurred_at or now, ""),
        )

    def create_touchpoint(self, tp_type: TouchpointType, subject_id: str,
                           channel: str = "", tracking_code: str = "",
                           occurred_at: str | None = None) -> AttributionTouchpoint:
        now = datetime.now(timezone.utc).isoformat()
        ts = occurred_at or now
        return AttributionTouchpoint(
            touchpoint_id=str(uuid.uuid4()),
            subject_id=subject_id,
            channel=channel or ExternalChannelCode.OTHER.value,
            tracking_code=tracking_code,
            touchpoint_type=tp_type,
            occurred_at=ts,
            deduplication_key=self.create_deduplication_key(tp_type.value, subject_id, ts, channel),
        )

    def ingest(self, touchpoint: AttributionTouchpoint) -> AttributionTouchpoint:
        return touchpoint


class AttributionEngine:
    def __init__(self, window_days: int = 30):
        self._window_days = window_days

    def _within_window(self, tp: AttributionTouchpoint, conversion: ConversionEvent) -> bool:
        from datetime import datetime, timedelta, timezone
        try:
            tp_dt = datetime.fromisoformat(tp.occurred_at)
            conv_dt = datetime.fromisoformat(conversion.occurred_at)
        except (ValueError, TypeError):
            return True
        delta = conv_dt - tp_dt
        return timedelta(0) <= delta <= timedelta(days=self._window_days)

    def first_touch(self, touchpoints: list[AttributionTouchpoint],
                     conversion: ConversionEvent) -> AttributionTouchpoint | None:
        valid = [tp for tp in touchpoints if self._within_window(tp, conversion)]
        if not valid:
            return None
        return min(valid, key=lambda tp: tp.occurred_at)

    def last_touch(self, touchpoints: list[AttributionTouchpoint],
                    conversion: ConversionEvent) -> AttributionTouchpoint | None:
        valid = [tp for tp in touchpoints if self._within_window(tp, conversion)]
        if not valid:
            return None
        return max(valid, key=lambda tp: tp.occurred_at)

    def multi_touch(self, touchpoints: list[AttributionTouchpoint],
                     conversion: ConversionEvent) -> dict[str, float]:
        valid = [tp for tp in touchpoints if self._within_window(tp, conversion)]
        if not valid:
            return {}
        weight = 1.0 / len(valid)
        return {tp.touchpoint_id: weight for tp in valid}

    def lawim_attribution(self, touchpoints: list[AttributionTouchpoint],
                           conversion: ConversionEvent) -> dict[str, Any]:
        valid = [tp for tp in touchpoints if self._within_window(tp, conversion)]
        if not valid:
            return {"model": "LAWIM_ATTRIBUTION", "weights": {}, "explanation": "No touchpoints in window"}

        # LAWIM Attribution: weighted by touchpoint type proximity to conversion
        # Conversation/qualification touchpoints near conversion get highest weight
        # Channel/actor credit is distributed proportionally
        weights: dict[str, float] = {}
        total_score = 0.0
        type_weights = {
            TouchpointType.CONVERSION: 0.05,
            TouchpointType.PAYMENT: 0.05,
            TouchpointType.TRANSACTION: 0.05,
            TouchpointType.VISIT: 0.10,
            TouchpointType.MATCHING: 0.10,
            TouchpointType.QUALIFICATION: 0.10,
            TouchpointType.CONVERSATION_OPEN: 0.15,
            TouchpointType.ACCOUNT_CREATION: 0.10,
            TouchpointType.REDIRECT: 0.10,
            TouchpointType.CLICK: 0.08,
            TouchpointType.IMPRESSION: 0.02,
            TouchpointType.QR_SCAN: 0.10,
        }

        for tp in valid:
            score = type_weights.get(tp.touchpoint_type, 0.05)
            if tp.touchpoint_value > 0:
                score *= min(1.0 + tp.touchpoint_value / 1000000, 2.0)
            weights[tp.touchpoint_id] = score
            total_score += score

        if total_score > 0:
            weights = {k: v / total_score for k, v in weights.items()}

        best = max(weights, key=weights.get) if weights else None
        touchpoint_map = {tp.touchpoint_id: tp for tp in valid}
        best_tp = touchpoint_map.get(best) if best else None

        return {
            "model": "LAWIM_ATTRIBUTION",
            "weights": weights,
            "selected_touchpoint": best,
            "selected_touchpoint_type": best_tp.touchpoint_type.value if best_tp else "",
            "touchpoint_count": len(valid),
            "explanation": f"LAWIM attribution over {len(valid)} touchpoints, "
                          f"type-weighted and value-adjusted, best={best_tp.touchpoint_type.value if best_tp else 'none'}",
        }

    def calculate(self, model: AttributionModel, touchpoints: list[AttributionTouchpoint],
                   conversion: ConversionEvent) -> LeadAttribution:
        now = datetime.now(timezone.utc).isoformat()
        result = LeadAttribution(
            attribution_id=str(uuid.uuid4()),
            model=model,
            attribution_window_days=self._window_days,
            touchpoint_count=len(touchpoints),
            calculated_at=now,
            calculation_version="1.0",
        )

        if model == AttributionModel.FIRST_TOUCH:
            ft = self.first_touch(touchpoints, conversion)
            result.selected_first_touch = ft.touchpoint_id if ft else ""
            result.explanation = f"First touch: {ft.touchpoint_type.value if ft else 'none'} at {ft.occurred_at if ft else 'n/a'}"
        elif model == AttributionModel.LAST_TOUCH:
            lt = self.last_touch(touchpoints, conversion)
            result.selected_last_touch = lt.touchpoint_id if lt else ""
            result.explanation = f"Last touch: {lt.touchpoint_type.value if lt else 'none'} at {lt.occurred_at if lt else 'n/a'}"
        elif model == AttributionModel.MULTI_TOUCH:
            result.weights = self.multi_touch(touchpoints, conversion)
            result.explanation = f"Multi-touch: {len(result.weights)} touchpoints with equal weight {1.0/len(result.weights) if result.weights else 0}"
        elif model == AttributionModel.LAWIM_ATTRIBUTION:
            lawim = self.lawim_attribution(touchpoints, conversion)
            result.weights = lawim["weights"]
            result.explanation = lawim["explanation"]
            result.selected_first_touch = lawim.get("selected_touchpoint", "")

        return result

    def recalculate(self, attribution: LeadAttribution, touchpoints: list[AttributionTouchpoint],
                     conversion: ConversionEvent) -> LeadAttribution:
        import copy
        new_attribution = copy.deepcopy(attribution)
        result = self.calculate(attribution.model, touchpoints, conversion)
        new_attribution.weights = result.weights
        new_attribution.selected_first_touch = result.selected_first_touch
        new_attribution.selected_last_touch = result.selected_last_touch
        new_attribution.explanation = result.explanation
        new_attribution.calculated_at = datetime.now(timezone.utc).isoformat()
        return new_attribution


class ConversionLinkingService:
    def link_conversation(self, conversation_id: str, conversion: ConversionEvent) -> ConversionEvent:
        conversion.conversation_id = conversation_id
        return conversion

    def link_matching(self, matching_id: str, conversion: ConversionEvent) -> ConversionEvent:
        conversion.matching_id = matching_id
        return conversion

    def link_visit(self, visit_id: str, conversion: ConversionEvent) -> ConversionEvent:
        conversion.visit_id = visit_id
        return conversion

    def link_transaction(self, transaction_id: str, conversion: ConversionEvent) -> ConversionEvent:
        conversion.transaction_id = transaction_id
        return conversion

    def link_payment(self, payment_id: str, provider: str, amount: float,
                      currency: str, conversion: ConversionEvent) -> ConversionEvent:
        conversion.payment_id = payment_id
        conversion.payment_provider = provider
        conversion.monetary_value = amount
        conversion.currency = currency
        return conversion

    def finalize(self, conversion: ConversionEvent) -> ConversionEvent:
        conversion.deduplication_key = self._build_dedup_key(conversion)
        return conversion

    def is_duplicate(self, conversion: ConversionEvent, existing: list[ConversionEvent]) -> bool:
        key = self._build_dedup_key(conversion)
        for e in existing:
            if e.deduplication_key == key:
                return True
        return False

    def _build_dedup_key(self, conversion: ConversionEvent) -> str:
        parts = [conversion.conversation_id or "",
                 conversion.matching_id or "",
                 conversion.transaction_id or "",
                 conversion.payment_id or "",
                 conversion.conversion_type]
        raw = ":".join(parts)
        import hashlib
        return hashlib.sha256(raw.encode()).hexdigest()[:32]
