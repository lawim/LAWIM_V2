export type StorageBand = 'normal' | 'attention' | 'slowdown' | 'blocked';
export type StorageStatus = 'ready' | 'watch' | 'degraded' | 'blocked';

export interface StorageResourceRow {
  driveId: string;
  logicalName: string;
  role: string;
  resourceType: string;
  priority: number;
  category: string;
  quotaGb: number;
  usedGb: number;
  availableGb: number;
  usagePercent: number;
  providerType: string;
  credentialId: string;
  state: string;
  status: StorageStatus;
  health: StorageStatus;
  lastControl: string;
  lastAccess: string;
  lastTest: string;
  lastConnectionTest: string;
  lastUploadTest: string;
  lastDownloadTest: string;
  lastHealthcheck: string;
  apiVersion: string;
  oauthStatus: string;
  routingStrategy: string;
  backupPolicy: string;
  restorePolicy: string;
  credentialStatus: string;
  testStatus: string;
  thresholdBand: StorageBand;
  routeHint: string;
}

export interface GoogleDriveConfigurationRow {
  driveId: string;
  logicalName: string;
  credentialId: string;
  emailPlaceholder: string;
  provider: string;
  category: string;
  quotaGb: number;
  usedGb: number;
  availableGb: number;
  credentialStatus: string;
  testStatus: string;
  apiVersion: string;
  oauthStatus: string;
  lastControl: string;
  lastAccess: string;
  lastConnectionTest: string;
  lastUploadTest: string;
  lastDownloadTest: string;
  lastHealthcheck: string;
  routingStrategy: string;
  backupPolicy: string;
  restorePolicy: string;
}

export interface GoogleDriveConnectorRow {
  driveId: string;
  logicalName: string;
  credentialId: string;
  provider: string;
  category: string;
  resourceType: string;
  quotaGb: number;
  usedGb: number;
  availableGb: number;
  usagePercent: number;
  state: string;
  health: string;
  credentialStatus: string;
  apiVersion: string;
  oauthStatus: string;
  lastControl: string;
  lastAccess: string;
  lastConnectionTest: string;
  lastUploadTest: string;
  lastDownloadTest: string;
  lastHealthcheck: string;
  lastUpload: string;
  lastDownload: string;
  lastIncident: string;
  alerts: string[];
  folders: string[];
  routingStrategy: string;
  backupPolicy: string;
  restorePolicy: string;
  routeHint: string;
}

export interface StorageRouteRow {
  category: string;
  label: string;
  route: string[];
  fallback: string;
  description: string;
}

export interface CredentialVaultRow {
  credentialId: string;
  driveId: string;
  logicalName: string;
  role: string;
  provider: string;
  credentialType: string;
  scope: string;
  status: string;
  oauthStatus: string;
  credentialStatus: string;
  maskedValue: string;
  maskedReference: string;
  rotationPolicy: string;
  expiration: string;
  rotationDue: string;
  lastUse: string;
  lastConnectionTest: string;
  lastUploadTest: string;
  lastDownloadTest: string;
  lastHealthcheck: string;
  alerts: string[];
}

export const storageThresholds = {
  normalMaxPercent: 70,
  attentionMaxPercent: 85,
  slowdownMaxPercent: 92,
};

export const setupWizardFolders = [
  'VIDEOS',
  'VIDEOS_ARCHIVE',
  'PHOTOS',
  'AUDIO',
  'DOCUMENTS',
  'CONVERSATIONS',
  'BACKUPS',
  'EXPORTS',
  'TEMP',
  'LOGS',
];

const activationTimestamp = '2026-07-05T10:00:00Z';
const expirationTimestamp = '2027-07-05T10:00:00Z';
const rotationDueTimestamp = '2026-10-03T10:00:00Z';

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

export function badgeVariantForStatus(status: StorageStatus | StorageBand | string): 'default' | 'success' | 'warning' | 'info' {
  if (status === 'ready' || status === 'healthy' || status === 'connected' || status === 'active' || status === 'activation-ready' || status === 'activation-passed') {
    return 'success';
  }
  if (status === 'placeholder-configured' || status === 'prepared' || status === 'never' || status === 'masked' || status === 'protected') {
    return 'info';
  }
  if (status === 'watch') {
    return 'info';
  }
  if (status === 'blocked' || status === 'slowdown' || status === 'attention' || status === 'degraded' || status === 'rotation-due' || status === 'expired' || status === 'invalid' || status === 'revoked' || status === 'disabled') {
    return 'warning';
  }
  return 'default';
}

function credentialIdForDrive(driveId: string): string {
  return `cred-${driveId}`;
}

