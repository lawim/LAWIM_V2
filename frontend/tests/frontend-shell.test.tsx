import '@testing-library/jest-dom/vitest';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { WebApp } from '../apps/web/src/App';
import { AdminApp } from '../apps/admin/src/App';

describe('LAWIM frontend shell', () => {
  it('renders the public web app shell', () => {
    render(
      <MemoryRouter>
        <WebApp />
      </MemoryRouter>
    );

    expect(screen.getByRole('heading', { name: /operational intelligence for modern teams/i })).toBeInTheDocument();
    expect(screen.getByText(/a polished frontend shell for monitoring, coordination, and mission control workflows/i)).toBeInTheDocument();
    expect(screen.getByText(/search/i)).toBeInTheDocument();
  });

  it('renders the administration shell', () => {
    render(
      <MemoryRouter>
        <AdminApp />
      </MemoryRouter>
    );

    expect(screen.getByRole('heading', { name: /manage operations and oversight/i })).toBeInTheDocument();
    expect(screen.getByText(/administrative controls, governance workflows, and deployment readiness in one place/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /operations/i })).toBeInTheDocument();
  });
});
