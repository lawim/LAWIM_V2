import { forwardRef } from 'react';
import { twMerge } from 'tailwind-merge';

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  tone?: 'dark' | 'light';
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(({ label, tone = 'dark', className = '', children, ...props }, ref) => (
  <label className="flex flex-col gap-2 text-sm text-slate-300">
    {label ? <span>{label}</span> : null}
    <select
      ref={ref}
      className={twMerge(`rounded-xl border px-3 py-2 text-sm outline-none transition focus:border-brand-500 ${
        tone === 'light'
          ? 'border-slate-200 bg-white text-slate-900'
          : 'border-slate-700 bg-slate-900/70 text-slate-100'
      }`, className)}
      {...props}
    >
      {children}
    </select>
  </label>
));

Select.displayName = 'Select';