export const storageResources: StorageResourceRow[] = driveSpecs.map((spec) => {
  const quotaGb = 13;
  const percent = usagePercent(spec.usedGb, quotaGb);
  const band = thresholdBand(percent);
  const status = statusForBand(band);
  const lastCheck = activationTimestamp;
  const credentialId = credentialIdForDrive(spec.driveId);
  const routingStrategy = 'official-priority-route';
  const backupPolicy = 'backup-center-activation';
  const restorePolicy = 'restore-center-activation';
  return {
    driveId: spec.driveId,
    logicalName: spec.logicalName,
    role: spec.role,
    resourceType: 'google-drive-resource',
    priority: spec.priority,
    category: spec.category,
    quotaGb,
    usedGb: spec.usedGb,
    availableGb: Number((quotaGb - spec.usedGb).toFixed(1)),
    usagePercent: percent,
    providerType: 'google-drive',
    credentialId,
    state: status,
    status,
    health: status,
    lastControl: lastCheck,
    lastAccess: lastCheck,
    lastTest: lastCheck,
    lastConnectionTest: lastCheck,
    lastUploadTest: lastCheck,
    lastDownloadTest: lastCheck,
    lastHealthcheck: lastCheck,
    apiVersion: 'v3',
    oauthStatus: 'placeholder-configured',
    routingStrategy,
    backupPolicy,
    restorePolicy,
    credentialStatus: 'placeholder-configured',
    testStatus: status === 'blocked' ? 'activation-review' : 'activation-passed',
    thresholdBand: band,
    routeHint: spec.routeHint,
  };
});

export const googleDriveConfigurations: GoogleDriveConfigurationRow[] = storageResources.map((resource) => ({
  driveId: resource.driveId,
  logicalName: resource.logicalName,
  credentialId: resource.credentialId,
  emailPlaceholder: `${resource.driveId}@placeholder.lawim.invalid`,
  provider: resource.providerType,
  category: resource.category,
  quotaGb: resource.quotaGb,
  usedGb: resource.usedGb,
  availableGb: resource.availableGb,
  credentialStatus: resource.credentialStatus,
  testStatus: resource.testStatus,
  apiVersion: resource.apiVersion,
  oauthStatus: resource.oauthStatus,
  lastControl: resource.lastControl,
  lastAccess: resource.lastAccess,
  lastConnectionTest: resource.lastConnectionTest,
  lastUploadTest: resource.lastUploadTest,
  lastDownloadTest: resource.lastDownloadTest,
  lastHealthcheck: resource.lastHealthcheck,
  routingStrategy: resource.routingStrategy,
  backupPolicy: resource.backupPolicy,
  restorePolicy: resource.restorePolicy,
}));

export const googleDriveConnectors: GoogleDriveConnectorRow[] = storageResources.map((resource) => {
  const isBlocked = resource.thresholdBand === 'blocked';
  const alert = isBlocked ? `${resource.driveId} blocked at ${resource.usagePercent.toFixed(1)}%` : '';
  return {
    driveId: resource.driveId,
    logicalName: resource.logicalName,
    credentialId: resource.credentialId,
    provider: resource.providerType,
    category: resource.category,
    resourceType: resource.resourceType,
    quotaGb: resource.quotaGb,
    usedGb: resource.usedGb,
    availableGb: resource.availableGb,
    usagePercent: resource.usagePercent,
    state: resource.state,
    health: resource.health,
    credentialStatus: resource.credentialStatus,
    apiVersion: resource.apiVersion,
    oauthStatus: resource.credentialStatus,
    lastControl: resource.lastControl,
    lastAccess: resource.lastAccess,
    lastConnectionTest: resource.lastConnectionTest,
    lastUploadTest: resource.lastUploadTest,
    lastDownloadTest: resource.lastDownloadTest,
    lastHealthcheck: resource.lastHealthcheck,
    lastUpload: resource.lastUploadTest,
    lastDownload: resource.lastDownloadTest,
    lastIncident: alert || 'none',
    alerts: alert ? [alert] : [],
    folders: [...setupWizardFolders],
    routingStrategy: resource.routingStrategy,
    backupPolicy: resource.backupPolicy,
    restorePolicy: resource.restorePolicy,
    routeHint: resource.routeHint,
  };
});

