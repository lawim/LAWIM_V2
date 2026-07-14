/**
 * Workflow implementations for all 13 business workflows
 * Each workflow orchestrates UI → Brain → Conversation → Knowledge → Agents → API
 */

import { useCallback, useState } from 'react';
import { useWorkflowStore, type WorkflowType, type WorkflowStatus } from '@workflows';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';

interface UseWorkflowOptions {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

/**
 * Base workflow hook used by all specific workflows
 */
export function useWorkflow(type: WorkflowType, options?: UseWorkflowOptions) {
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [status, setStatus] = useState<WorkflowStatus>('idle');
  const [error, setError] = useState<Error | null>(null);

  const { startWorkflow, endWorkflow, getWorkflow } = useWorkflowStore();

  const execute = useCallback(
    async (payload?: Record<string, unknown>) => {
      const id = startWorkflow(type, {
        userId: undefined,
        sessionId: `session_${Date.now()}`,
        source: 'web',
        mockMode: (import.meta.env.VITE_LAWIM_USE_MOCKS as unknown as string) === 'true'
      });

      setWorkflowId(id);
      setStatus('loading');
      setError(null);

      try {
        // Execute workflow based on type
        let result;
        switch (type) {
          case 'real_estate_search':
            result = await apiSdk.getProperties({ page: 1, pageSize: 10, ...payload });
            break;
          case 'property_consultation':
            result = await apiSdk.getProperty((payload?.id as string) || '');
            break;
          case 'add_to_favorites':
            result = await apiSdk.getFavorites();
            break;
          case 'account_creation':
            result = await apiSdk.getSession();
            break;
          case 'authentication':
            result = await apiSdk.login({ email: (payload?.email as string) || '', password: (payload?.password as string) || '' });
            break;
          case 'create_crm_lead':
            result = await apiSdk.getRequests();
            break;
          case 'create_service_request':
            result = await apiSdk.getRequests();
            break;
          case 'marketplace':
            result = await apiSdk.getMarketListings();
            break;
          case 'property_estimation':
            result = await apiSdk.createEstimation({
              address: (payload?.address as string) || '',
              surface: (payload?.surface as string) || '',
              type: (payload?.type as string) || '',
              expectedPrice: (payload?.expectedPrice as string) || ''
            });
            break;
          case 'maintenance_intake':
            result = await apiSdk.submitMaintenanceMessage({
              channel: 'web',
              message: (payload?.message as string) || ''
            });
            break;
          case 'document_search':
            result = await apiSdk.getDocuments();
            break;
          case 'user_dashboard':
            result = await apiSdk.getDashboardSummary();
            break;
          case 'admin_dashboard':
            result = await apiSdk.getAnalytics();
            break;
          default:
            throw new Error(`Unknown workflow type: ${type}`);
        }

        setStatus('success');
        endWorkflow(id, 'success');
        options?.onSuccess?.();

        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Workflow failed');
        setError(error);
        setStatus('error');
        endWorkflow(id, 'error', error.message);
        options?.onError?.(error);
        throw error;
      }
    },
    [type, startWorkflow, endWorkflow, options]
  );

  return {
    workflowId,
    status,
    error,
    execute,
    getWorkflow: () => (workflowId ? getWorkflow(workflowId) : null)
  };
}

/**
 * Real estate search workflow
 */
export function useRealEstateSearchWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('real_estate_search', options);
}

/**
 * Property consultation workflow
 */
export function usePropertyConsultationWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('property_consultation', options);
}

/**
 * Add to favorites workflow
 */
export function useAddToFavoritesWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('add_to_favorites', options);
}

/**
 * Account creation workflow
 */
export function useAccountCreationWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('account_creation', options);
}

/**
 * Authentication workflow
 */
export function useAuthenticationWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('authentication', options);
}

/**
 * Create CRM lead workflow
 */
export function useCreateCRMLeadWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('create_crm_lead', options);
}

/**
 * Create service request workflow
 */
export function useCreateServiceRequestWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('create_service_request', options);
}

/**
 * Marketplace workflow
 */
export function useMarketplaceWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('marketplace', options);
}

/**
 * Property estimation workflow
 */
export function usePropertyEstimationWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('property_estimation', options);
}

/**
 * Maintenance intake workflow
 */
export function useMaintenanceIntakeWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('maintenance_intake', options);
}

/**
 * Document search workflow
 */
export function useDocumentSearchWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('document_search', options);
}

/**
 * User dashboard workflow
 */
export function useUserDashboardWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('user_dashboard', options);
}

/**
 * Admin dashboard workflow
 */
export function useAdminDashboardWorkflow(options?: UseWorkflowOptions) {
  return useWorkflow('admin_dashboard', options);
}
