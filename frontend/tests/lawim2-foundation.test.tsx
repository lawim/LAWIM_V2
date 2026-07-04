import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { MemoryEvolutionPage } from '../apps/admin/src/MemoryEvolutionPage';
import { MonthlyReviewPage } from '../apps/admin/src/MonthlyReviewPage';
import { SupervisedLearningPage } from '../apps/admin/src/SupervisedLearningPage';
import { DigitalTwinIntelligencePage } from '../apps/admin/src/DigitalTwinIntelligencePage';
import { BrainIntelligencePage } from '../apps/admin/src/BrainIntelligencePage';
import { ConversationIntelligencePage } from '../apps/admin/src/ConversationIntelligencePage';
import { IntelligenceGovernancePage } from '../apps/admin/src/IntelligenceGovernancePage';
import { Lawim2ConsolePage } from '../apps/admin/src/Lawim2ConsolePage';

describe('LAWIM 2.0 foundation', () => {
  it('renders the memory evolution surface', () => {
    render(<MemoryEvolutionPage />);
    expect(screen.getByText('Memory Evolution Center')).toBeInTheDocument();
  });

  it('renders the monthly review surface', () => {
    render(<MonthlyReviewPage />);
    expect(screen.getByText('Monthly Intelligence Review Center')).toBeInTheDocument();
  });

  it('renders the supervised learning surface', () => {
    render(<SupervisedLearningPage />);
    expect(screen.getByText('Learning Governance Center')).toBeInTheDocument();
  });

  it('renders the digital twin intelligence surface', () => {
    render(<DigitalTwinIntelligencePage />);
    expect(screen.getByText('Digital Twin Intelligence Layer')).toBeInTheDocument();
  });

  it('renders the brain intelligence surface', () => {
    render(<BrainIntelligencePage />);
    expect(screen.getByText('Brain Intelligence Orchestration')).toBeInTheDocument();
  });

  it('renders the conversation intelligence surface', () => {
    render(<ConversationIntelligencePage />);
    expect(screen.getByText('Conversation Intelligence')).toBeInTheDocument();
  });

  it('renders the intelligence governance surface', () => {
    render(<IntelligenceGovernancePage />);
    expect(screen.getByText('AI Governance Center')).toBeInTheDocument();
  });

  it('renders the LAWIM 2.0 console surface', () => {
    render(<Lawim2ConsolePage />);
    expect(screen.getByText('LAWIM 2.0 Dashboard')).toBeInTheDocument();
  });
});
