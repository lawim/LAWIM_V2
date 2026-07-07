import { create } from 'zustand';
import { apiSdk, type AuthCredentials, type AuthSession, type UserProfile } from '@api-sdk';
import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

export interface AuthUser {
  id: string;
  email: string;
  role: 'admin' | 'operator' | 'viewer';
}

export interface AuthState {
  user: AuthUser | null;
  token: string | null;
  roles: string[];
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: AuthCredentials) => Promise<void>;
  logout: () => Promise<void>;
  hydrate: () => Promise<void>;
}

export function getUserDisplayName(user: AuthUser) {
  return user.email.split('@')[0];
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  roles: [],
  isAuthenticated: false,
  isLoading: false,
  login: async (credentials) => {
    set({ isLoading: true });
    try {
      const response = await apiSdk.login(credentials);
      const token = response.data?.token;
      if (!token) {
        throw new Error(response.message && response.message !== 'ok' && response.message !== 'mock' ? response.message : 'Authentication failed');
      }
      if (response.message !== 'ok' && response.message !== 'mock') {
        throw new Error(response.message || 'Authentication failed');
      }
      window.localStorage.setItem('lawim_token', token);
      set({
        user: response.data.user as AuthUser,
        token,
        roles: response.data.roles,
        isAuthenticated: true
      });
    } finally {
      set({ isLoading: false });
    }
  },
  logout: async () => {
    await apiSdk.logout();
    window.localStorage.removeItem('lawim_token');
    set({ user: null, token: null, roles: [], isAuthenticated: false, isLoading: false });
  },
  hydrate: async () => {
    set({ isLoading: true });
    const response = await apiSdk.getSession();
    if (response.data?.token) {
      window.localStorage.setItem('lawim_token', response.data.token);
      set({ user: response.data.user as AuthUser, token: response.data.token, roles: response.data.roles, isAuthenticated: true, isLoading: false });
    } else {
      window.localStorage.removeItem('lawim_token');
      set({ user: null, token: null, roles: [], isAuthenticated: false, isLoading: false });
    }
  }
}));

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

export function useAuthUser() {
  return useAuthStore((state) => state.user);
}

export function useAuthRoles() {
  return useAuthStore((state) => state.roles);
}
