import React, { useEffect, useState } from 'react';
import { Card, Button, Badge } from '@ui';

interface Service {
  name: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'unknown';
  uptime: number;
  containers: number;
  memory_mb: number;
  cpu_percent: number;
}

interface DeploymentConfig {
  environment: string;
  version: string;
  backend_version: string;
  frontend_version: string;
  database_host: string;
  redis_host: string;
}

export function AdminDeploymentConsolePage() {
  const [services, setServices] = useState<Service[]>([]);
  const [config, setConfig] = useState<DeploymentConfig | null>(null);
  const [backups, setBackups] = useState<Array<{ date: string; size: string; status: string }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDeploymentStatus();
    const interval = setInterval(fetchDeploymentStatus, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const fetchDeploymentStatus = async () => {
    try {
      // In production, these would call real APIs
      setServices([
        { name: 'Frontend', status: 'healthy', uptime: 99.98, containers: 2, memory_mb: 512, cpu_percent: 15 },
        { name: 'Backend', status: 'healthy', uptime: 99.97, containers: 3, memory_mb: 1024, cpu_percent: 25 },
        { name: 'PostgreSQL', status: 'healthy', uptime: 99.99, containers: 1, memory_mb: 2048, cpu_percent: 12 },
        { name: 'Redis', status: 'healthy', uptime: 99.99, containers: 1, memory_mb: 512, cpu_percent: 5 },
        { name: 'Brain', status: 'healthy', uptime: 99.95, containers: 2, memory_mb: 1024, cpu_percent: 18 },
        { name: 'Agents', status: 'healthy', uptime: 99.94, containers: 3, memory_mb: 1536, cpu_percent: 22 },
        { name: 'Knowledge', status: 'healthy', uptime: 99.96, containers: 2, memory_mb: 1024, cpu_percent: 16 },
        { name: 'Communication', status: 'degraded', uptime: 99.80, containers: 2, memory_mb: 768, cpu_percent: 8 },
      ]);

      setConfig({
        environment: 'production',
        version: '2.0.0-U',
        backend_version: 'v1.8.0',
        frontend_version: 'v1.5.0',
        database_host: 'postgres.lawim.internal',
        redis_host: 'redis.lawim.internal',
      });

      setBackups([
        { date: '2024-07-04 02:30', size: '2.4 GB', status: 'successful' },
        { date: '2024-07-03 02:30', size: '2.3 GB', status: 'successful' },
        { date: '2024-07-02 02:30', size: '2.2 GB', status: 'successful' },
      ]);

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch deployment status', error);
    }
  };

  const handleRestart = async (service: string) => {
    // TODO: Implement restart logic
  };

  const handleBackup = async () => {
    // TODO: Implement backup logic
  };

  const handleScaleService = async (service: string, replicas: number) => {
    // TODO: Implement scaling logic
  };

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Deployment Console</h1>
        <Button onClick={handleBackup}>Create Backup</Button>
      </div>

      {/* Configuration */}
      {config && (
        <Card title="Configuration" description="Current deployment configuration">
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
            <div>
              <p className="text-sm text-gray-500">Environment</p>
              <p className="font-mono text-lg">{config.environment}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Platform Version</p>
              <p className="font-mono text-lg">{config.version}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Backend Version</p>
              <p className="font-mono text-lg">{config.backend_version}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Frontend Version</p>
              <p className="font-mono text-lg">{config.frontend_version}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Database Host</p>
              <p className="font-mono text-sm">{config.database_host}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Redis Host</p>
              <p className="font-mono text-sm">{config.redis_host}</p>
            </div>
          </div>
        </Card>
      )}

      {/* Services Status */}
      <Card title="Services" description="Health and resource usage of running services">
        <div className="space-y-3">
          {services.map((service) => (
            <div key={service.name} className="flex items-center justify-between border-b pb-3 last:border-b-0">
              <div className="flex items-center gap-4 flex-1">
                <Badge
                  variant={
                    service.status === 'healthy'
                      ? 'success'
                      : service.status === 'degraded'
                        ? 'warning'
                        : 'warning'
                  }
                >
                  {service.status}
                </Badge>
                <div>
                  <p className="font-semibold">{service.name}</p>
                  <p className="text-xs text-gray-500">
                    Uptime: {service.uptime}% • Containers: {service.containers}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-6 text-sm">
                <div className="text-right">
                  <p className="text-gray-500">Memory</p>
                  <p className="font-mono">{service.memory_mb} MB</p>
                </div>
                <div className="text-right">
                  <p className="text-gray-500">CPU</p>
                  <p className="font-mono">{service.cpu_percent}%</p>
                </div>
                <Button
                  variant="secondary"
                  onClick={() => handleRestart(service.name)}
                >
                  Restart
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Backups */}
      <Card title="Backups" description="Recent backup operations">
        <div className="space-y-2">
          {backups.map((backup, idx) => (
            <div key={idx} className="flex items-center justify-between border-b pb-3 last:border-b-0">
              <div>
                <p className="font-mono text-sm">{backup.date}</p>
                <p className="text-xs text-gray-500">{backup.size}</p>
              </div>
              <Badge variant={backup.status === 'successful' ? 'success' : 'warning'}>
                {backup.status}
              </Badge>
            </div>
          ))}
        </div>
      </Card>

      {/* Scaling */}
      <Card title="Scaling" description="Manage service replicas">
        <div className="space-y-3">
          {['Backend', 'Agents', 'Knowledge', 'Brain'].map((service) => (
            <div key={service} className="flex items-center justify-between">
              <span>{service}</span>
              <div className="flex gap-2">
                <Button variant="secondary" onClick={() => handleScaleService(service, 1)}>
                  Scale to 1
                </Button>
                <Button variant="secondary" onClick={() => handleScaleService(service, 3)}>
                  Scale to 3
                </Button>
                <Button variant="secondary" onClick={() => handleScaleService(service, 5)}>
                  Scale to 5
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
