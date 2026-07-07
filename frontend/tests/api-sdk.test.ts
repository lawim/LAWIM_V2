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

    const loginResponse = await apiSdk.login({ email: 'admin@lawim.local', password: 'lawim-demo' });
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
});
