import { useEffect, useMemo, useState, type FormEvent, type ReactNode } from 'react';
import { Navigate, NavLink, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk, type MatchQuery, type ProjectSummary } from '@api-sdk';
import {
  Badge,
  BrandMark,
  Button,
  Input,
  LanguageSwitcher,
  LAWIM_BRAND_SLOGAN,
  LAWIM_OFFICIAL_CONTACT,
  Select,
  Textarea,
  translate,
  useFeatures,
  useFeature,
  type FeatureKey,
  useLanguage
} from '@ui';
import { resolveDashboardPath, resolvePrimaryRole, useAuthStore } from '@auth';
import { AdvisorPanel, AdvisorWidget } from './AdvisorPanel';
import { MatchSummaryWidget } from './MatchResultsPanel';

type MissionRole = 'admin' | 'manager' | 'agent' | 'partner' | 'user' | 'investor';
type Lang = 'fr' | 'en' | 'pcm';

type FrameProps = {
  title: string;
  children: ReactNode;
};

const MISSION_ROLE_BY_ACCESS_ROLE: Record<string, MissionRole> = {
  admin: 'admin',
  manager: 'manager',
  operator: 'agent',
  partner: 'partner',
  investor: 'investor',
  user: 'user'
};

const ROLE_LABEL_BY_MISSION_ROLE: Record<MissionRole, string> = {
  admin: 'role.admin',
  manager: 'role.manager',
  agent: 'role.agent',
  partner: 'role.partner',
  user: 'role.user',
  investor: 'role.investor'
};

function useTranslator() {
  const { language } = useLanguage();
  return {
    language,
    t: (key: string, params?: Record<string, string | number>) => translate(key, language, params)
  };
}

function missionRoleFromAccessRole(role: string | null | undefined): MissionRole {
  if (!role) return 'user';
  return MISSION_ROLE_BY_ACCESS_ROLE[role] ?? 'user';
}

function getInitials(value: string | undefined | null) {
  const parts = String(value ?? '').trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return 'LW';
  return parts.slice(0, 2).map((part) => part[0]?.toUpperCase() ?? '').join('').slice(0, 2);
}

function formatMoney(value?: number | null) {
  if (value == null) return '—';
  return new Intl.NumberFormat('fr-FR').format(value);
}

function getFirstName(value: string | undefined | null) {
  const parts = String(value ?? '').trim().split(/\s+/).filter(Boolean);
  return parts[0] ?? '';
}

function formatPropertyPrice(price?: number | null): string {
  if (price == null) return '';
  return `${formatMoney(price)} FCFA`;
}

function describeProjectTheme(objective?: string | null) {
  const lower = String(objective ?? '').toLowerCase();
  if (lower.includes('construct')) return 'construction';
  if (lower.includes('terrain')) return 'terrain';
  if (lower.includes('location') || lower.includes('louer')) return 'location';
  if (lower.includes('invest')) return 'investissement';
  if (lower.includes('achat') || lower.includes('acqu')) return 'achat';
  if (lower.includes('vente')) return 'vente';
  return 'projet';
}

const LANDING_ICONS: Record<string, string> = {
  conversation: '💬',
  project: '📁',
  partners: '🤝',
  search: '🔎',
  add: '➕',
  stats: '📊',
  settings: '⚙️',
  logout: '🚪',
  profile: '👤',
  documents: '📄',
  calendar: '📅',
  contact: '✉️',
  home: '🏠',
  land: '🌍',
  building: '🏗️',
  invest: '💰',
  rent: '🔑',
  alert: '⚠️',
  check: '✅',
  info: 'ℹ️',
  back: '←'
};

function CompactFooter() {
  const { t } = useTranslator();
  const phoneDigits = LAWIM_OFFICIAL_CONTACT.phoneInternational.replace(/[^0-9]/g, '');
  return (
    <footer className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 px-4 py-2 text-xs text-slate-400">
      <a className="hover:text-slate-700" href={LAWIM_OFFICIAL_CONTACT.websiteUrl} target="_blank" rel="noreferrer">🌐 lawim.app</a>
      <a className="hover:text-slate-700" href={`mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}`}>✉️ {LAWIM_OFFICIAL_CONTACT.supportEmail}</a>
      <a className="hover:text-slate-700" href={`tel:+${phoneDigits}`}>📞 {LAWIM_OFFICIAL_CONTACT.phoneInternational}</a>
      <a className="hover:text-slate-700" href={`https://wa.me/${phoneDigits}`} target="_blank" rel="noreferrer">💬 {t('auth.contact.whatsapp')}</a>
      <a className="hover:text-slate-700" href={`https://facebook.com/${LAWIM_OFFICIAL_CONTACT.facebookUsername.replace(/^@/, '')}`} target="_blank" rel="noreferrer">📘 {LAWIM_OFFICIAL_CONTACT.facebookUsername}</a>
    </footer>
  );
}

function Surface({ className = '', children }: { className?: string; children: ReactNode }) {
  return (
    <section className={`rounded-2xl border border-slate-200/80 bg-white/90 shadow-sm ${className}`.trim()}>
      {children}
    </section>
  );
}

