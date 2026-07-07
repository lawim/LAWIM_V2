import { useEffect, useMemo, useState } from 'react';
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk, type PropertySummary } from '@api-sdk';
import { Badge, BrandMark, Button, Card, Checkbox, Input, PageShell, Select, Textarea } from '@ui';
import { ProtectedRoute, resolveDashboardPath, resolvePrimaryRole, type AccessRole, useAuthStore } from '@auth';
import { WorkflowOrchestratorPage } from './WorkflowOrchestratorPage';
import { ObservabilityConsolePage } from './ObservabilityConsolePage';
import { ProductReadinessDashboardPage } from './ProductReadinessDashboardPage';

const publicNavItems = [
  { to: '/', label: 'Accueil' },
  { to: '/search', label: 'Recherche' },
  { to: '/map', label: 'Carte' },
  { to: '/estimation', label: 'Estimation' },
  { to: '/assistant', label: 'Assistant' },
  { to: '/marketplace', label: 'Marketplace' },
  { to: '/contact', label: 'Nous écrire' }
];

const protectedNavItems = [
  { to: '/profile', label: 'Profil' },
  { to: '/dashboard', label: 'Tableau de bord' },
  { to: '/favorites', label: 'Favoris' },
  { to: '/notifications', label: 'Notifications' },
  { to: '/requests', label: 'Demandes' },
  { to: '/documents', label: 'Documents' },
  { to: '/workflow', label: 'Parcours' },
  { to: '/observability', label: 'Observabilité' },
  { to: '/readiness', label: 'Préparation' }
];

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
  const role = resolvePrimaryRole(user?.role, roles);
  const dashboardPath = resolveDashboardPath(role);

  return (
    <PageShell
      eyebrow="LAWIM Intelligence Platform"
      title="Un seul espace. Cinq rôles officiels. Aucun sélecteur de rôle."
      description="LAWIM garde les parcours administrateur, manager, opérateur, partenaire et utilisateur dans le même produit. Connectez-vous avec votre email et votre mot de passe, puis le bon tableau de bord s'ouvre automatiquement."
      actions={
        <>
          <Button type="button" onClick={() => navigate('/login')}>
            Connexion
          </Button>
          <Button type="button" variant="secondary" onClick={() => navigate(isAuthenticated ? dashboardPath : '/search')}>
            {isAuthenticated ? 'Ouvrir le tableau de bord' : 'Explorer les outils publics'}
          </Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card title="Routage par rôle" description="La plateforme choisit l'espace à partir du payload API.">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="info">Administrateur</Badge>
              <p className="mt-3 text-sm text-slate-300">Gouvernance, supervision et contrôle de la plateforme.</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="success">Manager</Badge>
              <p className="mt-3 text-sm text-slate-300">Pilotage opérationnel, validations et équipes.</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <Badge variant="warning">Opérateur</Badge>
              <p className="mt-3 text-sm text-slate-300">Support, qualité et traitement des demandes.</p>
            </div>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <Button type="button" onClick={() => navigate('/login')}>
              Aller à la connexion
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate(isAuthenticated ? dashboardPath : '/login')}>
              Ouvrir l'espace
            </Button>
          </div>
        </Card>
        <Card title="Ce que vous obtenez" description="Une entrée plus nette, plus rapide, sans formulaire de rôle.">
          <div className="space-y-3 text-sm text-slate-300">
            <p>• Email et mot de passe uniquement.</p>
            <p>• Sélection automatique du tableau de bord à partir de `payload.user.role`.</p>
            <p>• Messages clairs pour les identifiants incorrects, les sessions expirées et les serveurs indisponibles.</p>
            <p>• Une marque LAWIM cohérente sur toutes les pages.</p>
          </div>
          <div className="mt-5 rounded-2xl border border-brand-500/20 bg-brand-500/10 p-4 text-sm text-brand-100">
            {isAuthenticated ? `Bienvenue ${user?.name || user?.email || 'utilisateur'}. Votre rôle actif est ${role}.` : 'Les nouveaux utilisateurs voient la même porte d’entrée que les utilisateurs déjà connectés.'}
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
  return (
    <PageShell eyebrow="Contact" title="Stay in touch" description="Reach the team for onboarding, collaboration, or support.">
      <Card title="Contact the LAWIM team" description="We reply within one business day.">
        <div className="grid gap-4 md:grid-cols-2">
          <Input label="Name" placeholder="Your name" />
          <Input label="Email" placeholder="you@company.com" />
          <Textarea label="Message" placeholder="How can we help?" className="md:col-span-2" />
          <Button className="md:col-span-2">Send message</Button>
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
    badge: string;
    badgeTone: 'info' | 'success' | 'warning';
    metrics: {
      properties: string;
      opportunities: string;
      communications: string;
      pendingTasks: string;
    };
    highlights: string[];
    actions: {
      primary: string;
      secondary: string;
    };
  }
> = {
  admin: {
    eyebrow: 'Administration LAWIM',
    title: 'Cockpit administrateur',
    description: 'Gouvernance, sécurité, diagnostics et releases.',
    badge: 'Supervision',
    badgeTone: 'info',
    metrics: {
      properties: 'Plateforme',
      opportunities: 'Priorités',
      communications: 'Alertes',
      pendingTasks: 'Tâches'
    },
    highlights: ['Accès', 'Audit', 'Préparation des releases'],
    actions: {
      primary: 'Revoir la gouvernance',
      secondary: 'Ouvrir les métriques'
    }
  },
  manager: {
    eyebrow: 'Pilotage opérationnel',
    title: 'Cockpit manager',
    description: 'Équipes, validations et priorités du jour.',
    badge: 'Coordination',
    badgeTone: 'success',
    metrics: {
      properties: 'Projets',
      opportunities: 'Validations',
      communications: 'Messages',
      pendingTasks: 'Relances'
    },
    highlights: ['Équipes', 'Objectifs', 'Suivi opérationnel'],
    actions: {
      primary: 'Voir les projets',
      secondary: 'Ouvrir les conversations'
    }
  },
  operator: {
    eyebrow: 'Exploitation quotidienne',
    title: 'Cockpit opérateur',
    description: 'Support, qualité et traitement des demandes.',
    badge: 'Qualité',
    badgeTone: 'warning',
    metrics: {
      properties: 'Biens',
      opportunities: 'Demandes',
      communications: 'Messages',
      pendingTasks: 'Contrôles'
    },
    highlights: ['Support', 'Vérification', 'Modération'],
    actions: {
      primary: 'Voir les biens',
      secondary: 'Ouvrir les demandes'
    }
  },
  partner: {
    eyebrow: 'Espace partenaire',
    title: 'Cockpit partenaire',
    description: 'Missions, rendez-vous et livrables liés à votre spécialité.',
    badge: 'Missions',
    badgeTone: 'success',
    metrics: {
      properties: 'Missions',
      opportunities: 'Opportunités',
      communications: 'Messages',
      pendingTasks: 'Livrables'
    },
    highlights: ['Livrables', 'Disponibilités', 'Échanges'],
    actions: {
      primary: 'Voir les opportunités',
      secondary: 'Ouvrir les dossiers'
    }
  },
  user: {
    eyebrow: 'Espace personnel',
    title: 'Cockpit utilisateur',
    description: 'Projet, biens, documents et prochaines étapes.',
    badge: 'Projet',
    badgeTone: 'warning',
    metrics: {
      properties: 'Biens suivis',
      opportunities: 'Opportunités',
      communications: 'Messages',
      pendingTasks: 'Actions'
    },
    highlights: ['Projet', 'Documents', 'Favoris'],
    actions: {
      primary: 'Rechercher un bien',
      secondary: 'Ouvrir les documents'
    }
  }
};

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
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const sessionExpired = useAuthStore((state) => state.sessionExpired);
  const role = resolvePrimaryRole(user?.role, roles);

  useEffect(() => {
    if (isAuthenticated) {
      traceAuth('DASHBOARD_SELECTED', {
        role,
        path: resolveDashboardPath(role)
      });
    }
  }, [isAuthenticated, role]);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center px-6 py-16">
        <div className="rounded-3xl border border-slate-800 bg-slate-950/70 px-6 py-8 text-center text-slate-200 shadow-[0_20px_80px_rgba(2,6,23,0.35)]">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">LAWIM</p>
          <h2 className="mt-2 text-2xl font-semibold text-white">Vérification de session</h2>
          <p className="mt-2 text-sm text-slate-400">Restauration de votre espace en cours.</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ reason: sessionExpired ? 'session_expired' : 'unauthorized' }} />;
  }

  return <Navigate to={resolveDashboardPath(role)} replace />;
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
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<{ tone: 'success' | 'error'; text: string } | null>(null);
  const loginBanner = getLoginBanner((location.state as { reason?: string } | null)?.reason ?? null);

  if (isAuthenticated) {
    return <Navigate to={resolveDashboardPath(role)} replace />;
  }

  if ((!hasHydrated || isLoading) && !email && !password && !message) {
    return (
      <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.96),_rgba(219,234,254,0.75)_36%,_rgba(148,163,184,0.35)_100%)] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
        <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-6xl flex-col justify-between gap-10">
          <div className="flex items-center justify-between">
            <BrandMark tone="light" slogan="LAWIM · accompagnement immobilier intelligent" />
            <Badge variant="info">Vérification de session</Badge>
          </div>
          <div className="flex flex-1 items-center justify-center">
            <div className="rounded-[2rem] border border-white/70 bg-white/90 px-8 py-10 text-center shadow-[0_24px_90px_rgba(15,23,42,0.14)] backdrop-blur">
              <p className="text-sm uppercase tracking-[0.32em] text-slate-500">LAWIM</p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900">Connexion en cours</h1>
              <p className="mt-2 text-sm leading-7 text-slate-600">Restauration de votre session et sélection du bon tableau de bord.</p>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.96),_rgba(219,234,254,0.75)_36%,_rgba(148,163,184,0.35)_100%)] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-6xl flex-col justify-between gap-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <BrandMark tone="light" slogan="LAWIM · accompagnement immobilier intelligent" />
          <Badge variant="info">Email + mot de passe uniquement</Badge>
        </div>

        <div className="grid flex-1 items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          <section className="space-y-8">
            <div className="max-w-2xl">
              <p className="text-xs font-semibold uppercase tracking-[0.32em] text-brand-700">Accès LAWIM</p>
              <h1 className="mt-4 text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">Connectez-vous une fois. Le bon tableau de bord s'ouvre automatiquement.</h1>
              <p className="mt-4 max-w-xl text-base leading-8 text-slate-600">
                LAWIM garde les parcours administrateur, manager, opérateur, partenaire et utilisateur dans un même produit. Saisissez votre email et votre mot de passe, puis l'API choisit l'espace à afficher.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="info">Administrateur</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">Gouvernance, sécurité et supervision.</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="success">Manager</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">Équipes, validations et priorités.</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="warning">Opérateur</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">Support, qualité et demandes.</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="info">Partenaire</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">Missions, livrables et disponibilité.</p>
              </div>
              <div className="rounded-[1.5rem] border border-white/80 bg-white/80 p-4 shadow-[0_18px_60px_rgba(15,23,42,0.08)]">
                <Badge variant="warning">Utilisateur</Badge>
                <p className="mt-3 text-sm leading-6 text-slate-600">Projet personnel, biens et documents.</p>
              </div>
            </div>

            <div className="rounded-[1.75rem] border border-brand-500/20 bg-brand-500/10 p-5 text-sm leading-7 text-slate-700">
              {loginBanner ? loginBanner : 'LAWIM ne demande jamais de rôle sur cette page. Le rôle provient de la réponse API.'}
            </div>
          </section>

          <section className="rounded-[2rem] border border-white/80 bg-white/95 p-8 shadow-[0_24px_90px_rgba(15,23,42,0.14)] backdrop-blur">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.32em] text-slate-500">Accès sécurisé</p>
                <h2 className="mt-2 text-2xl font-semibold text-slate-950">Connexion</h2>
              </div>
              <Badge variant="success">Protégé</Badge>
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
                      text: error instanceof Error ? error.message : 'Connexion impossible.'
                    });
                  }
                })()
              }
            >
              <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                <span>Email</span>
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
                <span>Mot de passe</span>
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
                {isLoading ? 'Connexion...' : 'Connexion'}
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

