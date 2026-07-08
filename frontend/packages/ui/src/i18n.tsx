import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

export type Language = 'fr' | 'en' | 'pcm';

export const LANGUAGE_STORAGE_KEY = 'lawim.language';
export const SUPPORTED_LANGUAGES: readonly Language[] = ['fr', 'en', 'pcm'] as const;
export const DEFAULT_LANGUAGE: Language = 'fr';

const TRANSLATIONS = {
  fr: {
    'app.name': 'LAWIM_V2',
    'language.fr': 'Français',
    'language.en': 'Anglais',
    'language.pcm': 'Pidgin English',
    'nav.language': 'Langue',
    'nav.home': 'Accueil',
    'nav.search': 'Recherche',
    'nav.map': 'Carte',
    'nav.estimation': 'Estimation',
    'nav.assistant': 'Assistant',
    'nav.marketplace': 'Marketplace',
    'nav.contact': 'Nous écrire',
    'nav.login': 'Connexion',
    'nav.dashboard': 'Tableau de bord',
    'nav.profile': 'Profil',
    'auth.login.title': 'Connexion',
    'auth.login.subtitle': '',
    'auth.login.email': 'Email',
    'auth.login.password': 'Mot de passe',
    'auth.login.button': 'Connexion',
    'auth.login.forgot': 'Mot de passe oublié',
    'auth.login.create': 'Créer un compte',
    'auth.login.connecting': 'Connexion...',
    'auth.login.banner.success': 'Connexion réussie.',
    'auth.login.banner.invalid': 'Identifiants incorrects.',
    'auth.login.banner.rate_limited': 'Trop de tentatives. Réessayez plus tard.',
    'auth.login.banner.server_unavailable': 'Serveur indisponible. Réessayez dans un instant.',
    'auth.login.banner.session_expired': 'Votre session a expiré. Connectez-vous de nouveau.',
    'auth.login.banner.unauthorized': 'Connectez-vous pour accéder à votre espace.',
    'auth.login.banner.restore': 'Restauration de votre session et sélection du bon tableau de bord.',
    'auth.login.banner.note': '',
    'auth.contact.website': 'Site',
    'auth.contact.email': 'Email',
    'auth.contact.phone': 'Téléphone',
    'auth.contact.whatsapp': 'WhatsApp',
    'auth.contact.facebook': 'Facebook',
    'auth.logout': 'Déconnexion',
    'auth.session.restoring': 'Restauration de session',
    'errors.generic': 'Une erreur inattendue est survenue.',
    'errors.unavailable': 'Serveur indisponible. Réessayez dans un instant.',
    'success.saved': 'Enregistré.',
    'role.admin': 'Administrateur',
    'role.manager': 'Manager',
    'role.operator': 'Opérateur',
    'role.partner': 'Partenaire',
    'role.user': 'Utilisateur',
    'dashboard.title': 'Cockpit moderne',
    'dashboard.subtitle': 'Vue courte, claire et orientée action.',
    'dashboard.greeting': 'Bonjour {name}',
    'dashboard.identity': 'Vous êtes connecté en tant que {role}.',
    'dashboard.activity_today': 'Activité du jour',
    'dashboard.priorities': 'Priorités',
    'dashboard.quick_stats': 'Statistiques rapides',
    'dashboard.progress': 'Progression',
    'dashboard.whats_next': 'Et maintenant ?',
    'dashboard.quick_actions': 'Actions rapides',
    'dashboard.modules': 'Modules',
    'dashboard.module_hint': 'Chaque carte ouvre un espace dédié.',
    'dashboard.open_module': 'Ouvrir',
    'dashboard.return_dashboard': 'Retour au tableau de bord',
    'dashboard.today': 'Aujourd’hui',
    'dashboard.stats.properties': 'Biens',
    'dashboard.stats.opportunities': 'Opportunités',
    'dashboard.stats.messages': 'Messages',
    'dashboard.stats.tasks': 'Tâches',
    'dashboard.stats.progress': 'Progression',
    'module.properties.title': 'Biens',
    'module.properties.description': 'Biens, recherches et dossiers prioritaires.',
    'module.messages.title': 'Messages',
    'module.messages.description': 'Conversations, relances et réponses utiles.',
    'module.visits.title': 'Visites',
    'module.visits.description': 'Planning, rendez-vous et suivi des visites.',
    'module.statistics.title': 'Statistiques',
    'module.statistics.description': 'KPI, progression et indicateurs de pilotage.',
    'module.documents.title': 'Documents',
    'module.documents.description': 'Dossiers, pièces et documents à partager.',
    'module.partners.title': 'Partenaires',
    'module.partners.description': 'Matching transversal pour photographe, architecte, notaire, banque, artisan, diagnostiqueur et déménageur.',
    'module.contact.title': 'Nous écrire',
    'module.contact.description': 'Contacter l’équipe sans quitter le cockpit.',
    'module.admin.title': 'Administration',
    'module.admin.description': 'Supervision, gouvernance et contrôles avancés.',
    'module.back': 'Retour',
    'module.learn_more': 'En savoir plus',
    'module.detail.focus': 'Focus',
    'module.detail.action': 'Action',
    'module.detail.insight': 'Insight',
    'module.detail.next_step': 'Prochaine étape',
    'module.detail.summary': 'Résumé',
    'contact.title': 'Nous écrire',
    'contact.description': 'Écrivez à l’équipe en gardant le contexte du cockpit.',
    'contact.name': 'Nom',
    'contact.email': 'Email',
    'contact.message': 'Message',
    'contact.send': 'Envoyer',
    'contact.sent': 'Message prêt à envoyer.',
    'contact.placeholder': 'Comment pouvons-nous vous aider ?',
    'shared.back_to_dashboard': 'Retour au tableau de bord',
    'shared.logout': 'Déconnexion',
    'shared.avatar': 'Avatar',
    'shared.role': 'Rôle',
    'shared.user': 'Utilisateur connecté',
    'shared.language': 'Langue',
  },
  en: {
    'app.name': 'LAWIM_V2',
    'language.fr': 'French',
    'language.en': 'English',
    'language.pcm': 'Pidgin English',
    'nav.language': 'Language',
    'nav.home': 'Home',
    'nav.search': 'Search',
    'nav.map': 'Map',
    'nav.estimation': 'Estimation',
    'nav.assistant': 'Assistant',
    'nav.marketplace': 'Marketplace',
    'nav.contact': 'Contact us',
    'nav.login': 'Login',
    'nav.dashboard': 'Dashboard',
    'nav.profile': 'Profile',
    'auth.login.title': 'Login',
    'auth.login.subtitle': '',
    'auth.login.email': 'Email',
    'auth.login.password': 'Password',
    'auth.login.button': 'Login',
    'auth.login.forgot': 'Forgot password',
    'auth.login.create': 'Create account',
    'auth.login.connecting': 'Logging in...',
    'auth.login.banner.success': 'Login successful.',
    'auth.login.banner.invalid': 'Invalid credentials.',
    'auth.login.banner.rate_limited': 'Too many attempts. Try again later.',
    'auth.login.banner.server_unavailable': 'Server unavailable. Try again in a moment.',
    'auth.login.banner.session_expired': 'Your session expired. Please log in again.',
    'auth.login.banner.unauthorized': 'Log in to access your space.',
    'auth.login.banner.restore': 'Restoring your session and selecting the right dashboard.',
    'auth.login.banner.note': '',
    'auth.contact.website': 'Website',
    'auth.contact.email': 'Email',
    'auth.contact.phone': 'Phone',
    'auth.contact.whatsapp': 'WhatsApp',
    'auth.contact.facebook': 'Facebook',
    'auth.logout': 'Logout',
    'auth.session.restoring': 'Restoring session',
    'errors.generic': 'An unexpected error occurred.',
    'errors.unavailable': 'Server unavailable. Try again in a moment.',
    'success.saved': 'Saved.',
    'role.admin': 'Administrator',
    'role.manager': 'Manager',
    'role.operator': 'Operator',
    'role.partner': 'Partner',
    'role.user': 'User',
    'dashboard.title': 'Modern cockpit',
    'dashboard.subtitle': 'Short, clear and action-oriented.',
    'dashboard.greeting': 'Hello {name}',
    'dashboard.identity': 'You are signed in as {role}.',
    'dashboard.activity_today': 'Today’s activity',
    'dashboard.priorities': 'Priorities',
    'dashboard.quick_stats': 'Quick stats',
    'dashboard.progress': 'Progress',
    'dashboard.whats_next': 'What now?',
    'dashboard.quick_actions': 'Quick actions',
    'dashboard.modules': 'Modules',
    'dashboard.module_hint': 'Each card opens a dedicated space.',
    'dashboard.open_module': 'Open',
    'dashboard.return_dashboard': 'Back to dashboard',
    'dashboard.today': 'Today',
    'dashboard.stats.properties': 'Properties',
    'dashboard.stats.opportunities': 'Opportunities',
    'dashboard.stats.messages': 'Messages',
    'dashboard.stats.tasks': 'Tasks',
    'dashboard.stats.progress': 'Progress',
    'module.properties.title': 'Properties',
    'module.properties.description': 'Properties, searches and priority files.',
    'module.messages.title': 'Messages',
    'module.messages.description': 'Conversations, follow-ups and useful replies.',
    'module.visits.title': 'Visits',
    'module.visits.description': 'Planning, appointments and visit tracking.',
    'module.statistics.title': 'Statistics',
    'module.statistics.description': 'KPIs, progress and operating indicators.',
    'module.documents.title': 'Documents',
    'module.documents.description': 'Files, records and documents to share.',
    'module.partners.title': 'Partners',
    'module.partners.description': 'Transversal matching for photographers, architects, notaries, banks, artisans, diagnosticians and movers.',
    'module.contact.title': 'Contact us',
    'module.contact.description': 'Reach the team without leaving the cockpit.',
    'module.admin.title': 'Administration',
    'module.admin.description': 'Supervision, governance and advanced controls.',
    'module.back': 'Back',
    'module.learn_more': 'Learn more',
    'module.detail.focus': 'Focus',
    'module.detail.action': 'Action',
    'module.detail.insight': 'Insight',
    'module.detail.next_step': 'Next step',
    'module.detail.summary': 'Summary',
    'contact.title': 'Contact us',
    'contact.description': 'Write to the team while keeping cockpit context.',
    'contact.name': 'Name',
    'contact.email': 'Email',
    'contact.message': 'Message',
    'contact.send': 'Send',
    'contact.sent': 'Message ready to send.',
    'contact.placeholder': 'How can we help?',
    'shared.back_to_dashboard': 'Back to dashboard',
    'shared.logout': 'Logout',
    'shared.avatar': 'Avatar',
    'shared.role': 'Role',
    'shared.user': 'Signed-in user',
    'shared.language': 'Language',
  },
  pcm: {
    'app.name': 'LAWIM_V2',
    'language.fr': 'French',
    'language.en': 'English',
    'language.pcm': 'Pidgin English',
    'nav.language': 'Languag',
    'nav.home': 'Haus',
    'nav.search': 'Search',
    'nav.map': 'Map',
    'nav.estimation': 'Estimation',
    'nav.assistant': 'Assistant',
    'nav.marketplace': 'Marketplace',
    'nav.contact': 'Tok to we',
    'nav.login': 'Login',
    'nav.dashboard': 'Dashboard',
    'nav.profile': 'Profile',
    'auth.login.title': 'Login',
    'auth.login.subtitle': '',
    'auth.login.email': 'Email',
    'auth.login.password': 'Password',
    'auth.login.button': 'Login',
    'auth.login.forgot': 'Reset password',
    'auth.login.create': 'Create account',
    'auth.login.connecting': 'Dey login...',
    'auth.login.banner.success': 'Login don succeed.',
    'auth.login.banner.invalid': 'Login details no correct.',
    'auth.login.banner.rate_limited': 'Too much try. Try again later.',
    'auth.login.banner.server_unavailable': 'Server no dey. Try again in small time.',
    'auth.login.banner.session_expired': 'Your session don expire. Login again.',
    'auth.login.banner.unauthorized': 'Login make you fit enter your space.',
    'auth.login.banner.restore': 'We dey bring your session back and choose the right dashboard.',
    'auth.login.banner.note': '',
    'auth.contact.website': 'Website',
    'auth.contact.email': 'Email',
    'auth.contact.phone': 'Phone',
    'auth.contact.whatsapp': 'WhatsApp',
    'auth.contact.facebook': 'Facebook',
    'auth.logout': 'Comot',
    'auth.session.restoring': 'Dey bring session back',
    'errors.generic': 'Something unexpected don happen.',
    'errors.unavailable': 'Server no dey. Try again in small time.',
    'success.saved': 'Saved.',
    'role.admin': 'Boss',
    'role.manager': 'Manager',
    'role.operator': 'Operator',
    'role.partner': 'Partner',
    'role.user': 'User',
    'dashboard.title': 'Modern cockpit',
    'dashboard.subtitle': 'Short, clear, and ready for action.',
    'dashboard.greeting': 'How you dey {name}',
    'dashboard.identity': 'You dey signed in as {role}.',
    'dashboard.activity_today': 'Today work',
    'dashboard.priorities': 'Important things',
    'dashboard.quick_stats': 'Quick numbers',
    'dashboard.progress': 'Progress',
    'dashboard.whats_next': 'Wetin next?',
    'dashboard.quick_actions': 'Quick actions',
    'dashboard.modules': 'Modules',
    'dashboard.module_hint': 'Every card go open its own space.',
    'dashboard.open_module': 'Open',
    'dashboard.return_dashboard': 'Back to dashboard',
    'dashboard.today': 'Today',
    'dashboard.stats.properties': 'Properties',
    'dashboard.stats.opportunities': 'Opportunities',
    'dashboard.stats.messages': 'Messages',
    'dashboard.stats.tasks': 'Tasks',
    'dashboard.stats.progress': 'Progress',
    'module.properties.title': 'Properties',
    'module.properties.description': 'Properties, searches and priority files.',
    'module.messages.title': 'Messages',
    'module.messages.description': 'Talks, follow-ups and useful replies.',
    'module.visits.title': 'Visits',
    'module.visits.description': 'Planning, appointments and visit tracking.',
    'module.statistics.title': 'Statistics',
    'module.statistics.description': 'KPIs, progress and operating signals.',
    'module.documents.title': 'Documents',
    'module.documents.description': 'Files, records and things to share.',
    'module.partners.title': 'Partners',
    'module.partners.description': 'Matching for photographer, architect, notary, bank, artisan, diagnostician and mover.',
    'module.contact.title': 'Tok to we',
    'module.contact.description': 'Reach the team without leaving the cockpit.',
    'module.admin.title': 'Administration',
    'module.admin.description': 'Supervision, governance and strong controls.',
    'module.back': 'Back',
    'module.learn_more': 'Learn more',
    'module.detail.focus': 'Focus',
    'module.detail.action': 'Action',
    'module.detail.insight': 'Insight',
    'module.detail.next_step': 'Next step',
    'module.detail.summary': 'Summary',
    'contact.title': 'Tok to we',
    'contact.description': 'Write to the team while keeping cockpit context.',
    'contact.name': 'Name',
    'contact.email': 'Email',
    'contact.message': 'Message',
    'contact.send': 'Send',
    'contact.sent': 'Message ready to send.',
    'contact.placeholder': 'How we fit help you?',
    'shared.back_to_dashboard': 'Back to dashboard',
    'shared.logout': 'Comot',
    'shared.avatar': 'Avatar',
    'shared.role': 'Role',
    'shared.user': 'Signed-in user',
    'shared.language': 'Language',
  }
} as const;

