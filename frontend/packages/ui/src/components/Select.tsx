import { forwardRef } from 'react';

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(({ label, className = '', children, ...props }, ref) => (
  <label className="flex flex-col gap-2 text-sm text-slate-300">
    {label ? <span>{label}</span> : null}
    <select
      ref={ref}
      className={`rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-brand-500 ${className}`}
      {...props}
    >
      {children}
    </select>
  </label>
));

Select.displayName = 'Select';
