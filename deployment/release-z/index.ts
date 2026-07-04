export interface ReleaseZArtifact {
  name: string;
  path: string;
  description: string;
}

export function getReleaseZPackageSummary(): string {
  return 'Production deployment package for Release Z: simulation-safe, server-prep focused, and ready for controlled execution.';
}

export function getReleaseZPackageArtifacts(): ReleaseZArtifact[] {
  return [
    { name: 'Production runbook', path: 'deployment/runbook/ProductionRunbook.md', description: 'Primary operational runbook' },
    { name: 'Server preparation runbook', path: 'deployment/runbook/ServerPreparationRunbook.md', description: 'Host and service preparation steps' },
    { name: 'Deployment runbook', path: 'deployment/runbook/DeploymentRunbook.md', description: 'Deployment and validation procedures' },
    { name: 'Backup policy', path: 'deployment/backup/backup-policy.md', description: 'Backup retention and controls' },
    { name: 'Production environment template', path: 'deployment/environments/production/.env.production.example', description: 'Example production environment values' },
    { name: 'Migration scripts', path: 'deployment/migration', description: 'Dry-run, rollback, verify, and post-migration scripts' },
    { name: 'Systemd timers', path: 'deployment/systemd', description: 'Backup scheduling assets' }
  ];
}

export function getReleaseZPackageChecklist(): string {
  return [
    'Prepare host',
    'Install dependencies',
    'Configure networking and SSL',
    'Set up backups and restore',
    'Validate migration dry-run',
    'Confirm go-live checklist'
  ].join('\n');
}
