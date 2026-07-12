import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { useAuthStore } from '@auth';
import { LAWIM_BRAND_SLOGAN } from '@ui';
import type { ReactElement } from 'react';
import { WebApp } from '../apps/web/src/App';
import { AdminApp } from '../apps/admin/src/App';

const defaultDashboardSummary = {
  properties: 8,
  opportunities: 3,
  communications: 2,
  pendingTasks: 1
};

const defaultProjects = {
  data: [
    {
      id: 1,
      title: 'LAWIM Demo Project',
      status: 'active',
      project_type: 'purchase',
      objective: 'Acquire a property in Yaounde',
      location_city: 'Yaounde',
      budget_min: 25000000,
      budget_max: 50000000
    }
  ],
  message: 'mock'
};

const defaultAssistantSuggestions = {
  data: [
    { title: 'Explore a project', description: 'Review the active dossier' },
    { title: 'Search by intent', description: 'Ask LAWIM to guide the next step' }
  ],
  message: 'mock'
};

const defaultPropertyMatches = {
  data: [
    {
      score: 89,
      score_percent: 89,
      grade: 'excellent',
      summary: 'location +20; budget +15; type +10',
      eligible: true,
      breakdown: { location: 20, budget: 15, type: 10 },
      reasons: ['city:Yaounde', 'property_type:house', 'budget:25000000'],
      distance_km: null,
      weights: {},
      target_type: 'property',
      property: {
        id: 'property-1',
        title: 'Yaounde House',
        location: 'Yaounde',
        price: 32000000,
        type: 'house',
        status: 'available'
      }
    }
  ],
  message: 'mock'
};

const defaultPartnerMatches = {
  data: [
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
  ],
  message: 'mock'
};

function renderWithProviders(ui: ReactElement, initialEntries: string[] = ['/']) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={initialEntries}>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
}

function loginResponse(role: string, roles: string[], email: string, name: string, token = 'live-token') {
  return {
    data: {
      user: { id: 'u-1', name, role, email },
      token,
      roles
    },
    message: 'ok'
  };
}

beforeEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
  useAuthStore.setState({
    user: null,
    token: null,
    roles: [],
    isAuthenticated: false,
    isLoading: false,
    hasHydrated: false,
    sessionExpired: false,
    sessionUnavailable: false
  });
  vi.spyOn(apiSdk, 'getSession').mockResolvedValue({ data: null, message: 'mock' });
  vi.spyOn(apiSdk, 'getDashboardSummary').mockResolvedValue({ data: defaultDashboardSummary, message: 'mock' });
  vi.spyOn(apiSdk, 'getProjects').mockResolvedValue(defaultProjects as never);
  vi.spyOn(apiSdk, 'getAssistantSuggestions').mockResolvedValue(defaultAssistantSuggestions as never);
  vi.spyOn(apiSdk, 'askAssistant').mockImplementation(async (payload) => ({
    data: {
      reply: `I can help with: ${payload.message}`,
      suggestions: ['Review project dossier', 'Open a related module']
    },
    message: 'mock'
  }));
  vi.spyOn(apiSdk, 'getMatches').mockImplementation(async (query) => {
    if (query?.target_type === 'property') return defaultPropertyMatches as never;
    return defaultPartnerMatches as never;
  });
  vi.spyOn(apiSdk, 'logout').mockResolvedValue({ data: { success: true }, message: 'mock' });
});

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

