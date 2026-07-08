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

function loginResponse(role: string | undefined, roles: string[], email: string, name: string, token = 'live-token', message = 'ok'): any {
  return {
    data: {
      user: {
        id: 'u-1',
        name,
        role,
        email
      },
      token,
      roles
    },
    message
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
  vi.spyOn(apiSdk, 'getMatches').mockResolvedValue(defaultPartnerMatches as never);
  vi.spyOn(apiSdk, 'logout').mockResolvedValue({ data: { success: true }, message: 'mock' });
});

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

describe('LAWIM frontend shell', () => {
  it('renders the public home page with branding', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('heading', { name: /cockpit moderne/i })).toBeInTheDocument();
    expect(screen.getByRole('navigation', { name: /primary/i })).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(2);
    expect(screen.getAllByText(LAWIM_BRAND_SLOGAN)).toHaveLength(2);
  });

  it.each([
    {
      language: 'fr',
      heading: /connexion sécurisée/i,
      subtitle: /entrez votre email et votre mot de passe pour ouvrir votre cockpit\./i
    },
    {
      language: 'en',
      heading: /secure login/i,
      subtitle: /use your email and password to open your cockpit\./i
    },
    {
      language: 'pcm',
      heading: /safe login/i,
      subtitle: /put your email and password make you open your cockpit\./i
    }
  ])('renders the login page in $language', async ({ language, heading, subtitle }) => {
    window.localStorage.setItem('lawim.language', language);

    renderWithProviders(<WebApp />, ['/login']);

    expect(await screen.findByRole('heading', { name: heading, level: 1 })).toBeInTheDocument();
    expect(screen.getByText(subtitle)).toBeInTheDocument();
  });

  it('persists the selected language across remounts', async () => {
    const user = userEvent.setup();
    const rendered = renderWithProviders(<WebApp />, ['/login']);

    const select = await screen.findByLabelText(/langue|language|languag/i);
    await user.selectOptions(select, 'en');

    await waitFor(() => {
      expect(window.localStorage.getItem('lawim.language')).toBe('en');
    });
    expect(await screen.findByRole('heading', { name: /secure login/i, level: 1 })).toBeInTheDocument();

    rendered.unmount();
    renderWithProviders(<WebApp />, ['/login']);

    expect(await screen.findByRole('heading', { name: /secure login/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByText(/use your email and password to open your cockpit\./i)).toBeInTheDocument();
  });

  it('logs in and shows a compact authenticated header without the login form', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /bonjour admin user/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /déconnexion|logout/i })).toBeInTheDocument();
    expect(screen.getByText(/vous êtes connecté en tant que administrateur\./i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/email/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/mot de passe|password/i)).not.toBeInTheDocument();
  });

  it('opens module cards in dedicated screens and returns to the dashboard', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /bonjour admin user/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /chaque carte ouvre un espace dédié/i, level: 2 })).toBeInTheDocument();

    await user.click(screen.getByRole('link', { name: /partenaires/i }));

    expect(await screen.findByRole('heading', { name: /partenaires/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retour au tableau de bord|back to dashboard/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ouvrir|open/i })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /retour au tableau de bord|back to dashboard/i }));

    expect(await screen.findByRole('heading', { name: /bonjour admin user/i, level: 1 })).toBeInTheDocument();
  });

  it('clears the session on logout', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('button', { name: /déconnexion|logout/i })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /déconnexion|logout/i }));

    expect(await screen.findByRole('heading', { name: /connexion sécurisée|secure login|safe login/i, level: 1 })).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
  });

  it('redirects an unauthenticated protected route to login without a session-expired banner', async () => {
    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /connexion sécurisée/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByText(/connectez-vous pour accéder à votre espace\./i)).toBeInTheDocument();
    expect(screen.queryByText(/votre session a expiré/i)).not.toBeInTheDocument();
  });

  it('shows a session-expired banner when an existing token cannot be restored', async () => {
    window.localStorage.setItem('lawim_token', 'orphan-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'mock' });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /connexion sécurisée/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByText(/votre session a expiré\. connectez-vous de nouveau\./i)).toBeInTheDocument();
  });

  it('shows a server-unavailable banner when session refresh fails with a 5xx error', async () => {
    window.localStorage.setItem('lawim_token', 'stale-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'Request failed with 500' });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /connexion sécurisée/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByText(/serveur indisponible\. réessayez dans un instant\./i)).toBeInTheDocument();
  });

  it('redirects authenticated users to the dashboard matching the resolved role', async () => {
    window.localStorage.setItem('lawim_token', 'agent-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({
      data: {
        user: {
          id: 'u-2',
          name: 'Agent User',
          role: 'agent',
          email: 'agent@lawim.app'
        },
        token: 'agent-token',
        roles: ['agent']
      },
      message: 'ok'
    });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /bonjour agent user/i, level: 1 })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /bonjour admin user/i, level: 1 })).not.toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(1);
  });

  it('emits controlled auth traces during a successful login', async () => {
    window.localStorage.setItem('lawim.debug.auth', '1');
    const debugSpy = vi.spyOn(console, 'debug').mockImplementation(() => undefined);
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await screen.findByRole('heading', { name: /connexion sécurisée/i, level: 1 });
    debugSpy.mockClear();

    await user.type(screen.getByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /bonjour admin user/i, level: 1 })).toBeInTheDocument();
    await waitFor(() => {
      expect(debugSpy.mock.calls.map(([label]) => label)).toEqual([
        'LOGIN_OK',
        'ROLE_RESOLVED',
        'DASHBOARD_SELECTED',
        'APPLY_JOURNEY',
        'DASHBOARD_RENDERED'
      ]);
    });
  });

  it('renders the administration shell', () => {
    renderWithProviders(<AdminApp />);

    expect(screen.getByRole('heading', { name: /manage operations and oversight/i })).toBeInTheDocument();
    expect(screen.getByText(/administrative controls, governance workflows, and deployment readiness in one place/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /operations/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /agents/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /credential vault/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /drive security/i })).toBeInTheDocument();
  });
});
