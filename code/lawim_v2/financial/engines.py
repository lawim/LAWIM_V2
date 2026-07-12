from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
import json
import re
from typing import Any

from ..errors import ValidationError
from .constants import (
    COMMISSION_STATUSES,
    INVOICE_STATUSES,
    PAYMENT_INTENT_STATUSES,
    PAYMENT_TRANSACTION_STATUSES,
    QUOTE_STATUSES,
    RECEIPT_STATUSES,
    REFUND_STATUSES,
    SUBSCRIPTION_CYCLE_STATUSES,
    SUBSCRIPTION_PLAN_FREQUENCIES,
    SUBSCRIPTION_STATUSES,
)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return fallback
    return parsed if parsed is not None else fallback


def _normalize_code(value: object, *, default: str = "") -> str:
    text = str(value or "").strip().upper()
    return text or default


def _minor_from_amount(amount: object, *, precision: int = 0) -> int:
    if amount is None or amount == "":
        return 0
    if isinstance(amount, int):
        return amount
    decimal_amount = Decimal(str(amount))
    multiplier = Decimal(10) ** precision
    return int((decimal_amount * multiplier).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _amount_from_minor(amount_minor: int, *, precision: int = 0) -> str:
    decimal_amount = Decimal(amount_minor) / (Decimal(10) ** precision)
    return format(decimal_amount, "f")


def _sanitize_reference(value: str | None) -> str:
    reference = re.sub(r"[^A-Z0-9_-]", "", (value or "").upper())
    return reference[:64]


def normalize_mobile_money_number(value: str) -> str:
    raw = re.sub(r"[\s().-]", "", (value or "").strip())
    if not raw:
        raise ValidationError("phone number is required")
    digits = re.sub(r"\D", "", raw)
    if raw.startswith("+"):
        digits = raw[1:]
    if digits.startswith("237"):
        digits = digits[3:]
    if len(digits) == 9 and digits.startswith("6"):
        return f"+237{digits}"
    if len(digits) == 12 and digits.startswith("2376"):
        return f"+{digits}"
    raise ValidationError("unsupported mobile money number format")


@dataclass(frozen=True, slots=True)
class PricingBreakdown:
    subtotal_minor: int
    discount_minor: int
    fee_minor: int
    tax_minor: int
    total_minor: int
    currency: str = "XAF"
    precision: int = 0
    source: str = "backend"
    context: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "subtotal_minor": self.subtotal_minor,
            "discount_minor": self.discount_minor,
            "fee_minor": self.fee_minor,
            "tax_minor": self.tax_minor,
            "total_minor": self.total_minor,
            "currency": self.currency,
            "precision": self.precision,
            "source": self.source,
            "context": self.context or {},
            "subtotal": _amount_from_minor(self.subtotal_minor, precision=self.precision),
            "discount": _amount_from_minor(self.discount_minor, precision=self.precision),
            "fee": _amount_from_minor(self.fee_minor, precision=self.precision),
            "tax": _amount_from_minor(self.tax_minor, precision=self.precision),
            "total": _amount_from_minor(self.total_minor, precision=self.precision),
        }


