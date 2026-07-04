/**
 * Workflow orchestration store using Zustand
 * Manages workflow execution, observability, and state
 */

import { create } from 'zustand';
import type {
  WorkflowExecution,
  WorkflowType,
  WorkflowStatus,
  ObservabilityEvent,
  WorkflowContext,
  BrainDecision,
  KnowledgeCall,
  AgentCall,
  ConversationEvent,
  LearningEvent,
  DigitalTwinUpdate,
  ProductReadinessMetrics
} from './types';

export interface WorkflowStore {
  // Workflow state
  currentWorkflow: WorkflowExecution | null;
  workflows: Map<string, WorkflowExecution>;
  
  // Observability
  events: ObservabilityEvent[];
  maxEvents: number;
  
  // Metrics
  metrics: ProductReadinessMetrics | null;
  
  // Actions
  startWorkflow: (type: WorkflowType, context: Partial<Omit<WorkflowContext, 'workflowId' | 'workflowType' | 'startTime'>>) => string;
  endWorkflow: (workflowId: string, status: WorkflowStatus, error?: string) => void;
  addEvent: (event: ObservabilityEvent) => void;
  updateMetrics: (metrics: ProductReadinessMetrics) => void;
  
  // Getters
  getWorkflow: (id: string) => WorkflowExecution | undefined;
  getExecutions: (type?: WorkflowType) => WorkflowExecution[];
  getRecentEvents: (count?: number) => ObservabilityEvent[];
  getEventsByWorkflow: (workflowId: string) => ObservabilityEvent[];
  getEventsByType: (eventType: string) => ObservabilityEvent[];
  
  // Cleanup
  clear: () => void;
  clearWorkflow: (id: string) => void;
}

let workflowCounter = 0;

export const useWorkflowStore = create<WorkflowStore>((set, get) => ({
  currentWorkflow: null,
  workflows: new Map(),
  events: [],
  maxEvents: 1000,
  metrics: null,

  startWorkflow: (type, context) => {
    const workflowId = `wf_${Date.now()}_${++workflowCounter}`;
    const workflow: WorkflowExecution = {
      id: workflowId,
      type,
      status: 'running',
      startTime: Date.now(),
      steps: [],
      layers: [],
      metadata: {
        ...context,
        source: context.source || 'web',
        mockMode: context.mockMode || false
      }
    };

    set((state) => ({
      currentWorkflow: workflow,
      workflows: new Map(state.workflows).set(workflowId, workflow)
    }));

    // Add workflow start event
    get().addEvent({
      type: 'workflow_execution',
      data: workflow
    });

    return workflowId;
  },

  endWorkflow: (workflowId, status, error) => {
    const workflow = get().getWorkflow(workflowId);
    if (!workflow) return;

    const updated = {
      ...workflow,
      status,
      endTime: Date.now(),
      duration: Date.now() - workflow.startTime,
      error
    };

    set((state) => {
      const workflows = new Map(state.workflows);
      workflows.set(workflowId, updated);
      return {
        workflows,
        currentWorkflow: state.currentWorkflow?.id === workflowId ? updated : state.currentWorkflow
      };
    });

    // Add workflow end event
    get().addEvent({
      type: 'workflow_execution',
      data: updated
    });
  },

  addEvent: (event) => {
    set((state) => {
      const events = [...state.events, event];
      // Keep only last maxEvents
      if (events.length > state.maxEvents) {
        events.shift();
      }
      return { events };
    });
  },

  updateMetrics: (metrics) => {
    set({ metrics });
  },

  getWorkflow: (id) => {
    return get().workflows.get(id);
  },

  getExecutions: (type) => {
    const workflows = Array.from(get().workflows.values());
    if (type) {
      return workflows.filter((w) => w.type === type);
    }
    return workflows;
  },

  getRecentEvents: (count = 50) => {
    const events = get().events;
    return events.slice(Math.max(0, events.length - count));
  },

  getEventsByWorkflow: (workflowId) => {
    return get().events.filter((e) => {
      const data = (e as any).data;
      return data.workflow === workflowId || data.id === workflowId;
    });
  },

  getEventsByType: (eventType) => {
    return get().events.filter((e) => e.type === eventType);
  },

  clear: () => {
    set({
      currentWorkflow: null,
      workflows: new Map(),
      events: [],
      metrics: null
    });
  },

  clearWorkflow: (id) => {
    set((state) => {
      const workflows = new Map(state.workflows);
      workflows.delete(id);
      return {
        workflows,
        currentWorkflow: state.currentWorkflow?.id === id ? null : state.currentWorkflow
      };
    });
  }
}));