export const credentialVaultRecords: CredentialVaultRow[] = storageResources.map((resource) => ({
  credentialId: resource.credentialId,
  driveId: resource.driveId,
  logicalName: resource.logicalName,
  role: resource.role,
  provider: resource.providerType,
  credentialType: 'google-drive-oauth2',
  scope: 'google-drive',
  status: resource.credentialStatus,
  oauthStatus: resource.oauthStatus,
  credentialStatus: resource.credentialStatus,
  maskedValue: '***',
  maskedReference: `credential-reference://${resource.credentialId}`,
  rotationPolicy: '90d rotation / 365d expiry / masked-only display',
  expiration: expirationTimestamp,
  rotationDue: rotationDueTimestamp,
  lastUse: resource.lastAccess,
  lastConnectionTest: resource.lastConnectionTest,
  lastUploadTest: resource.lastUploadTest,
  lastDownloadTest: resource.lastDownloadTest,
  lastHealthcheck: resource.lastHealthcheck,
  alerts: resource.thresholdBand === 'blocked' ? [`${resource.driveId} blocked at ${resource.usagePercent.toFixed(1)}%`] : [],
}));

export const credentialSecurityControls = [
  {
    name: 'CredentialEncryptor',
    status: 'active',
    description: 'Encrypted envelopes keep protected material outside Git, logs, docs, and the frontend.',
  },
  {
    name: 'CredentialMasker',
    status: 'active',
    description: 'Displays only masked references in UI snapshots and audit payloads.',
  },
  {
    name: 'CredentialRotationManager',
    status: 'ready',
    description: 'Schedules rotation and expiration windows without exposing raw protected values.',
  },
  {
    name: 'ProtectedMaterialScanner',
    status: 'active',
    description: 'Scans Git payloads and admin snapshots for exposed protected material.',
  },
  {
    name: 'GitProtectionGuard',
    status: 'active',
    description: 'Blocks commits that carry protected material or direct Google Drive URLs.',
  },
  {
    name: 'AuditTrail',
    status: 'active',
    description: 'Records credential lifecycle events with masked details only.',
  },
] as const;

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
  'Register the credential vault',
  'Declare the 10 Google Drive resources',
  'Bind credential references',
  'Validate OAuth connection',
  'Validate permissions',
  'Run the read test',
  'Run the write test',
  'Run the upload test',
  'Run the download test',
  'Create the automatic folders',
  'Run the final validation',
];

export function buildCredentialVaultSnapshot() {
  const activeCredentials = credentialVaultRecords.filter((record) => record.status === 'placeholder-configured' || record.status === 'ready' || record.status === 'active');
  const expiredCredentials = credentialVaultRecords.filter((record) => record.status === 'expired');
  const invalidCredentials = credentialVaultRecords.filter((record) => record.status === 'invalid');
  const rotationDueCredentials = credentialVaultRecords.filter((record) => record.status === 'rotation-due');
  const lastUse = credentialVaultRecords.reduce((value, record) => (record.lastUse > value ? record.lastUse : value), 'never');
  const lastConnectionTest = credentialVaultRecords.reduce((value, record) => (record.lastConnectionTest > value ? record.lastConnectionTest : value), 'never');
  const lastUploadTest = credentialVaultRecords.reduce((value, record) => (record.lastUploadTest > value ? record.lastUploadTest : value), 'never');
  const lastDownloadTest = credentialVaultRecords.reduce((value, record) => (record.lastDownloadTest > value ? record.lastDownloadTest : value), 'never');
  const lastHealthcheck = credentialVaultRecords.reduce((value, record) => (record.lastHealthcheck > value ? record.lastHealthcheck : value), 'never');

  return {
    vault: 'lawim-credential-vault',
    status: 'activation-ready',
    summary: {
      recordCount: credentialVaultRecords.length,
      activeCount: activeCredentials.length,
      expiredCount: expiredCredentials.length,
      invalidCount: invalidCredentials.length,
      rotationDueCount: rotationDueCredentials.length,
      maskedRecords: credentialVaultRecords.length,
      protectionLayers: credentialSecurityControls.length,
    },
    monitoring: {
      activeCredentials: activeCredentials.length,
      expiredCredentials: expiredCredentials.length,
      invalidCredentials: invalidCredentials.length,
      rotationDueCredentials: rotationDueCredentials.length,
      lastAccess: lastUse,
      lastConnectionTest,
      lastUploadTest,
      lastDownloadTest,
      lastHealthcheck,
      lastFailure: 'never',
      lastSuccess: lastHealthcheck,
      alerts: credentialVaultRecords.flatMap((record) => record.alerts),
    },
    records: credentialVaultRecords,
    securityControls: credentialSecurityControls,
    auditTrail: {
      eventCount: credentialVaultRecords.length,
      latestEvent: 'credential-registered',
      entries: credentialVaultRecords.map((record) => ({
        credentialId: record.credentialId,
        driveId: record.driveId,
        event: 'credential-registered',
        status: record.status,
      })),
    },
  };
}

