import '@testing-library/jest-dom/vitest';
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AgentsConsolePage } from '../apps/admin/src/AgentsConsole';

describe('agent dashboard', () => {
  it('renders the administration surface for the agent platform', () => {
    render(<AgentsConsolePage />);

    expect(screen.getByRole('heading', { name: /lawim agent platform/i })).toBeInTheDocument();
    expect(screen.getByText(/brain routing/i)).toBeInTheDocument();
    expect(screen.getByText(/agent registry/i)).toBeInTheDocument();
    expect(screen.getAllByText(/approval queue/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/13 agents/i)).toBeInTheDocument();
  });
});
