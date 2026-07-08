import { create } from 'zustand';
import { apiSdk, type AuthCredentials, type UserProfile } from '@api-sdk';
import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { getStoredLanguage, translate } from '@ui';

export type AccessRole = 'admin' | 'manager' | 'operator' | 'partner' | 'user';

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: AccessRole;
}

export interface AuthState {
  user: AuthUser | null;
  token: string | null;
  roles: string[];
  isAuthenticated: boolean;
  isLoading: boolean;
  hasHydrated: boolean;
  sessionExpired: boolean;
  sessionUnavailable: boolean;
  login: (credentials: AuthCredentials) => Promise<AuthUser>;
  logout: () => Promise<void>;
  hydrate: () => Promise<AuthUser | null>;
}

export function getUserDisplayName(user: AuthUser) {
  return user.name || user.email.split('@')[0];
}

const rolePriority: AccessRole[] = ['admin', 'manager', 'operator', 'partner', 'user'];

const roleAliases: Record<string, AccessRole> = {
  admin: 'admin',
  director: 'admin',
  superadmin: 'admin',
  manager: 'manager',
  supervisor: 'manager',
  lead: 'manager',
  coordinator: 'manager',
  operator: 'operator',
  agent: 'operator',
  operateur: 'operator',
  staff: 'operator',
  support: 'operator',
  moderator: 'operator',
  partner: 'partner',
  photographer: 'partner',
  photographe: 'partner',
  notary: 'partner',
  notaire: 'partner',
  bank: 'partner',
  banque: 'partner',
  artisan: 'partner',
  architect: 'partner',
  architecte: 'partner',
  diagnostician: 'partner',
  diagnostiqueur: 'partner',
  decorator: 'partner',
  decorateur: 'partner',
  demenageur: 'partner',
  mover: 'partner',
  broker: 'partner',
  user: 'user',
  owner: 'user',
  buyer: 'user',
  seller: 'user',
  vendeur: 'user',
  acheteur: 'user',
  viewer: 'user',
  customer: 'user',
  tenant: 'user',
  locataire: 'user',
  landlord: 'user',
  proprietaire: 'user',
  investor: 'user',
  investisseur: 'user',
  promoter: 'user',
  promoteur: 'user',
  company: 'user',
  enterprise: 'user',
  entreprise: 'user',
  business: 'user'
};

function normalizeRoleCandidate(value: unknown): AccessRole | null {
  const normalized = String(value ?? '').trim().toLowerCase();
  return roleAliases[normalized] ?? null;
}

export function resolvePrimaryRole(role: unknown, roles: unknown[] = []): AccessRole {
  const candidates = [role, ...roles];
  const normalized = candidates.map(normalizeRoleCandidate).filter((candidate): candidate is AccessRole => Boolean(candidate));
  for (const priority of rolePriority) {
    if (normalized.includes(priority)) {
      return priority;
    }
  }
  return 'user';
}

export function resolveDashboardPath(role: AccessRole | string) {
  return '/dashboard';
}

function formatAuthError(message: string, context: 'login' | 'session') {
  const lower = String(message || '').toLowerCase();
  const statusMatch = lower.match(/\b(\d{3})\b/);
  const status = statusMatch ? Number(statusMatch[1]) : null;
  const language = getStoredLanguage();

  if (context === 'login') {
    if (status === 401 || status === 403 || lower.includes('unauthorized') || lower.includes('forbidden')) {
      return translate('auth.login.banner.invalid', language);
    }
    if (status === 429) {
      return translate('auth.login.banner.rate_limited', language);
    }
    if (status && status >= 500) {
      return translate('auth.login.banner.server_unavailable', language);
    }
    if (lower.includes('fetch') || lower.includes('network')) {
      return translate('auth.login.banner.server_unavailable', language);
    }
    return translate('auth.login.banner.invalid', language);
  }

  if (status === 401 || status === 403 || lower.includes('unauthorized') || lower.includes('forbidden')) {
    return translate('auth.login.banner.session_expired', language);
  }
  if (status && status >= 500) {
    return translate('auth.login.banner.server_unavailable', language);
  }
  if (lower.includes('fetch') || lower.includes('network')) {
    return translate('auth.login.banner.server_unavailable', language);
  }
  return translate('auth.login.banner.session_expired', language);
}

function isServerUnavailable(message: string) {
  const lower = String(message || '').toLowerCase();
  const statusMatch = lower.match(/\b(\d{3})\b/);
  const status = statusMatch ? Number(statusMatch[1]) : null;
  return Boolean((status && status >= 500) || lower.includes('fetch') || lower.includes('network'));
}

