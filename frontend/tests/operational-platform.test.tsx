import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { PerformancePage } from '../apps/admin/src/PerformancePage';
import { SecurityPage } from '../apps/admin/src/SecurityPage';
import { ObservabilityPage } from '../apps/admin/src/ObservabilityPage';
import { IntegrationsPage } from '../apps/admin/src/IntegrationsPage';
import { QualityPage } from '../apps/admin/src/QualityPage';
import { OperationsPage } from '../apps/admin/src/OperationsPage';

describe('operational excellence platform', () => {
  it('renders the performance platform surface', () => {
    render(<PerformancePage />);
    expect(screen.getByText('Performance Center')).toBeInTheDocument();
  });

  it('renders the security platform surface', () => {
    render(<SecurityPage />);
    expect(screen.getByText('Security Center')).toBeInTheDocument();
  });

  it('renders the observability platform surface', () => {
    render(<ObservabilityPage />);
    expect(screen.getByText('Observability Center')).toBeInTheDocument();
  });

  it('renders the integrations platform surface', () => {
    render(<IntegrationsPage />);
    expect(screen.getByText('Integrations Center')).toBeInTheDocument();
  });

  it('renders the quality platform surface', () => {
    render(<QualityPage />);
    expect(screen.getByText('Quality Center')).toBeInTheDocument();
  });

  it('renders the operations platform surface', () => {
    render(<OperationsPage />);
    expect(screen.getByText('Operations Center')).toBeInTheDocument();
  });
});