class FinancialPricingEngine:
    def round_minor(self, amount: object, *, precision: int = 0) -> int:
        return _minor_from_amount(amount, precision=precision)

    def normalize_currency(self, currency: str | None) -> str:
        return _normalize_code(currency, default="XAF")

    def normalize_mobile_money_number(self, value: str) -> str:
        return normalize_mobile_money_number(value)

    def calculate_breakdown(
        self,
        *,
        line_items: list[dict[str, object]] | None = None,
        discount_minor: int = 0,
        fee_minor: int = 0,
        tax_rate_bps: int = 0,
        currency: str = "XAF",
        precision: int = 0,
        context: dict[str, object] | None = None,
    ) -> PricingBreakdown:
        items = line_items or []
        subtotal_minor = 0
        computed_discount_minor = max(0, int(discount_minor))
        computed_fee_minor = max(0, int(fee_minor))
        for item in items:
            quantity = max(0, int(item.get("quantity") or 0))
            unit_price_minor = max(0, int(item.get("unit_price_minor") or item.get("unit_price") or 0))
            line_discount_minor = max(0, int(item.get("discount_minor") or 0))
            line_fee_minor = max(0, int(item.get("fee_minor") or 0))
            line_tax_minor = max(0, int(item.get("tax_minor") or 0))
            line_subtotal = quantity * unit_price_minor
            subtotal_minor += line_subtotal
            computed_discount_minor += line_discount_minor
            computed_fee_minor += line_fee_minor
            subtotal_minor += line_tax_minor
        taxable_base = max(0, subtotal_minor - computed_discount_minor + computed_fee_minor)
        tax_minor = max(0, int((Decimal(taxable_base) * Decimal(tax_rate_bps) / Decimal(10_000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)))
        total_minor = max(0, taxable_base + tax_minor)
        return PricingBreakdown(
            subtotal_minor=subtotal_minor,
            discount_minor=computed_discount_minor,
            fee_minor=computed_fee_minor,
            tax_minor=tax_minor,
            total_minor=total_minor,
            currency=self.normalize_currency(currency),
            precision=precision,
            source="backend",
            context=context,
        )

    def calculate_line_totals(self, *, quantity: int, unit_price_minor: int, discount_minor: int = 0, fee_minor: int = 0, tax_minor: int = 0) -> dict[str, int]:
        quantity = max(0, int(quantity))
        unit_price_minor = max(0, int(unit_price_minor))
        discount_minor = max(0, int(discount_minor))
        fee_minor = max(0, int(fee_minor))
        tax_minor = max(0, int(tax_minor))
        subtotal_minor = quantity * unit_price_minor
        total_minor = max(0, subtotal_minor - discount_minor + fee_minor + tax_minor)
        return {
            "subtotal_minor": subtotal_minor,
            "discount_minor": discount_minor,
            "fee_minor": fee_minor,
            "tax_minor": tax_minor,
            "total_minor": total_minor,
        }

    def build_reference(self, prefix: str, *parts: object) -> str:
        payload = "|".join(str(part).strip() for part in parts if str(part).strip())
        digest = sha256(payload.encode("utf-8")).hexdigest()[:12]
        return f"{_sanitize_reference(prefix)}-{digest}"

    def normalize_idempotency_key(self, value: str | None) -> str:
        return _sanitize_reference(value or "")

    def validate_transition(self, current: str, next_status: str, allowed: set[str]) -> str:
        normalized_current = _normalize_code(current)
        normalized_next = _normalize_code(next_status)
        if normalized_next not in allowed:
            raise ValidationError(f"unsupported status transition: {normalized_current} -> {normalized_next}")
        return normalized_next

    def build_readiness_score(self, *, signals: list[dict[str, object]]) -> dict[str, object]:
        total_weight = sum(int(signal.get("weight") or 0) for signal in signals) or 100
        achieved = sum(int(signal.get("weight") or 0) for signal in signals if signal.get("passed"))
        score = round((achieved / total_weight) * 100.0, 2) if total_weight else 0.0
        reasons = [str(signal.get("detail") or signal.get("name") or "") for signal in signals if not signal.get("passed")]
        return {
            "score": score,
            "maximum_score": 100.0,
            "state": "ready" if score >= 80 else "degraded",
            "signals": signals,
            "reasons": [reason for reason in reasons if reason],
        }

    def document_status(self, status: str, *, category: str) -> str:
        normalized = _normalize_code(status)
        allowed = {
            "quote": QUOTE_STATUSES,
            "invoice": INVOICE_STATUSES,
            "payment_intent": PAYMENT_INTENT_STATUSES,
            "payment_transaction": PAYMENT_TRANSACTION_STATUSES,
            "receipt": RECEIPT_STATUSES,
            "refund": REFUND_STATUSES,
            "subscription": SUBSCRIPTION_STATUSES,
            "subscription_cycle": SUBSCRIPTION_CYCLE_STATUSES,
            "commission": COMMISSION_STATUSES,
        }.get(category, frozenset())
        if allowed and normalized not in allowed:
            raise ValidationError(f"unsupported {category} status: {normalized}")
        return normalized


class CampayNumberNormalizer:
    def normalize(self, value: str) -> str:
        return normalize_mobile_money_number(value)


FINANCIAL_ENGINE = FinancialPricingEngine()
