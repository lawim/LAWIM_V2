import { forwardRef } from 'react';

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(({ label, className = '', ...props }, ref) => (
  <label className="flex items-center gap-2 text-sm text-slate-300">
    <input ref={ref} type="checkbox" className={`h-4 w-4 rounded border-slate-700 bg-slate-900 ${className}`} {...props} />
    <span>{label}</span>
  </label>
));

Checkbox.displayName = 'Checkbox';
