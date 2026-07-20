import React from 'react';

interface AIConversationFooterProps {
  generatedByAI?: boolean;
  language?: 'fr' | 'en' | 'pcm';
  compact?: boolean;
  className?: string;
}

const FOOTER_TEXTS_FULL: Record<string, string> = {
  fr: 'ℹ️ LAWIM AI peut se tromper. Vérifiez les informations importantes.',
  en: 'ℹ️ LAWIM AI may err. Verify important information.',
  pcm: 'ℹ️ LAWIM AI fit make mistake. Check important information.',
};

const FOOTER_TEXTS_COMPACT: Record<string, string> = {
  fr: 'ℹ️ LAWIM AI peut se tromper.',
  en: 'ℹ️ LAWIM AI may err.',
  pcm: 'ℹ️ LAWIM AI fit make mistake.',
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
