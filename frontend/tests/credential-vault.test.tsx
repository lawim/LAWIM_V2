import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { CredentialVaultPage } from '../apps/admin/src/CredentialVaultPage';
import { GoogleDriveCredentialsPage } from '../apps/admin/src/GoogleDriveCredentialsPage';
import { GoogleDriveSecurityPage } from '../apps/admin/src/GoogleDriveSecurityPage';
import { buildCredentialVaultSnapshot, buildGoogleDriveSecuritySnapshot } from '../apps/admin/src/storageRegistry';

describe('credential vault frontend surfaces', () => {
  it('renders the encrypted credential vault dashboard', () => {
    render(<CredentialVaultPage />);

    expect(screen.getByRole('heading', { name: /encrypted credential vault/i })).toBeInTheDocument();
    expect(screen.getAllByText(/^cred-drive-1$/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/masked reference/i).length).toBeGreaterThan(0);
  });

  it('renders the google drive credential bindings dashboard', () => {
    render(<GoogleDriveCredentialsPage />);

    expect(screen.getByRole('heading', { name: /production credential bindings/i })).toBeInTheDocument();
    expect(screen.getAllByText(/^drive-1$/i).length).toBeGreaterThan(0);
  });

  it('renders the google drive security dashboard', () => {
    render(<GoogleDriveSecurityPage />);

    expect(screen.getByRole('heading', { name: /credential and protected material protection/i })).toBeInTheDocument();
    expect(screen.getByText(/protectedmaterialscanner/i)).toBeInTheDocument();
    expect(screen.getByText(/gitprotectionguard/i)).toBeInTheDocument();
  });

  it('keeps credential snapshots masked', () => {
    const vault = buildCredentialVaultSnapshot();
    const security = buildGoogleDriveSecuritySnapshot();

    expect(vault.summary.recordCount).toBe(10);
    expect(vault.summary.maskedRecords).toBe(10);
    expect(JSON.stringify(vault)).not.toMatch(/drive\.google\.com/i);
    expect(JSON.stringify(security)).not.toMatch(/drive\.google\.com/i);
  });
});
