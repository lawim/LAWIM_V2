import React from 'react';

interface AIConversationFooterProps {
  generatedByAI?: boolean;
  language?: 'fr' | 'en' | 'pcm';
  className?: string;
}

const FOOTER_TEXTS: Record<string, string> = {
  fr: 'ℹ️ Assisté par LAWIM AI',
  en: 'ℹ️ Assisted by LAWIM AI',
  pcm: 'ℹ️ Message wey LAWIM AI help produce am',
};

export function AIConversationFooter({
  generatedByAI = false,
  language = 'fr',
  className = '',
}: AIConversationFooterProps) {
  if (!generatedByAI) return null;

  const text = FOOTER_TEXTS[language] || FOOTER_TEXTS.fr;

  return (
    <p
      className={`mt-0.5 select-none text-[10px] leading-relaxed italic tracking-tight text-slate-400/70 dark:text-slate-500/60 ${className}`}
      aria-hidden="true"
    >
      {text}
    </p>
  );
}
