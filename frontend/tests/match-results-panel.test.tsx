import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const createJsonResponse = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });

describe('MatchResultsPanel SDK methods', () => {
  beforeEach(() => {
    vi.resetModules();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('brainFindMatches sends correct API request', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/matching')) {
        return createJsonResponse({
          proposals_count: 2,
          properties_found: 1,
          partners_found: 1,
          proposals: [
            { id: 1, project_id: 1, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: 'Correspond à votre recherche', status: 'detected', proposed_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
          ]
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainFindMatches({ project_id: 1 });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(response.data.proposals_count).toBe(2);
    expect(response.data.proposals).toHaveLength(1);
    expect(response.data.proposals[0].status).toBe('detected');
    setApiBaseForTesting(null);
  });

  it('brainProposals lists proposals for a project', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/dossiers/1/matches')) {
        return createJsonResponse({
          proposals: [
            { id: 1, project_id: 1, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: 'Bon score', status: 'proposed', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
            { id: 2, project_id: 1, relation_type: 'person_to_partner', target_type: 'partner', target_id: 2, score: 72, justification: 'Professionnel', status: 'detected', created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
          ]
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainProposals(1);
    expect(response.data).toHaveLength(2);
    expect(response.data[0].status).toBe('proposed');
    expect(response.data[1].status).toBe('detected');
    setApiBaseForTesting(null);
  });

  it('brainAcceptProposal sends accept request', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/proposals/accept')) {
        return createJsonResponse({
          id: 1,
          project_id: 1,
          relation_type: 'person_to_property',
          target_type: 'property',
          target_id: 1,
          score: 85,
          justification: 'Bon score',
          status: 'accepted',
          accepted_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainAcceptProposal({ proposal_id: 1 });
    expect(response.data.status).toBe('accepted');
    expect(response.data.id).toBe(1);
    setApiBaseForTesting(null);
  });

  it('brainRejectProposal sends reject request', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/proposals/reject')) {
        return createJsonResponse({
          id: 1, project_id: 1, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: '', status: 'rejected', rejected_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainRejectProposal({ proposal_id: 1 });
    expect(response.data.status).toBe('rejected');
    setApiBaseForTesting(null);
  });

  it('brainGrantConsent sends consent grant request', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/consent/grant')) {
        return createJsonResponse({
          id: 1, project_id: 1, relation_type: 'person_to_property', target_type: 'property', target_id: 1, score: 85, justification: '', status: 'relation_established', consent_granted_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString()
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainGrantConsent({ proposal_id: 1 });
    expect(response.data.status).toBe('relation_established');
    setApiBaseForTesting(null);
  });

  it('brainRelations lists established relations', async () => {
    localStorage.setItem('lawim_token', 'test-token');
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'false';

    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes('/api/v2/assistant/brain/dossiers/1/relations')) {
        return createJsonResponse({
          relations: [
            { id: 1, project_id: 1, relation_type: 'person_to_property', source_type: 'proposal', source_id: 1, target_type: 'property', target_id: 1, status: 'relation_established', established_at: new Date().toISOString(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
          ]
        });
      }
      throw new Error(`Unexpected: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await import('../packages/api-sdk/src');
    setApiBaseForTesting('http://localhost/api');

    const response = await apiSdk.brainRelations(1);
    expect(response.data).toHaveLength(1);
    expect(response.data[0].status).toBe('relation_established');
    setApiBaseForTesting(null);
  });

  it('brainFindMatches works with mock mode', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainFindMatches({ project_id: 1 });
    expect(response.data.proposals_count).toBeGreaterThan(0);
    expect(response.data.proposals.length).toBeGreaterThan(0);
    setMockModeForTesting(null);
  });

  it('brainProposals shows mock proposals', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainProposals(1);
    expect(response.data).toHaveLength(1);
    setMockModeForTesting(null);
  });

  it('brainAcceptProposal returns accepted in mock mode', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainAcceptProposal({ proposal_id: 1 });
    expect(response.data.status).toBe('accepted');
    setMockModeForTesting(null);
  });

  it('brainRejectProposal returns rejected in mock mode', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainRejectProposal({ proposal_id: 1 });
    expect(response.data.status).toBe('rejected');
    setMockModeForTesting(null);
  });

  it('brainGrantConsent returns relation_established in mock mode', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainGrantConsent({ proposal_id: 1 });
    expect(response.data.status).toBe('relation_established');
    setMockModeForTesting(null);
  });

  it('brainRelations returns established relation in mock mode', async () => {
    const env = import.meta.env as Record<string, string | boolean | undefined>;
    env.VITE_LAWIM_USE_MOCKS = 'true';

    const { apiSdk, setMockModeForTesting } = await import('../packages/api-sdk/src');
    setMockModeForTesting(true);

    const response = await apiSdk.brainRelations(1);
    expect(response.data).toHaveLength(1);
    expect(response.data[0].status).toBe('relation_established');
    setMockModeForTesting(null);
  });
});
