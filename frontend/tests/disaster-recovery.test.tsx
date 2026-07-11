import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { DisasterRecoveryPage } from '../apps/admin/src/DisasterRecoveryPage';

const mockStatus = {
  bundle_root: '/var/lib/lawim-backup/recovery-bundles',
  latest_bundle: {
    bundle_id: 'LAWIM-DRF-20260711-020000',
    created_at: '2026-06-01T02:00:00Z',
    size_bytes: 2456789,
    checksum: 'bundle-checksum',
    file_count: 42,
    environment: 'production',
    validation_state: 'generated',
    path: '/var/lib/lawim-backup/recovery-bundles/LAWIM-DRF-20260711-020000'
  },
  validation: {
    bundle_id: 'LAWIM-DRF-20260711-020000',
    manifest_present: true,
    checksum_valid: true,
    compatible: true,
    git_ok: true,
    docker_ok: true,
    postgresql_ok: true,
    restore_ready: true,
    missing_files: [],
    warnings: [],
    checks: [
      { name: 'manifest-present', passed: true, status: 'pass', detail: 'Manifest available' },
      { name: 'restore-ready', passed: true, status: 'pass', detail: 'Ready' }
    ],
    duration_seconds: 0.48,
    validated_at: '2026-07-11T02:05:00Z'
  },
  readiness: {
    score: 92,
    maximum_score: 100,
    state: 'READY',
    bundle_id: 'LAWIM-DRF-20260711-020000',
    bundle_age_days: 2,
    rpo_seconds: 300,
    rto_seconds: 900,
    signals: [
      { name: 'latest-bundle-present', passed: true, weight: 0, detail: 'Latest bundle is available' },
      { name: 'bundle-freshness', passed: true, weight: 0, detail: 'Latest bundle age is 2.0 days' },
      { name: 'validation-available', passed: true, weight: 0, detail: 'Recovery validation snapshot is available' }
    ],
    reasons: [],
    calculated_at: '2026-07-11T02:05:00Z'
  },
  git: {
    remote: 'git@github.com:lawim/lawim_v2.git',
    branch: 'main',
    sha: '17748006f463462e13241ea9f7429e6d52ad1acb',
    tags: ['v13.2'],
    status: '',
    is_clean: true
  },
  versions: {
    lawim: '0.1.0',
    docker: 'Docker version 27.0.3',
    docker_compose: '2.28.1',
    postgresql: 'psql (PostgreSQL) 15.8',
    python: '3.12.4',
    git: 'git version 2.45.2',
    node: 'v22.13.1',
    npm: '10.9.2',
    systemd: 'systemd 255',
    kernel: '6.8.0'
  },
  backup: {
    last_backup: {
      completed_at: '2026-07-11T00:00:00Z'
    },
    last_restore: {
      completed_at: '2026-07-11T01:30:00Z'
    },
    metrics: {
      rpo_seconds: 300,
      rto_seconds: 900
    }
  },
  checklist: '# Recovery Checklist\n\n1. Create the server.\n2. Install Docker.\n'
};

const mockBundles = [
  {
    bundle_id: 'LAWIM-DRF-20260711-020000',
    created_at: '2026-06-01T02:00:00Z',
    size_bytes: 2456789,
    checksum: 'bundle-checksum',
    file_count: 42,
    environment: 'production',
    validation_state: 'generated',
    path: '/var/lib/lawim-backup/recovery-bundles/LAWIM-DRF-20260711-020000'
  },
  {
    bundle_id: 'LAWIM-DRF-20260710-020000',
    created_at: '2026-07-10T02:00:00Z',
    size_bytes: 2198765,
    checksum: 'bundle-checksum-old',
    file_count: 40,
    environment: 'production',
    validation_state: 'generated',
    path: '/var/lib/lawim-backup/recovery-bundles/LAWIM-DRF-20260710-020000'
  }
];

function renderPage() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <DisasterRecoveryPage />
    </QueryClientProvider>
  );
}

beforeEach(() => {
  vi.restoreAllMocks();
  vi.spyOn(apiSdk, 'getDisasterRecoveryStatus').mockResolvedValue({ data: mockStatus as never, message: 'mock' });
  vi.spyOn(apiSdk, 'getDisasterRecoveryBundles').mockResolvedValue({ data: mockBundles as never, message: 'mock' });
  vi.spyOn(apiSdk, 'downloadDisasterRecoveryBundle').mockResolvedValue({
    blob: new Blob(['bundle'], { type: 'application/zip' }),
    filename: 'LAWIM-DRF-20260711-020000.zip'
  });
  Object.defineProperty(URL, 'createObjectURL', {
    configurable: true,
    writable: true,
    value: vi.fn(() => 'blob:mock')
  });
  Object.defineProperty(URL, 'revokeObjectURL', {
    configurable: true,
    writable: true,
    value: vi.fn()
  });
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('Disaster Recovery cockpit', () => {
  it('renders the recovery cockpit with score, validation, and bundle inventory', async () => {
    renderPage();

    expect(await screen.findByRole('heading', { name: /disaster recovery framework/i })).toBeInTheDocument();
    await screen.findAllByText('LAWIM-DRF-20260711-020000');
    expect(screen.getByText(/reconstruction cockpit for a fresh host/i)).toBeInTheDocument();
    expect(await screen.findByText(/^92%$/)).toBeInTheDocument();
    expect(screen.getByText(/readiness signals/i)).toBeInTheDocument();
    expect(screen.getByText(/validation checks/i)).toBeInTheDocument();
    expect(screen.getByText(/^# Recovery Checklist/)).toBeInTheDocument();
    expect(screen.getByText(/^Git state$/i)).toBeInTheDocument();
    expect(screen.getByText(/^Versions$/i)).toBeInTheDocument();
  });

  it('downloads the latest recovery bundle through the cockpit action', async () => {
    const user = userEvent.setup();
    renderPage();

    await user.click(await screen.findByRole('button', { name: /download latest bundle/i }));

    expect(apiSdk.downloadDisasterRecoveryBundle).toHaveBeenCalledWith('LAWIM-DRF-20260711-020000');
    expect(await screen.findByText(/download started/i)).toBeInTheDocument();
  });
});
