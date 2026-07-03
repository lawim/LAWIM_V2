import { describe, expect, it } from 'vitest';
import { ObservationCollector, LearningAnalyzer, RecommendationGenerator, ValidationWorkflow } from '../packages/learning/src';

describe('Learning framework', () => {
  it('produces a recommendation with a validation workflow', () => {
    const collector = new ObservationCollector();
    const observations = collector.collect([{ id: 'e-1', source: 'analytics', type: 'trend', payload: { metric: 'conversion', value: 0.82 }, createdAt: new Date().toISOString() }]);
    const analyzer = new LearningAnalyzer();
    const recommendations = analyzer.analyze(observations);
    const generator = new RecommendationGenerator();
    const recommendation = generator.generate(recommendations[0]);
    const workflow = new ValidationWorkflow();
    const validated = workflow.validate(recommendation, 'accepted');

    expect(validated.status).toBe('accepted');
    expect(validated.history.length).toBeGreaterThan(0);
  });
});