type TranslationMap = (typeof TRANSLATIONS)[Language];
export type TranslationKey = keyof TranslationMap;

function normalizeLanguageCandidate(language: string | null | undefined): Language {
  const normalized = String(language ?? '').trim().toLowerCase().replace('_', '-');
  if (!normalized) {
    return DEFAULT_LANGUAGE;
  }
  if (normalized === 'pidgin') {
    return 'pcm';
  }
  const base = normalized.split('-', 1)[0];
  if ((SUPPORTED_LANGUAGES as readonly string[]).includes(base)) {
    return base as Language;
  }
  return DEFAULT_LANGUAGE;
}

export function getStoredLanguage(): Language {
  if (typeof window === 'undefined') {
    return DEFAULT_LANGUAGE;
  }
  return normalizeLanguageCandidate(window.localStorage.getItem(LANGUAGE_STORAGE_KEY));
}

export function setStoredLanguage(language: string) {
  const normalized = normalizeLanguageCandidate(language);
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, normalized);
    document.documentElement.lang = normalized;
    window.dispatchEvent(new Event('lawim-language-change'));
  }
  return normalized;
}

export function translate(key: TranslationKey | string, language?: string | null, params: Record<string, string | number> = {}) {
  const resolvedLanguage = normalizeLanguageCandidate(language ?? getStoredLanguage());
  const languageTable = TRANSLATIONS[resolvedLanguage];
  const fallbackTable = TRANSLATIONS[DEFAULT_LANGUAGE];
  const raw = (languageTable as Record<string, string>)[key] ?? fallbackTable[key as TranslationKey] ?? key;
  return raw.replace(/\{([a-zA-Z0-9_]+)\}/g, (_, placeholder: string) => {
    const value = params[placeholder];
    return value === undefined || value === null ? '' : String(value);
  });
}

