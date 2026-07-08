const state = {
  token: localStorage.getItem("lawim.token") || "",
  bootstrap: null,
  health: null,
  activeJourney: localStorage.getItem("lawim.journey") || "user",
  activeModule: localStorage.getItem("lawim.module") || "dashboard",
  language: localStorage.getItem("lawim.language") || "fr",
  statsPeriod: localStorage.getItem("lawim.stats.period") || "today",
  selectedConversationId: null,
  selectedPropertyId: null,
  selectedPropertyVersion: null,
  selectedPropertyTitle: null,
  selectedProjectId: null,
  selectedSourceIntelligenceId: null,
  sourceIntelligenceDashboard: null,
  assistantSessionId: null,
  refreshInFlight: false,
};

const refs = {};
const moneyFormatter = new Intl.NumberFormat("fr-FR", {
  maximumFractionDigits: 0,
});
const ACCESS_ROLE_PRIORITY = ["admin", "manager", "operator", "partner", "user"];
const ROLE_LABELS = {
  admin: "Administrateur LAWIM",
  manager: "Manager",
  operator: "Opérateur LAWIM",
  partner: "Partenaire",
  user: "Utilisateur",
};
const ROLE_EMOJIS = {
  admin: "🛡️",
  manager: "📋",
  operator: "⚙️",
  partner: "🤝",
  user: "🏠",
};
const ROLE_JOURNEY_KEYS = {
  admin: ["admin", "project", "buyer", "seller"],
  manager: ["project", "buyer"],
  operator: ["seller", "project"],
  partner: ["project", "buyer"],
  user: ["buyer", "project"],
};
const ROLE_ALIASES = {
  admin: "admin",
  administrator: "admin",
  superadmin: "admin",
  director: "admin",
  root: "admin",
  manager: "manager",
  supervisor: "manager",
  lead: "manager",
  coordinator: "manager",
  operator: "operator",
  agent: "operator",
  staff: "operator",
  support: "operator",
  moderator: "operator",
  partner: "partner",
  photographer: "partner",
  notary: "partner",
  bank: "partner",
  artisan: "partner",
  architect: "partner",
  diagnostician: "partner",
  decorator: "partner",
  mover: "partner",
  broker: "partner",
  user: "user",
  owner: "user",
  buyer: "user",
  seller: "user",
  tenant: "user",
  landlord: "user",
  investor: "user",
  promoter: "user",
  customer: "user",
  viewer: "user",
  company: "user",
  enterprise: "user",
  business: "user",
  particulier: "user",
  private: "user",
  requester: "user",
};

const UI_COPY = {
  fr: {
    welcome: "Bonjour",
    loginTitle: "Connexion",
    loginLead: "",
    brandTagline: "L’immobilier autrement",
    authNote: "",
    secureAccess: "Accès sécurisé",
    authenticated: "Déconnexion",
    languageLabel: "Langue",
    modules: "Modules",
    dashboard: "Tableau de bord",
    moduleDeck: "Espaces dédiés",
    moduleDeckLead: "Choisissez un espace dédié pour ouvrir le bon module.",
    backToDashboard: "Retour au dashboard",
    openModule: "Ouvrir",
    loginEmail: "Email",
    loginPassword: "Mot de passe",
    loginForgot: "Mot de passe oublié",
    loginCreate: "Créer un compte",
    contactWebsite: "Site",
    contactEmail: "Email",
    contactPhone: "Téléphone",
    contactWhatsApp: "WhatsApp",
    contactFacebook: "Facebook",
    activity: "Activité du jour",
    priorities: "Mes priorités",
    quickActions: "Mes actions rapides",
    statistics: "Mes statistiques",
    recommendations: "Recommandations IA",
    next: "Et maintenant ?",
    support: "Nous écrire",
    session: "Session invitée",
    selectRole: "Cockpit sélectionné",
    supportHint: "Suggestion, support, réclamation, signalement, partenariat ou autre demande.",
    cockpitLeads: [
      "Étape actuelle, documents manquants et prochaine action.",
      "Les signaux les plus utiles de la journée.",
      "Ce qui mérite votre attention maintenant.",
      "Des raccourcis utiles pour avancer plus vite.",
      "Indicateurs sobres et lisibles.",
      "Suggestions contextuelles et discrètes.",
      "Les prochaines étapes les plus pertinentes.",
      "Suggestion, support, réclamation ou partenariat.",
    ],
  },
  en: {
    welcome: "Hello",
    loginTitle: "Login",
    loginLead: "",
    brandTagline: "L’immobilier autrement",
    authNote: "",
    secureAccess: "Secure access",
    authenticated: "Sign out",
    languageLabel: "Language",
    modules: "Modules",
    dashboard: "Dashboard",
    moduleDeck: "Dedicated spaces",
    moduleDeckLead: "Choose a dedicated space to open the right module.",
    backToDashboard: "Back to dashboard",
    openModule: "Open",
    loginEmail: "Email",
    loginPassword: "Password",
    loginForgot: "Forgot password",
    loginCreate: "Create account",
    contactWebsite: "Website",
    contactEmail: "Email",
    contactPhone: "Phone",
    contactWhatsApp: "WhatsApp",
    contactFacebook: "Facebook",
    activity: "Today's activity",
    priorities: "My priorities",
    quickActions: "Quick actions",
    statistics: "My statistics",
    recommendations: "AI recommendations",
    next: "What next?",
    support: "Write to us",
    session: "Guest session",
    selectRole: "Cockpit selected",
    supportHint: "Suggestion, support, complaint, report, partnership or other request.",
    cockpitLeads: [
      "Current step, missing documents and next action.",
      "The most useful signals of the day.",
      "What deserves your attention now.",
      "Useful shortcuts to move faster.",
      "Clear, sober indicators.",
      "Contextual and discreet suggestions.",
      "The most relevant next steps.",
      "Suggestion, support, complaint or partnership.",
    ],
  },
  pidgin: {
    welcome: "Hallo",
    loginTitle: "Login",
    loginLead: "",
    brandTagline: "L’immobilier autrement",
    authNote: "",
    secureAccess: "Secure access",
    authenticated: "Comot",
    languageLabel: "Languag",
    modules: "Modules",
    dashboard: "Dashboard",
    moduleDeck: "Dedicated spaces",
    moduleDeckLead: "Choose one dedicated space to open the right module.",
    backToDashboard: "Go back dashboard",
    openModule: "Open",
    loginEmail: "Email",
    loginPassword: "Password",
    loginForgot: "Reset password",
    loginCreate: "Create account",
    contactWebsite: "Website",
    contactEmail: "Email",
    contactPhone: "Phone",
    contactWhatsApp: "WhatsApp",
    contactFacebook: "Facebook",
    activity: "Today activity",
    priorities: "My priorities",
    quickActions: "Quick actions",
    statistics: "My stats",
    recommendations: "AI recommendations",
    next: "Wetin next?",
    support: "Write us",
    session: "Guest session",
    selectRole: "Cockpit selected",
    supportHint: "Suggestion, support, complaint, report, partnership or other request.",
    cockpitLeads: [
      "Current step, missing document, and next action.",
      "The most useful signals for today.",
      "Wetin need your attention now.",
      "Small shortcuts to move faster.",
      "Clear and simple indicators.",
      "Contextual and quiet suggestions.",
      "The next best steps.",
      "Suggestion, support, complaint, or partnership.",
    ],
  },
};

const SUMMARY_COPY = {
  fr: {
    organizations: "🏢 Organisations",
    users: "👥 Utilisateurs",
    properties: "🏠 Biens publiés",
    conversations: "💬 Conversations",
    messages: "✉️ Messages",
    notifications: "🔔 Notifications",
    media: "🖼 Médias",
    projects: "🚧 Projets",
  },
  en: {
    organizations: "🏢 Organizations",
    users: "👥 Users",
    properties: "🏠 Properties published",
    conversations: "💬 Conversations",
    messages: "✉️ Messages",
    notifications: "🔔 Notifications",
    media: "🖼 Media",
    projects: "🚧 Projects",
  },
  pidgin: {
    organizations: "🏢 Organizations",
    users: "👥 Users",
    properties: "🏠 Bens",
    conversations: "💬 Conversations",
    messages: "✉️ Messages",
    notifications: "🔔 Notifications",
    media: "🖼 Media",
    projects: "🚧 Projects",
  },
};

const STATS_PERIOD_COPY = {
  fr: {
    today: "Aujourd'hui",
    "7d": "7 jours",
    "30d": "30 jours",
    year: "Année",
    custom: "Période personnalisée",
    activePeriod: "Période active",
  },
  en: {
    today: "Today",
    "7d": "7 days",
    "30d": "30 days",
    year: "Year",
    custom: "Custom period",
    activePeriod: "Active period",
  },
  pidgin: {
    today: "Today",
    "7d": "7 days",
    "30d": "30 days",
    year: "Year",
    custom: "Custom period",
    activePeriod: "Active period",
  },
};

const RUNTIME_COPY = {
  fr: {
    refreshing: "Actualisation de l'environnement...",
    ready: "Environnement prêt.",
  },
  en: {
    refreshing: "Refreshing the environment...",
    ready: "Environment ready.",
  },
  pidgin: {
    refreshing: "Refreshing the environment...",
    ready: "Environment ready.",
  },
};

const NOTICE_COPY = {
  loginSuccess: {
    fr: (identity) => `Connexion réussie pour ${identity}.`,
    en: (identity) => `Signed in as ${identity}.`,
    pidgin: (identity) => `Login don succeed for ${identity}.`,
  },
  logout: {
    fr: "Session fermée.",
    en: "Session closed.",
    pidgin: "Session don close.",
  },
  projectCreateAuth: {
    fr: "Connectez-vous pour créer un projet.",
    en: "Sign in to create a project.",
    pidgin: "Sign in first to create project.",
  },
  projectCreated: {
    fr: "Projet créé.",
    en: "Project created.",
    pidgin: "Project created.",
  },
  matchReturned: {
    fr: (count, score) => `Retour de ${count} matchs classés (score min ${score}).`,
    en: (count, score) => `Returned ${count} ranked matches (min score ${score}).`,
    pidgin: (count, score) => `Returned ${count} ranked matches (min score ${score}).`,
  },
  recordsAuth: {
    fr: "Authentifiez-vous avant de créer des enregistrements.",
    en: "Authenticate before creating records.",
    pidgin: "Authenticate before creating records.",
  },
  propertyCreated: {
    fr: "Bien créé et enregistré.",
    en: "Property created and saved.",
    pidgin: "Property created and saved.",
  },
  geoLookup: {
    fr: "Géocodage terminé.",
    en: "Geo lookup completed.",
    pidgin: "Geo lookup completed.",
  },
  mediaAuth: {
    fr: "Authentifiez-vous avant de téléverser des médias.",
    en: "Authenticate before uploading media.",
    pidgin: "Authenticate before uploading media.",
  },
  mediaUploaded: {
    fr: "Média téléversé.",
    en: "Media uploaded.",
    pidgin: "Media uploaded.",
  },
  conversationAuth: {
    fr: "Sélectionnez une conversation puis authentifiez-vous.",
    en: "Select a conversation and authenticate first.",
    pidgin: "Select a conversation and authenticate first.",
  },
  replySent: {
    fr: "Réponse envoyée.",
    en: "Reply sent.",
    pidgin: "Reply sent.",
  },
  registerSuccess: {
    fr: (email) => `Compte créé pour ${email}.`,
    en: (email) => `Registered as ${email}.`,
    pidgin: (email) => `Registered as ${email}.`,
  },
  propertySearchFound: {
    fr: (count) => `${count} annonces trouvées.`,
    en: (count) => `Found ${count} listings.`,
    pidgin: (count) => `Found ${count} listings.`,
  },
  propertyPublishAuth: {
    fr: "Sélectionnez un bien puis authentifiez-vous.",
    en: "Select a property and authenticate first.",
    pidgin: "Select a property and authenticate first.",
  },
  propertyPublished: {
    fr: "Bien publié.",
    en: "Property published.",
    pidgin: "Property published.",
  },
  propertyArchived: {
    fr: "Bien archivé.",
    en: "Property archived.",
    pidgin: "Property archived.",
  },
  conversationOpened: {
    fr: "Conversation ouverte.",
    en: "Conversation opened.",
    pidgin: "Conversation opened.",
  },
  conversationSelect: {
    fr: "Sélectionnez d'abord une conversation.",
    en: "Select a conversation first.",
    pidgin: "Select a conversation first.",
  },
  negotiationUpdated: {
    fr: (stage) => `Étape de négociation mise à jour: ${stage}.`,
    en: (stage) => `Negotiation stage updated to ${stage}.`,
    pidgin: (stage) => `Negotiation stage updated to ${stage}.`,
  },
  notificationsFiltered: {
    fr: "Filtre de notifications appliqué.",
    en: "Notification filter applied.",
    pidgin: "Notification filter applied.",
  },
  adminAuth: {
    fr: "Authentifiez-vous comme administrateur d'abord.",
    en: "Authenticate as admin first.",
    pidgin: "Authenticate as admin first.",
  },
  organizationCreated: {
    fr: "Organisation créée.",
    en: "Organization created.",
    pidgin: "Organization created.",
  },
  staffCreated: {
    fr: "Compte collaborateur créé.",
    en: "Staff user created.",
    pidgin: "Staff user created.",
  },
};

const SYSTEM_COPY = {
  fr: {
    selectSourceFirst: "Sélectionnez une source d'abord.",
    sourceSelected: (name) => `Source sélectionnée : ${name}.`,
    noSourceRecords: "Aucun enregistrement d'intelligence des sources.",
    select: "Sélectionner",
    sourceLabel: "Source",
    whatsappLink: "Lien WhatsApp",
    referenceCode: "Code de référence",
    sieImportCompleted: "Import SIE terminé.",
    sourceContextUpdated: "Contexte source mis à jour.",
    sourceAnalysisCompleted: "Analyse source terminée.",
    whatsappLinkGenerated: "Lien WhatsApp généré.",
    referenceCodeGenerated: "Code de référence généré.",
    registrationMissingToken: "La réponse d'inscription n'inclut pas de jeton.",
    invalidJsonResponse: (path) => `Réponse JSON invalide depuis ${path}`,
  },
  en: {
    selectSourceFirst: "Select a source first.",
    sourceSelected: (name) => `Selected source: ${name}.`,
    noSourceRecords: "No source intelligence records yet.",
    select: "Select",
    sourceLabel: "Source",
    whatsappLink: "WhatsApp link",
    referenceCode: "Reference code",
    sieImportCompleted: "SIE import completed.",
    sourceContextUpdated: "Source context updated.",
    sourceAnalysisCompleted: "Source analysis completed.",
    whatsappLinkGenerated: "WhatsApp link generated.",
    referenceCodeGenerated: "Reference code generated.",
    registrationMissingToken: "The registration response did not include a token.",
    invalidJsonResponse: (path) => `Invalid JSON response from ${path}`,
  },
  pidgin: {
    selectSourceFirst: "Select source first.",
    sourceSelected: (name) => `Source selected: ${name}.`,
    noSourceRecords: "No source intelligence records yet.",
    select: "Select",
    sourceLabel: "Source",
    whatsappLink: "WhatsApp link",
    referenceCode: "Reference code",
    sieImportCompleted: "SIE import complete.",
    sourceContextUpdated: "Source context updated.",
    sourceAnalysisCompleted: "Source analysis complete.",
    whatsappLinkGenerated: "WhatsApp link generated.",
    referenceCodeGenerated: "Reference code generated.",
    registrationMissingToken: "Registration response no get token.",
    invalidJsonResponse: (path) => `Invalid JSON response from ${path}`,
  },
};

function noticeCopy(key, ...args) {
  const entry = NOTICE_COPY[key];
  if (!entry) {
    return "";
  }
  const value = entry[state.language] || entry.fr || entry.en || entry.pcm;
  return typeof value === "function" ? value(...args) : value;
}

function systemCopy(key, ...args) {
  const entry = SYSTEM_COPY[state.language] || SYSTEM_COPY.fr;
  const value = entry[key] || SYSTEM_COPY.fr[key] || SYSTEM_COPY.en[key] || "";
  return typeof value === "function" ? value(...args) : value;
}

function translateStatsPeriodSelect() {
  if (!refs.statsPeriodSelect) {
    return;
  }
  const copy = STATS_PERIOD_COPY[state.language] || STATS_PERIOD_COPY.fr;
  const labels = {
    today: copy.today,
    "7d": copy["7d"],
    "30d": copy["30d"],
    year: copy.year,
    custom: copy.custom,
  };
  Array.from(refs.statsPeriodSelect.options || []).forEach((option) => {
    if (labels[option.value]) {
      option.textContent = labels[option.value];
    }
  });
}