export function WebApp() {
  const location = useLocation();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const hydrate = useAuthStore((state) => state.hydrate);

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
  const dashboardPath = resolveDashboardPath(activeRole);
  const navItems = isAuthenticated
    ? [
        ...publicNavItems,
        ...protectedNavItems.map((item) => (item.to === '/dashboard' ? { ...item, to: dashboardPath } : item))
      ]
    : [...publicNavItems, { to: '/login', label: 'Connexion' }];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {!location.pathname.startsWith('/login') ? (
        <nav aria-label="Primary" className="sticky top-0 z-20 border-b border-slate-800/80 bg-slate-950/90 px-4 py-4 text-slate-300 backdrop-blur sm:px-6">
          <div className="mx-auto flex max-w-6xl flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <BrandMark slogan="LAWIM · accompagnement immobilier intelligent" />
            <div className="flex flex-wrap gap-2 text-sm">
              {navItems.map((item) => (
                <NavLink key={item.to} to={item.to} className={({ isActive }) => (isActive ? 'rounded-full bg-slate-800 px-3 py-2 text-white' : 'rounded-full px-3 py-2 text-slate-400 hover:bg-slate-900 hover:text-white')}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>
        </nav>
      ) : null}
      {isLoading && !isAuthenticated && !location.pathname.startsWith('/login') ? <div className="border-b border-slate-800/80 bg-slate-950 px-4 py-3 text-center text-xs uppercase tracking-[0.32em] text-slate-500">Restauration de session</div> : null}
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
        <Route path="/dashboard/admin" element={<ProtectedRoute><RoleDashboardPage role="admin" /></ProtectedRoute>} />
        <Route path="/dashboard/manager" element={<ProtectedRoute><RoleDashboardPage role="manager" /></ProtectedRoute>} />
        <Route path="/dashboard/operator" element={<ProtectedRoute><RoleDashboardPage role="operator" /></ProtectedRoute>} />
        <Route path="/dashboard/partner" element={<ProtectedRoute><RoleDashboardPage role="partner" /></ProtectedRoute>} />
        <Route path="/dashboard/user" element={<ProtectedRoute><RoleDashboardPage role="user" /></ProtectedRoute>} />
        <Route path="/dashboard/agent" element={<ProtectedRoute><Navigate to="/dashboard/operator" replace /></ProtectedRoute>} />
        <Route path="/dashboard/owner" element={<ProtectedRoute><Navigate to="/dashboard/user" replace /></ProtectedRoute>} />
        <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><NotificationsPage /></ProtectedRoute>} />
        <Route path="/requests" element={<ProtectedRoute><RequestsPage /></ProtectedRoute>} />
        <Route path="/documents" element={<ProtectedRoute><DocumentsPage /></ProtectedRoute>} />
        <Route path="/workflow" element={<WorkflowOrchestratorPage />} />
        <Route path="/observability" element={<ObservabilityConsolePage />} />
        <Route path="/readiness" element={<ProductReadinessDashboardPage />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
      {!isAuthenticated && !location.pathname.startsWith('/login') ? <div className="mx-auto max-w-6xl px-4 pb-4 text-sm text-slate-500">Utilisez la page de connexion pour accéder aux espaces protégés.</div> : null}
    </div>
  );
}