function RoleBadge({ role }: { role: MissionRole }) {
  const { t } = useTranslator();
  const colors: Record<MissionRole, string> = {
    admin: 'bg-slate-900 text-white',
    manager: 'bg-amber-500 text-white',
    agent: 'bg-sky-500 text-white',
    partner: 'bg-emerald-500 text-white',
    user: 'bg-indigo-500 text-white',
    investor: 'bg-rose-500 text-white'
  };
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold ${colors[role]}`}>
      {t(ROLE_LABEL_BY_MISSION_ROLE[role])}
    </span>
  );
}

function StatLine({ items }: { items: { icon: string; label: string; value: string }[] }) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      {items.map((item) => (
        <div key={item.label} className="flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1.5 text-sm">
          <span>{item.icon}</span>
          <span className="font-semibold text-slate-900">{item.value}</span>
          <span className="text-slate-500">{item.label}</span>
        </div>
      ))}
    </div>
  );
}

export function PublicLandingPage() {
  const { t, language } = useTranslator();
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const roles = useAuthStore((state) => state.roles);
  const user = useAuthStore((state) => state.user);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const loginAction = useAuthStore((state) => state.login);
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [registerForm, setRegisterForm] = useState({
    fullName: '', email: '', username: '', phone: '', password: '', confirmPassword: '', preferredLanguage: language, acceptTerms: false
  });

  if (isAuthenticated) {
    return <Navigate to={resolveDashboardPath(role)} replace />;
  }

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();
    if (!identifier.trim() || !password) return;
    setLoginError(null);
    setIsLoggingIn(true);
    try {
      const session = await loginAction({ identifier: identifier.trim(), password });
      navigate(resolveDashboardPath(session.role), { replace: true });
    } catch (err) {
      setLoginError(err instanceof Error ? err.message : t('errors.generic'));
    } finally {
      setIsLoggingIn(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-gradient-to-br from-slate-50 to-white text-slate-900">
      <header className="flex items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <BrandMark slogan={LAWIM_BRAND_SLOGAN} tone="light" />
        <LanguageSwitcher compact />
      </header>

      <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center gap-6 px-4 py-6 lg:flex-row lg:items-start lg:gap-12">
        <section className="w-full max-w-md space-y-4 lg:pt-4">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight text-slate-950">💬 {t('assistant.title')}</h1>
            <p className="text-sm text-slate-500">LAWIM — {LAWIM_BRAND_SLOGAN}</p>
          </div>

          <div className="flex flex-wrap gap-2">
            <Button type="button" variant="secondary" onClick={() => navigate('/search')}>
              🔎 {t('cockpit.new_project')}
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate('/search')}>
              ➕ {t('module.properties.title')}
            </Button>
          </div>

          <Surface className="p-5">
            {!showRegister ? (
            <form onSubmit={handleLogin} className="space-y-3">
              <h2 className="text-sm font-semibold text-slate-700">🔐 {t('auth.login.title')}</h2>
              {loginError ? (
                <div className="rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-600">{loginError}</div>
              ) : null}
              <div className="flex flex-col gap-2">
                <input
                  aria-label={t('auth.login.identifier')}
                  className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
                  placeholder={t('auth.login.identifier_help')}
                  autoComplete="username"
                  value={identifier}
                  onChange={(event) => setIdentifier(event.target.value)}
                  required
                  type="text"
                />
                <input
                  aria-label={t('auth.login.password')}
                  className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
                  placeholder={t('auth.login.password')}
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  type="password"
                />
              </div>
              <div className="flex gap-2">
                <Button className="flex-1 justify-center py-2.5 text-sm" loading={isLoggingIn} type="submit">
                  {isLoggingIn ? '...' : t('auth.login.button')}
                </Button>
                <Button type="button" variant="secondary" className="py-2.5 text-sm" onClick={() => setShowRegister(true)}>
                  {t('auth.login.create')}
                </Button>
              </div>
              <button type="button" className="text-xs text-slate-400 hover:text-slate-700" onClick={() => window.location.href = `mailto:${LAWIM_OFFICIAL_CONTACT.supportEmail}?subject=${encodeURIComponent('LAWIM - Mot de passe oublié')}`}>
                {t('auth.login.forgot')}
              </button>
            </form>
            ) : (
            <div className="space-y-3">
              <h2 className="text-sm font-semibold text-slate-700">📝 {t('auth.login.register_title')}</h2>
              <div className="grid gap-3">
                <input aria-label={t('auth.login.register_full_name')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_full_name')} value={registerForm.fullName} onChange={(e) => setRegisterForm(f => ({...f, fullName: e.target.value}))} />
                <input aria-label={t('auth.login.register_email')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_email')} value={registerForm.email} onChange={(e) => setRegisterForm(f => ({...f, email: e.target.value}))} />
                <input aria-label={t('auth.login.register_username')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_username')} value={registerForm.username} onChange={(e) => setRegisterForm(f => ({...f, username: e.target.value}))} />
                <input aria-label={t('auth.login.register_whatsapp')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_whatsapp')} value={registerForm.phone} onChange={(e) => setRegisterForm(f => ({...f, phone: e.target.value}))} />
                <div className="grid gap-3 sm:grid-cols-2">
                  <input aria-label={t('auth.login.register_password')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_password')} value={registerForm.password} onChange={(e) => setRegisterForm(f => ({...f, password: e.target.value}))} type="password" />
                  <input aria-label={t('auth.login.register_password_confirmation')} className="rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-slate-900" placeholder={t('auth.login.register_password_confirmation')} value={registerForm.confirmPassword} onChange={(e) => setRegisterForm(f => ({...f, confirmPassword: e.target.value}))} type="password" />
                </div>
              </div>
              <div className="flex gap-2">
                <Button className="flex-1 justify-center py-2.5 text-sm">{t('auth.login.register_submit')}</Button>
                <Button type="button" variant="secondary" className="py-2.5 text-sm" onClick={() => setShowRegister(false)}>
                  {t('auth.login.register_back')}
                </Button>
              </div>
            </div>
            )}
          </Surface>
        </section>

        <section className="w-full max-w-sm space-y-3 lg:pt-4">
          <Surface className="p-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">💡 {t('cockpit.new_project')}</p>
            <div className="mt-3 grid grid-cols-2 gap-2">
              {[
                { icon: '🏠', label: t('module.properties.category.terrain') },
                { icon: '🏠', label: t('module.properties.category.logement') },
                { icon: '🏗️', label: t('assistant.prompt_architecte') },
                { icon: '🔑', label: t('module.properties.category.immeuble') },
                { icon: '💰', label: t('assistant.prompt_banque') },
                { icon: '🤝', label: t('module.partners.need.architect') }
              ].map((item) => (
                <button key={item.label} type="button" onClick={() => navigate('/search')}
                  className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </Surface>

          <Surface className="p-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">💬 {t('assistant.quick_prompts')}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {['🏠 ' + t('module.properties.category.logement'), '🌍 ' + t('module.properties.category.terrain'), '🔑 ' + t('nav.estimation'), '🤝 ' + t('module.partners.title')].map((label) => (
                <button key={label} type="button" onClick={() => navigate('/search')}
                  className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600 transition hover:border-slate-300"
                >
                  {label}
                </button>
              ))}
            </div>
          </Surface>
        </section>
      </div>

      <CompactFooter />
    </main>
  );
}

function smartSearch(query: string): string {
  const q = query.toLowerCase().trim();
  if (/terrain|land/.test(q)) return '/biens?type=terrain';
  if (/maison|house|villa/.test(q)) return '/biens?type=maison';
  if (/appartement|apartment/.test(q)) return '/biens?type=appartement';
  if (/invest|investir|rendement/.test(q)) return '/biens?type=investir';
  if (/construction|construire|builder/.test(q)) return '/biens?type=construire';
  if (/location|louer|rent/.test(q)) return '/biens?type=louer';
  if (/architecte|architect/.test(q)) return '/partners?need=architecte';
  if (/notaire|notary/.test(q)) return '/partners?need=notaire';
  if (/banque|bank|finance|crédit/.test(q)) return '/partners?need=banque';
  if (/photographe|photographer/.test(q)) return '/partners?need=photographe';
  if (/partenaire|partner|professionnel/.test(q)) return '/partners';
  if (/dossier|projet|project/.test(q)) return '/dossier';
  if (/message|conversation|chat|discussion/.test(q)) return '/conversation';
  if (/document|fichier|file/.test(q)) return '/documents';
  if (/favori|favorite|sauvegarde|save/.test(q)) return '/favorites';
  if (/notification|alerte|alert/.test(q)) return '/notifications';
  if (/rendez-vous|rdv|meeting|calendar/.test(q)) return '/history';
  if (/profil|profile|compte|account/.test(q)) return '/profile';
  return `/search?q=${encodeURIComponent(query)}`;
}

function CockpitFrame({ title, children }: FrameProps) {
  const { t } = useTranslator();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const logout = useAuthStore((state) => state.logout);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const displayName = user?.name || user?.email || '';
  const initials = getInitials(displayName);
  const [search, setSearch] = useState('');

  const handleSearch = (event: FormEvent) => {
    event.preventDefault();
    const trimmed = search.trim();
    if (!trimmed) { navigate('/search'); return; }
    navigate(smartSearch(trimmed));
  };

  return (
    <main className="flex min-h-screen flex-col bg-gradient-to-br from-slate-50 to-white text-slate-900">
      <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-2">
          <div className="flex items-center gap-3">
            <BrandMark slogan={LAWIM_BRAND_SLOGAN} tone="light" />
          </div>
          <div className="hidden min-w-0 flex-1 items-center gap-2 sm:flex">
            <form onSubmit={handleSearch} className="flex flex-1" data-tooltip={t('assistant.chat_hint')}>
              <input
                aria-label={t('cockpit.search')}
                placeholder="🔎"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="w-full max-w-xs rounded-full border border-slate-200 bg-slate-50 px-4 py-1.5 text-sm outline-none focus:border-slate-300"
              />
            </form>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-2 py-1">
              <div className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-900 text-[10px] font-semibold text-white">{initials}</div>
              <span className="hidden text-sm font-medium text-slate-900 sm:inline">{displayName}</span>
              <RoleBadge role={role} />
            </div>
            <LanguageSwitcher compact />
            <button type="button" aria-label={t('auth.logout')} title={t('auth.logout')} onClick={() => void logout()} className="rounded-full p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700">
              🚪
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-4 px-4 py-4">
        {children}
      </div>

      <CompactFooter />
    </main>
  );
}

function SecondaryActionsBlock({ role }: { role?: MissionRole }) {
  const { t } = useTranslator();
  const navigate = useNavigate();
  const { features } = useFeatures();

  const allItems: { icon: string; label: string; to: string; feature: FeatureKey }[] = [
    { icon: '🔎', label: t('cockpit.resume'), to: '/biens', feature: 'property_search' },
    { icon: '➕', label: t('module.properties.title'), to: '/biens', feature: 'property_add' },
    { icon: '💬', label: t('assistant.title'), to: '/conversation', feature: 'conversation' },
    { icon: '📁', label: t('dashboard.project'), to: '/dossier', feature: 'dossiers' },
    { icon: '🤝', label: t('module.partners.title'), to: '/partners', feature: 'partners' },
    { icon: '📄', label: t('module.documents.title'), to: '/documents', feature: 'documents' },
    { icon: '⭐', label: t('favorites.title'), to: '/favorites', feature: 'favorites' },
    { icon: '📊', label: t('module.detail.compare'), to: '/comparison', feature: 'comparison' },
    { icon: '🗺️', label: t('nav.map'), to: '/map', feature: 'map' },
    { icon: '🔔', label: t('nav.notifications'), to: '/notifications', feature: 'notifications' },
    { icon: '📅', label: t('assistant.project_hint'), to: '/history', feature: 'history' },
    { icon: '👤', label: t('nav.profile'), to: '/profile', feature: 'profile' },
    { icon: '💰', label: t('nav.estimation'), to: '/estimation', feature: 'estimations' },
    { icon: '✉️', label: t('module.contact.title'), to: '/contact', feature: 'profile' },
    { icon: '💳', label: 'Finances', to: '/financial', feature: 'financial_core' },
  ];

  if (role === 'admin') {
    allItems.push({ icon: '⚙️', label: t('module.admin.description'), to: '/admin/features', feature: 'admin_features' });
  }

  const visible = allItems.filter((item) => features[item.feature]);

  if (visible.length === 0) return null;

  return (
    <Surface className="p-4">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">🧭 {t('assistant.quick_prompts')}</p>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {visible.map((item) => (
          <button key={item.label} type="button" data-tooltip={item.label} onClick={() => navigate(item.to)}
            className="flex items-center gap-1.5 rounded-xl px-3 py-2 text-sm text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>
    </Surface>
  );
}

function PrimaryAction({ icon, label, to, tooltip }: { icon: string; label: string; to: string; tooltip?: string }) {
  const navigate = useNavigate();
  return (
    <button type="button" data-tooltip={tooltip} onClick={() => navigate(to)}
      className="flex items-center gap-3 rounded-2xl border border-slate-900 bg-slate-900 px-6 py-4 text-lg font-semibold text-white shadow-lg transition hover:bg-slate-800 hover:shadow-xl"
    >
      <span className="text-2xl">{icon}</span>
      <span>{label}</span>
    </button>
  );
}

function useProjectsSummary() {
  const projectsQuery = useQuery({ queryKey: ['cockpit-projects'], queryFn: () => apiSdk.getProjects() });
  const summaryQuery = useQuery({ queryKey: ['cockpit-summary'], queryFn: () => apiSdk.getDashboardSummary() });
  return {
    projects: projectsQuery.data?.data ?? [],
    projectsPending: projectsQuery.isPending,
    summary: summaryQuery.data?.data ?? { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 },
    summaryPending: summaryQuery.isPending
  };
}

function CockpitLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 text-slate-500">
      <div className="text-center">
        <div className="text-4xl">⏳</div>
        <p className="mt-2 text-sm">Chargement...</p>
      </div>
    </div>
  );
}

function RoleCockpitBody({ role, projects, summary }: { role: MissionRole; projects: ProjectSummary[]; summary: { properties: number; opportunities: number; communications: number; pendingTasks: number } }) {
  const { t, language } = useTranslator();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const firstName = getFirstName(user?.name || user?.email) || '👋';
  const { features } = useFeatures();
  const activeProject = projects[0] ?? null;
  const projectTheme = describeProjectTheme(activeProject?.objective);

  const matchQuery = useMemo<MatchQuery | undefined>(() => {
    if (role === 'admin' || role === 'manager') return undefined;
    return {
      target_type: role === 'agent' || role === 'partner' ? 'partner' : 'property',
      city: activeProject?.location_city ?? 'Douala',
      country: 'Cameroon',
      partner_type: role === 'agent' ? 'architect' : role === 'partner' ? 'bank' : undefined,
      budget_max: activeProject?.budget_max ?? undefined,
      limit: 2
    };
  }, [activeProject?.budget_max, activeProject?.location_city, role]);

  const { data: matchData } = useQuery({
    queryKey: ['cockpit-matches', role, activeProject?.id],
    queryFn: () => apiSdk.getMatches(matchQuery),
    enabled: Boolean(matchQuery)
  });
  const matches = matchData?.data ?? [];

  const { data: brainProposalsData } = useQuery({
    queryKey: ['cockpit-brain-proposals', activeProject?.id],
    queryFn: () => apiSdk.brainProposals(activeProject!.id),
    enabled: Boolean(activeProject?.id),
    staleTime: 15_000,
  });
  const brainProposals = brainProposalsData?.data ?? [];
  const hasBrainMatches = brainProposals.length > 0;

  const roleConfig = (() => {
    switch (role) {
      case 'admin':
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '🟢', label: t('assistant.context'), value: `${Math.max(94, 100 - summary.pendingTasks)}%` },
            { icon: '🔐', label: t('security.audit'), value: summary.pendingTasks > 0 ? '⚠️' : '✅' },
            { icon: '👥', label: t('role.admin'), value: '5' }
          ],
          primaryAction: { icon: '🟢', label: t('dashboard.persona.admin.primary'), to: '/observability' },
          secondActions: [
            { icon: '🔐', label: t('security.audit'), to: '/readiness' },
            { icon: '⚙️', label: t('module.admin.description'), to: '/workflow' }
          ]
        };
      case 'manager':
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '👥', label: t('dashboard.stats.tasks'), value: `${Math.max(1, projects.length + 2)}` },
            { icon: '⚠️', label: t('module.properties.status'), value: `${summary.pendingTasks}` },
            { icon: '⏱️', label: t('partner.availability'), value: summary.communications > 0 ? '🔴' : '🟢' }
          ],
          primaryAction: { icon: '📁', label: t('module.documents.actions_title'), to: '/dossier' },
          secondActions: [
            { icon: '💬', label: t('assistant.title'), to: '/conversation' },
            { icon: '📊', label: t('module.statistics.title'), to: '/history' }
          ]
        };
      case 'agent':
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '💬', label: t('dashboard.stats.messages'), value: `${Math.max(summary.communications, projects.length)}` },
            { icon: '⚠️', label: t('match.to_verify'), value: `${summary.pendingTasks}` },
            { icon: '📅', label: t('module.visits.title'), value: `${Math.max(1, summary.opportunities)}` }
          ],
          primaryAction: { icon: '💬', label: t('dashboard.continue_project'), to: '/conversation' },
          secondActions: [
            { icon: '🔍', label: t('match.to_verify'), to: '/biens' },
            { icon: '🤝', label: t('module.partners.title'), to: '/partners' }
          ]
        };
      case 'partner':
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '📋', label: t('module.partners.title'), value: `${Math.max(1, projects.length)}` },
            { icon: '📩', label: t('dashboard.stats.messages'), value: `${summary.pendingTasks}` },
            { icon: '💬', label: t('dashboard.stats.opportunities'), value: `${Math.max(1, summary.communications)}` }
          ],
          primaryAction: { icon: '📋', label: t('module.partners.results_title'), to: '/partners' },
          secondActions: [
            { icon: '💬', label: t('assistant.title'), to: '/conversation' },
            { icon: '📊', label: t('dashboard.stats.progress'), to: '/history' }
          ]
        };
      case 'investor':
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '💼', label: t('dashboard.stats.opportunities'), value: `${Math.max(summary.opportunities, projects.length)}` },
            { icon: '📩', label: t('dashboard.stats.messages'), value: `${summary.pendingTasks}` },
            { icon: '💬', label: t('dashboard.stats.messages'), value: `${Math.max(1, summary.communications)}` }
          ],
          primaryAction: { icon: '💰', label: t('dashboard.persona.investor.primary'), to: '/biens' },
          secondActions: [
            { icon: '💬', label: t('assistant.title'), to: '/conversation' },
            { icon: '📊', label: t('dashboard.stats.progress'), to: '/history' }
          ]
        };
      default:
        return {
          greeting: `👋 ${firstName}`,
          statItems: [
            { icon: '📁', label: t('dashboard.project'), value: `${Math.max(1, projects.length)}` },
            { icon: '💬', label: t('dashboard.stats.messages'), value: `${Math.max(1, summary.communications)}` },
            { icon: '✨', label: t('dashboard.stats.opportunities'), value: `${Math.max(1, summary.opportunities)}` }
          ],
          primaryAction: { icon: '🔎', label: t('dashboard.persona.user.primary'), to: '/biens' },
          secondActions: [
            { icon: '➕', label: t('module.properties.title'), to: '/biens' },
            { icon: '💬', label: t('assistant.title'), to: '/conversation' }
          ]
        };
    }
  })();

  const suggestions = role === 'user'
    ? [
        { icon: '🏠', label: t('module.properties.category.logement'), to: '/biens' },
        { icon: '🌍', label: t('module.properties.category.terrain'), to: '/biens' },
        { icon: '🔑', label: t('module.properties.category.immeuble'), to: '/biens' },
        { icon: '🏗️', label: t('module.properties.subtype'), to: '/biens' },
        { icon: '💰', label: t('assistant.prompt_banque'), to: '/partners' },
        { icon: '🤝', label: t('module.partners.need.architect'), to: '/partners' }
      ]
    : [];

  return (
    <CockpitFrame title={roleConfig.greeting}>
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl">👋</span>
          <div>
            <h1 className="text-xl font-bold text-slate-900">{roleConfig.greeting}</h1>
            <p className="text-sm text-slate-500">{activeProject ? `${activeProject.title} · ${activeProject.status}` : t('assistant.no_project')}</p>
          </div>
        </div>
        <div className="hidden items-center gap-3 sm:flex">
          <NotificationsSummary />
          <StatLine items={roleConfig.statItems} />
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
        <div className="space-y-4">
          <AdvisorWidget onOpenConversation={() => navigate('/conversation')} />

          <div className="flex flex-wrap items-center gap-3">
            <PrimaryAction {...roleConfig.primaryAction} tooltip={roleConfig.primaryAction.label} />
            {roleConfig.secondActions.map((action) => (
              <button key={action.label} type="button" data-tooltip={action.label} onClick={() => navigate(action.to)}
                className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-medium text-slate-700 shadow-sm transition hover:border-slate-300 hover:shadow-md"
              >
                <span className="text-lg">{action.icon}</span>
                <span>{action.label}</span>
              </button>
            ))}
          </div>

          <Surface className="p-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">💬 {t('assistant.title')}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              <input
                className="min-w-0 flex-1 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm outline-none focus:border-slate-300"
                placeholder={`💬 ${t('assistant.chat_hint')}`}
                onKeyDown={(e) => { if (e.key === 'Enter' && (e.target as HTMLInputElement).value.trim()) navigate(smartSearch((e.target as HTMLInputElement).value)); }}
              />
              {suggestions.length > 0 ? suggestions.slice(0, 4).map((s) => (
                <button key={s.label} type="button" data-tooltip={s.label} onClick={() => navigate(s.to)}
                  className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600 transition hover:border-slate-300"
                >
                  <span>{s.icon}</span>
                  <span>{s.label}</span>
                </button>
              )) : null}
            </div>
          </Surface>

          {matches.length > 0 ? (
            <Surface className="p-4">
              <div className="flex items-center justify-between">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">✨ {t('dashboard.stats.opportunities')}</p>
                <button type="button" onClick={() => navigate('/search')} className="text-xs text-slate-400 hover:text-slate-700">{t('match.why_title')} →</button>
              </div>
              <div className="mt-3 grid gap-3 sm:grid-cols-2">
                {matches.slice(0, 2).map((match, index) => {
                  const title = match.property?.title || (match.partner && typeof match.partner === 'object' ? String((match.partner as Record<string, unknown>).display_name ?? '') : '') || `✨ ${index + 1}`;
                  const reasons = match.reasons.length > 0 ? match.reasons.map((r: string) => {
                    const parts = r.split(':');
                    if (parts.length === 2) return `${parts[0] === 'city' ? '📍' : parts[0] === 'budget' ? '💰' : parts[0] === 'property_type' ? '🏠' : '✓'} ${parts[1]}`;
                    return r;
                  }).join(' · ') : null;
                  return (
                    <button key={index} type="button" data-tooltip={reasons || ''} onClick={() => navigate('/search')}
                      className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 text-left transition hover:border-slate-300"
                    >
                      <span className="text-xl">{match.target_type === 'partner' ? '🤝' : role === 'investor' ? '💰' : '🏠'}</span>
                      <div className="min-w-0">
                        <p className="text-sm font-semibold text-slate-900">{title}</p>
                        {reasons ? <p className="truncate text-xs text-slate-500">{reasons}</p> : null}
                      </div>
                      <Badge variant={match.eligible ? 'success' : 'info'}>{match.eligible ? '✓' : '?'}</Badge>
                    </button>
                  );
                })}
              </div>
            </Surface>
          ) : role !== 'admin' && role !== 'manager' ? (
            <Surface className="p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">✨ {t('dashboard.stats.opportunities')}</p>
              <p className="mt-2 text-sm text-slate-500">{t('match.empty')}</p>
            </Surface>
          ) : null}

          {/* Brain proposals in cockpit */}
          {hasBrainMatches && activeProject && (
            <MatchSummaryWidget projectId={activeProject.id} />
          )}
        </div>

        <div className="space-y-4">
          <Surface className="p-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">📊 {t('dashboard.quick_stats')}</p>
            <div className="mt-3 space-y-2">
              {roleConfig.statItems.map((item) => (
                <div key={item.label} className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2 text-sm">
                  <span className="flex items-center gap-2 text-slate-600">
                    <span>{item.icon}</span>
                    <span>{item.label}</span>
                  </span>
                  <span className="font-semibold text-slate-900">{item.value}</span>
                </div>
              ))}
            </div>
          </Surface>

          {activeProject ? (
            <Surface className="p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">📁 {t('dashboard.project')}</p>
              <div className="mt-3 space-y-2">
                <div className="rounded-xl bg-slate-50 px-3 py-2 text-sm">
                  <p className="font-semibold text-slate-900">{activeProject.title}</p>
                  <p className="text-xs text-slate-500">{activeProject.status} · {activeProject.location_city || ''}</p>
                </div>
                <div className="flex gap-2">
                  <button type="button" onClick={() => navigate(`/dossier/${activeProject.id}`)}
                    className="flex-1 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-600 transition hover:border-slate-300"
                  >
                    📁 {t('dashboard.project')}
                  </button>
                  <button type="button" onClick={() => navigate(`/conversation?project=${activeProject.id}`)}
                    className="flex-1 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-600 transition hover:border-slate-300"
                  >
                    💬 {t('assistant.title')}
                  </button>
                </div>
              </div>
            </Surface>
          ) : null}

          <NotificationsSummary />
          <SecondaryActionsBlock role={role} />
        </div>
      </div>
    </CockpitFrame>
  );
}

export function CockpitEntryPage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const resolvedRole = resolvePrimaryRole(user?.role, roles);
  return <Navigate to={resolveDashboardPath(resolvedRole)} replace />;
}

function NotificationsSummary() {
  const { t } = useTranslator();
  const { data } = useQuery({
    queryKey: ['notifications-summary'],
    queryFn: () => apiSdk.getNotifications()
  });
  const items = (data?.data ?? []) as unknown as Array<Record<string, unknown>>;
  const unread = items.filter((n) => !n.read).length;
  const today = items.filter((n) => {
    const d = new Date(String(n.created_at ?? ''));
    const now = new Date();
    return d.toDateString() === now.toDateString();
  });

  if (items.length === 0) return null;

  return (
    <Surface className="p-3" data-tooltip={unread > 0 ? `${unread} non lu${unread > 1 ? 's' : ''}` : t('nav.notifications')}>
      <div className="flex items-center gap-3 text-sm">
        <span className="text-lg">{unread > 0 ? '🔔' : '🔕'}</span>
        <span className="text-slate-600">{t('nav.notifications')}</span>
        {unread > 0 ? <span className="ml-auto rounded-full bg-rose-500 px-2 py-0.5 text-xs font-bold text-white">{unread}</span> : null}
        {today.length > 0 ? <span className="ml-2 text-xs text-slate-400">📅 {today.length} aujourd'hui</span> : null}
      </div>
    </Surface>
  );
}

function ConseillerMessage({ firstName, projectTheme, pendingTasks }: { firstName: string; projectTheme: string; pendingTasks: number }) {
  const { t } = useTranslator();

  const messages: Record<string, string[]> = {
    construction: [
      `🏗️ ${firstName}, votre projet de construction avance bien.`,
      `📐 Pensez à contacter un architecte pour les plans.`,
    ],
    terrain: [
      `🌍 ${firstName}, la recherche de terrain progresse.`,
      `📋 Vérifions le titre foncier ensemble.`,
    ],
    location: [
      `🔑 ${firstName}, trouvons le bon logement à louer.`,
      `🏠 J'ai des suggestions adaptées à votre budget.`,
    ],
    investissement: [
      `💰 ${firstName}, les opportunités d'investissement sont prometteuses.`,
      `📈 Étudions ensemble les meilleurs rendements.`,
    ],
    achat: [
      `🏠 ${firstName}, votre projet d'achat est bien engagé.`,
      `🤝 Un notaire pourra vous accompagner.`,
    ],
  };

  const themeMessages = messages[projectTheme] ?? [`👋 ${firstName}, votre projet avance.`];
  const msg = pendingTasks > 0
    ? `${themeMessages[0]} ⚠️ ${pendingTasks} point${pendingTasks > 1 ? 's' : ''} mérite${pendingTasks > 1 ? 'nt' : ''} votre attention.`
    : themeMessages[0];

  return (
    <Surface className="p-4">
      <div className="flex items-start gap-3">
        <span className="text-2xl">🤖</span>
        <div>
          <p className="text-sm font-semibold text-slate-900">{t('cockpit.iai')}</p>
          <p className="mt-1 text-sm text-slate-600">{msg}</p>
        </div>
      </div>
    </Surface>
  );
}

