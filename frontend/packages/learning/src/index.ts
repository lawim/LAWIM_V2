export interface LearningEvent {
  id: string;
  source: string;
  type: string;
  payload: Record<string, unknown>;
  createdAt: string;
}

export interface LearningObservation {
  id: string;
  source: string;
  summary: string;
  trend: 'up' | 'down' | 'stable';
}

export interface LearningMetric {
  name: string;
  value: number;
}

export interface LearningConfidence {
  score: number;
  level: 'low' | 'medium' | 'high';
}

export interface LearningImpact {
  expected: string;
  severity: 'low' | 'medium' | 'high';
}

export interface LearningRecommendation {
  id: string;
  title: string;
  summary: string;
  confidence: number;
  impact: string;
  status: 'pending' | 'accepted' | 'rejected' | 'postponed' | 'implemented';
  history: Array<{ status: string; timestamp: string }>;
}

export interface LearningReport {
  observations: LearningObservation[];
  recommendations: LearningRecommendation[];
  metrics: LearningMetric[];
}

export class ObservationCollector {
  collect(events: LearningEvent[]): LearningObservation[] {
    return events.map((event) => ({
      id: event.id,
      source: event.source,
      summary: `${event.type} observed from ${event.source}`,
      trend: 'stable'
    }));
  }
}

export class LearningAnalyzer {
  analyze(observations: LearningObservation[]) {
    return observations.map((observation) => ({
      id: observation.id,
      summary: observation.summary,
      confidence: 0.8,
      impact: 'medium'
    }));
  }
}

export class RecommendationGenerator {
  generate(recommendation: { id: string; summary: string; confidence: number; impact: string }) {
    return {
      id: recommendation.id,
      title: `Recommendation ${recommendation.id}`,
      summary: recommendation.summary,
      confidence: recommendation.confidence,
      impact: recommendation.impact,
      status: 'pending' as const,
      history: [{ status: 'pending', timestamp: new Date().toISOString() }]
    } satisfies LearningRecommendation;
  }
}

export class MonthlyReviewGenerator {
  generate(observations: LearningObservation[]): LearningReport {
    return {
      observations,
      recommendations: observations.map((observation) => ({
        id: observation.id,
        title: `Monthly review for ${observation.source}`,
        summary: observation.summary,
        confidence: 0.81,
        impact: 'medium',
        status: 'pending',
        history: [{ status: 'pending', timestamp: new Date().toISOString() }]
      })),
      metrics: [{ name: 'observations', value: observations.length }]
    };
  }
}

export class ValidationWorkflow {
  validate(recommendation: LearningRecommendation, decision: 'accepted' | 'rejected' | 'postponed' | 'implemented') {
    return {
      ...recommendation,
      status: decision,
      history: [...recommendation.history, { status: decision, timestamp: new Date().toISOString() }]
    };
  }
}
