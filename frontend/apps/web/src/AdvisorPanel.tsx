import { useCallback, useEffect, useRef, useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiSdk, type BrainDossier, type BrainChatResult, type BrainResumption, type BrainSuggestion, type BrainProposalResult, type ProjectSummary } from '@api-sdk';
import { useLanguage } from '@ui';
import { MatchResultsPanel, MatchSummaryWidget } from './MatchResultsPanel';

/* ── Types ──────────────────────────────────── */

type Lang = 'fr' | 'en' | 'pcm';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  text: string;
  suggestions?: BrainSuggestion[];
  confirmation?: boolean;
}

interface AdvisorPanelProps {
  userId?: string;
  userName?: string;
  roleLabel?: string;
  onNavigate?: (path: string) => void;
}

/* ── Helpers ──────────────────────────────────── */

const GREETINGS: Record<Lang, string> = {
  fr: 'Bonjour ! Je suis votre Conseiller LAWIM. Comment puis-je vous accompagner dans votre projet immobilier ?',
  en: 'Hello! I am your LAWIM Advisor. How can I help you with your real estate project?',
  pcm: 'Hello! I be your LAWIM Advisor. How I fit help you for your property matter?',
};

const RESUME_CTA: Record<Lang, { continue: string; edit: string; view: string; new: string }> = {
  fr: { continue: '▶️ Continuer', edit: '✏️ Modifier', view: '📁 Voir le dossier', new: '🆕 Nouveau projet' },
  en: { continue: '▶️ Continue', edit: '✏️ Edit', view: '📁 View dossier', new: '🆕 New project' },
  pcm: { continue: '▶️ Continue', edit: '✏️ Change', view: '📁 See dossier', new: '🆕 New project' },
};

const DOSSIER_CREATION_QUESTIONS: Record<Lang, string> = {
  fr: '💬 Quel est votre projet immobilier aujourd’hui ?',
  en: '💬 What is your real estate project today?',
  pcm: '💬 Wetin you want do for property today?',
};

function getLang(language: string): Lang {
  if (language === 'en' || language === 'pcm') return language;
  return 'fr';
}

function getFirstName(name?: string): string {
  if (!name) return '';
  return name.split(/\s+/).filter(Boolean)[0] ?? '';
}

/* ── Sub-components ──────────────────────────── */

function SuggestionChip({ suggestion, onAction, lang }: {
  suggestion: BrainSuggestion;
  onAction: (text: string, action?: string) => void;
  lang: Lang;
}) {
  const icon = suggestion.partner ? '🤝' : suggestion.type === 'action' ? '✨' : '💡';
  return (
    <button
      type="button"
      onClick={() => onAction(suggestion.content, suggestion.action)}
      className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600 shadow-sm transition hover:border-slate-300 hover:bg-slate-50"
    >
      <span>{icon}</span>
      <span>{suggestion.content}</span>
    </button>
  );
}

function ConfirmBanner({ text, onYes, onNo, onEdit, lang }: {
  text: string;
  onYes: () => void;
  onNo: () => void;
  onEdit: () => void;
  lang: Lang;
}) {
  const labels: Record<Lang, { yes: string; no: string; edit: string }> = {
    fr: { yes: '✅ Oui', no: '❌ Non', edit: '✏️ Modifier' },
    en: { yes: '✅ Yes', no: '❌ No', edit: '✏️ Edit' },
    pcm: { yes: '✅ Na so', no: '❌ No be', edit: '✏️ Change' },
  };
  const l = labels[lang];
  return (
    <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
      <p className="text-sm text-amber-900">{text}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        <button type="button" onClick={onYes} className="rounded-full bg-emerald-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-emerald-600">{l.yes}</button>
        <button type="button" onClick={onEdit} className="rounded-full bg-sky-500 px-4 py-1.5 text-xs font-semibold text-white transition hover:bg-sky-600">{l.edit}</button>
        <button type="button" onClick={onNo} className="rounded-full border border-slate-300 bg-white px-4 py-1.5 text-xs font-semibold text-slate-600 transition hover:bg-slate-100">{l.no}</button>
      </div>
    </div>
  );
}

/* ── Dossier Selector ─────────────────────────── */

