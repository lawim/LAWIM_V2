import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const testEnv = import.meta.env as Record<string, string | boolean | undefined>;

const loadApiSdkModule = async () => import('../packages/api-sdk/src');

const createJsonResponse = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json'
    }
  });

describe('apiSdk', () => {
  beforeEach(() => {
    vi.resetModules();
    vi.restoreAllMocks();
    testEnv.VITE_LAWIM_API_URL = undefined;
    testEnv.VITE_LAWIM_USE_MOCKS = undefined;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    testEnv.VITE_LAWIM_API_URL = undefined;
    testEnv.VITE_LAWIM_USE_MOCKS = undefined;
  });

  it('returns mock properties when mock mode is enabled', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'true';
    const { apiSdk } = await loadApiSdkModule();

    const response = await apiSdk.getProperties();

    expect(response.data.length).toBeGreaterThan(0);
    expect(response.data[0]).toHaveProperty('title');
  });

  it('normalizes partner matches returned by /api/matches', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/matches?target_type=partner&need=photographe&city=Douala&limit=5')) {
        return createJsonResponse({
          matches: [
            {
              score: 94,
              score_percent: 94,
              grade: 'excellent',
              summary: 'need +25; location +20; language +10',
              eligible: true,
              breakdown: { need: 25, location: 20, language: 10 },
              reasons: ['partner_type:photographer', 'city:Douala'],
              distance_km: null,
              weights: {},
              target_type: 'partner',
              partner: {
                id: 'partner-1',
                partner_type: 'photographer',
                display_name: 'LAWIM Studio Photo',
                description: 'Photographe immobilier et événementiel'
              }
            }
          ]
        });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const response = await apiSdk.getMatches({ target_type: 'partner', need: 'photographe', city: 'Douala', limit: 5 });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/matches?target_type=partner&need=photographe&city=Douala&limit=5');
    expect(response.data).toHaveLength(1);
    expect(response.data[0].target_type).toBe('partner');
    expect(response.data[0].reasons).toContain('partner_type:photographer');
    setApiBaseForTesting(null);
  });

  it('targets /api/auth/login and /api/v2/dashboard when the API base is an origin', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/auth/login')) {
        return createJsonResponse(
          {
            user: {
              id: 'u-1',
              name: 'Admin User',
              role: 'admin',
              email: 'admin@lawim.local'
            },
            token: 'live-token',
            roles: ['admin']
          },
          201
        );
      }

      if (url.endsWith('/api/v2/dashboard')) {
        return createJsonResponse({
          properties: 8,
          opportunities: 3,
          communications: 2,
          pendingTasks: 1
        });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const loginResponse = await apiSdk.login({ identifier: 'admin@lawim.local', password: 'lawim-demo' });
    const summaryResponse = await apiSdk.getDashboardSummary();

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/auth/login');
    expect(fetchMock.mock.calls[0][1]?.method).toBe('POST');
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.lawim.app/api/v2/dashboard');
    expect(loginResponse.message).toBe('ok');
    expect(summaryResponse.data).toEqual({
      properties: 8,
      opportunities: 3,
      communications: 2,
      pendingTasks: 1
    });
    setApiBaseForTesting(null);
  });

  it('targets /api/auth/register with the public account payload', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/auth/register')) {
        return createJsonResponse(
          {
            user: {
              id: 'u-3',
              name: 'Owner Demo',
              full_name: 'Owner Demo',
              role: 'user',
              email: 'owner@example.local',
              username: 'owner_demo',
              phone_e164: '+237690000004',
              preferred_language: 'fr'
            },
            token: 'registered-token',
            roles: ['user']
          },
          201
        );
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const response = await apiSdk.register({
      full_name: 'Owner Demo',
      email: 'owner@example.local',
      username: 'owner_demo',
      phone_e164: '+237690000004',
      password: 'lawim-demo',
      password_confirmation: 'lawim-demo',
      preferred_language: 'fr',
      accept_terms: true
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/auth/register');
    expect(fetchMock.mock.calls[0][1]?.method).toBe('POST');
    expect(response.data.user.role).toBe('user');
    expect(response.data.token).toBe('registered-token');
    setApiBaseForTesting(null);
  });

  it('targets /api/matches for partner recommendations when the API base is an origin', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/matches?target_type=partner&need=architecte&city=Yaounde&project_type=build&limit=3')) {
        return createJsonResponse({
          matches: [
            {
              score: 91,
              score_percent: 91,
              grade: 'excellent',
              summary: 'need +25; location +20; compatibility +10',
              eligible: true,
              breakdown: { need: 25, location: 20, compatibility: 10 },
              reasons: ['partner_type:architect', 'city:Yaounde'],
              distance_km: null,
              weights: {},
              target_type: 'partner',
              partner: {
                id: 'partner-2',
                partner_type: 'architect',
                display_name: 'LAWIM Architecture'
              }
            }
          ],
          criteria: {
            target_type: 'partner',
            partner_type: 'architect'
          },
          explanation: {
            target_type: 'partner',
            need: 'architecte',
            partner_type: 'architect'
          }
        });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const response = await apiSdk.getMatches({ target_type: 'partner', need: 'architecte', city: 'Yaounde', project_type: 'build', limit: 3 });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/matches?target_type=partner&need=architecte&city=Yaounde&project_type=build&limit=3');
    expect(response.data[0].target_type).toBe('partner');
    expect(response.data[0].reasons).toContain('partner_type:architect');
    setApiBaseForTesting(null);
  });
});
