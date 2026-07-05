import { useMemo, useState } from 'react';
import { NavLink, Navigate, Route, Routes, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk, type PropertySummary } from '@api-sdk';
import { Badge, Button, Card, Checkbox, Input, PageShell, Select, Textarea } from '@ui';
import { ProtectedRoute, useAuthStore } from '@auth';
import { WorkflowOrchestratorPage } from './WorkflowOrchestratorPage';
import { ObservabilityConsolePage } from './ObservabilityConsolePage';
import { ProductReadinessDashboardPage } from './ProductReadinessDashboardPage';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/search', label: 'Search' },
  { to: '/map', label: 'Map' },
  { to: '/estimation', label: 'Estimation' },
  { to: '/assistant', label: 'Assistant' },
  { to: '/marketplace', label: 'Marketplace' },
  { to: '/contact', label: 'Contact' },
  { to: '/login', label: 'Login' },
  { to: '/profile', label: 'Profile' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/favorites', label: 'Favorites' },
  { to: '/notifications', label: 'Notifications' },
  { to: '/requests', label: 'Requests' },
  { to: '/documents', label: 'Documents' },
  { to: '/workflow', label: 'Workflow' },
  { to: '/observability', label: 'Observability' },
  { to: '/readiness', label: 'Readiness' }
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
  const { data: propertiesData, isPending: propertiesPending, error: propertiesError, refetch: refetchProperties } = useQuery({
    queryKey: ['properties-home'],
    queryFn: () => apiSdk.getProperties({ page: 1, pageSize: 3 })
  });
  const { data: profileData, isPending: profilePending, error: profileError } = useQuery({
    queryKey: ['profile'],
    queryFn: () => apiSdk.getProfile()
  });
  const { data: summaryData, isPending: summaryPending, error: summaryError } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: () => apiSdk.getDashboardSummary()
  });

  return (
    <PageShell
      eyebrow="LAWIM Intelligence Platform"
      title="Operational intelligence for modern teams"
      description="Live data flowing from the LAWIM backend with activation-ready routing."
      actions={
        <>
          <Button>Launch workspace</Button>
          <Button variant="secondary">Explore capabilities</Button>
        </>
      }
    >
      <div className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr_0.9fr]">
        {summaryPending ? <LoadingState label="Loading dashboard summary" /> : summaryError ? <ErrorState message="Unable to load the dashboard summary." retry={() => void refetchProperties()} /> : <Card title="Dashboard" description="Operational overview"><div className="space-y-3 text-sm text-slate-300"><p className="text-3xl font-semibold text-white">{summaryData?.data.properties ?? 0}</p><p>{summaryData?.data.opportunities ?? 0} active opportunities and {summaryData?.data.communications ?? 0} recent communications.</p><Button variant="secondary">Open dashboard</Button></div></Card>}
        {profilePending ? <LoadingState label="Loading profile" /> : profileError ? <ErrorState message="Unable to load profile." /> : <Card title="Profile" description="Signed-in workspace"><div className="space-y-3 text-sm text-slate-300"><p className="text-xl font-semibold text-white">{profileData?.data.name ?? 'Viewer'}</p><p>{profileData?.data.role ?? 'Director'}</p><p>{profileData?.data.email ?? 'No email available'}</p></div></Card>}
        {propertiesPending ? <LoadingState label="Loading opportunities" /> : propertiesError ? <ErrorState message="Unable to load opportunities." /> : <Card title="Latest opportunities" description="Fresh demand from the backend"><div className="space-y-2 text-sm text-slate-300">{(propertiesData?.data ?? []).slice(0, 3).map((property) => <div key={property.id} className="rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2">{property.title}</div>)}</div></Card>}
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

function LoginPage() {
  const login = useAuthStore((state) => state.login);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <PageShell eyebrow="Auth" title="Sign in to LAWIM" description="Use your workspace credentials to continue.">
      <Card title="Credentials" description="Secure access for clients and operators.">
        <div className="grid gap-4">
          <Input label="Email" placeholder="name@lawim.com" value={email} onChange={(event) => setEmail(event.target.value)} />
          <Input label="Password" placeholder="••••••••" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          <Button onClick={() => void (async () => { await login({ email, password }); setMessage('Signed in successfully'); })()}>Continue</Button>
          {message ? <p className="text-sm text-emerald-300">{message}</p> : null}
        </div>
      </Card>
    </PageShell>
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

function DashboardPage() {
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['dashboard'], queryFn: () => apiSdk.getDashboardSummary() });
  return (
    <PageShell eyebrow="Client workspace" title="Dashboard" description="Follow the latest opportunities and actions in one place.">
      {isPending ? <LoadingState label="Loading dashboard" /> : error ? <ErrorState message="Unable to load the dashboard." retry={() => void refetch()} /> : <div className="grid gap-6 md:grid-cols-3"><Card title="Pipeline" description={`${data?.data.opportunities ?? 0} new opportunities`} /><Card title="Communications" description={`${data?.data.communications ?? 0} recent updates`} /><Card title="Tasks" description={`${data?.data.pendingTasks ?? 0} pending tasks`} /></div>}
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
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <nav aria-label="Primary" className="sticky top-0 z-20 border-b border-slate-800/80 bg-slate-950/90 px-4 py-4 text-slate-300 backdrop-blur sm:px-6">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-brand-600/20 text-sm font-semibold text-brand-300">LW</div>
            <div>
              <div className="font-semibold text-white">LAWIM</div>
              <div className="text-xs text-slate-500">Product experience</div>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 text-sm">
            {navItems.map((item) => (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => (isActive ? 'rounded-full bg-slate-800 px-3 py-2 text-white' : 'rounded-full px-3 py-2 text-slate-400 hover:bg-slate-900 hover:text-white')}>
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      </nav>
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
        <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><NotificationsPage /></ProtectedRoute>} />
        <Route path="/requests" element={<ProtectedRoute><RequestsPage /></ProtectedRoute>} />
        <Route path="/documents" element={<ProtectedRoute><DocumentsPage /></ProtectedRoute>} />
        <Route path="/workflow" element={<WorkflowOrchestratorPage />} />
        <Route path="/observability" element={<ObservabilityConsolePage />} />
        <Route path="/readiness" element={<ProductReadinessDashboardPage />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
      {!isAuthenticated ? <div className="mx-auto max-w-6xl px-4 pb-4 text-sm text-slate-500">Use the Login route to authenticate and unlock protected areas.</div> : null}
    </div>
  );
}
