import { useCallback, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiSdk, type BrainProposalResult, type BrainFindMatchesResult } from '@api-sdk';
import { useLanguage } from '@ui';

type Lang = 'fr' | 'en' | 'pcm';

function getLang(language: string): Lang {
  if (language === 'en' || language === 'pcm') return language;
  return 'fr';
}

const STATUS_LABELS: Record<string, Record<Lang, string>> = {
  detected: {
    fr: 'Détecté',
    en: 'Detected',
    pcm: 'Don see am',
  },
  proposed: {
    fr: 'Proposé',
    en: 'Proposed',
    pcm: 'Don propose',
  },
  consulted: {
    fr: 'Consulté',
    en: 'Consulted',
    pcm: 'Don check',
  },
  accepted: {
    fr: 'Accepté',
    en: 'Accepted',
    pcm: 'Don take am',
  },
  rejected: {
    fr: 'Refusé',
    en: 'Rejected',
    pcm: 'No take',
  },
  deferred: {
    fr: 'Reporté',
    en: 'Deferred',
    pcm: 'Put for later',
  },
  consent_pending: {
    fr: 'Consentement requis',
    en: 'Consent pending',
    pcm: 'Need your okay',
  },
  relation_established: {
    fr: 'Mise en relation effectuée',
    en: 'Relationship established',
    pcm: 'Don connect',
  },
  contact_made: {
    fr: 'Contact établi',
    en: 'Contact made',
    pcm: 'Don talk',
  },
  in_progress: {
    fr: 'En cours',
    en: 'In progress',
    pcm: 'Dey go',
  },
  completed: {
    fr: 'Terminé',
    en: 'Completed',
    pcm: 'Don finish',
  },
};

const TYPE_LABELS: Record<string, Record<Lang, string>> = {
  person_to_property: {
    fr: 'Bien immobilier',
    en: 'Property',
    pcm: 'Property',
  },
  person_to_person: {
    fr: 'Personne',
    en: 'Person',
    pcm: 'Person',
  },
  person_to_partner: {
    fr: 'Professionnel',
    en: 'Professional',
    pcm: 'Professional',
  },
};

function formatStatus(status: string, lang: Lang): string {
  return STATUS_LABELS[status]?.[lang] || status;
}

function formatType(relationType: string, lang: Lang): string {
  return TYPE_LABELS[relationType]?.[lang] || relationType;
}

function scoreGrade(score: number): { label: string; color: string } {
  if (score >= 80) return { label: 'Excellent', color: 'text-emerald-600 bg-emerald-50 border-emerald-200' };
  if (score >= 60) return { label: 'Bon', color: 'text-sky-600 bg-sky-50 border-sky-200' };
  if (score >= 40) return { label: 'Moyen', color: 'text-amber-600 bg-amber-50 border-amber-200' };
  return { label: 'Faible', color: 'text-slate-500 bg-slate-50 border-slate-200' };
}

function statusColor(status: string): string {
  if (status === 'accepted' || status === 'relation_established' || status === 'contact_made' || status === 'completed') return 'border-emerald-300 bg-emerald-50';
  if (status === 'rejected' || status === 'cancelled') return 'border-rose-300 bg-rose-50';
  if (status === 'consent_pending') return 'border-amber-300 bg-amber-50';
  if (status === 'deferred') return 'border-slate-300 bg-slate-50';
  return 'border-slate-200 bg-white';
}

function statusActionColor(status: string): string {
  if (status === 'accepted' || status === 'relation_established') return 'bg-emerald-500 hover:bg-emerald-600';
  if (status === 'rejected' || status === 'cancelled') return 'bg-rose-500 hover:bg-rose-600';
  if (status === 'consent_pending') return 'bg-amber-500 hover:bg-amber-600';
  return 'bg-slate-900 hover:bg-slate-800';
}

interface MatchResultsPanelProps {
  projectId: number;
  language?: string;
  onNavigate?: (path: string) => void;
}

