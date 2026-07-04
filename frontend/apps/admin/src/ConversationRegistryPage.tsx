import { Badge, Card, PageShell } from '@ui';

export function ConversationRegistryPage() {
  return (
    <PageShell
      eyebrow="Conversation Registry"
      title="Conversation registry and archive index"
      description="Inspect deduplicated conversations, participants, and archive status."
    >
      <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card title="Registry overview" description="Conversations are stored once and linked through participants and media IDs.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="rounded-lg border border-slate-800 px-3 py-2">ConversationID is the canonical record key.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Participants are linked to the conversation without duplication.</div>
            <div className="rounded-lg border border-slate-800 px-3 py-2">Attachments reference MediaID, not direct Google Drive URLs.</div>
          </div>
        </Card>
        <Card title="Active status" description="Audit and lifecycle information for the conversation registry.">
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Active conversations</span><Badge variant="success">Healthy</Badge></div>
            <div className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2"><span>Archived conversations</span><Badge variant="info">Drive 8</Badge></div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