export function RoleCockpitPage() {
  const params = useParams();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const canonicalRole = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const { projects, projectsPending, summary, summaryPending } = useProjectsSummary();

  useEffect(() => {
    const routeRole = params.role as string | undefined;
    if (routeRole && routeRole !== canonicalRole) {
      navigate(resolveDashboardPath(canonicalRole), { replace: true });
    }
  }, [canonicalRole, navigate, params.role]);

  if (projectsPending || summaryPending) return <CockpitLoading />;

  return <RoleCockpitBody role={canonicalRole} projects={projects} summary={summary} />;
}

export function ConversationStudioPage() {
  const { t } = useTranslator();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));

  return (
    <CockpitFrame title={`💬 ${t('assistant.title')}`}>
      <div className="mx-auto max-w-4xl">
        <Surface className="overflow-hidden">
          <AdvisorPanel
            userName={(user as unknown as Record<string, string | undefined>)?.full_name || (user as unknown as Record<string, string | undefined>)?.username || user?.email || ''}
            roleLabel={t(ROLE_LABEL_BY_MISSION_ROLE[role])}
          />
        </Surface>
      </div>
    </CockpitFrame>
  );
}

export function ProjectDossierPage() {
  const { t } = useTranslator();
  const params = useParams();
  const { projects } = useProjectsSummary();

  return (
    <CockpitFrame title={`📁 ${t('dashboard.project')}`}>
      <Surface className="p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{t('dossier.summary')}</p>
        <div className="mt-3 space-y-3">
          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl bg-slate-50 px-4 py-3">
              <p className="text-xs text-slate-500">{t('module.properties.status')}</p>
              <p className="text-lg font-bold text-slate-900">{projects[0]?.status || t('assistant.no_project')}</p>
            </div>
            <div className="rounded-xl bg-slate-50 px-4 py-3">
              <p className="text-xs text-slate-500">{t('module.properties.budget')}</p>
              <p className="text-lg font-bold text-slate-900">{projects[0]?.budget_max ? formatPropertyPrice(projects[0].budget_max) : '—'}</p>
            </div>
            <div className="rounded-xl bg-slate-50 px-4 py-3">
              <p className="text-xs text-slate-500">{t('module.properties.city')}</p>
              <p className="text-lg font-bold text-slate-900">{projects[0]?.location_city || '—'}</p>
            </div>
          </div>
          <div className="space-y-2">
            {['💬 ' + t('dossier.last_conversation'), '✅ ' + t('dossier.last_decision'), '➡️ ' + t('dossier.next_action')].map((label, i) => (
              <div key={i} className="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3 text-sm">
                <span>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </Surface>
    </CockpitFrame>
  );
}

export function PropertyJourneyPage() {
  const { t, language } = useTranslator();

  return (
    <CockpitFrame title={`🔎 ${t('module.properties.title')}`}>
      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <Surface className="p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">💬 {t('cockpit.new_project')}</p>
          <div className="mt-3 space-y-3">
            <Select tone="light" label={t('module.properties.category')} value="acheter" onChange={() => {}}>
              <option value="acheter">{t('cockpit.new_project')}</option>
              <option value="louer">{t('nav.estimation')}</option>
              <option value="construire">{t('module.properties.subtype')}</option>
              <option value="investir">{t('assistant.prompt_banque')}</option>
            </Select>
            <Select tone="light" label={t('module.properties.subtype')} value="maison" onChange={() => {}}>
              <option value="maison">{t('module.properties.category.logement')}</option>
              <option value="terrain">{t('module.properties.category.terrain')}</option>
              <option value="appartement">{t('module.properties.lodging.apartment')}</option>
              <option value="immeuble">{t('module.properties.category.immeuble')}</option>
            </Select>
            <div className="grid gap-3 sm:grid-cols-2">
              <Select tone="light" label={t('module.properties.city')} value="Douala" onChange={() => {}}>
                <option>Douala</option>
                <option>Yaoundé</option>
                <option>Bafoussam</option>
              </Select>
              <Input tone="light" label={t('module.properties.budget')} placeholder="50 000 000" />
            </div>
            <Button type="button" className="w-full justify-center">
              🔎 {t('module.properties.match_button')}
            </Button>
          </div>
        </Surface>

        <Surface className="p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">✨ {t('match.why_title')}</p>
          <div className="mt-3 space-y-3">
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🏠</span>
                <div>
                  <p className="font-semibold text-slate-900">{t('module.properties.category.logement')} · Douala</p>
                  <p className="text-sm text-slate-500">50 000 000 FCFA</p>
                </div>
              </div>
              <div className="mt-2 flex flex-wrap gap-2">
                <Badge variant="info">📍 Douala</Badge>
                <Badge variant="info">💰 50M</Badge>
                <Badge variant="info">🏠 4 chambres</Badge>
              </div>
            </div>
          </div>
        </Surface>
      </div>
    </CockpitFrame>
  );
}

export function PartnerJourneyPage() {
  const { t } = useTranslator();

  return (
    <CockpitFrame title={`🤝 ${t('module.partners.title')}`}>
      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <Surface className="p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">💬 {t('module.partners.form_title')}</p>
          <div className="mt-3 space-y-3">
            <Select tone="light" label={t('module.partners.need')} value="architecte" onChange={() => {}}>
              <option value="architecte">{t('module.partners.need.architect')}</option>
              <option value="banque">{t('module.partners.need.bank')}</option>
              <option value="notaire">{t('module.partners.need.notary')}</option>
              <option value="photographe">{t('module.partners.need.photographer')}</option>
            </Select>
            <Input tone="light" label={t('module.properties.city')} placeholder="Douala" />
            <Button type="button" className="w-full justify-center">
              🤝 {t('module.partners.find')}
            </Button>
          </div>
        </Surface>

        <Surface className="p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">✨ {t('module.partners.results_title')}</p>
          <div className="mt-3 space-y-3">
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📐</span>
                <div>
                  <p className="font-semibold text-slate-900">{t('module.partners.need.architect')}</p>
                  <p className="text-sm text-slate-500">📍 Douala</p>
                </div>
              </div>
              <Badge variant="success">{t('partner.available')}</Badge>
            </div>
          </div>
        </Surface>
      </div>
    </CockpitFrame>
  );
}

export function HistoryPage() {
  const { t } = useTranslator();

  return (
    <CockpitFrame title={`📅 ${t('assistant.project_hint')}`}>
      <Surface className="p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{t('dossier.timeline')}</p>
        <div className="mt-3 space-y-3">
          <div className="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3 text-sm">
            <span>💬</span>
            <span className="text-slate-700">{t('dossier.last_conversation')}</span>
          </div>
          <div className="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3 text-sm">
            <span>✅</span>
            <span className="text-slate-700">{t('dossier.last_decision')}</span>
          </div>
          <div className="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3 text-sm">
            <span>➡️</span>
            <span className="text-slate-700">{t('dossier.next_action')}</span>
          </div>
        </div>
      </Surface>
    </CockpitFrame>
  );
}

export function SearchSpacePage() {
  const { t } = useTranslator();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialQuery = params.get('q') ?? '';
  const [search, setSearch] = useState(initialQuery);
  const { data } = useQuery({
    queryKey: ['search-space', search],
    queryFn: () => apiSdk.getProperties({ search, page: 1, pageSize: 6 })
  });
  const items = data?.data ?? [];

  return (
    <CockpitFrame title={`🔎 ${t('cockpit.search')}`}>
      <Surface className="p-4">
        <div className="flex gap-3">
          <input
            className="min-w-0 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm outline-none focus:border-slate-300"
            placeholder={t('cockpit.search_placeholder')}
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            onKeyDown={(event) => { if (event.key === 'Enter') setSearch((event.target as HTMLInputElement).value); }}
          />
          <Button type="button" onClick={() => setSearch(search.trim())}>
            🔎 {t('module.properties.match_button')}
          </Button>
        </div>
        <div className="mt-4 space-y-2">
          {items.length > 0 ? items.map((item) => (
            <div key={item.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3">
              <div>
                <p className="font-semibold text-slate-900">{item.title}</p>
                <p className="text-sm text-slate-500">{item.location} · {item.type}</p>
              </div>
              <Badge variant="info">{item.type}</Badge>
            </div>
          )) : (
            <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-6 text-center text-sm text-slate-500">
              {t('module.properties.match_empty')}
            </div>
          )}
        </div>
      </Surface>
    </CockpitFrame>
  );
}

export function CockpitRedirectPage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  return <Navigate to={resolveDashboardPath(role)} replace />;
}
