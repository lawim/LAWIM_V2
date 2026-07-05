export type StorageBand = 'normal' | 'attention' | 'slowdown' | 'blocked';
export type StorageStatus = 'ready' | 'watch' | 'degraded' | 'blocked';

export interface StorageResourceRow {
  driveId: string;
  logicalName: string;
  role: string;
  priority: number;
  category: string;
  quotaGb: number;
  usedGb: number;
  availableGb: number;
  usagePercent: number;
  providerType: string;
  status: StorageStatus;
  health: StorageStatus;
  lastTest: string;
  credentialStatus: string;
  testStatus: string;
  thresholdBand: StorageBand;
  routeHint: string;
}

export interface GoogleDriveConfigurationRow {
  driveId: string;
  logicalName: string;
  emailPlaceholder: string;
  provider: string;
  category: string;
  quotaGb: number;
  usedGb: number;
  availableGb: number;
  credentialStatus: string;
  testStatus: string;
}

export interface StorageRouteRow {
  category: string;
  label: string;
  route: string[];
  fallback: string;
  description: string;
}

export const storageThresholds = {
  normalMaxPercent: 70,
  attentionMaxPercent: 85,
  slowdownMaxPercent: 92,
};

const driveSpecs = [
  { driveId: 'drive-1', logicalName: 'videos-a', role: 'Videos A', category: 'video', priority: 1, usedGb: 3.2, routeHint: 'Drive 1 -> Drive 2 -> Drive 8' },
  { driveId: 'drive-2', logicalName: 'videos-b', role: 'Videos B', category: 'video', priority: 2, usedGb: 4.1, routeHint: 'Drive 1 -> Drive 2 -> Drive 8' },
  { driveId: 'drive-3', logicalName: 'photos-audio', role: 'Photos + Audio', category: 'photo/audio', priority: 3, usedGb: 5.8, routeHint: 'Drive 3 -> Drive 8' },
  { driveId: 'drive-4', logicalName: 'documents', role: 'Documents', category: 'document', priority: 4, usedGb: 6.4, routeHint: 'Drive 4 -> Drive 8' },
  { driveId: 'drive-5', logicalName: 'conversation-registry', role: 'Conversation Registry', category: 'conversation archive', priority: 5, usedGb: 9.4, routeHint: 'Drive 5 -> Drive 8' },
  { driveId: 'drive-6', logicalName: 'exports-reports-stats', role: 'Exports / reports / statistics', category: 'export rapport', priority: 6, usedGb: 10.5, routeHint: 'Drive 6 -> Drive 8' },
  { driveId: 'drive-7', logicalName: 'application-backups', role: 'Application backups', category: 'backup applicatif', priority: 7, usedGb: 11.9, routeHint: 'Drive 7 -> Drive 10' },
  { driveId: 'drive-8', logicalName: 'replication-overflow', role: 'Replication / overflow', category: 'replication critique', priority: 8, usedGb: 12.4, routeHint: 'Drive 8 -> Drive 10' },
  { driveId: 'drive-9', logicalName: 'strategic-reserve', role: 'Strategic reserve', category: 'reserve', priority: 9, usedGb: 1.3, routeHint: 'Drive 9' },
  { driveId: 'drive-10', logicalName: 'maintenance-migration', role: 'Maintenance / migration', category: 'maintenance migration', priority: 10, usedGb: 3.9, routeHint: 'Drive 10' },
] as const;

function usagePercent(usedGb: number, quotaGb: number): number {
  return Number(((usedGb / quotaGb) * 100).toFixed(1));
}

function thresholdBand(value: number): StorageBand {
  if (value > storageThresholds.slowdownMaxPercent) {
    return 'blocked';
  }
  if (value >= storageThresholds.attentionMaxPercent) {
    return 'slowdown';
  }
  if (value >= storageThresholds.normalMaxPercent) {
    return 'attention';
  }
  return 'normal';
}

function statusForBand(band: StorageBand): StorageStatus {
  switch (band) {
    case 'normal':
      return 'ready';
    case 'attention':
      return 'watch';
    case 'slowdown':
      return 'degraded';
    case 'blocked':
      return 'blocked';
  }
}

function statusLabel(status: StorageStatus): string {
  switch (status) {
    case 'ready':
      return 'Ready';
    case 'watch':
      return 'Watch';
    case 'degraded':
      return 'Degraded';
    case 'blocked':
      return 'Blocked';
  }
}

export function badgeVariantForStatus(status: StorageStatus | StorageBand): 'default' | 'success' | 'warning' | 'info' {
  if (status === 'ready') {
    return 'success';
  }
  if (status === 'watch') {
    return 'info';
  }
  if (status === 'blocked' || status === 'slowdown' || status === 'attention') {
    return 'warning';
  }
  return 'default';
}

