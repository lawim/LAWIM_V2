import type { ReactNode } from 'react';

export interface CardProps {
  title: string;
  description: string;
  children?: ReactNode;
}

export function Card({ title, description, children }: CardProps) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <p className="mt-2 text-sm text-slate-400">{description}</p>
      {children ? <div className="mt-4">{children}</div> : null}
    </section>
  );
}
