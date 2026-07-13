from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import re
from typing import Any

from ..brain.memory import BrainMemory
from ..brain.relation import RelationEngine


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "value"


def _compact(value: object) -> str:
    text = str(value or "").strip()
    return text


def _memory_field_value(memory_items: list[dict[str, Any]], field_key: str) -> str | None:
    for item in memory_items:
        if str(item.get("field_key") or "").strip() != field_key:
            continue
        if str(item.get("status") or "") != "active":
            continue
        value = str(item.get("value") or "").strip()
        if value:
            return value
    return None


def _parse_context(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    raw = row.get("context_json")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _first(items: object, key: str) -> Any:
    if not isinstance(items, list) or not items:
        return None
    first = items[0]
    if not isinstance(first, dict):
        return None
    return first.get(key)


def _project_type_from_intent(intent: str) -> str:
    mapping = {
        "buy": "buy",
        "rent": "rent",
        "sell": "sell",
        "invest": "invest",
        "build": "build",
        "find_land": "buy",
        "find_property": "buy",
        "find_partner": "other",
        "find_funding": "other",
        "manage": "other",
    }
    return mapping.get(intent, "other")


def _resolve_intent(*, analysis: dict[str, Any], progression: dict[str, Any], project: dict[str, Any] | None) -> str:
    progression_intent = str(progression.get("intent") or "").strip()
    if progression_intent in {"buy", "rent", "sell", "invest", "build", "find_land", "find_partner", "find_funding", "manage"}:
        return progression_intent
    project_intent = str(project.get("project_type") or "").strip() if project else ""
    if project_intent in {"buy", "rent", "sell", "invest", "build", "find_land", "find_partner", "find_funding", "manage"}:
        return project_intent
    analysis_intent = str(analysis.get("primary_intent") or "").strip()
    if analysis_intent in {"buy", "rent", "sell", "invest", "build", "find_land", "find_partner", "find_funding", "manage"}:
        return analysis_intent
    if analysis_intent == "find_property":
        return project_intent or "buy"
    return project_intent or progression_intent or analysis_intent or "other"


def _business_goal_from_intent(intent: str) -> str:
    mapping = {
        "buy": "search_properties",
        "rent": "search_properties",
        "find_land": "search_properties",
        "find_property": "search_properties",
        "sell": "qualify_listing",
        "invest": "analyse_market",
        "build": "qualify_construction_project",
        "find_partner": "search_partners",
        "find_funding": "qualify_financing",
        "manage": "qualification",
    }
    return mapping.get(intent, "qualification")


def _authorized_modules(action_key: str) -> tuple[str, ...]:
    if action_key == "SEARCH_LAWIM_PROPERTIES":
        return ("conversation_core", "brain_memory", "real_estate_intelligence", "brain_relation", "response_policy")
    if action_key == "CREATE_SEARCH_ALERT":
        return ("conversation_core", "brain_memory", "intelligent_core", "response_policy")
    if action_key == "REQUEST_RELATIONSHIP_CONSENT":
        return ("conversation_core", "brain_relation", "brain_memory", "response_policy")
    if action_key == "CREATE_RELATIONSHIP_REQUEST":
        return ("conversation_core", "brain_relation", "brain_memory", "response_policy")
    if action_key == "SCHEDULE_VISIT":
        return ("conversation_core", "real_estate_intelligence", "brain_memory", "response_policy")
    if action_key == "TRANSFER_TO_LAWIM_AGENT":
        return ("conversation_core", "brain_memory", "communication", "response_policy")
    return ("conversation_core", "brain_memory", "response_policy")


def _forbidden_modules() -> tuple[str, ...]:
    return ("assistant_legacy", "direct_llm", "external_platforms")


def _money_text(amount: int | None, currency: str | None) -> str:
    if amount is None:
        return ""
    normalized_currency = str(currency or "XAF").upper()
    if normalized_currency == "XAF":
        return f"{amount:,}".replace(",", " ") + " FCFA"
    return f"{amount:,}".replace(",", " ") + f" {normalized_currency}"


@dataclass(slots=True)
class BusinessActionResult:
    action_key: str
    status: str
    response_kind: str
    response_mode: str
    response_text: str | None
    business_goal: str
    next_action: str
    signature: str
    executed_modules: tuple[str, ...] = ()
    project_id: int | None = None
    project: dict[str, Any] | None = None
    state: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BusinessActionExecutor:
    def __init__(self, repository, memory: BrainMemory | None = None, relation_engine: RelationEngine | None = None) -> None:
        self.repository = repository
        self.memory = memory or BrainMemory(repository)
        self.relation_engine = relation_engine or RelationEngine(repository)

    def execute(
        self,
        *,
        project_id: int | None,
        project: dict[str, Any] | None,
        contact: dict[str, Any] | None,
        actor: dict[str, object] | None,
        channel: str,
        language: str,
        message_id: str,
        text: str,
        analysis: dict[str, Any],
        progression: dict[str, Any],
        conversation_key: str,
        thread_id: int | None,
        message_row: dict[str, Any],
    ) -> BusinessActionResult:
        intent = _resolve_intent(analysis=analysis, progression=progression, project=project)
        entities = analysis.get("entities") if isinstance(analysis.get("entities"), dict) else {}
        memory_items = self.memory.get_active(project_id) if project_id is not None else []
        property_type = self._resolve_property_type(project=project, entities=entities, memory_items=memory_items)
        city = self._resolve_city(project=project, entities=entities, memory_items=memory_items)
        budget_max = self._resolve_budget_max(project=project, entities=entities, memory_items=memory_items)
        budget_min = self._resolve_budget_min(project=project, memory_items=memory_items)
        currency = self._resolve_currency(project=project, entities=entities, memory_items=memory_items)
        transaction_type = _project_type_from_intent(intent)
        action_key = self._resolve_action_key(progression=progression, intent=intent)
        business_goal = _business_goal_from_intent(intent)
        next_action_label = str(progression.get("next_action") or "").strip()
        signature = self._build_signature(
            project_id=project_id,
            message_id=message_id,
            action_key=action_key,
            intent=intent,
            city=city,
            budget_max=budget_max,
            property_type=property_type,
            channel=channel,
        )
        if project_id is not None:
            cached = self._load_cached_state(project_id, signature)
            if cached is not None:
                return cached

        if action_key not in {"SEARCH_LAWIM_PROPERTIES", "CREATE_SEARCH_ALERT", "REQUEST_RELATIONSHIP_CONSENT", "CREATE_RELATIONSHIP_REQUEST", "SCHEDULE_VISIT", "TRANSFER_TO_LAWIM_AGENT"}:
            action_key = "CAPTURE_QUALIFICATION_FIELD" if progression.get("missing_fields") else "CREATE_NEXT_ACTION"

        captured_facts = self._capture_facts(
            project_id=project_id,
            project=project,
            actor=actor,
            contact=contact,
            analysis=analysis,
            progression=progression,
            channel=channel,
            message_id=message_id,
            message_row=message_row,
            city=city,
            budget_max=budget_max,
            budget_min=budget_min,
            currency=currency,
            property_type=property_type,
            intent=intent,
            transaction_type=transaction_type,
        )

        if project_id is not None:
            project = self._resolve_and_update_project(
                project_id=project_id,
                project=project,
                actor=actor,
                contact=contact,
                analysis=analysis,
                intent=intent,
                progression=progression,
                channel=channel,
                city=city,
                budget_min=budget_min,
                budget_max=budget_max,
                currency=currency,
                property_type=property_type,
                transaction_type=transaction_type,
                conversation_key=conversation_key,
                message_id=message_id,
                thread_id=thread_id,
                captured_facts=captured_facts,
            )

        response_text: str | None = None
        response_kind = "ai"
        response_mode = "ai"
        payload: dict[str, Any] = {
            "city": city,
            "budget_max": budget_max,
            "budget_min": budget_min,
            "currency": currency,
            "property_type": property_type,
            "intent": intent,
            "transaction_type": transaction_type,
        }

        if action_key == "SEARCH_LAWIM_PROPERTIES":
            response_mode = "deterministic_action"
            response_kind = "search_results"
            response_text, payload = self._execute_search(
                project_id=project_id,
                project=project,
                contact=contact,
                analysis=analysis,
                progression=progression,
                language=language,
                city=city,
                budget_max=budget_max,
                budget_min=budget_min,
                currency=currency,
                property_type=property_type,
                transaction_type=transaction_type,
                intent=intent,
                signature=signature,
                conversation_key=conversation_key,
            )
        elif action_key == "CREATE_SEARCH_ALERT":
            response_mode = "deterministic_action"
            response_kind = "no_result"
            response_text = self._execute_search_alert(
                language=language,
                city=city,
                budget_max=budget_max,
                property_type=property_type,
                intent=intent,
            )
        elif action_key == "TRANSFER_TO_LAWIM_AGENT":
            response_mode = "deterministic_action"
            response_kind = "handoff"
            response_text = self._execute_agent_handoff(
                project_id=project_id,
                actor=actor,
                contact=contact,
                language=language,
                city=city,
                budget_max=budget_max,
                property_type=property_type,
                intent=intent,
            )
        elif action_key == "REQUEST_RELATIONSHIP_CONSENT":
            response_mode = "deterministic_action"
            response_kind = "relationship"
            response_text = self._execute_consent_request(project_id=project_id, language=language)
        elif action_key == "CREATE_RELATIONSHIP_REQUEST":
            response_mode = "deterministic_action"
            response_kind = "relationship"
            response_text = self._execute_relationship_request(project_id=project_id, language=language)
        elif action_key == "SCHEDULE_VISIT":
            response_mode = "deterministic_action"
            response_kind = "visit"
            response_text = self._execute_visit_request(project_id=project_id, language=language)
        elif action_key == "CAPTURE_QUALIFICATION_FIELD":
            response_mode = "qualification"
            response_kind = "qualification"
            response_text = self._qualification_message(language=language, progression=progression, city=city, budget_max=budget_max, property_type=property_type)
        else:
            response_mode = "qualification"
            response_kind = "qualification"
            response_text = self._qualification_message(language=language, progression=progression, city=city, budget_max=budget_max, property_type=property_type)

        state = {
            "conversation_id": conversation_key,
            "dossier_id": project_id,
            "intent": intent,
            "transaction_type": transaction_type,
            "property_type": property_type,
            "conversation_state": str(progression.get("transaction_stage") or ""),
            "known_fields": list(progression.get("known_fields") or []),
            "missing_fields": list(progression.get("missing_fields") or []),
            "priority_field": self._priority_field(progression),
            "business_goal": business_goal,
            "next_action": action_key,
            "authorized_modules": list(_authorized_modules(action_key)),
            "forbidden_modules": list(_forbidden_modules()),
            "response_mode": response_mode,
            "responsible_actor": str(progression.get("responsible_actor") or "LAWIM_AI"),
            "deadline": progression.get("deadline"),
            "response_text": response_text,
            "signature": signature,
            "captured_facts": captured_facts,
            "payload": payload,
        }
        if project_id is not None:
            self._persist_state(project_id, state)
        return BusinessActionResult(
            action_key=action_key,
            status="executed" if response_text else "skipped",
            response_kind=response_kind,
            response_mode=response_mode,
            response_text=response_text,
            business_goal=business_goal,
            next_action=action_key,
            signature=signature,
            executed_modules=_authorized_modules(action_key),
            project_id=project_id,
            project=project,
            state=state,
            payload=payload,
        )

    def _resolve_action_key(self, *, progression: dict[str, Any], intent: str) -> str:
        if bool(progression.get("minimum_search_ready") or progression.get("search_ready")):
            return "SEARCH_LAWIM_PROPERTIES"
        if bool(progression.get("missing_fields")):
            return "CAPTURE_QUALIFICATION_FIELD"
        if intent in {"find_partner"}:
            return "CREATE_RELATIONSHIP_REQUEST"
        return "CREATE_NEXT_ACTION"

    def _resolve_property_type(self, *, project: dict[str, Any] | None, entities: dict[str, Any], memory_items: list[dict[str, Any]]) -> str:
        if project and project.get("property_type"):
            return str(project["property_type"]).strip().lower()
        memory_value = _memory_field_value(memory_items, "property_type")
        if memory_value:
            return memory_value.strip().lower()
        values = entities.get("property_types")
        if isinstance(values, list) and values:
            return str(values[0]).strip().lower()
        return ""

    def _resolve_city(self, *, project: dict[str, Any] | None, entities: dict[str, Any], memory_items: list[dict[str, Any]]) -> str:
        if project and project.get("location_city"):
            return str(project["location_city"]).strip()
        memory_value = _memory_field_value(memory_items, "city")
        if memory_value:
            return memory_value.strip()
        values = entities.get("cities")
        if isinstance(values, list) and values:
            first = values[0]
            if isinstance(first, dict):
                return str(first.get("city") or "").strip()
        return ""

    def _resolve_budget_max(self, *, project: dict[str, Any] | None, entities: dict[str, Any], memory_items: list[dict[str, Any]]) -> int | None:
        if project and project.get("budget_max") is not None:
            try:
                return int(project["budget_max"])
            except (TypeError, ValueError):
                return None
        memory_value = _memory_field_value(memory_items, "budget_max")
        if memory_value is not None:
            try:
                return int(float(memory_value))
            except (TypeError, ValueError):
                pass
        values = entities.get("budgets")
        if isinstance(values, list) and values:
            first = values[0]
            if isinstance(first, dict):
                try:
                    return int(first.get("value"))
                except (TypeError, ValueError):
                    return None
        return None

    def _resolve_budget_min(self, *, project: dict[str, Any] | None, memory_items: list[dict[str, Any]]) -> int | None:
        if project and project.get("budget_min") is not None:
            try:
                return int(project["budget_min"])
            except (TypeError, ValueError):
                return None
        memory_value = _memory_field_value(memory_items, "budget_min")
        if memory_value is not None:
            try:
                return int(float(memory_value))
            except (TypeError, ValueError):
                pass
        return None

    def _resolve_currency(self, *, project: dict[str, Any] | None, entities: dict[str, Any], memory_items: list[dict[str, Any]]) -> str:
        if project and project.get("currency"):
            return str(project["currency"]).strip().upper()
        memory_value = _memory_field_value(memory_items, "currency")
        if memory_value:
            return memory_value.strip().upper()
        values = entities.get("budgets")
        if isinstance(values, list) and values:
            first = values[0]
            if isinstance(first, dict) and first.get("currency"):
                return str(first.get("currency")).strip().upper()
        return "XAF"

    def _priority_field(self, progression: dict[str, Any]) -> str | None:
        missing = progression.get("missing_fields")
        if isinstance(missing, list) and missing:
            return str(missing[0])
        return None

    def _capture_facts(
        self,
        *,
        project_id: int | None,
        project: dict[str, Any] | None,
        actor: dict[str, object] | None,
        contact: dict[str, Any] | None,
        analysis: dict[str, Any],
        progression: dict[str, Any],
        channel: str,
        message_id: str,
        message_row: dict[str, Any],
        city: str,
        budget_max: int | None,
        budget_min: int | None,
        currency: str,
        property_type: str,
        intent: str,
        transaction_type: str,
    ) -> dict[str, Any]:
        captured: dict[str, Any] = {}
        if project_id is None:
            return captured
        source_id = int(message_row["id"]) if message_row.get("id") is not None else None
        context = self.repository.get_project_context(project_id)
        current = _parse_context(context)
        facts = {
            "city": city,
            "budget_max": budget_max,
            "budget_min": budget_min,
            "currency": currency,
            "property_type": property_type,
            "transaction_type": transaction_type,
            "intent": intent,
        }
        active_items = self.memory.get_active(project_id, kind="confirmed_fact")
        for field_key, raw_value in facts.items():
            if raw_value in {None, ""}:
                continue
            value = str(raw_value)
            existing = next((item for item in active_items if str(item.get("field_key") or "") == field_key), None)
            if existing and str(existing.get("value") or "") == value:
                captured[field_key] = raw_value
                continue
            if existing and str(existing.get("memory_key") or ""):
                self.memory.reject(project_id, str(existing["memory_key"]))
            memory_key = f"confirmed-{field_key}-{_slugify(value)}"
            try:
                label_map = {
                    "city": "ville",
                    "budget_max": "budget maximum",
                    "budget_min": "budget minimum",
                    "currency": "devise",
                    "property_type": "type de bien",
                    "transaction_type": "type de projet",
                    "intent": "intention",
                }
                self.memory.add_item(
                    project_id=project_id,
                    kind="confirmed_fact",
                    key=memory_key,
                    label=label_map.get(field_key, field_key.replace("_", " ")),
                    value=value,
                    field_key=field_key,
                    source_table="communication_messages",
                    source_id=source_id,
                    confidence=95,
                    metadata={
                        "channel": channel,
                        "message_id": message_id,
                        "intent": intent,
                        "transaction_type": transaction_type,
                    },
                )
            except Exception:
                pass
            captured[field_key] = raw_value
        merged_context = {
            **current,
            "conversation_id": current.get("conversation_id") or project_id,
            "dossier_id": project_id,
            "channel": channel,
            "actor_user_id": int(actor["id"]) if actor and actor.get("id") is not None else current.get("actor_user_id"),
            "contact_id": int(contact["id"]) if contact and contact.get("id") is not None else current.get("contact_id"),
            "city": city,
            "budget_max": budget_max,
            "budget_min": budget_min,
            "currency": currency,
            "property_type": property_type,
            "intent": intent,
            "transaction_type": transaction_type,
            "known_fields": list(progression.get("known_fields") or []),
            "missing_fields": list(progression.get("missing_fields") or []),
            "next_action": progression.get("next_action"),
            "business_goal": _business_goal_from_intent(intent),
            "response_mode": "deterministic_action" if bool(progression.get("minimum_search_ready") or progression.get("search_ready")) else "qualification",
            "captured_facts": captured,
        }
        try:
            self.repository.upsert_project_context(project_id, merged_context)
        except Exception:
            pass
        if project is not None:
            updates: dict[str, Any] = {}
            if city and not project.get("location_city"):
                updates["location_city"] = city
            if budget_max is not None and project.get("budget_max") is None:
                updates["budget_max"] = budget_max
            if budget_min is not None and project.get("budget_min") is None:
                updates["budget_min"] = budget_min
            if currency and not project.get("currency"):
                updates["currency"] = currency
            if intent and not project.get("project_type"):
                updates["project_type"] = transaction_type
            if updates:
                try:
                    self.repository.update_project(int(project["id"]), **updates)
                except Exception:
                    pass
        return captured

    def _resolve_and_update_project(
        self,
        *,
        project_id: int,
        project: dict[str, Any] | None,
        actor: dict[str, object] | None,
        contact: dict[str, Any] | None,
        analysis: dict[str, Any],
        intent: str,
        progression: dict[str, Any],
        channel: str,
        city: str,
        budget_min: int | None,
        budget_max: int | None,
        currency: str,
        property_type: str,
        transaction_type: str,
        conversation_key: str,
        message_id: str,
        thread_id: int | None,
        captured_facts: dict[str, Any],
    ) -> dict[str, Any] | None:
        if project is None:
            project = self.repository.get_project(project_id)
        updates: dict[str, Any] = {}
        if city and not project.get("location_city"):
            updates["location_city"] = city
        if budget_min is not None and project.get("budget_min") is None:
            updates["budget_min"] = budget_min
        if budget_max is not None and project.get("budget_max") is None:
            updates["budget_max"] = budget_max
        if currency and not project.get("currency"):
            updates["currency"] = currency
        if transaction_type and not project.get("project_type"):
            updates["project_type"] = transaction_type
        if updates:
            try:
                project = self.repository.update_project(project_id, **updates)
            except Exception:
                pass
        context = {
            "conversation_id": conversation_key,
            "dossier_id": project_id,
            "channel": channel,
            "actor_user_id": int(actor["id"]) if actor and actor.get("id") is not None else None,
            "contact_id": int(contact["id"]) if contact and contact.get("id") is not None else None,
            "intent": intent,
            "transaction_type": transaction_type,
            "property_type": property_type,
            "conversation_state": str(progression.get("transaction_stage") or ""),
            "known_fields": list(progression.get("known_fields") or []),
            "missing_fields": list(progression.get("missing_fields") or []),
            "priority_field": self._priority_field(progression),
            "business_goal": _business_goal_from_intent(intent),
            "next_action": str(progression.get("next_action") or ""),
            "authorized_modules": list(_authorized_modules(self._resolve_action_key(progression=progression, intent=intent))),
            "forbidden_modules": list(_forbidden_modules()),
            "response_mode": "deterministic_action" if bool(progression.get("minimum_search_ready") or progression.get("search_ready")) else "qualification",
            "responsible_actor": str(progression.get("responsible_actor") or "LAWIM_AI"),
            "deadline": progression.get("deadline"),
            "captured_facts": captured_facts,
            "updated_at_message_id": message_id,
            "thread_id": thread_id,
        }
        try:
            self.repository.upsert_project_context(project_id, context)
        except Exception:
            pass
        return project

    def _execute_search(
        self,
        *,
        project_id: int | None,
        project: dict[str, Any] | None,
        contact: dict[str, Any] | None,
        analysis: dict[str, Any],
        progression: dict[str, Any],
        language: str,
        city: str,
        budget_max: int | None,
        budget_min: int | None,
        currency: str,
        property_type: str,
        transaction_type: str,
        intent: str,
        signature: str,
        conversation_key: str,
    ) -> tuple[str, dict[str, Any]]:
        query_parts = [property_type, city, _compact(budget_max), transaction_type, intent]
        query = " ".join(part for part in query_parts if part)
        search_results = self.repository.rei_search(query=query, limit=10) if query else []
        user_id = int(contact["user_id"]) if contact and contact.get("user_id") is not None else None
        if user_id is None and project is not None and project.get("user_id") is not None:
            user_id = int(project["user_id"])
        criteria = {
            "city": city or None,
            "country": str(project.get("location_country") or "Cameroon") if project else "Cameroon",
            "budget_min": budget_min,
            "budget_max": budget_max,
            "property_type": property_type or None,
            "status": "published",
            "limit": 5,
        }
        matching = self.repository.run_rei_matching(user_id=user_id, project_id=project_id, criteria=criteria)
        match_rows = matching.get("results") if isinstance(matching, dict) else []
        if project_id is not None and match_rows:
            try:
                self.relation_engine.run_full_match(project_id=project_id, project=project, analysis=analysis, language=language)
            except Exception:
                pass
        if project_id is not None:
            action = self._ensure_project_action(
                project_id=project_id,
                action_key="SEARCH_LAWIM_PROPERTIES",
                title=f"Recherche LAWIM {property_type or 'bien'} {city or ''}".strip(),
                priority="high",
            )
            if not match_rows:
                self._ensure_project_action(
                    project_id=project_id,
                    action_key="CREATE_SEARCH_ALERT",
                    title=f"Créer une alerte de recherche pour {property_type or 'bien'} {city or ''}".strip(),
                    priority="normal",
                )
        summary = self._format_search_summary(
            language=language,
            city=city,
            budget_max=budget_max,
            currency=currency,
            property_type=property_type,
            search_results=search_results,
            matching_results=match_rows or [],
        )
        payload = {
            "query": query,
            "search_count": len(search_results),
            "matching_count": len(match_rows or []),
            "search_results": search_results[:5],
            "matching_results": match_rows[:5],
            "search_session_key": matching.get("session_key") if isinstance(matching, dict) else None,
            "conversation_key": conversation_key,
            "signature": signature,
        }
        return summary, payload

    def _execute_search_alert(
        self,
        *,
        language: str,
        city: str,
        budget_max: int | None,
        property_type: str,
        intent: str,
    ) -> str:
        if language == "en":
            return (
                f"🤖 LAWIM AI: I did not find an exact result for {property_type or 'the requested property'}"
                f"{f' in {city}' if city else ''}. I will keep the search active and can broaden the area, adjust the budget, or transfer the file to a LAWIM agent."
            )
        if language == "pcm":
            return (
                f"🤖 LAWIM AI: I no find exact result for {property_type or 'the requested property'}"
                f"{f' for {city}' if city else ''}. I go keep the search active and fit widen the area, adjust budget, or hand over to LAWIM agent."
            )
        budget_text = _money_text(budget_max, "XAF")
        return (
            f"🤖 LAWIM AI : Je n'ai pas trouvé de résultat exact pour {property_type or 'le bien demandé'}"
            f"{f' à {city}' if city else ''}{f' avec un budget maximal de {budget_text}' if budget_text else ''}. "
            "Je conserve la recherche, et je peux élargir la zone, ajuster le budget, créer une alerte ou transmettre le dossier à un agent LAWIM."
        )

    def _execute_agent_handoff(
        self,
        *,
        project_id: int | None,
        actor: dict[str, object] | None,
        contact: dict[str, Any] | None,
        language: str,
        city: str,
        budget_max: int | None,
        property_type: str,
        intent: str,
    ) -> str:
        if project_id is not None:
            self._ensure_project_action(
                project_id=project_id,
                action_key="TRANSFER_TO_LAWIM_AGENT",
                title=f"Transférer le dossier à un agent LAWIM",
                priority="high",
            )
        budget_text = _money_text(budget_max, "XAF")
        if language == "en":
            return (
                f"🤖 LAWIM AI: I have prepared a handoff to a LAWIM agent for {property_type or 'your request'}"
                f"{f' in {city}' if city else ''}{f' with a budget cap of {budget_text}' if budget_text else ''}."
            )
        if language == "pcm":
            return (
                f"🤖 LAWIM AI: I don prepare handoff to LAWIM agent for {property_type or 'your request'}"
                f"{f' for {city}' if city else ''}{f' with budget cap {budget_text}' if budget_text else ''}."
            )
        return (
            f"🤖 LAWIM AI : J'ai préparé une prise en charge par un agent LAWIM pour {property_type or 'votre demande'}"
            f"{f' à {city}' if city else ''}{f' avec un budget plafond de {budget_text}' if budget_text else ''}."
        )

    def _execute_consent_request(self, *, project_id: int | None, language: str) -> str:
        if project_id is not None:
            proposals = self.repository.list_relation_proposals(project_id, status="consent_pending", limit=5)
            if proposals:
                proposal_id = int(proposals[0]["id"])
                self.relation_engine.request_consent(proposal_id)
        if language == "en":
            return "🤖 LAWIM AI: Your consent request has been recorded. I keep the file active while waiting for your confirmation."
        if language == "pcm":
            return "🤖 LAWIM AI: Your consent request don go in. I keep the file active while waiting for your confirmation."
        return "🤖 LAWIM AI : Votre demande de consentement a été enregistrée. Je conserve le dossier actif en attendant votre confirmation."

    def _execute_relationship_request(self, *, project_id: int | None, language: str) -> str:
        if project_id is not None:
            proposals = self.repository.list_relation_proposals(project_id, status="proposed", limit=5)
            if proposals:
                proposal_id = int(proposals[0]["id"])
                self.relation_engine.request_consent(proposal_id)
        if language == "en":
            return "🤖 LAWIM AI: The relationship request has been created and is now tracked in the LAWIM file."
        if language == "pcm":
            return "🤖 LAWIM AI: Relationship request don enter the LAWIM file."
        return "🤖 LAWIM AI : La demande de mise en relation a été créée et suivie dans le dossier LAWIM."

    def _execute_visit_request(self, *, project_id: int | None, language: str) -> str:
        if project_id is not None:
            proposals = self.repository.list_relation_proposals(project_id, status="accepted", limit=5)
            if proposals:
                proposal = proposals[0]
                property_id = int(proposal["target_id"])
                try:
                    self.repository.schedule_rei_visit(property_id=property_id, user_id=None, scheduled_at=self._default_visit_datetime())
                except Exception:
                    pass
        if language == "en":
            return "🤖 LAWIM AI: A visit request has been recorded in the file."
        if language == "pcm":
            return "🤖 LAWIM AI: Visit request don enter the file."
        return "🤖 LAWIM AI : La demande de visite a été enregistrée dans le dossier."

    def _qualification_message(
        self,
        *,
        language: str,
        progression: dict[str, Any],
        city: str,
        budget_max: int | None,
        property_type: str,
    ) -> str:
        next_question = str(progression.get("next_question") or "").strip()
        if next_question:
            return next_question
        if language == "en":
            return "🤖 LAWIM AI: I still need one more detail to continue."
        if language == "pcm":
            return "🤖 LAWIM AI: I still need one more detail to continue."
        return "🤖 LAWIM AI : Il me manque encore une information pour continuer."

    def _ensure_project_action(self, *, project_id: int, action_key: str, title: str, priority: str = "normal") -> dict[str, Any]:
        existing = next((row for row in self.repository.list_project_actions(project_id) if str(row.get("action_key")) == action_key), None)
        if existing is not None:
            return existing
        return self.repository.create_project_action(project_id=project_id, action_key=action_key, title=title, priority=priority)

    def _format_search_summary(
        self,
        *,
        language: str,
        city: str,
        budget_max: int | None,
        currency: str,
        property_type: str,
        search_results: list[dict[str, Any]],
        matching_results: list[dict[str, Any]],
    ) -> str:
        top_matches: list[str] = []
        seen_ids: set[int] = set()
        for match in matching_results:
            property_id = match.get("property_id")
            if property_id is None:
                continue
            try:
                pid = int(property_id)
            except (TypeError, ValueError):
                continue
            if pid in seen_ids:
                continue
            seen_ids.add(pid)
            prop = self.repository.get_property(pid)
            title = str(prop.get("title") or f"Bien {pid}")
            city_name = str(prop.get("city") or "")
            price_min = prop.get("price_min")
            price_max = prop.get("price_max")
            price_text = ""
            if price_min is not None or price_max is not None:
                min_value = int(price_min or price_max or 0)
                max_value = int(price_max or price_min or 0)
                if min_value == max_value and min_value:
                    price_text = f"{min_value:,}".replace(",", " ") + f" {currency}"
                elif min_value or max_value:
                    price_text = f"{min_value:,}".replace(",", " ") + " - " + f"{max_value:,}".replace(",", " ") + f" {currency}"
            summary = f"{title}"
            if city_name:
                summary += f" ({city_name})"
            if price_text:
                summary += f" - {price_text}"
            top_matches.append(summary)
            if len(top_matches) >= 2:
                break
        match_count = len(matching_results)
        search_count = len(search_results)
        budget_text = _money_text(budget_max, currency)
        if match_count == 0:
            return self._execute_search_alert(
                language=language,
                city=city,
                budget_max=budget_max,
                property_type=property_type,
                intent="rent",
            )
        if language == "en":
            intro = f"🤖 LAWIM AI: I found {match_count} match(es)"
            if property_type or city:
                intro += f" for {property_type or 'the requested property'}"
                if city:
                    intro += f" in {city}"
            if budget_text:
                intro += f" with a budget cap of {budget_text}"
            lines = [intro + "."]
            if top_matches:
                lines.append("Top matches:")
                lines.extend(f"- {item}" for item in top_matches)
            lines.append("Next step: choose one property and I will continue the file.")
            return "\n".join(lines)
        if language == "pcm":
            intro = f"🤖 LAWIM AI: I find {match_count} match(es)"
            if property_type or city:
                intro += f" for {property_type or 'the requested property'}"
                if city:
                    intro += f" for {city}"
            if budget_text:
                intro += f" with budget cap {budget_text}"
            lines = [intro + "."]
            if top_matches:
                lines.append("Top matches:")
                lines.extend(f"- {item}" for item in top_matches)
            lines.append("Next step: choose one property and I will continue the file.")
            return "\n".join(lines)
        intro = f"🤖 LAWIM AI : J'ai trouvé {match_count} résultat(s)"
        if property_type or city:
            intro += f" pour {property_type or 'le bien demandé'}"
            if city:
                intro += f" à {city}"
        if budget_text:
            intro += f" avec un budget plafond de {budget_text}"
        lines = [intro + "."]
        if top_matches:
            lines.append("Résultats principaux :")
            lines.extend(f"- {item}" for item in top_matches)
        lines.append("Prochaine étape : choisissez un bien et je poursuis le dossier.")
        return "\n".join(lines)

    def _build_signature(
        self,
        *,
        project_id: int | None,
        message_id: str,
        action_key: str,
        intent: str,
        city: str,
        budget_max: int | None,
        property_type: str,
        channel: str,
    ) -> str:
        payload = {
            "project_id": project_id,
            "message_id": message_id,
            "action_key": action_key,
            "intent": intent,
            "city": city,
            "budget_max": budget_max,
            "property_type": property_type,
            "channel": channel,
        }
        digest = hashlib.sha1(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        return digest

    def _load_cached_state(self, project_id: int, signature: str) -> BusinessActionResult | None:
        context = self.repository.get_project_context(project_id)
        if not context:
            return None
        payload = _parse_context(context)
        runtime = payload.get("business_action")
        if not isinstance(runtime, dict):
            return None
        if str(runtime.get("signature") or "") != signature:
            return None
        if str(runtime.get("status") or "") != "executed":
            return None
        return BusinessActionResult(
            action_key=str(runtime.get("action_key") or "CREATE_NEXT_ACTION"),
            status=str(runtime.get("status") or "executed"),
            response_kind=str(runtime.get("response_kind") or "ai"),
            response_mode=str(runtime.get("response_mode") or "deterministic_action"),
            response_text=runtime.get("response_text"),
            business_goal=str(runtime.get("business_goal") or ""),
            next_action=str(runtime.get("next_action") or ""),
            signature=signature,
            executed_modules=tuple(runtime.get("executed_modules") or ()),
            project_id=project_id,
            project=None,
            state=runtime,
            payload=dict(runtime.get("payload") or {}),
        )

    def _persist_state(self, project_id: int, state: dict[str, Any]) -> None:
        context = self.repository.get_project_context(project_id)
        current = _parse_context(context)
        current.update(
            {
                "conversation_id": state.get("conversation_id"),
                "dossier_id": state.get("dossier_id"),
                "intent": state.get("intent"),
                "transaction_type": state.get("transaction_type"),
                "property_type": state.get("property_type"),
                "conversation_state": state.get("conversation_state"),
                "known_fields": state.get("known_fields"),
                "missing_fields": state.get("missing_fields"),
                "priority_field": state.get("priority_field"),
                "business_goal": state.get("business_goal"),
                "next_action": state.get("next_action"),
                "authorized_modules": state.get("authorized_modules"),
                "forbidden_modules": state.get("forbidden_modules"),
                "response_mode": state.get("response_mode"),
                "responsible_actor": state.get("responsible_actor"),
                "deadline": state.get("deadline"),
                "business_action": {
                    "action_key": state.get("next_action"),
                    "status": "executed" if state.get("response_text") else "skipped",
                    "response_kind": "search_results" if state.get("next_action") == "SEARCH_LAWIM_PROPERTIES" else state.get("response_mode"),
                    "response_mode": state.get("response_mode"),
                    "response_text": state.get("response_text"),
                    "business_goal": state.get("business_goal"),
                    "next_action": state.get("next_action"),
                    "signature": state.get("signature"),
                    "executed_modules": list(state.get("authorized_modules") or []),
                    "payload": state.get("payload") or {},
                },
                "captured_facts": state.get("captured_facts") or {},
            }
        )
        try:
            self.repository.upsert_project_context(project_id, current)
        except Exception:
            pass

    def _default_visit_datetime(self) -> str:
        from datetime import datetime, timedelta, timezone

        return (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
