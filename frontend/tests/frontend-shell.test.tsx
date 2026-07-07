import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { useAuthStore } from '@auth';
import type { ReactElement } from 'react';
import { WebApp } from '../apps/web/src/App';
import { AdminApp } from '../apps/admin/src/App';
import { WorkflowOrchestratorPage } from '../apps/web/src/WorkflowOrchestratorPage';
import { ObservabilityPage } from '../apps/admin/src/ObservabilityPage';
import { ProductReadinessPage } from '../apps/admin/src/ProductReadinessPage';
import { BackupCenterPage } from '../apps/admin/src/BackupCenterPage';
import { BackupManagerPage } from '../apps/admin/src/BackupManagerPage';
import { StorageSetupWizardPage } from '../apps/admin/src/StorageSetupWizardPage';

const defaultDashboardSummary = {
  properties: 8,
  opportunities: 3,
  communications: 2,
  pendingTasks: 1
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
});

afterEach(() => {
  window.localStorage.clear();
  vi.restoreAllMocks();
});

describe('LAWIM frontend shell', () => {
  it('renders the public home page with branding', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('heading', { name: /one workspace, three roles, zero role picker\./i })).toBeInTheDocument();
    expect(screen.getByRole('navigation', { name: /primary/i })).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(2);
    expect(screen.getAllByText(/lawim role-based workspace/i)).toHaveLength(2);
  });

  it('renders the login page without a role selector and with the LAWIM logo', async () => {
    renderWithProviders(<WebApp />, ['/login']);

    expect(await screen.findByRole('heading', { name: /welcome back/i })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: /lawim logo/i })).toBeInTheDocument();
    expect(screen.getByText(/lawim secure sign-in/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/role/i)).not.toBeInTheDocument();
  });

  it.each([
    {
      role: 'admin',
      email: 'admin@lawim.app',
      name: 'Admin User',
      heading: /admin dashboard/i
    },
    {
      role: 'agent',
      email: 'agent@lawim.app',
      name: 'Agent User',
      heading: /agent dashboard/i
    },
    {
      role: 'owner',
      email: 'owner@lawim.app',
      name: 'Owner User',
      heading: /owner dashboard/i
    }
  ])('logs in as $role and opens the matching dashboard', async ({ role, email, name, heading }) => {
    const user = userEvent.setup();
    const loginSpy = vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse(role, [role], email, name));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), email);
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByRole('heading', { name: heading })).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(2);
    expect(screen.getAllByText(/lawim role-based workspace/i)).toHaveLength(2);
    expect(window.localStorage.getItem('lawim_token')).toBe('live-token');
    expect(loginSpy).toHaveBeenCalledWith({ email, password: 'lawim-demo' });
  });

  it('routes a login response that omits user.role to the highest-priority role in payload.roles', async () => {
    const user = userEvent.setup();
    const loginSpy = vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse(undefined, ['owner', 'agent'], 'multi@lawim.app', 'Multi Role User'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'multi@lawim.app');
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByRole('heading', { name: /agent dashboard/i })).toBeInTheDocument();
    expect(loginSpy).toHaveBeenCalledWith({ email: 'multi@lawim.app', password: 'lawim-demo' });
  });

  it('surfaces an incorrect-credentials message for a bad password', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User', '', 'Request failed with 401'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/password/i), 'wrong-password');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/incorrect email or password/i)).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
  });

  it('surfaces a server-unavailable message for a login 5xx response', async () => {
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User', '', 'Request failed with 500'));

    renderWithProviders(<WebApp />, ['/login']);

    await user.type(await screen.findByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/server unavailable\. try again in a moment\./i)).toBeInTheDocument();
    expect(window.localStorage.getItem('lawim_token')).toBeNull();
  });

  it('redirects an unauthenticated protected route to login without a session-expired banner', async () => {
    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /welcome back/i })).toBeInTheDocument();
    expect(screen.getByText(/sign in to access your workspace\./i)).toBeInTheDocument();
    expect(screen.queryByText(/session expired/i)).not.toBeInTheDocument();
  });

  it('shows a session-expired banner when an existing token cannot be restored', async () => {
    window.localStorage.setItem('lawim_token', 'orphan-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'mock' });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /welcome back/i })).toBeInTheDocument();
    expect(screen.getByText(/your session expired\. sign in again\./i)).toBeInTheDocument();
  });

  it('shows a server-unavailable banner when session refresh fails with a 5xx error', async () => {
    window.localStorage.setItem('lawim_token', 'stale-token');
    vi.mocked(apiSdk.getSession).mockResolvedValue({ data: null, message: 'Request failed with 500' });

    renderWithProviders(<WebApp />, ['/dashboard/admin']);

    expect(await screen.findByRole('heading', { name: /welcome back/i })).toBeInTheDocument();
    expect(screen.getByText(/server unavailable\. try again in a moment\./i)).toBeInTheDocument();
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

    expect(await screen.findByRole('heading', { name: /agent dashboard/i })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /admin dashboard/i })).not.toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: /lawim logo/i })).toHaveLength(2);
    expect(screen.getAllByText(/lawim role-based workspace/i)).toHaveLength(2);
  });

  it('emits controlled auth traces during a successful login', async () => {
    window.localStorage.setItem('lawim.debug.auth', '1');
    const debugSpy = vi.spyOn(console, 'debug').mockImplementation(() => undefined);
    const user = userEvent.setup();
    vi.spyOn(apiSdk, 'login').mockResolvedValue(loginResponse('admin', ['admin'], 'admin@lawim.app', 'Admin User'));

    renderWithProviders(<WebApp />, ['/login']);

    await screen.findByRole('heading', { name: /welcome back/i });
    debugSpy.mockClear();

    await user.type(screen.getByLabelText(/email/i), 'admin@lawim.app');
    await user.type(screen.getByLabelText(/password/i), 'lawim-demo');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByRole('heading', { name: /admin dashboard/i })).toBeInTheDocument();
    await waitFor(() => {
      expect(debugSpy.mock.calls.map(([label]) => label)).toEqual([
        'LOGIN_OK',
        'ROLE_RESOLVED',
        'DASHBOARD_SELECTED',
        'APPLY_JOURNEY',
        'DASHBOARD_RENDERED',
        'RENDER_DONE'
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
