import { forwardRef } from 'react';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(({ label, className = '', ...props }, ref) => (
  <label className="flex flex-col gap-2 text-sm text-slate-300">
    {label ? <span>{label}</span> : null}
    <textarea
      ref={ref}
      className={`min-h-24 rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-brand-500 ${className}`}
      {...props}
    />
  </label>
));

Textarea.displayName = 'Textarea';