export function buildGoogleDriveCredentialsSnapshot() {
  const vault = buildCredentialVaultSnapshot();
  return {
    vault,
    credentials: googleDriveConfigurations,
    bindingCount: googleDriveConfigurations.length,
    secureReferences: googleDriveConfigurations.map((credential) => ({
      driveId: credential.driveId,
      credentialId: credential.credentialId,
      logicalName: credential.logicalName,
      role: storageResources.find((resource) => resource.driveId === credential.driveId)?.role ?? credential.logicalName,
      status: credential.credentialStatus,
      oauthStatus: credential.oauthStatus,
      lastConnectionTest: credential.lastConnectionTest,
      lastUploadTest: credential.lastUploadTest,
      lastDownloadTest: credential.lastDownloadTest,
      lastHealthcheck: credential.lastHealthcheck,
    })),
  };
}

export function buildGoogleDriveSecuritySnapshot() {
  const vault = buildCredentialVaultSnapshot();
  const monitoring = buildMonitoringSnapshot();
  return {
    vault,
    monitoring,
    controls: credentialSecurityControls,
    policy: {
      rotationDays: 90,
      expirationDays: 365,
      warningWindowDays: 14,
      autoRotate: true,
      maskedDisplay: true,
      noProtectedMaterialInGit: true,
      noProtectedMaterialInLogs: true,
      noProtectedMaterialInDocs: true,
      noProtectedMaterialInFrontend: true,
    },
    summary: {
      activeCredentials: vault.summary.activeCount,
      expiredCredentials: vault.summary.expiredCount,
      invalidCredentials: vault.summary.invalidCount,
      rotationDueCredentials: vault.summary.rotationDueCount,
      alerts: vault.monitoring.alerts.length,
      auditEvents: vault.auditTrail.eventCount,
      lastAccess: vault.monitoring.lastAccess,
      lastFailure: vault.monitoring.lastFailure,
      lastSuccess: vault.monitoring.lastSuccess,
    },
  };
}

export function buildManagerSnapshot() {
  const totalQuotaGb = storageResources.reduce((sum, resource) => sum + resource.quotaGb, 0);
  const totalUsedGb = storageResources.reduce((sum, resource) => sum + resource.usedGb, 0);
  const blocked = storageResources.filter((resource) => resource.thresholdBand === 'blocked');
  const alerts = storageResources.filter((resource) => resource.thresholdBand !== 'normal');
  const operationalAlerts = googleDriveConnectors.flatMap((connector) => connector.alerts);
  const vault = buildCredentialVaultSnapshot();
  const allAlerts = Array.from(
    new Set([
      ...alerts.map((resource) => `${resource.driveId} ${resource.thresholdBand} at ${resource.usagePercent.toFixed(1)}%`),
      ...operationalAlerts,
      ...vault.monitoring.alerts,
    ]),
  );

  return {
    totalQuotaGb: Number(totalQuotaGb.toFixed(1)),
    totalUsedGb: Number(totalUsedGb.toFixed(1)),
    remainingGb: Number((totalQuotaGb - totalUsedGb).toFixed(1)),
    usagePercent: Number(((totalUsedGb / totalQuotaGb) * 100).toFixed(1)),
    blockedCount: blocked.length,
    alertCount: allAlerts.length,
    lastTest: activationTimestamp,
    lastControl: activationTimestamp,
    lastAccess: activationTimestamp,
    lastUpload: activationTimestamp,
    lastDownload: activationTimestamp,
    backupStatus: 'Activation ready',
    availableResources: storageResources.filter((resource) => resource.thresholdBand !== 'blocked').length,
    blockedResources: blocked.map((resource) => resource.driveId),
    alerts: allAlerts,
    oauthReadyCount: googleDriveConnectors.filter((connector) => connector.oauthStatus === 'placeholder-configured').length,
    credentialReadyCount: vault.summary.activeCount,
    apiVersion: 'v3',
    monitoring: buildMonitoringSnapshot(),
    credentialVault: vault,
  };
}

