import React from 'react';

interface AIConversationFooterProps {
  generatedByAI?: boolean;
  language?: 'fr' | 'en' | 'pcm';
  compact?: boolean;
  className?: string;
}

const FOOTER_TEXTS_FULL: Record<string, string> = {
  fr: "ℹ️ Réponse générée avec l'assistance de LAWIM AI. Comme toute IA, elle peut parfois se tromper. Vérifiez les informations importantes avant toute décision.",
  en: 'ℹ️ This response was generated with the assistance of LAWIM AI. Like any AI, it may sometimes make mistakes. Verify important information before making a decision.',
  pcm: 'ℹ️ LAWIM AI help generate this answer. Like any AI, e fit make mistake sometimes. Abeg check important information before you decide.',
};

const FOOTER_TEXTS_COMPACT: Record<string, string> = {
  fr: 'ℹ️ Assisté par LAWIM AI',
  en: 'ℹ️ Assisted by LAWIM AI',
  pcm: 'ℹ️ Message wey LAWIM AI help produce am',
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
