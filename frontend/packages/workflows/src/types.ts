/**
 * Core workflow types and orchestration infrastructure
 * Supports all 13 business workflows with full observability
 */

import { z } from 'zod';

// Workflow execution states
export type WorkflowStatus = 'idle' | 'loading' | 'running' | 'success' | 'error' | 'offline' | 'timeout' | 'auth_error' | 'permission_denied';

// Application states
export type ApplicationState = 'loading' | 'empty' | 'offline' | 'error' | 'success' | 'auth_error' | 'permission_denied' | 'timeout' | 'retry';

// Workflow types - 13 business workflows
export type WorkflowType = 
  | 'real_estate_search'
  | 'property_consultation'
  | 'add_to_favorites'
  | 'account_creation'
  | 'authentication'
  | 'create_crm_lead'
  | 'create_service_request'
  | 'marketplace'
  | 'property_estimation'
  | 'ai_assistant'
  | 'document_search'
  | 'user_dashboard'
  | 'admin_dashboard';

// Workflow step
export interface WorkflowStep {
  id: string;
  name: string;
  status: ApplicationState;
  duration: number;
  error?: string;
  timestamp: number;
}

// Layer in workflow execution
export interface ExecutionLayer {
  name: 'UI' | 'Brain' | 'Conversation' | 'Knowledge' | 'Agents' | 'API SDK' | 'Backend';
  status: ApplicationState;
  duration: number;
  error?: string;
  timestamp: number;
  details?: Record<string, unknown>;
}

// Complete workflow execution trace
export interface WorkflowExecution {
  id: string;
  type: WorkflowType;
  status: WorkflowStatus;
  startTime: number;
  endTime?: number;
  duration?: number;
  steps: WorkflowStep[];
  layers: ExecutionLayer[];
  error?: string;
  metadata: {
    userId?: string;
    sessionId?: string;
    source: 'web' | 'admin' | 'assistant';
    mockMode: boolean;
  };
}

// Brain decision
export interface BrainDecision {
  id: string;
  workflow: WorkflowType;
  intent: string;
  confidence: number;
  selectedPath: string;
  alternativePaths: Array<{ path: string; confidence: number }>;
  timestamp: number;
}

// Knowledge call
export interface KnowledgeCall {
  id: string;
  workflow: WorkflowType;
  query: string;
  results: unknown[];
  confidence: number;
  sources: string[];
  timestamp: number;
}

// Agent call
export interface AgentCall {
  id: string;
  workflow: WorkflowType;
  agentType: string;
  action: string;
  status: ApplicationState;
  result?: unknown;
  error?: string;
  timestamp: number;
}

// Conversation event
export interface ConversationEvent {
  id: string;
  workflow: WorkflowType;
  step: number;
  message: string;
  sender: 'user' | 'system' | 'agent';
  timestamp: number;
}

// Learning event
export interface LearningEvent {
  id: string;
  workflow: WorkflowType;
  event: 'success' | 'failure' | 'optimization' | 'insight';
  data: Record<string, unknown>;
  timestamp: number;
}

// Digital Twin update
export interface DigitalTwinUpdate {
  id: string;
  workflow: WorkflowType;
  entity: string;
  change: Record<string, unknown>;
  timestamp: number;
}

// Observability events
export type ObservabilityEvent = 
  | { type: 'workflow_execution'; data: WorkflowExecution }
  | { type: 'brain_decision'; data: BrainDecision }
  | { type: 'knowledge_call'; data: KnowledgeCall }
  | { type: 'agent_call'; data: AgentCall }
  | { type: 'conversation_event'; data: ConversationEvent }
  | { type: 'learning_event'; data: LearningEvent }
  | { type: 'digital_twin_update'; data: DigitalTwinUpdate };

// Workflow orchestration context
export interface WorkflowContext {
  workflowId: string;
  workflowType: WorkflowType;
  userId?: string;
  sessionId: string;
  source: 'web' | 'admin' | 'assistant';
  mockMode: boolean;
  startTime: number;
  currentLayer: ExecutionLayer['name'];
  data: Record<string, unknown>;
}

// Product readiness metrics
export interface ProductReadinessMetrics {
  modules: {
    count: number;
    healthy: number;
    warnings: number;
  };
  routes: {
    count: number;
    public: number;
    protected: number;
  };
  pages: {
    count: number;
    responsive: number;
    accessible: number;
  };
  packages: {
    count: number;
    installed: number;
    outdated: number;
  };
  tests: {
    total: number;
    passing: number;
    failing: number;
    coverage: number;
  };
  build: {
    status: 'success' | 'warning' | 'error';
    duration: number;
    size: number;
  };
  workflows: {
    total: number;
    validated: number;
    coverage: number;
  };
  health: {
    overall: 'healthy' | 'warning' | 'critical';
    lastCheck: number;
  };
}

// Validators
export const WorkflowTypeSchema = z.enum([
  'real_estate_search',
  'property_consultation',
  'add_to_favorites',
  'account_creation',
  'authentication',
  'create_crm_lead',
  'create_service_request',
  'marketplace',
  'property_estimation',
  'ai_assistant',
  'document_search',
  'user_dashboard',
  'admin_dashboard'
]);

export const WorkflowStatusSchema = z.enum([
  'idle',
  'loading',
  'running',
  'success',
  'error',
  'offline',
  'timeout',
  'auth_error',
  'permission_denied'
]);

export const ApplicationStateSchema = z.enum([
  'loading',
  'empty',
  'offline',
  'error',
  'success',
  'auth_error',
  'permission_denied',
  'timeout',
  'retry'
]);
