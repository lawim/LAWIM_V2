import { useEffect, useMemo, useState } from 'react';
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk, type PropertySummary } from '@api-sdk';
import {
  Badge,
  BrandMark,
  Button,
  Card,
  Checkbox,
  Input,
  LanguageProvider,
  LanguageSwitcher,
  PageShell,
  Select,
  Textarea,
  LAWIM_BRAND_SLOGAN,
  translate,
  useLanguage
} from '@ui';
import { ProtectedRoute, resolveDashboardPath, resolvePrimaryRole, type AccessRole, useAuthStore } from '@auth';
import { WorkflowOrchestratorPage } from './WorkflowOrchestratorPage';
import { ObservabilityConsolePage } from './ObservabilityConsolePage';
import { ProductReadinessDashboardPage } from './ProductReadinessDashboardPage';

const publicNavItems = [
  { to: '/', labelKey: 'nav.home' },
  { to: '/search', labelKey: 'nav.search' },
  { to: '/map', labelKey: 'nav.map' },
  { to: '/estimation', labelKey: 'nav.estimation' },
  { to: '/assistant', labelKey: 'nav.assistant' },
  { to: '/marketplace', labelKey: 'nav.marketplace' },
  { to: '/contact', labelKey: 'nav.contact' }
];

const protectedNavItems = [
  { to: '/profile', labelKey: 'nav.profile' },
  { to: '/dashboard', labelKey: 'nav.dashboard' },
  { to: '/favorites', labelKey: 'favorites.title' },
  { to: '/notifications', labelKey: 'notifications.title' },
  { to: '/requests', labelKey: 'requests.title' },
  { to: '/documents', labelKey: 'documents.title' },
  { to: '/workflow', labelKey: 'workflow.title' },
  { to: '/observability', labelKey: 'observability.title' },
  { to: '/readiness', labelKey: 'readiness.title' }
];

const dashboardModuleDefinitions = [
  {
    key: 'properties',
    titleKey: 'module.properties.title',
    descriptionKey: 'module.properties.description',
    to: '/dashboard/modules/properties',
    tone: 'info'
  },
  {
    key: 'messages',
    titleKey: 'module.messages.title',
    descriptionKey: 'module.messages.description',
    to: '/dashboard/modules/messages',
    tone: 'success'
  },
  {
    key: 'visits',
    titleKey: 'module.visits.title',
    descriptionKey: 'module.visits.description',
    to: '/dashboard/modules/visits',
    tone: 'warning'
  },
  {
    key: 'statistics',
    titleKey: 'module.statistics.title',
    descriptionKey: 'module.statistics.description',
    to: '/dashboard/modules/statistics',
    tone: 'info'
  },
  {
    key: 'documents',
    titleKey: 'module.documents.title',
    descriptionKey: 'module.documents.description',
    to: '/dashboard/modules/documents',
    tone: 'success'
  },
  {
    key: 'partners',
    titleKey: 'module.partners.title',
    descriptionKey: 'module.partners.description',
    to: '/dashboard/modules/partners',
    tone: 'warning'
  },
  {
    key: 'contact',
    titleKey: 'module.contact.title',
    descriptionKey: 'module.contact.description',
    to: '/dashboard/modules/contact',
    tone: 'info'
  },
  {
    key: 'admin',
    titleKey: 'module.admin.title',
    descriptionKey: 'module.admin.description',
    to: '/dashboard/modules/admin',
    tone: 'success'
  }
] as const;

function useTranslator() {
  const { language } = useLanguage();
  return {
    language,
    t: (key: string, params?: Record<string, string | number>) => translate(key, language, params)
  };
}

function getInitials(name: string | undefined | null) {
  const cleaned = String(name || '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (cleaned.length === 0) {
    return 'LW';
  }
  return cleaned
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
    .slice(0, 2);
}

function roleTranslationKey(role: AccessRole | string) {
  return `role.${String(role || 'user')}`;
}

function titleCase(value: string) {
  return value
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function LoadingState({ label }: { label: string }) {
  return <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 text-sm text-slate-300">{label}</div>;
}

function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return (
    <div className="rounded-2xl border border-rose-500/20 bg-rose-500/10 p-6 text-sm text-rose-300">
      <p>{message}</p>
      {retry ? <Button className="mt-4" onClick={retry}>Retry</Button> : null}
    </div>
  );
}

function EmptyState({ label }: { label: string }) {
  return <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/40 p-6 text-sm text-slate-400">{label}</div>;
}

function HomePage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const navigate = useNavigate();
  const { t } = useTranslator();
  const role = resolvePrimaryRole(user?.role, roles);
  const dashboardPath = resolveDashboardPath(role);

  return (
    <PageShell
      eyebrow={t('app.name')}
      title={t('dashboard.title')}
      description={t('auth.login.banner.note')}
      actions={
        <>
          <Button type="button" onClick={() => navigate('/login')}>
            {t('nav.login')}
          </Button>
          <Button type="button" variant="secondary" onClick={() => navigate(isAuthenticated ? dashboardPath : '/search')}>
            {isAuthenticated ? t('dashboard.return_dashboard') : t('nav.search')}
          </Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card title={t('dashboard.quick_stats')} description={t('dashboard.module_hint')}>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="info">{t('role.admin')}</Badge>
              <p className="mt-3 text-sm text-slate-300">{t('module.admin.description')}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="success">{t('role.manager')}</Badge>
              <p className="mt-3 text-sm text-slate-300">{t('dashboard.priorities')}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="warning">{t('role.operator')}</Badge>
              <p className="mt-3 text-sm text-slate-300">{t('dashboard.activity_today')}</p>
            </div>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <Button type="button" onClick={() => navigate('/login')}>
              {t('nav.login')}
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate(isAuthenticated ? dashboardPath : '/login')}>
              {isAuthenticated ? t('dashboard.return_dashboard') : t('nav.login')}
            </Button>
          </div>
        </Card>
        <Card title={t('dashboard.whats_next')} description={t('auth.login.banner.restore')}>
          <div className="space-y-3 text-sm text-slate-300">
            <p>• {t('auth.login.email')} + {t('auth.login.password')}.</p>
            <p>• {t('dashboard.return_dashboard')}.</p>
            <p>• {t('auth.login.banner.invalid')}</p>
            <p>• {t('auth.login.banner.server_unavailable')}</p>
          </div>
        <div className="mt-5 rounded-2xl border border-brand-500/20 bg-brand-500/10 p-4 text-sm text-brand-100">
          {isAuthenticated
            ? t('dashboard.greeting', { name: user?.name || user?.email || t('shared.user') })
            : t('auth.login.banner.note')}
        </div>
      </Card>
      </div>
    </PageShell>
  );
}