function DossierSelector({ dossiers, onSelect, onNew, lang, loading }: {
  dossiers: BrainDossier[];
  onSelect: (d: BrainDossier) => void;
  onNew: () => void;
  lang: Lang;
  loading: boolean;
}) {
  const title: Record<Lang, string> = {
    fr: '📁 Vos dossiers',
    en: '📁 Your dossiers',
    pcm: '📁 Your dossiers',
  };
  const newBtn: Record<Lang, string> = {
    fr: '➕ Nouveau projet',
    en: '➕ New project',
    pcm: '➕ New project',
  };

  if (loading) {
    return (
      <div className="space-y-3 p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title[lang]}</p>
        <div className="animate-pulse space-y-2">
          <div className="h-16 rounded-xl bg-slate-100" />
          <div className="h-16 rounded-xl bg-slate-100" />
        </div>
      </div>
    );
  }

  const projectIcon = (type?: string) => {
    if (type === 'land' || type === 'find_land') return '🌍';
    if (type === 'build' || type === 'construction') return '🏗️';
    if (type === 'rent' || type === 'location') return '🔑';
    if (type === 'sell' || type === 'vente') return '📢';
    if (type === 'invest') return '💰';
    return '🏠';
  };

  return (
    <div className="space-y-3 p-4">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title[lang]}</p>
      {dossiers.length === 0 ? (
        <p className="text-sm text-slate-500 italic">
          {lang === 'fr' ? 'Aucun dossier pour le moment.' : lang === 'en' ? 'No dossiers yet.' : 'No get dossier.'}
        </p>
      ) : (
        <div className="space-y-2">
          {dossiers.map((d) => (
            <button
              key={d.project.id}
              type="button"
              onClick={() => onSelect(d)}
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-left text-sm transition hover:border-slate-300 hover:shadow-sm"
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">{projectIcon(d.project.project_type)}</span>
                <div className="min-w-0 flex-1">
                  <p className="truncate font-semibold text-slate-900">{d.project.title || d.project.objective}</p>
                  <p className="truncate text-xs text-slate-500">
                    {d.project.location_city ? `📍 ${d.project.location_city}` : ''}
                    {d.project.budget_max ? ` · 💰 ${Intl.NumberFormat('fr-FR').format(d.project.budget_max)} FCFA` : ''}
                  </p>
                </div>
                {d.resume.has_history && <span className="shrink-0 text-xs text-emerald-500">🔄</span>}
              </div>
              {d.resume.has_history && d.resume.short_summary && (
                <p className="mt-1 line-clamp-1 text-xs text-slate-400">{d.resume.short_summary}</p>
              )}
            </button>
          ))}
        </div>
      )}
      <button
        type="button"
        onClick={onNew}
        className="flex w-full items-center justify-center gap-2 rounded-xl border border-dashed border-slate-300 py-3 text-sm font-medium text-slate-500 transition hover:border-slate-400 hover:text-slate-700"
      >
        {newBtn[lang]}
      </button>
    </div>
  );
}

/* ── Main AdvisorPanel ─────────────────────────── */

