import { useEffect, useMemo, useState } from 'react';
import { NavLink, Navigate, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { apiSdk, type CreatePropertyPayload, type MatchQuery, type MatchResult, type ProjectSummary, type PropertySummary } from '@api-sdk';
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
  LAWIM_OFFICIAL_CONTACT,
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

type DashboardPersona = 'admin' | 'manager' | 'agent' | 'owner' | 'investor' | 'partner' | 'user';

const CAMEROON_MAJOR_CITIES = [
  'Yaounde',
  'Douala',
  'Bamenda',
  'Bafoussam',
  'Buea',
  'Kribi',
  'Nkongsamba',
  'Maroua',
  'Limbe',
  'Garoua'
] as const;

const CAMEROON_REGIONS = ['Adamaoua', 'Centre', 'Est', 'Extrême-Nord', 'Littoral', 'Nord', 'Nord-Ouest', 'Ouest', 'Sud', 'Sud-Ouest'] as const;

const CAMEROON_DEPARTMENTS_BY_REGION: Record<(typeof CAMEROON_REGIONS)[number], readonly string[]> = {
  Adamaoua: ['Vina', 'Faro-et-Déo', 'Mayo-Banyo'],
  Centre: ['Mfoundi', 'Lekié', 'Mbam-et-Inoubou', 'Mbam-et-Kim', "Nyong-et-Kéllé", 'Nyong-et-Mfoumou', "Nyong-et-So'o", 'Haute-Sanaga'],
  Est: ['Lom-et-Djérem', 'Boumba-et-Ngoko', 'Haut-Nyong', 'Kadey'],
  'Extrême-Nord': ['Diamaré', 'Mayo-Danay', 'Mayo-Kani', 'Mayo-Sava', 'Logone-et-Chari'],
  Littoral: ['Wouri', 'Moungo', 'Nkam', 'Sanaga-Maritime'],
  Nord: ['Bénoué', 'Mayo-Rey', 'Mayo-Louti', 'Faro'],
  'Nord-Ouest': ['Mezam', 'Momo', 'Ngo-Ketunjia', 'Boyo', 'Bui', 'Donga-Mantung'],
  Ouest: ['Mifi', 'Menoua', 'Bamboutos', 'Nde', 'Haut-Nkam', 'Koung-Khi', 'Noun'],
  Sud: ['Océan', 'Mvila', 'Vallée-du-Ntem'],
  'Sud-Ouest': ['Fako', 'Meme', 'Manyu', 'Ndian']
};

const PROPERTY_CATEGORY_OPTIONS = [
  { value: 'terrain', label: 'Terrain', hint: 'Terrain à bâtir ou à lotir' },
  { value: 'logement', label: 'Logement', hint: 'Studio, appartement, maison ou villa' },
  { value: 'immeuble', label: 'Immeuble', hint: 'Immeuble résidentiel ou mixte' },
  { value: 'local_commercial', label: 'Local commercial', hint: 'Boutique, showroom ou commerce' },
  { value: 'bureau', label: 'Bureau', hint: 'Espace professionnel ou coworking' },
  { value: 'autre', label: 'Autre', hint: 'Bien atypique ou non classé' }
] as const;

const LOGEMENT_TYPE_OPTIONS = ['Studio', 'Appartement', 'Maison', 'Villa', 'Duplex', 'Chambre', 'Résidence meublée', 'Autre'] as const;

const PARTNER_NEED_OPTIONS = [
  'photographe',
  'architecte',
  'notaire',
  'banque',
  'artisan',
  'diagnostiqueur',
  'déménageur',
  'autre partenaire'
] as const;

const PROPERTY_FEATURE_PRESETS: Record<string, readonly string[]> = {
  terrain: ['superficie', 'titre foncier', 'lotissement', 'accès', 'eau', 'électricité', 'route', 'usage', 'quartier', 'prix'],
  logement: ['pièces', 'chambres', 'salles d’eau', 'salon', 'cuisine', 'parking', 'étage', 'standing', 'équipements', 'charges', 'prix'],
  immeuble: ['étages', 'lots', 'occupation', 'ascenseur', 'parking', 'surface', 'revenu', 'charges', 'sécurité', 'prix'],
  local_commercial: ['surface', 'vitrine', 'visibilité', 'accès', 'parking', 'stockage', 'flux', 'charges', 'usage', 'prix'],
  bureau: ['surface', 'open space', 'salles', 'internet', 'climatisation', 'parking', 'sécurité', 'étage', 'charges', 'prix'],
  autre: ['surface', 'usage', 'accès', 'quartier', 'prix', 'documents', 'observations']
};

const PROPERTY_CATEGORY_LABEL_KEY_BY_VALUE: Record<string, string> = {
  terrain: 'module.properties.category.terrain',
  logement: 'module.properties.category.logement',
  immeuble: 'module.properties.category.immeuble',
  local_commercial: 'module.properties.category.local_commercial',
  bureau: 'module.properties.category.bureau',
  autre: 'module.properties.category.autre'
};

const LOGEMENT_TYPE_LABEL_KEY_BY_VALUE: Record<string, string> = {
  Studio: 'module.properties.lodging.studio',
  Appartement: 'module.properties.lodging.apartment',
  Maison: 'module.properties.lodging.house',
  Villa: 'module.properties.lodging.villa',
  Duplex: 'module.properties.lodging.duplex',
  Chambre: 'module.properties.lodging.room',
  'Résidence meublée': 'module.properties.lodging.furnished_residence',
  Autre: 'module.properties.lodging.other'
};

const PARTNER_NEED_LABEL_KEY_BY_VALUE: Record<string, string> = {
  photographe: 'module.partners.need.photographer',
  architecte: 'module.partners.need.architect',
  notaire: 'module.partners.need.notary',
  banque: 'module.partners.need.bank',
  artisan: 'module.partners.need.artisan',
  diagnostiqueur: 'module.partners.need.diagnostician',
  'déménageur': 'module.partners.need.mover',
  'autre partenaire': 'module.partners.need.other_partner'
};

const CAMEROON_CITY_REGION_MAP: Record<string, string> = {
  Yaounde: 'Centre',
  Douala: 'Littoral',
  Bamenda: 'Nord-Ouest',
  Bafoussam: 'Ouest',
  Buea: 'Sud-Ouest',
  Kribi: 'Sud',
  Nkongsamba: 'Littoral',
  Maroua: 'Extrême-Nord',
  Limbe: 'Sud-Ouest',
  Garoua: 'Nord'
};

const PROPERTY_TYPE_BY_CATEGORY: Record<string, string> = {
  terrain: 'land',
  logement: 'house',
  immeuble: 'building',
  local_commercial: 'retail',
  bureau: 'office',
  autre: 'residence'
};

const LOGEMENT_TYPE_TO_PROPERTY_TYPE: Record<string, string> = {
  Studio: 'apartment',
  Appartement: 'apartment',
  Maison: 'house',
  Villa: 'house',
  Duplex: 'house',
  Chambre: 'residence',
  'Résidence meublée': 'residence',
  Autre: 'residence'
};

const dashboardModuleOrderByPersona: Record<DashboardPersona, readonly string[]> = {
  admin: ['admin', 'statistics', 'documents', 'partners', 'messages', 'properties', 'visits', 'contact'],
  manager: ['statistics', 'messages', 'visits', 'partners', 'documents', 'properties', 'contact'],
  agent: ['messages', 'visits', 'properties', 'partners', 'statistics', 'documents', 'contact'],
  owner: ['properties', 'messages', 'documents', 'partners', 'visits', 'statistics', 'contact'],
  investor: ['statistics', 'properties', 'partners', 'documents', 'messages', 'visits', 'contact'],
  partner: ['partners', 'messages', 'visits', 'statistics', 'documents', 'contact'],
  user: ['properties', 'messages', 'partners', 'documents', 'statistics', 'visits', 'contact']
};

function resolveDashboardPersona(user: { email?: string | null; username?: string | null } | null, role: AccessRole): DashboardPersona {
  const email = String(user?.email ?? '').toLowerCase();
  const username = String(user?.username ?? '').toLowerCase();
  if (email.includes('admin') || username === 'admin') return 'admin';
  if (email.includes('manager') || username === 'manager') return 'manager';
  if (email.includes('agent') || username === 'agent') return 'agent';
  if (email.includes('investor') || username === 'investor') return 'investor';
  if (email.includes('owner') || username === 'owner') return 'owner';
  if (role === 'partner') return 'partner';
  return 'user';
}

function resolveRoleLabelKey(persona: DashboardPersona) {
  switch (persona) {
    case 'admin':
      return 'role.admin';
    case 'manager':
      return 'role.manager';
    case 'agent':
      return 'role.agent';
    case 'owner':
      return 'role.owner';
    case 'investor':
      return 'role.investor';
    case 'partner':
      return 'role.partner';
    default:
      return 'role.user';
  }
}

function resolveDashboardModuleOrder(persona: DashboardPersona) {
  return dashboardModuleOrderByPersona[persona];
}

function resolveDepartmentOptions(region: string) {
  return CAMEROON_DEPARTMENTS_BY_REGION[region as keyof typeof CAMEROON_DEPARTMENTS_BY_REGION] ?? [];
}

function buildPropertyTitle(category: string, city: string, subtype?: string) {
  const parts = [category === 'logement' && subtype ? subtype : titleCase(category.replace('_', ' ')), city].filter(Boolean);
  return parts.join(' - ');
}

function resolvePropertyType(category: string, lodgingSubtype?: string) {
  if (category === 'logement') {
    return LOGEMENT_TYPE_TO_PROPERTY_TYPE[lodgingSubtype || ''] ?? 'apartment';
  }
  return PROPERTY_TYPE_BY_CATEGORY[category] ?? 'residence';
}

function resolveMajorCityRegion(city: string) {
  return CAMEROON_CITY_REGION_MAP[city] ?? '';
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
      description={t('dashboard.subtitle')}
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
        <Card title={t('dashboard.whats_next')} description={t('dashboard.subtitle')}>
          <div className="space-y-3 text-sm text-slate-300">
            <p>• {t('auth.login.email')} + {t('auth.login.password')}.</p>
            <p>• {t('dashboard.return_dashboard')}.</p>
            <p>• {t('auth.login.banner.invalid')}</p>
            <p>• {t('auth.login.banner.server_unavailable')}</p>
          </div>
        <div className="mt-5 rounded-2xl border border-brand-500/20 bg-brand-500/10 p-4 text-sm text-brand-100">
          {isAuthenticated
            ? t('dashboard.greeting', { name: user?.name || user?.email || t('shared.user') })
            : t('dashboard.subtitle')}
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

type AssistantConversationMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  details?: string[];
};

function AssistantConversationPanel({ compact = false }: { compact?: boolean }) {
  const { t, language } = useTranslator();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<AssistantConversationMessage[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | ''>('');
  const [sessionId, setSessionId] = useState<number | undefined>(undefined);
  const [assistantKey, setAssistantKey] = useState<string | undefined>(undefined);
  const [assistantError, setAssistantError] = useState<string | null>(null);
  const [assistantReply, setAssistantReply] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);

  const {
    data: projectsData,
    isPending: isProjectsPending,
    error: projectsError,
    refetch: refetchProjects
  } = useQuery({ queryKey: ['assistant-projects'], queryFn: () => apiSdk.getProjects() });
  const {
    data: promptData,
    isPending: isPromptPending,
    error: promptError,
    refetch: refetchPrompts
  } = useQuery({ queryKey: ['assistant-prompts'], queryFn: () => apiSdk.getAssistantSuggestions() });

  const projects = useMemo(() => projectsData?.data ?? [], [projectsData]);
  const suggestedPrompts = useMemo(() => promptData?.data ?? [], [promptData]);
  const selectedProject = projects.find((project) => project.id === selectedProjectId) ?? projects[0] ?? null;

  useEffect(() => {
    if (selectedProjectId === '' && projects.length > 0) {
      setSelectedProjectId(projects[0].id);
    }
  }, [projects, selectedProjectId]);

  useEffect(() => {
    if (selectedProject && selectedProjectId !== selectedProject.id) {
      setSelectedProjectId(selectedProject.id);
    }
  }, [selectedProject, selectedProjectId]);

  const quickPrompts = useMemo(
    () => [
      t('assistant.prompt_terrain'),
      t('assistant.prompt_photographe'),
      t('assistant.prompt_architecte'),
      t('assistant.prompt_notaire'),
      t('assistant.prompt_banque')
    ],
    [language, t]
  );

  const sendMessage = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || typeof selectedProjectId !== 'number' || isSending) {
      return;
    }
    setIsSending(true);
    setAssistantError(null);
    try {
      setMessages((current) => [
        ...current,
        {
          id: `user-${Date.now()}`,
          role: 'user',
          text: trimmed
        }
      ]);
      const response = await apiSdk.askAssistant({
        message: trimmed,
        project_id: selectedProjectId,
        session_id: sessionId,
        agent_key: assistantKey
      });
      const reply = response.data.reply || t('assistant.empty');
      const suggestionList = response.data.suggestions.length > 0 ? response.data.suggestions : [t('assistant.follow_up')];
      setAssistantReply(reply);
      setSessionId(response.data.session_id ?? sessionId);
      setAssistantKey(response.data.agent_key ?? assistantKey);
      setMessages((current) => [
        ...current,
        {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          text: reply,
          details: suggestionList
        }
      ]);
      setMessage('');
    } catch (error) {
      const errorText = error instanceof Error ? error.message : t('errors.generic');
      setAssistantError(errorText);
    } finally {
      setIsSending(false);
    }
  };

  const selectedProjectLabel =
    selectedProject == null
      ? t('assistant.no_project')
      : `${selectedProject.title}${selectedProject.location_city ? ` · ${selectedProject.location_city}` : ''}`;

  const lastMessage = messages[messages.length - 1];
  const visibleMessages = compact ? messages.slice(-3) : messages;

  return (
    <div className={`grid gap-6 ${compact ? 'xl:grid-cols-[0.95fr_1.05fr]' : 'lg:grid-cols-[0.85fr_1.15fr]'}`.trim()}>
      <Card title={t('assistant.projects')} description={t('assistant.project_hint')}>
        {isProjectsPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : projectsError ? (
          <ErrorState message={projectsError instanceof Error ? projectsError.message : t('errors.generic')} retry={() => void refetchProjects()} />
        ) : projects.length === 0 ? (
          <EmptyState label={t('assistant.no_project')} />
        ) : (
          <div className="space-y-4">
            <Select
              label={t('assistant.choose_project')}
              value={selectedProjectId === '' ? '' : String(selectedProjectId)}
              onChange={(event) => {
                const nextValue = Number(event.target.value);
                setSelectedProjectId(Number.isFinite(nextValue) ? nextValue : '');
              }}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.title}
                </option>
              ))}
            </Select>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('assistant.context')}</p>
              <p className="mt-2 text-white">{selectedProjectLabel}</p>
              {selectedProject?.objective ? <p className="mt-2 leading-6 text-slate-300">{selectedProject.objective}</p> : null}
              <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-400">
                {selectedProject?.budget_min != null || selectedProject?.budget_max != null ? (
                  <Badge variant="info">
                    {selectedProject.budget_min != null ? `${selectedProject.budget_min.toLocaleString()} ` : ''}
                    {selectedProject.budget_max != null ? `- ${selectedProject.budget_max.toLocaleString()}` : ''}
                  </Badge>
                ) : null}
                {selectedProject?.project_type ? <Badge variant="success">{selectedProject.project_type}</Badge> : null}
                {selectedProject?.status ? <Badge variant="warning">{selectedProject.status}</Badge> : null}
              </div>
            </div>
            <div className="grid gap-2">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('assistant.quick_prompts')}</p>
              <div className="flex flex-wrap gap-2">
                {quickPrompts.map((prompt) => (
                  <Button key={prompt} type="button" variant="secondary" onClick={() => setMessage(prompt)}>
                    {prompt}
                  </Button>
                ))}
              </div>
            </div>
            <div className="grid gap-2">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('assistant.quick_prompts')}</p>
              <div className="space-y-2">
                {isPromptPending ? (
                  <LoadingState label={t('auth.session.restoring')} />
                ) : promptError ? (
                  <ErrorState message={promptError instanceof Error ? promptError.message : t('errors.generic')} retry={() => void refetchPrompts()} />
                ) : (
                  suggestedPrompts.slice(0, compact ? 2 : 4).map((item) => (
                    <button
                      key={`${item.title}-${item.description}`}
                      type="button"
                      className="w-full rounded-2xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-left transition hover:border-brand-500/30 hover:bg-slate-900/90"
                      onClick={() => setMessage(item.description || item.title)}
                    >
                      <p className="text-sm font-semibold text-white">{item.title}</p>
                      <p className="mt-1 text-xs leading-5 text-slate-400">{item.description}</p>
                    </button>
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </Card>

      <Card title={t('assistant.title')} description={t('assistant.description')}>
        <div className="space-y-4">
          <Textarea
            label={t('assistant.message_label')}
            placeholder={t('assistant.chat_hint')}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />
          <div className="flex flex-wrap gap-3">
            <Button type="button" onClick={() => void sendMessage(message)} loading={isSending}>
              {t('assistant.send')}
            </Button>
            <Button type="button" variant="secondary" onClick={() => setMessage('')}>
              {t('assistant.clear')}
            </Button>
          </div>

          {assistantError ? <p className="text-sm text-rose-300">{assistantError}</p> : null}

          <div className="space-y-3 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('assistant.reply')}</p>
            {visibleMessages.length === 0 ? (
              <p className="text-sm leading-6 text-slate-300">{t('assistant.empty')}</p>
            ) : (
              <div className="space-y-3">
                {visibleMessages.map((item) => (
                  <div
                    key={item.id}
                    className={`rounded-2xl border px-4 py-3 text-sm leading-6 ${
                      item.role === 'user'
                        ? 'border-brand-500/20 bg-brand-500/10 text-brand-50'
                        : 'border-emerald-500/20 bg-emerald-500/10 text-emerald-100'
                    }`}
                  >
                    <p className="text-[11px] uppercase tracking-[0.24em] text-slate-400">{item.role === 'user' ? t('shared.user') : t('assistant.reply')}</p>
                    <p className="mt-2">{item.text}</p>
                    {item.details && item.details.length > 0 ? (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {item.details.map((detail) => (
                          <Badge key={detail} variant={item.role === 'user' ? 'info' : 'success'}>
                            {detail}
                          </Badge>
                        ))}
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            )}
          </div>

          {lastMessage?.role === 'assistant' && assistantReply ? (
            <div className="rounded-2xl border border-brand-500/20 bg-brand-500/10 p-4 text-sm text-brand-50">
              <p className="text-xs uppercase tracking-[0.28em] text-brand-200">{t('assistant.context')}</p>
              <p className="mt-2 leading-6">{assistantReply}</p>
            </div>
          ) : null}
        </div>
      </Card>
    </div>
  );
}

function AssistantPage() {
  const { t } = useTranslator();
  return (
    <PageShell eyebrow={t('nav.assistant')} title={t('assistant.title')} description={t('assistant.description')}>
      <AssistantConversationPanel />
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
  const persona = resolveDashboardPersona(user, role);
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
  const orderedModules = dashboardModuleDefinitions
    .filter((module) => module.key !== 'admin' || persona === 'admin')
    .slice()
    .sort((left, right) => resolveDashboardModuleOrder(persona).indexOf(left.key) - resolveDashboardModuleOrder(persona).indexOf(right.key));
  const userName = user?.name || user?.email?.split('@')[0] || t('shared.user');
  const roleLabel = t(resolveRoleLabelKey(persona));
  const progressPercent = Math.min(100, Math.round(Math.max(14, summary.properties * 4 + summary.opportunities * 3 + summary.communications * 2 + summary.pendingTasks)));
  const personaCopy = {
    admin: {
      subtitle: t('dashboard.persona.admin.subtitle'),
      prompt: t('dashboard.persona.admin.prompt'),
      primary: t('dashboard.persona.admin.primary'),
      secondary: t('dashboard.persona.admin.secondary')
    },
    manager: {
      subtitle: t('dashboard.persona.manager.subtitle'),
      prompt: t('dashboard.persona.manager.prompt'),
      primary: t('dashboard.persona.manager.primary'),
      secondary: t('dashboard.persona.manager.secondary')
    },
    agent: {
      subtitle: t('dashboard.persona.agent.subtitle'),
      prompt: t('dashboard.persona.agent.prompt'),
      primary: t('dashboard.persona.agent.primary'),
      secondary: t('dashboard.persona.agent.secondary')
    },
    owner: {
      subtitle: t('dashboard.persona.owner.subtitle'),
      prompt: t('dashboard.persona.owner.prompt'),
      primary: t('dashboard.persona.owner.primary'),
      secondary: t('dashboard.persona.owner.secondary')
    },
    investor: {
      subtitle: t('dashboard.persona.investor.subtitle'),
      prompt: t('dashboard.persona.investor.prompt'),
      primary: t('dashboard.persona.investor.primary'),
      secondary: t('dashboard.persona.investor.secondary')
    },
    partner: {
      subtitle: t('dashboard.persona.partner.subtitle'),
      prompt: t('dashboard.persona.partner.prompt'),
      primary: t('dashboard.persona.partner.primary'),
      secondary: t('dashboard.persona.partner.secondary')
    },
    user: {
      subtitle: t('dashboard.persona.user.subtitle'),
      prompt: t('dashboard.persona.user.prompt'),
      primary: t('dashboard.persona.user.primary'),
      secondary: t('dashboard.persona.user.secondary')
    }
  }[persona];

  const activityItems = [
    { label: t('dashboard.stats.properties'), value: summary.properties },
    { label: t('dashboard.stats.opportunities'), value: summary.opportunities },
    { label: t('dashboard.stats.messages'), value: summary.communications },
    { label: t('dashboard.stats.tasks'), value: summary.pendingTasks }
  ];

  useEffect(() => {
    traceAuth('DASHBOARD_RENDERED', {
      role,
      persona,
      path: resolveDashboardPath(role),
      email: user?.email ?? null
    });
  }, [persona, role, user?.email]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(14,165,233,0.18),_rgba(2,6,23,0.98)_34%,_rgba(15,23,42,0.96)_100%)] px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <section className="rounded-[2rem] border border-white/10 bg-slate-950/85 p-6 shadow-[0_30px_120px_rgba(2,6,23,0.45)] backdrop-blur">
          <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
            <div className="space-y-4">
              <div className="flex flex-wrap items-center gap-3">
                <Badge variant="info">{t('dashboard.cockpit')}</Badge>
                <Badge variant="success">{roleLabel}</Badge>
              </div>
              <div className="space-y-2">
                <p className="text-xs font-semibold uppercase tracking-[0.32em] text-slate-400">{t('dashboard.today')}</p>
                <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">{t('dashboard.greeting', { name: userName })}</h1>
                <p className="max-w-2xl text-base leading-7 text-slate-300">{personaCopy.subtitle}</p>
              </div>
              <div className="flex flex-wrap gap-3">
                <Button type="button" onClick={() => navigate('/assistant')}>
                  {t('dashboard.open_assistant')}
                </Button>
                <Button type="button" variant="secondary" onClick={() => navigate('/contact')}>
                  {t('module.contact.title')}
                </Button>
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {activityItems.map((item) => (
                <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <p className="text-[11px] uppercase tracking-[0.3em] text-slate-500">{item.label}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">{item.value}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-6 grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
            <div className="rounded-[1.5rem] border border-slate-800 bg-slate-950/60 p-5">
              <div className="flex items-center justify-between gap-3 text-sm">
                <span className="text-slate-300">{t('dashboard.progress')}</span>
                <span className="font-semibold text-white">{progressPercent}%</span>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
                <div className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-sky-400 to-emerald-400" style={{ width: `${progressPercent}%` }} />
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-300">{t('dashboard.whats_next')} {personaCopy.prompt}</p>
            </div>
            <div className="rounded-[1.5rem] border border-slate-800 bg-slate-950/60 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-500">{t('dashboard.quick_actions')}</p>
              <div className="mt-3 space-y-2 text-sm text-slate-300">
                <p>{t('dashboard.stats.properties')}: {summary.properties}</p>
                <p>{t('dashboard.stats.opportunities')}: {summary.opportunities}</p>
                <p>{t('dashboard.stats.messages')}: {summary.communications}</p>
              </div>
              <div className="mt-4 flex flex-wrap gap-3">
                <Button type="button" onClick={() => navigate(`/dashboard/modules/${orderedModules[0]?.key ?? 'properties'}`)}>
                  {personaCopy.primary}
                </Button>
                <Button type="button" variant="secondary" onClick={() => navigate(`/dashboard/modules/${orderedModules[1]?.key ?? 'messages'}`)}>
                  {personaCopy.secondary}
                </Button>
              </div>
            </div>
          </div>
        </section>

        <div className="grid gap-6 xl:grid-cols-[1fr_0.92fr]">
          <Card title={t('dashboard.activity_today')} description={t('dashboard.subtitle')}>
            {isPending ? (
              <LoadingState label={t('auth.session.restoring')} />
            ) : error ? (
              <ErrorState message={error instanceof Error ? error.message : t('errors.generic')} retry={() => void refetch()} />
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                {activityItems.map((item) => (
                  <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-200">
                    <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{item.label}</p>
                    <p className="mt-2 text-2xl font-semibold text-white">{item.value}</p>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card title={t('dashboard.priorities')} description={personaCopy.prompt}>
            <div className="space-y-3 text-sm text-slate-300">
              <p>{personaCopy.subtitle}</p>
              <p>{t('dashboard.identity', { role: roleLabel })}</p>
            </div>
            <div className="mt-5 flex flex-wrap gap-3">
              <Button type="button" onClick={() => navigate(`/dashboard/modules/${orderedModules[0]?.key ?? 'properties'}`)}>
                {personaCopy.primary}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/assistant')}>
                {t('dashboard.open_assistant')}
              </Button>
            </div>
          </Card>
        </div>

        <Card title={t('dashboard.whats_next')} description={t('dashboard.quick_actions')}>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.action')}</p>
              <p className="mt-3">{personaCopy.prompt}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.next_step')}</p>
              <p className="mt-3">{t('dashboard.return_dashboard')}</p>
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
            {orderedModules.map((module) => (
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
  const shouldRestrictAdmin = moduleKey === 'admin' && role !== 'admin';

  if (!module) {
    return <Navigate to="/dashboard" replace />;
  }

  if (shouldRestrictAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  const moduleBody = (() => {
    switch (moduleKey) {
      case 'properties':
        return <PropertyWizardPanel />;
      case 'messages':
        return <AssistantConversationPanel compact />;
      case 'partners':
        return <PartnerMatchesPanel />;
      case 'statistics':
        return <StatisticsModulePanel />;
      case 'documents':
        return <DocumentsModulePanel />;
      case 'visits':
        return <VisitsModulePanel />;
      case 'contact':
        return <ContactModulePanel />;
      case 'admin':
        return <AdminModulePanel />;
      default:
        return <ModuleOverviewPanel title={t(module.titleKey)} description={t(module.descriptionKey)} />;
    }
  })();

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
      {moduleBody}
    </PageShell>
  );
}

type PropertyFormState = {
  cityMode: 'major' | 'other';
  majorCity: string;
  region: string;
  department: string;
  manualCity: string;
  category: string;
  lodgingSubtype: string;
  quartier: string;
  usage: string;
  standing: string;
  surface: string;
  bedrooms: string;
  bathrooms: string;
  priceMin: string;
  priceMax: string;
  notes: string;
  titleFoncier: boolean;
  lotissement: boolean;
  accessRoad: boolean;
  water: boolean;
  electricity: boolean;
  parking: boolean;
  status: string;
  availability: string;
};

function ModuleOverviewPanel({ title, description }: { title: string; description: string }) {
  const { t } = useTranslator();
  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
      <Card title={title} description={description}>
        <div className="space-y-3 text-sm leading-7 text-slate-300">
          <p>{description}</p>
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.action')}</p>
              <p className="mt-2 text-white">{t('dashboard.module_hint')}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.detail.next_step')}</p>
              <p className="mt-2 text-white">{t('shared.back_to_dashboard')}</p>
            </div>
          </div>
        </div>
      </Card>
      <Card title={t('dashboard.whats_next')} description={t('dashboard.quick_actions')}>
        <div className="space-y-3 text-sm text-slate-300">
          <p>{description}</p>
          <p>{t('module.detail.summary')}</p>
        </div>
      </Card>
    </div>
  );
}

function PropertyWizardPanel() {
  const { t, language } = useTranslator();
  const [form, setForm] = useState<PropertyFormState>(() => ({
    cityMode: 'major',
    majorCity: 'Yaounde',
    region: 'Centre',
    department: 'Mfoundi',
    manualCity: '',
    category: 'terrain',
    lodgingSubtype: 'Appartement',
    quartier: '',
    usage: 'residentiel',
    standing: 'standard',
    surface: '',
    bedrooms: '',
    bathrooms: '',
    priceMin: '',
    priceMax: '',
    notes: '',
    titleFoncier: true,
    lotissement: false,
    accessRoad: true,
    water: false,
    electricity: false,
    parking: false,
    status: 'draft',
    availability: 'available'
  }));
  const [savedProperty, setSavedProperty] = useState<PropertySummary | null>(null);
  const [matchRequest, setMatchRequest] = useState<MatchQuery | null>(null);
  const [banner, setBanner] = useState<{ tone: 'success' | 'error' | 'info'; text: string } | null>(null);

  const resolvedCity = form.cityMode === 'major' ? form.majorCity : form.manualCity.trim();
  const resolvedRegion = form.cityMode === 'major' ? resolveMajorCityRegion(form.majorCity) : form.region;
  const resolvedDepartment = form.cityMode === 'other' ? form.department : '';
  const lodgingSubtype = form.category === 'logement' ? form.lodgingSubtype : undefined;
  const propertyType = resolvePropertyType(form.category, lodgingSubtype);
  const featurePreview = PROPERTY_FEATURE_PRESETS[form.category] ?? PROPERTY_FEATURE_PRESETS.autre;
  const categoryOptions = PROPERTY_CATEGORY_OPTIONS.map((option) => ({
    ...option,
    label: t(PROPERTY_CATEGORY_LABEL_KEY_BY_VALUE[option.value] ?? 'module.properties.title')
  }));
  const lodgingTypeOptions = LOGEMENT_TYPE_OPTIONS.map((option) => ({
    value: option,
    label: t(LOGEMENT_TYPE_LABEL_KEY_BY_VALUE[option] ?? 'module.properties.subtype')
  }));
  const cityLabel = resolvedCity || t('module.properties.city');
  const selectedCategoryLabel = categoryOptions.find((option) => option.value === form.category)?.label ?? t('module.properties.title');
  const selectedLodgingLabel = lodgingTypeOptions.find((option) => option.value === form.lodgingSubtype)?.label;

  useEffect(() => {
    if (form.cityMode === 'major' && resolvedRegion && form.region !== resolvedRegion) {
      setForm((current) => ({ ...current, region: resolvedRegion }));
    }
  }, [form.cityMode, form.region, resolvedRegion]);

  useEffect(() => {
    if (form.cityMode === 'other' && form.region) {
      const validDepartments = resolveDepartmentOptions(form.region);
      if (form.department && !validDepartments.includes(form.department)) {
        setForm((current) => ({ ...current, department: '' }));
      }
    }
  }, [form.cityMode, form.department, form.region]);

  const propertyTitle = buildPropertyTitle(form.category, cityLabel, selectedLodgingLabel);
  const summary = form.notes.trim() || `${selectedCategoryLabel} ${resolvedCity ? `à ${resolvedCity}` : ''}`.trim();
  const priceMinValue = form.priceMin ? Number(form.priceMin) : null;
  const priceMaxValue = form.priceMax ? Number(form.priceMax) : null;
  const areaValue = form.surface ? Number(form.surface) : 0;
  const bedroomsValue = form.bedrooms ? Number(form.bedrooms) : 0;
  const bathroomsValue = form.bathrooms ? Number(form.bathrooms) : 0;

  const buildMatchRequest = (): MatchQuery => ({
    target_type: 'property',
    city: cityLabel,
    region: resolvedRegion || undefined,
    country: 'Cameroon',
    property_type: propertyType,
    budget_max: priceMaxValue ?? priceMinValue ?? undefined,
    availability: form.availability,
    limit: 4
  });

  const {
    data: matchResponse,
    isPending: matchPending,
    error: matchError,
    refetch: refetchMatches
  } = useQuery({
    queryKey: ['property-matches', matchRequest],
    enabled: Boolean(matchRequest),
    queryFn: async () => apiSdk.getMatches(matchRequest ?? undefined)
  });

  const matches = matchResponse?.data ?? [];

  const submitProperty = async () => {
    if (!resolvedCity) {
      setBanner({ tone: 'error', text: t('module.properties.city_required') });
      return;
    }
    setBanner(null);
    try {
      const payload: CreatePropertyPayload = {
        title: propertyTitle,
        summary,
        city: resolvedCity,
        country: 'Cameroon',
        region: resolvedRegion || undefined,
        address_line: form.quartier.trim() || undefined,
        price_min: priceMinValue,
        price_max: priceMaxValue,
        property_type: propertyType,
        availability: form.availability,
        status: form.status,
        bedrooms: bedroomsValue,
        bathrooms: bathroomsValue,
        area_sqm: areaValue,
        metadata: {
          category: form.category,
          lodgingSubtype,
          cityMode: form.cityMode,
          department: resolvedDepartment || undefined,
          usage: form.usage,
          standing: form.standing,
          titleFoncier: form.titleFoncier,
          lotissement: form.lotissement,
          accessRoad: form.accessRoad,
          water: form.water,
          electricity: form.electricity,
          parking: form.parking,
          notes: form.notes || undefined,
          language
        }
      };
      const response = await apiSdk.createProperty(payload);
      setSavedProperty(response.data);
      setBanner({ tone: 'success', text: t('module.properties.created_success') });
      setMatchRequest(buildMatchRequest());
    } catch (error) {
      setBanner({ tone: 'error', text: error instanceof Error ? error.message : t('errors.generic') });
    }
  };

  const launchMatchAnalysis = () => {
    if (!resolvedCity) {
      setBanner({ tone: 'error', text: t('module.properties.city_required') });
      return;
    }
    setBanner({ tone: 'info', text: t('module.properties.matching_launch') });
    setMatchRequest(buildMatchRequest());
  };

  return (
    <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
      <Card title={t('module.properties.form_title')} description={t('module.properties.form_hint')}>
        {banner ? (
          <div
            className={`mb-5 rounded-2xl border px-4 py-3 text-sm ${
              banner.tone === 'error'
                ? 'border-rose-200 bg-rose-50 text-rose-700'
                : banner.tone === 'success'
                  ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                  : 'border-brand-500/20 bg-brand-500/10 text-slate-700'
            }`}
          >
            {banner.text}
          </div>
        ) : null}

        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-[1.2fr_0.8fr]">
            <Select
              label={t('module.properties.location_mode')}
              value={form.cityMode}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  cityMode: event.target.value === 'other' ? 'other' : 'major'
                }))
              }
            >
              <option value="major">{t('module.properties.location_mode_major')}</option>
              <option value="other">{t('module.properties.location_mode_other')}</option>
            </Select>
            <Select
              label={t('module.properties.category')}
              value={form.category}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  category: event.target.value
                }))
              }
            >
              {categoryOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Select>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {form.cityMode === 'major' ? (
              <Select
                label={t('module.properties.city')}
                value={form.majorCity}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    majorCity: event.target.value
                  }))
                }
              >
                {CAMEROON_MAJOR_CITIES.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </Select>
            ) : (
              <Input
                label={t('module.properties.manual_city')}
                value={form.manualCity}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    manualCity: event.target.value
                  }))
                }
                placeholder="Bafia, Ebolowa, Kumba..."
              />
            )}
            {form.cityMode === 'other' ? (
              <Select
                label={t('module.properties.region')}
                value={form.region}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    region: event.target.value
                  }))
                }
              >
                {CAMEROON_REGIONS.map((region) => (
                  <option key={region} value={region}>
                    {region}
                  </option>
                ))}
              </Select>
            ) : (
              <div className="rounded-xl border border-slate-800 bg-slate-950/40 px-3 py-2 text-sm text-slate-300">
                <span className="block text-xs uppercase tracking-[0.28em] text-slate-500">{t('module.properties.region')}</span>
                <span className="mt-2 block text-white">{resolvedRegion || '—'}</span>
              </div>
            )}
          </div>

          {form.cityMode === 'other' ? (
            <Select
              label={t('module.properties.department')}
              value={form.department}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  department: event.target.value
                }))
              }
            >
              <option value="">{t('module.properties.department_placeholder')}</option>
              {resolveDepartmentOptions(form.region).map((department) => (
                <option key={department} value={department}>
                  {department}
                </option>
              ))}
            </Select>
          ) : null}

          <div className="grid gap-4 md:grid-cols-3">
            <Input
              label={t('module.properties.quartier')}
              value={form.quartier}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  quartier: event.target.value
                }))
              }
              placeholder="Bonanjo, Bastos, Molyko..."
            />
            <Select
              label={t('module.properties.subtype')}
              value={form.lodgingSubtype}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  lodgingSubtype: event.target.value
                }))
              }
              disabled={form.category !== 'logement'}
            >
              {lodgingTypeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Select>
            <Select
              label={t('module.properties.usage')}
              value={form.usage}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  usage: event.target.value
                }))
              }
            >
              <option value="residentiel">{t('module.properties.usage.residential')}</option>
              <option value="commercial">{t('module.properties.usage.commercial')}</option>
              <option value="mixte">{t('module.properties.usage.mixed')}</option>
              <option value="agricole">{t('module.properties.usage.agricultural')}</option>
              <option value="industriel">{t('module.properties.usage.industrial')}</option>
            </Select>
          </div>

          <div className="grid gap-4 md:grid-cols-4">
            <Input
              label={t('module.properties.surface')}
              value={form.surface}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  surface: event.target.value
                }))
              }
              placeholder="120"
            />
            <Input
              label={t('module.properties.price_min')}
              value={form.priceMin}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  priceMin: event.target.value
                }))
              }
              placeholder="25000000"
            />
            <Input
              label={t('module.properties.price_max')}
              value={form.priceMax}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  priceMax: event.target.value
                }))
              }
              placeholder="32000000"
            />
            <Select
              label={t('module.properties.standing')}
              value={form.standing}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  standing: event.target.value
                }))
              }
            >
              <option value="standard">{t('module.properties.standing.standard')}</option>
              <option value="moyen">{t('module.properties.standing.medium')}</option>
              <option value="bon">{t('module.properties.standing.good')}</option>
              <option value="haut">{t('module.properties.standing.premium')}</option>
            </Select>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <Input
              label={t('module.properties.bedrooms')}
              value={form.bedrooms}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  bedrooms: event.target.value
                }))
              }
              placeholder="3"
            />
            <Input
              label={t('module.properties.bathrooms')}
              value={form.bathrooms}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  bathrooms: event.target.value
                }))
              }
              placeholder="2"
            />
            <div className="grid gap-3 sm:grid-cols-2">
              <Checkbox
                label={t('module.properties.title_foncier')}
                checked={form.titleFoncier}
                onChange={(event) => setForm((current) => ({ ...current, titleFoncier: event.target.checked }))}
              />
              <Checkbox
                label={t('module.properties.lotissement')}
                checked={form.lotissement}
                onChange={(event) => setForm((current) => ({ ...current, lotissement: event.target.checked }))}
              />
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="grid gap-3 sm:grid-cols-2">
              <Checkbox
                label={t('module.properties.access')}
                checked={form.accessRoad}
                onChange={(event) => setForm((current) => ({ ...current, accessRoad: event.target.checked }))}
              />
              <Checkbox
                label={t('module.properties.water')}
                checked={form.water}
                onChange={(event) => setForm((current) => ({ ...current, water: event.target.checked }))}
              />
              <Checkbox
                label={t('module.properties.electricity')}
                checked={form.electricity}
                onChange={(event) => setForm((current) => ({ ...current, electricity: event.target.checked }))}
              />
              <Checkbox
                label={t('module.properties.parking')}
                checked={form.parking}
                onChange={(event) => setForm((current) => ({ ...current, parking: event.target.checked }))}
              />
            </div>
            <Textarea
              label={t('module.properties.notes')}
              value={form.notes}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  notes: event.target.value
                }))
              }
              placeholder={t('module.properties.notes_placeholder')}
            />
          </div>

          <div className="flex flex-wrap gap-3">
            <Button type="button" onClick={() => void submitProperty()}>
              {t('module.properties.create')}
            </Button>
            <Button type="button" variant="secondary" onClick={launchMatchAnalysis}>
              {t('module.properties.match_button')}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() =>
                setForm((current) => ({
                  ...current,
                  cityMode: 'major',
                  majorCity: 'Yaounde',
                  region: 'Centre',
                  department: 'Mfoundi',
                  manualCity: '',
                  category: 'terrain',
                  lodgingSubtype: 'Appartement',
                  quartier: '',
                  usage: 'residentiel',
                  standing: 'standard',
                  surface: '',
                  bedrooms: '',
                  bathrooms: '',
                  priceMin: '',
                  priceMax: '',
                  notes: '',
                  titleFoncier: true,
                  lotissement: false,
                  accessRoad: true,
                  water: false,
                  electricity: false,
                  parking: false,
                  status: 'draft',
                  availability: 'available'
                }))
              }
            >
              {t('module.properties.reset')}
            </Button>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            {featurePreview.map((feature) => (
              <Badge key={feature} variant="info">
                {feature}
              </Badge>
            ))}
          </div>
        </div>
      </Card>

      <div className="space-y-6">
        <Card title={t('dashboard.whats_next')} description={t('module.properties.ai_prompt')}>
          <div className="space-y-3 text-sm leading-6 text-slate-300">
            <p>{t('module.properties.guidance')}</p>
            <p>{propertyTitle}</p>
            <p>{summary}</p>
            {savedProperty ? (
              <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-emerald-100">
                <p className="text-xs uppercase tracking-[0.28em] text-emerald-300">{t('module.properties.saved')}</p>
                <p className="mt-2 font-semibold text-white">{savedProperty.title}</p>
                <p className="mt-1 text-sm text-emerald-100/80">{savedProperty.location}</p>
              </div>
            ) : null}
          </div>
        </Card>

        <Card title={t('module.properties.match_title')} description={t('module.properties.match_description')}>
          {matchPending ? (
            <LoadingState label={t('auth.session.restoring')} />
          ) : matchError ? (
            <ErrorState message={matchError instanceof Error ? matchError.message : t('errors.generic')} retry={() => void refetchMatches()} />
          ) : matches.length === 0 ? (
            <EmptyState label={t('module.properties.match_empty')} />
          ) : (
            <div className="space-y-3">
              {matches.map((match, index) => (
                <div key={`${String(match.property?.id ?? index)}`} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-white">{String(match.property?.title ?? `Property ${index + 1}`)}</p>
                      <p className="mt-1 text-xs uppercase tracking-[0.28em] text-slate-500">{String(match.property?.location ?? cityLabel)}</p>
                    </div>
                    <Badge variant="success">{Math.round(Number(match.score_percent ?? match.score ?? 0))}%</Badge>
                  </div>
                  <p className="mt-3 text-sm text-slate-300">{String(match.summary ?? '')}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {(match.reasons ?? []).map((reason) => (
                      <Badge key={reason} variant="info">
                        {reason}
                      </Badge>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

function PartnerMatchesPanel() {
  const { t, language } = useTranslator();
  const [need, setNeed] = useState('photographe');
  const [city, setCity] = useState('Douala');
  const [projectType, setProjectType] = useState('buy');
  const [budget, setBudget] = useState('');
  const [ratingMin, setRatingMin] = useState('0');
  const [deadlineDays, setDeadlineDays] = useState('');
  const [runQuery, setRunQuery] = useState(true);
  const needOptions = PARTNER_NEED_OPTIONS.map((option) => ({
    value: option,
    label: t(PARTNER_NEED_LABEL_KEY_BY_VALUE[option] ?? 'module.partners.partner')
  }));
  const formatNeedLabel = (value?: string | null) => (value ? t(PARTNER_NEED_LABEL_KEY_BY_VALUE[value] ?? value) : t('module.partners.partner'));
  const formatReason = (reason: string) => {
    if (reason.startsWith('partner_type:')) {
      return formatNeedLabel(reason.slice('partner_type:'.length));
    }
    if (reason.startsWith('city:')) {
      return `${t('module.partners.city')}: ${reason.slice('city:'.length)}`;
    }
    return reason;
  };

  const query = useMemo<MatchQuery>(
    () => ({
      target_type: 'partner',
      need,
      city,
      project_type: projectType,
      budget_max: budget ? Number(budget) : undefined,
      rating_min: ratingMin ? Number(ratingMin) : undefined,
      deadline_days: deadlineDays ? Number(deadlineDays) : undefined,
      language,
      limit: 5
    }),
    [budget, city, deadlineDays, language, need, projectType, ratingMin]
  );

  const {
    data: matchResponse,
    isPending: matchPending,
    error: matchError,
    refetch: refetchMatches
  } = useQuery({
    queryKey: ['partner-matches', query],
    enabled: runQuery,
    queryFn: async () => apiSdk.getMatches(query)
  });

  const matches = matchResponse?.data ?? [];

  const runAnalysis = () => {
    setRunQuery(true);
    void refetchMatches();
  };

  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
      <Card title={t('module.partners.form_title')} description={t('module.partners.form_description')}>
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {needOptions.map((option) => (
              <Button key={option.value} type="button" variant={need === option.value ? 'primary' : 'secondary'} onClick={() => setNeed(option.value)}>
                {option.label}
              </Button>
            ))}
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <Select label={t('module.partners.need')} value={need} onChange={(event) => setNeed(event.target.value)}>
              {needOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Select>
            <Select label={t('module.partners.city')} value={city} onChange={(event) => setCity(event.target.value)}>
              {CAMEROON_MAJOR_CITIES.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </Select>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <Select label={t('module.partners.project_type')} value={projectType} onChange={(event) => setProjectType(event.target.value)}>
              <option value="buy">{t('module.partners.project.buy')}</option>
              <option value="rent">{t('module.partners.project.rent')}</option>
              <option value="build">{t('module.partners.project.build')}</option>
              <option value="invest">{t('module.partners.project.invest')}</option>
              <option value="manage">{t('module.partners.project.manage')}</option>
            </Select>
            <Input
              label={t('module.partners.budget')}
              value={budget}
              onChange={(event) => setBudget(event.target.value)}
              placeholder="5000000"
            />
            <Select label={t('module.partners.rating_min')} value={ratingMin} onChange={(event) => setRatingMin(event.target.value)}>
              <option value="0">0</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="4.5">4.5</option>
            </Select>
          </div>
          <Input
            label={t('module.partners.deadline')}
            value={deadlineDays}
            onChange={(event) => setDeadlineDays(event.target.value)}
            placeholder="7"
          />
          <div className="flex flex-wrap gap-3">
            <Button type="button" onClick={runAnalysis}>
              {t('module.partners.find')}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setNeed('photographe');
                setCity('Douala');
                setProjectType('buy');
                setBudget('');
                setRatingMin('0');
                setDeadlineDays('');
              }}
            >
              {t('module.properties.reset')}
            </Button>
          </div>
        </div>
      </Card>

      <Card title={t('module.partners.results_title')} description={t('module.partners.results_description')}>
        {matchPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : matchError ? (
          <ErrorState message={matchError instanceof Error ? matchError.message : t('errors.generic')} retry={() => void refetchMatches()} />
        ) : matches.length === 0 ? (
          <EmptyState label={t('module.partners.no_match')} />
        ) : (
          <div className="space-y-3">
            {matches.map((match, index) => {
              const partner = match.partner ?? null;
              return (
                <div key={String(partner?.id ?? index)} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-white">{String(partner?.display_name ?? partner?.legal_name ?? partner?.partner_type ?? t('module.partners.partner'))}</p>
                      <p className="mt-1 text-xs uppercase tracking-[0.28em] text-slate-500">{formatNeedLabel(String(partner?.partner_type ?? ''))}</p>
                    </div>
                    <Badge variant="success">{Math.round(Number(match.score_percent ?? match.score ?? 0))}%</Badge>
                  </div>
                  <p className="mt-3 text-sm text-slate-300">{String(match.summary ?? '')}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {(match.reasons ?? []).map((reason) => (
                      <Badge key={reason} variant="info">
                        {formatReason(reason)}
                      </Badge>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </Card>
    </div>
  );
}

function StatisticsModulePanel() {
  const { t } = useTranslator();
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['module-statistics'], queryFn: () => apiSdk.getDashboardSummary() });
  const stats = data?.data ?? { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 };

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_0.85fr]">
      <Card title={t('module.statistics.title')} description={t('module.statistics.description')}>
        {isPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : error ? (
          <ErrorState message={error instanceof Error ? error.message : t('errors.generic')} retry={() => void refetch()} />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('dashboard.stats.properties')}</p>
              <p className="mt-2 text-3xl font-semibold text-white">{stats.properties}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('dashboard.stats.opportunities')}</p>
              <p className="mt-2 text-3xl font-semibold text-white">{stats.opportunities}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('dashboard.stats.messages')}</p>
              <p className="mt-2 text-3xl font-semibold text-white">{stats.communications}</p>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{t('dashboard.stats.tasks')}</p>
              <p className="mt-2 text-3xl font-semibold text-white">{stats.pendingTasks}</p>
            </div>
          </div>
        )}
      </Card>
      <Card title={t('module.statistics.actions_title')} description={t('module.statistics.actions_description')}>
        <div className="space-y-3 text-sm text-slate-300">
          <p>{t('dashboard.whats_next')}</p>
          <p>{t('module.statistics.actions_hint')}</p>
        </div>
      </Card>
    </div>
  );
}

function DocumentsModulePanel() {
  const { t } = useTranslator();
  const { data, isPending, error, refetch } = useQuery({ queryKey: ['module-documents'], queryFn: () => apiSdk.getDocuments() });
  const documents = data?.data ?? [];

  return (
    <div className="grid gap-6 xl:grid-cols-[0.92fr_1.08fr]">
      <Card title={t('module.documents.title')} description={t('module.documents.description')}>
        {isPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : error ? (
          <ErrorState message={error instanceof Error ? error.message : t('errors.generic')} retry={() => void refetch()} />
        ) : documents.length === 0 ? (
          <EmptyState label={t('module.documents.empty')} />
        ) : (
          <div className="space-y-3">
            {documents.map((item) => (
              <div key={item.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-sm font-semibold text-white">{item.title}</p>
                <p className="mt-1 text-xs uppercase tracking-[0.28em] text-slate-500">{item.kind}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
      <Card title={t('module.documents.actions_title')} description={t('module.documents.actions_description')}>
        <div className="space-y-3 text-sm text-slate-300">
          <p>{t('module.documents.actions_hint')}</p>
          <p>{t('shared.back_to_dashboard')}</p>
        </div>
      </Card>
    </div>
  );
}

function VisitsModulePanel() {
  const { t } = useTranslator();
  const { data: requests, isPending: requestsPending, error: requestsError, refetch: refetchRequests } = useQuery({
    queryKey: ['module-visits-requests'],
    queryFn: () => apiSdk.getRequests()
  });
  const { data: notifications, isPending: notificationsPending, error: notificationsError, refetch: refetchNotifications } = useQuery({
    queryKey: ['module-visits-notifications'],
    queryFn: () => apiSdk.getNotifications()
  });

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
      <Card title={t('module.visits.title')} description={t('module.visits.description')}>
        {requestsPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : requestsError ? (
          <ErrorState message={requestsError instanceof Error ? requestsError.message : t('errors.generic')} retry={() => void refetchRequests()} />
        ) : (requests?.data ?? []).length === 0 ? (
          <EmptyState label={t('module.visits.empty')} />
        ) : (
          <div className="space-y-3">
            {(requests?.data ?? []).map((item) => (
              <div key={item.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                <p className="text-sm font-semibold text-white">{item.title}</p>
                <p className="mt-1 text-xs uppercase tracking-[0.28em] text-slate-500">{item.status}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
      <Card title={t('module.visits.follow_up_title')} description={t('module.visits.follow_up_description')}>
        {notificationsPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : notificationsError ? (
          <ErrorState message={notificationsError instanceof Error ? notificationsError.message : t('errors.generic')} retry={() => void refetchNotifications()} />
        ) : (notifications?.data ?? []).length === 0 ? (
          <EmptyState label={t('module.visits.empty_follow_up')} />
        ) : (
          <div className="space-y-3">
            {(notifications?.data ?? []).map((item) => (
              <div key={item.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <p className="font-semibold text-white">{item.title}</p>
                <p className="mt-1 leading-6">{item.message}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}

function ContactModulePanel() {
  const { t } = useTranslator();
  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
      <Card title={t('contact.title')} description={t('contact.description')}>
        <OfficialContactGrid tone="dark" />
      </Card>
      <Card title={t('contact.title')} description={t('contact.description')}>
        <div className="grid gap-4">
          <Input label={t('contact.name')} placeholder="Jane Doe" />
          <Input label={t('contact.email')} placeholder="name@example.com" />
          <Textarea label={t('contact.message')} placeholder={t('contact.placeholder')} />
          <Button type="button">{t('contact.send')}</Button>
        </div>
      </Card>
    </div>
  );
}

function AdminModulePanel() {
  const { t } = useTranslator();
  const { data: security, isPending: securityPending, error: securityError, refetch: refetchSecurity } = useQuery({
    queryKey: ['module-admin-security'],
    queryFn: () => apiSdk.getSecuritySummary()
  });
  const { data: deployment, isPending: deploymentPending, error: deploymentError, refetch: refetchDeployment } = useQuery({
    queryKey: ['module-admin-deployment'],
    queryFn: () => apiSdk.getDeploymentStatus()
  });
  const { data: backup, isPending: backupPending, error: backupError, refetch: refetchBackup } = useQuery({
    queryKey: ['module-admin-backup'],
    queryFn: () => apiSdk.getBackupStatus()
  });

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
      <Card title={t('module.admin.title')} description={t('module.admin.description')}>
        {securityPending ? (
          <LoadingState label={t('auth.session.restoring')} />
        ) : securityError ? (
          <ErrorState message={securityError instanceof Error ? securityError.message : t('errors.generic')} retry={() => void refetchSecurity()} />
        ) : (
          <div className="space-y-3">
            {(security?.data ?? []).map((item) => (
              <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{item.label}</p>
                <p className="mt-2 text-white">{item.value}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
      <div className="space-y-6">
        <Card title={t('module.admin.deployment_title')} description={t('module.admin.deployment_description')}>
          {deploymentPending ? (
            <LoadingState label={t('auth.session.restoring')} />
          ) : deploymentError ? (
            <ErrorState message={deploymentError instanceof Error ? deploymentError.message : t('errors.generic')} retry={() => void refetchDeployment()} />
          ) : (
            <div className="space-y-3">
              {(deployment?.data ?? []).map((item) => (
                <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                  <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{item.label}</p>
                  <p className="mt-2 text-white">{item.value}</p>
                </div>
              ))}
            </div>
          )}
        </Card>
        <Card title={t('module.admin.backup_title')} description={t('module.admin.backup_description')}>
          {backupPending ? (
            <LoadingState label={t('auth.session.restoring')} />
          ) : backupError ? (
            <ErrorState message={backupError instanceof Error ? backupError.message : t('errors.generic')} retry={() => void refetchBackup()} />
          ) : (
            <div className="space-y-3">
              {(backup?.data ?? []).map((item) => (
                <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                  <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{item.label}</p>
                  <p className="mt-2 text-white">{item.value}</p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
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
      description={config.description}
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
    return <Navigate to={resolveDashboardPath(role)} replace />;
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
                      const path = resolveDashboardPath(session.role);
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
  const persona = resolveDashboardPersona(user, activeRole);
  const isLoginRoute = location.pathname.startsWith('/login');
  const isPublicRoute = !isLoginRoute && !location.pathname.startsWith('/dashboard') && !location.pathname.startsWith('/profile') && !location.pathname.startsWith('/favorites') && !location.pathname.startsWith('/notifications') && !location.pathname.startsWith('/requests') && !location.pathname.startsWith('/documents') && !location.pathname.startsWith('/workflow') && !location.pathname.startsWith('/observability') && !location.pathname.startsWith('/readiness');
  const publicLinks = publicNavItems.map((item) => ({ ...item, label: t(item.labelKey) }));
  const displayName = user?.name || user?.email || t('shared.user');
  const displayRole = t(resolveRoleLabelKey(persona));
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
            <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-end gap-4">
              <div className="flex flex-wrap items-center gap-3">
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