export function MatchResultsPanel({ projectId, language: languageProp, onNavigate }: MatchResultsPanelProps) {
  const { language: langFromCtx } = useLanguage();
  const lang = getLang(languageProp || langFromCtx);
  const queryClient = useQueryClient();
  const [searching, setSearching] = useState(false);

  const {
    data: matchesData,
    isLoading: matchesLoading,
    isError: matchesError,
    refetch: refetchMatches,
  } = useQuery({
    queryKey: ['brain-proposals', projectId],
    queryFn: () => apiSdk.brainProposals(projectId),
    enabled: !!projectId,
    staleTime: 15_000,
  });

  const {
    data: relationsData,
  } = useQuery({
    queryKey: ['brain-relations', projectId],
    queryFn: () => apiSdk.brainRelations(projectId),
    enabled: !!projectId,
    staleTime: 30_000,
  });

  const findMatchesMutation = useMutation({
    mutationFn: () => apiSdk.brainFindMatches({ project_id: projectId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brain-proposals', projectId] });
    },
  });

  const acceptMutation = useMutation({
    mutationFn: (proposalId: number) => apiSdk.brainAcceptProposal({ proposal_id: proposalId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brain-proposals', projectId] });
      queryClient.invalidateQueries({ queryKey: ['brain-relations', projectId] });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: (proposalId: number) => apiSdk.brainRejectProposal({ proposal_id: proposalId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brain-proposals', projectId] });
    },
  });

  const consentMutation = useMutation({
    mutationFn: (proposalId: number) => apiSdk.brainGrantConsent({ proposal_id: proposalId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brain-proposals', projectId] });
      queryClient.invalidateQueries({ queryKey: ['brain-relations', projectId] });
    },
  });

  const handleFindMatches = useCallback(async () => {
    setSearching(true);
    try {
      await findMatchesMutation.mutateAsync();
    } finally {
      setSearching(false);
    }
  }, [findMatchesMutation]);

  const proposals: BrainProposalResult[] = matchesData?.data ?? [];
  const relations = relationsData?.data ?? [];
  const hasEstablishedRelations = relations.some((r) => r.status === 'relation_established');
  const activeProposals = proposals.filter((p) => !['rejected', 'cancelled', 'expired'].includes(p.status));
  const inactiveCount = proposals.length - activeProposals.length;

  /* ── States ── */

  if (matchesLoading) {
    return (
      <div className="space-y-3 p-4">
        <div className="animate-pulse space-y-2">
          <div className="h-6 w-48 rounded bg-slate-100" />
          <div className="h-20 rounded-xl bg-slate-100" />
          <div className="h-20 rounded-xl bg-slate-100" />
        </div>
      </div>
    );
  }

  if (matchesError) {
    return (
      <div className="rounded-xl border border-rose-200 bg-rose-50 p-4">
        <p className="text-sm font-medium text-rose-800">
          {lang === 'fr' ? 'Erreur lors du chargement des correspondances.' :
           lang === 'en' ? 'Error loading matches.' :
           'Problem don happen for matches.'}
        </p>
        <button
          type="button"
          onClick={() => refetchMatches()}
          className="mt-2 rounded-full bg-rose-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-rose-600"
        >
          {lang === 'fr' ? 'Réessayer' : lang === 'en' ? 'Retry' : 'Try again'}
        </button>
      </div>
    );
  }

  if (proposals.length === 0 && !searching) {
    return (
      <div className="space-y-4 p-4">
        <p className="text-sm font-semibold text-slate-700">
          {lang === 'fr' ? '🔗 Correspondances' :
           lang === 'en' ? '🔗 Matches' :
           '🔗 Matches'}
        </p>
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
          <span className="text-2xl">🔎</span>
          <p className="mt-2 text-sm text-slate-500">
            {lang === 'fr' ? 'Aucune correspondance trouvée pour ce dossier.' :
             lang === 'en' ? 'No matches found for this dossier.' :
             'No get match for this dossier.'}
          </p>
          <p className="mt-1 text-xs text-slate-400">
            {lang === 'fr' ? 'Lancez une recherche pour découvrir des biens et professionnels pertinents.' :
             lang === 'en' ? 'Start a search to discover relevant properties and professionals.' :
             'Start search to find property and professionals wey fit you.'}
          </p>
          <button
            type="button"
            onClick={handleFindMatches}
            disabled={findMatchesMutation.isPending}
            className="mt-4 inline-flex items-center gap-2 rounded-full bg-slate-900 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
          >
            {findMatchesMutation.isPending
              ? (lang === 'fr' ? 'Recherche en cours...' : lang === 'en' ? 'Searching...' : 'Dey find...')
              : (lang === 'fr' ? '🔍 Lancer la recherche' : lang === 'en' ? '🔍 Start search' : '🔍 Find matches')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-700">
          {lang === 'fr' ? `🔗 Correspondances (${proposals.length})` :
           lang === 'en' ? `🔗 Matches (${proposals.length})` :
           `🔗 Matches (${proposals.length})`}
        </p>
        <button
          type="button"
          onClick={handleFindMatches}
          disabled={findMatchesMutation.isPending}
          className="rounded-full bg-slate-900 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
        >
          {findMatchesMutation.isPending
            ? (lang === 'fr' ? '...' : lang === 'en' ? '...' : '...')
            : (lang === 'fr' ? '🔄 Actualiser' : lang === 'en' ? '🔄 Refresh' : '🔄 Do again')}
        </button>
      </div>

      {/* Summary stats */}
      <div className="flex flex-wrap gap-2">
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
          {lang === 'fr' ? `${activeProposals.length} active(s)` :
           lang === 'en' ? `${activeProposals.length} active` :
           `${activeProposals.length} active`}
        </span>
        {inactiveCount > 0 && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
            {inactiveCount} {lang === 'fr' ? 'archivée(s)' : lang === 'en' ? 'archived' : 'done'}
          </span>
        )}
        {hasEstablishedRelations && (
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-800">
            ✅ {lang === 'fr' ? 'Relation établie' : lang === 'en' ? 'Connected' : 'Don connect'}
          </span>
        )}
      </div>

      {/* Proposals list */}
      <div className="space-y-3">
        {proposals.map((proposal) => {
          const grade = scoreGrade(proposal.score);
          const borderClass = statusColor(proposal.status);
          return (
            <div key={proposal.id} className={`rounded-xl border p-4 ${borderClass}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-slate-900">
                      {formatType(proposal.relation_type, lang)}
                    </span>
                    <span className={`rounded-full border px-2 py-0.5 text-xs font-medium ${grade.color}`}>
                      {proposal.score}% · {grade.label}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-slate-600">{proposal.justification}</p>
                  {proposal.target_type === 'property' && (
                    <p className="mt-1 text-xs text-slate-400">
                      {lang === 'fr' ? 'Bien #' : lang === 'en' ? 'Property #' : 'Property #'}{proposal.target_id}
                    </p>
                  )}
                  {proposal.target_type === 'partner' && (
                    <p className="mt-1 text-xs text-slate-400">
                      {lang === 'fr' ? 'Professionnel #' : lang === 'en' ? 'Partner #' : 'Partner #'}{proposal.target_id}
                    </p>
                  )}
                </div>
                <span className="shrink-0 rounded-full bg-white px-2.5 py-1 text-xs font-medium text-slate-500 shadow-sm">
                  {formatStatus(proposal.status, lang)}
                </span>
              </div>

              {/* Explanation */}
              {proposal.justification && (
                <div className="mt-3 rounded-lg bg-white/70 px-3 py-2">
                  <p className="text-xs font-medium text-slate-500">
                    {lang === 'fr' ? '💡 Pourquoi cette proposition ?' :
                     lang === 'en' ? '💡 Why this match?' :
                     '💡 Why dis one?'}
                  </p>
                  <p className="mt-0.5 text-xs text-slate-600">{proposal.justification}</p>
                </div>
              )}

              {/* Actions */}
              {(proposal.status === 'detected' || proposal.status === 'proposed' || proposal.status === 'consulted') && (
                <div className="mt-3 flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={() => acceptMutation.mutate(proposal.id)}
                    disabled={acceptMutation.isPending}
                    className="rounded-full bg-emerald-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-emerald-600 disabled:opacity-50"
                  >
                    {acceptMutation.isPending
                      ? '...'
                      : (lang === 'fr' ? '✅ Accepter' : lang === 'en' ? '✅ Accept' : '✅ Take am')}
                  </button>
                  <button
                    type="button"
                    onClick={() => rejectMutation.mutate(proposal.id)}
                    disabled={rejectMutation.isPending}
                    className="rounded-full border border-slate-300 bg-white px-4 py-1.5 text-xs font-semibold text-slate-600 transition hover:bg-slate-100 disabled:opacity-50"
                  >
                    {rejectMutation.isPending
                      ? '...'
                      : (lang === 'fr' ? '❌ Refuser' : lang === 'en' ? '❌ Reject' : '❌ No take')}
                  </button>
                </div>
              )}

              {/* Consent flow */}
              {proposal.status === 'accepted' && (
                <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50 p-3">
                  <p className="text-xs font-medium text-amber-800">
                    {lang === 'fr' ? '🔐 Consentement requis pour la mise en relation' :
                     lang === 'en' ? '🔐 Consent required for introduction' :
                     '🔐 We need your okay to connect you'}
                  </p>
                  <button
                    type="button"
                    onClick={() => consentMutation.mutate(proposal.id)}
                    disabled={consentMutation.isPending}
                    className="mt-2 rounded-full bg-amber-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-amber-600 disabled:opacity-50"
                  >
                    {consentMutation.isPending
                      ? '...'
                      : (lang === 'fr' ? '✅ Donner mon consentement' : lang === 'en' ? '✅ Give consent' : '✅ I agree')}
                  </button>
                </div>
              )}

              {/* Consent pending state (if already requested from backend) */}
              {proposal.status === 'consent_pending' && !consentMutation.isPending && (
                <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50 p-3">
                  <p className="text-xs font-medium text-amber-800">
                    {lang === 'fr' ? '🔐 Veuillez donner votre consentement pour finaliser la mise en relation' :
                     lang === 'en' ? '🔐 Please give your consent to finalize the introduction' :
                     '🔐 Make you give your okay make we connect you'}
                  </p>
                  <button
                    type="button"
                    onClick={() => consentMutation.mutate(proposal.id)}
                    disabled={consentMutation.isPending}
                    className="mt-2 rounded-full bg-amber-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-amber-600 disabled:opacity-50"
                  >
                    {lang === 'fr' ? '✅ Donner mon consentement' : lang === 'en' ? '✅ Give consent' : '✅ I agree'}
                  </button>
                </div>
              )}

              {/* Established relationship */}
              {proposal.status === 'relation_established' && (
                <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50 p-3">
                  <p className="text-xs font-medium text-emerald-800">
                    {lang === 'fr' ? '✅ Mise en relation effectuée' :
                     lang === 'en' ? '✅ Introduction completed' :
                     '✅ Don connect you'}
                  </p>
                </div>
              )}

              {/* Rejected state */}
              {proposal.status === 'rejected' && (
                <div className="mt-3 rounded-lg border border-slate-200 bg-slate-50 p-3">
                  <p className="text-xs text-slate-500">
                    {lang === 'fr' ? 'Proposition refusée.' :
                     lang === 'en' ? 'Proposal rejected.' :
                     'No take dis one.'}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Established relations summary */}
      {relations.length > 0 && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
          <p className="text-sm font-semibold text-emerald-800">
            {lang === 'fr' ? '✅ Relations établies' :
             lang === 'en' ? '✅ Established relations' :
             '✅ Don connect'}
          </p>
          <div className="mt-2 space-y-1">
            {relations.map((rel) => (
              <p key={rel.id} className="text-xs text-emerald-700">
                {formatType(rel.relation_type, lang)} · {formatStatus(rel.status, lang)}
                {rel.established_at ? ` · ${new Date(rel.established_at).toLocaleDateString()}` : ''}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ── Compact match summary for cockpits ── */

export function MatchSummaryWidget({ projectId, language: languageProp }: { projectId: number; language?: string }) {
  const { language: langFromCtx } = useLanguage();
  const lang = getLang(languageProp || langFromCtx);

  const { data: proposalsData, isLoading } = useQuery({
    queryKey: ['brain-proposals-summary', projectId],
    queryFn: () => apiSdk.brainProposals(projectId),
    enabled: !!projectId,
    staleTime: 30_000,
  });

  const proposals = proposalsData?.data ?? [];
  const accepted = proposals.filter((p) => p.status === 'accepted').length;
  const established = proposals.filter((p) => p.status === 'relation_established').length;
  const pending = proposals.filter((p) => !['rejected', 'accepted', 'relation_established', 'cancelled', 'expired'].includes(p.status)).length;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="h-4 w-32 animate-pulse rounded bg-slate-100" />
      </div>
    );
  }

  if (proposals.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <p className="text-xs font-semibold text-slate-400">
          {lang === 'fr' ? '🔗 Correspondances' : lang === 'en' ? '🔗 Matches' : '🔗 Matches'}
        </p>
        <p className="mt-1 text-xs text-slate-400">
          {lang === 'fr' ? 'Aucune correspondance' : lang === 'en' ? 'No matches' : 'No match'}
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold text-slate-400">
          {lang === 'fr' ? '🔗 Correspondances' : lang === 'en' ? '🔗 Matches' : '🔗 Matches'}
        </p>
        <span className="text-sm font-bold text-slate-900">{proposals.length}</span>
      </div>
      <div className="mt-2 flex flex-wrap gap-2">
        {pending > 0 && <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs text-amber-700">{pending} en attente</span>}
        {accepted > 0 && <span className="rounded-full bg-sky-100 px-2 py-0.5 text-xs text-sky-700">{accepted} accepté(s)</span>}
        {established > 0 && <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-700">{established} établi(s)</span>}
      </div>
    </div>
  );
}