function normalizeSessionUser(user: UserProfile | undefined, role: AccessRole): AuthUser {
  return {
    id: String(user?.id ?? user?.email ?? 'user'),
    email: String(user?.email ?? ''),
    name: String(user?.name ?? user?.email?.split('@')[0] ?? 'User'),
    role
  };
}

function persistToken(token: string) {
  window.localStorage.setItem('lawim_token', token);
}

function clearToken() {
  window.localStorage.removeItem('lawim_token');
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  roles: [],
  isAuthenticated: false,
  isLoading: false,
  hasHydrated: false,
  sessionExpired: false,
  sessionUnavailable: false,
  login: async (credentials) => {
    set({ isLoading: true });
    try {
      const response = await apiSdk.login(credentials);
      const token = response.data?.token;
      const resolvedRole = resolvePrimaryRole(response.data?.user?.role, response.data?.roles);
      const normalizedRoles = Array.from(new Set([resolvedRole, ...(response.data?.roles ?? []).map(normalizeRoleCandidate).filter((candidate): candidate is AccessRole => Boolean(candidate))]));
      if (!token) {
        throw new Error(formatAuthError(response.message ?? 'Authentication failed', 'login'));
      }
      if (response.message !== 'ok' && response.message !== 'mock') {
        throw new Error(formatAuthError(response.message ?? 'Authentication failed', 'login'));
      }
      persistToken(token);
      const user = normalizeSessionUser(response.data.user, resolvedRole);
      set({
        user,
        token,
        roles: normalizedRoles,
        isAuthenticated: true,
        hasHydrated: true,
        sessionExpired: false,
        sessionUnavailable: false
      });
      return user;
    } catch (error) {
      clearToken();
      set({ user: null, token: null, roles: [], isAuthenticated: false, hasHydrated: true, sessionExpired: false, sessionUnavailable: false });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  logout: async () => {
    try {
      await apiSdk.logout();
    } finally {
      clearToken();
      set({ user: null, token: null, roles: [], isAuthenticated: false, isLoading: false, hasHydrated: true, sessionExpired: false, sessionUnavailable: false });
    }
  },
  hydrate: async () => {
    set({ isLoading: true });
    const hadStoredToken = Boolean(window.localStorage.getItem('lawim_token'));
    try {
      const response = await apiSdk.getSession();
      if (response.data?.token) {
        const resolvedRole = resolvePrimaryRole(response.data.user?.role, response.data.roles);
        const normalizedRoles = Array.from(new Set([resolvedRole, ...(response.data.roles ?? []).map(normalizeRoleCandidate).filter((candidate): candidate is AccessRole => Boolean(candidate))]));
        persistToken(response.data.token);
        const user = normalizeSessionUser(response.data.user, resolvedRole);
        set({ user, token: response.data.token, roles: normalizedRoles, isAuthenticated: true, isLoading: false, hasHydrated: true, sessionExpired: false, sessionUnavailable: false });
        return user;
      }
      const unavailable = isServerUnavailable(response.message || '');
      clearToken();
      set({ user: null, token: null, roles: [], isAuthenticated: false, isLoading: false, hasHydrated: true, sessionExpired: hadStoredToken && !unavailable, sessionUnavailable: unavailable });
      return null;
    } catch (error) {
      const unavailable = isServerUnavailable(error instanceof Error ? error.message : '');
      clearToken();
      set({ user: null, token: null, roles: [], isAuthenticated: false, isLoading: false, hasHydrated: true, sessionExpired: hadStoredToken && !unavailable, sessionUnavailable: unavailable });
      return null;
    }
  }
}));

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isLoading = useAuthStore((state) => state.isLoading);
  const hasHydrated = useAuthStore((state) => state.hasHydrated);
  const sessionExpired = useAuthStore((state) => state.sessionExpired);
  const sessionUnavailable = useAuthStore((state) => state.sessionUnavailable);

  if (!hasHydrated || isLoading) {
    return <div className="min-h-screen bg-slate-950 text-slate-100" />;
  }

  const reason = sessionUnavailable ? 'server_unavailable' : sessionExpired ? 'session_expired' : 'unauthorized';

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace state={{ reason }} />;
}

export function useAuthUser() {
  return useAuthStore((state) => state.user);
}

export function useAuthRoles() {
  return useAuthStore((state) => state.roles);
}
