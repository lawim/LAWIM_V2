import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { useAuthStore } from '@auth';
import { WebApp } from '../apps/web/src/App';
import { AdminApp } from '../apps/admin/src/App';
import { WorkflowOrchestratorPage } from '../apps/web/src/WorkflowOrchestratorPage';
import { ObservabilityPage } from '../apps/admin/src/ObservabilityPage';
import { ProductReadinessPage } from '../apps/admin/src/ProductReadinessPage';
import { BackupCenterPage } from '../apps/admin/src/BackupCenterPage';
import { BackupManagerPage } from '../apps/admin/src/BackupManagerPage';
import { StorageSetupWizardPage } from '../apps/admin/src/StorageSetupWizardPage';

function renderWithProviders(ui: React.ReactElement, initialEntries: string[] = ['/']) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={initialEntries}>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
}

beforeEach(() => {
  useAuthStore.setState({
    user: null,
    token: null,
    roles: [],
    isAuthenticated: false,
    isLoading: false
  });
  window.localStorage.clear();
  vi.restoreAllMocks();
});

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

describe('LAWIM frontend shell', () => {
  it('renders the public web app shell', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('heading', { name: /operational intelligence for modern teams/i })).toBeInTheDocument();
    expect(screen.getByText(/live data flowing from the lawim backend with activation-ready routing/i)).toBeInTheDocument();
    expect(screen.getByText(/search/i)).toBeInTheDocument();
  });

  it('exposes accessible primary navigation for the public shell', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('navigation', { name: /primary/i })).toBeInTheDocument();
  });

  it('logs in and redirects the web app to the dashboard', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue({
      data: {
        user: {
          id: 'u-1',
          name: 'Admin User',
          role: 'admin',
          email: 'admin@lawim.local'
        },
        token: 'live-token',
        roles: ['admin']
      },
      message: 'ok'
    });
    vi.spyOn(apiSdk, 'getDashboardSummary').mockResolvedValue({
      data: {
        properties: 8,
        opportunities: 3,
        communications: 2,
        pendingTasks: 1
      },
      message: 'ok'
    });

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(screen.getByLabelText(/email/i), 'admin@lawim.local');
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByRole('heading', { name: /dashboard/i })).toBeInTheDocument();
    expect(screen.getByText(/follow the latest opportunities and actions in one place/i)).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBe('live-token');
    expect(apiSdk.login).toHaveBeenCalledWith({ email: 'admin@lawim.local', password: 'lawim-demo' });
  });

  it('surfaces a login error when the session payload does not include a token', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue({
      data: {
        user: {
          id: 'u-1',
          name: 'Admin User',
          role: 'admin',
          email: 'admin@lawim.local'
        },
        token: '',
        roles: ['admin']
      },
      message: 'ok'
    });

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(screen.getByLabelText(/email/i), 'admin@lawim.local');
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/authentication failed/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /dashboard/i })).not.toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
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

  it('renders the workflow orchestrator experience', () => {
    render(<WorkflowOrchestratorPage />);

    expect(screen.getByRole('heading', { name: /workflow orchestration/i })).toBeInTheDocument();
    expect(screen.getAllByText(/status: ready/i)).toHaveLength(3);
    expect(screen.getAllByText(/escalation path/i)).toHaveLength(2);
  });

  it('renders the backup center, manager, and setup wizard experiences', () => {
    render(
      <>
        <BackupCenterPage />
        <BackupManagerPage />
        <StorageSetupWizardPage />
      </>
    );

    expect(screen.getByRole('heading', { name: /admin backup and storage control center/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /simplified manager console/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /google drive activation wizard/i })).toBeInTheDocument();
  });

  it('renders the observability and readiness panels', () => {
    render(
      <>
        <ObservabilityPage />
        <ProductReadinessPage />
      </>
    );

    expect(screen.getByRole('heading', { name: /observability console/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /product readiness/i })).toBeInTheDocument();
    expect(screen.getByText(/brain decisions/i)).toBeInTheDocument();
    expect(screen.getByText(/test coverage/i)).toBeInTheDocument();
  });
});
