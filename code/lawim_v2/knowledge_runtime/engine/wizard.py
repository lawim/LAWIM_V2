from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .readiness import ReadinessEvaluator
from .resolver import NextQuestionResolver

STEP_INTENTION = 1
STEP_TYPE = 2
STEP_VILLE = 3
STEP_QUARTIER = 4
STEP_BUDGET = 5
STEP_DELAI = 6
STEP_CRITERES = 7
STEP_PREFERENCES = 8
STEP_CONFIRMATION = 9
STEP_ESCALADE = 10

STEP_NAMES: dict[int, str] = {
    STEP_INTENTION: "Intention",
    STEP_TYPE: "Type",
    STEP_VILLE: "Ville",
    STEP_QUARTIER: "Quartier",
    STEP_BUDGET: "Budget",
    STEP_DELAI: "Delai",
    STEP_CRITERES: "Criteres",
    STEP_PREFERENCES: "Preferences",
    STEP_CONFIRMATION: "Confirmation",
    STEP_ESCALADE: "Escalade",
}

STEP_FIELDS: dict[int, tuple[str, ...]] = {
    STEP_INTENTION: ("intent", "transaction_type"),
    STEP_TYPE: ("property_type",),
    STEP_VILLE: ("city",),
    STEP_QUARTIER: ("neighborhood", "zone"),
    STEP_BUDGET: ("budget_min", "budget_max", "budget_negotiable"),
    STEP_DELAI: ("timeline", "urgence"),
    STEP_CRITERES: ("surface", "chambres", "douches", "cuisine", "meuble",
                    "condition", "construction_year"),
    STEP_PREFERENCES: ("meuble", "parking", "balcon", "jardin", "ascenseur",
                       "piscine", "terrasse", "climatisation", "internet", "securite"),
    STEP_CONFIRMATION: ("confirmation",),
    STEP_ESCALADE: ("escalade_note", "agent_assistance"),
}

STEP_MANDATORY: dict[int, tuple[str, ...]] = {
    STEP_INTENTION: ("intent", "transaction_type"),
    STEP_TYPE: ("property_type",),
    STEP_VILLE: ("city",),
    STEP_QUARTIER: ("neighborhood",),
    STEP_BUDGET: ("budget_max",),
    STEP_DELAI: (),
    STEP_CRITERES: ("surface", "chambres"),
    STEP_PREFERENCES: (),
    STEP_CONFIRMATION: ("confirmation",),
    STEP_ESCALADE: (),
}

STEP_CHANNEL_LIMITS: dict[int, dict[str, int]] = {
    STEP_INTENTION: {"whatsapp": 1, "telegram": 1, "dashboard": 1},
    STEP_TYPE: {"whatsapp": 1, "telegram": 1, "dashboard": 1},
    STEP_VILLE: {"whatsapp": 1, "telegram": 2, "dashboard": 2},
    STEP_QUARTIER: {"whatsapp": 1, "telegram": 2, "dashboard": 2},
    STEP_BUDGET: {"whatsapp": 1, "telegram": 2, "dashboard": 3},
    STEP_DELAI: {"whatsapp": 1, "telegram": 2, "dashboard": 2},
    STEP_CRITERES: {"whatsapp": 1, "telegram": 3, "dashboard": 10},
    STEP_PREFERENCES: {"whatsapp": 0, "telegram": 2, "dashboard": 10},
    STEP_CONFIRMATION: {"whatsapp": 1, "telegram": 1, "dashboard": 1},
    STEP_ESCALADE: {"whatsapp": 1, "telegram": 1, "dashboard": 1},
}


@dataclass
class QualificationSession:
    session_id: str
    known_fields: dict[str, Any] = field(default_factory=dict)
    current_step: int = STEP_INTENTION
    channel: str = "dashboard"
    errors: list[str] = field(default_factory=list)
    completed: bool = False
    retry_count: dict[str, int] = field(default_factory=dict)
    escalated: bool = False


