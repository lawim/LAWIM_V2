import '@testing-library/jest-dom/vitest';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { WebApp } from '../apps/web/src/App';
import { AdminApp } from '../apps/admin/src/App';
import { WorkflowOrchestratorPage } from '../apps/web/src/WorkflowOrchestratorPage';
import { ObservabilityPage } from '../apps/admin/src/ObservabilityPage';
import { ProductReadinessPage } from '../apps/admin/src/ProductReadinessPage';
import { BackupCenterPage } from '../apps/admin/src/BackupCenterPage';
import { BackupManagerPage } from '../apps/admin/src/BackupManagerPage';
import { StorageSetupWizardPage } from '../apps/admin/src/StorageSetupWizardPage';

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
}

describe('LAWIM frontend shell', () => {
  it('renders the public web app shell', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('heading', { name: /operational intelligence for modern teams/i })).toBeInTheDocument();
    expect(screen.getByText(/live data flowing from the lawim backend with mock-safe fallbacks/i)).toBeInTheDocument();
    expect(screen.getByText(/search/i)).toBeInTheDocument();
  });

  it('exposes accessible primary navigation for the public shell', () => {
    renderWithProviders(<WebApp />);

    expect(screen.getByRole('navigation', { name: /primary/i })).toBeInTheDocument();
  });

  it('renders the administration shell', () => {
    renderWithProviders(<AdminApp />);

    expect(screen.getByRole('heading', { name: /manage operations and oversight/i })).toBeInTheDocument();
    expect(screen.getByText(/administrative controls, governance workflows, and deployment readiness in one place/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /operations/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /agents/i })).toBeInTheDocument();
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
    expect(screen.getByRole('heading', { name: /mock setup for the aac-b2 storage platform/i })).toBeInTheDocument();
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
