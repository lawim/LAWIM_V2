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

function renderWithProviders(ui: ReactElement, initialEntries: any[] = ['/']) {
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
    if (query?.target_type === 'property') {
      return defaultPropertyMatches as never;
    }
    return defaultPartnerMatches as never;
  });
  vi.spyOn(apiSdk, 'logout').mockResolvedValue({ data: { success: true }, message: 'mock' });
});

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

describe('LAWIM frontend shell', () => {
  it('renders the public home page with branding', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('heading', { name: /l’immobilier autrement/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /bonjour\. nous pouvons reprendre un dossier ou en ouvrir un nouveau\./i })).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /connexion/i })).toHaveLength(2);
    expect(screen.getByRole('button', { name: /nouveau projet/i })).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(1);
    expect(screen.getByText(LAWIM_BRAND_SLOGAN)).toBeInTheDocument();
  });

  it.each([
    {
      language: 'fr',
      button: /connexion/i
    },
    {
      language: 'en',
      button: /login/i
    },
    {
      language: 'pcm',
      button: /login/i
    }
  ])('renders the login page in $language', async ({ language, button }) => {
    window.localStorage.setItem('lawim.language', language);

    renderWithProviders(<WebApp />, ['/login']);

    expect(screen.getByText(LAWIM_BRAND_SLOGAN)).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(1);
    expect(screen.getByText(/contact@lawim\.app/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /^lawim\.app$/i })).toHaveAttribute('href', 'https://lawim.app');
    expect(screen.getByRole('combobox', { name: /langue|language|languag/i })).toBeInTheDocument();
    expect(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }, { timeout: 10000 })).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: button }, { timeout: 10000 })).toBeInTheDocument();
  });

  it('switches the access card to the register form and back', async () => {
    const user = userEvent.setup();
    renderWithProviders(<WebApp />, ['/login']);

    await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i });
    await user.click(screen.getByRole('button', { name: /créer un compte|create account/i }));

    expect(await screen.findByLabelText(/numéro whatsapp|whatsapp number/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retour à la connexion|back to login/i })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /retour à la connexion|back to login/i }));

    expect(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i })).toBeInTheDocument();
  });

  it('persists the selected language across remounts', async () => {
    const user = userEvent.setup();
    const rendered = renderWithProviders(<WebApp />, ['/login']);

    const select = await screen.findByLabelText(/langue|language|languag/i);
    await user.selectOptions(select, 'en');

    await waitFor(() => {
      expect(window.localStorage.getItem('lawim.language')).toBe('en');
    });
    expect(await screen.findByRole('button', { name: /login/i }, { timeout: 10000 })).toBeInTheDocument();

    rendered.unmount();
    renderWithProviders(<WebApp />, ['/login']);

    expect(await screen.findByRole('button', { name: /login/i }, { timeout: 10000 })).toBeInTheDocument();
    expect(screen.getByText(/contact@lawim\.app/i)).toBeInTheDocument();
  });

  it('logs in and lands on the cockpit without the login form', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /cockpit administrateur/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /bonjour admin user\. la supervision de la plateforme reste active\./i, level: 2 })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /continuer la conversation/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /déconnexion|logout/i })).toBeInTheDocument();
    expect(screen.getAllByText(/^administrateur$/i)).toHaveLength(2);
    expect(screen.queryByLabelText(/identifiant|identifier|identifia/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/mot de passe|password/i)).not.toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /langue|language|languag/i })).toBeInTheDocument();
  });

  it('shows a loading state on the login button while the request is pending', async () => {
    const user = userEvent.setup();
    let resolveLogin: (value: any) => void = () => undefined;
    const pendingLogin = new Promise<any>((resolve) => {
      resolveLogin = resolve;
    });
    vi.spyOn(apiSdk, 'login').mockImplementation(() => pendingLogin);

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    const button = screen.getByRole('button', { name: /connexion|login/i });
    await waitFor(() => {
      expect(button).toBeDisabled();
      expect(button).toHaveAttribute('aria-busy', 'true');
    });

    resolveLogin(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    expect(await screen.findByText(/bonjour admin user/i)).toBeInTheDocument();
  });

  it('opens the conversation studio from the cockpit and returns to it', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /cockpit administrateur/i, level: 1 })).toBeInTheDocument();

    await user.click(screen.getByRole('link', { name: /continuer la conversation/i }));

    expect(await screen.findByRole('heading', { name: /conversation/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retour au cockpit/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /message/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /web/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /whatsapp/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /telegram/i })).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /retour au cockpit/i }));

    expect(await screen.findByRole('heading', { name: /cockpit administrateur/i, level: 1 })).toBeInTheDocument();
  });

  it('exposes the conversation studio controls from the cockpit', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /cockpit administrateur/i, level: 1 })).toBeInTheDocument();
    await user.click(screen.getByRole('link', { name: /continuer la conversation/i }));

    expect(await screen.findByRole('heading', { name: /conversation/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /projet/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /message/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^continuer$/i })).toBeInTheDocument();
  });

  it('guides the property workflow through progressive steps', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('user', ['user'], 'user@lawim.app', 'User Demo'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'user@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /cockpit utilisateur/i, level: 1 })).toBeInTheDocument();
    await user.click(screen.getByRole('link', { name: /découvrir un bien/i }));

    expect(await screen.findByRole('heading', { name: /biens/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /quel est votre projet/i, level: 2 })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /intention/i })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /type de bien/i })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /mode de localisation/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /budget max/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /titre foncier/i })).toBeInTheDocument();

    await user.selectOptions(screen.getByRole('combobox', { name: /type de bien/i }), 'maison');

    expect(screen.getByRole('textbox', { name: /chambres/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /salles de bain/i })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /standing/i })).toBeInTheDocument();

    expect(screen.getByRole('button', { name: /continuer/i })).toBeInTheDocument();
  });

  it('clears the session on logout', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('button', { name: /déconnexion|logout/i })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /déconnexion|logout/i }));

    expect(screen.getByText(LAWIM_BRAND_SLOGAN)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /connexion|login/i })).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
  });

  it('redirects an unauthenticated protected route to login without a session-expired banner', async () => {
    renderWithProviders(<WebApp />, ['/login']);

    expect(await screen.findByText(LAWIM_BRAND_SLOGAN)).toBeInTheDocument();
    expect(screen.queryByText(/votre session a expiré/i)).not.toBeInTheDocument();
  });

  it('shows a session-expired banner when an existing token cannot be restored', async () => {
    window.localStorage.setItem('lawim_token', 'orphan-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'mock' });

    renderWithProviders(<WebApp />, [{ pathname: '/login', state: { reason: 'session_expired' } }]);

    expect(await screen.findByText(/votre session a expiré\. connectez-vous de nouveau\./i)).toBeInTheDocument();
  });

  it('shows a server-unavailable banner when session refresh fails with a 5xx error', async () => {
    window.localStorage.setItem('lawim_token', 'stale-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'Request failed with 500' });

    renderWithProviders(<WebApp />, [{ pathname: '/login', state: { reason: 'server_unavailable' } }]);

    expect(await screen.findByText(/serveur indisponible\. réessayez dans un instant\./i)).toBeInTheDocument();
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

    expect(await screen.findByRole('heading', { name: /cockpit agent lawim/i, level: 1 })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /cockpit administrateur/i, level: 1 })).not.toBeInTheDocument();
  });

  it('emits controlled auth traces during a successful login', async () => {
    window.localStorage.setItem('lawim.debug.auth', '1');
    const debugSpy = vi.spyOn(console, 'debug').mockImplementation(() => undefined);
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await screen.findByRole('heading', { name: /connexion/i, level: 1 });
    debugSpy.mockClear();

    await user.type(screen.getByRole('textbox', { name: /identifiant|identifier|identifia/i }), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/mot de passe|password/i), 'LAWIM@Demo2026µ');
    await user.click(screen.getByRole('button', { name: /connexion|login/i }));

    expect(await screen.findByRole('heading', { name: /cockpit administrateur/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /bonjour admin user\. la supervision de la plateforme reste active\./i, level: 2 })).toBeInTheDocument();
    await waitFor(() => {
      expect(debugSpy.mock.calls.map(([label]) => label)).toEqual([
        'LOGIN_OK',
        'ROLE_RESOLVED',
        'COCKPIT_SELECTED',
        'APPLY_COCKPIT',
        'COCKPIT_RENDERED'
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
