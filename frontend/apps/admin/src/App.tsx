import { NavLink, Route, Routes } from 'react-router-dom';
import { Badge, Button, Card, Input, PageShell, Select, Textarea } from '@ui';
import { AgentsConsolePage } from './AgentsConsole';
import { BrainConsolePage } from './BrainConsole';
import { ObservabilityPage } from './ObservabilityPage';
import { ProductReadinessPage } from './ProductReadinessPage';
import { InfrastructureMigrationPage } from './InfrastructureMigrationPage';
import { DeploymentOrchestratorPage } from './DeploymentOrchestratorPage';
import { AcceptanceDashboardPage } from './AcceptanceDashboardPage';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/crm', label: 'CRM' },
  { to: '/real-estate', label: 'Immobilier' },
  { to: '/marketplace', label: 'Marketplace' },
  { to: '/users', label: 'Users' },
  { to: '/iam', label: 'IAM' },
  { to: '/security', label: 'Security' },
  { to: '/communication', label: 'Communication' },
  { to: '/analytics', label: 'Analytics' },
  { to: '/operations', label: 'Operations' },
  { to: '/deployment', label: 'Deployment' },
  { to: '/backup', label: 'Backup' },
  { to: '/releases', label: 'Releases' },
  { to: '/brain', label: 'Brain' },
  { to: '/agents', label: 'Agents' },
  { to: '/source-intelligence', label: 'Source Intelligence' },
  { to: '/settings', label: 'Settings' },
  { to: '/observability', label: 'Observability' },
  { to: '/readiness', label: 'Readiness' },
  { to: '/migration', label: 'Migration' },
  { to: '/deployment-orchestrator', label: 'Orchestrator' },
  { to: '/acceptance', label: 'Acceptance' }
];

function DashboardPage() {
  return (
    <PageShell
      eyebrow="Admin Console"
      title="Manage operations and oversight"
      description="Administrative controls, governance workflows, and deployment readiness in one place."
      actions={
        <>
          <Button>Open operations</Button>
          <Button variant="secondary">Review reports</Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr_0.9fr]">
        <Card title="Signal review" description="Inspect and validate incoming intelligence flows."><div className="mt-4 flex items-center gap-3 text-sm text-slate-300"><Badge variant="warning">12 pending</Badge><span>Focus on the highest-priority items first.</span></div></Card>
        <Card title="Access control" description="Manage role-based controls and approvals."><div className="mt-4 flex items-center gap-3 text-sm text-slate-300"><Badge variant="success">Protected</Badge><span>Policies remain aligned with governance controls.</span></div></Card>
        <Card title="Release health" description="Monitor delivery quality and team readiness."><div className="mt-4 flex items-center gap-3 text-sm text-slate-300"><Badge variant="info">Healthy</Badge><span>Delivery confidence remains strong.</span></div></Card>
      </div>
    </PageShell>
  );
}

function CrmPage() {
  return (
    <PageShell eyebrow="CRM" title="Customer relationship command center" description="Track accounts and opportunities with an admin-ready view.">
      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Active accounts" description="24 engaged accounts this month"><div className="mt-4 text-sm text-slate-300">Priority accounts are moving steadily through the funnel.</div></Card>
        <Card title="Open deals" description="6 opportunities need follow-up"><div className="mt-4 text-sm text-slate-300">A dedicated follow-up queue keeps momentum high.</div></Card>
      </div>
    </PageShell>
  );
}

function RealEstatePage() {
  return (
    <PageShell eyebrow="Immobilier" title="Property operations" description="Coordinate listing quality, compliance, and approvals.">
      <Card title="Portfolio pulse" description="All assets are currently aligned with policy.">
        <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-slate-300">
          <Badge variant="success">Healthy</Badge>
          <span>Portfolio readiness is above target for this week.</span>
        </div>
      </Card>
    </PageShell>
  );
}

function MarketplacePage() {
  return (
    <PageShell eyebrow="Marketplace" title="Admin marketplace" description="Control offers, approvals, and marketplace health.">
      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Pending approvals" description="3 items are awaiting review" />
        <Card title="Revenue influence" description="High intent campaigns are trending upward" />
      </div>
    </PageShell>
  );
}

function UsersPage() {
  return (
    <PageShell eyebrow="Users" title="User administration" description="Review roles, provisioning, and governance details.">
      <Card title="Directory" description="Administrators, operators, and auditors are active.">
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge variant="info">Director</Badge>
          <Badge variant="success">Operator</Badge>
          <Badge variant="warning">Viewer</Badge>
        </div>
        <p className="mt-4 text-sm text-slate-300">Teams remain synchronized with the current operating model.</p>
      </Card>
    </PageShell>
  );
}

