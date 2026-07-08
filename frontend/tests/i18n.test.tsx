import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LanguageProvider, LanguageSwitcher, translate } from '@ui';

beforeEach(() => {
  window.localStorage.clear();
  document.documentElement.lang = 'fr';
});

afterEach(() => {
  window.localStorage.clear();
  document.documentElement.lang = 'fr';
});

describe('frontend i18n', () => {
  it('translates core actions in French, English, and Pidgin', () => {
    expect(translate('auth.login.title', 'fr')).toBe('Connexion');
    expect(translate('auth.login.title', 'en')).toBe('Login');
    expect(translate('auth.login.title', 'pcm')).toBe('Login');
    expect(translate('auth.login.forgot', 'fr')).toBe('Mot de passe oublié');
    expect(translate('auth.login.create', 'en')).toBe('Create account');
    expect(translate('auth.contact.website', 'pcm')).toBe('Website');
    expect(translate('dashboard.whats_next', 'pcm')).toBe('Wetin next?');
    expect(translate('shared.logout', 'pcm')).toBe('Comot');
    expect(translate('auth.login.banner.note', 'fr')).toBe('');
  });

  it('persists the selected language and restores it on remount', async () => {
    const user = userEvent.setup();

    const rendered = render(
      <LanguageProvider>
        <LanguageSwitcher />
      </LanguageProvider>
    );

    const select = screen.getByRole('combobox', { name: /langue/i });
    expect(select).toHaveValue('fr');

    await user.selectOptions(select, 'en');

    expect(select).toHaveValue('en');
    await waitFor(() => {
      expect(window.localStorage.getItem('lawim.language')).toBe('en');
      expect(document.documentElement.lang).toBe('en');
    });

    rendered.unmount();

    render(
      <LanguageProvider>
        <LanguageSwitcher />
      </LanguageProvider>
    );

    expect(screen.getByRole('combobox', { name: /language/i })).toHaveValue('en');

    await user.selectOptions(screen.getByRole('combobox', { name: /language/i }), 'pcm');

    await waitFor(() => {
      expect(window.localStorage.getItem('lawim.language')).toBe('pcm');
      expect(document.documentElement.lang).toBe('pcm');
    });
    expect(screen.getByRole('combobox', { name: /languag/i })).toHaveValue('pcm');
  });
});
