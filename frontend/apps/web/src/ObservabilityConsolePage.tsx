import React, { useEffect, useState } from 'react';
import { useWorkflowStore, type WorkflowExecution } from '@workflows';
import { Badge, Button, Card, PageShell } from '@ui';

export function ObservabilityConsolePage() {
  const { getRecentEvents, getExecutions, metrics } = useWorkflowStore();
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Trigger component re-render by updating state
        setAutoRefresh((prev) => prev);
      }, 1000);
      setRefreshInterval(interval);

      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const recentEvents = getRecentEvents(20);
  const executions = getExecutions();
  const workflowMetrics = executions.reduce(
    (acc: { total: number; successful: number; failed: number; totalDuration: number }, exec: WorkflowExecution) => {
      acc.total += 1;
      if (exec.status === 'success') acc.successful += 1;
      if (exec.status === 'error') acc.failed += 1;
      acc.totalDuration += exec.duration || 0;
      return acc;
    },
    { total: 0, successful: 0, failed: 0, totalDuration: 0 }
  );

  return (
    <PageShell
      eyebrow="Engineering"
      title="Observability console"
      description="Monitor workflow execution, decisions, and system state in real-time."
      actions={
        <>
          <Button variant={autoRefresh ? 'primary' : 'secondary'} onClick={() => setAutoRefresh(!autoRefresh)}>
            {autoRefresh ? 'Auto-refreshing' : 'Paused'}
          </Button>
          <Button variant="secondary">Export logs</Button>
        </>
      }
    >
      <div className="space-y-6">
        {/* Metrics summary */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card title="Workflows" description="Total executions">
            <div className="text-2xl font-semibold text-white">{workflowMetrics.total}</div>
            <p className="mt-1 text-xs text-slate-400">{workflowMetrics.successful} successful</p>
          </Card>
          <Card title="Success rate" description="% of executions">
            <div className="text-2xl font-semibold text-white">
              {workflowMetrics.total > 0 ? Math.round((workflowMetrics.successful / workflowMetrics.total) * 100) : 0}%
            </div>
            <p className="mt-1 text-xs text-slate-400">{workflowMetrics.failed} failed</p>
          </Card>
          <Card title="Avg duration" description="Execution time (ms)">
            <div className="text-2xl font-semibold text-white">
              {workflowMetrics.total > 0 ? Math.round(workflowMetrics.totalDuration / workflowMetrics.total) : 0}
            </div>
            <p className="mt-1 text-xs text-slate-400">across all workflows</p>
          </Card>
          <Card title="Events" description="Recent activity">
            <div className="text-2xl font-semibold text-white">{recentEvents.length}</div>
            <p className="mt-1 text-xs text-slate-400">in last hour</p>
          </Card>
        </div>

        {/* Workflow execution timeline */}
        <Card title="Workflow execution trace" description="Latest workflow executions and their status">
          <div className="space-y-2 text-sm">
            {executions.length === 0 ? (
              <p className="text-slate-400">No workflows executed yet</p>
            ) : (
              executions
                .slice(-10)
                .reverse()
                .map((exec: WorkflowExecution) => (
                  <div
                    key={exec.id}
                    className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <span className="font-medium text-white capitalize">{exec.type.replace(/_/g, ' ')}</span>
                        <Badge
                          variant={
                            exec.status === 'success'
                              ? 'success'
                              : exec.status === 'error'
                                ? 'warning'
                                : exec.status === 'running'
                                  ? 'warning'
                                  : 'default'
                          }
                        >
                          {exec.status}
                        </Badge>
                      </div>
                      <p className="mt-1 text-xs text-slate-400">{exec.id}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-mono text-xs text-slate-300">{(exec.duration || 0).toFixed(0)}ms</p>
                      <p className="mt-1 text-xs text-slate-400">{new Date(exec.startTime).toLocaleTimeString()}</p>
                    </div>
                  </div>
                ))
            )}
          </div>
        </Card>

        {/* Brain decisions */}
        <Card title="Brain decisions" description="Intent resolution and path selection">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'brain_decision')
              .slice(-5)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <p className="font-medium text-white">Decision {event.data.id}</p>
                  <p className="mt-1 text-xs">Intent: {event.data.intent}</p>
                  <p className="text-xs">Confidence: {Math.round(event.data.confidence * 100)}%</p>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'brain_decision').length === 0 && (
              <p className="text-slate-400">No brain decisions yet</p>
            )}
          </div>
        </Card>

        {/* Knowledge calls */}
        <Card title="Knowledge calls" description="RAG engine and semantic search">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'knowledge_call')
              .slice(-5)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <p className="font-medium text-white">Query {idx + 1}</p>
                  <p className="mt-1 text-xs">Query: {event.data.query.substring(0, 60)}...</p>
                  <p className="text-xs">Results: {event.data.results.length} items</p>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'knowledge_call').length === 0 && (
              <p className="text-slate-400">No knowledge calls yet</p>
            )}
          </div>
        </Card>

        {/* Agent calls */}
        <Card title="Agent calls" description="Agent execution and actions">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'agent_call')
              .slice(-5)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <p className="font-medium text-white">{event.data.agentType}</p>
                  <p className="mt-1 text-xs">Action: {event.data.action}</p>
                  <Badge
                    variant={
                      event.data.status === 'success'
                        ? 'success'
                        : event.data.status === 'error'
                          ? 'warning'
                          : 'default'
                    }
                  >
                    {event.data.status}
                  </Badge>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'agent_call').length === 0 && (
              <p className="text-slate-400">No agent calls yet</p>
            )}
          </div>
        </Card>

        {/* Conversation pipeline */}
        <Card title="Conversation pipeline" description="Dialog flow and message exchange">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'conversation_event')
              .slice(-10)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <p className="font-medium text-white capitalize">{event.data.sender}</p>
                  <p className="mt-1 text-xs">{event.data.message.substring(0, 80)}...</p>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'conversation_event').length === 0 && (
              <p className="text-slate-400">No conversation events yet</p>
            )}
          </div>
        </Card>

        {/* Learning events */}
        <Card title="Learning events" description="System optimization and insights">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'learning_event')
              .slice(-5)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <Badge variant={event.data.event === 'success' ? 'success' : 'warning'}>
                    {event.data.event}
                  </Badge>
                  <p className="mt-1 text-xs capitalize">{event.data.event} event recorded</p>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'learning_event').length === 0 && (
              <p className="text-slate-400">No learning events yet</p>
            )}
          </div>
        </Card>

        {/* Digital Twin updates */}
        <Card title="Digital Twin updates" description="Entity state changes and synchronization">
          <div className="space-y-2 text-sm text-slate-300">
            {recentEvents
              .filter((e) => e.type === 'digital_twin_update')
              .slice(-5)
              .map((event: any, idx: number) => (
                <div key={idx} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                  <p className="font-medium text-white">{event.data.entity}</p>
                  <p className="mt-1 text-xs">Updated at {new Date(event.data.timestamp).toLocaleTimeString()}</p>
                </div>
              ))}
            {recentEvents.filter((e) => e.type === 'digital_twin_update').length === 0 && (
              <p className="text-slate-400">No digital twin updates yet</p>
            )}
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
