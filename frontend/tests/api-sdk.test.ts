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
    const { apiSdk, setMockModeForTesting } = await loadApiSdkModule();
    setMockModeForTesting(true);

    const response = await apiSdk.getProperties();

    expect(response.data.length).toBeGreaterThan(0);
    expect(response.data[0]).toHaveProperty('title');
    setMockModeForTesting(null);
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

    const loginResponse = await apiSdk.login({ identifier: 'admin@lawim.local', password: 'LAWIM@Demo2026µ' });
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
      password: 'LAWIM@Demo2026µ',
      password_confirmation: 'LAWIM@Demo2026µ',
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

  it('targets /api/v2/backup/status and exposes the backup summary cards', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/v2/backup/status')) {
        return createJsonResponse({
          global_status: 'PROTECTED',
          policy: {
            google_drive: { time: ['02:00', '14:30'], timezone: 'Africa/Douala' },
            retention: { google_drive_days: 30 }
          },
          last_backup: {
            backup_id: 'LAWIM-20260711-020000',
            finished_at: '2026-07-11T02:00:00+00:00'
          },
          next_backup: {
            next_run_at: '2026-07-11T14:30:00+00:00'
          },
          metrics: {
            rpo_seconds: 3600,
            rto_seconds: 180,
            availability_percent: 99.9
          }
        });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const response = await apiSdk.getBackupStatus();

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/v2/backup/status');
    expect(response.data.map((item) => item.label)).toContain('Retention');
    expect(response.data.map((item) => item.label)).toContain('Global status');
    setApiBaseForTesting(null);
  });

  it('targets /api/v2/backup/run when orchestrating a backup job', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/v2/backup/run')) {
        expect(init?.method).toBe('POST');
        expect(JSON.parse(String(init?.body))).toMatchObject({
          kind: 'postgresql',
          destination: 'local',
          provider_name: 'google-drive'
        });
        return createJsonResponse({
          identifier: 'job-1',
          backup_id: 'LAWIM-20260711-020000',
          kind: 'postgresql',
          state: 'RUNNING'
        });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const response = await apiSdk.runBackup({
      kind: 'postgresql',
      destination: 'local',
      provider_name: 'google-drive',
      trigger: 'cockpit'
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/v2/backup/run');
    expect(response.data.backup_id).toBe('LAWIM-20260711-020000');
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

  it('loads projects and posts property creations through the sdk', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/v2/projects')) {
        return createJsonResponse([
          {
            id: '7',
            title: 'Yaounde Build',
            status: 'active',
            project_type: 'build',
            objective: 'Construct a duplex in Yaounde',
            location_city: 'Yaounde',
            budget_min: '12000000',
            budget_max: '18000000'
          }
        ]);
      }

      if (url.endsWith('/api/properties') && init?.method === 'POST') {
        expect(JSON.parse(String(init.body))).toMatchObject({
          title: 'Terrain Bonaberi',
          summary: 'Terrain with easy access',
          city: 'Douala',
          country: 'Cameroon',
          property_type: 'terrain'
        });
        return createJsonResponse(
          {
            id: 'prop-1',
            title: 'Terrain Bonaberi',
            city: 'Douala',
            region: 'Littoral',
            country: 'Cameroon',
            price_max: 12000000,
            property_type: 'terrain',
            status: 'draft'
          },
          201
        );
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const projects = await apiSdk.getProjects();
    const created = await apiSdk.createProperty({
      title: 'Terrain Bonaberi',
      summary: 'Terrain with easy access',
      city: 'Douala',
      country: 'Cameroon',
      price_max: 12000000,
      property_type: 'terrain',
      status: 'draft'
    });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/v2/projects');
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.lawim.app/api/properties');
    expect(projects.data[0]).toMatchObject({
      id: 7,
      title: 'Yaounde Build',
      status: 'active',
      project_type: 'build',
      objective: 'Construct a duplex in Yaounde',
      location_city: 'Yaounde',
      budget_min: 12000000,
      budget_max: 18000000
    });
    expect(created.data).toMatchObject({
      id: 'prop-1',
      title: 'Terrain Bonaberi',
      location: 'Douala • Littoral',
      price: 12000000,
      type: 'terrain',
      status: 'draft'
    });
    setApiBaseForTesting(null);
  });

  it('targets the financial core endpoints for catalog, pricing, quotes, invoices and payment intents', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/v2/financial/catalog/products?status=active&limit=2')) {
        return createJsonResponse({ products: [{ id: 1, code: 'FIN-001', name: 'Finance', status: 'active' }] });
      }

      if (url.endsWith('/api/v2/financial/pricing/calculate')) {
        expect(JSON.parse(String(init?.body))).toMatchObject({
          currency: 'XAF',
          discount_minor: 100,
          fee_minor: 50
        });
        return createJsonResponse({
          subtotal_minor: 2500,
          discount_minor: 100,
          fee_minor: 50,
          tax_minor: 0,
          total_minor: 2450,
          currency: 'XAF',
          lines: [{ description: 'Service', quantity: 1, unit_price_minor: 2500 }]
        });
      }

      if (url.endsWith('/api/v2/financial/quotes')) {
        return createJsonResponse({
          id: 11,
          number: 'DEV-2026-000011',
          status: 'ISSUED',
          currency: 'XAF',
          total_minor: 2500,
          lines: [{ description: 'Service', quantity: 1, unit_price_minor: 2500 }]
        }, 201);
      }

      if (url.endsWith('/api/v2/financial/payments/intents')) {
        expect(JSON.parse(String(init?.body))).toMatchObject({
          invoice_id: 44,
          provider_code: 'CAMPAY',
          initiate: true
        });
        return createJsonResponse({
          id: 77,
          number: 'PAY-2026-000077',
          status: 'PENDING',
          amount_minor: 2500,
          currency: 'XAF',
          provider_code: 'CAMPAY',
          phone_number_e164: '+237677000111'
        }, 201);
      }

      if (url.endsWith('/api/v2/financial/payments/intents/77/status')) {
        return createJsonResponse({
          payment_intent: { id: 77, number: 'PAY-2026-000077', status: 'SUCCEEDED' },
          provider_status: { status: 'SUCCESSFUL', provider_reference: 'campay-77' }
        });
      }

      if (url.endsWith('/api/v2/financial/receipts?limit=2')) {
        return createJsonResponse({ receipts: [{ id: 3, number: 'REC-2026-000003', status: 'GENERATED', currency: 'XAF', amount_minor: 2500 }] });
      }

      if (url.endsWith('/api/v2/financial/subscriptions?limit=2')) {
        return createJsonResponse({ subscriptions: [{ id: 4, status: 'ACTIVE', customer_user_id: 1, plan_id: 2, renewal_mode: 'automatic' }] });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const products = await apiSdk.listFinancialProducts({ status: 'active', limit: 2 });
    const pricing = await apiSdk.calculatePrice({
      line_items: [{ description: 'Service', quantity: 1, unit_price_minor: 2500 }],
      discount_minor: 100,
      fee_minor: 50,
      tax_rate_bps: 0,
      currency: 'XAF'
    });
    const quote = await apiSdk.createQuote({ customer_user_id: 1, lines: [{ description: 'Service', quantity: 1, unit_price_minor: 2500 }], currency: 'XAF' });
    const intent = await apiSdk.createPaymentIntent({
      invoice_id: 44,
      amount_minor: 2500,
      currency: 'XAF',
      provider_code: 'CAMPAY',
      channel: 'mobile_money',
      phone_number_e164: '+237677000111',
      initiate: true,
      idempotency_key: 'intent-77'
    });
    const status = await apiSdk.getPaymentStatus(77);
    const receipts = await apiSdk.listReceipts({ limit: 2 });
    const subscriptions = await apiSdk.listSubscriptions({ limit: 2 });

    expect(fetchMock).toHaveBeenCalledTimes(7);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/v2/financial/catalog/products?status=active&limit=2');
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.lawim.app/api/v2/financial/pricing/calculate');
    expect(fetchMock.mock.calls[2][0]).toBe('https://api.lawim.app/api/v2/financial/quotes');
    expect(fetchMock.mock.calls[3][0]).toBe('https://api.lawim.app/api/v2/financial/payments/intents');
    expect(fetchMock.mock.calls[4][0]).toBe('https://api.lawim.app/api/v2/financial/payments/intents/77/status');
    expect(fetchMock.mock.calls[5][0]).toBe('https://api.lawim.app/api/v2/financial/receipts?limit=2');
    expect(fetchMock.mock.calls[6][0]).toBe('https://api.lawim.app/api/v2/financial/subscriptions?limit=2');
    expect(products.data[0].code).toBe('FIN-001');
    expect(pricing.data.total_minor).toBe(2450);
    expect(quote.data.status).toBe('ISSUED');
    expect(intent.data.number).toBe('PAY-2026-000077');
    expect(status.data.payment_intent).toBeDefined();
    expect(receipts.data[0].number).toBe('REC-2026-000003');
    expect(subscriptions.data[0].status).toBe('ACTIVE');
    setApiBaseForTesting(null);
  });

  it('targets the admin financial endpoints for provider health and reconciliation', async () => {
    testEnv.VITE_LAWIM_USE_MOCKS = 'false';

    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/v2/financial/providers/health')) {
        return createJsonResponse({
          code: 'CAMPAY',
          name: 'Campay',
          status: 'active',
          environment: 'sandbox',
          available: true,
          details: { supports_collection: true }
        });
      }

      if (url.endsWith('/api/v2/financial/reconciliation?status=CONFLICT&limit=5')) {
        return createJsonResponse({ records: [{ id: 9, status: 'CONFLICT', conflict_type: 'amount_mismatch', currency: 'XAF' }] });
      }

      if (url.endsWith('/api/v2/financial/reconciliation/9/resolve')) {
        expect(JSON.parse(String(init?.body))).toMatchObject({
          status: 'RESOLVED',
          resolution_note: 'Checked in admin cockpit'
        });
        return createJsonResponse({ id: 9, status: 'RESOLVED', conflict_type: 'amount_mismatch', currency: 'XAF' });
      }

      if (url.endsWith('/api/v2/financial/refunds?limit=3')) {
        return createJsonResponse({ refunds: [{ id: 5, number: 'AVR-2026-000005', status: 'APPROVED', amount_minor: 300, currency: 'XAF' }] });
      }

      if (url.endsWith('/api/v2/financial/commissions?limit=3')) {
        return createJsonResponse({ commissions: [{ id: 6, status: 'CALCULATED', amount_minor: 300, currency: 'XAF' }] });
      }

      if (url.endsWith('/api/v2/financial/provider-events?limit=3')) {
        return createJsonResponse({ provider_events: [{ id: 7, provider_code: 'CAMPAY', event_type: 'webhook', provider_event_id: 'evt-7', status: 'RECEIVED' }] });
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    const { apiSdk, setApiBaseForTesting } = await loadApiSdkModule();
    setApiBaseForTesting('https://api.lawim.app');

    const health = await apiSdk.adminGetProviderHealth();
    const conflicts = await apiSdk.adminListReconciliationConflicts({ status: 'CONFLICT', limit: 5 });
    const resolved = await apiSdk.adminResolveReconciliation(9, { status: 'RESOLVED', resolution_note: 'Checked in admin cockpit' });
    const refunds = await apiSdk.adminListRefunds({ limit: 3 });
    const commissions = await apiSdk.adminListCommissions({ limit: 3 });
    const events = await apiSdk.adminListProviderEvents({ limit: 3 });

    expect(fetchMock).toHaveBeenCalledTimes(6);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.lawim.app/api/v2/financial/providers/health');
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.lawim.app/api/v2/financial/reconciliation?status=CONFLICT&limit=5');
    expect(fetchMock.mock.calls[2][0]).toBe('https://api.lawim.app/api/v2/financial/reconciliation/9/resolve');
    expect(health.data.available).toBe(true);
    expect(conflicts.data[0].status).toBe('CONFLICT');
    expect(resolved.data.status).toBe('RESOLVED');
    expect(refunds.data[0].number).toBe('AVR-2026-000005');
    expect(commissions.data[0].status).toBe('CALCULATED');
    expect(events.data[0].provider_event_id).toBe('evt-7');
    setApiBaseForTesting(null);
  });
});
