from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field


def _percentile(values: list[float], ratio: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * ratio))))
    return round(ordered[index], 2)


@dataclass
class RuntimeMetrics:
    started_at: float = field(default_factory=time.time)
    requests_total: int = 0
    requests_failed: int = 0
    matches_total: int = 0
    conversations_total: int = 0
    notifications_total: int = 0
    projects_total: int = 0
    intelligent_workspace_total: int = 0
    ecosystem_partners_total: int = 0
    ecosystem_services_total: int = 0
    ecosystem_matching_total: int = 0
    ecosystem_workflows_total: int = 0
    ecosystem_reputation_total: int = 0
    ecosystem_notifications_total: int = 0
    ecosystem_orchestration_total: int = 0
    cognition_graph_total: int = 0
    cognition_context_total: int = 0
    cognition_refresh_total: int = 0
    cognition_reasoning_total: int = 0
    cognition_simulation_total: int = 0
    cognition_intelligence_total: int = 0
    cognition_next_action_total: int = 0
    cognition_risks_total: int = 0
    cognition_opportunities_total: int = 0
    assistant_sessions_total: int = 0
    assistant_chat_total: int = 0
    assistant_agents_total: int = 0
    assistant_prompts_total: int = 0
    assistant_context_total: int = 0
    assistant_rag_total: int = 0
    knowledge_documents_total: int = 0
    knowledge_chunks_total: int = 0
    knowledge_queries_total: int = 0
    knowledge_import_total: int = 0
    knowledge_index_total: int = 0
    rag_requests_total: int = 0
    rag_context_size_total: int = 0
    workflow_definitions_total: int = 0
    workflow_created_total: int = 0
    process_executions_total: int = 0
    task_list_total: int = 0
    task_completed_total: int = 0
    queue_list_total: int = 0
    queue_enqueue_total: int = 0
    queue_dequeue_total: int = 0
    event_list_total: int = 0
    automation_events_total: int = 0
    automation_started_total: int = 0
    automation_retry_total: int = 0
    automation_escalation_total: int = 0
    approval_list_total: int = 0
    approval_created_total: int = 0
    approval_decided_total: int = 0
    automation_notifications_total: int = 0
    notification_sent_total: int = 0
    property_list_total: int = 0
    property_detail_total: int = 0
    property_search_total: int = 0
    listing_list_total: int = 0
    listing_created_total: int = 0
    listing_published_total: int = 0
    listing_archived_total: int = 0
    verification_run_total: int = 0
    valuation_computed_total: int = 0
    matching_run_total: int = 0
    matching_results_total: int = 0
    recommendation_generated_total: int = 0
    visit_list_total: int = 0
    visit_scheduled_total: int = 0
    visit_completed_total: int = 0
    transaction_list_total: int = 0
    transaction_started_total: int = 0
    transaction_closed_total: int = 0
    intelligence_computed_total: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)
    _latency_samples: list[float] = field(default_factory=list)
    _knowledge_search_latency_samples: list[float] = field(default_factory=list)
    _process_execution_latency_samples: list[float] = field(default_factory=list)
    _verification_latency_samples: list[float] = field(default_factory=list)
    _route_counts: dict[str, int] = field(default_factory=dict)

    def increment(self, name: str, *, failed: bool = False) -> None:
        with self.lock:
            self.requests_total += 1
            if failed:
                self.requests_failed += 1
            if name == "matches":
                self.matches_total += 1
            elif name == "conversations":
                self.conversations_total += 1
            elif name == "notifications":
                self.notifications_total += 1
            elif name == "projects":
                self.projects_total += 1
            elif name == "intelligent_workspace":
                self.intelligent_workspace_total += 1
            elif name == "ecosystem_partners":
                self.ecosystem_partners_total += 1
            elif name == "ecosystem_services":
                self.ecosystem_services_total += 1
            elif name == "ecosystem_matching":
                self.ecosystem_matching_total += 1
            elif name == "ecosystem_workflows":
                self.ecosystem_workflows_total += 1
            elif name == "ecosystem_reputation":
                self.ecosystem_reputation_total += 1
            elif name == "ecosystem_notifications":
                self.ecosystem_notifications_total += 1
            elif name == "ecosystem_orchestration":
                self.ecosystem_orchestration_total += 1
            elif name == "cognition_graph":
                self.cognition_graph_total += 1
            elif name == "cognition_context":
                self.cognition_context_total += 1
            elif name == "cognition_refresh":
                self.cognition_refresh_total += 1
            elif name == "cognition_reasoning":
                self.cognition_reasoning_total += 1
            elif name == "cognition_simulation":
                self.cognition_simulation_total += 1
            elif name == "cognition_intelligence":
                self.cognition_intelligence_total += 1
            elif name == "cognition_next_action":
                self.cognition_next_action_total += 1
            elif name == "cognition_risks":
                self.cognition_risks_total += 1
            elif name == "cognition_opportunities":
                self.cognition_opportunities_total += 1
            elif name == "assistant_sessions":
                self.assistant_sessions_total += 1
            elif name == "assistant_chat":
                self.assistant_chat_total += 1
            elif name == "assistant_agents":
                self.assistant_agents_total += 1
            elif name == "assistant_prompts":
                self.assistant_prompts_total += 1
            elif name == "assistant_context":
                self.assistant_context_total += 1
            elif name == "assistant_rag":
                self.assistant_rag_total += 1
            elif name == "knowledge_documents":
                self.knowledge_documents_total += 1
            elif name == "knowledge_chunks":
                self.knowledge_chunks_total += 1
            elif name == "knowledge_queries":
                self.knowledge_queries_total += 1
            elif name == "knowledge_import":
                self.knowledge_import_total += 1
            elif name == "knowledge_index":
                self.knowledge_index_total += 1
            elif name == "workflow_definitions":
                self.workflow_definitions_total += 1
            elif name == "workflow_created":
                self.workflow_created_total += 1
            elif name == "process_executions":
                self.process_executions_total += 1
            elif name == "task_list":
                self.task_list_total += 1
            elif name == "task_completed":
                self.task_completed_total += 1
            elif name == "queue_list":
                self.queue_list_total += 1
            elif name == "queue_enqueue":
                self.queue_enqueue_total += 1
            elif name == "queue_dequeue":
                self.queue_dequeue_total += 1
            elif name == "event_list":
                self.event_list_total += 1
            elif name == "automation_events":
                self.automation_events_total += 1
            elif name == "automation_started":
                self.automation_started_total += 1
            elif name == "automation_retry":
                self.automation_retry_total += 1
            elif name == "automation_escalation":
                self.automation_escalation_total += 1
            elif name == "approval_list":
                self.approval_list_total += 1
            elif name == "approval_created":
                self.approval_created_total += 1
            elif name == "approval_decided":
                self.approval_decided_total += 1
            elif name == "automation_notifications":
                self.automation_notifications_total += 1
            elif name == "notification_sent":
                self.notification_sent_total += 1
            elif name == "property_list":
                self.property_list_total += 1
            elif name == "property_detail":
                self.property_detail_total += 1
            elif name == "property_search":
                self.property_search_total += 1
            elif name == "listing_list":
                self.listing_list_total += 1
            elif name == "listing_created":
                self.listing_created_total += 1
            elif name == "listing_published":
                self.listing_published_total += 1
            elif name == "listing_archived":
                self.listing_archived_total += 1
            elif name == "verification_run":
                self.verification_run_total += 1
            elif name == "valuation_computed":
                self.valuation_computed_total += 1
            elif name == "matching_run":
                self.matching_run_total += 1
            elif name == "recommendation_generated":
                self.recommendation_generated_total += 1
            elif name == "visit_list":
                self.visit_list_total += 1
            elif name == "visit_scheduled":
                self.visit_scheduled_total += 1
            elif name == "visit_completed":
                self.visit_completed_total += 1
            elif name == "transaction_list":
                self.transaction_list_total += 1
            elif name == "transaction_started":
                self.transaction_started_total += 1
            elif name == "transaction_closed":
                self.transaction_closed_total += 1
            elif name == "intelligence_computed":
                self.intelligence_computed_total += 1

    def record_verification(self, *, latency_ms: float) -> None:
        with self.lock:
            self._verification_latency_samples.append(latency_ms)
            if len(self._verification_latency_samples) > 500:
                self._verification_latency_samples = self._verification_latency_samples[-500:]

    def record_matching(self, *, score: int) -> None:
        with self.lock:
            self.matching_results_total += max(0, score)

    def record_knowledge_search(self, *, latency_ms: float) -> None:
        with self.lock:
            self.knowledge_queries_total += 1
            self._knowledge_search_latency_samples.append(latency_ms)
            if len(self._knowledge_search_latency_samples) > 500:
                self._knowledge_search_latency_samples = self._knowledge_search_latency_samples[-500:]

    def record_process_execution(self, *, duration_ms: float) -> None:
        with self.lock:
            self._process_execution_latency_samples.append(duration_ms)
            if len(self._process_execution_latency_samples) > 500:
                self._process_execution_latency_samples = self._process_execution_latency_samples[-500:]

    def record_rag_request(self, *, context_size: int) -> None:
        with self.lock:
            self.rag_requests_total += 1
            self.rag_context_size_total += max(0, context_size)

    def record_request(self, *, route: str, duration_ms: float, failed: bool = False) -> None:
        with self.lock:
            self.requests_total += 1
            if failed:
                self.requests_failed += 1
            self._latency_samples.append(duration_ms)
            if len(self._latency_samples) > 1000:
                self._latency_samples = self._latency_samples[-1000:]
            self._route_counts[route] = self._route_counts.get(route, 0) + 1

    def snapshot(self) -> dict[str, object]:
        with self.lock:
            uptime_seconds = max(0, int(time.time() - self.started_at))
            samples = list(self._latency_samples)
            top_routes = sorted(self._route_counts.items(), key=lambda item: item[1], reverse=True)[:10]
            return {
                "uptime_seconds": uptime_seconds,
                "requests_total": self.requests_total,
                "requests_failed": self.requests_failed,
                "matches_total": self.matches_total,
                "conversations_total": self.conversations_total,
                "notifications_total": self.notifications_total,
                "projects_total": self.projects_total,
                "intelligent_workspace_total": self.intelligent_workspace_total,
                "ecosystem_partners_total": self.ecosystem_partners_total,
                "ecosystem_services_total": self.ecosystem_services_total,
                "ecosystem_matching_total": self.ecosystem_matching_total,
                "ecosystem_workflows_total": self.ecosystem_workflows_total,
                "ecosystem_reputation_total": self.ecosystem_reputation_total,
                "ecosystem_notifications_total": self.ecosystem_notifications_total,
                "ecosystem_orchestration_total": self.ecosystem_orchestration_total,
                "cognition_graph_total": self.cognition_graph_total,
                "cognition_context_total": self.cognition_context_total,
                "cognition_refresh_total": self.cognition_refresh_total,
                "cognition_reasoning_total": self.cognition_reasoning_total,
                "cognition_simulation_total": self.cognition_simulation_total,
                "cognition_intelligence_total": self.cognition_intelligence_total,
                "cognition_next_action_total": self.cognition_next_action_total,
                "cognition_risks_total": self.cognition_risks_total,
                "cognition_opportunities_total": self.cognition_opportunities_total,
                "assistant_sessions_total": self.assistant_sessions_total,
                "assistant_chat_total": self.assistant_chat_total,
                "assistant_agents_total": self.assistant_agents_total,
                "assistant_prompts_total": self.assistant_prompts_total,
                "assistant_context_total": self.assistant_context_total,
                "assistant_rag_total": self.assistant_rag_total,
                "knowledge_documents_total": self.knowledge_documents_total,
                "knowledge_chunks_total": self.knowledge_chunks_total,
                "knowledge_queries_total": self.knowledge_queries_total,
                "knowledge_import_total": self.knowledge_import_total,
                "knowledge_index_total": self.knowledge_index_total,
                "rag_requests_total": self.rag_requests_total,
                "rag_context_size_total": self.rag_context_size_total,
                "workflow_definitions_total": self.workflow_definitions_total,
                "workflow_created_total": self.workflow_created_total,
                "process_executions_total": self.process_executions_total,
                "task_list_total": self.task_list_total,
                "task_completed_total": self.task_completed_total,
                "queue_list_total": self.queue_list_total,
                "queue_enqueue_total": self.queue_enqueue_total,
                "queue_dequeue_total": self.queue_dequeue_total,
                "event_list_total": self.event_list_total,
                "automation_events_total": self.automation_events_total,
                "automation_started_total": self.automation_started_total,
                "automation_retry_total": self.automation_retry_total,
                "automation_escalation_total": self.automation_escalation_total,
                "approval_list_total": self.approval_list_total,
                "approval_created_total": self.approval_created_total,
                "approval_decided_total": self.approval_decided_total,
                "automation_notifications_total": self.automation_notifications_total,
                "notification_sent_total": self.notification_sent_total,
                "property_list_total": self.property_list_total,
                "property_detail_total": self.property_detail_total,
                "property_search_total": self.property_search_total,
                "listing_list_total": self.listing_list_total,
                "listing_created_total": self.listing_created_total,
                "listing_published_total": self.listing_published_total,
                "listing_archived_total": self.listing_archived_total,
                "verification_run_total": self.verification_run_total,
                "valuation_computed_total": self.valuation_computed_total,
                "matching_run_total": self.matching_run_total,
                "matching_results_total": self.matching_results_total,
                "recommendation_generated_total": self.recommendation_generated_total,
                "visit_list_total": self.visit_list_total,
                "visit_scheduled_total": self.visit_scheduled_total,
                "visit_completed_total": self.visit_completed_total,
                "transaction_list_total": self.transaction_list_total,
                "transaction_started_total": self.transaction_started_total,
                "transaction_closed_total": self.transaction_closed_total,
                "intelligence_computed_total": self.intelligence_computed_total,
                "verification_latency_ms": {
                    "p50": _percentile(self._verification_latency_samples, 0.50),
                    "p95": _percentile(self._verification_latency_samples, 0.95),
                    "samples": len(self._verification_latency_samples),
                },
                "process_execution_latency_ms": {
                    "p50": _percentile(self._process_execution_latency_samples, 0.50),
                    "p95": _percentile(self._process_execution_latency_samples, 0.95),
                    "samples": len(self._process_execution_latency_samples),
                },
                "knowledge_search_latency_ms": {
                    "p50": _percentile(self._knowledge_search_latency_samples, 0.50),
                    "p95": _percentile(self._knowledge_search_latency_samples, 0.95),
                    "samples": len(self._knowledge_search_latency_samples),
                },
                "latency_ms": {
                    "p50": _percentile(samples, 0.50),
                    "p95": _percentile(samples, 0.95),
                    "max": round(max(samples), 2) if samples else 0.0,
                    "samples": len(samples),
                },
                "routes_top": [{"route": route, "count": count} for route, count in top_routes],
            }


METRICS = RuntimeMetrics()
