import type { ReactNode } from 'react';
import { Badge } from './Badge';
import { Button } from './Button';

export interface PageShellProps {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: ReactNode;
  children: ReactNode;
}

export function PageShell({ eyebrow, title, description, actions, children }: PageShellProps) {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.2),_transparent_35%),linear-gradient(135deg,_#020617_0%,_#0f172a_100%)] px-4 py-8 text-slate-100 sm:px-6 lg:px-8 lg:py-12">
      <section className="mx-auto flex max-w-6xl flex-col gap-8">
        <div className="flex flex-col gap-5 rounded-3xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-[0_20px_80px_rgba(2,6,23,0.45)] backdrop-blur sm:p-8 lg:flex-row lg:items-end lg:justify-between">
          <div className="space-y-3">
            {eyebrow ? <Badge variant="info">{eyebrow}</Badge> : null}
            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{title}</h1>
            <p className="max-w-2xl text-base leading-7 text-slate-400">{description}</p>
          </div>
          {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
        </div>
        <div className="space-y-6">{children}</div>
      </section>
    </main>
  );
}
