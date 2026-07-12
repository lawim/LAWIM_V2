import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiSdk } from '@api-sdk';
import { Badge, Button, Card, Input, PageShell } from '@ui';
import { useAuthStore } from '@auth';

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
      return 'success';
    case 'PENDING':
    case 'PROCESSING':
    case 'ISSUED':
    case 'APPROVED':
    case 'CALCULATED':
      return 'info';
    case 'FAILED':
    case 'CANCELLED':
    case 'EXPIRED':
    case 'CONFLICT':
      return 'warning';
    default:
      return 'default';
  }
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
      <div className="text-xs uppercase tracking-[0.22em] text-slate-500">{label}</div>
      <div className="mt-2 text-xl font-semibold text-white">{value}</div>
    </div>
  );
}

function PaymentPanel({
  invoiceId,
  defaultAmount,
  defaultCurrency,
}: {
  invoiceId?: number | null;
  defaultAmount?: number | null;
  defaultCurrency?: string | null;
}) {
  const [targetInvoiceId, setTargetInvoiceId] = useState(String(invoiceId ?? ''));
  const [phoneNumber, setPhoneNumber] = useState('+237677000111');
  const [message, setMessage] = useState<string | null>(null);
  const [latestIntentId, setLatestIntentId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const submitPayment = async () => {
    const parsedInvoiceId = Number(targetInvoiceId || invoiceId || 0);
    if (!Number.isFinite(parsedInvoiceId) || parsedInvoiceId <= 0) {
      setMessage('Sélectionnez une facture valide.');
      return;
    }
    setLoading(true);
    setMessage(null);
    try {
      const response = await apiSdk.createPaymentIntent({
        invoice_id: parsedInvoiceId,
        amount_minor: defaultAmount ?? undefined,
        currency: defaultCurrency ?? 'XAF',
        provider_code: 'CAMPAY',
        channel: 'mobile_money',
        phone_number_e164: phoneNumber,
        initiate: true,
        idempotency_key: `financial-${parsedInvoiceId}-${phoneNumber}`,
      });
      const intent = response.data;
      setLatestIntentId(intent?.id ?? null);
      const status = String(intent?.status ?? 'PENDING');
      setMessage(`${intent?.number ?? 'Payment intent'}: ${status}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Impossible de créer l’intention de paiement.');
    } finally {
      setLoading(false);
    }
  };

  const refreshStatus = async () => {
    if (!latestIntentId) return;
    setLoading(true);
    try {
      const response = await apiSdk.getPaymentStatus(latestIntentId);
      const payload = response.data as Record<string, unknown>;
      const intent = payload.payment_intent as Record<string, unknown> | undefined;
      const provider = payload.provider_status as Record<string, unknown> | undefined;
      setMessage(`${String(intent?.number ?? 'Payment')} → ${String(intent?.status ?? 'UNKNOWN')} / ${String(provider?.status ?? 'UNKNOWN')}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Impossible de vérifier le statut.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Paiement Mobile Money" description="Initier un paiement Campay à partir d’une facture payable.">
      <div className="grid gap-4">
        <Input
          label="Invoice ID"
          value={targetInvoiceId}
          onChange={(event) => setTargetInvoiceId(event.target.value)}
          placeholder={invoiceId ? String(invoiceId) : '1'}
        />
        <Input
          label="Numéro Mobile Money"
          value={phoneNumber}
          onChange={(event) => setPhoneNumber(event.target.value)}
          placeholder="+237677000111"
        />
        <div className="flex flex-wrap gap-3">
          <Button loading={loading} onClick={() => void submitPayment()}>
            Initier le paiement
          </Button>
          <Button variant="secondary" onClick={() => void refreshStatus()} disabled={!latestIntentId || loading}>
            Vérifier le statut
          </Button>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
          {message ?? 'Aucune initiation en cours.'}
        </div>
      </div>
    </Card>
  );
}

export function FinancialHubPage() {
  const user = useAuthStore((state) => state.user);
  const invoicesQuery = useQuery({ queryKey: ['financial', 'invoices'], queryFn: () => apiSdk.listInvoices({ limit: 8 }) });
  const receiptsQuery = useQuery({ queryKey: ['financial', 'receipts'], queryFn: () => apiSdk.listReceipts({ limit: 8 }) });
  const intentsQuery = useQuery({ queryKey: ['financial', 'payment-intents'], queryFn: () => apiSdk.listPaymentIntents({ limit: 8 }) });
  const subscriptionsQuery = useQuery({ queryKey: ['financial', 'subscriptions'], queryFn: () => apiSdk.listSubscriptions({ limit: 8 }) });
  const commissionsQuery = useQuery({ queryKey: ['financial', 'commissions'], queryFn: () => apiSdk.listOwnCommissions({ limit: 8 }) });
  const payoutsQuery = useQuery({ queryKey: ['financial', 'payouts'], queryFn: () => apiSdk.listOwnPayouts({ limit: 8 }) });

  const invoices = invoicesQuery.data?.data ?? [];
  const receipts = receiptsQuery.data?.data ?? [];
  const intents = intentsQuery.data?.data ?? [];
  const subscriptions = subscriptionsQuery.data?.data ?? [];
  const commissions = commissionsQuery.data?.data ?? [];
  const payouts = payoutsQuery.data?.data ?? [];

  const selectedInvoice = useMemo(() => invoices[0] ?? null, [invoices]);

  return (
    <PageShell
      eyebrow="Financial Core"
      title="Financial Hub"
      description="Consultez les factures, paiements, reçus et abonnements liés à votre compte."
      actions={<Button variant="secondary" onClick={() => void invoicesQuery.refetch()}>Rafraîchir</Button>}
    >
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <Card
            title={`Résumé financier ${user?.name ? `de ${user.name}` : ''}`.trim()}
            description="Vue rapide des documents et opérations financières."
          >
            <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              <MiniStat label="Factures" value={String(invoices.length)} />
              <MiniStat label="Paiements" value={String(intents.length)} />
              <MiniStat label="Reçus" value={String(receipts.length)} />
              <MiniStat label="Abonnements" value={String(subscriptions.length)} />
            </div>
          </Card>

          <Card title="Factures" description="Les montants proviennent du Financial Core.">
            <div className="grid gap-3">
              {invoices.length === 0 ? (
                <p className="text-sm text-slate-400">Aucune facture disponible.</p>
              ) : invoices.map((invoice) => (
                <div key={invoice.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="font-semibold text-white">{invoice.number}</div>
                      <div className="text-sm text-slate-400">Solde {formatMoney(invoice.balance_minor, invoice.currency)}</div>
                    </div>
                    <Badge variant={statusTone(invoice.status) as never}>{invoice.status}</Badge>
                  </div>
                  <div className="mt-3 text-sm text-slate-300">
                    Total {formatMoney(invoice.total_minor, invoice.currency)} · Payé {formatMoney(invoice.amount_paid_minor, invoice.currency)}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Paiements et reçus" description="Suivi des intentions, confirmations et documents générés.">
            <div className="grid gap-3 lg:grid-cols-2">
              <div className="space-y-3">
                <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Intentions</h3>
                {intents.length === 0 ? <p className="text-sm text-slate-400">Aucune intention.</p> : intents.map((intent) => (
                  <div key={intent.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <div className="font-semibold text-white">{intent.number}</div>
                      <Badge variant={statusTone(intent.status) as never}>{intent.status}</Badge>
                    </div>
                    <div className="mt-2 text-sm text-slate-400">{formatMoney(intent.amount_minor, intent.currency)}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Reçus</h3>
                {receipts.length === 0 ? <p className="text-sm text-slate-400">Aucun reçu.</p> : receipts.map((receipt) => (
                  <div key={receipt.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <div className="font-semibold text-white">{receipt.number}</div>
                      <Badge variant={statusTone(receipt.status) as never}>{receipt.status}</Badge>
                    </div>
                    <div className="mt-2 text-sm text-slate-400">{formatMoney(receipt.amount_minor, receipt.currency)}</div>
                  </div>
                ))}
              </div>
            </div>
          </Card>

          <Card title="Abonnements, commissions et reversements" description="Surveillez les cycles récurrents et la rémunération.">
            <div className="grid gap-4 lg:grid-cols-3">
              <div className="space-y-2">
                <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Abonnements</h3>
                {subscriptions.length === 0 ? <p className="text-sm text-slate-400">Aucun abonnement.</p> : subscriptions.map((subscription) => (
                  <div key={subscription.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-sm text-slate-300">
                    <div className="flex items-center justify-between gap-3">
                      <span>{String(subscription.id)}</span>
                      <Badge variant={statusTone(subscription.status) as never}>{subscription.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
              <div className="space-y-2">
                <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Commissions</h3>
                {commissions.length === 0 ? <p className="text-sm text-slate-400">Aucune commission.</p> : commissions.map((commission) => (
                  <div key={commission.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-sm text-slate-300">
                    <div className="flex items-center justify-between gap-3">
                      <span>{formatMoney(commission.amount_minor, commission.currency)}</span>
                      <Badge variant={statusTone(commission.status) as never}>{commission.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
              <div className="space-y-2">
                <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Reversements</h3>
                {payouts.length === 0 ? <p className="text-sm text-slate-400">Aucun reversement.</p> : payouts.map((payout) => (
                  <div key={payout.id} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-sm text-slate-300">
                    <div className="flex items-center justify-between gap-3">
                      <span>{formatMoney(payout.amount_minor, payout.currency)}</span>
                      <Badge variant={statusTone(payout.status) as never}>{payout.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <PaymentPanel
            invoiceId={selectedInvoice?.id ?? null}
            defaultAmount={selectedInvoice?.balance_minor ?? selectedInvoice?.total_minor ?? null}
            defaultCurrency={selectedInvoice?.currency ?? 'XAF'}
          />

          <Card title="Facture sélectionnée" description="La première facture disponible sert de référence rapide.">
            {selectedInvoice ? (
              <div className="space-y-2 text-sm text-slate-300">
                <div className="font-semibold text-white">{selectedInvoice.number}</div>
                <div>Status: {selectedInvoice.status}</div>
                <div>Total: {formatMoney(selectedInvoice.total_minor, selectedInvoice.currency)}</div>
                <div>Solde: {formatMoney(selectedInvoice.balance_minor, selectedInvoice.currency)}</div>
              </div>
            ) : (
              <p className="text-sm text-slate-400">Aucune facture sélectionnée.</p>
            )}
          </Card>
        </div>
      </div>
    </PageShell>
  );
}
