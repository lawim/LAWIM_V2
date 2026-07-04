import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { CognitiveCorePage } from '../apps/admin/src/CognitiveCorePage';
import { PermanentConversationPage } from '../apps/admin/src/PermanentConversationPage';
import { AdvancedDigitalTwinPage } from '../apps/admin/src/AdvancedDigitalTwinPage';
import { DistributedIntelligencePage } from '../apps/admin/src/DistributedIntelligencePage';
import { AutonomousWorkflowPreviewPage } from '../apps/admin/src/AutonomousWorkflowPreviewPage';
import { CognitiveKnowledgeEvolutionPage } from '../apps/admin/src/CognitiveKnowledgeEvolutionPage';
import { PredictiveIntelligencePreviewPage } from '../apps/admin/src/PredictiveIntelligencePreviewPage';
import { AutonomyGovernancePage } from '../apps/admin/src/AutonomyGovernancePage';
import { CognitiveOperationsPage } from '../apps/admin/src/CognitiveOperationsPage';
import { FutureCompatibilityPage } from '../apps/admin/src/FutureCompatibilityPage';
import { Lawim3ConsolePage } from '../apps/admin/src/Lawim3ConsolePage';
import { Lawim3ConstitutionPage } from '../apps/admin/src/Lawim3ConstitutionPage';

describe('LAWIM 3.0 foundation', () => {
  it('renders the cognitive core surface', () => {
    render(<CognitiveCorePage />);
    expect(screen.getByText('Cognitive Core Center')).toBeInTheDocument();
  });

  it('renders the permanent conversation surface', () => {
    render(<PermanentConversationPage />);
    expect(screen.getByText('Permanent Conversation Center')).toBeInTheDocument();
  });

  it('renders the advanced digital twin surface', () => {
    render(<AdvancedDigitalTwinPage />);
    expect(screen.getByText('Advanced Digital Twin Center')).toBeInTheDocument();
  });

  it('renders the distributed intelligence surface', () => {
    render(<DistributedIntelligencePage />);
    expect(screen.getByText('Distributed Intelligence Center')).toBeInTheDocument();
  });

  it('renders the autonomous workflow preview surface', () => {
    render(<AutonomousWorkflowPreviewPage />);
    expect(screen.getByText('Autonomous Workflow Preview Center')).toBeInTheDocument();
  });

  it('renders the cognitive knowledge evolution surface', () => {
    render(<CognitiveKnowledgeEvolutionPage />);
    expect(screen.getByText('Knowledge Evolution Center')).toBeInTheDocument();
  });

  it('renders the predictive intelligence preview surface', () => {
    render(<PredictiveIntelligencePreviewPage />);
    expect(screen.getByText('Predictive Intelligence Preview')).toBeInTheDocument();
  });

  it('renders the autonomy governance surface', () => {
    render(<AutonomyGovernancePage />);
    expect(screen.getByText('Autonomy Governance Center')).toBeInTheDocument();
  });

  it('renders the cognitive operations surface', () => {
    render(<CognitiveOperationsPage />);
    expect(screen.getByText('Cognitive Operations Center')).toBeInTheDocument();
  });

  it('renders the future compatibility surface', () => {
    render(<FutureCompatibilityPage />);
    expect(screen.getByText('Future Compatibility Center')).toBeInTheDocument();
  });

  it('renders the LAWIM 3.0 console surface', () => {
    render(<Lawim3ConsolePage />);
    expect(screen.getByText('LAWIM 3.0 Dashboard')).toBeInTheDocument();
  });

  it('renders the constitution surface', () => {
    render(<Lawim3ConstitutionPage />);
    expect(screen.getByText('LAWIM 3.0 Constitution Console')).toBeInTheDocument();
  });
});
