import type { ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const buttonStyles = cva(
  'inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 disabled:cursor-not-allowed disabled:opacity-60',
  {
    variants: {
      variant: {
        primary: 'bg-brand-600 text-white shadow-lg shadow-brand-600/20 hover:bg-brand-700 active:translate-y-px active:bg-brand-800 disabled:bg-brand-300 disabled:text-white/80',
        secondary: 'bg-slate-800 text-white hover:bg-slate-700 active:translate-y-px active:bg-slate-900 disabled:bg-slate-600'
      }
    },
    defaultVariants: {
      variant: 'primary'
    }
  }
);

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonStyles> {
  loading?: boolean;
}

export function Button({ className, variant, loading = false, disabled, children, ...props }: ButtonProps) {
  const isDisabled = Boolean(disabled || loading);
  return (
    <button
      aria-busy={loading || undefined}
      className={buttonStyles({ variant, className })}
      disabled={isDisabled}
      {...props}
    >
      {loading ? (
        <span className="inline-flex items-center gap-2">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-r-transparent" aria-hidden="true" />
          <span>{children}</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
}
