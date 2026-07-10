import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

export type FeatureKey =
  | 'property_search'
  | 'property_add'
  | 'conversation'
  | 'partners'
  | 'dossiers'
  | 'documents'
  | 'favorites'
  | 'comparison'
  | 'map'
  | 'notifications'
  | 'history'
  | 'stats'
  | 'profile'
  | 'calendar'
  | 'estimations'
  | 'marketplace'
  | 'admin_supervision'
  | 'admin_security'
  | 'admin_users'
  | 'admin_features';

export type FeatureConfig = Record<FeatureKey, boolean>;

const STORAGE_KEY = 'lawim.features';

const DEFAULT_FEATURES: FeatureConfig = {
  property_search: true,
  property_add: true,
  conversation: true,
  partners: true,
  dossiers: true,
  documents: true,
  favorites: true,
  comparison: true,
  map: true,
  notifications: true,
  history: true,
  stats: true,
  profile: true,
  calendar: true,
  estimations: true,
  marketplace: true,
  admin_supervision: true,
  admin_security: true,
  admin_users: true,
  admin_features: true
};

const FEATURE_LABELS: Record<FeatureKey, string> = {
  property_search: '🔎 Recherche de biens',
  property_add: '➕ Mise en ligne de biens',
  conversation: '💬 Conversation',
  partners: '🤝 Partenaires',
  dossiers: '📁 Dossiers',
  documents: '📄 Documents',
  favorites: '⭐ Favoris',
  comparison: '📊 Comparaison',
  map: '🗺️ Carte',
  notifications: '🔔 Notifications',
  history: '📅 Historique',
  stats: '📊 Statistiques',
  profile: '👤 Profil',
  calendar: '📅 Calendrier',
  estimations: '💰 Estimations',
  marketplace: '🏪 Marketplace',
  admin_supervision: '🟢 Supervision',
  admin_security: '🔐 Sécurité',
  admin_users: '👥 Utilisateurs',
  admin_features: '⚙️ Fonctionnalités'
};

function loadFeatures(): FeatureConfig {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored) as Partial<FeatureConfig>;
      return { ...DEFAULT_FEATURES, ...parsed };
    }
  } catch { /* ignore */ }
  return { ...DEFAULT_FEATURES };
}

function saveFeatures(config: FeatureConfig) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
  } catch { /* ignore */ }
}

type FeatureContextValue = {
  features: FeatureConfig;
  setFeature: (key: FeatureKey, enabled: boolean) => void;
  resetFeatures: () => void;
};

const FeatureContext = createContext<FeatureContextValue | null>(null);

export function FeatureProvider({ children }: { children: ReactNode }) {
  const [features, setFeaturesState] = useState<FeatureConfig>(loadFeatures);

  useEffect(() => {
    saveFeatures(features);
  }, [features]);

  const setFeature = useCallback((key: FeatureKey, enabled: boolean) => {
    setFeaturesState((prev) => ({ ...prev, [key]: enabled }));
  }, []);

  const resetFeatures = useCallback(() => {
    setFeaturesState({ ...DEFAULT_FEATURES });
  }, []);

  const value = useMemo(() => ({ features, setFeature, resetFeatures }), [features, setFeature, resetFeatures]);

  return (
    <FeatureContext.Provider value={value}>
      {children}
    </FeatureContext.Provider>
  );
}

export function useFeatures() {
  const ctx = useContext(FeatureContext);
  if (!ctx) {
    return {
      features: DEFAULT_FEATURES,
      setFeature: (_key: FeatureKey, _enabled: boolean) => {},
      resetFeatures: () => {}
    };
  }
  return ctx;
}

export function useFeature(key: FeatureKey): boolean {
  const { features } = useFeatures();
  return features[key];
}

export { FEATURE_LABELS, DEFAULT_FEATURES };
export type { FeatureContextValue };