export function AdvisorPanel({ userName, roleLabel, onNavigate }: AdvisorPanelProps) {
  const { language } = useLanguage();
  const lang = getLang(language);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  // Dossier state
  const [activeDossier, setActiveDossier] = useState<ProjectSummary | null>(null);
  const [activeResume, setActiveResume] = useState<BrainResumption | null>(null);
  const [showDossierSelector, setShowDossierSelector] = useState(true);
  const [isNewDossier, setIsNewDossier] = useState(false);
  const [pendingConfirmation, setPendingConfirmation] = useState<string | null>(null);

  const [showMatchPanel, setShowMatchPanel] = useState(false);
  const [hasProposals, setHasProposals] = useState(false);

  const { data: dossiersData, isLoading: dossiersLoading } = useQuery({
    queryKey: ['brain-dossiers'],
    queryFn: () => apiSdk.brainDossiers(),
    staleTime: 30_000,
  });
  const dossiers = dossiersData?.data ?? [];

  const chatMutation = useMutation({
    mutationFn: (payload: { message: string; projectId: number; sessionId?: number }) =>
      apiSdk.brainChat({
        message: payload.message,
        project_id: payload.projectId,
        language,
        channel: 'web',
      }),
  });

  // Pre-fetch proposals to check if any exist
  const projectIdNum = activeDossier?.id;
  const { data: proposalCheck } = useQuery({
    queryKey: ['brain-proposals-check', projectIdNum],
    queryFn: () => apiSdk.brainProposals(projectIdNum!),
    enabled: !!projectIdNum,
    staleTime: 10_000,
  });
  const proposalsForCheck = proposalCheck?.data ?? [];
  const hasAnyProposals = proposalsForCheck.length > 0;

  const resumeQuery = (projectId: number) =>
    useQuery({
      queryKey: ['brain-resume', projectId],
      queryFn: () => apiSdk.brainResume(projectId, language),
      enabled: !!projectId,
    });

  const scrollBottom = () => {
    setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
  };

  useEffect(scrollBottom, [messages]);

  const addAssistantMessage = useCallback((text: string, suggestions?: BrainSuggestion[], confirmation?: boolean) => {
    setMessages((prev) => [...prev, {
      id: `a-${Date.now()}`,
      role: 'assistant',
      text,
      suggestions,
      confirmation,
    }]);
  }, []);

  const handleSelectDossier = useCallback((dossier: BrainDossier) => {
    setActiveDossier(dossier.project);
    setActiveResume(dossier.resume);
    setShowDossierSelector(false);
    setIsNewDossier(false);
    setMessages([]);
    setPendingConfirmation(null);

    if (dossier.resume.has_history) {
      addAssistantMessage(dossier.resume.summary);
      if (dossier.resume.next_question) {
        addAssistantMessage(`💡 ${dossier.resume.next_question}`);
      }
    } else {
      addAssistantMessage(GREETINGS[lang]);
    }
  }, [addAssistantMessage, lang]);

  const handleNewDossier = useCallback(() => {
    setActiveDossier(null);
    setActiveResume(null);
    setShowDossierSelector(false);
    setIsNewDossier(true);
    setMessages([{
      id: 'start',
      role: 'assistant',
      text: DOSSIER_CREATION_QUESTIONS[lang],
    }]);
    setPendingConfirmation(null);
  }, [lang]);

  const handleSend = useCallback(async (text?: string) => {
    const message = (text || input).trim();
    if (!message || sending) return;
    setInput('');
    setSending(true);

    setMessages((prev) => [...prev, { id: `u-${Date.now()}`, role: 'user', text: message }]);
    setPendingConfirmation(null);

    // Check for confirmation responses
    if (pendingConfirmation && message.length < 50) {
      const lower = message.toLowerCase();
      const isYes = ['oui', 'yes', 'yeah', 'yep', 'na so', 'true', 'ok', 'd\'accord', 'correct'].some((w) => lower.includes(w));
      if (isYes) {
        addAssistantMessage('✅ Confirmation enregistrée.');
        setPendingConfirmation(null);
        setSending(false);
        return;
      }
    }

    try {
      if (!activeDossier && !isNewDossier) {
        // Need a project - create one or offer selection
        addAssistantMessage(GREETINGS[lang]);
        setShowDossierSelector(true);
        setSending(false);
        return;
      }

      const projectId = activeDossier?.id;
      if (!projectId) {
        // Create a project from this message, then send
        addAssistantMessage(
          lang === 'fr' ? 'Je crée un dossier pour votre projet...' :
          lang === 'en' ? 'Creating a dossier for your project...' :
          'I dey create dossier for your project...'
        );
        // The project creation would happen via apiSdk.brainCreateDossier
        // For now, inform the user
        addAssistantMessage(
          lang === 'fr' ? '📁 Pour commencer, décrivez votre projet en quelques mots.' :
          lang === 'en' ? '📁 To start, describe your project in a few words.' :
          '📁 To start, tell me your project small.'
        );
        setSending(false);
        return;
      }

      const response = await chatMutation.mutateAsync({ message, projectId });
      const result = response.data;

      // Build response text
      const parts: string[] = [];
      const analysis = result.analysis;
      const progression = result.progression;

      // Next question
      if (progression.next_question) {
        parts.push(progression.next_question);
      } else if (progression.complete) {
        parts.push(
          lang === 'fr' ? '✅ J\'ai toutes les informations nécessaires. Que souhaitez-vous faire ensuite ?' :
          lang === 'en' ? '✅ I have all the necessary information. What would you like to do next?' :
          '✅ I don get all the info. Wetin you want do next?'
        );
      } else if (analysis.primary_intent === 'other') {
        parts.push(
          lang === 'fr' ? '💬 Pouvez-vous me décrire votre projet plus en détail ?' :
          lang === 'en' ? '💬 Can you describe your project in more detail?' :
          '💬 You fit tell me your project small?'
        );
      }

      const responseText = parts.join('\n\n');
      const suggestions = result.suggestions || [];

      // Check if progression is complete -> suggest matching
      if (progression.complete && !hasAnyProposals) {
        suggestions.push({
          type: 'action',
          content: lang === 'fr' ? '🔍 Rechercher des correspondances' :
                    lang === 'en' ? '🔍 Find matches' :
                    '🔍 Find matches',
          action: 'find_matches',
          priority: 'high',
          priority_order: 5,
        });
      }

      if (responseText) {
        addAssistantMessage(responseText, suggestions.length > 0 ? suggestions : undefined);
      } else {
        addAssistantMessage(
          lang === 'fr' ? '👍 Compris ! Continuez lorsque vous êtes prêt.' :
          lang === 'en' ? '👍 Got it! Continue when you\'re ready.' :
          '👍 I don hear! Continue when you ready.'
        );
      }
    } catch {
      addAssistantMessage(
        lang === 'fr' ? '⚠️ Désolé, une erreur est survenue. Veuillez réessayer.' :
        lang === 'en' ? '⚠️ Sorry, an error occurred. Please try again.' :
        '⚠️ Sorry, problem don happen. Try again.'
      );
    }
    setSending(false);
  }, [input, sending, pendingConfirmation, activeDossier, isNewDossier, chatMutation, addAssistantMessage, lang]);

  const handleSuggestionAction = useCallback((text: string, suggestionAction?: string) => {
    if (suggestionAction === 'find_matches') {
      setShowMatchPanel(true);
      return;
    }
    setInput(text);
    handleSend(text);
  }, [handleSend]);

  const handleBackToDossiers = useCallback(() => {
    setShowDossierSelector(true);
    setActiveDossier(null);
    setActiveResume(null);
    setIsNewDossier(false);
    setMessages([]);
  }, []);

  // If showing dossier selector
  if (showDossierSelector) {
    return (
      <div className="flex flex-col">
        <div className="border-b border-slate-200 px-4 py-3">
          <p className="text-sm font-semibold text-slate-900">
            {userName ? `Bonjour ${getFirstName(userName)} 👋` : '👋 Conseiller LAWIM'}
          </p>
          {roleLabel && <p className="mt-0.5 text-xs text-slate-500">{roleLabel}</p>}
        </div>
        <DossierSelector
          dossiers={dossiers}
          onSelect={handleSelectDossier}
          onNew={handleNewDossier}
          lang={lang}
          loading={dossiersLoading}
        />
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-slate-200 px-4 py-3">
        <button
          type="button"
          onClick={handleBackToDossiers}
          className="flex h-8 w-8 items-center justify-center rounded-full text-slate-400 transition hover:bg-slate-100 hover:text-slate-600"
          title={lang === 'fr' ? 'Retour aux dossiers' : 'Back to dossiers'}
        >
          ←
        </button>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-slate-900">
            {activeDossier?.title || (isNewDossier ? '📋 Nouveau projet' : '💬 Conseiller LAWIM')}
          </p>
          {activeResume?.short_summary && (
            <p className="truncate text-xs text-slate-400">{activeResume.short_summary}</p>
          )}
        </div>
      </div>

      {/* Match results toggle */}
      {projectIdNum && hasAnyProposals && !showMatchPanel && (
        <div className="border-b border-slate-100 px-4 py-2">
          <button
            type="button"
            onClick={() => setShowMatchPanel(true)}
            className="flex w-full items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2.5 text-sm transition hover:bg-emerald-100"
          >
            <span className="font-medium text-emerald-800">
              {lang === 'fr' ? `🔗 ${proposalsForCheck.length} correspondance(s) trouvée(s)` :
               lang === 'en' ? `🔗 ${proposalsForCheck.length} match(es) found` :
               `🔗 ${proposalsForCheck.length} match(es) found`}
            </span>
            <span className="text-emerald-600">→</span>
          </button>
        </div>
      )}

      {/* Match Results Panel */}
      {showMatchPanel && projectIdNum && (
        <div className="border-b border-slate-200">
          <div className="flex items-center justify-between px-4 py-2">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              {lang === 'fr' ? '🔗 Correspondances' : lang === 'en' ? '🔗 Matches' : '🔗 Matches'}
            </p>
            <button
              type="button"
              onClick={() => setShowMatchPanel(false)}
              className="text-xs text-slate-400 hover:text-slate-600"
            >
              {lang === 'fr' ? 'Masquer' : lang === 'en' ? 'Hide' : 'Hide'}
            </button>
          </div>
          <MatchResultsPanel projectId={projectIdNum} />
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4" style={{ maxHeight: '50vh' }}>
        {messages.length === 0 && (
          <div className="flex items-center justify-center py-8 text-sm text-slate-400">
            {lang === 'fr' ? 'Commencez la conversation...' : lang === 'en' ? 'Start the conversation...' : 'Start conversation...'}
          </div>
        )}
        {messages.map((msg) => (
          <div key={msg.id}>
            {msg.role === 'system' ? (
              <div className="rounded-xl bg-slate-100 px-4 py-2 text-center text-xs text-slate-500">
                {msg.text}
              </div>
            ) : (
              <div className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-slate-900 text-white'
                    : 'border border-slate-200 bg-white text-slate-700'
                }`}>
                  {msg.text.split('\n\n').map((paragraph, i) => (
                    <p key={i} className={i > 0 ? 'mt-2' : ''}>{paragraph}</p>
                  ))}
                </div>
              </div>
            )}
            {/* Suggestions */}
            {msg.suggestions && msg.suggestions.length > 0 && (
              <div className="ml-2 mt-2 flex flex-wrap gap-2">
                {msg.suggestions.map((s, i) => (
                  <SuggestionChip key={i} suggestion={s} onAction={handleSuggestionAction} lang={lang} />
                ))}
              </div>
            )}
            {/* Confirmation banner */}
            {msg.confirmation && (
              <div className="ml-2 mt-2">
                <ConfirmBanner
                  text={pendingConfirmation || 'Confirmez-vous cette information ?'}
                  onYes={() => handleSend('Oui')}
                  onNo={() => handleSend('Non')}
                  onEdit={() => setInput(
                    lang === 'fr' ? 'Corrigeons : ' :
                    lang === 'en' ? 'Let me correct: ' :
                    'Make I correct: '
                  )}
                  lang={lang}
                />
              </div>
            )}
          </div>
        ))}
        {sending && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-3">
              <div className="flex gap-1">
                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" style={{ animationDelay: '0ms' }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" style={{ animationDelay: '150ms' }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-slate-200 px-4 py-3">
        <div className="flex gap-2">
          <input
            className="min-w-0 flex-1 rounded-full border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm outline-none transition focus:border-slate-300 focus:bg-white"
            placeholder={
              lang === 'fr' ? 'Votre message...' :
              lang === 'en' ? 'Your message...' :
              'Your message...'
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
            disabled={sending}
          />
          <button
            type="button"
            onClick={() => handleSend()}
            disabled={sending || !input.trim()}
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-900 text-white transition hover:bg-slate-800 disabled:opacity-50"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Compact Advisor Widget for Cockpits ─────────── */

export function AdvisorWidget({ onOpenConversation }: { onOpenConversation?: () => void }) {
  const { language } = useLanguage();
  const lang = getLang(language);

  const { data: dossiersData, isLoading } = useQuery({
    queryKey: ['brain-dossiers-widget'],
    queryFn: () => apiSdk.brainDossiers(),
    staleTime: 30_000,
  });
  const dossiers = dossiersData?.data ?? [];
  const active = dossiers.find((d) => d.resume.has_history);

  const greetings: Record<Lang, string> = {
    fr: 'Votre Conseiller LAWIM',
    en: 'Your LAWIM Advisor',
    pcm: 'Your LAWIM Advisor',
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 text-lg text-white">💬</span>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold text-slate-900">{greetings[lang]}</p>
          <p className="text-xs text-slate-500">
            {isLoading
              ? '...'
              : active
                ? (lang === 'fr' ? '📁 Dossier en cours' : lang === 'en' ? '📁 Active dossier' : '📁 Dossier dey')
                : (lang === 'fr' ? 'Aucun dossier actif' : lang === 'en' ? 'No active dossier' : 'No get dossier')}
          </p>
        </div>
        <button
          type="button"
          onClick={onOpenConversation}
          className="rounded-full bg-slate-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-slate-800"
        >
          {lang === 'fr' ? '💬 Parler' : lang === 'en' ? '💬 Chat' : '💬 Talk'}
        </button>
      </div>
      {active && active.resume.short_summary && (
        <p className="mt-3 line-clamp-2 text-xs text-slate-500">{active.resume.short_summary}</p>
      )}
    </div>
  );
}
