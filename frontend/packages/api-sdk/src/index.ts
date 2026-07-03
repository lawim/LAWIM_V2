export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PropertySummary {
  id: string;
  title: string;
  location: string;
  price: number;
  type: string;
  status?: string;
}

export interface PropertyDetail extends PropertySummary {
  description: string;
  surface: string;
  bedrooms: number;
  bathrooms: number;
}

export interface MarketListing {
  id: string;
  title: string;
  category: string;
  price: number;
  status: string;
}

export interface UserProfile {
  id: string;
  name: string;
  role: string;
  email: string;
}

export interface DashboardSummary {
  properties: number;
  opportunities: number;
  communications: number;
  pendingTasks: number;
}

export interface FavoriteItem {
  id: string;
  title: string;
  type: string;
  score: number;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  read: boolean;
}

export interface RequestItem {
  id: string;
  title: string;
  status: string;
}

export interface DocumentItem {
  id: string;
  title: string;
  kind: string;
}

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthSession {
  user: UserProfile;
  token: string;
  roles: string[];
}

export interface EstimationPayload {
  address: string;
  surface: string;
  type: string;
  expectedPrice: string;
  notes?: string;
}

export interface EstimationResult {
  estimate: string;
  confidence: string;
}

export interface AssistantMessagePayload {
  message: string;
}

export interface AssistantReply {
  reply: string;
  suggestions: string[];
}

const mockDelay = () => Promise.resolve();
const env = (import.meta as ImportMeta & { env?: Record<string, string | boolean | undefined> }).env ?? {};
const apiBase = String(env.VITE_LAWIM_API_URL ?? '/api').replace(/\/$/, '');
const useMocks = env.VITE_LAWIM_USE_MOCKS === 'true';

const readStorageToken = () => {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('lawim_token');
};

const normalizePayload = <T>(payload: unknown, fallback: T): T => {
  if (payload == null) return fallback;
  if (Array.isArray(payload)) return payload as T;
  if (typeof payload === 'object') {
    const record = payload as Record<string, unknown>;
    if (Array.isArray(record.data)) return record.data as T;
    if (Array.isArray(record.items)) return record.items as T;
    if (Array.isArray(record.results)) return record.results as T;
    if (Array.isArray(record.properties)) return record.properties as T;
    if (Array.isArray(record.contacts)) return record.contacts as T;
    if (Array.isArray(record.marketplace)) return record.marketplace as T;
    if (Array.isArray(record.notifications)) return record.notifications as T;
    if (Array.isArray(record.documents)) return record.documents as T;
    if (Array.isArray(record.requests)) return record.requests as T;
    if (Array.isArray(record.favorites)) return record.favorites as T;
    if (Array.isArray(record.users)) return record.users as T;
    if (Array.isArray(record.roles)) return record.roles as T;
    if (Array.isArray(record.messages)) return record.messages as T;
    if (Array.isArray(record.workflows)) return record.workflows as T;
    if (Array.isArray(record.analytics)) return record.analytics as T;
    if (Array.isArray(record.security)) return record.security as T;
  }
  return payload as T;
};

const resolveUrl = (path: string) => {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  if (path.startsWith('/api/auth')) return `${apiBase}${path}`;
  if (path.startsWith('/api/v2')) return `${apiBase}${path}`;
  if (path.startsWith('/auth')) return `${apiBase}/auth${path}`;
  if (path.startsWith('/v2')) return `${apiBase}${path}`;
  return `${apiBase}/v2${path}`;
};

const requestJson = async <T>(path: string, init: RequestInit = {}, fallback: T): Promise<ApiResponse<T>> => {
  if (useMocks) {
    await mockDelay();
    return { data: fallback, message: 'mock' };
  }

  try {
    const token = readStorageToken();
    const response = await fetch(resolveUrl(path), {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(init.headers || {})
      }
    });

    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    const text = await response.text();
    const payload = text ? JSON.parse(text) : null;
    return { data: normalizePayload<T>(payload, fallback), message: 'ok' };
  } catch (error) {
    return { data: fallback, message: error instanceof Error ? error.message : 'Unknown error' };
  }
};

const mockProperties: PropertySummary[] = [
  { id: 'p1', title: 'Maison Bellevue', location: 'Lyon', price: 420000, type: 'House', status: 'Available' },
  { id: 'p2', title: 'Appartement Lumière', location: 'Paris', price: 610000, type: 'Apartment', status: 'Reserved' }
];

