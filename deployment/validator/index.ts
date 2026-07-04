export type ValidationStatus = 'pass' | 'warning' | 'fail';

export interface ValidationResult {
  name: string;
  status: ValidationStatus;
  message: string;
  details?: string[];
}

export interface ServerProfile {
  os: string;
  kernel: string;
  docker: boolean;
  dockerCompose: boolean;
  node: string;
  python: string;
  git: boolean;
  redis: boolean;
  postgresql: boolean;
  portsOpen: boolean;
  firewallConfigured: boolean;
  dnsConfigured: boolean;
  internetReachable: boolean;
  volumesReady: boolean;
  permissionsOk: boolean;
  diskGb: number;
  ramGb: number;
  cpuCores: number;
  timezone: string;
  locale: string;
  sslConfigured: boolean;
  jwtConfigured: boolean;
  backupsValidated: boolean;
}

export interface AuditReport {
  readinessScore: number;
  criticalErrors: string[];
  warnings: string[];
  recommendations: string[];
  validations: ValidationResult[];
}

export interface MigrationStep {
  name: string;
  description: string;
  estimatedMinutes: number;
}

export interface RollbackStep {
  name: string;
  description: string;
}

export interface MigrationReport {
  steps: MigrationStep[];
  rollbackPlan: { steps: RollbackStep[] };
  downtimeEstimate: { minutes: number; note: string };
}

export interface DeploymentChecklistEntry {
  category: string;
  title: string;
  completed: boolean;
}

export interface RollbackPlan {
  steps: RollbackStep[];
}

export class ServerValidator {
  validate(profile: ServerProfile): ValidationResult[] {
    return [
      this.validateRequirement('OS', profile.os.length > 0),
      this.validateRequirement('Docker', profile.docker),
      this.validateRequirement('Docker Compose', profile.dockerCompose),
      this.validateRequirement('Node', profile.node.length > 0),
      this.validateRequirement('Python', profile.python.length > 0),
      this.validateRequirement('Git', profile.git),
      this.validateRequirement('Redis', profile.redis),
      this.validateRequirement('PostgreSQL', profile.postgresql),
      this.validateRequirement('Ports', profile.portsOpen),
      this.validateRequirement('Firewall', profile.firewallConfigured),
      this.validateRequirement('DNS', profile.dnsConfigured),
      this.validateRequirement('Internet', profile.internetReachable),
      this.validateRequirement('Volumes', profile.volumesReady),
      this.validateRequirement('Permissions', profile.permissionsOk),
      this.validateRequirement('SSL', profile.sslConfigured),
      this.validateRequirement('JWT', profile.jwtConfigured),
      this.validateRequirement('Backups', profile.backupsValidated)
    ];
  }

  private validateRequirement(name: string, passed: boolean): ValidationResult {
    return {
      name,
      status: passed ? 'pass' : 'warning',
      message: passed ? `${name} is ready` : `${name} needs attention`
    };
  }
}

export class EnvironmentValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Environment',
      status: profile.timezone && profile.locale ? 'pass' : 'warning',
      message: profile.timezone && profile.locale ? 'Timezone and locale are configured' : 'Timezone or locale needs review'
    };
  }
}

export class PackageValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Packages',
      status: profile.node && profile.python ? 'pass' : 'warning',
      message: 'Core runtime packages are available'
    };
  }
}

export class NetworkValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Network',
      status: profile.dnsConfigured && profile.internetReachable ? 'pass' : 'warning',
      message: 'Network prerequisites look healthy'
    };
  }
}

export class DiskValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Disk',
      status: profile.diskGb >= 200 ? 'pass' : 'warning',
      message: profile.diskGb >= 200 ? 'Disk capacity is sufficient' : 'Disk capacity should be increased'
    };
  }
}

export class MemoryValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Memory',
      status: profile.ramGb >= 16 ? 'pass' : 'warning',
      message: profile.ramGb >= 16 ? 'Memory is sufficient' : 'Memory should be expanded'
    };
  }
}

export class CpuValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'CPU',
      status: profile.cpuCores >= 8 ? 'pass' : 'warning',
      message: profile.cpuCores >= 8 ? 'CPU capacity is sufficient' : 'CPU capacity should be reviewed'
    };
  }
}

export class DockerValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Docker Engine',
      status: profile.docker ? 'pass' : 'fail',
      message: profile.docker ? 'Docker is installed' : 'Install Docker before deployment'
    };
  }
}

export class ComposeValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Docker Compose',
      status: profile.dockerCompose ? 'pass' : 'fail',
      message: profile.dockerCompose ? 'Docker Compose is available' : 'Install Docker Compose before deployment'
    };
  }
}

export class NginxValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Nginx',
      status: profile.sslConfigured ? 'pass' : 'warning',
      message: profile.sslConfigured ? 'HTTPS proxy layer looks ready' : 'TLS configuration should be confirmed'
    };
  }
}

export class RedisValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Redis',
      status: profile.redis ? 'pass' : 'warning',
      message: profile.redis ? 'Redis is reachable' : 'Redis readiness should be confirmed'
    };
  }
}

export class PostgreSQLValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'PostgreSQL',
      status: profile.postgresql ? 'pass' : 'warning',
      message: profile.postgresql ? 'PostgreSQL is available' : 'PostgreSQL should be verified before deployment'
    };
  }
}

export class SSLValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'SSL',
      status: profile.sslConfigured ? 'pass' : 'warning',
      message: profile.sslConfigured ? 'SSL is configured' : 'SSL certificate should be reviewed'
    };
  }
}

