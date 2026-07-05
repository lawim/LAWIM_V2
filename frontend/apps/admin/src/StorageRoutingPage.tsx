import { Badge, Card, PageShell } from '@ui';
import { badgeVariantForStatus, storageRoutes, storageThresholds } from './storageRegistry';

export function StorageRoutingPage() {
  return (
    <PageShell
      eyebrow="Storage Routing"
      title="Storage routing policy"
      description="The Storage Orchestrator selects the first available resource on the official route for each content class."
    >
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card title="Routing matrix" description="Each path has a primary route and an overflow or fallback resource.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {storageRoutes.map((route) => (
              <div key={route.category} className="rounded-2xl border border-slate-800/80 bg-slate-950/70 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{route.label}</div>
                    <div className="mt-1 text-lg font-semibold text-white">{route.category}</div>
                  </div>
                  <Badge variant="info">{route.fallback}</Badge>
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  {route.route.map((drive) => (
                    <Badge key={drive} variant={badgeVariantForStatus(drive === 'Drive 9' ? 'ready' : 'watch')}>{drive}</Badge>
                  ))}
                </div>
                <div className="mt-3 text-xs text-slate-500">{route.description}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Routing rules" description="Selection remains ordered and mock-safe.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">Video: Drive 1, then Drive 2, then Drive 8.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Photo and audio: Drive 3, then Drive 8.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Conversation archive: Drive 5, then Drive 8.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Backup applicatif: Drive 7, then Drive 10.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Critical replication: Drive 8, then Drive 10.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Reserve and maintenance remain isolated on Drive 9 and Drive 10.</div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Card title="Threshold logic" description="The router uses the official quota bands to avoid blocked resources.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Normal</span>
              <Badge variant="success">0-70%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Attention</span>
              <Badge variant="info">70-85%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Slowdown</span>
              <Badge variant="warning">85-92%</Badge>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
              <span>Blocked</span>
              <Badge variant="warning">&gt;92%</Badge>
            </div>
          </div>
        </Card>
        <Card title="Operational note" description="The routing policy is ready for the secure assistant phase with real Google credentials.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-xl border border-slate-800 px-3 py-2">No Google Drive URLs are present in any business object.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">The Storage Orchestrator chooses the first available drive in the route.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 8 remains the overflow target, and Drive 10 remains the maintenance target.</div>
            <div className="rounded-xl border border-slate-800 px-3 py-2">Drive 9 is the strategic reserve.</div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
