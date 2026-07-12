import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { Badge, Button, Card, Input, PageShell, Textarea } from '@ui';

function formatMoney(value?: number | null, currency = 'XAF') {
  if (value == null) return '—';
  return `${new Intl.NumberFormat('fr-FR').format(value)} ${currency}`;
}

function statusTone(status?: string | null) {
  switch (String(status ?? '').toUpperCase()) {
    case 'PAID':
    case 'SUCCEEDED':
    case 'SUCCESSFUL':
    case 'ACTIVE':
    case 'GENERATED':
    case 'RESOLVED':
    case 'APPROVED':
    case 'VALIDATED':
      return 'success';
    case 'PENDING':
    case 'PROCESSING':
    case 'ISSUED':
    case 'CALCULATED':
      return 'info';
    case 'FAILED':
    case 'CANCELLED':
    case 'EXPIRED':
    case 'CONFLICT':
    case 'REJECTED':
      return 'warning';
    default:
      return 'default';
  }
}

function ProviderHealthCard() {
  const healthQuery = useQuery({ queryKey: ['admin', 'financial', 'provider-health'], queryFn: () => apiSdk.adminGetProviderHealth() });
  const provider = healthQuery.data?.data;

  return (
    <Card title="Campay provider health" description="État opérationnel du connecteur de paiement.">
      {provider ? (
        <div className="space-y-3 text-sm text-slate-300">
          <div className="flex items-center justify-between gap-3">
            <strong className="text-white">{provider.name}</strong>
            <Badge variant={statusTone(provider.status) as never}>{provider.status}</Badge>
          </div>
          <div>Environment: {provider.environment}</div>
          <div>Available: {provider.available ? 'yes' : 'no'}</div>
          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-xs text-slate-400">
            {JSON.stringify(provider.details, null, 2)}
          </div>
        </div>
      ) : (
        <p className="text-sm text-slate-400">Aucune donnée de santé.</p>
      )}
    </Card>
  );
}

function ReconciliationCard() {
  const conflictsQuery = useQuery({ queryKey: ['admin', 'financial', 'reconciliation'], queryFn: () => apiSdk.adminListReconciliationConflicts({ limit: 8 }) });
  const [conflictId, setConflictId] = useState('');
  const [note, setNote] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const conflicts = conflictsQuery.data?.data ?? [];

  const firstConflictId = useMemo(() => conflicts[0]?.id ?? null, [conflicts]);

  const resolveConflict = async () => {
    const id = Number(conflictId || firstConflictId || 0);
    if (!Number.isFinite(id) || id <= 0) {
      setMessage('Sélectionnez un conflit de rapprochement valide.');
      return;
    }
    setLoading(true);
    try {
      const response = await apiSdk.adminResolveReconciliation(id, {
        status: 'RESOLVED',
        resolution_note: note || 'Reviewed from admin cockpit',
      });
      setMessage(`Résolution enregistrée: ${String(response.data.status ?? 'RESOLVED')}`);
      await conflictsQuery.refetch();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Impossible de résoudre le conflit.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Rapprochement" description="Gérez les conflits, preuves et écarts de statut.">
      <div className="grid gap-4">
        <div className="space-y-3">
          {conflicts.length === 0 ? (
            <p className="text-sm text-slate-400">Aucun conflit ouvert.</p>
          ) : conflicts.map((conflict) => (
            <div key={conflict.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <div className="font-semibold text-white">Conflict #{conflict.id}</div>
                  <div className="text-sm text-slate-400">{conflict.conflict_type}</div>
                </div>
                <Badge variant={statusTone(conflict.status) as never}>{conflict.status}</Badge>
              </div>
              <div className="mt-2 text-sm text-slate-300">Currency: {conflict.currency}</div>
            </div>
          ))}
        </div>
        <Input label="Conflict ID" value={conflictId} onChange={(event) => setConflictId(event.target.value)} placeholder={firstConflictId ? String(firstConflictId) : '1'} />
        <Textarea label="Resolution note" value={note} onChange={(event) => setNote(event.target.value)} placeholder="Explain the manual resolution" />
        <div className="flex flex-wrap gap-3">
          <Button loading={loading} onClick={() => void resolveConflict()}>
            Resolve conflict
          </Button>
          <Button variant="secondary" onClick={() => void conflictsQuery.refetch()}>Refresh</Button>
        </div>
        {message ? <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-sm text-slate-300">{message}</div> : null}
      </div>
    </Card>
  );
}

function PaymentsCard() {
  const paymentsQuery = useQuery({ queryKey: ['admin', 'financial', 'payments'], queryFn: () => apiSdk.adminListPayments({ limit: 8 }) });
  const payments = paymentsQuery.data?.data ?? [];

  return (
    <Card title="Paiements" description="Surveillez les intentions, statuts et réceptions des fonds.">
      <div className="space-y-3">
        {payments.length === 0 ? (
          <p className="text-sm text-slate-400">Aucun paiement.</p>
        ) : payments.map((payment) => (
          <div key={payment.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="font-semibold text-white">{payment.number}</div>
                <div className="text-sm text-slate-400">{formatMoney(payment.amount_minor, payment.currency)}</div>
              </div>
              <Badge variant={statusTone(payment.status) as never}>{payment.status}</Badge>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

function FinancialSummaryCard() {
  const paymentsQuery = useQuery({ queryKey: ['admin', 'financial', 'payments-count'], queryFn: () => apiSdk.adminListPayments({ limit: 50 }) });
  const refundsQuery = useQuery({ queryKey: ['admin', 'financial', 'refunds'], queryFn: () => apiSdk.adminListRefunds({ limit: 8 }) });
  const commissionsQuery = useQuery({ queryKey: ['admin', 'financial', 'commissions'], queryFn: () => apiSdk.adminListCommissions({ limit: 8 }) });
  const eventsQuery = useQuery({ queryKey: ['admin', 'financial', 'provider-events'], queryFn: () => apiSdk.adminListProviderEvents({ limit: 8 }) });

  return (
    <Card title="Financial summary" description="Indicateurs de supervision et d’administration financière.">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="text-xs uppercase tracking-[0.22em] text-slate-500">Payments</div>
          <div className="mt-2 text-xl font-semibold text-white">{paymentsQuery.data?.data.length ?? 0}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="text-xs uppercase tracking-[0.22em] text-slate-500">Refunds</div>
          <div className="mt-2 text-xl font-semibold text-white">{refundsQuery.data?.data.length ?? 0}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="text-xs uppercase tracking-[0.22em] text-slate-500">Commissions</div>
          <div className="mt-2 text-xl font-semibold text-white">{commissionsQuery.data?.data.length ?? 0}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="text-xs uppercase tracking-[0.22em] text-slate-500">Provider events</div>
          <div className="mt-2 text-xl font-semibold text-white">{eventsQuery.data?.data.length ?? 0}</div>
        </div>
      </div>
    </Card>
  );
}

export function FinancialOperationsPage() {
  return (
    <PageShell
      eyebrow="Administration financière"
      title="Financial Operations"
      description="Pilotage des paiements, remboursements, commissions, reversements et rapprochement."
    >
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <FinancialSummaryCard />
          <PaymentsCard />
          <ReconciliationCard />
        </div>
        <div className="space-y-6">
          <ProviderHealthCard />
        </div>
      </div>
    </PageShell>
  );
}
