import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { StorageResourcesPage } from '../apps/admin/src/StorageResourcesPage';
import { GoogleDriveRegistryPage } from '../apps/admin/src/GoogleDriveRegistryPage';
import { StorageRoutingPage } from '../apps/admin/src/StorageRoutingPage';
import { StorageSetupWizardPage } from '../apps/admin/src/StorageSetupWizardPage';
import { BackupManagerPage } from '../apps/admin/src/BackupManagerPage';

describe('storage registry frontend surfaces', () => {
  it('renders the storage resource registry dashboard', () => {
    render(<StorageResourcesPage />);

    expect(screen.getByRole('heading', { name: /storage resource registry/i })).toBeInTheDocument();
    expect(screen.getAllByText(/drive 1 -> drive 2 -> drive 8/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/threshold bands/i)).toBeInTheDocument();
  });

  it('renders the google drive registry dashboard', () => {
    render(<GoogleDriveRegistryPage />);

    expect(screen.getByRole('heading', { name: /google drive operational control center/i })).toBeInTheDocument();
    expect(screen.getByText(/drive-1@placeholder\.lawim\.invalid/i)).toBeInTheDocument();
    expect(screen.getByText(/credential vault keeps protected material encrypted/i)).toBeInTheDocument();
  });

  it('renders the storage routing dashboard', () => {
    render(<StorageRoutingPage />);

    expect(screen.getByRole('heading', { name: /storage routing policy/i })).toBeInTheDocument();
    expect(screen.getByText(/drive 5, then drive 8/i)).toBeInTheDocument();
    expect(screen.getByText(/critical replication: drive 8, then drive 10/i)).toBeInTheDocument();
  });

  it('renders the setup wizard and manager view', () => {
    render(
      <>
        <StorageSetupWizardPage />
        <BackupManagerPage />
      </>
    );

    expect(screen.getByRole('heading', { name: /google drive activation wizard/i })).toBeInTheDocument();
    expect(screen.getByText(/register the credential vault/i)).toBeInTheDocument();
    expect(screen.getByText(/declare the 10 google drive resources/i)).toBeInTheDocument();
    expect(screen.getByText(/automatic folders:/i)).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /simplified manager console/i })).toBeInTheDocument();
    expect(screen.getByText(/global storage, alerts, control timestamps, and backup status at a glance/i)).toBeInTheDocument();
  });
});
