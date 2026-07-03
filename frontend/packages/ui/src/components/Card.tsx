import type { ReactNode } from 'react';

export interface CardProps {
  title: string;
  description: string;
  children?: ReactNode;
}

export function Card({ title, description, children }: CardProps) {
  return (
    <section className="rounded-3xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-[0_14px_40px_rgba(2,6,23,0.35)] backdrop-blur transition-transform duration-200 hover:-translate-y-1">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-400">{description}</p>
      {children ? <div className="mt-5">{children}</div> : null}
    </section>
  );
}
