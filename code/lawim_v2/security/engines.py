from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from .constants import CONSENT_STATUSES, RISK_LEVELS, RISK_SIGNAL_TYPES
from .permissions import permission_key
from .policies import evaluate_access_policy


class PermissionEngine:
    def build_grants(self, *, permissions: list[dict[str, object]]) -> list[str]:
        grants: list[str] = []
        for perm in permissions:
            resource = str(perm.get("resource") or "*")
            action = str(perm.get("action") or "read")
            key = str(perm.get("permission_key") or permission_key(resource, action))
            grants.append(key if ":" in key else permission_key(resource, action))
        return grants

    def evaluate(
        self,
        *,
        role_keys: list[str],
        permission_grants: list[str],
        policy: dict[str, object],
        attributes: dict[str, Any] | None = None,
    ) -> bool:
        return evaluate_access_policy(
            role_keys=role_keys,
            permission_grants=permission_grants,
            attributes=attributes,
            policy=policy,
        )

    def user_has_permission(self, *, grants: list[str], resource: str, action: str) -> bool:
        from .permissions import evaluate_permissions

        required = permission_key(resource, action)
        return evaluate_permissions(grants=grants, required=[required])


class AuditEngine:
    GENESIS_CHECKSUM = "0" * 64

    def compute_checksum(
        self,
        *,
        entry_key: str,
        event_type: str,
        action: str,
        payload: dict[str, Any],
        previous_checksum: str,
        created_at: str,
    ) -> str:
        canonical = json.dumps(
            {
                "entry_key": entry_key,
                "event_type": event_type,
                "action": action,
                "payload": payload,
                "previous_checksum": previous_checksum,
                "created_at": created_at,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def verify_chain(self, entries: list[dict[str, object]]) -> dict[str, object]:
        if not entries:
            return {"valid": True, "checked": 0}
        previous = self.GENESIS_CHECKSUM
        for entry in entries:
            expected = self.compute_checksum(
                entry_key=str(entry.get("entry_key") or ""),
                event_type=str(entry.get("event_type") or "system"),
                action=str(entry.get("action") or ""),
                payload=json.loads(str(entry.get("payload_json") or "{}")) if entry.get("payload_json") else {},
                previous_checksum=previous,
                created_at=str(entry.get("created_at") or ""),
            )
            actual = str(entry.get("checksum") or "")
            if actual != expected:
                return {"valid": False, "checked": len(entries), "failed_entry": entry.get("entry_key")}
            previous = actual
        return {"valid": True, "checked": len(entries)}


class ComplianceEngine:
    def consent_valid(self, *, consent: dict[str, object] | None, consent_type: str) -> bool:
        if consent is None:
            return False
        if str(consent.get("consent_type") or "") != consent_type:
            return False
        return str(consent.get("status") or "") in {"granted"} and str(consent.get("status") or "") in CONSENT_STATUSES

    def retention_due(self, *, created_at: str | None, retention_days: int, now: datetime | None = None) -> bool:
        if not created_at:
            return False
        try:
            created = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
        except ValueError:
            return False
        ref = now or datetime.now(timezone.utc)
        delta = ref - created
        return delta.days >= max(1, retention_days)

    def check_policy(self, *, policy: dict[str, object], context: dict[str, Any]) -> dict[str, object]:
        rules_raw = policy.get("rules_json") or "[]"
        try:
            rules = json.loads(str(rules_raw)) if isinstance(rules_raw, str) else list(rules_raw)
        except json.JSONDecodeError:
            rules = []
        violations: list[str] = []
        for rule in rules:
            field = str(rule.get("field") or "")
            required = rule.get("required")
            if required and not context.get(field):
                violations.append(f"missing:{field}")
        return {
            "compliant": len(violations) == 0,
            "framework": policy.get("framework"),
            "violations": violations,
        }


class RiskEngine:
    AUTO_LOCK_THRESHOLD = 80

    def score_signal(self, *, signal_type: str, severity: str, base_score: int = 0) -> dict[str, object]:
        if signal_type not in RISK_SIGNAL_TYPES:
            signal_type = "login_anomaly"
        severity_weights = {"low": 5, "medium": 15, "high": 30, "critical": 50}
        delta = severity_weights.get(severity, 10)
        score = min(100, max(0, base_score + delta))
        level = self.level_for_score(score)
        return {
            "signal_type": signal_type,
            "severity": severity,
            "score_delta": delta,
            "score": score,
            "level": level,
            "auto_lock": score >= self.AUTO_LOCK_THRESHOLD,
        }

    def level_for_score(self, score: int) -> str:
        if score >= 80:
            return "critical"
        if score >= 60:
            return "high"
        if score >= 35:
            return "medium"
        return "low"

    def aggregate(self, *, signals: list[dict[str, object]], base_score: int = 0) -> dict[str, object]:
        total = base_score
        factors: dict[str, int] = {}
        for signal in signals:
            signal_type = str(signal.get("signal_type") or "login_anomaly")
            delta = int(signal.get("score_delta") or 0)
            total += delta
            factors[signal_type] = factors.get(signal_type, 0) + delta
        score = min(100, total)
        level = self.level_for_score(score)
        if level not in RISK_LEVELS:
            level = "low"
        return {
            "score": score,
            "level": level,
            "factors": factors,
            "auto_lock": score >= self.AUTO_LOCK_THRESHOLD,
            "open_signals": len(signals),
        }


class PrivacyEngine:
    DEFAULT_EXPORT_SCOPE = ("profile", "sessions", "audit", "consents")

    def normalize_scope(self, scope: list[str] | None) -> list[str]:
        if not scope:
            return list(self.DEFAULT_EXPORT_SCOPE)
        allowed = set(self.DEFAULT_EXPORT_SCOPE)
        return [s for s in scope if s in allowed] or list(self.DEFAULT_EXPORT_SCOPE)

    def validate_erasure(self, *, scope: dict[str, Any], has_active_sessions: bool = False) -> dict[str, object]:
        errors: list[str] = []
        if has_active_sessions and scope.get("include_sessions"):
            errors.append("active_sessions_present")
        if not scope.get("subject_id") and not scope.get("user_id") and not scope.get("contact_id"):
            errors.append("subject_required")
        if scope.get("include_financial") and not scope.get("legal_hold_cleared"):
            errors.append("legal_hold_active")
        return {"valid": len(errors) == 0, "errors": errors}

    def export_payload(self, *, scope: list[str], data: dict[str, Any]) -> dict[str, object]:
        normalized = self.normalize_scope(scope)
        return {key: data.get(key) for key in normalized if key in data}


class IntegrationBridge:
    PROGRAM_SOURCES: tuple[str, ...] = (
        "intelligent_core",
        "ecosystem",
        "cognition",
        "assistant",
        "knowledge_platform",
        "workflow_automation",
        "real_estate_intelligence",
        "crm",
        "marketplace",
    )

    def sources(self) -> list[str]:
        return list(self.PROGRAM_SOURCES)


class SecurityPlatformEngine:
    def __init__(self) -> None:
        self.permission = PermissionEngine()
        self.audit = AuditEngine()
        self.compliance = ComplianceEngine()
        self.risk = RiskEngine()
        self.privacy = PrivacyEngine()
        self.integration = IntegrationBridge()

    def integration_sources(self) -> list[str]:
        return self.integration.sources()