export const storageResources: StorageResourceRow[] = driveSpecs.map((spec) => {
  const quotaGb = 13;
  const percent = usagePercent(spec.usedGb, quotaGb);
  const band = thresholdBand(percent);
  const status = statusForBand(band);
  return {
    driveId: spec.driveId,
    logicalName: spec.logicalName,
    role: spec.role,
    priority: spec.priority,
    category: spec.category,
    quotaGb,
    usedGb: spec.usedGb,
    availableGb: Number((quotaGb - spec.usedGb).toFixed(1)),
    usagePercent: percent,
    providerType: 'google-drive',
    status,
    health: status,
    lastTest: 'mock-2026-07-05T10:00:00Z',
    credentialStatus: 'placeholder-configured',
    testStatus: status === 'blocked' ? 'mock-warning' : 'mock-passed',
    thresholdBand: band,
    routeHint: spec.routeHint,
  };
});

export const googleDriveConfigurations: GoogleDriveConfigurationRow[] = storageResources.map((resource) => ({
  driveId: resource.driveId,
  logicalName: resource.logicalName,
  emailPlaceholder: `${resource.driveId}@placeholder.lawim.invalid`,
  provider: resource.providerType,
  category: resource.category,
  quotaGb: resource.quotaGb,
  usedGb: resource.usedGb,
  availableGb: resource.availableGb,
  credentialStatus: resource.credentialStatus,
  testStatus: resource.testStatus,
}));

export const storageRoutes: StorageRouteRow[] = [
  {
    category: 'video',
    label: 'Video',
    route: ['Drive 1', 'Drive 2', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Videos land on Drive 1, then Drive 2, then Drive 8 overflow.',
  },
  {
    category: 'photo',
    label: 'Photo',
    route: ['Drive 3', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Photos stay on Drive 3 before overflowing to Drive 8.',
  },
  {
    category: 'audio',
    label: 'Audio',
    route: ['Drive 3', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Audio uses the shared Drive 3 pool and falls back to Drive 8.',
  },
  {
    category: 'document',
    label: 'Document',
    route: ['Drive 4', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Documents route through Drive 4 and overflow to Drive 8.',
  },
  {
    category: 'conversation archive',
    label: 'Conversation archive',
    route: ['Drive 5', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Conversation archives use Drive 5 first, then Drive 8.',
  },
  {
    category: 'export rapport',
    label: 'Export / report / statistics',
    route: ['Drive 6', 'Drive 8'],
    fallback: 'Drive 8 overflow',
    description: 'Exports, reports, and statistics move through Drive 6 first.',
  },
  {
    category: 'backup applicatif',
    label: 'Application backup',
    route: ['Drive 7', 'Drive 10'],
    fallback: 'Drive 10 maintenance',
    description: 'Application backups prefer Drive 7 and fall back to Drive 10.',
  },
  {
    category: 'replication critique',
    label: 'Critical replication',
    route: ['Drive 8', 'Drive 10'],
    fallback: 'Drive 10 maintenance',
    description: 'Critical replication can use Drive 8 or Drive 10 when required.',
  },
  {
    category: 'reserve',
    label: 'Strategic reserve',
    route: ['Drive 9'],
    fallback: 'Drive 9 reserve',
    description: 'Drive 9 stays available as the strategic reserve pool.',
  },
  {
    category: 'maintenance migration',
    label: 'Maintenance / migration',
    route: ['Drive 10'],
    fallback: 'Drive 10 maintenance',
    description: 'Maintenance and migration work stay on Drive 10.',
  },
];

export const setupWizardSteps = [
  'Declaration of the 10 drives',
  'Mock account validation',
  'Mock read test',
  'Mock write test',
  'Video upload simulation',
  'Conversation archive simulation',
  'Backup simulation',
  'Final summary',
];

export function buildManagerSnapshot() {
  const totalQuotaGb = storageResources.reduce((sum, resource) => sum + resource.quotaGb, 0);
  const totalUsedGb = storageResources.reduce((sum, resource) => sum + resource.usedGb, 0);
  const blocked = storageResources.filter((resource) => resource.thresholdBand === 'blocked');
  const alerts = storageResources.filter((resource) => resource.thresholdBand !== 'normal');

  return {
    totalQuotaGb: Number(totalQuotaGb.toFixed(1)),
    totalUsedGb: Number(totalUsedGb.toFixed(1)),
    remainingGb: Number((totalQuotaGb - totalUsedGb).toFixed(1)),
    usagePercent: Number(((totalUsedGb / totalQuotaGb) * 100).toFixed(1)),
    blockedCount: blocked.length,
    alertCount: alerts.length,
    lastTest: 'mock-2026-07-05T10:00:00Z',
    backupStatus: 'Ready',
    availableResources: storageResources.filter((resource) => resource.thresholdBand !== 'blocked').length,
    blockedResources: blocked.map((resource) => resource.driveId),
    alerts: alerts.map((resource) => `${resource.driveId} ${resource.thresholdBand} at ${resource.usagePercent.toFixed(1)}%`),
  };
}

export function driveStatusLabel(resource: StorageResourceRow): string {
  return `${statusLabel(resource.status)} · ${resource.thresholdBand}`;
}
