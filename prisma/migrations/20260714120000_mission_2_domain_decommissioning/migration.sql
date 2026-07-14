-- Mission 2: decommission Conversation/Qualification/Search/Matching/Relationship legacy runtime.
-- Git keeps deleted code history. This migration preserves independent data and creates maintenance intake.

CREATE TABLE IF NOT EXISTS maintenance_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    channel_identity_id INTEGER NULL,
    channel TEXT NOT NULL,
    raw_message TEXT NOT NULL,
    received_at TEXT NOT NULL,
    delivery_metadata_json TEXT NOT NULL DEFAULT '{}',
    maintenance_status TEXT NOT NULL DEFAULT 'received',
    handover_requested BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_maintenance_messages_channel
    ON maintenance_messages(channel, received_at);

CREATE INDEX IF NOT EXISTS idx_maintenance_messages_handover
    ON maintenance_messages(handover_requested, received_at);

DROP TABLE IF EXISTS brain_relation_proposals CASCADE;
DROP TABLE IF EXISTS brain_relations CASCADE;
DROP TABLE IF EXISTS brain_suggestions CASCADE;
DROP TABLE IF EXISTS brain_progression_state CASCADE;
DROP TABLE IF EXISTS brain_memory_items CASCADE;
DROP TABLE IF EXISTS brain_intents CASCADE;

DROP TABLE IF EXISTS assistant_agent_assignments CASCADE;
DROP TABLE IF EXISTS assistant_memory_summaries CASCADE;
DROP TABLE IF EXISTS assistant_turns CASCADE;
DROP TABLE IF EXISTS assistant_rag_retrievals CASCADE;
DROP TABLE IF EXISTS assistant_rag_chunks CASCADE;
DROP TABLE IF EXISTS assistant_rag_documents CASCADE;
DROP TABLE IF EXISTS assistant_context_snapshots CASCADE;
DROP TABLE IF EXISTS assistant_messages CASCADE;
DROP TABLE IF EXISTS assistant_sessions CASCADE;
DROP TABLE IF EXISTS assistant_prompt_versions CASCADE;
DROP TABLE IF EXISTS assistant_agents CASCADE;

DO $$
BEGIN
    IF to_regclass('public.project_match_results') IS NOT NULL THEN
        UPDATE project_match_results
        SET status = 'expired', updated_at = CURRENT_TIMESTAMP
        WHERE status = 'active';
    END IF;

    IF to_regclass('public.marketplace_matching_sessions') IS NOT NULL THEN
        UPDATE marketplace_matching_sessions
        SET status = 'decommissioned', completed_at = COALESCE(completed_at, CURRENT_TIMESTAMP)
        WHERE status IN ('pending', 'running', 'completed');
    END IF;
END $$;