function SearchPage() {
  const [query, setQuery] = useState('');
  const { data, isPending, error, refetch } = useQuery({
    queryKey: ['properties-search', query],
    queryFn: () => apiSdk.getProperties({ search: query, page: 1, pageSize: 8 })
  });

  const properties = useMemo(() => data?.data ?? [], [data]);

  return (
    <PageShell eyebrow="Discovery" title="Search opportunities" description="Browse the latest listings and refine your next move.">
      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="space-y-4">
          <div className="rounded-3xl border border-slate-800/80 bg-slate-900/60 p-4">
            <Input label="Search" placeholder="Search by title or location" value={query} onChange={(event) => setQuery(event.target.value)} />
          </div>
          {isPending ? <LoadingState label="Loading properties" /> : error ? <ErrorState message="Unable to load properties." retry={() => void refetch()} /> : properties.length === 0 ? <EmptyState label="No properties matched the current filter." /> : properties.map((property) => (
            <Card key={property.id} title={property.title} description={`${property.location} • ${property.type}`}>
              <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-slate-300">
                <span>{property.location}</span>
                <div className="flex items-center gap-3">
                  <Badge variant="success">Hot lead</Badge>
                  <span className="font-semibold text-white">€{property.price.toLocaleString()}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
        <Card title="Refine search" description="Filter by region, type, and priority.">
          <div className="flex flex-col gap-3">
            <Input label="Keyword" placeholder="Luxury villa" value={query} onChange={(event) => setQuery(event.target.value)} />
            <Select label="Category">
              <option>Residential</option>
              <option>Commercial</option>
            </Select>
            <Checkbox label="Ready to review" />
            <Button>Apply filters</Button>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function PropertyDetailPage() {
  const params = useParams();
  const { data, isPending, error, refetch } = useQuery({
    queryKey: ['property', params.id],
    queryFn: () => apiSdk.getProperty(params.id ?? '')
  });

  if (isPending) return <LoadingState label="Loading property details" />;
  if (error) return <ErrorState message="Unable to load the property." retry={() => void refetch()} />;
  if (!data?.data) return <EmptyState label="Property not found." />;

  return (
    <PageShell eyebrow="Property detail" title={data.data.title} description={data.data.description}>
      <div className="grid gap-6 lg:grid-cols-[1fr_0.7fr]">
        <Card title="Overview" description="Live property summary">
          <div className="space-y-2 text-sm text-slate-300">
            <p>Location: {data.data.location}</p>
            <p>Type: {data.data.type}</p>
            <p>Surface: {data.data.surface}</p>
            <p>Bedrooms: {data.data.bedrooms}</p>
            <p>Bathrooms: {data.data.bathrooms}</p>
          </div>
        </Card>
        <Card title="Valuation" description="Current indicative estimate">
          <p className="text-2xl font-semibold text-white">€{data.data.price.toLocaleString()}</p>
          <Badge variant="success">Available</Badge>
        </Card>
      </div>
    </PageShell>
  );
}

function MapPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['map-properties'], queryFn: () => apiSdk.getProperties({ page: 1, pageSize: 6 }) });
  return (
    <PageShell eyebrow="Location intelligence" title="Map overview" description="Visualize properties and operations across the territory.">
      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-10 text-center text-slate-300">
          {isPending ? <LoadingState label="Loading map data" /> : error ? <ErrorState message="Unable to load map data." retry={() => void refetch()} /> : <div className="space-y-2">{(data?.data ?? []).map((item) => <div key={item.id}>{item.title} • {item.location}</div>)}</div>}
        </div>
        <Card title="Live signals" description="Monitor hotspots and recent actions.">
          <div className="flex flex-col gap-2 text-sm text-slate-300">
            <div className="flex items-center justify-between"><span>North district</span><Badge variant="success">Healthy</Badge></div>
            <div className="flex items-center justify-between"><span>Harbor market</span><Badge variant="warning">Needs review</Badge></div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function EstimationPage() {
  const [address, setAddress] = useState('');
  const [surface, setSurface] = useState('');
  const [type, setType] = useState('House');
  const [expectedPrice, setExpectedPrice] = useState('');
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async () => {
    setError(null);
    const response = await apiSdk.createEstimation({ address, surface, type, expectedPrice, notes });
    if (response.message && response.message !== 'mock' && response.data.estimate === 'Pending') {
      setError('The estimation service is unavailable right now.');
    } else {
      setResult(`${response.data.estimate} • ${response.data.confidence}`);
    }
  };

  return (
    <PageShell eyebrow="Valuation" title="Estimate a property" description="Capture the essentials and generate a quick assessment.">
      <div className="grid gap-6 lg:grid-cols-[1fr_0.7fr]">
        <Card title="Property details" description="Share the information needed to build a first estimate.">
          <div className="grid gap-4 md:grid-cols-2">
            <Input label="Address" placeholder="12 Rue de la Paix" value={address} onChange={(event) => setAddress(event.target.value)} />
            <Input label="Surface" placeholder="120 m²" value={surface} onChange={(event) => setSurface(event.target.value)} />
            <Select label="Property type" value={type} onChange={(event) => setType(event.target.value)}>
              <option>House</option>
              <option>Apartment</option>
              <option>Office</option>
            </Select>
            <Input label="Expected price" placeholder="€500k" value={expectedPrice} onChange={(event) => setExpectedPrice(event.target.value)} />
            <Textarea label="Notes" placeholder="Recent renovations, view quality, parking, etc." className="md:col-span-2" value={notes} onChange={(event) => setNotes(event.target.value)} />
          </div>
        </Card>
        <Card title="Suggested outcome" description="A guided result for the current workflow.">
          <div className="space-y-3 text-sm text-slate-300">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">{result ?? 'Ready to generate an estimate.'}</div>
            {error ? <p className="text-rose-300">{error}</p> : null}
            <Button className="w-full" onClick={() => void onSubmit()}>Generate estimate</Button>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function AssistantPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['assistant'], queryFn: () => apiSdk.getAssistantSuggestions() });
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState<string | null>(null);
  const [assistantError, setAssistantError] = useState<string | null>(null);

  const sendMessage = async () => {
    setAssistantError(null);
    const response = await apiSdk.askAssistant({ message });
    if (response.data.reply) {
      setReply(response.data.reply);
    } else {
      setAssistantError('The assistant service could not answer yet.');
    }
  };

  return (
    <PageShell eyebrow="AI assistant" title="Ask your intelligent copilot" description="Use the assistant to surface the right next action.">
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <Card title="Suggested prompts" description="Get started faster with prepared workflows.">
          {isPending ? <LoadingState label="Loading prompts" /> : error ? <ErrorState message="Failed to load prompts." retry={() => void refetch()} /> : <div className="flex flex-col gap-2 text-sm text-slate-300">{(data?.data ?? []).map((item) => <div key={item.title} className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2">{item.title} — {item.description}</div>)}</div>}
        </Card>
        <Card title="Conversation" description="The assistant is ready to support your team.">
          <Textarea label="Message" placeholder="What do you want to understand today?" value={message} onChange={(event) => setMessage(event.target.value)} />
          <div className="mt-4 flex flex-wrap gap-3">
            <Button onClick={() => void sendMessage()}>Send</Button>
            <Button variant="secondary">Save draft</Button>
          </div>
          {reply ? <div className="mt-4 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-sm text-emerald-200">{reply}</div> : null}
          {assistantError ? <p className="mt-2 text-sm text-rose-300">{assistantError}</p> : null}
        </Card>
      </div>
    </PageShell>
  );
}

function MarketplacePage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['marketplace'], queryFn: () => apiSdk.getMarketListings() });
  return (
    <PageShell eyebrow="Marketplace" title="Marketplace flows" description="Coordinate offers, deals, and service requests from one place.">
      <div className="grid gap-6 md:grid-cols-2">
        {isPending ? <LoadingState label="Loading marketplace" /> : error ? <ErrorState message="Unable to load marketplace items." retry={() => void refetch()} /> : (data?.data ?? []).length === 0 ? <EmptyState label="No marketplace items loaded yet." /> : (data?.data ?? []).map((listing) => (
          <Card key={listing.id} title={listing.title} description="Available for review">
            <Badge variant="info">{listing.status}</Badge>
          </Card>
        ))}
      </div>
    </PageShell>
  );
}

function ContactPage() {
  const { t } = useTranslator();
  return (
    <PageShell eyebrow={t('module.contact.title')} title={t('contact.title')} description={t('contact.description')}>
      <Card title={t('contact.title')} description={t('contact.description')}>
        <div className="grid gap-4 md:grid-cols-2">
          <Input label={t('contact.name')} placeholder="Your name" />
          <Input label={t('contact.email')} placeholder="you@company.com" />
          <Textarea label={t('contact.message')} placeholder={t('contact.placeholder')} className="md:col-span-2" />
          <Button className="md:col-span-2">{t('contact.send')}</Button>
        </div>
      </Card>
    </PageShell>
  );
}

const dashboardConfig: Record<
  AccessRole,
  {
    eyebrow: string;
    title: string;
    description: string;
    descriptionKey: string;
    badge: string;
    badgeTone: 'info' | 'success' | 'warning';
    metrics: {
      properties: string;
      opportunities: string;
      communications: string;
      pendingTasks: string;
    };
    highlights: string[];
    highlightKeys: string[];
    actions: {
      primary: string;
      secondary: string;
    };
    actionPrimaryKey: string;
    actionSecondaryKey: string;
  }
> = {
  admin: {
    eyebrow: 'Administration LAWIM',
    title: 'Cockpit administrateur',
    description: 'Gouvernance, sécurité, diagnostics et releases.',
    descriptionKey: 'module.admin.description',
    badge: 'Supervision',
    badgeTone: 'info',
    metrics: {
      properties: 'Plateforme',
      opportunities: 'Priorités',
      communications: 'Alertes',
      pendingTasks: 'Tâches'
    },
    highlights: ['Accès', 'Audit', 'Préparation des releases'],
    highlightKeys: ['dashboard.activity_today', 'dashboard.quick_stats'],
    actions: {
      primary: 'Revoir la gouvernance',
      secondary: 'Ouvrir les métriques'
    },
    actionPrimaryKey: 'module.statistics.title',
    actionSecondaryKey: 'module.documents.title'
  },
  manager: {
    eyebrow: 'Pilotage opérationnel',
    title: 'Cockpit manager',
    description: 'Équipes, validations et priorités du jour.',
    descriptionKey: 'module.statistics.description',
    badge: 'Coordination',
    badgeTone: 'success',
    metrics: {
      properties: 'Projets',
      opportunities: 'Validations',
      communications: 'Messages',
      pendingTasks: 'Relances'
    },
    highlights: ['Équipes', 'Objectifs', 'Suivi opérationnel'],
    highlightKeys: ['dashboard.activity_today', 'dashboard.quick_stats'],
    actions: {
      primary: 'Voir les projets',
      secondary: 'Ouvrir les conversations'
    },
    actionPrimaryKey: 'module.messages.title',
    actionSecondaryKey: 'module.statistics.title'
  },
  operator: {
    eyebrow: 'Exploitation quotidienne',
    title: 'Cockpit opérateur',
    description: 'Support, qualité et traitement des demandes.',
    descriptionKey: 'module.messages.description',
    badge: 'Qualité',
    badgeTone: 'warning',
    metrics: {
      properties: 'Biens',
      opportunities: 'Demandes',
      communications: 'Messages',
      pendingTasks: 'Contrôles'
    },
    highlights: ['Support', 'Vérification', 'Modération'],
    highlightKeys: ['dashboard.activity_today', 'dashboard.quick_stats'],
    actions: {
      primary: 'Voir les biens',
      secondary: 'Ouvrir les demandes'
    },
    actionPrimaryKey: 'module.properties.title',
    actionSecondaryKey: 'module.contact.title'
  },
  partner: {
    eyebrow: 'Espace partenaire',
    title: 'Cockpit partenaire',
    description: 'Missions, rendez-vous et livrables liés à votre spécialité.',
    descriptionKey: 'module.partners.description',
    badge: 'Missions',
    badgeTone: 'success',
    metrics: {
      properties: 'Missions',
      opportunities: 'Opportunités',
      communications: 'Messages',
      pendingTasks: 'Livrables'
    },
    highlights: ['Livrables', 'Disponibilités', 'Échanges'],
    highlightKeys: ['dashboard.activity_today', 'dashboard.quick_stats'],
    actions: {
      primary: 'Voir les opportunités',
      secondary: 'Ouvrir les dossiers'
    },
    actionPrimaryKey: 'module.partners.title',
    actionSecondaryKey: 'module.contact.title'
  },
  user: {
    eyebrow: 'Espace personnel',
    title: 'Cockpit utilisateur',
    description: 'Projet, biens, documents et prochaines étapes.',
    descriptionKey: 'module.properties.description',
    badge: 'Projet',
    badgeTone: 'warning',
    metrics: {
      properties: 'Biens suivis',
      opportunities: 'Opportunités',
      communications: 'Messages',
      pendingTasks: 'Actions'
    },
    highlights: ['Projet', 'Documents', 'Favoris'],
    highlightKeys: ['dashboard.activity_today', 'dashboard.quick_stats'],
    actions: {
      primary: 'Rechercher un bien',
      secondary: 'Ouvrir les documents'
    },
    actionPrimaryKey: 'module.properties.title',
    actionSecondaryKey: 'module.documents.title'
  }
};

function DashboardHomePage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const navigate = useNavigate();
  const role = resolvePrimaryRole(user?.role, roles);
  const config = dashboardConfig[role];
  const { t } = useTranslator();
  const { data, isPending, error, refetch } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: async () => {
      const response = await apiSdk.getDashboardSummary();
      const message = response.message ?? '';
      if (message !== 'ok' && message !== 'mock') {
        throw new Error(message.includes('401') || message.includes('403') ? 'Session expirée. Veuillez vous reconnecter.' : 'Impossible de charger le tableau de bord.');
      }
      return response;
    }
  });

  const summary = data?.data ?? { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 };
  const modules = dashboardModuleDefinitions.filter((module) => module.key !== 'admin' || role === 'admin');
  const userName = user?.name || user?.email?.split('@')[0] || t('shared.user');
  const roleLabel = t(roleTranslationKey(role));
  const progressPercent = Math.min(100, summary.properties * 4 + summary.opportunities * 3 + summary.communications);
  const activityItems = [
    `${t('dashboard.stats.properties')}: ${summary.properties}`,
    `${t('dashboard.stats.opportunities')}: ${summary.opportunities}`,
    `${t('dashboard.stats.messages')}: ${summary.communications}`,
    `${t('dashboard.stats.tasks')}: ${summary.pendingTasks}`
  ];
  const priorities = [config.highlightKeys[0], config.highlightKeys[1], config.actionPrimaryKey, config.actionSecondaryKey]
    .map((key) => t(key))
    .filter(Boolean);

  useEffect(() => {
    traceAuth('DASHBOARD_RENDERED', {
      role,
      path: resolveDashboardPath(role),
      email: user?.email ?? null
    });
  }, [role, user?.email]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(14,165,233,0.2),_rgba(2,6,23,0.98)_34%,_rgba(15,23,42,0.94)_100%)] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <section className="rounded-[2rem] border border-white/10 bg-slate-950/80 p-6 shadow-[0_30px_120px_rgba(2,6,23,0.45)] backdrop-blur">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-4">
              <p className="text-xs font-semibold uppercase tracking-[0.32em] text-slate-400">{t('dashboard.today')}</p>
              <div className="flex flex-wrap items-center gap-3">
                <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">{t('dashboard.greeting', { name: userName })}</h1>
                <Badge variant="info">{roleLabel}</Badge>
              </div>
              <p className="max-w-3xl text-sm leading-7 text-slate-300">{t('dashboard.identity', { role: roleLabel })}</p>
              <div className="flex flex-wrap gap-3 text-xs uppercase tracking-[0.28em] text-slate-400">
                <span>{t('dashboard.activity_today')}</span>
                <span>•</span>
                <span>{t('dashboard.priorities')}</span>
                <span>•</span>
                <span>{t('dashboard.whats_next')}</span>
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              {[
                { label: t('dashboard.stats.properties'), value: summary.properties },
                { label: t('dashboard.stats.opportunities'), value: summary.opportunities },
                { label: t('dashboard.stats.messages'), value: summary.communications },
                { label: t('dashboard.stats.tasks'), value: summary.pendingTasks }
              ].map((item) => (
                <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <p className="text-[11px] uppercase tracking-[0.3em] text-slate-500">{item.label}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">{item.value}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <div className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
          <Card title={t('dashboard.activity_today')} description={t('dashboard.subtitle')}>
            {isPending ? (
              <LoadingState label={t('auth.session.restoring')} />
            ) : error ? (
              <ErrorState message={error instanceof Error ? error.message : t('errors.generic')} retry={() => void refetch()} />
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                {activityItems.map((item) => (
                  <div key={item} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-200">
                    {item}
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card title={t('dashboard.priorities')} description={t(config.descriptionKey)}>
            <div className="space-y-3">
              {priorities.map((item) => (
                <div key={item} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                  {item}
                </div>
              ))}
            </div>
            <div className="mt-5 flex flex-wrap gap-3">
              <Button type="button" onClick={() => navigate('/search')}>
                {t(config.actionPrimaryKey)}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/contact')}>
                {t(config.actionSecondaryKey)}
              </Button>
            </div>
          </Card>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
          <Card title={t('dashboard.quick_stats')} description={t('dashboard.module_hint')}>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.stats.properties')}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{summary.properties}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.stats.opportunities')}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{summary.opportunities}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.stats.messages')}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{summary.communications}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.stats.tasks')}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{summary.pendingTasks}</p>
              </div>
            </div>
          </Card>

          <Card title={t('dashboard.progress')} description={t('dashboard.whats_next')}>
            <div className="space-y-4">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span>{t('dashboard.stats.progress')}</span>
                  <span className="font-semibold text-white">{progressPercent}%</span>
                </div>
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
                  <div className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400" style={{ width: `${progressPercent}%` }} />
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                {config.actions.primary}
              </div>
              <div className="flex flex-wrap gap-3">
                <Button type="button" onClick={() => navigate('/dashboard/modules/partners')}>
                  {t('module.partners.title')}
                </Button>
                <Button type="button" variant="secondary" onClick={() => navigate('/dashboard/modules/documents')}>
                  {t('module.documents.title')}
                </Button>
              </div>
            </div>
          </Card>
        </div>

        <Card title={t('dashboard.whats_next')} description={t('dashboard.quick_actions')}>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.action')}</p>
              <p className="mt-3">{t(config.actionPrimaryKey)}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.next_step')}</p>
              <p className="mt-3">{t(config.actionSecondaryKey)}</p>
            </div>
          </div>
        </Card>

        <section>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.32em] text-slate-500">{t('dashboard.modules')}</p>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">{t('dashboard.module_hint')}</h2>
            </div>
            <Button type="button" variant="secondary" onClick={() => navigate('/contact')}>
              {t('module.contact.title')}
            </Button>
          </div>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {modules.map((module) => (
              <NavLink
                key={module.key}
                to={module.to}
                className="group rounded-[1.75rem] border border-white/10 bg-white/5 p-5 shadow-[0_18px_60px_rgba(2,6,23,0.35)] transition hover:-translate-y-1 hover:border-white/20 hover:bg-white/10"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[11px] uppercase tracking-[0.3em] text-slate-500">{t('module.detail.focus')}</p>
                    <h3 className="mt-2 text-lg font-semibold text-white">{t(module.titleKey)}</h3>
                    <p className="mt-2 text-sm leading-6 text-slate-300">{t(module.descriptionKey)}</p>
                  </div>
                  <Badge variant={module.tone}>{t('dashboard.open_module')}</Badge>
                </div>
                <div className="mt-5 flex items-center justify-between text-sm text-slate-400">
                  <span>{t('dashboard.return_dashboard')}</span>
                  <span className="font-semibold text-white">{t('module.learn_more')}</span>
                </div>
              </NavLink>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

function DashboardModulePage() {
  const params = useParams();
  const moduleKey = String(params.moduleKey || '').trim();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = resolvePrimaryRole(user?.role, roles);
  const { t } = useTranslator();
  const module = dashboardModuleDefinitions.find((item) => item.key === moduleKey);
  const [matchNeed, setMatchNeed] = useState('photographe');
  const isPartnerModule = moduleKey === 'partners';
  const shouldRestrictAdmin = moduleKey === 'admin' && role !== 'admin';
  const { data: partnerMatches, isPending: isPartnerMatchesPending, error: partnerMatchesError, refetch: refetchPartnerMatches } = useQuery({
    queryKey: ['dashboard-partner-matches', matchNeed],
    enabled: isPartnerModule,
    queryFn: async () => apiSdk.getMatches({ target_type: 'partner', need: matchNeed, city: 'Douala', limit: 5 })
  });

  if (!module) {
    return <Navigate to="/dashboard" replace />;
  }

  if (shouldRestrictAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <PageShell
      eyebrow={t('dashboard.modules')}
      title={t(module.titleKey)}
      description={t(module.descriptionKey)}
      actions={
        <Button type="button" variant="secondary" onClick={() => navigate('/dashboard')}>
          {t('shared.back_to_dashboard')}
        </Button>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
        <Card title={t(module.titleKey)} description={t('dashboard.whats_next')}>
          <div className="space-y-3 text-sm leading-7 text-slate-300">
            <p>{t(module.descriptionKey)}</p>
            <p>{t('module.detail.summary')}</p>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.action')}</p>
                <p className="mt-2 text-white">{t('module.learn_more')}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.next_step')}</p>
                <p className="mt-2 text-white">{t('shared.back_to_dashboard')}</p>
              </div>
            </div>
          </div>
        </Card>
        <Card title={t('dashboard.activity_today')} description={t('dashboard.quick_actions')}>
          <div className="space-y-3 text-sm text-slate-300">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">{t(module.descriptionKey)}</div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">{t('dashboard.module_hint')}</div>
          </div>
        </Card>
      </div>

      {isPartnerModule ? (
        <Card title={t('module.partners.title')} description={t('module.partners.description')}>
          <div className="space-y-4">
            <div className="grid gap-3 md:grid-cols-[1fr_auto]">
              <Input label={t('module.partners.title')} value={matchNeed} onChange={(event) => setMatchNeed(event.target.value)} placeholder="photographe, architecte, notaire..." />
              <div className="flex items-end">
                <Button type="button" onClick={() => void refetchPartnerMatches()}>
                  {t('dashboard.open_module')}
                </Button>
              </div>
            </div>
            {isPartnerMatchesPending ? (
              <LoadingState label={t('auth.session.restoring')} />
            ) : partnerMatchesError ? (
              <ErrorState message={partnerMatchesError instanceof Error ? partnerMatchesError.message : t('errors.generic')} retry={() => void refetchPartnerMatches()} />
            ) : (
              <div className="grid gap-3">
                {(partnerMatches?.data ?? []).map((match, index) => (
                  <div key={`${String(match.partner?.id ?? index)}`} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold text-white">{String(match.partner?.display_name ?? match.partner?.name ?? match.partner?.partner_type ?? 'Partner')}</p>
                        <p className="mt-1 text-xs uppercase tracking-[0.28em] text-slate-500">{String(match.partner?.partner_type ?? '')}</p>
                      </div>
                      <Badge variant="success">{Math.round(Number(match.score ?? 0))}%</Badge>
                    </div>
                    <p className="mt-3 text-sm text-slate-300">{String(match.summary ?? '')}</p>
                    <p className="mt-2 text-xs text-slate-500">{(match.reasons ?? []).join(' · ')}</p>
                  </div>
                ))}
                {(partnerMatches?.data ?? []).length === 0 ? <EmptyState label={t('errors.generic')} /> : null}
              </div>
            )}
          </div>
        </Card>
      ) : null}
    </PageShell>
  );
}

function traceAuth(step: string, details: Record<string, unknown> = {}) {
  const env = (import.meta as ImportMeta & { env?: { DEV?: boolean } }).env;
  const debugEnabled = Boolean(env?.DEV) || window.localStorage.getItem('lawim.debug.auth') === '1';
  if (debugEnabled) {
    console.debug(step, details);
  }
}

function getLoginBanner(reason?: string | null) {
  switch (reason) {
    case 'server_unavailable':
      return 'Serveur indisponible. Réessayez dans un instant.';
    case 'session_expired':
      return 'Votre session a expiré. Connectez-vous de nouveau.';
    case 'unauthorized':
      return 'Connectez-vous pour accéder à votre espace.';
    default:
      return null;
  }
}

function DashboardPage() {
  return <DashboardHomePage />;
}

function RoleDashboardPage({ role }: { role: AccessRole }) {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const navigate = useNavigate();
  const config = dashboardConfig[role];
  const activeRole = resolvePrimaryRole(user?.role, roles);
  const shouldRedirect = activeRole !== role;
  const { data, isPending, error, refetch } = useQuery({
    queryKey: ['dashboard-summary', role],
    enabled: !shouldRedirect,
    queryFn: async () => {
      const response = await apiSdk.getDashboardSummary();
      const message = response.message ?? '';
      if (message !== 'ok' && message !== 'mock') {
        throw new Error(message.includes('401') || message.includes('403') ? 'Session expirée. Veuillez vous reconnecter.' : 'Impossible de charger le tableau de bord.');
      }
      return response;
    }
  });

  useEffect(() => {
    if (shouldRedirect) {
      return;
    }
    traceAuth('DASHBOARD_RENDERED', {
      role,
      path: resolveDashboardPath(role),
      email: user?.email ?? null
    });
    traceAuth('RENDER_DONE', {
      role,
      path: resolveDashboardPath(role),
      dashboardVisible: true
    });
  }, [role, shouldRedirect, user?.email]);

  if (shouldRedirect) {
    return <Navigate to={resolveDashboardPath(activeRole)} replace />;
  }

  return (
    <PageShell
      eyebrow={config.eyebrow}
      title={config.title}
      description={`${config.description} Connecté en tant que ${user?.name || user?.email || 'utilisateur'}.`}
      actions={
        <>
          <Button type="button" onClick={() => navigate('/search')}>
            Open search
          </Button>
          <Button type="button" variant="secondary" onClick={() => navigate('/profile')}>
            Profile
          </Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card title={config.badge} description="Live metrics from the backend.">
          {isPending ? (
            <LoadingState label="Loading dashboard metrics" />
          ) : error ? (
            <ErrorState message={error instanceof Error ? error.message : 'Unable to load the dashboard.'} retry={() => void refetch()} />
          ) : (
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{config.metrics.properties}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{data?.data.properties ?? 0}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{config.metrics.opportunities}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{data?.data.opportunities ?? 0}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{config.metrics.communications}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{data?.data.communications ?? 0}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{config.metrics.pendingTasks}</p>
                <p className="mt-2 text-3xl font-semibold text-white">{data?.data.pendingTasks ?? 0}</p>
              </div>
            </div>
          )}
        </Card>
        <Card title="Role focus" description="Your current workspace emphasis.">
          <div className="space-y-4">
            <Badge variant={config.badgeTone}>{config.badge}</Badge>
            <div className="space-y-3">
              {config.highlights.map((item) => (
                <div key={item} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                  {item}
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-3">
              <Button type="button" onClick={() => navigate('/search')}>
                {config.actions.primary}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/documents')}>
                {config.actions.secondary}
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}

function LoginPage() {
  const login = useAuthStore((state) => state.login);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const hasHydrated = useAuthStore((state) => state.hasHydrated);
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = resolvePrimaryRole(user?.role, roles);
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslator();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<{ tone: 'success' | 'error'; text: string } | null>(null);
  const reason = (location.state as { reason?: string } | null)?.reason ?? null;
  const loginBanner =
    reason === 'server_unavailable'
      ? t('auth.login.banner.server_unavailable')
      : reason === 'session_expired'
        ? t('auth.login.banner.session_expired')
        : reason === 'unauthorized'
          ? t('auth.login.banner.unauthorized')
          : null;

  if (isAuthenticated) {
    return <Navigate to={resolveDashboardPath(role)} replace />;
  }

  if ((!hasHydrated || isLoading) && !email && !password && !message) {
    return (
      <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(216,180,106,0.2),_rgba(255,250,240,0.96)_36%,_rgba(243,238,230,0.94)_100%)] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
        <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-6xl flex-col justify-between gap-10">
          <div className="flex items-center justify-between">
            <BrandMark tone="light" slogan={LAWIM_BRAND_SLOGAN} />
            <div className="flex items-center gap-3">
              <LanguageSwitcher compact />
              <Badge variant="info">{t('auth.session.restoring')}</Badge>
            </div>
          </div>
          <div className="flex flex-1 items-center justify-center">
            <div className="rounded-[2rem] border border-white/70 bg-white/90 px-8 py-10 text-center shadow-[0_24px_90px_rgba(15,23,42,0.14)] backdrop-blur">
              <p className="text-sm uppercase tracking-[0.32em] text-slate-500">LAWIM</p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900">{t('auth.session.restoring')}</h1>
              <p className="mt-2 text-sm leading-7 text-slate-600">{t('auth.login.banner.restore')}</p>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(216,180,106,0.2),_rgba(255,250,240,0.96)_36%,_rgba(243,238,230,0.94)_100%)] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-6xl flex-col justify-between gap-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <BrandMark tone="light" slogan={LAWIM_BRAND_SLOGAN} />
          <div className="flex items-center gap-3">
            <LanguageSwitcher compact />
            <Badge variant="info">{t('auth.login.banner.note')}</Badge>
          </div>
        </div>

        <div className="grid flex-1 items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          <section className="space-y-8">
            <div className="max-w-2xl">
              <p className="text-xs font-semibold uppercase tracking-[0.32em] text-brand-700">{t('nav.login')}</p>
              <h1 className="mt-4 text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">{t('auth.login.title')}</h1>
              <p className="mt-4 max-w-xl text-base leading-8 text-slate-600">{t('auth.login.subtitle')}</p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="info">{t('role.admin')}</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">{t('role.admin')}</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="success">{t('role.manager')}</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">{t('dashboard.priorities')}</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="warning">{t('role.operator')}</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">{t('dashboard.activity_today')}</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="info">{t('role.partner')}</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">{t('module.partners.description')}</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="warning">{t('role.user')}</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">{t('module.documents.description')}</p>
              </div>
            </div>

            <div className="rounded-[1.75rem] border border-brand-500/20 bg-brand-500/10 p-5 text-sm leading-7 text-slate-700">
              {loginBanner ? loginBanner : t('auth.login.banner.note')}
            </div>
          </section>

          <section className="rounded-[2rem] border border-white/80 bg-white/95 p-8 shadow-[0_24px_90px_rgba(15,23,42,0.14)] backdrop-blur">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.32em] text-slate-500">{t('auth.login.title')}</p>
                <h2 className="mt-2 text-2xl font-semibold text-slate-950">{t('auth.login.title')}</h2>
              </div>
              <Badge variant="success">{t('auth.login.button')}</Badge>
            </div>

            <form
              className="mt-7 space-y-4"
              onSubmit={(event) =>
                void (async () => {
                  event.preventDefault();
                  try {
                    const session = await login({ email, password });
                    traceAuth('LOGIN_OK', { email: session.email, role: session.role });
                    traceAuth('ROLE_RESOLVED', { role: session.role, source: 'payload.user.role or payload.roles' });
                    const path = resolveDashboardPath(session.role);
                    traceAuth('DASHBOARD_SELECTED', { role: session.role, path });
                    traceAuth('APPLY_JOURNEY', { role: session.role, path });
                    navigate(path, { replace: true });
                  } catch (error) {
                    setMessage({
                      tone: 'error',
                      text: error instanceof Error ? error.message : t('errors.generic')
                    });
                  }
                })()
              }
            >
              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                <span>{t('auth.login.email')}</span>
                <input
                  className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                  placeholder="name@lawim.app"
                  autoComplete="username"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  type="email"
                />
              </label>
              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                <span>{t('auth.login.password')}</span>
                <input
                  className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                  placeholder="••••••••"
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  type="password"
                />
              </label>

              {message ? (
                <div className={`rounded-2xl border px-4 py-3 text-sm ${message.tone === 'error' ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-emerald-200 bg-emerald-50 text-emerald-700'}`}>
                  {message.text}
                </div>
              ) : null}

              <Button className="w-full justify-center py-3 text-base" disabled={isLoading} type="submit">
                {isLoading ? t('auth.login.connecting') : t('auth.login.button')}
              </Button>
            </form>

            <div className="mt-6 flex items-center justify-between text-xs uppercase tracking-[0.28em] text-slate-400">
              <span>LAWIM</span>
              <span>LAWIM</span>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

function ProfilePage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['profile-page'], queryFn: () => apiSdk.getProfile() });
  return (
    <PageShell eyebrow="Profile" title="Your workspace profile" description="Manage your preferences, identity, and coverage.">
      <Card title="Preferences" description="Personalize your experience.">
        {isPending ? <LoadingState label="Loading profile" /> : error ? <ErrorState message="Unable to load your profile." retry={() => void refetch()} /> : <div className="space-y-3 text-sm text-slate-300"><p>Role: {data?.data.role}</p><p>Email: {data?.data.email}</p><p>Name: {data?.data.name}</p></div>}
      </Card>
    </PageShell>
  );
}

function FavoritesPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['favorites'], queryFn: () => apiSdk.getFavorites() });
  return (
    <PageShell eyebrow="Favorites" title="Saved favorites" description="Keep the best opportunities at hand.">
      {isPending ? <LoadingState label="Loading favorites" /> : error ? <ErrorState message="Unable to load favorites." retry={() => void refetch()} /> : (data?.data ?? []).length === 0 ? <EmptyState label="No favorites saved yet." /> : <div className="grid gap-6 md:grid-cols-2">{(data?.data ?? []).map((item) => <Card key={item.id} title={item.title} description={item.type}><Badge variant="info">Score {item.score}</Badge></Card>)}</div>}
    </PageShell>
  );
}

function NotificationsPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['notifications'], queryFn: () => apiSdk.getNotifications() });
  return (
    <PageShell eyebrow="Notifications" title="Inbox" description="Stay updated on inspections, approvals, and signals.">
      {isPending ? <LoadingState label="Loading notifications" /> : error ? <ErrorState message="Unable to load notifications." retry={() => void refetch()} /> : (data?.data ?? []).length === 0 ? <EmptyState label="No notifications yet." /> : <div className="space-y-4">{(data?.data ?? []).map((item) => <Card key={item.id} title={item.title} description={item.message}><Badge variant={item.read ? 'default' : 'warning'}>{item.read ? 'Read' : 'Unread'}</Badge></Card>)}</div>}
    </PageShell>
  );
}

function RequestsPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['requests'], queryFn: () => apiSdk.getRequests() });
  return (
    <PageShell eyebrow="Requests" title="Service requests" description="Track ongoing requests and workflow progress.">
      {isPending ? <LoadingState label="Loading requests" /> : error ? <ErrorState message="Unable to load requests." retry={() => void refetch()} /> : (data?.data ?? []).length === 0 ? <EmptyState label="No requests to show." /> : <div className="grid gap-6 md:grid-cols-2">{(data?.data ?? []).map((item) => <Card key={item.id} title={item.title} description="Workflow updated"><Badge variant="info">{item.status}</Badge></Card>)}</div>}
    </PageShell>
  );
}

function DocumentsPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['documents'], queryFn: () => apiSdk.getDocuments() });
  return (
    <PageShell eyebrow="Documents" title="Shared documents" description="Manage the documents attached to your workspace.">
      {isPending ? <LoadingState label="Loading documents" /> : error ? <ErrorState message="Unable to load documents." retry={() => void refetch()} /> : (data?.data ?? []).length === 0 ? <EmptyState label="No documents available." /> : <div className="grid gap-6 md:grid-cols-2">{(data?.data ?? []).map((item) => <Card key={item.id} title={item.title} description={item.kind}><Badge variant="success">Ready</Badge></Card>)}</div>}
    </PageShell>
  );
}

function WebAppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const hydrate = useAuthStore((state) => state.hydrate);
  const logout = useAuthStore((state) => state.logout);
  const { t } = useTranslator();

  useEffect(() => {
    const path = window.location.pathname;
    const hadStoredToken = Boolean(window.localStorage.getItem('lawim_token'));
    traceAuth('REFRESH_START', {
      path,
      hadStoredToken
    });
    void hydrate().then((session) => {
      traceAuth('REFRESH_DONE', {
        path,
        authenticated: Boolean(session),
        role: session?.role ?? null
      });
    });
  }, [hydrate]);

  const activeRole = resolvePrimaryRole(user?.role, roles);
  const isLoginRoute = location.pathname.startsWith('/login');
  const isPublicRoute = !isLoginRoute && !location.pathname.startsWith('/dashboard') && !location.pathname.startsWith('/profile') && !location.pathname.startsWith('/favorites') && !location.pathname.startsWith('/notifications') && !location.pathname.startsWith('/requests') && !location.pathname.startsWith('/documents') && !location.pathname.startsWith('/workflow') && !location.pathname.startsWith('/observability') && !location.pathname.startsWith('/readiness');
  const publicLinks = publicNavItems.map((item) => ({ ...item, label: t(item.labelKey) }));
  const displayName = user?.name || user?.email || t('shared.user');
  const displayRole = t(roleTranslationKey(activeRole));
  const initials = getInitials(displayName);

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {!isLoginRoute ? (
        isAuthenticated ? (
          <header className="sticky top-0 z-20 border-b border-slate-800/80 bg-slate-950/90 px-4 py-4 text-slate-300 backdrop-blur sm:px-6">
            <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
              <BrandMark slogan={LAWIM_BRAND_SLOGAN} />
              <div className="flex flex-wrap items-center gap-3">
                <LanguageSwitcher compact />
                <div className="flex items-center gap-3 rounded-full border border-white/10 bg-white/5 px-3 py-2">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-sm font-semibold text-white">{initials}</div>
                  <div className="leading-tight">
                    <p className="text-sm font-semibold text-white">{displayName}</p>
                    <p className="text-xs uppercase tracking-[0.28em] text-slate-400">{displayRole}</p>
                  </div>
                </div>
                <Button type="button" variant="secondary" onClick={() => void handleLogout()}>
                  {t('auth.logout')}
                </Button>
              </div>
            </div>
          </header>
        ) : (
          <nav aria-label="Primary" className="sticky top-0 z-20 border-b border-slate-800/80 bg-slate-950/90 px-4 py-4 text-slate-300 backdrop-blur sm:px-6">
            <div className="mx-auto flex max-w-7xl flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <BrandMark slogan={LAWIM_BRAND_SLOGAN} />
              <div className="flex flex-wrap items-center gap-2 text-sm">
                <LanguageSwitcher compact />
                {publicLinks.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      isActive
                        ? 'rounded-full bg-slate-800 px-3 py-2 text-white'
                        : 'rounded-full px-3 py-2 text-slate-400 transition hover:bg-slate-900 hover:text-white'
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
                <Button type="button" onClick={() => navigate('/login')}>
                  {t('nav.login')}
                </Button>
              </div>
            </div>
          </nav>
        )
      ) : null}
      {isLoading && !isAuthenticated && !isLoginRoute ? (
        <div className="border-b border-slate-800/80 bg-slate-950 px-4 py-3 text-center text-xs uppercase tracking-[0.32em] text-slate-500">
          {t('auth.session.restoring')}
        </div>
      ) : null}
      {isAuthenticated && isPublicRoute ? (
        <div className="mx-auto max-w-7xl px-4 pt-4 text-sm text-slate-400 sm:px-6">{t('dashboard.return_dashboard')}</div>
      ) : null}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/property/:id" element={<PropertyDetailPage />} />
        <Route path="/estimation" element={<EstimationPage />} />
        <Route path="/assistant" element={<AssistantPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/dashboard/modules/:moduleKey" element={<ProtectedRoute><DashboardModulePage /></ProtectedRoute>} />
        <Route path="/dashboard/admin" element={<ProtectedRoute><Navigate to="/dashboard/modules/admin" replace /></ProtectedRoute>} />
        <Route path="/dashboard/manager" element={<ProtectedRoute><Navigate to="/dashboard/modules/statistics" replace /></ProtectedRoute>} />
        <Route path="/dashboard/operator" element={<ProtectedRoute><Navigate to="/dashboard/modules/messages" replace /></ProtectedRoute>} />
        <Route path="/dashboard/partner" element={<ProtectedRoute><Navigate to="/dashboard/modules/partners" replace /></ProtectedRoute>} />
        <Route path="/dashboard/user" element={<ProtectedRoute><Navigate to="/dashboard/modules/properties" replace /></ProtectedRoute>} />
        <Route path="/dashboard/agent" element={<ProtectedRoute><Navigate to="/dashboard/modules/messages" replace /></ProtectedRoute>} />
        <Route path="/dashboard/owner" element={<ProtectedRoute><Navigate to="/dashboard/modules/properties" replace /></ProtectedRoute>} />
        <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><NotificationsPage /></ProtectedRoute>} />
        <Route path="/requests" element={<ProtectedRoute><RequestsPage /></ProtectedRoute>} />
        <Route path="/documents" element={<ProtectedRoute><DocumentsPage /></ProtectedRoute>} />
        <Route path="/workflow" element={<WorkflowOrchestratorPage />} />
        <Route path="/observability" element={<ObservabilityConsolePage />} />
        <Route path="/readiness" element={<ProductReadinessDashboardPage />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
      {!isAuthenticated && !isLoginRoute ? (
        <div className="mx-auto max-w-7xl px-4 pb-4 text-sm text-slate-500 sm:px-6">{t('auth.login.banner.unauthorized')}</div>
      ) : null}
    </div>
  );
}

export function WebApp() {
  return (
    <LanguageProvider>
      <WebAppContent />
    </LanguageProvider>
  );
}