type LanguageContextValue = {
  language: Language;
  setLanguage: (language: string) => void;
};

const LanguageContext = createContext<LanguageContextValue | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() => getStoredLanguage());

  useEffect(() => {
    setStoredLanguage(language);
  }, [language]);

  const value = useMemo(
    () => ({
      language,
      setLanguage: (next: string) => setLanguageState(normalizeLanguageCandidate(next))
    }),
    [language]
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context) {
    return context;
  }
  const language = getStoredLanguage();
  return {
    language,
    setLanguage: (next: string) => setStoredLanguage(next)
  };
}

export function LanguageSwitcher({ compact = false }: { compact?: boolean }) {
  const { language, setLanguage } = useLanguage();

  return (
    <label className={`flex items-center gap-3 ${compact ? 'text-xs' : 'text-sm'}`}>
      <span className={compact ? 'sr-only' : 'text-slate-400'}>{translate('nav.language', language)}</span>
      <select
        aria-label={translate('nav.language', language)}
        className={[
          'rounded-full border border-white/10 bg-slate-950/80 px-3 py-2 text-sm text-slate-100 outline-none transition',
          'focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20',
          compact ? 'min-w-[7.5rem]' : 'min-w-[9rem]'
        ].join(' ')}
        value={language}
        onChange={(event) => setLanguage(event.target.value)}
      >
        <option value="fr">{translate('language.fr', language)}</option>
        <option value="en">{translate('language.en', language)}</option>
        <option value="pcm">{translate('language.pcm', language)}</option>
      </select>
    </label>
  );
}

export function useTranslatedValue<T extends string>(key: TranslationKey, params?: Record<string, string | number>) {
  const { language } = useLanguage();
  return translate(key, language, params);
}
