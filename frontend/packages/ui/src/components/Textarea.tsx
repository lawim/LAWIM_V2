import { forwardRef } from 'react';
import { twMerge } from 'tailwind-merge';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  tone?: 'dark' | 'light';
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(({ label, tone = 'dark', className = '', ...props }, ref) => (
  <label className="flex flex-col gap-2 text-sm text-slate-300">
    {label ? <span>{label}</span> : null}
    <textarea
      ref={ref}
      className={twMerge(`min-h-24 rounded-xl border px-3 py-2 text-sm outline-none transition focus:border-brand-500 ${
        tone === 'light'
          ? 'border-slate-200 bg-white text-slate-900 placeholder:text-slate-400'
          : 'border-slate-700 bg-slate-900/70 text-slate-100 placeholder:text-slate-500'
      }`, className)}
      {...props}
    />
  </label>
));

Textarea.displayName = 'Textarea';
