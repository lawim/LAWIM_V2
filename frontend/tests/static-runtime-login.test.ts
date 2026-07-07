import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { waitFor } from '@testing-library/react';
import { readFileSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const testDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(testDir, '..', '..');
const staticIndexHtml = readFileSync(path.join(repoRoot, 'code/lawim_v2/static/index.html'), 'utf8');
const staticAppJs = readFileSync(path.join(repoRoot, 'code/lawim_v2/static/app.js'), 'utf8');

const createJsonResponse = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json',
    },
  });

function installStaticRuntime(fetchMock: typeof fetch) {
  const bodyMatch = staticIndexHtml.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (!bodyMatch) {
    throw new Error('Unable to extract static runtime body');
  }

  document.body.innerHTML = bodyMatch[1];
  vi.stubGlobal('fetch', fetchMock);
  vi.stubGlobal('localStorage', window.localStorage);

  const debugSpy = vi.spyOn(console, 'debug').mockImplementation(() => undefined);
  window.eval(staticAppJs);
  document.dispatchEvent(new Event('DOMContentLoaded', { bubbles: true, cancelable: true }));

  return debugSpy;
}

describe('static runtime login flow', () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.body.innerHTML = '';
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  afterEach(() => {
    window.localStorage.clear();
    document.body.innerHTML = '';
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('renders the admin dashboard after login without exposing demo credentials', async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(String(input), window.location.origin);
      const path = `${url.pathname}${url.search}`;
      const headers = new Headers(init?.headers || {});
      const hasAuth = headers.has('Authorization');

      if (path === '/api/auth/login') {
        return createJsonResponse(
          {
            user: {
              email: 'admin@lawim.app',
              role: 'admin',
            },
            token: 'admin-token',
          },
          201,
        );
      }

      if (path === '/api/health') {
        return createJsonResponse(
          hasAuth
            ? {
                environment: {
                  app_env: 'test',
                },
                database: {
                  driver: 'sqlite',
                  schema_version: 1,
                },
                summary: {
                  events: 0,
                },
              }
            : {
                status: 'ok',
                environment: {
                  app_env: 'test',
                },
                database: {
                  driver: 'sqlite',
                  schema_version: 1,
                },
                summary: {
                  events: 0,
                },
              },
        );
      }

      if (path === '/api/bootstrap') {
        return createJsonResponse(
          hasAuth
              ? {
                current_user: {
                  full_name: 'Admin User',
                  email: 'admin@lawim.app',
                  role: 'admin',
                  roles: ['admin'],
                },
                summary: {},
                organizations: [],
                properties: [],
                media: [],
                matches: [],
                conversations: [],
                notifications: [],
                features: {},
              }
            : {
                current_user: null,
                summary: {},
                organizations: [],
                properties: [],
                media: [],
                matches: [],
                conversations: [],
                notifications: [],
                features: {},
              },
        );
      }

      if (path === '/api/v2/projects') {
        return createJsonResponse({ projects: [] });
      }

      if (path === '/api/v2/partners') {
        return createJsonResponse({ partners: [] });
      }

      if (path === '/api/v2/services') {
        return createJsonResponse({ services: [] });
      }

      if (path === '/api/v2/knowledge/documents') {
        return createJsonResponse({ documents: [] });
      }

      if (path === '/api/v2/knowledge/categories') {
        return createJsonResponse({ categories: [] });
      }

      if (path === '/api/metrics') {
        return createJsonResponse({
          metrics: {
            requests_total: 0,
            matches_total: 0,
            conversations_total: 0,
          },
        });
      }

      if (path.startsWith('/api/events')) {
        return createJsonResponse({ events: [] });
      }

      return createJsonResponse({});
    });

    const debugSpy = installStaticRuntime(fetchMock);

    await waitFor(() => {
      expect(document.getElementById('runtime-chip')).toHaveTextContent(/OK/i);
    });

    expect(document.body).not.toHaveTextContent(/admin@lawim\.local/i);
    expect(document.body).not.toHaveTextContent(/lawim-demo/i);
    expect(document.getElementById('login-form')).toBeInTheDocument();
    expect(document.querySelector('.brand-mark')).toBeInTheDocument();
    expect(document.querySelector('.brand-lockup__copy .lede')).toHaveTextContent(/accompagnement immobilier intelligent/i);
    expect(document.getElementById('login-form')?.querySelector('[name="role"]')).toBeNull();

    debugSpy.mockClear();

    const emailInput = document.getElementById('login-email') as HTMLInputElement;
    const passwordInput = document.getElementById('login-password') as HTMLInputElement;
    const loginForm = document.getElementById('login-form') as HTMLFormElement;

    emailInput.value = 'admin@lawim.app';
    passwordInput.value = 'secure-password';
    loginForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));

    await waitFor(() => {
      expect(document.querySelector('[data-journey-panel="admin"]')).not.toHaveAttribute('hidden');
      expect(document.getElementById('admin-dashboard')).toHaveTextContent(/Runtime metrics/i);
      expect(document.getElementById('current-user')).toHaveTextContent(/Admin User/);
    });

    const labels = debugSpy.mock.calls.map(([label]) => label);
    expect(labels).toEqual([
      'LOGIN_OK',
      'ROLE_RESOLVED',
      'DASHBOARD_SELECTED',
      'REFRESH_START',
      'DASHBOARD_RENDERED',
      'ROLE_DASHBOARD_RENDERED',
      'REFRESH_DONE',
      'APPLY_JOURNEY',
      'RENDER_DONE',
      'DASHBOARD_RENDERED'
    ]);

    expect(debugSpy.mock.calls[0]?.[1]).toMatchObject({
      email: 'admin@lawim.app',
      role: 'admin',
      journey: 'admin',
    });
    expect(debugSpy.mock.calls[1]?.[1]).toMatchObject({
      role: 'admin',
      journey: 'admin',
    });
    expect(debugSpy.mock.calls[2]?.[1]).toMatchObject({
      role: 'admin',
      journey: 'admin',
    });
  });
});
