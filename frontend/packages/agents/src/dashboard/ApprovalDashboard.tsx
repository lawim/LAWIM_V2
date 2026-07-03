import { Badge, Card } from '@ui';
import { ApprovalStatus, type ApprovalQueue } from '../core';

export interface ApprovalDashboardProps {
  approvals: ApprovalQueue;
}

function statusVariant(status: ApprovalStatus) {
  switch (status) {
    case ApprovalStatus.Approved:
      return 'success';
    case ApprovalStatus.Pending:
      return 'warning';
    case ApprovalStatus.Rejected:
    case ApprovalStatus.Revoked:
    case ApprovalStatus.Expired:
      return 'warning';
    default:
      return 'default';
  }
}

export function ApprovalDashboard({ approvals }: ApprovalDashboardProps) {
  const summary = approvals.summary();
  const pending = approvals.pending();
  const notifications = approvals.notifications().slice(-4);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
      <Card title="Approval Queue" description="Sensitive actions wait here until the Brain authorizes them.">
        <div className="mt-4 grid gap-3">
          {pending.length === 0 ? <p className="text-sm text-slate-400">No pending approvals.</p> : null}
          {pending.map((request) => (
            <div key={request.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="font-medium text-white">{request.title}</p>
                  <p className="text-xs text-slate-400">{request.description}</p>
                </div>
                <Badge variant={statusVariant(request.status)}>{request.status}</Badge>
              </div>
              <p className="mt-3 text-xs text-slate-500">Reference: {request.referenceId}</p>
            </div>
          ))}
        </div>
      </Card>
      <div className="grid gap-6">
        <Card title="Approval Summary" description="Queue overview and status split.">
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Total</div>
              <div className="mt-1 text-lg font-semibold text-white">{summary.total}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Pending</div>
              <div className="mt-1 text-lg font-semibold text-amber-300">{summary.pending}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Approved</div>
              <div className="mt-1 text-lg font-semibold text-emerald-300">{summary.approved}</div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
              <div className="text-slate-500">Rejected</div>
              <div className="mt-1 text-lg font-semibold text-slate-100">{summary.rejected}</div>
            </div>
          </div>
        </Card>
        <Card title="Approval Notifications" description="Recent notifications emitted by the approval queue.">
          <div className="mt-4 space-y-3">
            {notifications.length === 0 ? <p className="text-sm text-slate-400">No approval notifications yet.</p> : null}
            {notifications.map((notification) => (
              <div key={notification.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
                <div className="flex items-center justify-between gap-3">
                  <span>{notification.message}</span>
                  <Badge variant="info">{notification.channel}</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
