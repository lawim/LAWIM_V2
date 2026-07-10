import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import type { ReactElement } from 'react';
import { WebApp } from '../apps/web/src/App';
import { useAuthStore } from '@auth';

const mockProjects = { data: [{ id: 1, title: 'Projet Test', status: 'active', project_type: 'purchase', objective: 'Test', location_city: 'Douala', budget_min: 10000000, budget_max: 50000000 }], message: 'mock' };
const mockSummary = { properties: 5, opportunities: 2, communications: 1, pendingTasks: 0 };

function authState(role: string | null) {
  useAuthStore.setState({
    user: role ? { id: 'u-1', name: 'Test User', role, email: 'test@lawim.app' } : null,
    token: role ? 'test-token' : null,
    roles: role ? [role] : [],
    isAuthenticated: Boolean(role),
    isLoading: false,
    hasHydrated: true,
    sessionExpired: false,
    sessionUnavailable: false
  });
  if (role) {
    vi.mocked(apiSdk.getSession).mockResolvedValue({
      data: { user: { id: 'u-1', name: 'Test User', role, email: 'test@lawim.app' }, token: 'test-token', roles: [role] },
      message: 'ok'
    });
  }
}

function renderApp(language: string, initialEntries: string[] = ['/']) {
  window.localStorage.setItem('lawim.language', language);
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={qc}><MemoryRouter initialEntries={initialEntries}><WebApp /></MemoryRouter></QueryClientProvider>);
}

beforeEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
  authState(null);
  vi.spyOn(apiSdk, 'getSession').mockResolvedValue({ data: null, message: 'mock' });
  vi.spyOn(apiSdk, 'getDashboardSummary').mockResolvedValue({ data: mockSummary, message: 'mock' });
  vi.spyOn(apiSdk, 'getProjects').mockResolvedValue(mockProjects as never);
  vi.spyOn(apiSdk, 'getAssistantSuggestions').mockResolvedValue({ data: [], message: 'mock' });
  vi.spyOn(apiSdk, 'askAssistant').mockResolvedValue({ data: { reply: 'Réponse test', suggestions: [] }, message: 'mock' });
  vi.spyOn(apiSdk, 'getMatches').mockResolvedValue({ data: [], message: 'mock' });
  vi.spyOn(apiSdk, 'getFavorites').mockResolvedValue({ data: [], message: 'mock' });
  vi.spyOn(apiSdk, 'getNotifications').mockResolvedValue({ data: [], message: 'mock' });
  vi.spyOn(apiSdk, 'getProperties').mockResolvedValue({ data: [], message: 'mock' });
  vi.spyOn(apiSdk, 'logout').mockResolvedValue({ data: { success: true }, message: 'mock' });
});

afterEach(() => { window.localStorage.clear(); vi.restoreAllMocks(); });

describe('i18n — Landing page in 3 languages', () => {
  it('renders in French', () => {
    renderApp('fr');
    expect(screen.getByRole('textbox', { name: /identifiant/i })).toBeInTheDocument();
  });
  it('renders in English', () => {
    renderApp('en');
    expect(screen.getByRole('textbox', { name: /identifier/i })).toBeInTheDocument();
  });
  it('renders in Pidgin', () => {
    renderApp('pcm');
    expect(screen.getByRole('textbox', { name: /identifia/i })).toBeInTheDocument();
  });
  it('shows footer with coordinates in French', () => {
    renderApp('fr');
    expect(screen.getAllByText(/lawim/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/contact@lawim\.app/i)).toBeInTheDocument();
  });
  it('shows create account button in French', () => {
    renderApp('fr');
    expect(screen.getByRole('button', { name: /créer un compte|create account/i })).toBeInTheDocument();
  });
});

describe('i18n — Cockpits in French', () => {
  it('renders user cockpit with search action', async () => {
    authState('user');
    renderApp('fr', ['/cockpit']);
    expect(await screen.findByText(/rechercher/i)).toBeInTheDocument();
  });
});

describe('Route protection', () => {
  it('redirects unauthenticated to login from /cockpit', async () => {
    renderApp('fr', ['/cockpit']);
    await waitFor(() => {
      expect(screen.getByRole('textbox', { name: /identifiant|identifier/i })).toBeInTheDocument();
    });
  });

  it('redirects unauthenticated to login from /biens', async () => {
    renderApp('fr', ['/biens']);
    await waitFor(() => {
      expect(screen.getByRole('textbox', { name: /identifiant|identifier/i })).toBeInTheDocument();
    });
  });

  it('redirects unauthenticated to login from /conversation', async () => {
    renderApp('fr', ['/conversation']);
    await waitFor(() => {
      expect(screen.getByRole('textbox', { name: /identifiant|identifier/i })).toBeInTheDocument();
    });
  });
});

describe('Feature flags respected', () => {
  it('admin can access /admin/features when authenticated', async () => {
    authState('admin');
    renderApp('fr', ['/admin/features']);
    expect(await screen.findByText(/gestion des fonctionnalités/i)).toBeInTheDocument();
  });
});