export function buildGoogleDriveAdminSnapshot() {
  const totalQuotaGb = googleDriveConnectors.reduce((sum, connector) => sum + connector.quotaGb, 0);
  const totalUsedGb = googleDriveConnectors.reduce((sum, connector) => sum + connector.usedGb, 0);
  const blocked = googleDriveConnectors.filter((connector) => connector.usagePercent > 92);
  const alerts = Array.from(new Set(googleDriveConnectors.flatMap((connector) => connector.alerts)));
  const vault = buildCredentialVaultSnapshot();
  const security = buildGoogleDriveSecuritySnapshot();

  return {
    totalQuotaGb: Number(totalQuotaGb.toFixed(1)),
    totalUsedGb: Number(totalUsedGb.toFixed(1)),
    remainingGb: Number((totalQuotaGb - totalUsedGb).toFixed(1)),
    usagePercent: Number(((totalUsedGb / totalQuotaGb) * 100).toFixed(1)),
    availableResources: googleDriveConnectors.filter((connector) => connector.usagePercent <= 92).length,
    blockedResources: blocked.map((connector) => connector.driveId),
    alertCount: alerts.length,
    oauthReadyCount: googleDriveConnectors.filter((connector) => connector.oauthStatus === 'placeholder-configured').length,
    lastControl: activationTimestamp,
    lastAccess: activationTimestamp,
    lastTest: activationTimestamp,
    lastUpload: activationTimestamp,
    lastDownload: activationTimestamp,
    oauthState: 'placeholder-configured',
    apiVersion: 'v3',
    alerts,
    connectors: googleDriveConnectors,
    routes: storageRoutes,
    requiredFolders: setupWizardFolders,
    monitoring: buildMonitoringSnapshot(),
    credentialVault: vault,
    security,
  };
}

export function buildMonitoringSnapshot() {
  const totalQuotaGb = storageResources.reduce((sum, resource) => sum + resource.quotaGb, 0);
  const totalUsedGb = storageResources.reduce((sum, resource) => sum + resource.usedGb, 0);
  const usagePercent = Number(((totalUsedGb / totalQuotaGb) * 100).toFixed(1));
  const blockedCount = storageResources.filter((resource) => resource.thresholdBand === 'blocked').length;
  const vault = buildCredentialVaultSnapshot();

  return {
    quotaMonitor: {
      totalQuotaGb: Number(totalQuotaGb.toFixed(1)),
      totalUsedGb: Number(totalUsedGb.toFixed(1)),
      remainingGb: Number((totalQuotaGb - totalUsedGb).toFixed(1)),
      usagePercent,
      band: thresholdBand(usagePercent),
    },
    latencyMs: blockedCount > 0 ? 64 : 28,
    throughputMbps: blockedCount > 0 ? 92 : 180,
    apiMonitor: {
      apiVersion: 'v3',
      oauthState: 'placeholder-configured',
      status: blockedCount > 0 ? 'watch' : 'healthy',
    },
    credentialMonitor: {
      activeCredentials: vault.summary.activeCount,
      expiredCredentials: vault.summary.expiredCount,
      invalidCredentials: vault.summary.invalidCount,
      rotationDueCredentials: vault.summary.rotationDueCount,
      lastAccess: vault.monitoring.lastAccess,
      lastFailure: vault.monitoring.lastFailure,
      lastSuccess: vault.monitoring.lastSuccess,
    },
    alerts: storageResources
      .filter((resource) => resource.thresholdBand !== 'normal')
      .map((resource) => `${resource.driveId} ${resource.thresholdBand} at ${resource.usagePercent.toFixed(1)}%`),
    occupation: {
      availableResources: storageResources.filter((resource) => resource.thresholdBand !== 'blocked').length,
      blockedResources: blockedCount,
    },
    rotation: {
      video: ['Drive 1', 'Drive 2', 'Drive 8'],
      photo: ['Drive 3', 'Drive 8'],
      audio: ['Drive 3', 'Drive 8'],
      document: ['Drive 4', 'Drive 8'],
      conversation: ['Drive 5', 'Drive 8'],
      backup: ['Drive 7', 'Drive 10'],
      exports: ['Drive 6', 'Drive 8'],
      maintenance: ['Drive 10'],
    },
    api_monitor: {
      apiVersion: 'v3',
      oauthState: 'placeholder-configured',
      status: blockedCount > 0 ? 'watch' : 'healthy',
    },
    credential_monitor: {
      activeCredentials: vault.summary.activeCount,
      expiredCredentials: vault.summary.expiredCount,
      invalidCredentials: vault.summary.invalidCount,
      rotationDueCredentials: vault.summary.rotationDueCount,
      lastAccess: vault.monitoring.lastAccess,
      lastFailure: vault.monitoring.lastFailure,
      lastSuccess: vault.monitoring.lastSuccess,
    },
  };
}

export function driveStatusLabel(resource: StorageResourceRow): string {
  return `${statusLabel(resource.status)} · ${resource.thresholdBand}`;
}