describe('LAWIM frontend shell', () => {
  it('renders the unified landing page with branding and login form', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getAllByText(/LAWIM/).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(LAWIM_BRAND_SLOGAN)).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /identifiant|identifier|identifia/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /connexion|login/i })).toBeInTheDocument();
    expect(screen.getByText(/contact@lawim\.app/i)).toBeInTheDocument();
  });

  it('login form works and redirects to cockpit', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />);

    await user.type(screen.getByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('button', { name: /déconnexion|logout|comot/i })).toBeInTheDocument();
    expect(screen.queryByRole('textbox', { name: /identifiant|identifier|identifia/i })).not.toBeInTheDocument();
  });

  it('switches to register mode', async () => {
    const user = userEvent.setup();
    renderWithProviders(<WebApp />);

    await user.click(screen.getByRole('button', { name: /créer un compte|create account/i }));
    expect(await screen.findByRole('button', { name: /retour à la connexion|back to login/i })).toBeInTheDocument();
  });

  it('persists language selection', async () => {
    const user = userEvent.setup();
    const rendered = renderWithProviders(<WebApp />);

    const langSelect = await screen.findByRole('combobox', { name: /langue|language|languag/i });
    await user.selectOptions(langSelect, 'en');

    await waitFor(() => {
      expect(window.localStorage.getItem('lawim.language')).toBe('en');
    });

    rendered.unmount();
    renderWithProviders(<WebApp />);
    expect(await screen.findByRole('combobox', { name: /langue|language|languag/i })).toBeInTheDocument();
  });

  it('redirects authenticated user to cockpit', async () => {
    window.localStorage.setItem('lawim_token', 'agent-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({
      data: {
        user: { id: 'u-2', name: 'Agent User', role: 'agent', email: 'agent@lawim.app' },
        token: 'agent-token',
        roles: ['agent']
      },
      message: 'ok'
    });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    await waitFor(() => {
      expect(screen.queryByRole('textbox', { name: /identifiant|identifier/i })).not.toBeInTheDocument();
    });
  });

  it('clears session on logout', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />);

    await user.type(screen.getByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('button', { name: /déconnexion|logout|comot/i })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /déconnexion|logout|comot/i }));

    expect(screen.getByRole('button', { name: /connexion|login/i })).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
  });

  it('renders the administration shell', () => {
    renderWithProviders(<AdminApp />);
    expect(screen.getByRole('heading', { name: /manage operations and oversight/i })).toBeInTheDocument();
  });

  it('renders the financial hub and initiates a Campay payment', async () => {
    const user = userEvent.setup();
    window.localStorage.setItem('lawim_token', 'financial-token');
    useAuthStore.setState({
      user: { id: 'u-1', name: 'Finance Admin', role: 'admin', email: 'admin@lawim.app' },
      token: 'financial-token',
      roles: ['admin'],
      isAuthenticated: true,
      isLoading: false,
      hasHydrated: true,
      sessionExpired: false,
      sessionUnavailable: false
    });
    vi.mocked(apiSdk.getSession).mockResolvedValue({
      data: {
        user: { id: 'u-1', name: 'Finance Admin', role: 'admin', email: 'admin@lawim.app' },
        token: 'financial-token',
        roles: ['admin']
      },
      message: 'ok'
    });
    vi.spyOn(apiSdk, 'listInvoices').mockResolvedValue({
      data: [
        {
          id: 42,
          number: 'FAC-2026-000042',
          status: 'ISSUED',
          currency: 'XAF',
          total_minor: 2500,
          balance_minor: 2500,
          amount_paid_minor: 0,
          lines: []
        }
      ],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'listReceipts').mockResolvedValue({
      data: [{ id: 5, number: 'REC-2026-000005', status: 'GENERATED', currency: 'XAF', amount_minor: 2500 }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'listPaymentIntents').mockResolvedValue({
      data: [{ id: 77, number: 'PAY-2026-000077', status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'listSubscriptions').mockResolvedValue({
      data: [{ id: 3, status: 'ACTIVE', customer_user_id: 1, plan_id: 2, renewal_mode: 'automatic' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'listOwnCommissions').mockResolvedValue({
      data: [{ id: 8, status: 'PAYABLE', amount_minor: 300, currency: 'XAF' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'listOwnPayouts').mockResolvedValue({
      data: [{ id: 9, status: 'APPROVED', amount_minor: 300, currency: 'XAF' }],
      message: 'mock'
    } as never);
    const createPaymentIntentSpy = vi.spyOn(apiSdk, 'createPaymentIntent').mockResolvedValue({
      data: { id: 88, number: 'PAY-2026-000088', status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY', phone_number_e164: '+237677000111' },
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'getPaymentStatus').mockResolvedValue({
      data: {
        payment_intent: { id: 88, number: 'PAY-2026-000088', status: 'SUCCEEDED' },
        provider_status: { status: 'SUCCESSFUL' }
      },
      message: 'mock'
    } as never);

    renderWithProviders(<WebApp />, ['/financial']);

    expect(await screen.findByRole('heading', { name: /financial hub/i })).toBeInTheDocument();
    expect(screen.getAllByText('FAC-2026-000042').length).toBeGreaterThan(0);
    await user.click(screen.getByRole('button', { name: /initier le paiement/i }));
    expect(createPaymentIntentSpy).toHaveBeenCalled();
    expect(createPaymentIntentSpy.mock.calls[0][0]).toMatchObject({
      invoice_id: 42,
      provider_code: 'CAMPAY',
      initiate: true
    });
    expect(await screen.findByText(/PAY-2026-000088/)).toBeInTheDocument();
  });

  it('renders the admin financial operations cockpit', async () => {
    vi.spyOn(apiSdk, 'adminGetProviderHealth').mockResolvedValue({
      data: {
        code: 'CAMPAY',
        name: 'Campay',
        status: 'active',
        environment: 'sandbox',
        available: true,
        details: { supports_collection: true }
      },
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminListPayments').mockResolvedValue({
      data: [{ id: 1, number: 'PAY-2026-000001', status: 'PENDING', amount_minor: 2500, currency: 'XAF', provider_code: 'CAMPAY' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminListReconciliationConflicts').mockResolvedValue({
      data: [{ id: 9, status: 'CONFLICT', conflict_type: 'amount_mismatch', currency: 'XAF' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminResolveReconciliation').mockResolvedValue({
      data: { id: 9, status: 'RESOLVED', conflict_type: 'amount_mismatch', currency: 'XAF' },
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminListRefunds').mockResolvedValue({
      data: [{ id: 5, number: 'AVR-2026-000005', status: 'APPROVED', amount_minor: 300, currency: 'XAF' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminListCommissions').mockResolvedValue({
      data: [{ id: 6, status: 'CALCULATED', amount_minor: 300, currency: 'XAF' }],
      message: 'mock'
    } as never);
    vi.spyOn(apiSdk, 'adminListProviderEvents').mockResolvedValue({
      data: [{ id: 7, provider_code: 'CAMPAY', event_type: 'webhook', provider_event_id: 'evt-7', status: 'RECEIVED' }],
      message: 'mock'
    } as never);

    render(
      <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })}>
        <MemoryRouter initialEntries={['/admin/financial']}>
          <AdminApp />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(await screen.findByRole('heading', { name: /financial operations/i })).toBeInTheDocument();
    expect(screen.getByText(/Campay provider health/i)).toBeInTheDocument();
    expect(await screen.findByText(/PAY-2026-000001/)).toBeInTheDocument();
  });
});
