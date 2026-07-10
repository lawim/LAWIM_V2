import { useEffect, useState } from 'react';
import { Navigate, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import {
  Badge,
  BrandMark,
  Button,
  Card,
  Checkbox,
  FeatureProvider,
  Input,
  LanguageProvider,
  LanguageSwitcher,
  PageShell,
  Select,
  Textarea,
  useFeatures,
  FEATURE_LABELS,
  LAWIM_BRAND_SLOGAN,
  LAWIM_OFFICIAL_CONTACT,
  translate,
  useLanguage,
  type FeatureKey
} from '@ui';
import { ProtectedRoute, resolveDashboardPath as resolveCockpitPath, resolvePrimaryRole, useAuthStore } from '@auth';
import { WorkflowOrchestratorPage } from './WorkflowOrchestratorPage';
import { ObservabilityConsolePage } from './ObservabilityConsolePage';
import { ProductReadinessDashboardPage } from './ProductReadinessDashboardPage';
import {
  CockpitEntryPage,
  ConversationStudioPage,
  HistoryPage,
  PartnerJourneyPage,
  ProjectDossierPage,
  PropertyJourneyPage,
  PublicLandingPage,
  RoleCockpitPage,
  SearchSpacePage
} from './lawim-cockpits';

function useTranslator() {
  const { language } = useLanguage();
  return {
    language,
    t: (key: string, params?: Record<string, string | number>) => translate(key, language, params)
  };
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

function OfficialContactGrid({ tone = 'light', className = '' }: { tone?: 'light' | 'dark'; className?: string }) {
  const { t } = useTranslator();
  const phoneDigits = LAWIM_OFFICIAL_CONTACT.phoneInternational.replace(/[^0-9]/g, '');
  const items = [
    {
      icon: '🌐',
      label: t('auth.contact.website'),
      value: LAWIM_OFFICIAL_CONTACT.websiteUrl.replace(/^https?:\/\//, ''),
      href: LAWIM_OFFICIAL_CONTACT.websiteUrl,
      external: true
    },
    {
      icon: '✉️',
      label: t('auth.contact.email'),
      value: LAWIM_OFFICIAL_CONTACT.supportEmail,
      href: `mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}`,
      external: false
    },
    {
      icon: '📞',
      label: t('auth.contact.phone'),
      value: LAWIM_OFFICIAL_CONTACT.phoneInternational,
      href: `tel:+${phoneDigits}`,
      external: false
    },
    {
      icon: '💬',
      label: t('auth.contact.whatsapp'),
      value: LAWIM_OFFICIAL_CONTACT.whatsappUsername,
      href: `https://wa.me/${phoneDigits}`,
      external: true
    },
    {
      icon: 'f',
      label: t('auth.contact.facebook'),
      value: LAWIM_OFFICIAL_CONTACT.facebookUsername,
      href: `https://facebook.com/${LAWIM_OFFICIAL_CONTACT.facebookUsername.replace(/^@/, '')}`,
      external: true
    }
  ];

  const itemClasses =
    tone === 'light'
      ? 'border-slate-200/80 bg-white/80 text-slate-800 shadow-sm hover:border-brand-500/30'
      : 'border-white/10 bg-white/5 text-slate-100 hover:border-brand-500/30';
  const labelClasses = tone === 'light' ? 'text-slate-500' : 'text-slate-400';

  return (
    <div className={`grid gap-3 sm:grid-cols-2 lg:grid-cols-3 ${className}`.trim()}>
      {items.map((item) => (
        <a
          key={item.label}
          className={`flex items-start gap-3 rounded-2xl border px-3 py-3 transition hover:-translate-y-0.5 hover:no-underline ${itemClasses}`}
          href={item.href}
          target={item.external ? '_blank' : undefined}
          rel={item.external ? 'noreferrer' : undefined}
          aria-label={`${item.label} ${item.value}`}
        >
          <span className="mt-0.5 text-base" aria-hidden="true">
            {item.icon}
          </span>
          <span className="grid gap-0.5">
            <span className={`text-[0.68rem] uppercase tracking-[0.22em] ${labelClasses}`}>{item.label}</span>
            <strong className="text-sm font-semibold">{item.value}</strong>
          </span>
        </a>
      ))}
    </div>
  );
}

function AccessFooterBand() {
  const { t } = useTranslator();
  const phoneDigits = LAWIM_OFFICIAL_CONTACT.phoneInternational.replace(/[^0-9]/g, '');

  return (
    <footer className="mt-4 flex flex-wrap items-center justify-center gap-x-3 gap-y-2 rounded-full border border-slate-200/65 bg-white/72 px-4 py-2 text-[0.62rem] font-medium uppercase tracking-[0.22em] text-slate-500 shadow-sm backdrop-blur">
      <a className="transition hover:text-slate-800" href={LAWIM_OFFICIAL_CONTACT.websiteUrl} target="_blank" rel="noreferrer">
        lawim.app
      </a>
      <a className="transition hover:text-slate-800" href={`mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}`}>
        {LAWIM_OFFICIAL_CONTACT.supportEmail}
      </a>
      <a className="transition hover:text-slate-800" href={`https://wa.me/${phoneDigits}`} target="_blank" rel="noreferrer">
        {t('auth.contact.whatsapp')}
      </a>
      <a className="transition hover:text-slate-800" href={`https://facebook.com/${LAWIM_OFFICIAL_CONTACT.facebookUsername.replace(/^@/, '')}`} target="_blank" rel="noreferrer">
        {LAWIM_OFFICIAL_CONTACT.facebookUsername}
      </a>
    </footer>
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
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <Card title={t('contact.title')} description={t('contact.description')}>
          <OfficialContactGrid tone="dark" />
          <div className="mt-6 flex flex-wrap gap-3">
            <Button type="button" onClick={() => window.location.assign(`mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}`)}>
              {t('nav.contact')}
            </Button>
            <Button type="button" variant="secondary" onClick={() => window.location.assign(LAWIM_OFFICIAL_CONTACT.websiteUrl)}>
              {LAWIM_OFFICIAL_CONTACT.websiteUrl.replace(/^https?:\/\//, '')}
            </Button>
          </div>
        </Card>
        <Card title={t('contact.title')} description={t('contact.description')}>
          <div className="grid gap-4 md:grid-cols-2">
            <Input label={t('contact.name')} placeholder="Your name" />
            <Input label={t('contact.email')} placeholder="you@company.com" />
            <Textarea label={t('contact.message')} placeholder={t('contact.placeholder')} className="md:col-span-2" />
            <Button className="md:col-span-2">{t('contact.send')}</Button>
          </div>
        </Card>
      </div>
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

function LoginPage() {
  const login = useAuthStore((state) => state.login);
  const registerAccount = useAuthStore((state) => state.register);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const hasHydrated = useAuthStore((state) => state.hasHydrated);
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = resolvePrimaryRole(user?.role, roles);
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslator();
  const { language, setLanguage } = useLanguage();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [registerForm, setRegisterForm] = useState(() => ({
    fullName: '',
    email: '',
    username: '',
    phone: '',
    password: '',
    confirmPassword: '',
    preferredLanguage: language,
    acceptTerms: false
  }));
  const [message, setMessage] = useState<{ tone: 'success' | 'error' | 'info'; text: string } | null>(null);
  const reason = (location.state as { reason?: string } | null)?.reason ?? null;
  const loginBanner =
    reason === 'server_unavailable'
      ? t('auth.login.banner.server_unavailable')
      : reason === 'session_expired'
        ? t('auth.login.banner.session_expired')
        : reason === 'unauthorized'
          ? t('auth.login.banner.unauthorized')
          : null;
  const statusMessage = message ?? (loginBanner ? { tone: 'info' as const, text: loginBanner } : null);
  const isRestoring = !hasHydrated;
  const openSupportRequest = (subject: string) => {
    window.location.href = `mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}?subject=${encodeURIComponent(subject)}`;
  };

  if (isAuthenticated) {
    return <Navigate to={resolveCockpitPath(role)} replace />;
  }

  const setRegisterMode = () => {
    setMessage(null);
    setMode('register');
    setRegisterForm((current) => ({
      ...current,
      preferredLanguage: language
    }));
  };

  const setLoginMode = () => {
    setMessage(null);
    setMode('login');
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(216,180,106,0.2),_rgba(255,250,240,0.96)_36%,_rgba(243,238,230,0.94)_100%)] px-4 py-5 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-2.5rem)] max-w-3xl flex-col">
        <div className="flex items-center justify-between gap-4 py-1">
          <BrandMark tone="light" showWordmark={false} slogan={LAWIM_BRAND_SLOGAN} sloganClassName="text-sm font-serif italic tracking-normal text-slate-600 sm:text-base" />
          <LanguageSwitcher compact />
        </div>

        <div className="flex flex-1 items-center justify-center py-5">
          <section className="w-full rounded-[2rem] border border-white/80 bg-white/96 p-6 shadow-[0_24px_90px_rgba(15,23,42,0.14)] backdrop-blur sm:p-8">
            <h1 className="sr-only">{t('auth.login.title')}</h1>

            {statusMessage ? (
              <div
                className={`mb-5 rounded-2xl border px-4 py-3 text-sm ${
                  statusMessage.tone === 'error'
                    ? 'border-rose-200 bg-rose-50 text-rose-700'
                    : statusMessage.tone === 'success'
                      ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                      : 'border-brand-500/20 bg-brand-500/10 text-slate-700'
                }`}
              >
                {statusMessage.text}
              </div>
            ) : null}

            {isRestoring ? (
              <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-600">
                {t('auth.session.restoring')}
              </div>
            ) : mode === 'login' ? (
              <>
                <form
                  className="space-y-4"
                  onSubmit={(event) => {
                    event.preventDefault();
                    void (async () => {
                      try {
                        const session = await login({ identifier, password });
                        traceAuth('LOGIN_OK', { email: session.email, role: session.role });
                        traceAuth('ROLE_RESOLVED', { role: session.role, source: 'payload.user.role or payload.roles' });
                        const path = resolveCockpitPath(session.role);
                        traceAuth('COCKPIT_SELECTED', { role: session.role, path });
                        traceAuth('APPLY_COCKPIT', { role: session.role, path });
                        navigate(path, { replace: true });
                      } catch (error) {
                        setMessage({
                          tone: 'error',
                          text: error instanceof Error ? error.message : t('errors.generic')
                        });
                      }
                    })();
                  }}
                >
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.identifier')}</span>
                    <span className="text-xs font-normal text-slate-500">{t('auth.login.identifier_help')}</span>
                    <input
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      placeholder={t('auth.login.identifier_help')}
                      autoComplete="username"
                      value={identifier}
                      onChange={(event) => setIdentifier(event.target.value)}
                      required
                      type="text"
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

                  <Button className="w-full justify-center py-3 text-base shadow-[0_18px_36px_rgba(217,119,6,0.24)]" loading={isLoading} type="submit">
                    {isLoading ? t('auth.login.loading') : t('auth.login.button')}
                  </Button>
                </form>

                <div className="mt-4 flex flex-col gap-3 sm:flex-row">
                  <Button className="justify-center" type="button" variant="secondary" onClick={() => openSupportRequest('LAWIM - Mot de passe oublié')}>
                    {t('auth.login.forgot')}
                  </Button>
                  <Button className="justify-center" type="button" variant="secondary" onClick={setRegisterMode}>
                    {t('auth.login.create')}
                  </Button>
                </div>
              </>
            ) : (
              <form
                className="space-y-4"
                onSubmit={(event) => {
                  event.preventDefault();
                  void (async () => {
                    try {
                      const session = await registerAccount({
                        full_name: registerForm.fullName,
                        email: registerForm.email,
                        username: registerForm.username,
                        phone_e164: registerForm.phone,
                        password: registerForm.password,
                        password_confirmation: registerForm.confirmPassword,
                        preferred_language: registerForm.preferredLanguage,
                        accept_terms: registerForm.acceptTerms
                      });
                      traceAuth('REGISTER_OK', {
                        email: session.email,
                        role: session.role,
                        preferred_language: registerForm.preferredLanguage
                      });
                      setLanguage(registerForm.preferredLanguage);
                      const path = resolveCockpitPath(session.role);
                      navigate(path, { replace: true });
                    } catch (error) {
                      setMessage({
                        tone: 'error',
                        text: error instanceof Error ? error.message : t('errors.generic')
                      });
                    }
                  })();
                }}
              >
                <div className="grid gap-4">
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.register_full_name')}</span>
                    <input
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      placeholder="Jane Seller"
                      autoComplete="name"
                      value={registerForm.fullName}
                      onChange={(event) => setRegisterForm((current) => ({ ...current, fullName: event.target.value }))}
                      required
                      type="text"
                    />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.register_email')}</span>
                    <input
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      placeholder="name@lawim.app"
                      autoComplete="email"
                      value={registerForm.email}
                      onChange={(event) => setRegisterForm((current) => ({ ...current, email: event.target.value }))}
                      required
                      type="email"
                    />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.register_username')}</span>
                    <input
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      placeholder="lawim_user"
                      autoComplete="username"
                      value={registerForm.username}
                      onChange={(event) => setRegisterForm((current) => ({ ...current, username: event.target.value }))}
                      required
                      type="text"
                    />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.register_whatsapp')}</span>
                    <input
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      placeholder="+237686822667"
                      autoComplete="tel"
                      value={registerForm.phone}
                      onChange={(event) => setRegisterForm((current) => ({ ...current, phone: event.target.value }))}
                      required
                      type="tel"
                    />
                  </label>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                      <span>{t('auth.login.register_password')}</span>
                      <input
                        className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                        placeholder="••••••••"
                        autoComplete="new-password"
                        value={registerForm.password}
                        onChange={(event) => setRegisterForm((current) => ({ ...current, password: event.target.value }))}
                        required
                        type="password"
                      />
                    </label>
                    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                      <span>{t('auth.login.register_password_confirmation')}</span>
                      <input
                        className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                        placeholder="••••••••"
                        autoComplete="new-password"
                        value={registerForm.confirmPassword}
                        onChange={(event) => setRegisterForm((current) => ({ ...current, confirmPassword: event.target.value }))}
                        required
                        type="password"
                      />
                    </label>
                  </div>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    <span>{t('auth.login.register_language')}</span>
                    <select
                      className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 outline-none transition focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15"
                      value={registerForm.preferredLanguage}
                      onChange={(event) =>
                        setRegisterForm((current) => ({
                          ...current,
                          preferredLanguage: event.target.value as typeof language
                        }))
                      }
                      required
                    >
                      <option value="fr">{t('language.fr')}</option>
                      <option value="en">{t('language.en')}</option>
                      <option value="pcm">{t('language.pcm')}</option>
                    </select>
                  </label>
                  <label className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    <input
                      className="mt-1 h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                      checked={registerForm.acceptTerms}
                      onChange={(event) => setRegisterForm((current) => ({ ...current, acceptTerms: event.target.checked }))}
                      required
                      type="checkbox"
                    />
                    <span>{t('auth.login.register_terms')}</span>
                  </label>
                </div>

                <div className="flex flex-col gap-3 pt-1 sm:flex-row">
                  <Button className="w-full justify-center py-3 text-base sm:w-auto" loading={isLoading} type="submit">
                    {isLoading ? t('auth.login.register_loading') : t('auth.login.register_submit')}
                  </Button>
                  <Button className="w-full justify-center py-3 text-base sm:w-auto" type="button" variant="secondary" onClick={setLoginMode}>
                    {t('auth.login.register_back')}
                  </Button>
                </div>
              </form>
            )}
          </section>
        </div>

        <AccessFooterBand />
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

function LegacyModuleRedirectPage() {
  const params = useParams();
  const moduleKey = String(params.moduleKey || '').trim();

  switch (moduleKey) {
    case 'properties':
      return <Navigate to="/biens" replace />;
    case 'messages':
      return <Navigate to="/conversation" replace />;
    case 'partners':
      return <Navigate to="/partners" replace />;
    case 'statistics':
      return <Navigate to="/cockpit" replace />;
    case 'documents':
      return <Navigate to="/documents" replace />;
    case 'visits':
      return <Navigate to="/conversation" replace />;
    case 'contact':
      return <Navigate to="/contact" replace />;
    case 'admin':
      return <Navigate to="/cockpit/admin" replace />;
    default:
      return <Navigate to="/cockpit" replace />;
  }
}

function LegacyDashboardRedirectPage() {
  return <Navigate to="/cockpit" replace />;
}

function LegacyDashboardRoleRedirectPage() {
  const params = useParams();
  const role = String(params.role || '').trim();
  return <Navigate to={role ? `/cockpit/${role}` : '/cockpit'} replace />;
}

function WebAppContent() {
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

  return (
    <Routes>
      <Route path="/" element={<PublicLandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/cockpit" element={<ProtectedRoute><CockpitEntryPage /></ProtectedRoute>} />
      <Route path="/cockpit/:role" element={<ProtectedRoute><RoleCockpitPage /></ProtectedRoute>} />
      <Route path="/dashboard" element={<ProtectedRoute><LegacyDashboardRedirectPage /></ProtectedRoute>} />
      <Route path="/dashboard/:role" element={<ProtectedRoute><LegacyDashboardRoleRedirectPage /></ProtectedRoute>} />
      <Route path="/dashboard/modules/:moduleKey" element={<ProtectedRoute><LegacyModuleRedirectPage /></ProtectedRoute>} />
      <Route path="/biens" element={<ProtectedRoute><PropertyJourneyPage /></ProtectedRoute>} />
      <Route path="/search" element={<SearchSpacePage />} />
      <Route path="/conversation" element={<ProtectedRoute><ConversationStudioPage /></ProtectedRoute>} />
      <Route path="/assistant" element={<ProtectedRoute><ConversationStudioPage /></ProtectedRoute>} />
      <Route path="/dossier" element={<ProtectedRoute><ProjectDossierPage /></ProtectedRoute>} />
      <Route path="/dossier/:projectId" element={<ProtectedRoute><ProjectDossierPage /></ProtectedRoute>} />
      <Route path="/partners" element={<ProtectedRoute><PartnerJourneyPage /></ProtectedRoute>} />
      <Route path="/history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
      <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
      <Route path="/notifications" element={<ProtectedRoute><NotificationsPage /></ProtectedRoute>} />
      <Route path="/requests" element={<ProtectedRoute><RequestsPage /></ProtectedRoute>} />
      <Route path="/documents" element={<ProtectedRoute><DocumentsPage /></ProtectedRoute>} />
      <Route path="/map" element={<MapPage />} />
      <Route path="/property/:id" element={<PropertyDetailPage />} />
      <Route path="/estimation" element={<EstimationPage />} />
      <Route path="/marketplace" element={<MarketplacePage />} />
      <Route path="/contact" element={<ContactPage />} />
      <Route path="/workflow" element={<WorkflowOrchestratorPage />} />
      <Route path="/observability" element={<ObservabilityConsolePage />} />
      <Route path="/readiness" element={<ProductReadinessDashboardPage />} />
      <Route path="/admin/features" element={<ProtectedRoute><AdminFeaturesPage /></ProtectedRoute>} />
      <Route path="*" element={<PublicLandingPage />} />
    </Routes>
  );
}

function AdminFeaturesPage() {
  const { t } = useTranslator();
  const { features, setFeature, resetFeatures } = useFeatures();

  return (
    <PageShell eyebrow="Admin" title="⚙️ Gestion des fonctionnalités" description="Activez ou désactivez les fonctionnalités visibles dans les Cockpits.">
      <Card title="Fonctionnalités" description="Cochez pour activer, décochez pour masquer complètement.">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {(Object.keys(FEATURE_LABELS) as FeatureKey[]).map((key) => (
            <label key={key} className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 transition hover:border-slate-300">
              <input
                className="h-5 w-5 rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                checked={features[key]}
                onChange={() => setFeature(key, !features[key])}
                type="checkbox"
              />
              <span>{FEATURE_LABELS[key]}</span>
            </label>
          ))}
        </div>
        <div className="mt-6 flex gap-3">
          <Button type="button" onClick={resetFeatures}>
            Réinitialiser
          </Button>
        </div>
      </Card>
    </PageShell>
  );
}

export function WebApp() {
  return (
    <LanguageProvider>
      <FeatureProvider>
        <WebAppContent />
      </FeatureProvider>
    </LanguageProvider>
  );
}
