import { cva, type VariantProps } from 'class-variance-authority';

const badgeStyles = cva('inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold', {
  variants: {
    variant: {
      default: 'bg-slate-800 text-slate-100',
      success: 'bg-emerald-500/15 text-emerald-400',
      warning: 'bg-amber-500/15 text-amber-400',
      info: 'bg-brand-500/15 text-brand-300'
    }
  },
  defaultVariants: {
    variant: 'default'
  }
});

export interface BadgeProps extends VariantProps<typeof badgeStyles> {
  children: React.ReactNode;
}

export function Badge({ children, variant }: BadgeProps) {
  return <span className={badgeStyles({ variant })}>{children}</span>;
}
