import React from 'react';

interface AIConversationFooterProps {
  generatedByAI?: boolean;
  language?: 'fr' | 'en' | 'pcm';
  compact?: boolean;
  className?: string;
}

const FOOTER_TEXTS_FULL: Record<string, string> = {
  fr: 'ℹ️ Réponse assistée par LAWIM AI.',
  en: 'ℹ️ Response assisted by LAWIM AI.',
  pcm: 'ℹ️ LAWIM AI help for this answer.',
};

const FOOTER_TEXTS_COMPACT: Record<string, string> = {
  fr: 'ℹ️ Assisté par LAWIM AI.',
  en: 'ℹ️ Assisted by LAWIM AI.',
  pcm: 'ℹ️ LAWIM AI help for this one.',
};

export function AIConversationFooter({
  generatedByAI = false,
  language = 'fr',
  compact = false,
  className = '',
}: AIConversationFooterProps) {
  if (!generatedByAI) return null;

  const texts = compact ? FOOTER_TEXTS_COMPACT : FOOTER_TEXTS_FULL;
  const text = texts[language] || texts.fr;

  return (
    <p
      role="note"
      aria-label="AI assistance notice"
      className={`mt-1 select-none text-[10px] leading-tight italic tracking-tight text-slate-400/70 dark:text-slate-500/60 ${className}`}
    >
      {text}
    </p>
  );
}
