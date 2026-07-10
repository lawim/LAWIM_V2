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
  useLanguage
} from '@ui';
import { resolveDashboardPath, resolvePrimaryRole, type AccessRole, useAuthStore } from '@auth';

type MissionRole = 'admin' | 'manager' | 'agent' | 'partner' | 'user' | 'investor';

type RoleDefinition = {
  title: string;
  intro: string;
  emptyConversation: string;
  projectLabel: string;
  projectEmpty: string;
  summaryLabels: readonly [string, string, string];
  actions: readonly string[];
  relationTitle: string;
  relationDescription: string;
  relationCta: string;
  secondaryNav: readonly { label: string; to: string }[];
};

type CockpitStat = {
  label: string;
  value: string;
  tone?: 'default' | 'accent';
};

type RelationshipCard = {
  title: string;
  description: string;
  cta: string;
  to?: string;
};

type ProjectCard = {
  title: string;
  status: string;
  description: string;
  to: string;
};

type FrameProps = {
  title: string;
  subtitle: string;
  children: ReactNode;
  backTo?: { label: string; to: string };
};

const MISSION_ROLE_BY_ACCESS_ROLE: Record<AccessRole, MissionRole> = {
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

const CAMEROON_MAJOR_CITIES = [
  { value: 'Yaounde', label: 'Yaoundé', region: 'Centre', quartiers: ['Bastos', 'Biyem-Assi', 'Essos', 'Mendong', 'Ngoa-Ekellé', 'Nlongkak', 'Omnisports', 'Mvog-Mbi', 'Etoudi', 'Autre'] },
  { value: 'Douala', label: 'Douala', region: 'Littoral', quartiers: ['Bonanjo', 'Akwa', 'Bonapriso', 'Bonamoussadi', 'Makepe', 'Logpom', 'Deido', 'Bali', 'New Bell', 'Autre'] },
  { value: 'Bamenda', label: 'Bamenda', region: 'Nord-Ouest', quartiers: ['Commercial Avenue', 'Nkwen', 'Old Town', 'Mile 4', 'Quarter 1', 'Autre'] },
  { value: 'Bafoussam', label: 'Bafoussam', region: 'Ouest', quartiers: ['Banengo', 'Kamkop', 'Tougang', 'Kouogouo', 'Tamdja', 'Autre'] },
  { value: 'Buea', label: 'Buea', region: 'Sud-Ouest', quartiers: ['Molyko', 'Malingo', 'Bokwango', 'Muea', 'Bonduma', 'Autre'] },
  { value: 'Kribi', label: 'Kribi', region: 'Sud', quartiers: ['Likodo', 'Bongandoue', 'Dombe', 'Lolabe', 'Ngoye', 'Autre'] },
  { value: 'Nkongsamba', label: 'Nkongsamba', region: 'Littoral', quartiers: ['Makenene', 'Centre-ville', 'Ndogpassi', 'Autre'] },
  { value: 'Maroua', label: 'Maroua', region: 'Extrême-Nord', quartiers: ['Domayo', 'Pitoaré', 'Baoliwol', 'Doualaré', 'Ziling', 'Autre'] },
  { value: 'Limbe', label: 'Limbé', region: 'Sud-Ouest', quartiers: ['Mokunda', 'Down Beach', 'New Town', 'Mile 4', 'Autre'] },
  { value: 'Garoua', label: 'Garoua', region: 'Nord', quartiers: ['Plateau', 'Poumpoumré', 'Djamboutou', 'Marouaré', 'Autre'] }
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

const ROLE_DEFINITIONS: Record<MissionRole, RoleDefinition> = {
  admin: {
    title: 'Cockpit administrateur',
    intro: 'Santé plateforme, sécurité, supervision et performance.',
    emptyConversation: 'Aucune alerte n’est ouverte.',
    projectLabel: 'Dossiers de supervision',
    projectEmpty: 'Aucun contrôle prioritaire pour le moment.',
    summaryLabels: ['Santé plateforme', 'Sécurité', 'Déploiements'],
    actions: ['Ouvrir la supervision', 'Vérifier la sécurité', 'Consulter les performances', 'Lancer un contrôle'],
    relationTitle: 'Une sauvegarde mérite vérification.',
    relationDescription: 'Le cycle de continuité est prêt à être relu avant la prochaine mise en production.',
    relationCta: 'Voir pourquoi',
    secondaryNav: [
      { label: 'Supervision', to: '/observability' },
      { label: 'Déploiement', to: '/workflow' },
      { label: 'Sécurité', to: '/readiness' }
    ]
  },
  manager: {
    title: 'Cockpit manager',
    intro: 'Activité d’équipe, dossiers bloqués et délais.',
    emptyConversation: 'Les équipes sont en attente de votre arbitrage.',
    projectLabel: 'Dossiers actifs',
    projectEmpty: 'Aucun dossier urgent n’a remonté.',
    summaryLabels: ['Équipes', 'Bloqués', 'Délais'],
    actions: ['Voir les équipes', 'Ouvrir les dossiers bloqués', 'Suivre les délais', 'Relancer le dossier'],
    relationTitle: 'Un dossier attend une décision.',
    relationDescription: 'La progression est gelée depuis 48 heures et la prochaine action est claire.',
    relationCta: 'Voir le blocage',
    secondaryNav: [
      { label: 'Dossiers', to: '/dossier' },
      { label: 'Conversations', to: '/conversation' },
      { label: 'Historique', to: '/history' }
    ]
  },
  agent: {
    title: 'Cockpit Agent LAWIM',
    intro: 'Conversations à reprendre, urgences et rendez-vous.',
    emptyConversation: 'Aucune conversation n’attend votre reprise.',
    projectLabel: 'Conversations à reprendre',
    projectEmpty: 'Aucun dossier n’est en attente de l’agent.',
    summaryLabels: ['Conversations', 'Urgences', 'Rendez-vous'],
    actions: ['Reprendre la conversation', 'Prendre rendez-vous', 'Voir les relations', 'Ouvrir les urgences'],
    relationTitle: 'Un partenaire pourrait rejoindre le dossier.',
    relationDescription: 'Cette mise en relation arrive maintenant au bon moment pour accélérer le projet.',
    relationCta: 'Voir la proposition',
    secondaryNav: [
      { label: 'Conversations', to: '/conversation' },
      { label: 'Dossier', to: '/dossier' },
      { label: 'Partenaires', to: '/partners' }
    ]
  },
  partner: {
    title: 'Cockpit partenaire',
    intro: 'Missions, demandes et échanges liés à votre spécialité.',
    emptyConversation: 'Aucune mission ne requiert votre réponse immédiate.',
    projectLabel: 'Missions actives',
    projectEmpty: 'Aucune mission ouverte pour le moment.',
    summaryLabels: ['Missions', 'Demandes', 'Échanges'],
    actions: ['Voir les missions', 'Ouvrir les conversations', 'Mettre à jour mes disponibilités', 'Partager une disponibilité'],
    relationTitle: 'Un nouveau dossier correspond à votre spécialité.',
    relationDescription: 'La demande est contextualisée et prête à vous être présentée.',
    relationCta: 'Découvrir la mission',
    secondaryNav: [
      { label: 'Missions', to: '/partners' },
      { label: 'Conversations', to: '/conversation' },
      { label: 'Historique', to: '/history' }
    ]
  },
  user: {
    title: 'Cockpit utilisateur',
    intro: 'Nous poursuivons votre projet, sans perdre le contexte.',
    emptyConversation: 'Vous n’avez aucun projet actif pour le moment.',
    projectLabel: 'Projets actifs',
    projectEmpty: 'Aucun dossier projet n’est ouvert.',
    summaryLabels: ['Projets actifs', 'Conversations', 'Opportunités'],
    actions: ['Continuer le projet', 'Ajouter un document', 'Découvrir un bien', 'Voir les partenaires proposés'],
    relationTitle: 'Nous avons identifié 2 biens susceptibles de vous intéresser.',
    relationDescription: 'Ils correspondent à votre intention, à votre budget et à votre localisation.',
    relationCta: 'Découvrir',
    secondaryNav: [
      { label: 'Conversation', to: '/conversation' },
      { label: 'Biens', to: '/biens' },
      { label: 'Historique', to: '/history' }
    ]
  },
  investor: {
    title: 'Cockpit investisseur',
    intro: 'Opportunités, échanges et demandes reçues.',
    emptyConversation: 'Aucune opportunité active n’est disponible.',
    projectLabel: 'Opportunités suivies',
    projectEmpty: 'Aucune opportunité suivie pour le moment.',
    summaryLabels: ['Opportunités', 'Demandes', 'Conversations'],
    actions: ['Voir les opportunités', 'Comparer les biens', 'Ouvrir les échanges', 'Revoir le dossier'],
    relationTitle: 'Une opportunité semble correspondre à votre profil.',
    relationDescription: 'La proposition met l’accent sur le rendement, la localisation et l’usage.',
    relationCta: 'Découvrir',
    secondaryNav: [
      { label: 'Opportunités', to: '/biens' },
      { label: 'Conversation', to: '/conversation' },
      { label: 'Historique', to: '/history' }
    ]
  }
};

function useTranslator() {
  const { language } = useLanguage();
  return {
    language,
    t: (key: string, params?: Record<string, string | number>) => translate(key, language, params)
  };
}

function missionRoleFromAccessRole(role: AccessRole | null | undefined): MissionRole {
  if (!role) {
    return 'user';
  }
  return MISSION_ROLE_BY_ACCESS_ROLE[role] ?? 'user';
}

function getInitials(value: string | undefined | null) {
  const parts = String(value ?? '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (parts.length === 0) return 'LW';
  return parts
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
    .slice(0, 2);
}

function normalizeProjectTitle(project: ProjectSummary | null, fallback: string) {
  if (!project) {
    return fallback;
  }
  const city = project.location_city ? ` · ${project.location_city}` : '';
  return `${project.title}${city}`;
}

function getCurrentCityDefinition(value: string) {
  return CAMEROON_MAJOR_CITIES.find((city) => city.value === value) ?? CAMEROON_MAJOR_CITIES[0];
}

function resolveDepartmentOptions(region: string) {
  return CAMEROON_DEPARTMENTS_BY_REGION[region as keyof typeof CAMEROON_DEPARTMENTS_BY_REGION] ?? [];
}

function formatMoney(value?: number | null) {
  if (value == null) return '—';
  return new Intl.NumberFormat('fr-FR').format(value);
}

function getFirstName(value: string | undefined | null) {
  const parts = String(value ?? '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  return parts[0] ?? 'Abel';
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

function describeProjectThemePhrase(theme: string) {
  switch (theme) {
    case 'construction':
      return 'de construction';
    case 'terrain':
      return 'terrain';
    case 'location':
      return 'de location';
    case 'investissement':
      return "d'investissement";
    case 'achat':
      return "d'achat";
    case 'vente':
      return 'de vente';
    default:
      return '';
  }
}

function buildCockpitNarrative(
  role: MissionRole,
  userName: string,
  activeProject: ProjectSummary | null,
  summary: { properties: number; opportunities: number; communications: number; pendingTasks: number }
) {
  const firstName = getFirstName(userName);
  const theme = describeProjectTheme(activeProject?.objective);
  const themePhrase = describeProjectThemePhrase(theme);
  const projectTitle = activeProject ? normalizeProjectTitle(activeProject, 'Dossier actif') : 'votre dossier';
  const pendingText =
    summary.pendingTasks > 1
      ? `${summary.pendingTasks} décisions importantes vous attendent aujourd’hui.`
      : summary.pendingTasks === 1
        ? '1 décision importante vous attend aujourd’hui.'
        : 'Aucune action critique ne bloque le dossier.';
  const conversationText =
    summary.communications > 1
      ? `${summary.communications} conversations actives`
      : summary.communications === 1
        ? '1 conversation active'
        : 'Reprise immédiate';

  switch (role) {
    case 'admin':
      return {
        title: `Bonjour ${firstName}. La plateforme reste sous contrôle.`,
        lead: `${pendingText} LAWIM garde la supervision, la sécurité et les déploiements bien alignés.`,
        signal: pendingText,
        note: `La vue d’ensemble reste centrée sur ${projectTitle}.`
      };
    case 'manager':
      return {
        title: `Bonjour ${firstName}. Vos dossiers sensibles avancent.`,
        lead:
          summary.pendingTasks > 0
            ? `${summary.pendingTasks} relances sont prêtes. LAWIM garde les équipes et les délais sous la même lecture.`
            : 'Les équipes, les délais et les arbitrages restent dans le même cadre.',
        signal: conversationText,
        note: `Le dossier ${projectTitle} reste visible et actionnable.`
      };
    case 'agent':
      return {
        title: `Bonjour ${firstName}. Les conversations prêtes à reprendre vous attendent.`,
        lead:
          summary.pendingTasks > 0
            ? `${summary.pendingTasks} échange${summary.pendingTasks > 1 ? 's' : ''} demande${summary.pendingTasks > 1 ? 'nt' : ''} votre attention. LAWIM garde le contexte complet sous la main.`
            : 'LAWIM garde le contexte complet sous la main.',
        signal: conversationText,
        note: `Le dossier ${projectTitle} reste lié aux bonnes personnes et au bon moment.`
      };
    case 'partner':
      return {
        title: `Bonjour ${firstName}. Une mission peut vous être confiée.`,
        lead: 'LAWIM vous présente les interventions utiles à votre spécialité et au bon timing.',
        signal: summary.opportunities > 1 ? `${summary.opportunities} missions ciblées` : 'Mission ciblée',
        note: `Le dossier ${projectTitle} reste contextualisé avant toute prise de contact.`
      };
    case 'investor':
      return {
        title: `Bonjour ${firstName}. Vos opportunités se précisent.`,
        lead:
          summary.pendingTasks > 0
            ? `${summary.pendingTasks} demande${summary.pendingTasks > 1 ? 's' : ''} et ${summary.opportunities} opportunité${summary.opportunities > 1 ? 's' : ''} restent à arbitrer.`
            : 'LAWIM affine les biens compatibles avec votre stratégie.',
        signal: summary.opportunities > 1 ? `${summary.opportunities} opportunités suivies` : 'Veille active',
        note: themePhrase ? `Le dossier ${projectTitle} reste orienté vers ${themePhrase}.` : `Le dossier ${projectTitle} reste orienté vers votre stratégie.`
      };
    default:
      return {
        title: `Bonjour ${firstName}. Votre projet ${themePhrase ? `${themePhrase} ` : ''}avance.`.replace(/\s+\./, '.'),
        lead:
          summary.pendingTasks > 0
            ? `${pendingText} LAWIM garde le contexte, le budget et les prochaines propositions dans le même dossier.`
            : 'LAWIM garde le contexte, le budget et les prochaines propositions dans le même dossier.',
        signal: summary.communications > 1 ? `${summary.communications} conversations en cours` : summary.communications === 1 ? '1 conversation en cours' : 'Projet actif',
        note: themePhrase ? `Nous restons concentrés sur ${themePhrase}.` : `Nous restons concentrés sur ${projectTitle}.`
      };
  }
}

function getPropertyTone(asset: string, index: number) {
  const palette = {
    terrain: {
      label: 'Terrain',
      accent: 'amber',
      gradient: index % 2 === 0 ? 'from-amber-100 via-white to-slate-100' : 'from-amber-50 via-white to-orange-50',
      orb: 'bg-amber-300/35',
      frame: 'border-amber-100'
    },
    maison: {
      label: 'Maison',
      accent: 'sky',
      gradient: index % 2 === 0 ? 'from-sky-100 via-white to-slate-100' : 'from-cyan-100 via-white to-sky-50',
      orb: 'bg-sky-300/35',
      frame: 'border-sky-100'
    },
    appartement: {
      label: 'Appartement',
      accent: 'emerald',
      gradient: index % 2 === 0 ? 'from-emerald-100 via-white to-slate-100' : 'from-teal-100 via-white to-emerald-50',
      orb: 'bg-emerald-300/35',
      frame: 'border-emerald-100'
    },
    immeuble: {
      label: 'Immeuble',
      accent: 'slate',
      gradient: index % 2 === 0 ? 'from-slate-100 via-white to-zinc-100' : 'from-stone-100 via-white to-slate-50',
      orb: 'bg-slate-300/30',
      frame: 'border-slate-200'
    },
    local: {
      label: 'Local commercial',
      accent: 'rose',
      gradient: index % 2 === 0 ? 'from-rose-100 via-white to-slate-100' : 'from-pink-100 via-white to-rose-50',
      orb: 'bg-rose-300/30',
      frame: 'border-rose-100'
    },
    autre: {
      label: 'Bien',
      accent: 'indigo',
      gradient: index % 2 === 0 ? 'from-indigo-100 via-white to-slate-100' : 'from-violet-100 via-white to-indigo-50',
      orb: 'bg-indigo-300/30',
      frame: 'border-indigo-100'
    }
  } as const;

  return palette[asset as keyof typeof palette] ?? palette.autre;
}

function getPropertyFeatureLabels(
  asset: string,
  data: { rooms: string; bathrooms: string; standing: string; titleFoncier: boolean; accessRoad: boolean; viabilisation: boolean; garage: boolean; kitchen: boolean }
) {
  if (asset === 'terrain') {
    return [
      data.titleFoncier ? 'Titre foncier' : 'Titre à confirmer',
      data.accessRoad ? 'Accès direct' : 'Accès à préciser',
      data.viabilisation ? 'Viabilisé' : 'Viabilisation à prévoir'
    ];
  }

  const roomLabel = data.rooms ? `${data.rooms} chambre${data.rooms === '1' ? '' : 's'}` : 'Configuration à préciser';
  const bathLabel = data.bathrooms ? `${data.bathrooms} salle${data.bathrooms === '1' ? '' : 's'} de bain` : 'Salles de bain à préciser';
  const standingLabel =
    data.standing === 'haut' ? 'Standing haut' : data.standing === 'bon' ? 'Standing bon' : data.standing === 'moyen' ? 'Standing moyen' : 'Standing standard';

  return [roomLabel, bathLabel, standingLabel, data.garage ? 'Garage' : 'Sans garage', data.kitchen ? 'Cuisine équipée' : 'Cuisine à aménager'].slice(0, 4);
}

function getPartnerTone(need: string, index: number) {
  const palette = {
    architecte: {
      label: 'Architecte',
      accent: 'amber',
      gradient: index % 2 === 0 ? 'from-amber-100 via-white to-slate-100' : 'from-orange-100 via-white to-amber-50',
      orb: 'bg-amber-300/35',
      frame: 'border-amber-100'
    },
    géomètre: {
      label: 'Géomètre',
      accent: 'teal',
      gradient: index % 2 === 0 ? 'from-teal-100 via-white to-slate-100' : 'from-cyan-100 via-white to-teal-50',
      orb: 'bg-teal-300/30',
      frame: 'border-teal-100'
    },
    notaire: {
      label: 'Notaire',
      accent: 'slate',
      gradient: index % 2 === 0 ? 'from-slate-100 via-white to-zinc-100' : 'from-stone-100 via-white to-slate-50',
      orb: 'bg-slate-300/30',
      frame: 'border-slate-200'
    },
    banque: {
      label: 'Banque',
      accent: 'indigo',
      gradient: index % 2 === 0 ? 'from-indigo-100 via-white to-slate-100' : 'from-violet-100 via-white to-indigo-50',
      orb: 'bg-indigo-300/30',
      frame: 'border-indigo-100'
    },
    entrepreneur: {
      label: 'Entrepreneur',
      accent: 'rose',
      gradient: index % 2 === 0 ? 'from-rose-100 via-white to-slate-100' : 'from-pink-100 via-white to-rose-50',
      orb: 'bg-rose-300/30',
      frame: 'border-rose-100'
    },
    décorateur: {
      label: 'Décorateur',
      accent: 'emerald',
      gradient: index % 2 === 0 ? 'from-emerald-100 via-white to-slate-100' : 'from-green-100 via-white to-emerald-50',
      orb: 'bg-emerald-300/30',
      frame: 'border-emerald-100'
    },
    promoteur: {
      label: 'Promoteur',
      accent: 'amber',
      gradient: index % 2 === 0 ? 'from-amber-100 via-white to-slate-100' : 'from-yellow-100 via-white to-amber-50',
      orb: 'bg-amber-300/35',
      frame: 'border-amber-100'
    },
    'expert foncier': {
      label: 'Expert foncier',
      accent: 'sky',
      gradient: index % 2 === 0 ? 'from-sky-100 via-white to-slate-100' : 'from-cyan-100 via-white to-sky-50',
      orb: 'bg-sky-300/30',
      frame: 'border-sky-100'
    },
    photographe: {
      label: 'Photographe',
      accent: 'purple',
      gradient: index % 2 === 0 ? 'from-purple-100 via-white to-slate-100' : 'from-fuchsia-100 via-white to-purple-50',
      orb: 'bg-purple-300/30',
      frame: 'border-purple-100'
    },
    artisan: {
      label: 'Artisan',
      accent: 'amber',
      gradient: index % 2 === 0 ? 'from-orange-100 via-white to-slate-100' : 'from-amber-100 via-white to-orange-50',
      orb: 'bg-orange-300/30',
      frame: 'border-orange-100'
    }
  } as const;

  return palette[need as keyof typeof palette] ?? palette.artisan;
}

function getPartnerProjects(projectType: string) {
  switch (projectType) {
    case 'construction':
      return ['Construction', 'Achat de terrain', 'Rénovation'];
    case 'achat':
      return ['Achat', 'Sécurisation', 'Signature'];
    case 'location':
      return ['Location', 'Publication', 'Gestion'];
    case 'investissement':
      return ['Investissement', 'Rendement', 'Décision'];
    case 'vente':
      return ['Vente', 'Présentation', 'Relance'];
    default:
      return ['Construction', 'Achat', 'Investissement'];
  }
}

function traceCockpitRender(step: string, details: Record<string, unknown> = {}) {
  if (window.localStorage.getItem('lawim.debug.auth') === '1') {
    console.debug(step, details);
  }
}

function resolveMissionRoleFromLocation(pathname: string) {
  if (pathname.startsWith('/cockpit/manager')) return 'manager';
  if (pathname.startsWith('/cockpit/agent')) return 'agent';
  if (pathname.startsWith('/cockpit/partner')) return 'partner';
  if (pathname.startsWith('/cockpit/investor')) return 'investor';
  if (pathname.startsWith('/cockpit/user')) return 'user';
  if (pathname.startsWith('/cockpit/admin')) return 'admin';
  return null;
}

function Surface({ className = '', children }: { className?: string; children: ReactNode }) {
  return (
    <section
      className={`lawim-reveal rounded-[32px] border border-slate-200/80 bg-white/92 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_24px_80px_rgba(15,23,42,0.12)] ${className}`.trim()}
    >
      {children}
    </section>
  );
}

function StatPill({ label, value, tone = 'default' }: CockpitStat) {
  return (
    <div
      className={`rounded-[24px] border px-4 py-3 transition-all duration-300 ${
        tone === 'accent'
          ? 'border-amber-200/80 bg-gradient-to-br from-amber-50 via-white to-white shadow-[0_12px_30px_rgba(180,140,40,0.08)]'
          : 'border-slate-200 bg-slate-50/80 shadow-[0_10px_24px_rgba(15,23,42,0.04)]'
      }`}
    >
      <div className="text-[11px] uppercase tracking-[0.24em] text-slate-500">{label}</div>
      <div className="mt-2 text-2xl font-semibold tracking-tight text-slate-950">{value}</div>
    </div>
  );
}

function ActionChip({ label, to, onClick, tone = 'secondary' }: { label: string; to?: string; onClick?: () => void; tone?: 'primary' | 'secondary' }) {
  const className =
    tone === 'primary'
      ? 'bg-slate-950 text-white shadow-[0_12px_28px_rgba(15,23,42,0.16)] hover:bg-slate-900'
      : 'border border-slate-200/80 bg-white text-slate-800 shadow-[0_10px_24px_rgba(15,23,42,0.05)] hover:border-slate-300 hover:bg-slate-50';
  if (to) {
    return (
      <NavLink
        to={to}
        className={`inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-medium transition-all duration-300 hover:-translate-y-0.5 ${className}`}
      >
        {label}
      </NavLink>
    );
  }
  return (
    <button
      type="button"
      className={`inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-medium transition-all duration-300 hover:-translate-y-0.5 ${className}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

function Frame({ title, subtitle, children, backTo }: FrameProps) {
  const { language, t } = useTranslator();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const logout = useAuthStore((state) => state.logout);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const displayName = user?.name || user?.email || t('shared.user');
  const initials = getInitials(displayName);
  const [search, setSearch] = useState('');

  const submitSearch = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = search.trim();
    if (!trimmed) {
      navigate('/search');
      return;
    }
    navigate(`/search?q=${encodeURIComponent(trimmed)}`);
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(226,232,240,0.88),_rgba(248,250,252,0.98)_30%,_rgba(241,245,249,1)_100%)] text-slate-900">
      <header className="sticky top-0 z-30 border-b border-slate-200/90 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <BrandMark slogan={LAWIM_BRAND_SLOGAN} tone="light" className="shrink-0" />
          <div className="flex min-w-0 flex-1 items-center gap-3">
            <form onSubmit={submitSearch} className="min-w-0 flex-1">
              <Input
                tone="light"
                aria-label={t('cockpit.search')}
                placeholder={t('cockpit.search_placeholder')}
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="w-full rounded-full border-slate-200 bg-white px-4 py-2.5 text-sm shadow-sm"
              />
            </form>
          </div>
          <LanguageSwitcher compact />
          <div className="flex items-center gap-3 rounded-full border border-slate-200 bg-white px-3 py-2 shadow-sm">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">{initials}</div>
            <div className="leading-tight">
              <div className="text-sm font-semibold text-slate-900">{displayName}</div>
              <div className="text-[11px] uppercase tracking-[0.24em] text-slate-500">{translate(ROLE_LABEL_BY_MISSION_ROLE[role], language)}</div>
            </div>
          </div>
          <Button type="button" variant="secondary" onClick={() => void logout()}>
            {t('auth.logout')}
          </Button>
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        {backTo ? (
          <div className="flex items-center justify-between gap-4">
            <button
              type="button"
              className="text-sm font-medium text-slate-500 transition hover:text-slate-900"
              onClick={() => navigate(backTo.to)}
            >
              ← {backTo.label}
            </button>
            <div className="text-xs uppercase tracking-[0.28em] text-slate-400">{LAWIM_BRAND_SLOGAN}</div>
          </div>
        ) : null}
        <section className="grid gap-6 xl:grid-cols-[1.18fr_0.82fr]">
          <div className="space-y-6">
            <Surface className="p-6 sm:p-7">
              <div className="flex flex-wrap items-center gap-3">
                <Badge variant="info">{title}</Badge>
                <Badge variant="success">{subtitle}</Badge>
              </div>
              <h1 className="mt-5 max-w-3xl text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">{title}</h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">{subtitle}</p>
            </Surface>
            {children}
          </div>
          <aside className="space-y-6">
            <Surface className="p-6 sm:p-7">
              <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">{t('cockpit.topbar')}</div>
              <p className="mt-3 text-sm leading-6 text-slate-600">{LAWIM_OFFICIAL_CONTACT.supportEmail}</p>
              <p className="mt-2 text-sm text-slate-500">{LAWIM_OFFICIAL_CONTACT.websiteUrl.replace(/^https?:\/\//, '')}</p>
            </Surface>
            {backTo ? null : (
            <Surface className="p-6 sm:p-7">
              <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">{t('cockpit.navigation')}</div>
              <div className="mt-4 flex flex-wrap gap-2">
                <ActionChip label={t('cockpit.resume')} tone="primary" to="/conversation" />
                <ActionChip label={t('cockpit.new_project')} to="/biens" />
                <ActionChip label={t('cockpit.history')} to="/history" />
              </div>
            </Surface>
            )}
          </aside>
        </section>
      </div>
    </main>
  );
}

function roleStatSummary(role: MissionRole, summary: { properties: number; opportunities: number; communications: number; pendingTasks: number }, projects: ProjectSummary[]): CockpitStat[] {
  const projectCount = projects.length;
  if (role === 'admin') {
    return [
      { label: 'Santé', value: `${Math.max(94, 100 - summary.pendingTasks)}%`, tone: 'accent' },
      { label: 'Sécurité', value: summary.pendingTasks > 0 ? '1 contrôle' : 'OK' },
      { label: 'Déploiements', value: `${Math.max(1, Math.min(3, summary.opportunities || 1))}` }
    ];
  }
  if (role === 'manager') {
    return [
      { label: 'Équipes', value: `${Math.max(1, projectCount + 2)}` },
      { label: 'Bloqués', value: `${summary.pendingTasks}` },
      { label: 'Délais', value: summary.communications > 0 ? 'À relancer' : 'Sous contrôle', tone: 'accent' }
    ];
  }
  if (role === 'agent') {
    return [
      { label: 'Conversations', value: `${Math.max(summary.communications, projectCount)}` },
      { label: 'Urgences', value: `${summary.pendingTasks}` },
      { label: 'Rendez-vous', value: `${Math.max(1, summary.opportunities)}`, tone: 'accent' }
    ];
  }
  if (role === 'investor') {
    return [
      { label: 'Opportunités', value: `${Math.max(summary.opportunities, projectCount)}` },
      { label: 'Demandes', value: `${summary.pendingTasks}` },
      { label: 'Conversations', value: `${Math.max(1, summary.communications)}`, tone: 'accent' }
    ];
  }
  if (role === 'partner') {
    return [
      { label: 'Missions', value: `${Math.max(1, projectCount)}` },
      { label: 'Demandes', value: `${summary.pendingTasks}` },
      { label: 'Échanges', value: `${Math.max(1, summary.communications)}`, tone: 'accent' }
    ];
  }
  return [
    { label: 'Projets', value: `${Math.max(1, projectCount)}` },
    { label: 'Conversations', value: `${Math.max(1, summary.communications)}` },
    { label: 'Opportunités', value: `${Math.max(1, summary.opportunities)}`, tone: 'accent' }
  ];
}

function buildProjectCards(role: MissionRole, projects: ProjectSummary[]): ProjectCard[] {
  if (role === 'admin') {
    return [
      {
        title: 'Santé plateforme',
        status: 'Stable',
        description: 'Les services principaux répondent et la supervision reste lisible.',
        to: '/observability'
      },
      {
        title: 'Déploiement',
        status: 'À relire',
        description: 'Le prochain jalon attend le contrôle final avant mise en production.',
        to: '/workflow'
      }
    ];
  }

  if (projects.length === 0) {
    return [];
  }

  return projects.slice(0, 3).map((project, index) => ({
    title: project.title,
    status: project.status || (index === 0 ? 'En cours' : 'En attente'),
    description: project.objective || normalizeProjectTitle(project, 'Dossier projet'),
    to: `/dossier/${project.id}`
  }));
}

function buildRoleDefinition(role: MissionRole): RoleDefinition {
  const base = ROLE_DEFINITIONS[role];
  return {
    ...base,
    title: base.title,
    intro: base.intro,
    emptyConversation: base.emptyConversation,
    projectLabel: base.projectLabel,
    projectEmpty: base.projectEmpty,
    summaryLabels: base.summaryLabels,
    actions: base.actions,
    relationTitle: base.relationTitle,
    relationDescription: base.relationDescription,
    relationCta: base.relationCta,
    secondaryNav: base.secondaryNav
  };
}

function roleActionTarget(role: MissionRole, index: number) {
  const targets: Record<MissionRole, readonly string[]> = {
    admin: ['/observability', '/readiness', '/workflow', '/observability'],
    manager: ['/dossier', '/conversation', '/history', '/dossier'],
    agent: ['/conversation', '/conversation', '/partners', '/partners'],
    partner: ['/partners', '/conversation', '/history', '/partners'],
    user: ['/conversation', '/documents', '/biens', '/partners'],
    investor: ['/biens', '/biens', '/conversation', '/history']
  };
  return targets[role][index] ?? '/conversation';
}

function RoleCockpitBody({ role, projects, summary }: { role: MissionRole; projects: ProjectSummary[]; summary: { properties: number; opportunities: number; communications: number; pendingTasks: number } }) {
  const { language, t } = useTranslator();
  const navigate = useNavigate();
  const roleCopy = buildRoleDefinition(role);
  const user = useAuthStore((state) => state.user);
  const userName = user?.name || user?.email?.split('@')[0] || t('shared.user');
  const activeProject = projects[0] ?? null;
  const projectCards = buildProjectCards(role, projects);
  const stats = roleStatSummary(role, summary, projects);

  useEffect(() => {
    traceCockpitRender('COCKPIT_RENDERED', {
      role,
      path: resolveDashboardPath(role)
    });
  }, [role]);

  const matchQuery = useMemo<MatchQuery | undefined>(() => {
    if (role === 'admin' || role === 'manager') {
      return undefined;
    }
    if (role === 'agent' || role === 'partner') {
      return {
        target_type: 'partner',
        partner_type: role === 'agent' ? 'architect' : 'bank',
        city: activeProject?.location_city ?? 'Douala',
        country: 'Cameroon',
        limit: 2
      };
    }
    return {
      target_type: 'property',
      city: activeProject?.location_city ?? 'Douala',
      country: 'Cameroon',
      budget_max: activeProject?.budget_max ?? activeProject?.budget_min ?? undefined,
      limit: 2
    };
  }, [activeProject?.budget_max, activeProject?.budget_min, activeProject?.location_city, role]);

  const { data: matchData } = useQuery({
    queryKey: ['cockpit-matches', role, activeProject?.id],
    queryFn: () => apiSdk.getMatches(matchQuery),
    enabled: Boolean(matchQuery)
  });

  const matches = matchData?.data ?? [];
  const relations: RelationshipCard[] =
    matches.length > 0
      ? matches.slice(0, 2).map((match, index) => {
          const partnerName =
            match.partner != null && typeof match.partner === 'object' && 'display_name' in match.partner
              ? String((match.partner as Record<string, unknown>).display_name ?? '')
              : '';
          const label = match.property?.title ?? partnerName ?? `Opportunité ${index + 1}`;
          const description = match.summary || (match.reasons.length > 0 ? match.reasons.join(' · ') : roleCopy.relationDescription);
          const to = role === 'user' || role === 'investor' ? '/search' : role === 'agent' || role === 'partner' ? '/partners' : '/conversation';
          return { title: label, description, cta: 'Découvrir', to };
        })
      : role === 'admin'
        ? []
        : [
            {
              title: roleCopy.relationTitle,
              description: roleCopy.relationDescription,
              cta: roleCopy.relationCta,
              to: role === 'agent' || role === 'partner' ? '/partners' : '/search'
            }
          ];

  const activeConversationCopy =
    activeProject != null
      ? (() => {
          switch (role) {
            case 'admin':
              return `Bonjour ${userName}. La supervision de la plateforme reste active.`;
            case 'manager':
              return `Bonjour ${userName}. Les dossiers sensibles restent sous contrôle.`;
            case 'agent':
              return `Bonjour ${userName}. Les conversations à reprendre sont prêtes.`;
            case 'partner':
              return `Bonjour ${userName}. Vos missions et vos échanges restent centralisés.`;
            case 'investor':
              return `Bonjour ${userName}. Vos opportunités restent suivies.`;
            default:
              return `Bonjour ${userName}. Nous poursuivons votre projet.`;
          }
        })()
      : roleCopy.emptyConversation;
  const narrative = buildCockpitNarrative(role, userName, activeProject, summary);

  const primaryAction = (() => {
    switch (role) {
      case 'admin':
        return { label: 'Ouvrir la supervision', to: '/observability' };
      case 'manager':
        return { label: 'Voir les dossiers', to: '/dossier' };
      case 'agent':
        return { label: 'Reprendre le dossier', to: '/dossier' };
      case 'partner':
        return { label: 'Voir les missions', to: '/partners' };
      case 'investor':
        return { label: 'Voir les opportunités', to: '/biens' };
      default:
        return { label: activeProject ? 'Reprendre le projet' : 'Décrire mon projet', to: '/biens' };
    }
  })();

  const headline = role === 'admin' ? roleCopy.title : roleCopy.title;
  const subline = roleCopy.intro;

  return (
    <Frame title={headline} subtitle={subline}>
      <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-6">
          <Surface className="overflow-hidden p-6 sm:p-7">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex flex-wrap items-center gap-3">
                <Badge variant="info">{roleCopy.title}</Badge>
                <Badge variant="success">{translate(ROLE_LABEL_BY_MISSION_ROLE[role], language)}</Badge>
              </div>
              <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
                <span className="lawim-pulse-soft h-2 w-2 rounded-full bg-emerald-500" />
                LAWIM en veille
              </div>
            </div>
            <div className="mt-5 grid gap-5 lg:grid-cols-[1.18fr_0.82fr]">
              <div>
                <p className="text-sm uppercase tracking-[0.28em] text-slate-400">Conversation principale</p>
                <h2 className="mt-2 max-w-3xl text-3xl font-semibold tracking-tight text-slate-950">{narrative.title}</h2>
                <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">{narrative.lead}</p>
                <div className="mt-5 flex flex-wrap gap-3">
                  <ActionChip label={activeProject ? 'Continuer la conversation' : 'Créer une nouvelle conversation'} tone="primary" to="/conversation" />
                  <ActionChip label={primaryAction.label} to={primaryAction.to} />
                </div>
              </div>
              <div className="rounded-[28px] border border-slate-200 bg-slate-50/80 p-5 shadow-[0_12px_32px_rgba(15,23,42,0.05)]">
                <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Ce que LAWIM garde en tête</div>
                <p className="mt-3 text-sm leading-6 text-slate-700">{narrative.note}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Badge variant="info">{narrative.signal}</Badge>
                  <Badge variant="success">{activeProject ? activeProject.status : 'En attente'}</Badge>
                </div>
                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white bg-white p-4 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">État</p>
                    <p className="mt-2 text-sm font-semibold text-slate-950">{activeProject?.status ?? 'En attente'}</p>
                  </div>
                  <div className="rounded-2xl border border-white bg-white p-4 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Budget</p>
                    <p className="mt-2 text-sm font-semibold text-slate-950">
                      {activeProject?.budget_min != null || activeProject?.budget_max != null ? `${formatMoney(activeProject?.budget_min)} - ${formatMoney(activeProject?.budget_max)}` : 'À préciser'}
                    </p>
                  </div>
                  <div className="rounded-2xl border border-white bg-white p-4 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Contexte</p>
                    <p className="mt-2 text-sm font-semibold text-slate-950">{activeProject?.objective ?? roleCopy.intro}</p>
                  </div>
                  <div className="rounded-2xl border border-white bg-white p-4 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Prochaine étape</p>
                    <p className="mt-2 text-sm font-semibold text-slate-950">{primaryAction.label}</p>
                  </div>
                </div>
              </div>
            </div>
          </Surface>

          <section className="grid gap-3 sm:grid-cols-3">
            {stats.map((item) => (
              <StatPill key={item.label} {...item} />
            ))}
          </section>

          <div className="grid gap-6 xl:grid-cols-[1.03fr_0.97fr]">
            <Surface className="p-6 sm:p-7">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">{roleCopy.projectLabel}</p>
                  <h3 className="mt-2 text-xl font-semibold text-slate-950">{role === 'admin' ? 'Contrôles actifs' : 'Dossiers actifs'}</h3>
                </div>
                <Badge variant="info">{projectCards.length > 0 ? `${projectCards.length}` : '0'}</Badge>
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {projectCards.length > 0 ? (
                  projectCards.map((project) => (
                    <NavLink
                      key={project.title}
                      to={project.to}
                      className="rounded-[28px] border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-lg font-semibold text-slate-950">{project.title}</p>
                          <p className="mt-1 text-sm leading-6 text-slate-500">{project.description}</p>
                        </div>
                        <Badge variant="success">{project.status}</Badge>
                      </div>
                      <p className="mt-5 text-sm font-medium text-slate-900">Reprendre</p>
                    </NavLink>
                  ))
                ) : (
                  <div className="rounded-[28px] border border-dashed border-slate-200 bg-slate-50 p-5 text-sm text-slate-500">
                    {roleCopy.projectEmpty}
                  </div>
                )}
              </div>
            </Surface>

            <Surface className="p-6 sm:p-7">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">LAWIM anticipe</p>
                  <h3 className="mt-2 text-xl font-semibold text-slate-950">La prochaine étape est déjà préparée</h3>
                </div>
              </div>
              <div className="mt-5 grid gap-3">
                <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Lecture du dossier</p>
                  <p className="mt-2 text-sm leading-6 text-slate-700">{narrative.note}</p>
                </div>
                <div className="rounded-[24px] border border-slate-200 bg-white p-4">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Actions rapides</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {roleCopy.actions.map((action, index) => (
                      <ActionChip key={action} label={action} tone={index === 0 ? 'primary' : 'secondary'} to={roleActionTarget(role, index)} />
                    ))}
                  </div>
                </div>
              </div>
            </Surface>
          </div>

          {role !== 'admin' ? (
            <Surface className="p-6 sm:p-7">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Mises en relation</p>
                  <h3 className="mt-2 text-xl font-semibold text-slate-950">Le bon service au bon moment</h3>
                </div>
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {relations.length > 0 ? (
                  relations.map((relation) => (
                    <div key={relation.title} className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-[0_12px_30px_rgba(15,23,42,0.05)]">
                      <p className="text-lg font-semibold text-slate-950">{relation.title}</p>
                      <p className="mt-2 text-sm leading-6 text-slate-600">{relation.description}</p>
                      <div className="mt-4">
                        <ActionChip label={relation.cta} to={relation.to} />
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="rounded-[28px] border border-dashed border-slate-200 bg-slate-50 p-5 text-sm text-slate-500">
                    {roleCopy.relationDescription}
                  </div>
                )}
              </div>
            </Surface>
          ) : null}
        </div>

        <aside className="space-y-6 xl:sticky xl:top-28">
          <Surface className="p-6 sm:p-7">
            <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Résumé du dossier</div>
            <div className="mt-4 grid gap-3">
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">État</p>
                <p className="mt-2 text-sm font-semibold text-slate-950">{activeProject?.status ?? 'En attente'}</p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Contexte</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">{activeProject?.objective ?? roleCopy.intro}</p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Budget</p>
                <p className="mt-2 text-sm font-semibold text-slate-950">
                  {activeProject?.budget_min != null || activeProject?.budget_max != null
                    ? `${formatMoney(activeProject?.budget_min)} - ${formatMoney(activeProject?.budget_max)}`
                    : 'À préciser'}
                </p>
              </div>
            </div>
          </Surface>

          <Surface className="p-6 sm:p-7">
            <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Ce que LAWIM prépare</div>
            <div className="mt-4 space-y-3">
              <div className="rounded-2xl border border-slate-200 bg-white p-4">
                <p className="text-sm font-semibold text-slate-950">Dernière lecture</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">{narrative.lead}</p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-white p-4">
                <p className="text-sm font-semibold text-slate-950">Prochaine décision</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">{narrative.signal}</p>
              </div>
            </div>
          </Surface>

          <Surface className="p-6 sm:p-7">
            <div className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Navigation secondaire</div>
            <div className="mt-4 flex flex-wrap gap-2">
              {roleCopy.secondaryNav.map((item) => (
                <ActionChip key={item.to} label={item.label} to={item.to} />
              ))}
            </div>
          </Surface>
        </aside>
      </section>
    </Frame>
  );
}

function useProjectsSummary() {
  const projectsQuery = useQuery({ queryKey: ['cockpit-projects'], queryFn: () => apiSdk.getProjects() });
  const summaryQuery = useQuery({ queryKey: ['cockpit-summary'], queryFn: () => apiSdk.getDashboardSummary() });
  return {
    projects: projectsQuery.data?.data ?? [],
    projectsPending: projectsQuery.isPending,
    projectsError: projectsQuery.error,
    summary: summaryQuery.data?.data ?? { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 },
    summaryPending: summaryQuery.isPending,
    summaryError: summaryQuery.error
  };
}

function roleFromRouteOrUser(routeRole: string | undefined, userRole: AccessRole | null | undefined) {
  if (routeRole) {
    const normalized = routeRole.toLowerCase();
    if (normalized === 'agent' || normalized === 'operator') return 'agent';
    if (normalized === 'admin') return 'admin';
    if (normalized === 'manager') return 'manager';
    if (normalized === 'partner') return 'partner';
    if (normalized === 'investor') return 'investor';
    if (normalized === 'user' || normalized === 'owner') return 'user';
  }
  return missionRoleFromAccessRole(userRole ?? 'user');
}

export function PublicLandingPage() {
  const { t } = useTranslator();
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const roles = useAuthStore((state) => state.roles);
  const user = useAuthStore((state) => state.user);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));

  if (isAuthenticated) {
    return <Navigate to={resolveDashboardPath(role)} replace />;
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(226,232,240,0.92),_rgba(248,250,252,1)_35%,_rgba(241,245,249,1)_100%)] text-slate-900">
      <header className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-6 sm:px-6 lg:px-8">
        <BrandMark slogan={LAWIM_BRAND_SLOGAN} tone="light" />
        <div className="flex items-center gap-3">
          <LanguageSwitcher compact />
          <Button type="button" onClick={() => navigate('/login')}>
            {t('nav.login')}
          </Button>
        </div>
      </header>
      <div className="mx-auto grid max-w-7xl gap-8 px-4 py-10 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:px-8 lg:py-16">
        <section className="space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-500 shadow-sm">
            LAWIM
          </div>
          <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-slate-950 sm:text-6xl">L’immobilier autrement.</h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600">
            Un conseiller immobilier intelligent accompagne votre projet, garde le contexte et rend la prochaine étape évidente.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button type="button" onClick={() => navigate('/login')}>
              {t('nav.login')}
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate('/biens')}>
              {t('cockpit.new_project')}
            </Button>
          </div>
        </section>
        <section className="space-y-4">
          <Surface className="p-6 sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Conversation</p>
            <h2 className="mt-3 text-2xl font-semibold text-slate-950">Bonjour. Nous pouvons reprendre un dossier ou en ouvrir un nouveau.</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              LAWIM garde la conversation, les documents et les décisions au même endroit.
            </p>
          </Surface>
          <div className="grid gap-4 sm:grid-cols-3">
            <Surface className="p-5">
              <p className="text-xs uppercase tracking-[0.26em] text-slate-400">Projets</p>
              <p className="mt-3 text-3xl font-semibold text-slate-950">1</p>
            </Surface>
            <Surface className="p-5">
              <p className="text-xs uppercase tracking-[0.26em] text-slate-400">Conversations</p>
              <p className="mt-3 text-3xl font-semibold text-slate-950">1</p>
            </Surface>
            <Surface className="p-5">
              <p className="text-xs uppercase tracking-[0.26em] text-slate-400">Opportunités</p>
              <p className="mt-3 text-3xl font-semibold text-slate-950">2</p>
            </Surface>
          </div>
        </section>
      </div>
    </main>
  );
}

export function CockpitEntryPage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const resolvedRole = resolvePrimaryRole(user?.role, roles);
  return <Navigate to={resolveDashboardPath(resolvedRole)} replace />;
}

export function RoleCockpitPage() {
  const params = useParams();
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const canonicalRole = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const routeRole = resolveMissionRoleFromLocation(window.location.pathname) ?? (params.role as string | undefined);
  const { projects, projectsPending, summary, summaryPending } = useProjectsSummary();
  useEffect(() => {
    if (routeRole && routeRole !== canonicalRole) {
      navigate(resolveDashboardPath(canonicalRole), { replace: true });
    }
  }, [canonicalRole, navigate, routeRole]);

  const role = canonicalRole;

  if (projectsPending || summaryPending) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-10 text-slate-900">
        <div className="mx-auto max-w-7xl rounded-[28px] border border-slate-200 bg-white p-8 text-sm text-slate-500 shadow-sm">
          Restauration du cockpit…
        </div>
      </main>
    );
  }

  return <RoleCockpitBody role={role} projects={projects} summary={summary} />;
}

function ConversationThreadCard({ role, projects }: { role: MissionRole; projects: ProjectSummary[] }) {
  const { t } = useTranslator();
  const [input, setInput] = useState('');
  const assistantGreeting = (() => {
    switch (role) {
      case 'admin':
        return 'Bonjour. La supervision de la plateforme est prête.';
      case 'manager':
        return 'Bonjour. Les dossiers sensibles peuvent être repris.';
      case 'agent':
        return 'Bonjour. Les conversations en attente peuvent être rouvertes.';
      case 'partner':
        return 'Bonjour. Vos missions et vos échanges sont prêts.';
      case 'investor':
        return 'Bonjour. Vos opportunités sont prêtes.';
      default:
        return 'Bonjour. Décrivons ensemble votre nouveau projet.';
    }
  })();
  const [messages, setMessages] = useState<Array<{ id: string; role: 'user' | 'assistant'; text: string; details?: string[] }>>([
    {
      id: 'assistant-start',
      role: 'assistant',
      text: assistantGreeting,
      details: []
    }
  ]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>(() => (projects[0] ? String(projects[0].id) : ''));
  const [channel, setChannel] = useState<'web' | 'whatsapp' | 'telegram'>('web');
  const [sessionId, setSessionId] = useState<number | undefined>(undefined);
  const [assistantKey, setAssistantKey] = useState<string | undefined>(undefined);
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (selectedProjectId === '' && projects.length > 0) {
      setSelectedProjectId(String(projects[0].id));
    }
  }, [projects, selectedProjectId]);

  const selectedProject = projects.find((project) => String(project.id) === selectedProjectId) ?? projects[0] ?? null;

  const send = async () => {
    const trimmed = input.trim();
    if (!trimmed || isSending || !selectedProject) {
      return;
    }
    setIsSending(true);
    setMessages((current) => [...current, { id: `user-${Date.now()}`, role: 'user', text: trimmed }]);
    try {
      const selectedProjectIdNumber = Number(selectedProject.id);
      const response = await apiSdk.askAssistant({
        message: trimmed,
        project_id: Number.isFinite(selectedProjectIdNumber) ? selectedProjectIdNumber : undefined,
        session_id: sessionId,
        agent_key: assistantKey
      });
      const reply = response.data.reply || 'Je prends le relais.';
      setSessionId(response.data.session_id ?? sessionId);
      setAssistantKey(response.data.agent_key ?? assistantKey);
      setMessages((current) => [
        ...current,
        {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          text: reply,
          details: response.data.suggestions.length > 0 ? response.data.suggestions : ['Continuer']
        }
      ]);
      setInput('');
    } finally {
      setIsSending(false);
    }
  };

  const quickPrompts =
    role === 'admin'
      ? ['Ouvrir la supervision', 'Vérifier la sécurité', 'Consulter les performances', 'Lancer un contrôle']
      : role === 'manager'
        ? ['Voir les équipes', 'Ouvrir les dossiers bloqués', 'Suivre les délais', 'Relancer le dossier']
        : role === 'agent'
          ? ['Reprendre la conversation', 'Prendre rendez-vous', 'Voir les partenaires', 'Ajouter un document']
          : role === 'partner'
            ? ['Voir les missions', 'Partager une disponibilité', 'Ouvrir un échange', 'Mettre à jour mes horaires']
            : role === 'investor'
              ? ['Voir les opportunités', 'Comparer les biens', 'Ouvrir les échanges', 'Revoir le dossier']
              : ['Continuer le projet', 'Ajouter un document', 'Prendre rendez-vous', 'Découvrir un bien'];

  return (
    <Surface className="p-6 sm:p-7">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Conversation vivante</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-950">{selectedProject ? selectedProject.title : 'Nouvelle conversation'}</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          <Badge variant="info">{channel}</Badge>
          <ActionChip label="Web" tone={channel === 'web' ? 'primary' : 'secondary'} onClick={() => setChannel('web')} />
          <ActionChip label="WhatsApp" tone={channel === 'whatsapp' ? 'primary' : 'secondary'} onClick={() => setChannel('whatsapp')} />
          <ActionChip label="Telegram" tone={channel === 'telegram' ? 'primary' : 'secondary'} onClick={() => setChannel('telegram')} />
        </div>
      </div>
      <div className="mt-5 grid gap-4 xl:grid-cols-[0.78fr_1.22fr]">
        <div className="space-y-4">
          <Select
            tone="light"
            label="Projet"
            value={selectedProjectId}
            onChange={(event) => setSelectedProjectId(event.target.value)}
          >
            {(projects.length > 0 ? projects : [{ id: 'new', title: 'Nouveau dossier', status: 'Nouveau', objective: 'Créer une nouvelle conversation', location_city: undefined }]).map((project) => (
              <option key={project.id} value={project.id}>
                {project.title}
              </option>
            ))}
          </Select>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Contexte</p>
            <p className="mt-2 text-sm font-semibold text-slate-950">{selectedProject ? normalizeProjectTitle(selectedProject, 'Dossier projet') : role === 'user' ? 'Aucun projet actif' : 'Aucun dossier actif'}</p>
            <p className="mt-2 text-sm leading-6 text-slate-600">{selectedProject?.objective ?? 'La conversation garde l’historique, les décisions et les recommandations.'}</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Intentions rapides</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {quickPrompts.map((prompt) => (
                <ActionChip key={prompt} label={prompt} onClick={() => setInput(prompt)} />
              ))}
            </div>
          </div>
        </div>
        <div className="space-y-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Conversation</p>
            <div className="mt-4 space-y-3">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`max-w-[92%] rounded-3xl border px-4 py-3 text-sm leading-6 ${
                    message.role === 'user' ? 'ml-auto border-sky-200 bg-sky-50 text-slate-900' : 'border-slate-200 bg-white text-slate-700'
                  }`}
                >
                  {message.text}
                  {message.details && message.details.length > 0 ? (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {message.details.map((detail) => (
                        <Badge key={detail} variant={message.role === 'user' ? 'info' : 'success'}>
                          {detail}
                        </Badge>
                      ))}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
            <div className="mt-4 grid gap-3">
              <Textarea tone="light" label="Message" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Décrire la prochaine étape" />
              <div className="flex flex-wrap gap-3">
                <Button type="button" onClick={() => void send()} loading={isSending}>
                  Continuer
                </Button>
                <Button type="button" variant="secondary" onClick={() => setInput('')}>
                  Effacer
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Surface>
  );
}

export function ConversationStudioPage() {
  const { t } = useTranslator();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialProjectId = params.get('project') ?? '';
  const { projects, projectsPending, summary } = useProjectsSummary();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const activeProject = projects.find((project) => String(project.id) === initialProjectId) ?? projects[0] ?? null;

  if (projectsPending) {
    return <RoleCockpitPage />;
  }

  return (
    <Frame
      title="Conversation"
      subtitle="Le point d’entrée principal de LAWIM. Chaque échange garde le contexte, le dossier et la décision."
      backTo={{ label: t('cockpit.back_to_cockpit'), to: resolveDashboardPath(role) }}
    >
      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Surface className="p-6 sm:p-7">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Dossiers</p>
          <div className="mt-4 space-y-3">
            {projects.length > 0 ? (
              projects.map((project) => (
                <button
                  key={project.id}
                  type="button"
                  className={`w-full rounded-3xl border px-4 py-3 text-left transition ${
                    activeProject?.id === project.id ? 'border-slate-900 bg-slate-900 text-white' : 'border-slate-200 bg-slate-50 text-slate-900'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-semibold">{project.title}</span>
                    <Badge variant={activeProject?.id === project.id ? 'success' : 'info'}>{project.status}</Badge>
                  </div>
                  <p className="mt-2 text-sm leading-6 opacity-80">{project.objective}</p>
                </button>
              ))
            ) : (
              <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
                {summary.communications > 0 ? 'Aucun dossier chargé.' : 'Vous pouvez créer une nouvelle conversation.'}
              </div>
            )}
          </div>
        </Surface>
        <ConversationThreadCard role={role} projects={activeProject ? [activeProject] : []} />
      </div>
    </Frame>
  );
}

export function ProjectDossierPage() {
  const { t } = useTranslator();
  const params = useParams();
  const { projects } = useProjectsSummary();
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  const currentProject = projects.find((project) => String(project.id) === String(params.projectId ?? '')) ?? projects[0] ?? null;

  return (
    <Frame title="Dossier projet" subtitle="Les décisions, les documents, les partenaires et les échéances restent regroupés." backTo={{ label: t('cockpit.back_to_cockpit'), to: resolveDashboardPath(role) }}>
      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Surface className="p-6 sm:p-7">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Résumé</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">{currentProject?.title ?? 'Aucun dossier ouvert'}</h2>
          <p className="mt-3 text-sm leading-7 text-slate-600">{currentProject?.objective ?? 'Le dossier projet centralise la conversation et les décisions.'}</p>
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <StatPill label="État" value={currentProject?.status ?? 'En attente'} />
            <StatPill label="Budget" value={currentProject?.budget_max != null ? formatMoney(currentProject.budget_max) : 'À préciser'} />
            <StatPill label="Ville" value={currentProject?.location_city ?? '—'} />
          </div>
        </Surface>
        <Surface className="p-6 sm:p-7">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Décisions récentes</p>
          <div className="mt-4 space-y-3">
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">Projet conservé dans le même dossier.</div>
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">Conversation suspendue puis reprise sans perte de contexte.</div>
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">Documents et recommandations liés au même objectif.</div>
          </div>
        </Surface>
      </div>
    </Frame>
  );
}

export function PropertyJourneyPage() {
  const { t } = useTranslator();
  const [intent, setIntent] = useState('acheter');
  const [asset, setAsset] = useState('terrain');
  const [cityMode, setCityMode] = useState<'major' | 'other'>('major');
  const [majorCity, setMajorCity] = useState('Douala');
  const [region, setRegion] = useState('Centre');
  const [department, setDepartment] = useState('Mfoundi');
  const [manualCity, setManualCity] = useState('');
  const [quartier, setQuartier] = useState('Bonanjo');
  const [customQuartier, setCustomQuartier] = useState('');
  const [budgetMax, setBudgetMax] = useState('');
  const [surface, setSurface] = useState('');
  const [rooms, setRooms] = useState('');
  const [bathrooms, setBathrooms] = useState('');
  const [titleFoncier, setTitleFoncier] = useState(true);
  const [accessRoad, setAccessRoad] = useState(true);
  const [viabilisation, setViabilisation] = useState(false);
  const [garage, setGarage] = useState(false);
  const [kitchen, setKitchen] = useState(false);
  const [standing, setStanding] = useState('standard');
  const [summaryMessage, setSummaryMessage] = useState<string>('Répondez à la première question pour commencer.');

  const cityDefinition = getCurrentCityDefinition(majorCity);
  const resolvedCity = cityMode === 'major' ? cityDefinition.label : manualCity.trim();
  const resolvedRegion = cityMode === 'major' ? cityDefinition.region : region;
  const resolvedQuarter = cityMode === 'major' ? (quartier === 'Autre' ? customQuartier.trim() : quartier) : quartier;

  const matchQuery = useMemo<MatchQuery | undefined>(() => {
    if (!resolvedCity) return undefined;
    return {
      target_type: 'property',
      city: resolvedCity,
      region: resolvedRegion,
      country: 'Cameroon',
      property_type: asset === 'terrain' ? 'land' : asset === 'maison' ? 'house' : asset === 'appartement' ? 'apartment' : 'residence',
      budget_max: budgetMax ? Number(budgetMax) : undefined,
      limit: 2
    };
  }, [asset, budgetMax, resolvedCity, resolvedRegion]);

  const { data: matchesData } = useQuery({
    queryKey: ['property-journey-matches', matchQuery],
    queryFn: () => apiSdk.getMatches(matchQuery),
    enabled: Boolean(matchQuery)
  });

  const matches = matchesData?.data ?? [];

  const submitSummary = () => {
    const parts = [intent, asset, resolvedCity, resolvedRegion, resolvedQuarter].filter(Boolean);
    setSummaryMessage(`Projet ${parts.join(' · ')}.`);
  };

  type FeatureToggle = {
    label: string;
    checked: boolean;
    onToggle: () => void;
  };

  const featureChecklist: FeatureToggle[] =
    asset === 'terrain'
      ? [
          { label: 'Titre foncier', checked: titleFoncier, onToggle: () => setTitleFoncier((current) => !current) },
          { label: 'Accès', checked: accessRoad, onToggle: () => setAccessRoad((current) => !current) },
          { label: 'Viabilisation', checked: viabilisation, onToggle: () => setViabilisation((current) => !current) }
        ]
      : [
          { label: 'Garage', checked: garage, onToggle: () => setGarage((current) => !current) },
          { label: 'Cuisine', checked: kitchen, onToggle: () => setKitchen((current) => !current) },
          {
            label: 'Standing',
            checked: standing !== 'standard',
            onToggle: () =>
              setStanding((current) =>
                current === 'standard' ? 'moyen' : current === 'moyen' ? 'bon' : current === 'bon' ? 'haut' : 'standard'
              )
          }
        ];

  return (
    <Frame title="Biens" subtitle="Le point de départ est conversationnel. Les champs apparaissent seulement quand ils deviennent utiles." backTo={{ label: t('cockpit.back_to_cockpit'), to: resolveDashboardPath('user') }}>
      <div className="grid gap-6 xl:grid-cols-[1.02fr_0.98fr]">
        <Surface className="p-6 sm:p-7">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Conversation guidée</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Bonjour. Quel est votre projet aujourd’hui ?</h2>
          <div className="mt-6 grid gap-4">
            <Select tone="light" label="Intention" value={intent} onChange={(event) => setIntent(event.target.value)}>
              <option value="acheter">Acheter</option>
              <option value="louer">Louer</option>
              <option value="vendre">Vendre</option>
              <option value="construire">Construire</option>
              <option value="investir">Investir</option>
            </Select>
            <Select tone="light" label="Type de bien" value={asset} onChange={(event) => setAsset(event.target.value)}>
              <option value="terrain">Terrain</option>
              <option value="maison">Maison</option>
              <option value="appartement">Appartement</option>
              <option value="immeuble">Immeuble</option>
              <option value="local">Local commercial</option>
              <option value="autre">Autre</option>
            </Select>
            <div className="grid gap-4 md:grid-cols-2">
              <Select tone="light" label="Mode de localisation" value={cityMode} onChange={(event) => setCityMode(event.target.value === 'other' ? 'other' : 'major')}>
                <option value="major">Villes principales</option>
                <option value="other">Autre ville</option>
              </Select>
              {cityMode === 'major' ? (
                <Select tone="light" label="Ville" value={majorCity} onChange={(event) => setMajorCity(event.target.value)}>
                  {CAMEROON_MAJOR_CITIES.map((city) => (
                    <option key={city.value} value={city.value}>
                      {city.label}
                    </option>
                  ))}
                </Select>
              ) : (
                <Input tone="light" label="Ville" value={manualCity} onChange={(event) => setManualCity(event.target.value)} placeholder="Bafia, Kumba..." />
              )}
            </div>
            {cityMode === 'major' ? (
              <>
                <Select tone="light" label="Quartier" value={quartier} onChange={(event) => setQuartier(event.target.value)}>
                  {getCurrentCityDefinition(majorCity).quartiers.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </Select>
                {quartier === 'Autre' ? <Input tone="light" label="Quartier à préciser" value={customQuartier} onChange={(event) => setCustomQuartier(event.target.value)} /> : null}
              </>
            ) : (
              <>
                <Select tone="light" label="Région" value={region} onChange={(event) => setRegion(event.target.value)}>
                  {CAMEROON_REGIONS.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </Select>
                <Select tone="light" label="Département" value={department} onChange={(event) => setDepartment(event.target.value)}>
                  {resolveDepartmentOptions(region).map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </Select>
                <Input tone="light" label="Quartier" value={quartier} onChange={(event) => setQuartier(event.target.value)} />
              </>
            )}
            <div className="grid gap-4 md:grid-cols-2">
              <Input tone="light" label="Budget max" value={budgetMax} onChange={(event) => setBudgetMax(event.target.value)} placeholder="50000000" />
              <Input tone="light" label="Surface" value={surface} onChange={(event) => setSurface(event.target.value)} placeholder="120 m²" />
            </div>
            {asset === 'terrain' ? (
              <div className="grid gap-3 md:grid-cols-3">
                {featureChecklist.map((feature) => (
                  <button
                    key={feature.label}
                    type="button"
                    className={`rounded-2xl border px-4 py-3 text-left text-sm transition ${
                      feature.checked ? 'border-slate-900 bg-slate-900 text-white' : 'border-slate-200 bg-slate-50 text-slate-700'
                    }`}
                    onClick={feature.onToggle}
                  >
                    {feature.label}
                  </button>
                ))}
              </div>
            ) : (
              <div className="grid gap-3 md:grid-cols-3">
                <Input tone="light" label="Chambres" value={rooms} onChange={(event) => setRooms(event.target.value)} />
                <Input tone="light" label="Salles de bain" value={bathrooms} onChange={(event) => setBathrooms(event.target.value)} />
                <Select tone="light" label="Standing" value={standing} onChange={(event) => setStanding(event.target.value)}>
                  <option value="standard">Standard</option>
                  <option value="moyen">Moyen</option>
                  <option value="bon">Bon</option>
                  <option value="haut">Haut</option>
                </Select>
              </div>
            )}
            <div className="flex flex-wrap gap-3">
              <Button type="button" onClick={submitSummary}>
                Continuer
              </Button>
              <Button type="button" variant="secondary" onClick={() => setSummaryMessage('Répondez à la première question pour commencer.')}>
                Réinitialiser
              </Button>
            </div>
            <p className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700">{summaryMessage}</p>
          </div>
        </Surface>
        <div className="space-y-6">
          <Surface className="p-6 sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Recommandations</p>
            <h2 className="mt-3 text-2xl font-semibold text-slate-950">2 biens susceptibles de vous intéresser</h2>
            <div className="mt-5 space-y-3">
              {matches.length > 0 ? (
                matches.map((match, index) => (
                  <div key={index} className="rounded-3xl border border-slate-200 bg-white p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-base font-semibold text-slate-950">{match.property?.title ?? `Bien ${index + 1}`}</p>
                      <Badge variant="info">{match.eligible ? 'Pertinent' : 'À vérifier'}</Badge>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{match.summary}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.24em] text-slate-400">{match.reasons.join(' · ')}</p>
                  </div>
                ))
              ) : (
                <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
                  Les propositions apparaîtront lorsque la localisation et le budget seront suffisants.
                </div>
              )}
            </div>
          </Surface>
          <Surface className="p-6 sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">IA</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              LAWIM commence par comprendre votre projet, puis révèle seulement les champs utiles et les propositions pertinentes.
            </p>
          </Surface>
        </div>
      </div>
    </Frame>
  );
}

export function PartnerJourneyPage() {
  const { t } = useTranslator();
  const [need, setNeed] = useState('architecte');
  const [projectType, setProjectType] = useState('construction');
  const [city, setCity] = useState('Douala');
  const [budget, setBudget] = useState('');
  const [summary, setSummary] = useState('Décrivez le besoin pour voir les partenaires pertinents.');

  const matchQuery = useMemo<MatchQuery>(
    () => ({
      target_type: 'partner',
      city,
      country: 'Cameroon',
      partner_type: need,
      project_type: projectType,
      budget_max: budget ? Number(budget) : undefined,
      limit: 2
    }),
    [budget, city, need, projectType]
  );

  const { data: matchData } = useQuery({
    queryKey: ['partner-journey-matches', matchQuery],
    queryFn: () => apiSdk.getMatches(matchQuery)
  });

  const matches = matchData?.data ?? [];

  return (
    <Frame title="Partenaires" subtitle="La mise en relation apparaît seulement quand elle apporte de la valeur au projet." backTo={{ label: t('cockpit.back_to_cockpit'), to: resolveDashboardPath('agent') }}>
      <div className="grid gap-6 xl:grid-cols-[1.02fr_0.98fr]">
        <Surface className="p-6 sm:p-7">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Conversation guidée</p>
          <div className="mt-6 grid gap-4">
            <Select tone="light" label="Besoin" value={need} onChange={(event) => setNeed(event.target.value)}>
              <option value="architecte">Architecte</option>
              <option value="banque">Banque</option>
              <option value="notaire">Notaire</option>
              <option value="géomètre">Géomètre</option>
              <option value="artisan">Artisan</option>
              <option value="photographe">Photographe</option>
            </Select>
            <Select tone="light" label="Projet" value={projectType} onChange={(event) => setProjectType(event.target.value)}>
              <option value="construction">Construction</option>
              <option value="achat">Achat</option>
              <option value="location">Location</option>
              <option value="investissement">Investissement</option>
            </Select>
            <Input tone="light" label="Ville" value={city} onChange={(event) => setCity(event.target.value)} />
            <Input tone="light" label="Budget" value={budget} onChange={(event) => setBudget(event.target.value)} placeholder="75000000" />
            <Textarea tone="light" label="Contexte" value={summary} onChange={(event) => setSummary(event.target.value)} />
          </div>
        </Surface>
        <div className="space-y-6">
          <Surface className="p-6 sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Propositions</p>
            <h2 className="mt-3 text-2xl font-semibold text-slate-950">Un partenaire pourrait vous accompagner</h2>
            <div className="mt-5 space-y-3">
              {matches.length > 0 ? (
                matches.map((match, index) => (
                  <div key={index} className="rounded-3xl border border-slate-200 bg-white p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-semibold text-slate-950">
                        {match.partner != null && typeof match.partner === 'object' && 'display_name' in match.partner
                          ? String((match.partner as Record<string, unknown>).display_name ?? `Partenaire ${index + 1}`)
                          : `Partenaire ${index + 1}`}
                      </p>
                      <Badge variant="info">{match.eligible ? 'Pertinent' : 'À vérifier'}</Badge>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{match.summary}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.24em] text-slate-400">{match.reasons.join(' · ')}</p>
                  </div>
                ))
              ) : (
                <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
                  Les partenaires pertinents s’affichent quand le besoin est assez précis.
                </div>
              )}
            </div>
          </Surface>
          <Surface className="p-6 sm:p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">Pourquoi maintenant ?</p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              LAWIM n’ouvre la relation que lorsque le contexte du projet rend l’intervention utile.
            </p>
          </Surface>
        </div>
      </div>
    </Frame>
  );
}

export function HistoryPage() {
  const { t } = useTranslator();
  return (
    <Frame title="Historique" subtitle="Conversations, décisions et retours restent consultables sans alourdir le cockpit." backTo={{ label: t('cockpit.back_to_cockpit'), to: '/cockpit' }}>
      <Surface className="p-6 sm:p-7">
        <div className="space-y-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-950">Conversation du jour</p>
            <p className="mt-2 text-sm leading-6 text-slate-600">Reprise du dossier sans répéter les informations déjà validées.</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-950">Décision validée</p>
            <p className="mt-2 text-sm leading-6 text-slate-600">Le projet est suspendu puis repris exactement au bon endroit.</p>
          </div>
        </div>
      </Surface>
    </Frame>
  );
}

export function SearchSpacePage() {
  const { t } = useTranslator();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const query = params.get('q') ?? '';
  const [search, setSearch] = useState(query);
  const { data } = useQuery({
    queryKey: ['search-space', search],
    queryFn: () => apiSdk.getProperties({ search, page: 1, pageSize: 6 })
  });
  const items = data?.data ?? [];

  return (
    <Frame title="Biens" subtitle="Une recherche sobre, pensée pour reprendre un projet ou en démarrer un nouveau." backTo={{ label: t('cockpit.back_to_cockpit'), to: '/cockpit' }}>
      <Surface className="p-6 sm:p-7">
        <div className="grid gap-4 md:grid-cols-[1fr_auto]">
          <Input tone="light" label="Recherche" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Terrain à Yaoundé" />
          <div className="flex items-end">
            <Button type="button" onClick={() => setSearch((current) => current.trim())}>
              Rechercher
            </Button>
          </div>
        </div>
        <div className="mt-6 space-y-3">
          {items.length > 0 ? (
            items.map((item) => (
              <div key={item.id} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <p className="font-semibold text-slate-950">{item.title}</p>
                  <Badge variant="info">{item.type}</Badge>
                </div>
                <p className="mt-2 text-sm text-slate-600">{item.location}</p>
              </div>
            ))
          ) : (
            <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
              Aucun bien ne correspond à cette recherche.
            </div>
          )}
        </div>
      </Surface>
    </Frame>
  );
}

export function CockpitRedirectPage() {
  const user = useAuthStore((state) => state.user);
  const roles = useAuthStore((state) => state.roles);
  const role = missionRoleFromAccessRole(resolvePrimaryRole(user?.role, roles));
  return <Navigate to={resolveDashboardPath(role)} replace />;
}