const MODULE_DEFS = {
  dashboard: {
    icon: "🏠",
    label: { fr: "Tableau de bord", en: "Dashboard", pidgin: "Dashboard" },
    description: {
      fr: "Vue courte, priorités et actions rapides.",
      en: "Short overview, priorities and quick actions.",
      pidgin: "Small view, top priorities and quick actions.",
    },
    panelGroups: [],
    cardGroups: [],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  biens: {
    icon: "🏘️",
    label: { fr: "Biens", en: "Properties", pidgin: "Bens" },
    description: {
      fr: "Créer, chercher, publier et suivre les biens.",
      en: "Create, search, publish and track properties.",
      pidgin: "Create, search, publish and follow di bens.",
    },
    panelGroups: ["biens"],
    cardGroups: ["biens"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  messages: {
    icon: "💬",
    label: { fr: "Messages", en: "Messages", pidgin: "Messages" },
    description: {
      fr: "Conversations, notifications et suivi relationnel.",
      en: "Conversations, notifications and relationship tracking.",
      pidgin: "Talks, notifications and follow-up.",
    },
    panelGroups: ["messages"],
    cardGroups: ["messages"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  visites: {
    icon: "🗓️",
    label: { fr: "Visites", en: "Visits", pidgin: "Visits" },
    description: {
      fr: "Parcours projet, rendez-vous et étapes de visite.",
      en: "Project path, appointments and visit steps.",
      pidgin: "Project route, appointments and visit steps.",
    },
    panelGroups: ["projet", "messages"],
    cardGroups: ["projet", "messages"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  statistiques: {
    icon: "📊",
    label: { fr: "Statistiques", en: "Statistics", pidgin: "Stats" },
    description: {
      fr: "Vue analytique, supervision et suivi.",
      en: "Analytics, supervision and follow-up.",
      pidgin: "Numbers, watch and follow-up.",
    },
    panelGroups: ["statistiques", "administration"],
    cardGroups: ["statistiques", "administration"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  documents: {
    icon: "📚",
    label: { fr: "Documents", en: "Documents", pidgin: "Documents" },
    description: {
      fr: "Connaissance, sources et intelligence documentaire.",
      en: "Knowledge, sources and document intelligence.",
      pidgin: "Knowledge, sources and document work.",
    },
    panelGroups: ["documents"],
    cardGroups: ["documents"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  partenaires: {
    icon: "🤝",
    label: { fr: "Partenaires", en: "Partners", pidgin: "Partners" },
    description: {
      fr: "Marketplace, prestataires et écosystème.",
      en: "Marketplace, providers and ecosystem.",
      pidgin: "Marketplace, service people and ecosystem.",
    },
    panelGroups: ["partenaires"],
    cardGroups: ["partenaires"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  contact: {
    icon: "✉️",
    label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" },
    description: {
      fr: "Demande, signalement ou partenariat.",
      en: "Request, report or partnership.",
      pidgin: "Send request, report, or partnership.",
    },
    panelGroups: ["messages"],
    cardGroups: ["messages"],
    roles: ["admin", "manager", "operator", "partner", "user"],
  },
  administration: {
    icon: "🛡️",
    label: { fr: "Administration", en: "Administration", pidgin: "Administration" },
    description: {
      fr: "Paramètres, comptes et supervision interne.",
      en: "Settings, accounts and internal supervision.",
      pidgin: "Settings, accounts and inside supervision.",
    },
    panelGroups: ["administration"],
    cardGroups: ["administration"],
    roles: ["admin"],
  },
};

const ROLE_COCKPIT_CONFIG = {
  admin: {
    subtitle: {
      fr: "Supervision complète de la plateforme et des releases.",
      en: "Full platform and release supervision.",
      pidgin: "Full platform and release control.",
    },
    activity: {
      fr: ["Suivi des utilisateurs", "Santé du runtime", "Préparation des releases"],
      en: ["User tracking", "Runtime health", "Release preparation"],
      pidgin: ["Track users", "Watch runtime health", "Prepare release"],
    },
    priorities: {
      fr: ["Vérifier les accès", "Surveiller les métriques", "Piloter les comptes internes"],
      en: ["Review access", "Watch metrics", "Manage internal accounts"],
      pidgin: ["Check access", "Watch metrics", "Manage inside accounts"],
    },
    quickActions: [
      { label: { fr: "Créer une organisation", en: "Create an organization", pidgin: "Create organization" }, href: "#admin-org-form" },
      { label: { fr: "Créer un utilisateur", en: "Create a user", pidgin: "Create user" }, href: "#admin-user-form" },
      { label: { fr: "Ouvrir les métriques", en: "Open metrics", pidgin: "Open metrics" }, href: "#admin-dashboard" },
      { label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" }, href: "#message-form" },
    ],
    recommendations: {
      fr: ["Sécuriser les accès sensibles", "Contrôler les validations en attente", "Préparer le prochain déploiement"],
      en: ["Secure sensitive access", "Review pending approvals", "Prepare the next deployment"],
      pidgin: ["Secure sensitive access", "Review pending approvals", "Prepare the next deployment"],
    },
    nextActions: {
      fr: ["Planifier la revue opérationnelle", "Ouvrir les alertes prioritaires", "Valider les nouveaux comptes"],
      en: ["Plan the operational review", "Open priority alerts", "Validate new accounts"],
      pidgin: ["Plan the operational review", "Open priority alerts", "Validate new accounts"],
    },
    support: {
      fr: ["Suggestion", "Support", "Réclamation", "Signalement", "Partenariat", "Autre demande"],
      en: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
      pidgin: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
    },
  },
  manager: {
    subtitle: {
      fr: "Pilotage opérationnel, équipes et priorités du jour.",
      en: "Operational steering, teams and daily priorities.",
      pidgin: "Operational steering, teams and daily priorities.",
    },
    activity: {
      fr: ["Suivi des projets", "Validation des dossiers", "Communication d'équipe"],
      en: ["Project tracking", "Case validation", "Team communication"],
      pidgin: ["Project tracking", "Case validation", "Team communication"],
    },
    priorities: {
      fr: ["Relancer les dossiers bloqués", "Valider les étapes critiques", "Répartir les actions rapides"],
      en: ["Follow up blocked files", "Approve critical steps", "Distribute quick actions"],
      pidgin: ["Follow up blocked files", "Approve critical steps", "Distribute quick actions"],
    },
    quickActions: [
      { label: { fr: "Voir les projets", en: "View projects", pidgin: "View projects" }, href: "#projects-list" },
      { label: { fr: "Suivre les conversations", en: "Track conversations", pidgin: "Track conversations" }, href: "#conversations-list" },
      { label: { fr: "Consulter les statistiques", en: "View statistics", pidgin: "View statistics" }, href: "#status-strip" },
      { label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" }, href: "#message-form" },
    ],
    recommendations: {
      fr: ["Clarifier les étapes en retard", "Réduire les points de friction", "Renforcer les validations utiles"],
      en: ["Clarify delayed steps", "Reduce friction points", "Strengthen useful approvals"],
      pidgin: ["Clarify delayed steps", "Reduce friction points", "Strengthen useful approvals"],
    },
    nextActions: {
      fr: ["Rattraper les dossiers en cours", "Prioriser les validations", "Ouvrir le suivi des notifications"],
      en: ["Catch up on active files", "Prioritize approvals", "Open notification tracking"],
      pidgin: ["Catch up on active files", "Prioritize approvals", "Open notification tracking"],
    },
    support: {
      fr: ["Suggestion", "Support", "Réclamation", "Signalement", "Partenariat", "Autre demande"],
      en: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
      pidgin: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
    },
  },
  operator: {
    subtitle: {
      fr: "Gestion quotidienne, support et contrôle qualité.",
      en: "Daily operations, support and quality control.",
      pidgin: "Daily operations, support and quality control.",
    },
    activity: {
      fr: ["Biens à vérifier", "Photos et médias", "Messages en attente"],
      en: ["Listings to review", "Photos and media", "Pending messages"],
      pidgin: ["Listings to review", "Photos and media", "Pending messages"],
    },
    priorities: {
      fr: ["Contrôler les publications", "Mettre à jour les médias", "Répondre aux demandes"],
      en: ["Check publications", "Update media", "Reply to requests"],
      pidgin: ["Check publications", "Update media", "Reply to requests"],
    },
    quickActions: [
      { label: { fr: "Créer un bien", en: "Create a property", pidgin: "Create property" }, href: "#property-form" },
      { label: { fr: "Géolocaliser", en: "Geolocate", pidgin: "Geolocate" }, href: "#geo-form" },
      { label: { fr: "Téléverser des médias", en: "Upload media", pidgin: "Upload media" }, href: "#media-upload-form" },
      { label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" }, href: "#message-form" },
    ],
    recommendations: {
      fr: ["Améliorer la qualité des annonces", "Vérifier les doublons de médias", "Traiter les retours clients"],
      en: ["Improve listing quality", "Check duplicate media", "Handle customer feedback"],
      pidgin: ["Improve listing quality", "Check duplicate media", "Handle customer feedback"],
    },
    nextActions: {
      fr: ["Publier un bien prêt", "Relancer un dossier", "Ouvrir le fil de conversation"],
      en: ["Publish a ready listing", "Follow up a file", "Open the conversation thread"],
      pidgin: ["Publish a ready listing", "Follow up a file", "Open the conversation thread"],
    },
    support: {
      fr: ["Suggestion", "Support", "Réclamation", "Signalement", "Partenariat", "Autre demande"],
      en: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
      pidgin: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
    },
  },
  partner: {
    subtitle: {
      fr: "Missions, rendez-vous et échanges liés à votre spécialité.",
      en: "Assignments, meetings and specialty-related exchanges.",
      pidgin: "Assignments, meetings and specialty-related exchanges.",
    },
    activity: {
      fr: ["Missions en cours", "Rendez-vous", "Documents partagés"],
      en: ["Active assignments", "Meetings", "Shared documents"],
      pidgin: ["Active assignments", "Meetings", "Shared documents"],
    },
    priorities: {
      fr: ["Confirmer les disponibilités", "Préparer les livrables", "Répondre aux sollicitations"],
      en: ["Confirm availability", "Prepare deliverables", "Reply to requests"],
      pidgin: ["Confirm availability", "Prepare deliverables", "Reply to requests"],
    },
    quickActions: [
      { label: { fr: "Voir les opportunités", en: "View opportunities", pidgin: "View opportunities" }, href: "#matches-list" },
      { label: { fr: "Consulter les partenaires", en: "View partners", pidgin: "View partners" }, href: "#partners-list" },
      { label: { fr: "Relire les biens", en: "Review listings", pidgin: "Review listings" }, href: "#properties-list" },
      { label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" }, href: "#message-form" },
    ],
    recommendations: {
      fr: ["Proposer une offre plus lisible", "Documenter les livrables", "Raccourcir le délai de réponse"],
      en: ["Offer clearer packages", "Document deliverables", "Shorten response time"],
      pidgin: ["Offer clearer packages", "Document deliverables", "Shorten response time"],
    },
    nextActions: {
      fr: ["Préparer le prochain rendez-vous", "Relancer une mission", "Ouvrir les messages"],
      en: ["Prepare the next meeting", "Follow up an assignment", "Open messages"],
      pidgin: ["Prepare the next meeting", "Follow up an assignment", "Open messages"],
    },
    support: {
      fr: ["Suggestion", "Support", "Réclamation", "Signalement", "Partenariat", "Autre demande"],
      en: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
      pidgin: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
    },
  },
  user: {
    subtitle: {
      fr: "Votre projet immobilier, vos priorités et les prochaines étapes.",
      en: "Your property project, your priorities and next steps.",
      pidgin: "Your property project, your priorities and next steps.",
    },
    activity: {
      fr: ["Recherche en cours", "Visites prévues", "Documents à compléter"],
      en: ["Active search", "Planned visits", "Documents to complete"],
      pidgin: ["Active search", "Planned visits", "Documents to complete"],
    },
    priorities: {
      fr: ["Comparer les biens", "Préparer les documents", "Suivre les notifications"],
      en: ["Compare listings", "Prepare documents", "Track notifications"],
      pidgin: ["Compare listings", "Prepare documents", "Track notifications"],
    },
    quickActions: [
      { label: { fr: "Rechercher un bien", en: "Search a property", pidgin: "Search property" }, href: "#property-search-form" },
      { label: { fr: "Créer un projet", en: "Create a project", pidgin: "Create project" }, href: "#project-form" },
      { label: { fr: "Démarrer une conversation", en: "Start a conversation", pidgin: "Start a conversation" }, href: "#buyer-conversation-form" },
      { label: { fr: "Nous écrire", en: "Write to us", pidgin: "Write us" }, href: "#message-form" },
    ],
    recommendations: {
      fr: ["Activer les favoris utiles", "Planifier les visites", "Finaliser le dossier"],
      en: ["Save useful listings", "Schedule visits", "Finalize the file"],
      pidgin: ["Save useful listings", "Schedule visits", "Finalize the file"],
    },
    nextActions: {
      fr: ["Lancer une recherche ciblée", "Ouvrir la carte des biens", "Comparer les opportunités"],
      en: ["Run a focused search", "Open the property map", "Compare opportunities"],
      pidgin: ["Run a focused search", "Open the property map", "Compare opportunities"],
    },
    support: {
      fr: ["Suggestion", "Support", "Réclamation", "Signalement", "Partenariat", "Autre demande"],
      en: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
      pidgin: ["Suggestion", "Support", "Complaint", "Report", "Partnership", "Other request"],
    },
  },
};

function byId(id) {
  return document.getElementById(id);
}

function shouldTraceAuth() {
  try {
    return window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || localStorage.getItem("lawim.debug.auth") === "1";
  } catch {
    return false;
  }
}

function uiCopy() {
  return UI_COPY[state.language] || UI_COPY.fr;
}

function localizedValue(value) {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return value[state.language] || value.fr || value.en || value.pcm || "";
  }
  return value;
}

function localizedList(value) {
  const resolved = localizedValue(value);
  return Array.isArray(resolved) ? resolved : [];
}

function moduleCopy(moduleKey) {
  const module = MODULE_DEFS[moduleKey] || MODULE_DEFS.dashboard;
  return {
    label: module.label[state.language] || module.label.fr,
    description: module.description[state.language] || module.description.fr,
    icon: module.icon || "•",
  };
}

function splitModuleGroups(value) {
  return String(value || "")
    .split(/\s+/)
    .map((group) => group.trim())
    .filter(Boolean);
}

function moduleGroups(moduleKey, kind = "panel") {
  const module = MODULE_DEFS[moduleKey] || MODULE_DEFS.dashboard;
  return Array.isArray(module[`${kind}Groups`]) ? module[`${kind}Groups`] : [];
}

function moduleVisibleForRole(moduleKey, role) {
  const module = MODULE_DEFS[moduleKey] || MODULE_DEFS.dashboard;
  const normalizedRole = normalizeAccessRole(role) || "user";
  return module.roles.includes(normalizedRole);
}

function currentVisibleRoleKeys() {
  const role = journeyForRole(state.activeJourney || state.bootstrap?.current_user?.role || "user");
  return ROLE_JOURNEY_KEYS[role] || ROLE_JOURNEY_KEYS.user;
}

function elementRoleAllowed(element, visibleKeys) {
  const allowed = splitModuleGroups(element.getAttribute("data-journey-panel"));
  if (!allowed.length) {
    return true;
  }
  return allowed.some((key) => visibleKeys.includes(key));
}

function elementModuleAllowed(element, activeModule, attributeName) {
  const groups = splitModuleGroups(element.getAttribute(attributeName));
  if (!groups.length) {
    return false;
  }
  if (activeModule === "dashboard") {
    return false;
  }
  const activeGroups = new Set([
    ...moduleGroups(activeModule, "panel"),
    ...moduleGroups(activeModule, "card"),
  ]);
  return groups.some((group) => activeGroups.has(group));
}

function decorateModuleChrome() {
  document.querySelectorAll("[data-module-panel], [data-module-card]").forEach((element) => {
    if (element.querySelector(":scope > .module-toolbar")) {
      return;
    }
    const toolbar = document.createElement("div");
    toolbar.className = "module-toolbar";
    const backButton = document.createElement("button");
    backButton.type = "button";
    backButton.className = "button ghost module-back";
    backButton.textContent = uiCopy().backToDashboard;
    backButton.addEventListener("click", () => applyModule("dashboard"));
    toolbar.appendChild(backButton);
    element.prepend(toolbar);
  });
}

function refreshModuleChrome() {
  document.querySelectorAll(".module-back").forEach((button) => {
    button.textContent = uiCopy().backToDashboard;
  });
}

function translateModulePanels() {
  if (state.language === "fr") {
    return;
  }

  const copy = {
    en: {
      headings: {
        "Connaissance experte": "Expert know-how",
        "Moteur d'intelligence des sources": "Source brain",
        "Gestion de la relation client": "Customer relation hub",
        "Centre de communication": "Talk center",
        "Centre analytique & BI": "Analytics & BI center",
        "Marketplace & écosystème de partenaires": "Partner marketplace",
        "Intelligence immobilière": "Property intelligence",
      },
      knowledge: {
        title: "Expert knowledge",
        description: "Documents, search, categories and RAG foundation (API v2).",
        searchLabel: "Search",
        searchPlaceholder: "Search the expert base…",
        searchButton: "Search knowledge",
        stats: "Sign in to load knowledge statistics.",
      },
      sourceIntelligence: {
        title: "Source intelligence engine",
        description: "Reference codes, imports, source context, analysis, WhatsApp links and source governance (API v2).",
        labels: [
          "Source URL",
          "Source name",
          "Channel",
          "Import notes",
          "Selected source ID",
          "Network",
          "Publication URL",
          "Publication title",
          "Publication author",
          "Publication text",
          "Campaign",
          "City",
        ],
        placeholders: {
          sourceName: "Publication source",
          notes: "Import context and comments",
          network: "web",
          publicationTitle: "Publication title",
          publicationAuthor: "Author name",
          publicationText: "Excerpt or summary of the source",
          campaign: "campaign key",
        },
        importButton: "Import source",
        stats: "Sign in to load source intelligence statistics.",
      },
      marketplace: {
        searchLabel: "Search the catalog",
        searchPlaceholder: "Service, category, provider…",
        searchButton: "Search marketplace",
        stats: "Sign in to load marketplace statistics.",
      },
    },
    pidgin: {
      headings: {
        "Connaissance experte": "Expert knowledge",
        "Moteur d'intelligence des sources": "Source intelligence engine",
        "Gestion de la relation client": "Customer relationship management",
        "Centre de communication": "Communication center",
        "Centre analytique & BI": "Analytics & BI center",
        "Marketplace & écosystème de partenaires": "Marketplace & partner ecosystem",
        "Intelligence immobilière": "Real estate intelligence",
      },
      knowledge: {
        title: "Expert know-how",
        description: "Documents, search, categories and RAG base (API v2).",
        searchLabel: "Find",
        searchPlaceholder: "Search inside di expert base…",
        searchButton: "Search know-how",
        stats: "Sign in to load know-how statistics.",
      },
      sourceIntelligence: {
        title: "Source brain",
        description: "Reference codes, imports, source context, analysis, WhatsApp links and source control (API v2).",
        labels: [
          "Source URL",
          "Source name",
          "Channel",
          "Import notes",
          "Selected source ID",
          "Network",
          "Publication URL",
          "Publication title",
          "Publication author",
          "Publication text",
          "Campaign",
          "City",
        ],
        placeholders: {
          sourceName: "Publication source",
          notes: "Import context and comments",
          network: "web",
          publicationTitle: "Publication title",
          publicationAuthor: "Author name",
          publicationText: "Excerpt or summary of the source",
          campaign: "campaign key",
        },
        importButton: "Import source",
        stats: "Sign in to load source statistics.",
      },
      marketplace: {
        searchLabel: "Find in catalog",
        searchPlaceholder: "Service, category, provider…",
        searchButton: "Search marketplace",
        stats: "Sign in to load marketplace statistics.",
      },
    },
  }[state.language] || null;

  if (!copy) {
    return;
  }

  document.querySelectorAll('[data-module-card="documents"]').forEach((card) => {
    const heading = card.querySelector(".section-heading h2");
    const lead = card.querySelector(".section-heading .muted");
    const knowledgeSearch = card.querySelector("#knowledge-search-form");
    const sieImport = card.querySelector("#sie-import-form");
    if (knowledgeSearch) {
      if (heading) {
        heading.textContent = copy.knowledge.title;
      }
      if (lead) {
        lead.textContent = copy.knowledge.description;
      }
      const label = knowledgeSearch.querySelector("label span");
      const input = knowledgeSearch.querySelector("input[name='query']");
      const button = knowledgeSearch.querySelector("button[type='submit']");
      if (label) {
        label.textContent = copy.knowledge.searchLabel;
      }
      if (input) {
        input.placeholder = copy.knowledge.searchPlaceholder;
      }
      if (button) {
        button.textContent = copy.knowledge.searchButton;
      }
    }
    if (sieImport) {
      if (heading) {
        heading.textContent = copy.sourceIntelligence.title;
      }
      if (lead) {
        lead.textContent = copy.sourceIntelligence.description;
      }
      const spans = sieImport.querySelectorAll("label > span");
      spans.forEach((span, index) => {
        if (copy.sourceIntelligence.labels[index]) {
          span.textContent = copy.sourceIntelligence.labels[index];
        }
      });
      const urlInput = sieImport.querySelector("input[name='url']");
      const nameInput = sieImport.querySelector("input[name='name']");
      const channelSelect = sieImport.querySelector("select[name='channel']");
      const notesInput = sieImport.querySelector("textarea[name='notes']");
      const button = sieImport.querySelector("button[type='submit']");
      if (nameInput) {
        nameInput.placeholder = copy.sourceIntelligence.placeholders.sourceName;
      }
      if (channelSelect) {
        Array.from(channelSelect.options || []).forEach((option) => {
          if (option.value === "web") option.textContent = "web";
          if (option.value === "whatsapp") option.textContent = "whatsapp";
          if (option.value === "referral") option.textContent = state.language === "pidgin" ? "referral" : "referral";
          if (option.value === "internal") option.textContent = state.language === "pidgin" ? "internal" : "internal";
          if (option.value === "publication") option.textContent = state.language === "pidgin" ? "publication" : "publication";
          if (option.value === "other") option.textContent = state.language === "pidgin" ? "other" : "other";
        });
      }
      if (notesInput) {
        notesInput.placeholder = copy.sourceIntelligence.placeholders.notes;
      }
      if (button) {
        button.textContent = copy.sourceIntelligence.importButton;
      }
      if (urlInput) {
        urlInput.placeholder = "https://example.cm/publication";
      }
    }
    const sieStats = card.querySelector("#sie-admin-stats");
    if (sieStats) {
      sieStats.textContent = copy.sourceIntelligence.stats;
    }
    const sieSource = card.querySelector("#sie-source-form");
    if (sieSource) {
      const spans = sieSource.querySelectorAll("label > span");
      spans.forEach((span, index) => {
        if (copy.sourceIntelligence.labels[index + 4]) {
          span.textContent = copy.sourceIntelligence.labels[index + 4];
        }
      });
      const networkInput = sieSource.querySelector("input[name='network']");
      const publicationUrl = sieSource.querySelector("input[name='publication_url']");
      const publicationTitle = sieSource.querySelector("input[name='publication_title']");
      const publicationAuthor = sieSource.querySelector("input[name='publication_author']");
      const publicationText = sieSource.querySelector("textarea[name='publication_text']");
      const campaignInput = sieSource.querySelector("input[name='campaign']");
      const cityInput = sieSource.querySelector("input[name='city']");
      if (networkInput) {
        networkInput.placeholder = copy.sourceIntelligence.placeholders.network;
      }
      if (publicationUrl) {
        publicationUrl.placeholder = "https://example.cm/publication";
      }
      if (publicationTitle) {
        publicationTitle.placeholder = copy.sourceIntelligence.placeholders.publicationTitle;
      }
      if (publicationAuthor) {
        publicationAuthor.placeholder = copy.sourceIntelligence.placeholders.publicationAuthor;
      }
      if (publicationText) {
        publicationText.placeholder = copy.sourceIntelligence.placeholders.publicationText;
      }
      if (campaignInput) {
        campaignInput.placeholder = copy.sourceIntelligence.placeholders.campaign;
      }
      if (cityInput) {
        cityInput.placeholder = "Douala";
      }
    }
  });

  document.querySelectorAll('[data-module-card="partenaires"]').forEach((card) => {
    const searchForm = card.querySelector("#marketplace-search-form");
    if (searchForm) {
      const label = searchForm.querySelector("label span");
      const input = searchForm.querySelector("input[name='query']");
      const button = searchForm.querySelector("button[type='submit']");
      if (label) {
        label.textContent = copy.marketplace.searchLabel;
      }
      if (input) {
        input.placeholder = copy.marketplace.searchPlaceholder;
      }
      if (button) {
        button.textContent = copy.marketplace.searchButton;
      }
    }
    const stats = card.querySelector("#marketplace-admin-stats");
    if (stats) {
      stats.textContent = copy.marketplace.stats;
    }
  });
}

function translateStaticShell() {
  const copy = uiCopy();
  const logoutButton = document.querySelector("#logout-button");
  const moduleDeckTitle = document.querySelector(".sidebar > .form-panel:nth-of-type(2) .section-heading h2");
  const moduleDeckLead = document.querySelector(".sidebar > .form-panel:nth-of-type(2) .section-heading p.muted");
  const cockpitLeads = copy.cockpitLeads || [];

  if (moduleDeckTitle) {
    moduleDeckTitle.textContent = copy.modules;
  }
  if (moduleDeckLead) {
    moduleDeckLead.textContent = copy.moduleDeckLead || moduleDeckLead.textContent;
  }
  if (refs.authLanguageLabel) {
    refs.authLanguageLabel.textContent = copy.languageLabel || refs.authLanguageLabel.textContent;
  }
  if (refs.authSlogan) {
    refs.authSlogan.textContent = copy.brandTagline || refs.authSlogan.textContent;
  }
  if (refs.loginEmailLabel) {
    refs.loginEmailLabel.textContent = copy.loginEmail || refs.loginEmailLabel.textContent;
  }
  if (refs.loginPasswordLabel) {
    refs.loginPasswordLabel.textContent = copy.loginPassword || refs.loginPasswordLabel.textContent;
  }
  if (refs.loginButton) {
    refs.loginButton.textContent = copy.loginTitle;
  }
  if (refs.loginForgot) {
    refs.loginForgot.textContent = copy.loginForgot;
  }
  if (refs.loginCreate) {
    refs.loginCreate.textContent = copy.loginCreate;
  }
  if (logoutButton) {
    logoutButton.textContent = copy.authenticated;
  }
  renderOfficialContactBlock();
  document.querySelectorAll("#role-cockpit .cockpit-grid .cockpit-card .section-heading p.muted").forEach((paragraph, index) => {
    if (cockpitLeads[index]) {
      paragraph.textContent = cockpitLeads[index];
    }
  });
  translateModulePanels();
}

function renderModuleDeck(currentUser) {
  if (!refs.journeyNav) {
    return;
  }
  const role = resolveAccessRole(currentUser?.role, currentUser?.roles || state.bootstrap?.roles || []);
  const modules = Object.entries(MODULE_DEFS).filter(([moduleKey]) => moduleVisibleForRole(moduleKey, role));
  refs.journeyNav.innerHTML = modules
    .map(([moduleKey]) => {
      const copy = moduleCopy(moduleKey);
      return `
        <button type="button" class="module-launcher" data-module="${escapeHtml(moduleKey)}">
          <strong>${escapeHtml(`${copy.icon} ${copy.label}`)}</strong>
          <span>${escapeHtml(copy.description)}</span>
        </button>
      `;
    })
    .join("");
  refs.journeyNav.querySelectorAll("[data-module]").forEach((button) => {
    button.addEventListener("click", () => applyModule(button.getAttribute("data-module") || "dashboard"));
  });
  refs.journeyNav.querySelectorAll("[data-module]").forEach((button) => {
    button.dataset.active = button.getAttribute("data-module") === state.activeModule ? "true" : "false";
  });
}

function syncWorkspaceVisibility() {
  const activeModule = state.activeModule || "dashboard";
  document.body.dataset.module = activeModule;
  const visibleKeys = currentVisibleRoleKeys();

  if (refs.cardsGrid) {
    refs.cardsGrid.hidden = !state.token || activeModule === "dashboard";
  }

  document.querySelectorAll("[data-journey-panel]").forEach((panel) => {
    if (!state.token) {
      panel.hidden = true;
      return;
    }
    const roleAllowed = elementRoleAllowed(panel, visibleKeys);
    const moduleAllowed = elementModuleAllowed(panel, activeModule, "data-module-panel");
    const pinnedAdminPanel =
      activeModule === "dashboard" &&
      panel.getAttribute("data-journey-panel") === "admin" &&
      visibleKeys.includes("admin");
    panel.hidden = !(roleAllowed && (moduleAllowed || pinnedAdminPanel));
  });

  document.querySelectorAll("[data-module-card]").forEach((card) => {
    if (!state.token || activeModule === "dashboard") {
      card.hidden = true;
      return;
    }
    const roleAllowed = elementRoleAllowed(card, visibleKeys);
    const moduleAllowed = elementModuleAllowed(card, activeModule, "data-module-card");
    card.hidden = !(roleAllowed && moduleAllowed);
  });

  if (refs.journeyNav) {
    refs.journeyNav.querySelectorAll("[data-module]").forEach((button) => {
      button.dataset.active = button.getAttribute("data-module") === activeModule ? "true" : "false";
    });
  }
}

function applyModule(moduleKey, { persist = true } = {}) {
  const normalized = MODULE_DEFS[moduleKey] ? moduleKey : "dashboard";
  state.activeModule = normalized;
  if (persist) {
    localStorage.setItem("lawim.module", normalized);
  }
  syncWorkspaceVisibility();
}

function updateAuthShell(isAuthenticated) {
  document.body.dataset.authenticated = isAuthenticated ? "true" : "false";
  if (refs.workspace) {
    refs.workspace.hidden = !isAuthenticated;
  }
  if (refs.runtimeChip) {
    refs.runtimeChip.hidden = isAuthenticated;
  }
  if (refs.currentUser) {
    refs.currentUser.hidden = !isAuthenticated;
  }
  if (refs.logoutButton) {
    refs.logoutButton.hidden = !isAuthenticated;
  }
  if (refs.authContact) {
    refs.authContact.hidden = isAuthenticated;
  }
  if (refs.loginForm) {
    refs.loginForm.hidden = isAuthenticated;
  }
  if (refs.journeyNav) {
    refs.journeyNav.hidden = !isAuthenticated;
  }
}

function extractRoleValue(role) {
  if (typeof role === "string" || typeof role === "number") {
    return role;
  }
  if (role && typeof role === "object") {
    return role.role || role.role_key || role.key || role.name || "";
  }
  return "";
}

function normalizeAccessRole(role) {
  const normalized = String(extractRoleValue(role) || "").trim().toLowerCase();
  if (!normalized) {
    return "";
  }
  return ROLE_ALIASES[normalized] || "";
}

function resolveAccessRole(primaryRole, roles = []) {
  const direct = normalizeAccessRole(primaryRole);
  if (direct) {
    return direct;
  }
  const candidates = Array.isArray(roles) ? roles : [];
  for (const priority of ACCESS_ROLE_PRIORITY) {
    if (candidates.some((candidate) => normalizeAccessRole(candidate) === priority)) {
      return priority;
    }
  }
  return "user";
}

function journeyForRole(role) {
  return normalizeAccessRole(role) || "user";
}

function roleLabel(role) {
  const normalized = normalizeAccessRole(role);
  return ROLE_LABELS[normalized] || ROLE_LABELS.user;
}

function clearSession() {
  state.token = "";
  localStorage.removeItem("lawim.token");
  state.activeModule = "dashboard";
  localStorage.removeItem("lawim.module");
  updateAuthShell(false);
  if (refs.currentUser) {
    refs.currentUser.textContent = uiCopy().session;
  }
  if (refs.logoutButton) {
    refs.logoutButton.disabled = true;
  }
  if (refs.roleCockpit) {
    refs.roleCockpit.hidden = true;
  }
  if (refs.loginPassword) {
    refs.loginPassword.value = "";
  }
}

function isServerUnavailableError(error) {
  const status = Number(error?.status || 0);
  return status >= 500 || (!status && /fetch|network|timeout|unavailable/i.test(String(error?.message || "")));
}

function formatLoginError(error) {
  const status = Number(error?.status || 0);
  const copy = {
    fr: {
      invalid: "Identifiants incorrects.",
      forbidden: "Accès non autorisé.",
      unavailable: "Serveur indisponible. Réessayez dans un instant.",
      fallback: "Connexion impossible.",
    },
    en: {
      invalid: "Incorrect credentials.",
      forbidden: "Access denied.",
      unavailable: "Server unavailable. Try again in a moment.",
      fallback: "Unable to sign in.",
    },
    pidgin: {
      invalid: "Login details no correct.",
      forbidden: "Access no dey allowed.",
      unavailable: "Server no dey. Try again in a moment.",
      fallback: "Login no fit happen.",
    },
  }[state.language] || {};
  if (status === 401) {
    return copy.invalid || "Identifiants incorrects.";
  }
  if (status === 403) {
    return copy.forbidden || "Accès non autorisé.";
  }
  if (isServerUnavailableError(error)) {
    return copy.unavailable || "Serveur indisponible. Réessayez dans un instant.";
  }
  return error?.message || copy.fallback || "Connexion impossible.";
}

function formatSessionError(error) {
  const status = Number(error?.status || 0);
  const copy = {
    fr: {
      expired: "Session expirée. Connectez-vous de nouveau.",
      forbidden: "Accès non autorisé.",
      unavailable: "Serveur indisponible. Réessayez dans un instant.",
      fallback: "Impossible de restaurer la session.",
    },
    en: {
      expired: "Session expired. Sign in again.",
      forbidden: "Access denied.",
      unavailable: "Server unavailable. Try again in a moment.",
      fallback: "Unable to restore the session.",
    },
    pidgin: {
      expired: "Session don expire. Sign in again.",
      forbidden: "Access no dey allowed.",
      unavailable: "Server no dey. Try again in a moment.",
      fallback: "No fit restore session.",
    },
  }[state.language] || {};
  if (status === 401) {
    return { message: copy.expired || "Session expirée. Connectez-vous de nouveau.", tone: "warn", clearToken: true };
  }
  if (status === 403) {
    return { message: copy.forbidden || "Accès non autorisé.", tone: "warn", clearToken: true };
  }
  if (isServerUnavailableError(error)) {
    return { message: copy.unavailable || "Serveur indisponible. Réessayez dans un instant.", tone: "error", clearToken: false };
  }
  return { message: error?.message || copy.fallback || "Impossible de restaurer la session.", tone: "error", clearToken: false };
}

function cacheRefs() {
  Object.assign(refs, {
    runtimeChip: byId("runtime-chip"),
    languageSelect: byId("language-select"),
    authLanguageLabel: document.querySelector(".language-switcher .sr-only"),
    currentUser: byId("current-user"),
    workspace: byId("workspace"),
    notice: byId("notice"),
    bootstrapSummary: byId("bootstrap-summary"),
    authPanel: document.querySelector(".auth-panel"),
    authContact: document.getElementById("auth-contact"),
    authSlogan: document.querySelector(".auth-slogan"),
    loginButton: document.getElementById("login-submit"),
    loginForgot: document.getElementById("login-forgot"),
    loginCreate: document.getElementById("login-create"),
    loginEmailLabel: document.getElementById("login-email-label"),
    loginPasswordLabel: document.getElementById("login-password-label"),
    statusStrip: byId("status-strip"),
    roleCockpit: byId("role-cockpit"),
    cardsGrid: document.querySelector(".cards-grid"),
    roleGreeting: byId("role-greeting"),
    roleSubtitle: byId("role-subtitle"),
    roleChip: byId("role-chip"),
    roleActivityChip: byId("role-activity-chip"),
    progressCard: byId("progress-card"),
    activityCard: byId("activity-card"),
    prioritiesCard: byId("priorities-card"),
    quickActionsCard: byId("quick-actions-card"),
    statsCard: byId("stats-card"),
    statsPeriodSelect: byId("stats-period-select"),
    recommendationsCard: byId("recommendations-card"),
    nextActionsCard: byId("next-actions-card"),
    supportCard: byId("support-card"),
    organizationsList: byId("organizations-list"),
    propertiesList: byId("properties-list"),
    mediaList: byId("media-list"),
    matchesList: byId("matches-list"),
    conversationsList: byId("conversations-list"),
    notificationsList: byId("notifications-list"),
    markNotificationsReadButton: byId("mark-notifications-read"),
    conversationDetail: byId("conversation-detail"),
    messageForm: byId("message-form"),
    loginForm: byId("login-form"),
    loginEmail: byId("login-email"),
    loginPassword: byId("login-password"),
    logoutButton: byId("logout-button"),
    matchForm: byId("match-form"),
    propertyForm: byId("property-form"),
    geoForm: byId("geo-form"),
    geoResult: byId("geo-result"),
    mediaUploadForm: byId("media-upload-form"),
    mediaPropertySelect: byId("media-property-select"),
    ownerOrganizationSelect: byId("owner-organization-select"),
    registerOrganizationSelect: byId("register-organization-select"),
    adminOrganizationSelect: byId("admin-organization-select"),
    journeyNav: byId("journey-nav"),
    registerForm: byId("register-form"),
    propertySearchForm: byId("property-search-form"),
    propertySearchMeta: byId("property-search-meta"),
    notificationFilterForm: byId("notification-filter-form"),
    notificationUnreadCount: byId("notification-unread-count"),
    negotiationForm: byId("negotiation-form"),
    buyerConversationForm: byId("buyer-conversation-form"),
    adminOrgForm: byId("admin-org-form"),
    adminUserForm: byId("admin-user-form"),
    adminDashboard: byId("admin-dashboard"),
    selectedPropertyLabel: byId("selected-property-label"),
    publishPropertyButton: byId("publish-property-button"),
    archivePropertyButton: byId("archive-property-button"),
    projectForm: byId("project-form"),
    projectsList: byId("projects-list"),
    projectDetail: byId("project-detail"),
    partnersList: byId("partners-list"),
    servicesList: byId("services-list"),
    assistantSummary: byId("assistant-summary"),
    assistantForm: byId("assistant-form"),
    assistantChat: byId("assistant-chat"),
    knowledgeAdminStats: byId("knowledge-admin-stats"),
    knowledgeAdminList: byId("knowledge-admin-list"),
    knowledgeSearchForm: byId("knowledge-search-form"),
    knowledgeSearchResults: byId("knowledge-search-results"),
    workflowAdminStats: byId("workflow-admin-stats"),
    workflowAdminList: byId("workflow-admin-list"),
    workflowMonitorForm: byId("workflow-monitor-form"),
    workflowMonitorResults: byId("workflow-monitor-results"),
    reiAdminStats: byId("rei-admin-stats"),
    reiAdminList: byId("rei-admin-list"),
    reiSearchForm: byId("rei-search-form"),
    reiSearchResults: byId("rei-search-results"),
    crmAdminStats: byId("crm-admin-stats"),
    crmAdminList: byId("crm-admin-list"),
    crmSearchForm: byId("crm-search-form"),
    crmSearchResults: byId("crm-search-results"),
    marketplaceAdminStats: byId("marketplace-admin-stats"),
    marketplaceAdminList: byId("marketplace-admin-list"),
    marketplaceSearchForm: byId("marketplace-search-form"),
    marketplaceSearchResults: byId("marketplace-search-results"),
    communicationAdminStats: byId("communication-admin-stats"),
    communicationAdminList: byId("communication-admin-list"),
    analyticsAdminStats: byId("analytics-admin-stats"),
    analyticsAdminList: byId("analytics-admin-list"),
    sieAdminStats: byId("sie-admin-stats"),
    sieAdminList: byId("sie-admin-list"),
    sieImportForm: byId("sie-import-form"),
    sieSourceForm: byId("sie-source-form"),
    sieReferenceForm: byId("sie-reference-form"),
    sieReferenceResult: byId("sie-reference-result"),
    sieLinkResult: byId("sie-link-result"),
    sieAnalyzeButton: byId("sie-analyze-button"),
    sieWhatsappButton: byId("sie-whatsapp-button"),
    securityAdminStats: byId("security-admin-stats"),
    securityAdminList: byId("security-admin-list"),
    securityAuditForm: byId("security-audit-form"),
    securityAuditResults: byId("security-audit-results"),
  });
}

function setNotice(message, tone = "neutral", code = "") {
  refs.notice.dataset.tone = tone;
  refs.notice.textContent = code ? `[${code}] ${message}` : message;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function setLoading(isLoading, message = "Loading...") {
  document.body.dataset.loading = isLoading ? "true" : "false";
  if (isLoading && refs.notice) {
    refs.notice.dataset.tone = "neutral";
    refs.notice.textContent = message === "Loading..." ? (state.language === "fr" ? "Chargement..." : "Loading...") : message;
  }
}

function traceRuntime(step, details = {}) {
  if (!shouldTraceAuth()) {
    return;
  }
  console.debug(step, details);
}

function formatApiError(payload, status) {
  const code = payload?.error?.code;
  const message = payload?.error?.message || payload?.message || `HTTP ${status}`;
  return { code: code || "", message };
}

function statusChipClass(status) {
  const normalized = String(status || "draft").toLowerCase();
  if (normalized === "published") {
    return "chip accent";
  }
  if (normalized === "archived") {
    return "chip subtle";
  }
  return "chip subtle";
}

function setRuntimeChip(message, tone = "neutral") {
  refs.runtimeChip.dataset.tone = tone;
  refs.runtimeChip.textContent = message;
}

function openSupportRequest(subject) {
  const official = state.bootstrap?.official_contact || {};
  const supportEmail = official.support_email || "contact@lawim.app";
  window.location.href = `mailto:${supportEmail}?subject=${encodeURIComponent(subject)}`;
}

function renderOfficialContactBlock() {
  if (!refs.authContact) {
    return;
  }
  const copy = uiCopy();
  const official = state.bootstrap?.official_contact || {};
  const website = official.website_url || "https://lawim.app";
  const websiteLabel = String(website).replace(/^https?:\/\//, "");
  const email = official.support_email || "contact@lawim.app";
  const phone = official.phone_international || official.phone_number || "";
  const phoneDigits = String(official.phone_e164 || phone).replace(/[^0-9]/g, "");
  const whatsappLink = official.whatsapp_link || (phoneDigits ? `https://wa.me/${phoneDigits}` : website);
  const facebookLink = official.facebook_link || "https://facebook.com/lawimofficial";
  const items = [
    { icon: "🌐", label: copy.contactWebsite, value: websiteLabel, href: website, external: true },
    { icon: "✉️", label: copy.contactEmail, value: email, href: `mailto:${email}`, external: false },
    { icon: "📞", label: copy.contactPhone, value: phone, href: phoneDigits ? `tel:+${phoneDigits}` : website, external: false },
    { icon: "💬", label: copy.contactWhatsApp, value: official.whatsapp_username || "@lawimofficial", href: whatsappLink, external: true },
    { icon: "f", label: copy.contactFacebook, value: official.facebook_username || "@lawimofficial", href: facebookLink, external: true },
  ];

  refs.authContact.hidden = false;
  refs.authContact.innerHTML = items
    .map(
      (item) => `
        <a class="auth-contact__item" href="${escapeHtml(item.href)}"${item.external ? ' target="_blank" rel="noreferrer"' : ""} aria-label="${escapeHtml(`${item.label} ${item.value}`)}">
          <span class="auth-contact__icon" aria-hidden="true">${escapeHtml(item.icon)}</span>
          <span class="auth-contact__copy">
            <span class="auth-contact__label">${escapeHtml(item.label)}</span>
            <strong>${escapeHtml(item.value)}</strong>
          </span>
        </a>
      `,
    )
    .join("");
}

function money(value, currency = "XAF") {
  if (value === null || value === undefined || value === "") {
    return "n/a";
  }
  const formatted = moneyFormatter.format(Number(value));
  return `${formatted} ${currency}`;
}

function propertyPrice(property) {
  if (property.price) {
    return {
      min: property.price.min,
      max: property.price.max,
      currency: property.price.currency || "XAF",
    };
  }
  return {
    min: property.price_min,
    max: property.price_max,
    currency: property.currency || "XAF",
  };
}

function propertyGeo(property) {
  if (property.geo) {
    return property.geo;
  }
  return {
    city: property.city,
    country: property.country,
    region: property.region,
    address_line: property.address_line,
    coordinates: { latitude: property.latitude, longitude: property.longitude },
  };
}

function requestHeaders(headers = {}, auth = false) {
  const merged = { ...headers };
  if (auth && state.token) {
    merged.Authorization = `Bearer ${state.token}`;
  }
  return merged;
}

async function api(path, { method = "GET", auth = false, body = null, query = null, headers = {} } = {}) {
  const url = new URL(path, window.location.origin);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && `${value}`.trim() !== "") {
        url.searchParams.set(key, String(value));
      }
    }
  }

  const response = await fetch(url, {
    method,
    headers: requestHeaders({ ...(body ? { "Content-Type": "application/json" } : {}), ...headers }, auth),
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  let payload = {};
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch (error) {
      throw new Error(systemCopy("invalidJsonResponse", path));
    }
  }

  if (!response.ok) {
    const formatted = formatApiError(payload, response.status);
    const error = new Error(formatted.message);
    error.code = formatted.code;
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

async function apiMultipart(path, { auth = false, formData }) {
  const response = await fetch(path, {
    method: "POST",
    headers: requestHeaders({}, auth),
    body: formData,
  });
  const text = await response.text();
  let payload = {};
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch (error) {
      throw new Error(systemCopy("invalidJsonResponse", path));
    }
  }
  if (!response.ok) {
    const formatted = formatApiError(payload, response.status);
    const error = new Error(formatted.message);
    error.code = formatted.code;
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
}

function clearNode(node) {
  node.replaceChildren();
}

function renderStat(label, value, accent = "") {
  const item = document.createElement("article");
  item.className = "stat-card";
  if (accent) {
    item.dataset.accent = accent;
  }
  const statLabel = document.createElement("span");
  statLabel.className = "stat-label";
  statLabel.textContent = label;
  const statValue = document.createElement("strong");
  statValue.textContent = value;
  item.append(statLabel, statValue);
  return item;
}

function renderSummary(summary) {
  const fragment = document.createDocumentFragment();
  const labels = SUMMARY_COPY[state.language] || SUMMARY_COPY.fr;
  const cards = [
    [labels.organizations, summary.organizations ?? 0, "teal"],
    [labels.users, summary.users ?? 0, "gold"],
    [labels.properties, summary.published_properties ?? 0, "violet"],
    [labels.conversations, summary.conversations ?? 0, "coral"],
    [labels.messages, summary.messages ?? 0, "sea"],
    [labels.notifications, summary.notifications ?? 0, "gold"],
    [labels.media, summary.media ?? 0, "slate"],
    [labels.projects, summary.projects ?? 0, "teal"],
  ];
  cards.forEach(([label, value, accent]) => fragment.appendChild(renderStat(label, value, accent)));
  refs.statusStrip?.replaceChildren(fragment);
}

function renderList(target, items, renderer, emptyText) {
  const fragment = document.createDocumentFragment();
  if (!items || !items.length) {
    const empty = document.createElement("p");
    empty.className = "muted empty-state";
    empty.textContent = String(localizedValue(emptyText) || "");
    target.replaceChildren(empty);
    return;
  }
  items.forEach((item) => fragment.appendChild(renderer(item)));
  target.replaceChildren(fragment);
}

function renderPillList(items, emptyText) {
  if (!items.length) {
    return `<p class="muted empty-state">${escapeHtml(localizedValue(emptyText) || "")}</p>`;
  }
  return `<div class="pill-list">${items.map((item) => `<span class="pill">${escapeHtml(item)}</span>`).join("")}</div>`;
}

function renderActionLinks(actions) {
  if (!actions.length) {
    return "<p class='muted empty-state'>—</p>";
  }
  return `<div class="action-link-grid">${actions
    .map(
      (action) => `<a class="button secondary action-link" href="${escapeHtml(action.href)}">${escapeHtml(action.label)}</a>`,
    )
    .join("")}</div>`;
}

function renderKeyValueRows(rows, emptyText) {
  if (!rows.length) {
    return `<p class="muted empty-state">${escapeHtml(emptyText)}</p>`;
  }
  return `<div class="cockpit-stack">${rows
    .map(
      (row) => `
        <article class="cockpit-row">
          <span class="cockpit-row__label">${escapeHtml(row.label)}</span>
          <strong>${escapeHtml(row.value)}</strong>
          <span class="muted">${escapeHtml(row.detail || "")}</span>
        </article>
      `,
    )
    .join("")}</div>`;
}

function pickPrimaryProject(items) {
  return (items || []).find((project) => project.status !== "archived") || (items || [])[0] || null;
}

function formatRoleStatus(role) {
  return `${ROLE_EMOJIS[role] || "✨"} ${roleLabel(role)}`;
}

function setLanguage(language) {
  const normalized = ["fr", "en", "pidgin"].includes(language) ? language : "fr";
  state.language = normalized;
  localStorage.setItem("lawim.language", normalized);
  document.documentElement.lang = normalized === "pidgin" ? "en" : normalized;
  if (refs.languageSelect && refs.languageSelect.value !== normalized) {
    refs.languageSelect.value = normalized;
  }
  translateStatsPeriodSelect();
  translateStaticShell();
  if (state.bootstrap?.current_user) {
    renderRoleCockpit(state.bootstrap.current_user, state.bootstrap);
    renderModuleDeck(state.bootstrap.current_user);
    refreshModuleChrome();
  }
}

function renderRoleCockpit(currentUser, payload) {
  if (!refs.roleCockpit || !refs.roleGreeting || !refs.progressCard || !refs.activityCard) {
    return;
  }

  const role = resolveAccessRole(currentUser?.role, currentUser?.roles || payload.roles || []);
  const config = ROLE_COCKPIT_CONFIG[role] || ROLE_COCKPIT_CONFIG.user;
  const summary = payload.summary || {};
  const projects = payload.projects || [];
  const conversations = payload.conversations || [];
  const notifications = payload.notifications || [];
  const matches = payload.matches || [];
  const unread = notifications.filter((notification) => !notification.read);
  const currentProject = pickPrimaryProject(projects);
  const name = currentUser?.full_name || currentUser?.name || currentUser?.email?.split("@")?.[0] || "Utilisateur";
  const progress = currentProject?.progress_percent ?? 0;
  const supportHint = uiCopy().supportHint;
  const roleStatus = formatRoleStatus(role);
  const activeConversation = conversations[0] || null;
  const topMatch = matches[0] || null;
  const activityItems = localizedList(config.activity);
  const priorityText = localizedList(config.priorities);
  const recommendationText = localizedList(config.recommendations);
  const nextActionText = localizedList(config.nextActions);
  const supportText = localizedList(config.support);
  const quickActions = (Array.isArray(config.quickActions) ? config.quickActions : []).map((action) => ({
    href: action.href,
    label: localizedValue(action.label),
  }));
  const statsCopyByLanguage = {
    fr: {
      organizations: "Organisations",
      organizationsDetail: "Organisation(s) connectée(s)",
      users: "Utilisateurs",
      usersDetail: "Comptes disponibles",
      properties: "Biens",
      propertiesDetail: "Biens publiés",
      conversations: "Conversations",
      conversationsDetail: "Fils de discussion",
      messages: "Messages",
      messagesDetail: "Échanges actifs",
      notifications: "Notifications",
      notificationsDetail: "Alertes à traiter",
      today: "Aujourd'hui",
      activity: "Journal d'activité",
      unread: "non lues",
      openConversations: "ouvertes",
      activePeriod: "Période active",
      role: "Rôle",
      roleDetail: "Profil actif",
      progress: "Progression",
      nextStep: "Prochaine étape",
      currentProject: "Aucun projet actif",
      currentProjectDetail: "Créez ou choisissez un projet",
      missingDocuments: "Documents manquants",
      criticalAlerts: "Aucune alerte critique",
      noPath: "Aucun parcours actif.",
      noActivity: "Aucune activité disponible.",
      noPriority: "Aucune priorité détectée.",
      noRecommendation: "Aucune recommandation disponible.",
      noSuggestion: "Aucune suggestion immédiate.",
      noCategory: "Aucune catégorie",
      openModule: "Ouvrir le module",
      viewNotifications: "Voir les notifications",
    },
    en: {
      organizations: "Organizations",
      organizationsDetail: "Connected organization(s)",
      users: "Users",
      usersDetail: "Available accounts",
      properties: "Listings",
      propertiesDetail: "Published listings",
      conversations: "Conversations",
      conversationsDetail: "Threads",
      messages: "Messages",
      messagesDetail: "Active exchanges",
      notifications: "Notifications",
      notificationsDetail: "Alerts to handle",
      today: "Today",
      activity: "Activity log",
      unread: "unread",
      openConversations: "open",
      activePeriod: "Active period",
      role: "Role",
      roleDetail: "Active profile",
      progress: "Progress",
      nextStep: "Next step",
      currentProject: "No active project",
      currentProjectDetail: "Create or choose a project",
      missingDocuments: "Missing documents",
      criticalAlerts: "No critical alert",
      noPath: "No active path.",
      noActivity: "No activity available.",
      noPriority: "No priority detected.",
      noRecommendation: "No recommendation available.",
      noSuggestion: "No immediate suggestion.",
      noCategory: "No category",
      openModule: "Open module",
      viewNotifications: "View notifications",
    },
    pidgin: {
      organizations: "Organizations",
      organizationsDetail: "Connected organization(s)",
      users: "Users",
      usersDetail: "Available accounts",
      properties: "Listings",
      propertiesDetail: "Published listings",
      conversations: "Conversations",
      conversationsDetail: "Threads",
      messages: "Messages",
      messagesDetail: "Active exchanges",
      notifications: "Notifications",
      notificationsDetail: "Alerts to handle",
      today: "Today",
      activity: "Activity log",
      unread: "unread",
      openConversations: "open",
      activePeriod: "Active period",
      role: "Role",
      roleDetail: "Active profile",
      progress: "Progress",
      nextStep: "Next step",
      currentProject: "No active project",
      currentProjectDetail: "Create or choose a project",
      missingDocuments: "Missing documents",
      criticalAlerts: "No critical alert",
      noPath: "No active path.",
      noActivity: "No activity available.",
      noPriority: "No priority detected.",
      noRecommendation: "No recommendation available.",
      noSuggestion: "No immediate suggestion.",
      noCategory: "No category",
      openModule: "Open module",
      viewNotifications: "View notifications",
    },
  };
  const statsCopy = statsCopyByLanguage[state.language] || statsCopyByLanguage.fr;
  const roleStats = [
    { label: statsCopy.organizations, value: String(summary.organizations ?? 0), detail: statsCopy.organizationsDetail },
    { label: statsCopy.users, value: String(summary.users ?? 0), detail: statsCopy.usersDetail },
    { label: statsCopy.properties, value: String(summary.published_properties ?? 0), detail: statsCopy.propertiesDetail },
    { label: statsCopy.conversations, value: String(summary.conversations ?? 0), detail: statsCopy.conversationsDetail },
    { label: statsCopy.messages, value: String(summary.messages ?? 0), detail: statsCopy.messagesDetail },
    { label: statsCopy.notifications, value: String(summary.notifications ?? 0), detail: statsCopy.notificationsDetail },
  ];

  refs.roleGreeting.textContent = `${uiCopy().welcome}, ${name}`;
  refs.roleSubtitle.textContent = `${localizedValue(config.subtitle)} ${activeConversation ? `${state.language === "fr" ? "Conversation active" : "Active conversation"}: ${activeConversation.subject}` : ""}`.trim();
  refs.roleChip.textContent = roleStatus;
  refs.roleActivityChip.textContent = uiCopy().activity;
  if (refs.languageSelect) {
    refs.languageSelect.value = state.language;
  }
  if (refs.statsPeriodSelect) {
    refs.statsPeriodSelect.value = state.statsPeriod;
  }

  refs.progressCard.innerHTML = renderKeyValueRows(
    [
      { label: statsCopy.role, value: roleStatus, detail: statsCopy.roleDetail },
      {
        label: statsCopy.progress,
        value: `${progress}%`,
        detail: currentProject ? `${currentProject.title} · ${currentProject.project_type}` : statsCopy.currentProject,
      },
      {
        label: statsCopy.nextStep,
        value: currentProject ? (currentProject.location?.city || currentProject.city || (state.language === "fr" ? "Continuer" : "Continue")) : (state.language === "fr" ? "Définir un projet" : "Define a project"),
        detail: currentProject ? currentProject.objective || (state.language === "fr" ? "Parcours en cours" : "Path in progress") : statsCopy.currentProjectDetail,
      },
      {
        label: statsCopy.missingDocuments,
        value: String(Math.max(0, unread.length)),
        detail: unread[0]?.title || statsCopy.criticalAlerts,
      },
    ],
    statsCopy.noPath,
  );

  refs.activityCard.innerHTML = renderKeyValueRows(
    [
      { label: statsCopy.today, value: `${summary.events ?? 0} événements`, detail: statsCopy.activity },
      { label: statsCopy.notifications, value: `${unread.length} ${statsCopy.unread}`, detail: unread[0]?.title || (state.language === "fr" ? "Rien à relancer" : "Nothing to follow up") },
      { label: statsCopy.conversations, value: `${conversations.length} ${statsCopy.openConversations}`, detail: activeConversation?.subject || (state.language === "fr" ? "Aucun fil actif" : "No active thread") },
      { label: statsCopy.properties, value: `${summary.published_properties ?? 0} ${state.language === "fr" ? "publiés" : "published"}`, detail: topMatch?.property?.title || (state.language === "fr" ? "Catalogue disponible" : "Catalog available") },
    ],
    statsCopy.noActivity,
  );

  const priorityItems = [
    ...(unread.slice(0, 2).map((notification) => `${notification.title} · ${notification.kind}`) || []),
    ...(conversations.slice(0, 2).map((conversation) => `${conversation.subject} · ${conversation.status}`) || []),
    ...priorityText,
  ].slice(0, 4);
  refs.prioritiesCard.innerHTML = renderPillList(priorityItems, statsCopy.noPriority);

  refs.quickActionsCard.innerHTML = renderActionLinks(quickActions);

  const statsPeriodCopy = STATS_PERIOD_COPY[state.language] || STATS_PERIOD_COPY.fr;
  const statsPeriodLabel =
    refs.statsPeriodSelect?.selectedOptions?.[0]?.textContent || statsPeriodCopy[state.statsPeriod] || statsPeriodCopy.today;
  refs.statsCard.innerHTML = `
    <div class="cockpit-stack">
      <p class="muted">${escapeHtml(statsPeriodCopy.activePeriod)}: ${escapeHtml(statsPeriodLabel)}</p>
      <div class="stats-mini-grid">
        ${roleStats
          .map(
            (stat) => `
              <article class="mini-stat">
                <span class="stat-label">${escapeHtml(stat.label)}</span>
                <strong>${escapeHtml(stat.value)}</strong>
                <span class="muted">${escapeHtml(stat.detail)}</span>
              </article>
            `,
          )
          .join("")}
      </div>
    </div>
  `;

  refs.recommendationsCard.innerHTML = renderPillList(
    (matches
      .slice(0, 4)
      .map((match) => `${match.property?.title || match.title || "Bien"} · score ${match.score ?? match.score_percent ?? "n/a"}`)
      .concat(recommendationText)
      .slice(0, 4)) || [],
    statsCopy.noRecommendation,
  );

  refs.nextActionsCard.innerHTML = renderPillList(
    nextActionText.concat(currentProject ? [`${state.language === "fr" ? "Poursuivre" : "Continue"} ${currentProject.title}`] : []).slice(0, 4),
    statsCopy.noSuggestion,
  );

  refs.supportCard.innerHTML = `
    <div class="cockpit-stack">
      <p class="muted">${escapeHtml(supportHint)}</p>
      ${renderPillList(supportText, statsCopy.noCategory)}
      <div class="action-link-grid">
        <a class="button primary action-link" href="#message-form">${escapeHtml(statsCopy.openModule)}</a>
        <a class="button secondary action-link" href="#notification-filter-form">${escapeHtml(statsCopy.viewNotifications)}</a>
      </div>
    </div>
  `;

  traceRuntime("DASHBOARD_RENDERED", {
    role,
    journey: role,
    progress,
    unread: unread.length,
    projects: projects.length,
  });
  traceRuntime("ROLE_DASHBOARD_RENDERED", {
    role,
    journey: role,
    visible: true,
  });
}

function renderOrganizations(items) {
  renderList(refs.organizationsList, items, (organization) => {
    const article = document.createElement("article");
    article.className = "mini-card";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(organization.name)}</strong>
        <span class="chip subtle">${escapeHtml(organization.kind)}</span>
      </div>
      <p class="muted">${escapeHtml(organization.slug)}</p>
      <p>${escapeHtml(organization.city || "Aucune ville")} · ${organization.user_count ?? 0} utilisateurs</p>
    `;
    return article;
  }, { fr: "Aucune organisation disponible.", en: "No organization available.", pidgin: "No organization available." });

  const options = [`<option value="">${state.language === "fr" ? "Aucune" : "None"}</option>`]
    .concat(items.map((organization) => `<option value="${organization.id}">${escapeHtml(organization.name)}</option>`))
    .join("");
  refs.ownerOrganizationSelect.innerHTML = options;
  if (refs.registerOrganizationSelect) {
    refs.registerOrganizationSelect.innerHTML = options;
  }
  if (refs.adminOrganizationSelect) {
    refs.adminOrganizationSelect.innerHTML = [`<option value="">${state.language === "fr" ? "Sélectionner une organisation" : "Select an organization"}</option>`]
      .concat(items.map((organization) => `<option value="${organization.id}">${escapeHtml(organization.name)}</option>`))
      .join("");
  }
}

function renderProjects(items) {
  if (!refs.projectsList) {
    return;
  }
  renderList(refs.projectsList, items, (project) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--project";
    const budget = project.budget || {};
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(project.title)}</strong>
        <span class="${statusChipClass(project.status)}">${escapeHtml(project.status)}</span>
      </div>
      <p class="muted">${escapeHtml(project.project_type)} · ${project.progress_percent ?? 0}% · ${escapeHtml(project.priority || "normal")}</p>
      <p>${escapeHtml(project.location?.city || "—")} · ${money(budget.min, budget.currency)} - ${money(budget.max, budget.currency)}</p>
      <p class="muted">${escapeHtml(project.objective || "")}</p>
    `;
    article.addEventListener("click", () => selectProject(project.id));
    return article;
  }, state.token ? { fr: "Aucun projet pour le moment. Créez-en un depuis le panneau.", en: "No projects yet. Create one from the panel.", pidgin: "No projects yet. Create one from the panel." } : { fr: "Connectez-vous pour voir les projets.", en: "Sign in to view projects.", pidgin: "Sign in to view projects." });
}

async function refreshEcosystemLists() {
  if (!state.token) {
    renderList(refs.partnersList, [], () => document.createElement("div"), { fr: "Connectez-vous pour charger les partenaires.", en: "Sign in to load partners.", pidgin: "Sign in to load partners." });
    renderList(refs.servicesList, [], () => document.createElement("div"), { fr: "Connectez-vous pour charger les services.", en: "Sign in to load services.", pidgin: "Sign in to load services." });
    return;
  }
  try {
    const [partnersPayload, servicesPayload] = await Promise.all([
      api("/api/v2/partners", { auth: true, query: { limit: 8 } }),
      api("/api/v2/services", { auth: true, query: { limit: 8 } }),
    ]);
    renderList(refs.partnersList, partnersPayload.partners || [], (partner) => {
      const article = document.createElement("article");
      article.className = "mini-card";
      article.innerHTML = `
        <strong>${escapeHtml(partner.display_name)}</strong>
        <p class="muted">${escapeHtml(partner.partner_type)} · Trust ${partner.trust_score ?? "n/a"}</p>
      `;
      return article;
    }, { fr: "Aucun partenaire dans l'annuaire.", en: "No partner in the directory.", pidgin: "No partner in the directory." });
    renderList(refs.servicesList, servicesPayload.services || [], (service) => {
      const article = document.createElement("article");
      article.className = "mini-card";
      const pricing = service.pricing || {};
      article.innerHTML = `
        <strong>${escapeHtml(service.title)}</strong>
        <p class="muted">${escapeHtml(service.category)} · ${money(pricing.min, pricing.currency)} - ${money(pricing.max, pricing.currency)}</p>
      `;
      return article;
    }, { fr: "Aucun service dans le catalogue.", en: "No service in the catalog.", pidgin: "No service in the catalog." });
  } catch (error) {
    renderList(refs.partnersList, [], () => document.createElement("div"), error.message);
  }
}

async function selectProject(projectId) {
  if (!state.token || !refs.projectDetail) {
    return;
  }
  state.selectedProjectId = projectId;
  try {
    const [payload, orchPayload, matchPayload, wfPayload, graphPayload, intelPayload, nbaPayload, risksPayload, oppPayload] = await Promise.all([
      api(`/api/v2/projects/${projectId}/workspace`, { auth: true }),
      api(`/api/v2/projects/${projectId}/orchestration`, { auth: true }),
      api(`/api/v2/matching?project_id=${projectId}`, { auth: true }),
      api(`/api/v2/projects/${projectId}/workflows`, { auth: true }),
      api("/api/v2/knowledge/graph", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/intelligence", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/next-actions", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/risks", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/opportunities", { auth: true, query: { project_id: projectId } }),
    ]);
    const workspace = payload.workspace || payload;
    const orchestration = orchPayload.orchestration || {};
    const matches = matchPayload.matches || [];
    const workflow = wfPayload.workflow_instance || {};
    const graph = graphPayload.graph || {};
    const cognitionIntel = intelPayload.intelligence || {};
    const nextAction = nbaPayload.next_action || {};
    const cognitionRisks = risksPayload.risks || [];
    const cognitionOpportunities = oppPayload.opportunities || [];
    const project = workspace.project;
    const progress = workspace.progress || {};
    const stepsHtml = (workspace.steps || [])
      .map(
        (step) => `
          <article class="message">
            <div class="message__meta">
              <strong>${escapeHtml(step.title)}</strong>
              <span class="chip subtle">${escapeHtml(step.status)}</span>
            </div>
            <p class="muted">${escapeHtml(step.milestone || "")} · ${escapeHtml(step.next_action || "")}</p>
          </article>
        `,
      )
      .join("");
    const goalsHtml = (workspace.goals || [])
      .slice(0, 5)
      .map((goal) => `<li>${escapeHtml(goal.title || goal.goal_key)} · ${escapeHtml(goal.status || "active")}</li>`)
      .join("");
    const timeline = workspace.timeline || {};
    const timelineHtml = (timeline.past_events || timeline.history || [])
      .slice(0, 4)
      .map((entry) => `<li>${escapeHtml(entry.title || entry.to_status || entry.kind || "Event")}</li>`)
      .join("");
    const tasksHtml = (workspace.tasks || [])
      .slice(0, 5)
      .map((task) => `<li>${escapeHtml(task.title)} · ${escapeHtml(task.status || "pending")}</li>`)
      .join("");
    const lifeEventsHtml = (workspace.life_events || [])
      .slice(0, 4)
      .map((event) => `<li>${escapeHtml(event.title || event.event_type)}</li>`)
      .join("");
    const graphNodesHtml = (graph.nodes || [])
      .slice(0, 6)
      .map((node) => `<li>${escapeHtml(node.title || node.node_key)} · ${escapeHtml(node.node_type || "")}</li>`)
      .join("");
    const cognitionRisksHtml = cognitionRisks
      .slice(0, 4)
      .map((risk) => `<li>${escapeHtml(risk.risk_key || "risk")} · score ${risk.score ?? "n/a"}</li>`)
      .join("");
    const cognitionOpportunitiesHtml = cognitionOpportunities
      .slice(0, 4)
      .map((item) => `<li>${escapeHtml(item.opportunity_key || "opportunity")} · ${item.opportunity_score ?? "n/a"}</li>`)
      .join("");
    const knowledgeHtml = (workspace.knowledge || [])
      .slice(0, 4)
      .map((fact) => `<li>${escapeHtml(fact.title)} · ${escapeHtml(fact.category || "")}</li>`)
      .join("");
    const actionsListHtml = (workspace.actions || [])
      .slice(0, 4)
      .map((action) => `<li>${escapeHtml(action.title)} · ${escapeHtml(action.status || "pending")}</li>`)
      .join("");
    const recommendationsHtml = (workspace.recommendations || workspace.next_actions || [])
      .slice(0, 3)
      .map((action) => `<li>${escapeHtml(action.title || action.next_action || "Action")}</li>`)
      .join("");
    const partnerMatchesHtml = matches
      .filter((m) => m.match_type === "partner" || m.partner)
      .slice(0, 4)
      .map((m) => {
        const label = m.partner?.display_name || m.partner_type || "Partner";
        return `<li>${escapeHtml(label)} · score ${m.score} · ${escapeHtml((m.rationale?.[0]?.label) || "")}</li>`;
      })
      .join("");
    const serviceMatchesHtml = matches
      .filter((m) => m.match_type === "service" || m.service)
      .slice(0, 4)
      .map((m) => {
        const label = m.service?.title || m.service_key || "Service";
        return `<li>${escapeHtml(label)} · score ${m.score}</li>`;
      })
      .join("");
    const interventionsHtml = (orchestration.planning || [])
      .slice(0, 4)
      .map((item) => `<li>${escapeHtml(item.title || item.type)} · ${escapeHtml(item.status || "")}</li>`)
      .join("");
    refs.projectDetail.innerHTML = `
      <div class="detail-summary">
        <div>
          <p class="eyebrow">${escapeHtml(project.project_type)} project</p>
          <h3>${escapeHtml(project.title)}</h3>
          <p>${escapeHtml(project.objective)}</p>
          <p class="muted">Progress ${progress.progress_percent ?? 0}% · ${progress.steps_completed ?? 0}/${progress.steps_total ?? 0} steps · Journey ${escapeHtml(workspace.journey?.status || workspace.journey_state?.status || "active")}</p>
        </div>
      </div>
      <div class="detail-grid">
        <section>
          <h4>Ecosystem — partner matches</h4>
          <ul>${partnerMatchesHtml || "<li class='muted'>No partner matches</li>"}</ul>
        </section>
        <section>
          <h4>Ecosystem — service matches</h4>
          <ul>${serviceMatchesHtml || "<li class='muted'>No service matches</li>"}</ul>
        </section>
        <section>
          <h4>Workflow</h4>
          <p class="muted">${escapeHtml(workflow.status || "—")} · ${workflow.progress_percent ?? 0}% · step ${escapeHtml(workflow.current_step_key || "—")}</p>
        </section>
        <section>
          <h4>Interventions</h4>
          <ul>${interventionsHtml || "<li class='muted'>No interventions planned</li>"}</ul>
        </section>
        <section>
          <h4>Orchestration</h4>
          <p class="muted">${orchestration.partners_engaged ?? 0} partners · ${orchestration.services_recommended ?? 0} services · ${money(orchestration.cost_summary?.estimated, orchestration.cost_summary?.currency)} estimated</p>
        </section>
        <section>
          <h4>Goals</h4>
          <ul>${goalsHtml || "<li class='muted'>No goals</li>"}</ul>
        </section>
        <section>
          <h4>Recommendations</h4>
          <ul>${recommendationsHtml || "<li class='muted'>No recommendations</li>"}</ul>
        </section>
        <section>
          <h4>Intelligence</h4>
          <p class="muted">Blockers: ${workspace.intelligence?.blockers?.open_high_risks ?? 0} high risks · Trust ${workspace.trust_score?.score ?? "n/a"}</p>
          <p class="muted">Priorities: ${escapeHtml((workspace.intelligence?.priorities || []).slice(0, 2).join(" · ") || "—")}</p>
        </section>
        <section>
          <h4>Timeline</h4>
          <ul>${timelineHtml || "<li class='muted'>No timeline entries</li>"}</ul>
        </section>
        <section>
          <h4>Actions</h4>
          <ul>${actionsListHtml || "<li class='muted'>No actions</li>"}</ul>
        </section>
        <section>
          <h4>Tasks</h4>
          <ul>${tasksHtml || "<li class='muted'>No tasks</li>"}</ul>
        </section>
        <section>
          <h4>Life events</h4>
          <ul>${lifeEventsHtml || "<li class='muted'>No life events</li>"}</ul>
        </section>
        <section>
          <h4>Knowledge graph</h4>
          <p class="muted">${(graph.nodes || []).length} nodes · ${(graph.edges || []).length} edges</p>
          <ul>${graphNodesHtml || "<li class='muted'>No graph nodes</li>"}</ul>
        </section>
        <section>
          <h4>Decision platform</h4>
          <p class="muted">${escapeHtml(nextAction.title || "—")} · confidence ${nextAction.confidence ?? "n/a"}</p>
          <p class="muted">${escapeHtml(nextAction.justification || cognitionIntel.snapshot?.decision?.reason || "—")}</p>
        </section>
        <section>
          <h4>Next best action</h4>
          <p class="muted">${escapeHtml(nextAction.title || "—")} · score ${nextAction.score ?? "n/a"}</p>
        </section>
        <section>
          <h4>Risk intelligence</h4>
          <ul>${cognitionRisksHtml || "<li class='muted'>No risk scores</li>"}</ul>
        </section>
        <section>
          <h4>Opportunity intelligence</h4>
          <ul>${cognitionOpportunitiesHtml || "<li class='muted'>No opportunities scored</li>"}</ul>
        </section>
        <section>
          <h4>Knowledge</h4>
          <ul>${knowledgeHtml || "<li class='muted'>No knowledge facts</li>"}</ul>
        </section>
      </div>
      <h4>Journey steps</h4>
      <div class="message-stream">${stepsHtml}</div>
    `;
  } catch (error) {
    refs.projectDetail.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
  await refreshAssistant(state.selectedProjectId);
}

async function refreshAssistant(projectId) {
  if (!state.token || !projectId || !refs.assistantSummary) {
    if (refs.assistantForm) {
      refs.assistantForm.classList.add("hidden");
    }
    return;
  }
  try {
    const [agentsPayload, messagesPayload] = await Promise.all([
      api("/api/v2/assistant/agents", { auth: true }),
      api(`/api/v2/assistant/sessions?project_id=${projectId}`, { auth: true }),
    ]);
    const sessions = messagesPayload.sessions || [];
    const session = sessions[0];
    state.assistantSessionId = session?.id || null;
    refs.assistantSummary.innerHTML = `
      <p class="muted">${(agentsPayload.agents || []).length} agents · session ${session?.session_key || "new"}</p>
    `;
    refs.assistantForm?.classList.remove("hidden");
    if (session?.id) {
      const msgPayload = await api(
        `/api/v2/assistant/messages?project_id=${projectId}&session_id=${session.id}`,
        { auth: true },
      );
      const messages = msgPayload.messages || [];
      if (refs.assistantChat) {
        refs.assistantChat.innerHTML = messages
          .map(
            (msg) => `
              <article class="message">
                <div class="message__meta"><strong>${escapeHtml(msg.role)}</strong></div>
                <p>${escapeHtml(msg.content)}</p>
              </article>
            `,
          )
          .join("") || "<p class='muted'>No assistant messages yet.</p>";
      }
    } else if (refs.assistantChat) {
      refs.assistantChat.innerHTML = "<p class='muted'>No assistant messages yet.</p>";
    }
  } catch (error) {
    refs.assistantSummary.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleAssistantChat(event) {
  event.preventDefault();
  if (!state.token || !state.selectedProjectId || !refs.assistantForm) {
    return;
  }
  const form = new FormData(refs.assistantForm);
  const message = String(form.get("message") || "").trim();
  if (!message) {
    return;
  }
  try {
    const body = { project_id: state.selectedProjectId, message };
    if (state.assistantSessionId) {
      body.session_id = state.assistantSessionId;
    }
    await api("/api/v2/assistant/chat", { auth: true, method: "POST", body });
    refs.assistantForm.reset();
    await refreshAssistant(state.selectedProjectId);
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function refreshProjects() {
  if (!state.token || !refs.projectsList) {
    renderProjects([]);
    return;
  }
  try {
    const payload = await api("/api/v2/projects", { auth: true, query: { limit: 20 } });
    renderProjects(payload.projects || []);
    if (state.selectedProjectId) {
      await selectProject(state.selectedProjectId);
    }
  } catch (error) {
    renderProjects([]);
  }
}

function renderProperties(items) {
  const mediaOptions = [`<option value="">${state.language === "fr" ? "Sélectionner un bien" : "Select a listing"}</option>`]
    .concat(
      (items || []).map((property) => {
        const label = property.listing_code || property.title;
        return `<option value="${property.id}">${escapeHtml(label)}</option>`;
      }),
    )
    .join("");
  refs.mediaPropertySelect.innerHTML = mediaOptions;

  renderList(refs.propertiesList, items, (property) => {
    const price = propertyPrice(property);
    const geo = propertyGeo(property);
    const coords = geo.coordinates || {};
    const article = document.createElement("article");
    article.className = "mini-card mini-card--property";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(property.title)}</strong>
        <span class="${statusChipClass(property.status)}" data-status="${escapeHtml(property.status || "draft")}">${escapeHtml(property.status || "draft")}</span>
      </div>
      <p class="muted">${escapeHtml(property.listing_code || "sans-code")} · ${escapeHtml(property.property_type || "n/d")} · ${escapeHtml(property.availability || "disponible")}</p>
      <p>${escapeHtml(geo.city || (state.language === "fr" ? "n/d" : "n/a"))}, ${escapeHtml(geo.region || "—")}, ${escapeHtml(geo.country || (state.language === "fr" ? "n/d" : "n/a"))}</p>
      <p>${money(price.min, price.currency)} - ${money(price.max, price.currency)}</p>
      <p class="muted">${state.language === "fr" ? "Coordonnées" : "Coordinates"}: ${coords.latitude ?? "—"}, ${coords.longitude ?? "—"}</p>
      <p class="muted">${state.language === "fr" ? "Propriétaire" : "Owner"}: ${escapeHtml(property.ownership?.organization_name || property.owner_organization_name || (state.language === "fr" ? "n/d" : "n/a"))} · ${state.language === "fr" ? "Médias" : "Media"}: ${property.media_count ?? 0}</p>
      <p>${escapeHtml(property.summary || "")}</p>
    `;
    article.addEventListener("click", () => {
      state.selectedPropertyId = property.id;
      state.selectedPropertyVersion = property.version;
      state.selectedPropertyTitle = property.title;
      updateSelectedPropertyLabel();
      setNotice(state.language === "fr" ? `Bien sélectionné #${property.id} (${property.title})` : `Selected property #${property.id} (${property.title})`, "neutral");
    });
    return article;
  }, { fr: "Aucun bien disponible.", en: "No listing available.", pidgin: "No listing available." });
}

function renderMedia(items) {
  renderList(refs.mediaList, items, (media) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--media";
    const preview =
      media.mime_type?.startsWith("image/") && media.url
        ? `<img class="media-preview" src="${escapeHtml(media.url)}" alt="${escapeHtml(media.caption || media.kind)}" loading="lazy">`
        : "";
    article.innerHTML = `
      ${preview}
      <div class="mini-card__header">
        <strong>${escapeHtml(media.caption || media.kind)}</strong>
        <span class="chip subtle">${escapeHtml(media.kind)}</span>
      </div>
      <p class="muted">${escapeHtml(media.property_title || `${state.language === "fr" ? "Bien" : "Property"} #${media.property_id}`)}</p>
      <p>${escapeHtml(media.mime_type || (state.language === "fr" ? "inconnu" : "unknown"))} · ${media.size_bytes ?? 0} ${state.language === "fr" ? "octets" : "bytes"}</p>
      <p class="muted">${escapeHtml(media.url)}</p>
    `;
    return article;
  }, { fr: "Aucun média disponible.", en: "No media available.", pidgin: "No media available." });
}

function renderMatches(items) {
  renderList(refs.matchesList, items, (match) => {
    const property = match.property;
    const price = propertyPrice(property);
    const geo = propertyGeo(property);
    const breakdown = match.breakdown || {};
    const breakdownText = Object.entries(breakdown)
      .map(([key, value]) => `${key}:${value}`)
      .join(" · ");
    const article = document.createElement("article");
    article.className = "mini-card mini-card--match";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(property.title)}</strong>
        <span class="chip accent">${match.score} · ${escapeHtml(match.grade || "n/a")}</span>
      </div>
      <p class="muted">${escapeHtml(geo.city || property.city)}, ${escapeHtml(geo.country || property.country)}</p>
      <p>${money(price.min, price.currency)} - ${money(price.max, price.currency)}</p>
      <p class="muted">${escapeHtml(match.summary || (match.reasons || []).join(" · ") || (state.language === "fr" ? "Aucun résumé." : "No summary."))}</p>
      <p class="muted breakdown">${escapeHtml(breakdownText || (state.language === "fr" ? "Aucun détail de score." : "No score breakdown."))}</p>
    `;
    return article;
  }, { fr: "Aucun résultat de matching pour le moment.", en: "No matching result yet.", pidgin: "No matching result yet." });
}

function conversationRequester(conversation) {
  return conversation.requester?.full_name || conversation.requester_name || "n/a";
}

function conversationPropertyTitle(conversation) {
  return conversation.property?.title || conversation.property_title || "n/a";
}

function messageSenderName(message) {
  return message.sender?.full_name || message.sender_name || "n/a";
}

function renderConversationDetail(conversation) {
  const messages = conversation.messages || [];
  const negotiation = conversation.negotiation || {};
  const allowedStages = negotiation.allowed_stages || [];
  refs.conversationDetail.innerHTML = `
    <div class="detail-summary">
      <div>
        <p class="eyebrow">
          <span class="chip subtle" data-status="${escapeHtml(conversation.status)}">${escapeHtml(conversation.status)}</span>
          <span class="chip accent">${escapeHtml(conversation.negotiation_stage || negotiation.stage || (state.language === "fr" ? "demande" : "inquiry"))}</span>
        </p>
        <h3>${escapeHtml(conversation.subject)}</h3>
          <p class="muted">
          ${state.language === "fr" ? "Demandeur" : "Requester"}: ${escapeHtml(conversationRequester(conversation))} · ${state.language === "fr" ? "Bien" : "Property"}: ${escapeHtml(conversationPropertyTitle(conversation))}
        </p>
      </div>
      <div class="detail-badge">
        <span>${state.language === "fr" ? "Messages" : "Messages"}</span>
        <strong>${conversation.message_count ?? messages.length}</strong>
      </div>
    </div>
    <div class="message-stream">
      ${messages
        .map(
          (message) => `
            <article class="message">
              <div class="message__meta">
                <strong>${escapeHtml(messageSenderName(message))}</strong>
                <span class="muted">${escapeHtml(message.created_at)}</span>
              </div>
              <p>${escapeHtml(message.body)}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
    refs.messageForm.classList.toggle("hidden", !state.token);
  if (refs.negotiationForm) {
    const stageSelect = refs.negotiationForm.querySelector('[name="negotiation_stage"]');
    if (stageSelect) {
      stageSelect.innerHTML = allowedStages
        .map((stage) => `<option value="${stage}" ${stage === (conversation.negotiation_stage || "inquiry") ? "selected" : ""}>${escapeHtml(stage)}</option>`)
        .join("");
    }
    refs.negotiationForm.classList.toggle("hidden", !state.token || !allowedStages.length);
  }
}

function renderNotifications(items) {
  const unread = (items || []).filter((notification) => !notification.read).length;
  if (refs.notificationUnreadCount) {
    refs.notificationUnreadCount.textContent = state.language === "fr" ? `${unread} non lues` : `${unread} unread`;
    refs.notificationUnreadCount.dataset.tone = unread ? "warn" : "ok";
  }
  renderList(refs.notificationsList, items, (notification) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--notification";
    if (!notification.read) {
      article.dataset.unread = "true";
    }
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(notification.title)}</strong>
        <span class="chip subtle">${escapeHtml(notification.kind)}</span>
      </div>
      <p>${escapeHtml(notification.body)}</p>
      <p class="muted">${notification.read ? (state.language === "fr" ? "lu" : "read") : (state.language === "fr" ? "non lu" : "unread")} · ${escapeHtml(notification.created_at || "")}</p>
    `;
    article.addEventListener("click", () => markNotificationRead(notification.id));
    return article;
  }, { fr: "Aucune notification pour le moment.", en: "No notifications yet.", pidgin: "No notifications yet." });
}

async function refreshNotifications() {
  if (!state.token) {
    renderNotifications([]);
    return;
  }
  const form = refs.notificationFilterForm ? new FormData(refs.notificationFilterForm) : null;
  const payload = await api("/api/notifications", {
    auth: true,
    query: {
      limit: 20,
      kind: form?.get("kind") || undefined,
      unread_only: form?.get("unread_only") ? "true" : undefined,
    },
  });
  renderNotifications(payload.notifications || []);
}

async function markNotificationRead(notificationId) {
  if (!state.token) {
    return;
  }
  try {
    await api(`/api/notifications/${notificationId}/read`, { method: "PATCH", auth: true, body: {} });
    await refreshNotifications();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function markAllNotificationsRead() {
  if (!state.token) {
    return;
  }
  try {
    await api("/api/notifications/read-all", { method: "POST", auth: true, body: {} });
    await refreshNotifications();
    setNotice(state.language === "fr" ? "Toutes les notifications sont marquées comme lues." : "All notifications marked as read.", "ok");
  } catch (error) {
    setNotice(error.message, "error");
  }
}

function renderConversations(items) {
  renderList(refs.conversationsList, items, (conversation) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--conversation";
    if (conversation.id === state.selectedConversationId) {
      article.dataset.active = "true";
    }
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(conversation.subject)}</strong>
        <span class="chip subtle">${escapeHtml(conversation.status)} · ${escapeHtml(conversation.negotiation_stage || "inquiry")}</span>
      </div>
      <p class="muted">${escapeHtml(conversationRequester(conversation))} · ${escapeHtml(conversationPropertyTitle(conversation))}</p>
      <p>${escapeHtml(conversation.last_message || (state.language === "fr" ? "Aucun message pour le moment." : "No message yet."))}</p>
    `;
    article.addEventListener("click", () => selectConversation(conversation.id));
    return article;
  }, { fr: "Aucune conversation disponible.", en: "No conversation available.", pidgin: "No conversation available." });
}

function updateSelectedPropertyLabel() {
  if (!refs.selectedPropertyLabel) {
    return;
  }
  if (!state.selectedPropertyId) {
    refs.selectedPropertyLabel.textContent = "Aucun bien sélectionné.";
    return;
  }
  refs.selectedPropertyLabel.textContent = `#${state.selectedPropertyId} · ${state.selectedPropertyTitle || "Bien"} · v${state.selectedPropertyVersion ?? "?"}`;
}

function applyJourney(journey) {
  traceRuntime("APPLY_JOURNEY", { journey });
  state.activeJourney = journey;
  localStorage.setItem("lawim.journey", journey);
  updateAuthShell(Boolean(state.token));
  syncWorkspaceVisibility();
  if (journey === "admin" && state.token) {
    loadAdminDashboard();
  }
  traceRuntime("RENDER_DONE", {
    journey,
    adminDashboardVisible: Boolean(refs.adminDashboard && !refs.adminDashboard.hidden),
  });
}

function journeyForRole(role) {
  const normalizedRole = normalizeAccessRole(role);
  return normalizedRole || "user";
}

async function loadAdminDashboard() {
  if (!refs.adminDashboard || !state.token) {
    return;
  }
  try {
    const [metrics, events] = await Promise.all([
      api("/api/metrics", { auth: true }),
      api("/api/events?limit=10", { auth: true }),
    ]);
    const counters = metrics.metrics || {};
    refs.adminDashboard.innerHTML = `
      <div class="detail-summary">
        <div>
          <p class="eyebrow">Runtime metrics</p>
          <p>Requests ${counters.requests_total ?? 0} · Matches ${counters.matches_total ?? 0} · Conversations ${counters.conversations_total ?? 0}</p>
        </div>
      </div>
      <div class="message-stream">
        ${(events.events || [])
          .map(
            (event) => `
              <article class="message">
                <div class="message__meta">
                  <strong>${escapeHtml(event.kind)}</strong>
                  <span class="muted">${escapeHtml(event.created_at)}</span>
                </div>
              </article>
            `,
          )
          .join("")}
      </div>
    `;
    traceRuntime("DASHBOARD_RENDERED", {
      journey: state.activeJourney,
      adminDashboardVisible: Boolean(refs.adminDashboard && !refs.adminDashboard.hidden),
    });
  } catch (error) {
    refs.adminDashboard.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

function renderHealth(health) {
  const environment = health.environment || {};
  const database = health.database || {};
  setRuntimeChip(`${health.status.toUpperCase()} · ${environment.app_env || "unknown"}`, health.status === "ok" ? "ok" : "warn");
  const metricsNote = health.metrics ? `${health.metrics.requests_total ?? 0} requêtes` : "métriques réservées aux administrateurs";
  refs.bootstrapSummary.textContent = `Pilote ${environment.db_driver || database.driver || "sqlite"} · schéma v${database.schema_version ?? "?"} · ${health.summary?.events ?? 0} événements · ${metricsNote}.`;
}

function renderBootstrap(payload) {
  state.bootstrap = payload;
  const currentUser = payload.current_user;

  if (currentUser) {
    const resolvedRole = resolveAccessRole(currentUser.role, currentUser.roles || payload.roles || []);
    state.activeJourney = journeyForRole(resolvedRole);
    refs.currentUser.textContent = `${currentUser.full_name || currentUser.name || "Utilisateur"} · ${roleLabel(resolvedRole)}`;
    refs.logoutButton.disabled = false;
    if (refs.roleCockpit) {
      refs.roleCockpit.hidden = false;
    }
    renderRoleCockpit(currentUser, payload);
    renderModuleDeck(currentUser);
    refreshModuleChrome();
  } else {
    refs.currentUser.textContent = uiCopy().session;
    refs.logoutButton.disabled = !state.token;
    if (refs.roleCockpit) {
      refs.roleCockpit.hidden = true;
    }
    if (refs.journeyNav) {
      refs.journeyNav.replaceChildren();
    }
  }

  updateAuthShell(Boolean(state.token && currentUser));
  translateStaticShell();

  renderSummary(payload.summary || {});
  renderOrganizations(payload.organizations || []);
  renderProperties(payload.properties || []);
  renderMedia(payload.media || []);
  renderMatches(payload.matches || []);
  renderConversations(payload.conversations || []);
  renderNotifications(payload.notifications || []);

  if (state.token && !currentUser) {
    clearSession();
  }

  if (!state.selectedConversationId && (payload.conversations || []).length) {
    selectConversation(payload.conversations[0].id);
  } else if (state.selectedConversationId) {
    const current = (payload.conversations || []).find((conversation) => conversation.id === state.selectedConversationId);
    if (current) {
      selectConversation(current.id);
    } else {
      state.selectedConversationId = null;
      refs.conversationDetail.innerHTML = `<p class="muted">${escapeHtml(state.language === "fr" ? "Aucune conversation sélectionnée." : "No conversation selected.")}</p>`;
    }
  }
}

async function selectConversation(conversationId) {
  state.selectedConversationId = conversationId;
  try {
    const payload = await api(`/api/conversations/${conversationId}`, { auth: true });
    renderConversationDetail(payload.conversation);
    renderConversations(state.bootstrap?.conversations || []);
  } catch (error) {
    state.selectedConversationId = null;
    refs.conversationDetail.innerHTML = `<p class="muted">${error.message}</p>`;
    setNotice(error.message, "error", error.code || "");
  }
}

function parseNumber(value) {
  if (value === "" || value === null || value === undefined) {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

async function refresh({ renderJourney = true } = {}) {
  if (state.refreshInFlight) {
    return;
  }
  state.refreshInFlight = true;
  traceRuntime("REFRESH_START", {
    token: Boolean(state.token),
    journey: state.activeJourney,
    renderJourney,
  });
  setLoading(true, RUNTIME_COPY[state.language]?.refreshing || RUNTIME_COPY.fr.refreshing);
  let refreshError = null;
  try {
    const healthPromise = api("/api/health", { auth: Boolean(state.token) });
    const bootstrapPromise = api("/api/bootstrap", { auth: Boolean(state.token) });
    const [health, bootstrap] = await Promise.all([healthPromise, bootstrapPromise]);
    state.health = health;
    try {
      renderHealth(health);
    } catch (error) {
      refreshError = error;
      setRuntimeChip("DEGRADED", "warn");
    }
    renderBootstrap(bootstrap);
    await refreshProjects();
    await refreshEcosystemLists();
    await refreshKnowledgeAdmin();
    await refreshReiAdmin();
    await refreshCrmAdmin();
    await refreshCommunicationAdmin();
    await refreshAnalyticsAdmin();
    await refreshSourceIntelligenceAdmin();
    await refreshSecurityAdmin();
    await refreshMarketplaceAdmin();
    await refreshWorkflowAdmin();
    if (renderJourney) {
      applyJourney(state.activeJourney);
    }
    setNotice(RUNTIME_COPY[state.language]?.ready || RUNTIME_COPY.fr.ready, "success");
  } catch (error) {
    refreshError = error;
    const sessionError = formatSessionError(error);
    if (sessionError.clearToken) {
      clearSession();
    }
    setNotice(sessionError.message, sessionError.tone, error.code || "");
    setRuntimeChip("DEGRADED", "warn");
  } finally {
    traceRuntime("REFRESH_DONE", {
      token: Boolean(state.token),
      journey: state.activeJourney,
      renderJourney,
      error: refreshError ? refreshError.message : null,
    });
    state.refreshInFlight = false;
    setLoading(false);
  }
}

async function refreshKnowledgeAdmin() {
  if (!state.token || !refs.knowledgeAdminStats) {
    return;
  }
  try {
    const [statsPayload, docsPayload, catsPayload] = await Promise.all([
      api("/api/v2/knowledge/stats", { auth: true }),
      api("/api/v2/knowledge/documents", { auth: true }),
      api("/api/v2/knowledge/categories", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    refs.knowledgeAdminStats.innerHTML = `
      <p class="muted">${stats.documents ?? 0} documents · ${stats.chunks ?? 0} chunks · ${stats.categories ?? 0} categories</p>
    `;
    refs.knowledgeSearchForm?.classList.remove("hidden");
    const docs = docsPayload.documents || [];
    refs.knowledgeAdminList.innerHTML = docs
      .slice(0, 8)
      .map(
        (doc) => `
          <article class="mini-card">
            <strong>${escapeHtml(doc.title)}</strong>
            <p class="muted">${escapeHtml(doc.status || "draft")} · ${escapeHtml(doc.format || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No expert documents.</p>";
  } catch (error) {
    refs.knowledgeAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleKnowledgeSearch(event) {
  event.preventDefault();
  if (!state.token || !refs.knowledgeSearchForm) {
    return;
  }
  const query = String(new FormData(refs.knowledgeSearchForm).get("query") || "").trim();
  if (!query) {
    return;
  }
  try {
    const payload = await api(`/api/v2/knowledge/search?q=${encodeURIComponent(query)}`, { auth: true });
    const results = payload.results || [];
    refs.knowledgeSearchResults.innerHTML = results
      .map(
        (row) => `
          <article class="message">
            <div class="message__meta"><strong>${escapeHtml(row.title || "Result")}</strong> · score ${row.score ?? 0}</div>
            <p class="muted">${escapeHtml(row.snippet || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No results.</p>";
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function refreshCommunicationAdmin() {
  if (!state.token || !refs.communicationAdminStats) {
    return;
  }
  try {
    const [statsPayload, messagesPayload, channelsPayload] = await Promise.all([
      api("/api/v2/communication/statistics", { auth: true }),
      api("/api/v2/communication/messages", { auth: true }),
      api("/api/v2/communication/channels", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    refs.communicationAdminStats.innerHTML = `
      <p class="muted">${stats.messages ?? 0} messages · ${stats.notifications ?? 0} notifications · ${stats.queue_pending ?? 0} queue pending · ${stats.campaigns ?? 0} campaigns</p>
    `;
    const messages = messagesPayload.messages || [];
    refs.communicationAdminList.innerHTML = messages
      .slice(0, 6)
      .map(
        (message) => `
          <article class="mini-card">
            <strong>${escapeHtml(message.subject || message.channel_type || "Message")}</strong>
            <p class="muted">${escapeHtml(message.status || "")} · ${escapeHtml(message.channel_type || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No communication messages loaded.</p>";
    const channels = channelsPayload.channels || [];
    if (channels.length && refs.communicationAdminList) {
      const channelSummary = channels
        .slice(0, 3)
        .map((channel) => escapeHtml(channel.name || channel.channel_type || ""))
        .join(" · ");
      if (channelSummary) {
        refs.communicationAdminStats.innerHTML += `<p class="muted">${state.language === "fr" ? "Canaux" : "Channels"}: ${channelSummary}</p>`;
      }
    }
  } catch (error) {
    refs.communicationAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function refreshAnalyticsAdmin() {
  if (!state.token || !refs.analyticsAdminStats) {
    return;
  }
  try {
    const [statsPayload, executivePayload, integrationsPayload] = await Promise.all([
      api("/api/v2/analytics/statistics", { auth: true }),
      api("/api/v2/analytics/executive", { auth: true }),
      api("/api/v2/analytics/integrations", { auth: true }),
    ]);
    const stats = statsPayload.statistics || {};
    refs.analyticsAdminStats.innerHTML = `
      <p class="muted">${stats.total_kpis ?? 0} ${state.language === "fr" ? "KPI" : "KPI"} · ${stats.dashboards_active ?? 0} ${state.language === "fr" ? "tableaux de bord" : "dashboards"} · ${stats.reports_generated ?? 0} ${state.language === "fr" ? "rapports" : "reports"} · ${stats.exports_completed ?? 0} ${state.language === "fr" ? "exports" : "exports"} · ${stats.ai_insights ?? 0} ${state.language === "fr" ? "analyses IA" : "AI insights"} · ${state.language === "fr" ? "santé" : "health"} ${stats.platform_health_score ?? 0}</p>
    `;
    const executive = executivePayload.executive || {};
    const kpis = executive.kpis || [];
    refs.analyticsAdminList.innerHTML = kpis
      .slice(0, 6)
      .map(
        (kpi) => `
          <article class="mini-card">
            <strong>${escapeHtml(kpi.name || kpi.kpi_key || "KPI")}</strong>
            <p class="muted">${escapeHtml(String(kpi.value ?? 0))}</p>
          </article>
        `,
      )
      .join("") || `<p class='muted'>${state.language === "fr" ? "Aucun KPI exécutif chargé." : "No executive KPIs loaded."}</p>`;
    const programs = integrationsPayload.programs || {};
    const integrated = Object.values(programs).filter(Boolean).length;
    refs.analyticsAdminStats.innerHTML += `<p class="muted">${state.language === "fr" ? "Sources intégrées" : "Sources integrated"}: ${integrated} ${state.language === "fr" ? "programmes" : "programs"}</p>`;
  } catch (error) {
    refs.analyticsAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

function fillSourceIntelligenceForm(source) {
  if (!refs.sieSourceForm || !source) {
    return;
  }
  const elements = refs.sieSourceForm.elements;
  const setValue = (name, value) => {
    if (elements[name]) {
      elements[name].value = value ?? "";
    }
  };
  setValue("source_id", source.id ?? "");
  setValue("network", source.network || source.channel || "");
  setValue("publication_url", source.publication_url || "");
  setValue("publication_title", source.publication_title || source.name || "");
  setValue("publication_text", source.publication_text || "");
  setValue("publication_author", source.publication_author || "");
  setValue("campaign", source.campaign || "");
  setValue("city", source.city || "");
  setValue("district", source.district || "");
  setValue("property_type", source.property_type || "");
  setValue("target_audience", source.target_audience || "");
  setValue("format", source.format || "");
  setValue("language", source.language || "");
  setValue("tags", Array.isArray(source.tags) ? source.tags.join(", ") : "");
  setValue("ai_classification", source.ai_classification || "");
  setValue("ai_confidence", source.ai_confidence ?? "");
  setValue("notes", source.notes || "");
}

function selectSourceIntelligence(source) {
  if (!source) {
    return;
  }
  state.selectedSourceIntelligenceId = source.id || null;
  fillSourceIntelligenceForm(source);
  if (refs.sieReferenceResult && source.reference_code) {
    refs.sieReferenceResult.innerHTML = `
      <article class="message">
        <div class="message__meta"><strong>${escapeHtml(source.name || source.source_key || systemCopy("sourceLabel"))}</strong> · ${escapeHtml(source.reference_code || "")}</div>
      </article>
    `;
  } else if (refs.sieReferenceResult) {
    refs.sieReferenceResult.innerHTML = "";
  }
  if (refs.sieLinkResult && source.whatsapp_link) {
    refs.sieLinkResult.innerHTML = `
      <article class="message">
        <div class="message__meta"><strong>${escapeHtml(systemCopy("whatsappLink"))}</strong> · ${escapeHtml(source.whatsapp_link || "")}</div>
      </article>
    `;
  } else if (refs.sieLinkResult) {
    refs.sieLinkResult.innerHTML = "";
  }
}

async function refreshSourceIntelligenceAdmin() {
  if (!state.token || !refs.sieAdminStats || !refs.sieAdminList) {
    return;
  }
  try {
    const payload = await api("/api/v2/source-intelligence/dashboard", { auth: true, query: { limit: 8 } });
    const dashboard = payload.dashboard || {};
    const stats = dashboard.stats || {};
    state.sourceIntelligenceDashboard = dashboard;
    refs.sieAdminStats.innerHTML = `
      <p class="muted">${stats.total ?? 0} sources · ${stats.active ?? stats.active_sources ?? 0} active · ${stats.with_context ?? stats.sources_with_context ?? 0} with context · ${stats.imports_total ?? 0} imports · confidence ${(Number(stats.average_ai_confidence) || 0).toFixed(2)}</p>
    `;
    refs.sieImportForm?.classList.remove("hidden");
    refs.sieSourceForm?.classList.remove("hidden");
    refs.sieReferenceForm?.classList.remove("hidden");
    const sources = dashboard.top_sources || dashboard.sources || [];
    if (sources.length) {
      const selected =
        sources.find((source) => Number(source.id) === Number(state.selectedSourceIntelligenceId)) || sources[0];
      if (selected) {
        selectSourceIntelligence(selected);
      }
    }
    refs.sieAdminList.innerHTML = sources
      .slice(0, 8)
      .map(
        (source) => `
          <article class="mini-card" data-sie-source-id="${escapeHtml(String(source.id || ""))}">
            <strong>${escapeHtml(source.name || source.source_key || "Source")}</strong>
            <p class="muted">${escapeHtml(source.reference_code || "")} · ${escapeHtml(source.channel || source.network || "")} · ${escapeHtml(source.status || "")}</p>
            <p class="muted">${escapeHtml(source.city || "")} · leads ${source.lead_count ?? 0} · customers ${source.customer_count ?? 0} · imports ${source.import_count ?? 0}</p>
            <div class="actions single">
              <button type="button" class="button ghost" data-sie-select-source="${escapeHtml(String(source.id || ""))}">Select</button>
            </div>
          </article>
        `,
      )
      .join("") || `<p class='muted'>${escapeHtml(systemCopy("noSourceRecords"))}</p>`;
    refs.sieAdminList.querySelectorAll("[data-sie-select-source]").forEach((button) => {
      button.addEventListener("click", () => {
        const sourceId = Number(button.getAttribute("data-sie-select-source") || 0);
        const source = sources.find((item) => Number(item.id) === sourceId);
        if (source) {
          selectSourceIntelligence(source);
          setNotice(systemCopy("sourceSelected", source.name || source.source_key || systemCopy("sourceLabel")), "success");
        }
      });
    });
  } catch (error) {
    refs.sieAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleSourceIntelligenceImport(event) {
  event.preventDefault();
  if (!state.token || !refs.sieImportForm) {
    return;
  }
  try {
    const form = new FormData(refs.sieImportForm);
    const payload = await api("/api/v2/source-intelligence/imports", {
      method: "POST",
      auth: true,
      body: {
        url: form.get("url"),
        name: form.get("name"),
        channel: form.get("channel"),
        notes: form.get("notes"),
      },
    });
    const source = { ...(payload.source || {}), whatsapp_link: payload.whatsapp_link || payload.context?.whatsapp_link || "" };
    if (source.id) {
      state.selectedSourceIntelligenceId = source.id;
      selectSourceIntelligence(source);
    }
    refs.sieImportForm.reset();
    setNotice(systemCopy("sieImportCompleted"), "success");
    await refreshSourceIntelligenceAdmin();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleSourceIntelligenceContext(event) {
  event.preventDefault();
  if (!state.token || !refs.sieSourceForm) {
    return;
  }
  try {
    const form = new FormData(refs.sieSourceForm);
    const sourceId = parseNumber(form.get("source_id"));
    if (!sourceId) {
      throw new Error(systemCopy("selectSourceFirst"));
    }
    const tags = String(form.get("tags") || "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);
    await api(`/api/v2/source-intelligence/sources/${sourceId}/context`, {
      method: "PATCH",
      auth: true,
      body: {
        network: form.get("network"),
        publication_url: form.get("publication_url"),
        publication_title: form.get("publication_title"),
        publication_text: form.get("publication_text"),
        publication_author: form.get("publication_author"),
        campaign: form.get("campaign"),
        city: form.get("city"),
        district: form.get("district"),
        property_type: form.get("property_type"),
        target_audience: form.get("target_audience"),
        format: form.get("format"),
        language: form.get("language"),
        tags,
        ai_classification: form.get("ai_classification"),
        ai_confidence: parseNumber(form.get("ai_confidence")) || 0,
        notes: form.get("notes"),
      },
    });
    setNotice(systemCopy("sourceContextUpdated"), "success");
    await refreshSourceIntelligenceAdmin();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleSourceIntelligenceAnalyze() {
  if (!state.token || !refs.sieSourceForm) {
    return;
  }
  try {
    const form = new FormData(refs.sieSourceForm);
    const sourceId = parseNumber(form.get("source_id"));
    if (!sourceId) {
      throw new Error(systemCopy("selectSourceFirst"));
    }
    const tags = String(form.get("tags") || "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);
    const payload = await api("/api/v2/source-intelligence/analyze", {
      method: "POST",
      auth: true,
      body: {
        source_id: sourceId,
        network: form.get("network"),
        url: form.get("publication_url"),
        title: form.get("publication_title"),
        text: form.get("publication_text"),
        author: form.get("publication_author"),
        campaign: form.get("campaign"),
        city: form.get("city"),
        district: form.get("district"),
        property_type: form.get("property_type"),
        target_audience: form.get("target_audience"),
        format: form.get("format"),
        language: form.get("language"),
        tags,
        notes: form.get("notes"),
      },
    });
    const analysis = payload.analysis || {};
    if (analysis.source) {
      selectSourceIntelligence({ ...analysis.source, whatsapp_link: analysis.context?.whatsapp_link || analysis.source.whatsapp_link || "" });
    }
    if (analysis.context) {
      fillSourceIntelligenceForm(analysis.context);
    }
    if (analysis.import?.import_key) {
      refs.sieReferenceResult.innerHTML = `
        <article class="message">
          <div class="message__meta"><strong>${escapeHtml(analysis.import.import_key)}</strong> · ${escapeHtml(analysis.import.import_status || "")}</div>
        </article>
      `;
    }
    setNotice(systemCopy("sourceAnalysisCompleted"), "success");
    await refreshSourceIntelligenceAdmin();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleSourceIntelligenceWhatsApp() {
  if (!state.token || !refs.sieSourceForm) {
    return;
  }
  try {
    const sourceId = parseNumber(new FormData(refs.sieSourceForm).get("source_id"));
    if (!sourceId) {
      throw new Error(systemCopy("selectSourceFirst"));
    }
    const payload = await api(`/api/v2/source-intelligence/sources/${sourceId}/whatsapp-link`, {
      auth: true,
    });
    const link = payload.whatsapp_link || "";
    refs.sieLinkResult.innerHTML = `
      <article class="message">
        <div class="message__meta"><strong>${escapeHtml(systemCopy("whatsappLink"))}</strong> · ${escapeHtml(link)}</div>
      </article>
    `;
    setNotice(systemCopy("whatsappLinkGenerated"), "success");
    await refreshSourceIntelligenceAdmin();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleSourceIntelligenceReference(event) {
  event.preventDefault();
  if (!state.token || !refs.sieReferenceForm) {
    return;
  }
  try {
    const form = new FormData(refs.sieReferenceForm);
    const payload = await api("/api/v2/source-intelligence/reference-code", {
      method: "POST",
      auth: true,
      body: { seed: form.get("seed") },
    });
    const referenceCode = payload.reference_code || "";
    refs.sieReferenceResult.innerHTML = `
      <article class="message">
        <div class="message__meta"><strong>${escapeHtml(systemCopy("referenceCode"))}</strong> · ${escapeHtml(referenceCode)}</div>
      </article>
    `;
    setNotice(systemCopy("referenceCodeGenerated"), "success");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function refreshSecurityAdmin() {
  if (!state.token || !refs.securityAdminStats) {
    return;
  }
  try {
    const [statsPayload, rolesPayload, sessionsPayload] = await Promise.all([
      api("/api/v2/security/stats", { auth: true }),
      api("/api/v2/security/roles", { auth: true }),
      api("/api/v2/security/sessions", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    refs.securityAdminStats.innerHTML = `
      <p class="muted">${stats.users ?? 0} users · ${stats.roles ?? 0} roles · ${stats.active_sessions ?? 0} sessions · ${stats.audit_entries ?? 0} audit entries · risk ${stats.risk_alerts ?? 0}</p>
    `;
    refs.securityAuditForm?.classList.remove("hidden");
    const roles = rolesPayload.roles || [];
    refs.securityAdminList.innerHTML = roles
      .slice(0, 6)
      .map(
        (role) => `
          <article class="mini-card">
            <strong>${escapeHtml(role.name || role.role_key || "")}</strong>
            <p class="muted">${escapeHtml(role.status || "")} · ${escapeHtml(role.scope || "global")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No IAM roles loaded.</p>";
    const sessions = sessionsPayload.sessions || [];
    if (sessions.length && refs.securityAuditResults) {
      refs.securityAuditResults.innerHTML = sessions
        .slice(0, 4)
        .map(
          (session) => `
            <article class="message">
              <div class="message__meta"><strong>Session ${escapeHtml(String(session.id || ""))}</strong> · ${escapeHtml(session.status || "")}</div>
            </article>
          `,
        )
        .join("");
    }
  } catch (error) {
    refs.securityAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleSecurityAudit(event) {
  event.preventDefault();
  if (!state.token || !refs.securityAuditForm) {
    return;
  }
  const eventType = String(new FormData(refs.securityAuditForm).get("event_type") || "").trim();
  try {
    const query = eventType ? `?event_type=${encodeURIComponent(eventType)}` : "";
    const payload = await api(`/api/v2/security/audit${query}`, { auth: true });
    const entries = payload.entries || [];
    refs.securityAuditResults.innerHTML = entries
      .slice(0, 10)
      .map(
        (entry) => `
          <article class="message">
            <div class="message__meta"><strong>${escapeHtml(entry.action || entry.event_type || "event")}</strong> · ${escapeHtml(entry.outcome || "")}</div>
            <p class="muted">${escapeHtml(entry.resource_type || "")} ${escapeHtml(String(entry.resource_id || ""))}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No audit entries.</p>";
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function refreshMarketplaceAdmin() {
  if (!state.token || !refs.marketplaceAdminStats) {
    return;
  }
  try {
    const [statsPayload, providersPayload, catalogPayload] = await Promise.all([
      api("/api/v2/marketplace/stats", { auth: true }),
      api("/api/v2/marketplace/providers", { auth: true }),
      api("/api/v2/marketplace/catalog", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    refs.marketplaceAdminStats.innerHTML = `
      <p class="muted">${stats.providers ?? 0} providers · ${stats.requests ?? 0} requests · ${stats.missions ?? 0} missions · ${stats.contracts ?? 0} contracts</p>
    `;
    refs.marketplaceSearchForm?.classList.remove("hidden");
    const providers = providersPayload.providers || [];
    refs.marketplaceAdminList.innerHTML = providers
      .slice(0, 6)
      .map(
        (provider) => `
          <article class="mini-card">
            <strong>${escapeHtml(provider.headline || provider.provider_key || "")}</strong>
            <p class="muted">${escapeHtml(provider.provider_type || "")} · score ${provider.quality_score ?? "—"}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No marketplace providers yet.</p>";
    const items = catalogPayload.items || [];
    if (items.length && refs.marketplaceSearchResults) {
      refs.marketplaceSearchResults.innerHTML = items
        .slice(0, 4)
        .map(
          (item) => `
            <article class="message">
              <div class="message__meta"><strong>${escapeHtml(item.title || "")}</strong> · ${escapeHtml(item.category || "")}</div>
            </article>
          `,
        )
        .join("");
    }
  } catch (error) {
    refs.marketplaceAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleMarketplaceSearch(event) {
  event.preventDefault();
  if (!state.token || !refs.marketplaceSearchForm) {
    return;
  }
  const query = String(new FormData(refs.marketplaceSearchForm).get("query") || "").trim();
  if (!query) {
    return;
  }
  try {
    const payload = await api(`/api/v2/marketplace/catalog?category=${encodeURIComponent(query)}`, { auth: true });
    const results = payload.items || [];
    refs.marketplaceSearchResults.innerHTML = results
      .map(
        (item) => `
          <article class="message">
            <div class="message__meta"><strong>${escapeHtml(item.title || "")}</strong> · ${escapeHtml(item.category || "")}</div>
            <p>${escapeHtml(item.description || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No catalog matches.</p>";
  } catch (error) {
    refs.marketplaceSearchResults.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function refreshCrmAdmin() {
  if (!state.token || !refs.crmAdminStats) {
    return;
  }
  try {
    const [statsPayload, contactsPayload, officialPayload] = await Promise.all([
      api("/api/v2/crm/stats", { auth: true }),
      api("/api/v2/crm/contacts", { auth: true }),
      api("/api/v2/crm/official-contact", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    const official = officialPayload.contact || {};
    refs.crmAdminStats.innerHTML = `
      <p class="muted">${stats.contacts ?? 0} contacts · ${stats.leads ?? 0} leads · ${stats.customers ?? 0} customers · ${stats.campaigns ?? 0} campaigns</p>
      <p class="muted">Official: ${escapeHtml(official.phone_number || "")} · ${escapeHtml(official.whatsapp_username || "")} · ${escapeHtml(official.telegram_bot || "")}</p>
    `;
    refs.crmSearchForm?.classList.remove("hidden");
    const contacts = contactsPayload.contacts || [];
    refs.crmAdminList.innerHTML = contacts
      .slice(0, 8)
      .map(
        (contact) => `
          <article class="mini-card">
            <strong>${escapeHtml(contact.full_name)}</strong>
            <p class="muted">${escapeHtml(contact.contact_type || "")} · ${escapeHtml(contact.email || contact.phone || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No CRM contacts yet.</p>";
  } catch (error) {
    refs.crmAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleCrmSearch(event) {
  event.preventDefault();
  if (!state.token || !refs.crmSearchForm) {
    return;
  }
  const query = String(new FormData(refs.crmSearchForm).get("query") || "").trim();
  if (!query) {
    return;
  }
  try {
    const payload = await api(`/api/v2/crm/search?q=${encodeURIComponent(query)}`, { auth: true });
    const results = payload.results || [];
    refs.crmSearchResults.innerHTML = results
      .map(
        (item) => `
          <article class="message">
            <div class="message__meta"><strong>${escapeHtml(item.full_name || "")}</strong> · ${escapeHtml(item.contact_type || "")}</div>
            <p>${escapeHtml(item.email || item.phone || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No matches.</p>";
  } catch (error) {
    refs.crmSearchResults.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function refreshReiAdmin() {
  if (!state.token || !refs.reiAdminStats) {
    return;
  }
  try {
    const [statsPayload, listingsPayload, analyticsPayload] = await Promise.all([
      api("/api/v2/properties/stats", { auth: true }),
      api("/api/v2/properties/listings", { auth: true }),
      api("/api/v2/properties/analytics", { auth: true }),
    ]);
    const stats = statsPayload.stats || {};
    const analytics = analyticsPayload.analytics || {};
    refs.reiAdminStats.innerHTML = `
      <p class="muted">${stats.properties ?? 0} properties · ${stats.listings ?? 0} listings · ${stats.transactions ?? 0} transactions · trust avg ${analytics.avg_trust_score ?? "—"}</p>
    `;
    refs.reiSearchForm?.classList.remove("hidden");
    const listings = listingsPayload.listings || [];
    refs.reiAdminList.innerHTML = listings
      .slice(0, 8)
      .map(
        (listing) => `
          <article class="mini-card">
            <strong>${escapeHtml(listing.title)}</strong>
            <p class="muted">${escapeHtml(listing.status || "draft")} · AI ${listing.ai_score ?? 0}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No listings yet.</p>";
  } catch (error) {
    refs.reiAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleReiSearch(event) {
  event.preventDefault();
  if (!state.token || !refs.reiSearchForm) {
    return;
  }
  const query = String(new FormData(refs.reiSearchForm).get("query") || "").trim();
  if (!query) {
    return;
  }
  try {
    const payload = await api(`/api/v2/properties/search?q=${encodeURIComponent(query)}`, { auth: true });
    const results = payload.results || [];
    refs.reiSearchResults.innerHTML = results
      .map(
        (item) => `
          <article class="message">
            <div class="message__meta"><strong>${escapeHtml(item.title || item.listing_key || "")}</strong> · ${escapeHtml(item.status || "")}</div>
            <p>${escapeHtml(item.city || "")} · score ${item.ai_score ?? "—"}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No matches.</p>";
  } catch (error) {
    refs.reiSearchResults.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function refreshWorkflowAdmin() {
  if (!state.token || !refs.workflowAdminStats) {
    return;
  }
  try {
    const [metricsPayload, defsPayload, instancesPayload] = await Promise.all([
      api("/api/v2/workflows/metrics", { auth: true }),
      api("/api/v2/workflows/definitions", { auth: true }),
      api("/api/v2/workflows/instances?limit=8", { auth: true }),
    ]);
    const metrics = metricsPayload.metrics || {};
    refs.workflowAdminStats.innerHTML = `
      <p class="muted">${metrics.workflows ?? 0} workflows · ${metrics.instances ?? 0} instances · ${metrics.tasks ?? 0} tasks</p>
    `;
    refs.workflowMonitorForm?.classList.remove("hidden");
    const defs = defsPayload.workflows || [];
    refs.workflowAdminList.innerHTML = defs
      .slice(0, 6)
      .map(
        (row) => `
          <article class="mini-card">
            <strong>${escapeHtml(row.title)}</strong>
            <p class="muted">${escapeHtml(row.domain || "")} · ${escapeHtml(row.status || "")}</p>
          </article>
        `,
      )
      .join("") || "<p class='muted'>No automation workflows.</p>";
    const instances = instancesPayload.instances || [];
    if (instances.length && refs.workflowMonitorResults) {
      refs.workflowMonitorResults.innerHTML = instances
        .slice(0, 4)
        .map(
          (inst) => `
            <article class="message">
              <div class="message__meta"><strong>${escapeHtml(inst.workflow_key || "")}</strong> · ${escapeHtml(inst.status || "")}</div>
              <p class="muted">state ${escapeHtml(inst.current_state_key || "—")}</p>
            </article>
          `,
        )
        .join("");
    }
  } catch (error) {
    refs.workflowAdminStats.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function handleWorkflowMonitor(event) {
  event.preventDefault();
  if (!state.token) {
    return;
  }
  try {
    const payload = await api("/api/v2/workflows/monitoring", { auth: true });
    const monitoring = payload.monitoring || {};
    refs.workflowMonitorResults.innerHTML = `
      <article class="message">
        <div class="message__meta"><strong>Monitoring</strong></div>
        <p class="muted">SLA policies: ${monitoring.sla_policies ?? 0} · pending approvals: ${monitoring.pending_approvals ?? 0} · open escalations: ${monitoring.open_escalations ?? 0}</p>
      </article>
    `;
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleLogin(event) {
  event.preventDefault();
  try {
    const email = refs.loginEmail.value.trim();
    const password = refs.loginPassword.value;
    const payload = await api("/api/auth/login", {
      method: "POST",
      body: { email, password },
    });
    const token = String(payload.token || "");
    if (!token) {
      throw new Error("Login response did not include a token.");
    }
    state.token = token;
    localStorage.setItem("lawim.token", state.token);
    updateAuthShell(true);
    applyModule("dashboard");
    const resolvedRole = resolveAccessRole(payload.user?.role, payload.roles || payload.user?.roles || []);
    const resolvedJourney = journeyForRole(resolvedRole);
    traceRuntime("LOGIN_OK", {
      email: payload.user?.email || email,
      role: resolvedRole,
      journey: resolvedJourney,
    });
    traceRuntime("ROLE_RESOLVED", {
      role: resolvedRole,
      journey: resolvedJourney,
    });
    traceRuntime("DASHBOARD_SELECTED", {
      role: resolvedRole,
      journey: resolvedJourney,
    });
    await refresh({ renderJourney: false });
    applyJourney(resolvedJourney);
    // applyJourney(journeyForRole(payload.user.role));
    refs.loginPassword.value = "";
    setNotice(noticeCopy("loginSuccess", payload.user?.email || email), "success");
  } catch (error) {
    setNotice(formatLoginError(error), "error", error.code || "");
  }
}

async function handleLogout() {
  try {
    if (state.token) {
      await api("/api/auth/logout", { method: "POST", auth: true });
    }
  } catch (error) {
    console.warn("Logout warning:", error);
  } finally {
    clearSession();
    refs.messageForm.classList.add("hidden");
    refs.conversationDetail.innerHTML = `<p class="muted">${escapeHtml(state.language === "fr" ? "Aucune conversation sélectionnée." : "No conversation selected.")}</p>`;
    state.selectedConversationId = null;
    setNotice(noticeCopy("logout"), "neutral");
    applyModule("dashboard");
    await refresh();
  }
}

async function handleProjectCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice(noticeCopy("projectCreateAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.projectForm);
    const payload = await api("/api/v2/projects", {
      method: "POST",
      auth: true,
      body: {
        title: form.get("title"),
        objective: form.get("objective"),
        project_type: form.get("project_type"),
        budget_min: parseNumber(form.get("budget_min")),
        budget_max: parseNumber(form.get("budget_max")),
        location_city: form.get("location_city"),
        timeline_horizon: form.get("timeline_horizon"),
        status: "active",
      },
    });
    refs.projectForm.reset();
    state.selectedProjectId = payload.project.id;
    setNotice(noticeCopy("projectCreated"), "success");
    await refreshProjects();
    applyJourney("project");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleMatchSearch(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.matchForm);
    const payload = await api("/api/matches", {
      auth: Boolean(state.token),
      query: {
        city: form.get("city"),
        budget_min: parseNumber(form.get("budget_min")),
        budget_max: parseNumber(form.get("budget_max")),
        latitude: parseNumber(form.get("latitude")),
        longitude: parseNumber(form.get("longitude")),
        limit: parseNumber(form.get("limit")),
        min_score: parseNumber(form.get("min_score")),
      },
    });
    renderMatches(payload.matches || []);
    setNotice(noticeCopy("matchReturned", payload.matches?.length || 0, payload.criteria?.min_score ?? "n/a"), "success");
    if (state.token) {
      await refreshNotifications();
    }
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handlePropertyCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice(noticeCopy("recordsAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.propertyForm);
    await api("/api/properties", {
      method: "POST",
      auth: true,
      body: {
        title: form.get("title"),
        summary: form.get("summary"),
        city: form.get("city"),
        country: form.get("country") || "Cameroon",
        address_line: form.get("address_line"),
        region: form.get("region"),
        property_type: form.get("property_type"),
        status: form.get("status") || "draft",
        availability: form.get("availability") || "available",
        price_min: parseNumber(form.get("price_min")),
        price_max: parseNumber(form.get("price_max")),
        latitude: parseNumber(form.get("latitude")),
        longitude: parseNumber(form.get("longitude")),
        owner_organization_id: parseNumber(form.get("owner_organization_id")),
      },
    });
    refs.propertyForm.reset();
    setNotice(noticeCopy("propertyCreated"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleGeoLookup(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.geoForm);
    const payload = await api("/api/geo/geocode", {
      query: {
        city: form.get("city"),
        country: form.get("country"),
        address_line: form.get("address_line"),
        region: form.get("region"),
      },
    });
    const location = payload.location || {};
    const coords = location.coordinates || {};
    refs.geoResult.textContent = `${location.city}, ${location.region || "—"}, ${location.country} · ${coords.latitude}, ${coords.longitude} · provider=${payload.provider}`;
    setNotice(noticeCopy("geoLookup"), "success");
  } catch (error) {
    refs.geoResult.textContent = error.message;
    setNotice(error.message, "error");
  }
}

async function handleMediaUpload(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice(noticeCopy("mediaAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.mediaUploadForm);
    const file = form.get("file");
    const propertyId = form.get("property_id");
    if (!file || !propertyId) {
      throw new Error("Property and file are required.");
    }
    const uploadData = new FormData();
    uploadData.append("property_id", String(propertyId));
    uploadData.append("file", file);
    uploadData.append("caption", form.get("caption") || "Uploaded media");
    uploadData.append("kind", form.get("kind") || "image");
    await apiMultipart("/api/media/upload", { auth: true, formData: uploadData });
    refs.mediaUploadForm.reset();
    setNotice(noticeCopy("mediaUploaded"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleMessageCreate(event) {
  event.preventDefault();
  if (!state.token || !state.selectedConversationId) {
    setNotice(noticeCopy("conversationAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.messageForm);
    await api(`/api/conversations/${state.selectedConversationId}/messages`, {
      method: "POST",
      auth: true,
      body: {
        body: form.get("body"),
      },
    });
    refs.messageForm.reset();
    setNotice(noticeCopy("replySent"), "success");
    await selectConversation(state.selectedConversationId);
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleRegister(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.registerForm);
    const payload = await api("/api/auth/register", {
      method: "POST",
      body: {
        full_name: form.get("full_name"),
        email: form.get("email"),
        password: form.get("password"),
        role: form.get("role"),
        organization_id: parseNumber(form.get("organization_id")),
      },
    });
    const token = String(payload.token || "");
    if (!token) {
      throw new Error(systemCopy("registrationMissingToken"));
    }
    state.token = token;
    localStorage.setItem("lawim.token", state.token);
    updateAuthShell(true);
    applyModule("dashboard");
    // applyJourney(journeyForRole(form.get("role")));
    const resolvedRole = resolveAccessRole(payload.user?.role || form.get("role"));
    applyJourney(journeyForRole(resolvedRole));
    setNotice(noticeCopy("registerSuccess", payload.user.email), "success");
    await refresh({ renderJourney: false });
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handlePropertySearch(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.propertySearchForm);
    const payload = await api("/api/properties", {
      query: {
        city: form.get("city"),
        region: form.get("region"),
        property_type: form.get("property_type"),
        status: form.get("status"),
        price_min: parseNumber(form.get("price_min")),
        price_max: parseNumber(form.get("price_max")),
        sort: form.get("sort") || "created_at",
        order: form.get("order") || "desc",
        page: parseNumber(form.get("page")) || 1,
        limit: parseNumber(form.get("limit")) || 10,
      },
    });
    renderProperties(payload.properties || []);
    const pagination = payload.pagination || {};
    if (refs.propertySearchMeta) {
      refs.propertySearchMeta.textContent = `Page ${pagination.page || 1}/${pagination.pages || 1} · ${pagination.total ?? payload.properties?.length ?? 0} total · sort ${pagination.sort || "created_at"} ${pagination.order || "desc"}`;
    }
    setNotice(noticeCopy("propertySearchFound", payload.properties?.length || 0), "success");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handlePublishProperty() {
  if (!state.token || !state.selectedPropertyId) {
    setNotice(noticeCopy("propertyPublishAuth"), "error");
    return;
  }
  try {
    const payload = await api(`/api/properties/${state.selectedPropertyId}/publish`, {
      method: "POST",
      auth: true,
      body: { version: state.selectedPropertyVersion },
    });
    state.selectedPropertyVersion = payload.property.version;
    updateSelectedPropertyLabel();
    setNotice(noticeCopy("propertyPublished"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleArchiveProperty() {
  if (!state.token || !state.selectedPropertyId) {
    setNotice(noticeCopy("propertyPublishAuth"), "error");
    return;
  }
  try {
    const payload = await api(`/api/properties/${state.selectedPropertyId}`, {
      method: "PATCH",
      auth: true,
      body: { status: "archived", version: state.selectedPropertyVersion },
    });
    state.selectedPropertyVersion = payload.property.version;
    updateSelectedPropertyLabel();
    setNotice(noticeCopy("propertyArchived"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleBuyerConversation(event) {
  event.preventDefault();
  if (!state.token || !state.selectedPropertyId) {
    setNotice(noticeCopy("propertyPublishAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.buyerConversationForm);
    const payload = await api("/api/conversations", {
      method: "POST",
      auth: true,
      body: {
        property_id: state.selectedPropertyId,
        subject: form.get("subject"),
        initial_message: form.get("initial_message"),
      },
    });
    refs.buyerConversationForm.reset();
    state.selectedConversationId = payload.conversation.id;
    setNotice(noticeCopy("conversationOpened"), "success");
    await refresh();
    await selectConversation(payload.conversation.id);
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleNegotiationUpdate(event) {
  event.preventDefault();
  if (!state.token || !state.selectedConversationId) {
    setNotice(noticeCopy("conversationSelect"), "error");
    return;
  }
  try {
    const form = new FormData(refs.negotiationForm);
    const payload = await api(`/api/conversations/${state.selectedConversationId}`, {
      method: "PATCH",
      auth: true,
      body: { negotiation_stage: form.get("negotiation_stage") },
    });
    renderConversationDetail(payload.conversation);
    setNotice(noticeCopy("negotiationUpdated", payload.conversation.negotiation_stage), "success");
    await refresh();
    await refreshNotifications();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleNotificationFilter(event) {
  event.preventDefault();
  try {
    await refreshNotifications();
    setNotice(noticeCopy("notificationsFiltered"), "success");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleAdminOrgCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice(noticeCopy("adminAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.adminOrgForm);
    await api("/api/organizations", {
      method: "POST",
      auth: true,
      body: { name: form.get("name"), slug: form.get("slug"), kind: "agency", city: "Douala" },
    });
    refs.adminOrgForm.reset();
    setNotice(noticeCopy("organizationCreated"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleAdminUserCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice(noticeCopy("adminAuth"), "error");
    return;
  }
  try {
    const form = new FormData(refs.adminUserForm);
    await api("/api/users", {
      method: "POST",
      auth: true,
      body: {
        email: form.get("email"),
        full_name: form.get("full_name"),
        role: "agent",
        password: form.get("password") || "",
        organization_id: parseNumber(form.get("organization_id")),
      },
    });
    refs.adminUserForm.reset();
    setNotice(noticeCopy("staffCreated"), "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

function bindEvents() {
  refs.loginForm.addEventListener("submit", handleLogin);
  refs.loginForgot?.addEventListener("click", () => {
    openSupportRequest("LAWIM - Mot de passe oublié");
  });
  refs.loginCreate?.addEventListener("click", () => {
    openSupportRequest("LAWIM - Création de compte");
  });
  refs.logoutButton.addEventListener("click", handleLogout);
  refs.registerForm?.addEventListener("submit", handleRegister);
  refs.projectForm?.addEventListener("submit", handleProjectCreate);
  refs.assistantForm?.addEventListener("submit", handleAssistantChat);
  refs.knowledgeSearchForm?.addEventListener("submit", handleKnowledgeSearch);
  refs.reiSearchForm?.addEventListener("submit", handleReiSearch);
  refs.crmSearchForm?.addEventListener("submit", handleCrmSearch);
  refs.marketplaceSearchForm?.addEventListener("submit", handleMarketplaceSearch);
  refs.sieImportForm?.addEventListener("submit", handleSourceIntelligenceImport);
  refs.sieSourceForm?.addEventListener("submit", handleSourceIntelligenceContext);
  refs.sieReferenceForm?.addEventListener("submit", handleSourceIntelligenceReference);
  refs.sieAnalyzeButton?.addEventListener("click", handleSourceIntelligenceAnalyze);
  refs.sieWhatsappButton?.addEventListener("click", handleSourceIntelligenceWhatsApp);
  refs.securityAuditForm?.addEventListener("submit", handleSecurityAudit);
  refs.workflowMonitorForm?.addEventListener("submit", handleWorkflowMonitor);
  refs.propertySearchForm?.addEventListener("submit", handlePropertySearch);
  refs.matchForm.addEventListener("submit", handleMatchSearch);
  refs.propertyForm.addEventListener("submit", handlePropertyCreate);
  refs.geoForm.addEventListener("submit", handleGeoLookup);
  refs.mediaUploadForm.addEventListener("submit", handleMediaUpload);
  refs.messageForm.addEventListener("submit", handleMessageCreate);
  refs.buyerConversationForm?.addEventListener("submit", handleBuyerConversation);
  refs.negotiationForm?.addEventListener("submit", handleNegotiationUpdate);
  refs.notificationFilterForm?.addEventListener("submit", handleNotificationFilter);
  refs.adminOrgForm?.addEventListener("submit", handleAdminOrgCreate);
  refs.adminUserForm?.addEventListener("submit", handleAdminUserCreate);
  refs.publishPropertyButton?.addEventListener("click", handlePublishProperty);
  refs.archivePropertyButton?.addEventListener("click", handleArchiveProperty);
  refs.languageSelect?.addEventListener("change", (event) => {
    setLanguage(String(event.target.value || "fr"));
  });
  refs.statsPeriodSelect?.addEventListener("change", (event) => {
    state.statsPeriod = String(event.target.value || "today");
    localStorage.setItem("lawim.stats.period", state.statsPeriod);
    if (state.bootstrap?.current_user) {
      renderRoleCockpit(state.bootstrap.current_user, state.bootstrap);
    }
  });
  refs.journeyNav?.querySelectorAll("[data-journey]").forEach((button) => {
    button.addEventListener("click", () => applyJourney(button.getAttribute("data-journey")));
  });
  if (refs.markNotificationsReadButton) {
    refs.markNotificationsReadButton.addEventListener("click", markAllNotificationsRead);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  cacheRefs();
  bindEvents();
  decorateModuleChrome();
  updateAuthShell(Boolean(state.token));
  setLanguage(state.language);
  applyModule(state.activeModule, { persist: false });
  applyJourney(state.activeJourney);
  updateSelectedPropertyLabel();
  await refresh();
});