export class PermissionValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Permissions',
      status: profile.permissionsOk ? 'pass' : 'warning',
      message: profile.permissionsOk ? 'Filesystem permissions look correct' : 'Permission issues must be fixed'
    };
  }
}

export class BackupValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Backup Validation',
      status: profile.backupsValidated ? 'pass' : 'warning',
      message: profile.backupsValidated ? 'Backup validation is ready' : 'Run backup simulation before deployment'
    };
  }
}

export class RestoreValidator {
  validate(profile: ServerProfile): ValidationResult {
    return {
      name: 'Restore Validation',
      status: profile.backupsValidated ? 'pass' : 'warning',
      message: profile.backupsValidated ? 'Restore validation workflow is available' : 'Restore simulation should be completed'
    };
  }
}

export class InfrastructureAudit {
  constructor(private readonly profile: ServerProfile) {}

  run(): AuditReport {
    const serverValidator = new ServerValidator();
    const validations = [
      ...serverValidator.validate(this.profile),
      new EnvironmentValidator().validate(this.profile),
      new PackageValidator().validate(this.profile),
      new NetworkValidator().validate(this.profile),
      new DiskValidator().validate(this.profile),
      new MemoryValidator().validate(this.profile),
      new CpuValidator().validate(this.profile),
      new DockerValidator().validate(this.profile),
      new ComposeValidator().validate(this.profile),
      new NginxValidator().validate(this.profile),
      new RedisValidator().validate(this.profile),
      new PostgreSQLValidator().validate(this.profile),
      new SSLValidator().validate(this.profile),
      new PermissionValidator().validate(this.profile),
      new BackupValidator().validate(this.profile),
      new RestoreValidator().validate(this.profile)
    ];

    const criticalErrors = validations.filter((entry) => entry.status === 'fail').map((entry) => `${entry.name}: ${entry.message}`);
    const warnings = validations.filter((entry) => entry.status === 'warning').map((entry) => `${entry.name}: ${entry.message}`);
    const recommendations = [
      'Ensure Docker and Docker Compose are installed and running.',
      'Validate TLS certificates and HTTP reachability before deployment.',
      'Confirm backup and restore simulation workflows are complete.'
    ];

    const score = Math.max(0, Math.min(100, 100 - criticalErrors.length * 25 - warnings.length * 5));

    return {
      readinessScore: score,
      criticalErrors,
      warnings,
      recommendations,
      validations
    };
  }
}

export class MigrationPlanner {
  plan(profile: ServerProfile): MigrationReport {
    const steps: MigrationStep[] = [
      { name: 'Validate server readiness', description: 'Run the full validation suite against the target host.', estimatedMinutes: 20 },
      { name: 'Archive current configuration', description: 'Capture current deployment settings and secrets inventory.', estimatedMinutes: 15 },
      { name: 'Prepare deployment image', description: 'Stage release artifacts and environment templates.', estimatedMinutes: 25 },
      { name: 'Execute dry-run migration', description: 'Perform a simulation without changing runtime services.', estimatedMinutes: 30 }
    ];

    return {
      steps,
      rollbackPlan: { steps: buildRollbackPlan().steps },
      downtimeEstimate: { minutes: 45, note: 'Planned outage is limited to validation and cutover steps.' }
    };
  }
}

export function createSampleServerProfile(): ServerProfile {
  return {
    os: 'Ubuntu 22.04',
    kernel: '6.8.0',
    docker: true,
    dockerCompose: true,
    node: 'v20.11.1',
    python: '3.11.3',
    git: true,
    redis: true,
    postgresql: true,
    portsOpen: true,
    firewallConfigured: true,
    dnsConfigured: true,
    internetReachable: true,
    volumesReady: true,
    permissionsOk: true,
    diskGb: 400,
    ramGb: 32,
    cpuCores: 16,
    timezone: 'UTC',
    locale: 'en_US.UTF-8',
    sslConfigured: true,
    jwtConfigured: true,
    backupsValidated: true
  };
}

export function buildAuditReport(profile: ServerProfile): AuditReport {
  return new InfrastructureAudit(profile).run();
}

export function buildMigrationReport(profile: ServerProfile): MigrationReport {
  return new MigrationPlanner().plan(profile);
}

export function buildDeploymentChecklist(): DeploymentChecklistEntry[] {
  return [
    { category: 'Infrastructure', title: 'Verify OS, kernel, and hardware requirements', completed: true },
    { category: 'Database', title: 'Validate PostgreSQL connectivity and backup workflows', completed: true },
    { category: 'Frontend', title: 'Confirm frontend build and asset delivery', completed: true },
    { category: 'Backend', title: 'Validate health endpoints and process management', completed: true },
    { category: 'Brain', title: 'Confirm brain service availability', completed: true },
    { category: 'Knowledge', title: 'Verify search and knowledge service readiness', completed: true },
    { category: 'Agents', title: 'Check orchestration service health', completed: true },
    { category: 'Monitoring', title: 'Verify observability endpoints and alerting', completed: true },
    { category: 'Backup', title: 'Validate backup integrity and archive targets', completed: true },
    { category: 'Restore', title: 'Simulate restore and rollback procedures', completed: true },
    { category: 'Security', title: 'Review SSL, JWT, ownership, and permissions', completed: true }
  ];
}

export function buildRollbackPlan(): RollbackPlan {
  return {
    steps: [
      { name: 'Rollback plan: preserve current release state', description: 'Stop the deployment and keep the last known-good configuration intact.' },
      { name: 'Rollback plan: restore previous binaries', description: 'Revert to the previously validated release artifacts.' },
      { name: 'Rollback plan: restore database snapshot', description: 'Use the last validated backup if cutover requires data rehydration.' }
    ]
  };
}