const mockProfile: UserProfile = {
  id: 'u1',
  name: 'Alicia Dubois',
  role: 'Director',
  email: 'alicia@lawim.example'
};

export const apiSdk = {
  async login(credentials: AuthCredentials): Promise<ApiResponse<AuthSession>> {
    if (useMocks) {
      await mockDelay();
      return { data: { user: mockProfile, token: 'mock-token', roles: ['admin', 'director'] }, message: 'mock' };
    }
    return requestJson<AuthSession>('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }, {
      user: mockProfile,
      token: 'mock-token',
      roles: ['admin', 'director']
    });
  },

  async logout(): Promise<ApiResponse<{ success: boolean }>> {
    if (useMocks) {
      await mockDelay();
      return { data: { success: true }, message: 'mock' };
    }
    return requestJson<{ success: boolean }>('/auth/logout', { method: 'POST' }, { success: true });
  },

  async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    if (useMocks) {
      await mockDelay();
      return { data: { token: 'mock-token' }, message: 'mock' };
    }
    return requestJson<{ token: string }>('/auth/refresh', { method: 'POST' }, { token: 'mock-token' });
  },

  async getSession(): Promise<ApiResponse<AuthSession | null>> {
    if (useMocks) {
      const token = readStorageToken();
      return { data: token ? { user: mockProfile, token, roles: ['admin'] } : null, message: 'mock' };
    }
    return requestJson<AuthSession | null>('/auth/session', { method: 'GET' }, null);
  },

  async getProfile(): Promise<ApiResponse<UserProfile>> {
    if (useMocks) {
      await mockDelay();
      return { data: mockProfile, message: 'mock' };
    }
    return requestJson<UserProfile>('/v2/users/me', { method: 'GET' }, mockProfile);
  },

  async getUsers(): Promise<ApiResponse<UserProfile[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [mockProfile], message: 'mock' };
    }
    return requestJson<UserProfile[]>('/v2/users', { method: 'GET' }, [mockProfile]);
  },

  async getProperties(params?: { search?: string; page?: number; pageSize?: number }): Promise<ApiResponse<PropertySummary[]>> {
    if (useMocks) {
      await mockDelay();
      const search = params?.search?.toLowerCase() ?? '';
      const filtered = mockProperties.filter((property) => property.title.toLowerCase().includes(search) || property.location.toLowerCase().includes(search));
      return { data: filtered.slice(0, params?.pageSize ?? 10), message: 'mock' };
    }
    const query = new URLSearchParams();
    if (params?.search) query.set('q', params.search);
    if (params?.page) query.set('page', String(params.page));
    if (params?.pageSize) query.set('page_size', String(params.pageSize));
    return requestJson<PropertySummary[]>(`/v2/properties${query.toString() ? `?${query.toString()}` : ''}`, { method: 'GET' }, mockProperties);
  },

  async getProperty(id: string): Promise<ApiResponse<PropertyDetail | null>> {
    if (useMocks) {
      await mockDelay();
      const property = mockProperties.find((item) => item.id === id);
      return { data: property ? { ...property, description: 'Beautiful property with strong yield.', surface: '120 m²', bedrooms: 3, bathrooms: 2 } : null, message: 'mock' };
    }
    return requestJson<PropertyDetail | null>(`/v2/properties/${id}`, { method: 'GET' }, null);
  },

  async getDashboardSummary(): Promise<ApiResponse<DashboardSummary>> {
    if (useMocks) {
      await mockDelay();
      return { data: { properties: 12, opportunities: 6, communications: 18, pendingTasks: 4 }, message: 'mock' };
    }
    return requestJson<DashboardSummary>('/v2/dashboard', { method: 'GET' }, { properties: 0, opportunities: 0, communications: 0, pendingTasks: 0 });
  },

  async getFavorites(): Promise<ApiResponse<FavoriteItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'f1', title: 'Maison Bellevue', type: 'Property', score: 94 }], message: 'mock' };
    }
    return requestJson<FavoriteItem[]>('/v2/favorites', { method: 'GET' }, []);
  },

  async getNotifications(): Promise<ApiResponse<NotificationItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'n1', title: 'Inspection confirmed', message: 'The inspection is scheduled for Thursday', read: false }], message: 'mock' };
    }
    return requestJson<NotificationItem[]>('/v2/notifications', { method: 'GET' }, []);
  },

  async getRequests(): Promise<ApiResponse<RequestItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'r1', title: 'Document review', status: 'Pending' }], message: 'mock' };
    }
    return requestJson<RequestItem[]>('/v2/requests', { method: 'GET' }, []);
  },

  async getDocuments(): Promise<ApiResponse<DocumentItem[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'd1', title: 'Listing memo', kind: 'PDF' }], message: 'mock' };
    }
    return requestJson<DocumentItem[]>('/v2/documents', { method: 'GET' }, []);
  },

  async getMarketListings(): Promise<ApiResponse<MarketListing[]>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'm1', title: 'Audit immobilier', category: 'Services', price: 1800, status: 'Open' }, { id: 'm2', title: 'Campagne de prospection', category: 'Marketing', price: 3200, status: 'In review' }], message: 'mock' };
    }
    return requestJson<MarketListing[]>('/v2/marketplace/providers', { method: 'GET' }, []);
  },

  async getWorkflowInstances(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'w1', title: 'Lead nurture', status: 'Ready' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/workflows/instances', { method: 'GET' }, []);
  },

  async getCommunicationItems(): Promise<ApiResponse<Array<{ id: string; title: string; channel: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'c1', title: 'Follow-up', channel: 'Email' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; channel: string }>>('/v2/communication/messages', { method: 'GET' }, []);
  },

  async getAnalytics(): Promise<ApiResponse<Array<{ label: string; value: number }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Conversion', value: 82 }, { label: 'Engagement', value: 71 }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: number }>>('/v2/analytics/dashboard', { method: 'GET' }, []);
  },

  async getSecuritySummary(): Promise<ApiResponse<Array<{ label: string; value: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Audit', value: 'Complete' }, { label: 'Risk', value: 'Low' }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: string }>>('/v2/security/stats', { method: 'GET' }, []);
  },

  async getOperations(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'o1', title: 'Deployment health', status: 'Healthy' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/operations', { method: 'GET' }, []);
  },

  async getDeploymentStatus(): Promise<ApiResponse<Array<{ label: string; value: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Environment', value: 'Production' }, { label: 'Status', value: 'Online' }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: string }>>('/v2/deployment/status', { method: 'GET' }, []);
  },

  async getBackupStatus(): Promise<ApiResponse<Array<{ label: string; value: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ label: 'Last backup', value: '2h ago' }, { label: 'Retention', value: '30 days' }], message: 'mock' };
    }
    return requestJson<Array<{ label: string; value: string }>>('/v2/backup/status', { method: 'GET' }, []);
  },

  async getReleases(): Promise<ApiResponse<Array<{ id: string; title: string; status: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 'r1', title: 'Release Program O', status: 'Planned' }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; status: string }>>('/v2/releases', { method: 'GET' }, []);
  },

  async getSourceIntelligence(): Promise<ApiResponse<Array<{ id: string; title: string; score: number }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ id: 's1', title: 'Reference code ingestion', score: 91 }], message: 'mock' };
    }
    return requestJson<Array<{ id: string; title: string; score: number }>>('/v2/source-intelligence/dashboard', { method: 'GET' }, []);
  },

  async getAssistantSuggestions(): Promise<ApiResponse<Array<{ title: string; description: string }>>> {
    if (useMocks) {
      await mockDelay();
      return { data: [{ title: 'Summarize pipeline', description: 'Review last updates' }], message: 'mock' };
    }
    return requestJson<Array<{ title: string; description: string }>>('/v2/assistant/agents', { method: 'GET' }, []);
  },

  async askAssistant(payload: AssistantMessagePayload): Promise<ApiResponse<AssistantReply>> {
    if (useMocks) {
      await mockDelay();
      return { data: { reply: `I can help with: ${payload.message}`, suggestions: ['Review pipeline', 'Send follow-up'] }, message: 'mock' };
    }
    return requestJson<AssistantReply>('/v2/assistant/ask', { method: 'POST', body: JSON.stringify(payload) }, { reply: 'Connected to assistant service', suggestions: [] });
  },

  async createEstimation(payload: EstimationPayload): Promise<ApiResponse<EstimationResult>> {
    if (useMocks) {
      await mockDelay();
      return { data: { estimate: '€500k - €560k', confidence: 'High' }, message: 'mock' };
    }
    return requestJson<EstimationResult>('/v2/estimation', { method: 'POST', body: JSON.stringify(payload) }, { estimate: 'Pending', confidence: 'Low' });
  }
};

export type ApiSdk = typeof apiSdk;
