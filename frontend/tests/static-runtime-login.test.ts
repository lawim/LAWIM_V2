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
    const officialContact = {
      company_name: 'LAWIM',
      brand_slogan: 'L’immobilier autrement',
      brand_subslogan: '',
      institutional_tagline: 'Intelligent Real Estate Relationships',
      brand_message: 'Plateforme officielle LAWIM',
      brand_positioning: 'Connecting people, properties and opportunities.',
      phone_number: '686 822 667',
      phone_e164: '+237686822667',
      phone_international: '+237 686 822 667',
      whatsapp_number: '686 822 667',
      green_api_number: '686 822 667',
      facebook_username: '@lawimofficial',
      whatsapp_username: '@lawimofficial',
      telegram_bot: '@lawim_assistant_bot',
      support_contact: 'LAWIM',
      support_email: 'contact@lawim.app',
      default_country: 'Cameroon',
      website_url: 'https://lawim.app',
      whatsapp_link: 'https://wa.me/237686822667',
      telegram_link: 'https://t.me/lawim_assistant_bot',
      facebook_link: 'https://facebook.com/lawimofficial',
    };

    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(String(input), window.location.origin);
      const path = `${url.pathname}${url.search}`;
      const headers = new Headers(init?.headers || {});
      const hasAuth = headers.has('Authorization');

      if (path === '/api/auth/login') {
        const requestBody = typeof init?.body === 'string' ? JSON.parse(init.body) : {};
        expect(requestBody.identifier).toBe('admin');
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
                official_contact: officialContact,
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
                official_contact: officialContact,
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
    expect(document.getElementById('login-identifier')).toBeInTheDocument();
    expect(document.querySelector('.brand-mark')).toBeInTheDocument();
    expect(document.querySelector('.auth-slogan')).toHaveTextContent(/L’immobilier autrement/i);
    expect(document.querySelector('.auth-panel #auth-contact')).toBeNull();
    expect(document.getElementById('auth-contact')).toHaveTextContent(/contact@lawim\.app/i);
    expect(document.getElementById('auth-contact')).toHaveTextContent(/lawim\.app/i);
    expect(document.getElementById('register-panel')).toHaveAttribute('hidden');

    debugSpy.mockClear();

    const identifierInput = document.getElementById('login-identifier') as HTMLInputElement;
    const passwordInput = document.getElementById('login-password') as HTMLInputElement;
    const loginForm = document.getElementById('login-form') as HTMLFormElement;

    identifierInput.value = 'admin';
    passwordInput.value = 'secure-password';
    loginForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));

    await waitFor(() => {
      expect(document.querySelector('[data-journey-panel="admin"]')).not.toHaveAttribute('hidden');
      expect(document.getElementById('admin-dashboard')).toHaveTextContent(/Runtime metrics/i);
      expect(document.getElementById('current-user')).toHaveTextContent(/Admin User/);
    });

    expect(document.getElementById('login-form')).toBeInTheDocument();
    expect(document.querySelector('.auth-panel')).toHaveAttribute('hidden');
    expect(document.getElementById('register-panel')).toHaveAttribute('hidden');
    expect(document.getElementById('logout-button')).not.toHaveAttribute('hidden');
    expect(document.getElementById('runtime-chip')).toHaveAttribute('hidden');

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

  it('switches between login and register panels without showing the contact band above the form', async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(String(input), window.location.origin);
      const path = `${url.pathname}${url.search}`;

      if (path === '/api/health') {
        return createJsonResponse({
          status: 'ok',
          environment: { app_env: 'test' },
          database: { driver: 'sqlite', schema_version: 19 },
          summary: { events: 0 },
        });
      }

      if (path === '/api/bootstrap') {
        return createJsonResponse({
          current_user: null,
          official_contact: {
            company_name: 'LAWIM',
            brand_slogan: 'L’immobilier autrement',
            support_email: 'contact@lawim.app',
            website_url: 'https://lawim.app',
            phone_e164: '+237686822667',
            phone_international: '+237 686 822 667',
            whatsapp_username: '@lawimofficial',
            facebook_username: '@lawimofficial',
            whatsapp_link: 'https://wa.me/237686822667',
            facebook_link: 'https://facebook.com/lawimofficial',
          },
          summary: {},
          organizations: [],
          properties: [],
          media: [],
          matches: [],
          conversations: [],
          notifications: [],
          features: {},
        });
      }

      return createJsonResponse({});
    });

    installStaticRuntime(fetchMock);

    await waitFor(() => {
      expect(document.getElementById('login-form')).toBeInTheDocument();
    });

    expect(document.getElementById('register-panel')).toHaveAttribute('hidden');
    expect(document.querySelector('.auth-panel #auth-contact')).toBeNull();

    (document.getElementById('login-create') as HTMLButtonElement).click();

    await waitFor(() => {
      expect(document.querySelector('.auth-panel')).toHaveAttribute('hidden');
      expect(document.getElementById('register-panel')).not.toHaveAttribute('hidden');
    });

    expect(document.getElementById('register-form')).toBeInTheDocument();
    expect(document.getElementById('register-terms')).toBeInTheDocument();

    (document.getElementById('register-back') as HTMLButtonElement).click();

    await waitFor(() => {
      expect(document.getElementById('register-panel')).toHaveAttribute('hidden');
      expect(document.querySelector('.auth-panel')).not.toHaveAttribute('hidden');
    });
  });
});
