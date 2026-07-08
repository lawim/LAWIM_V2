import type { HTMLAttributes } from 'react';
import { LAWIM_BRAND_SLOGAN } from '../brand';

export interface BrandMarkProps extends HTMLAttributes<HTMLDivElement> {
  tone?: 'dark' | 'light';
  slogan?: string;
}

export function BrandMark({ tone = 'dark', slogan = LAWIM_BRAND_SLOGAN, className = '', ...props }: BrandMarkProps) {
  const isLight = tone === 'light';

  return (
    <div className={`flex items-center gap-3 ${className}`.trim()} {...props}>
      <div className={`flex h-11 w-11 items-center justify-center overflow-hidden rounded-2xl ${isLight ? 'bg-white shadow-[0_16px_35px_rgba(15,23,42,0.12)]' : 'bg-slate-950/60 shadow-[0_16px_35px_rgba(216,180,106,0.24)]'}`}>
        <img src="/logo.svg" alt="LAWIM logo" className="h-full w-full object-cover" />
      </div>
      <div className="leading-tight">
        <div className={`text-sm font-semibold uppercase tracking-[0.34em] ${isLight ? 'text-slate-900' : 'text-white'}`}>LAWIM</div>
        <div className={`text-sm ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>{slogan}</div>
      </div>
    </div>
  );
}