class ProgressiveWizard:
    def __init__(
        self,
        readiness: ReadinessEvaluator,
        resolver: NextQuestionResolver,
        repository: Any = None,
    ) -> None:
        self._readiness = readiness
        self._resolver = resolver
        self._repository = repository
        self._sessions: dict[str, QualificationSession] = {}

    def create_session(
        self,
        session_id: str,
        channel: str = "dashboard",
    ) -> QualificationSession:
        session = QualificationSession(
            session_id=session_id,
            channel=channel,
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> QualificationSession | None:
        return self._sessions.get(session_id)

    def submit_answer(
        self,
        session_id: str,
        field: str,
        value: Any,
    ) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            return {"error": "session_not_found", "session_id": session_id}

        if session.completed:
            return {"error": "qualification_completed", "session_id": session_id}

        if field in session.known_fields:
            session.retry_count[field] = session.retry_count.get(field, 0) + 1
            if session.retry_count[field] > 3:
                return {
                    "error": "max_retries_exceeded",
                    "field": field,
                    "step": session.current_step,
                    "action": "escalate",
                }

        session.known_fields[field] = value
        self._check_step_completion(session)
        self._auto_persist(session_id)

        return {
            "session_id": session_id,
            "current_step": session.current_step,
            "step_name": STEP_NAMES.get(session.current_step, ""),
            "known_fields": dict(session.known_fields),
            "completed": session.completed,
            "errors": list(session.errors),
        }

    def _check_step_completion(self, session: QualificationSession) -> None:
        while True:
            step = session.current_step
            mandatory = STEP_MANDATORY.get(step, ())
            known = set(session.known_fields.keys())

            missing = [f for f in mandatory if f not in known]
            if missing:
                return

            if step >= STEP_CONFIRMATION:
                session.completed = True
                return

            session.current_step += 1
            session.errors.clear()

    def get_step_info(self, step: int) -> dict[str, Any]:
        fields = STEP_FIELDS.get(step, ())
        mandatory = STEP_MANDATORY.get(step, ())
        return {
            "step": step,
            "name": STEP_NAMES.get(step, ""),
            "fields": list(fields),
            "mandatory": list(mandatory),
            "channel_limits": STEP_CHANNEL_LIMITS.get(step, {}),
        }

    def get_current_step_info(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            return {"error": "session_not_found"}

        info = self.get_step_info(session.current_step)
        readiness = self._readiness.readiness_summary(session.known_fields)
        next_q = self._resolver.resolve_next(
            session.known_fields,
            property_type=session.known_fields.get("property_type"),
        )

        info.update({
            "session_id": session_id,
            "known_fields": dict(session.known_fields),
            "readiness": readiness,
            "next_question": next_q,
            "completed": session.completed,
            "channel": session.channel,
        })
        return info

    def list_steps(self) -> list[dict[str, Any]]:
        return [
            {
                "step": step,
                "name": STEP_NAMES[step],
                "fields": list(STEP_FIELDS.get(step, ())),
                "mandatory": list(STEP_MANDATORY.get(step, ())),
            }
            for step in sorted(STEP_NAMES)
        ]

    def escalate(self, session_id: str, reason: str = "") -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            return {"error": "session_not_found"}
        session.current_step = STEP_ESCALADE
        session.escalated = True
        return {
            "session_id": session_id,
            "step": STEP_ESCALADE,
            "step_name": "Escalade",
            "reason": reason,
            "known_fields": dict(session.known_fields),
        }

    def reload_session(self, session_id: str) -> QualificationSession | None:
        loaded = self.load_session(session_id)
        if loaded:
            self._sessions[session_id] = loaded
        return loaded

    def _ensure_wizard_table(self) -> None:
        if self._repository is None:
            return
        try:
            self._repository.execute(
                """CREATE TABLE IF NOT EXISTS wizard_sessions (
                    session_id TEXT PRIMARY KEY,
                    channel TEXT DEFAULT 'dashboard',
                    current_step INTEGER DEFAULT 1,
                    known_fields TEXT DEFAULT '{}',
                    errors_json TEXT DEFAULT '[]',
                    completed INTEGER DEFAULT 0,
                    retry_count_json TEXT DEFAULT '{}',
                    escalated INTEGER DEFAULT 0,
                    updated_at TEXT
                )"""
            )
        except Exception:
            pass

    def persist_session(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            return {"error": "session_not_found"}
        if self._repository is None:
            return {"status": "no_repository"}
        self._ensure_wizard_table()
        try:
            self._repository.execute(
                """INSERT OR REPLACE INTO wizard_sessions (
                    session_id, channel, current_step, known_fields,
                    errors_json, completed, retry_count_json, escalated, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    session.session_id,
                    session.channel,
                    session.current_step,
                    json.dumps(session.known_fields, ensure_ascii=False),
                    json.dumps(session.errors),
                    1 if session.completed else 0,
                    json.dumps(session.retry_count),
                    1 if session.escalated else 0,
                    __import__("datetime").datetime.now(
                        __import__("datetime").timezone.utc
                    ).isoformat(),
                ],
            )
            return {"status": "saved", "session_id": session_id}
        except Exception:
            return {"error": "persist_failed"}

    def load_session(self, session_id: str) -> QualificationSession | None:
        if self._repository is None:
            return None
        try:
            row = self._repository.fetch_one(
                "SELECT * FROM wizard_sessions WHERE session_id = ?",
                [session_id],
            )
            if not row:
                return None
            return QualificationSession(
                session_id=row["session_id"],
                channel=row.get("channel", "dashboard"),
                current_step=row.get("current_step", STEP_INTENTION),
                known_fields=json.loads(row.get("known_fields", "{}")),
                errors=json.loads(row.get("errors_json", "[]")),
                completed=bool(row.get("completed", 0)),
                retry_count=json.loads(row.get("retry_count_json", "{}")),
                escalated=bool(row.get("escalated", 0)),
            )
        except Exception:
            return None

    def _auto_persist(self, session_id: str) -> None:
        if self._repository is not None:
            try:
                self.persist_session(session_id)
            except Exception:
                pass

    def reset_session(self, session_id: str) -> dict[str, Any]:
        if session_id in self._sessions:
            del self._sessions[session_id]
        return {"session_id": session_id, "status": "reset"}