function IamPage() {
  return (
    <PageShell eyebrow="IAM" title="Identity and access" description="Keep policies and access levels aligned with operations.">
      <Card title="Policies" description="Least privilege controls are active across all workspaces." />
    </PageShell>
  );
}

function SecurityPage() {
  return (
    <PageShell eyebrow="Security" title="Security oversight" description="Control alerts, compliance, and audit readiness.">
      <Card title="Risk posture" description="No critical items require intervention." />
    </PageShell>
  );
}

function CommunicationPage() {
  return (
    <PageShell eyebrow="Communication" title="Communication center" description="Launch updates, templates, and campaign workflows.">
      <Card title="Templates" description="Campaign flows are ready for activation." />
    </PageShell>
  );
}

function AnalyticsPage() {
  return (
    <PageShell eyebrow="Analytics" title="Performance analytics" description="Follow adoption, growth, and service health.">
      <Card title="Adoption" description="Week-over-week activity is rising steadily." />
    </PageShell>
  );
}

function OperationsPage() {
  return (
    <PageShell eyebrow="Operations" title="Operational playbooks" description="Keep the team aligned on delivery and escalation.">
      <Card title="Daily operations" description="All critical queues are healthy." />
    </PageShell>
  );
}

function DeploymentPage() {
  return (
    <PageShell eyebrow="Deployment" title="Release deployment" description="Track rollout readiness and customer impact.">
      <Card title="Channels" description="Web and admin deployments stay synchronized." />
    </PageShell>
  );
}

function BackupPage() {
  return (
    <PageShell eyebrow="Backup" title="Backup and recovery" description="Review backup policies, retention, and restore readiness.">
      <Card title="Recovery plan" description="A tested restore path is available." />
    </PageShell>
  );
}

function ReleasesPage() {
  return (
    <PageShell eyebrow="Releases" title="Release management" description="Plan upcoming milestones and verify readiness.">
      <Card title="Upcoming release" description="The next release is queued for validation." />
    </PageShell>
  );
}

function SourceIntelligencePage() {
  return (
    <PageShell eyebrow="Source Intelligence" title="Engine overview" description="Inspect the intelligence engine, signals, and ingestion health.">
      <Card title="Signal reservoir" description="New sources are being tracked continuously." />
    </PageShell>
  );
}

function SettingsPage() {
  return (
    <PageShell eyebrow="Settings" title="Platform settings" description="Configure the console to fit your environment.">
      <Card title="Preferences" description="Tailor the admin experience to your workflow.">
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <Input label="Workspace name" placeholder="LAWIM" />
          <Select label="Theme">
            <option>Dark</option>
            <option>Light</option>
          </Select>
          <Textarea label="Notes" placeholder="Internal instructions" className="md:col-span-2" />
          <Button className="md:col-span-2">Save changes</Button>
        </div>
      </Card>
    </PageShell>
  );
}

export function AdminApp() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <nav aria-label="Primary" className="sticky top-0 z-20 border-b border-slate-300 bg-white/90 px-4 py-4 text-slate-700 backdrop-blur sm:px-6">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">LA</div>
            <div>
              <div className="font-semibold text-slate-900">LAWIM Admin</div>
              <div className="text-xs text-slate-500">Operations console</div>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 text-sm">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => (isActive ? 'rounded-full bg-slate-900 px-3 py-2 text-white' : 'rounded-full px-3 py-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900')}
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/crm" element={<CrmPage />} />
        <Route path="/real-estate" element={<RealEstatePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/iam" element={<IamPage />} />
        <Route path="/security" element={<SecurityPage />} />
        <Route path="/communication" element={<CommunicationPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/operations" element={<OperationsPage />} />
        <Route path="/deployment" element={<DeploymentPage />} />
        <Route path="/backup" element={<BackupPage />} />
        <Route path="/releases" element={<ReleasesPage />} />
        <Route path="/brain" element={<BrainConsolePage />} />
        <Route path="/agents" element={<AgentsConsolePage />} />
        <Route path="/source-intelligence" element={<SourceIntelligencePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/observability" element={<ObservabilityPage />} />
        <Route path="/readiness" element={<ProductReadinessPage />} />
        <Route path="/migration" element={<InfrastructureMigrationPage />} />
        <Route path="/deployment-orchestrator" element={<DeploymentOrchestratorPage />} />
        <Route path="/acceptance" element={<AcceptanceDashboardPage />} />
        <Route path="*" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}
