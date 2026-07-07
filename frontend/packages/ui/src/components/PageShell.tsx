import type { ReactNode } from 'react';
import { Badge } from './Badge';
import { Button } from './Button';
import { BrandMark } from './BrandMark';

export interface PageShellProps {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: ReactNode;
  children: ReactNode;
}

export function PageShell({ eyebrow, title, description, actions, children }: PageShellProps) {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.24),_transparent_34%),radial-gradient(circle_at_85%_15%,_rgba(16,185,129,0.14),_transparent_24%),linear-gradient(135deg,_#020617_0%,_#0f172a_58%,_#111827_100%)] px-4 py-8 text-slate-100 sm:px-6 lg:px-8 lg:py-12">
      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:48px_48px] opacity-20" />
      <section className="mx-auto flex max-w-6xl flex-col gap-8">
        <div className="relative z-10 flex flex-col gap-5 rounded-[2rem] border border-white/10 bg-slate-950/70 p-6 shadow-[0_28px_120px_rgba(2,6,23,0.5)] backdrop-blur-xl sm:p-8 lg:flex-row lg:items-end lg:justify-between">
          <div className="space-y-4">
            <BrandMark slogan="LAWIM · accompagnement immobilier intelligent" />
            <div className="flex flex-wrap items-center gap-3">
              {eyebrow ? <Badge variant="info">{eyebrow}</Badge> : null}
              <span className="text-xs uppercase tracking-[0.28em] text-slate-400">LAWIM</span>
            </div>
            <h1 className="max-w-3xl text-3xl font-semibold tracking-tight text-white sm:text-4xl">{title}</h1>
            <p className="max-w-2xl text-base leading-7 text-slate-300">{description}</p>
          </div>
          {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
        </div>
        <div className="relative z-10 space-y-6">{children}</div>
      </section>
    </main>
  );
}
