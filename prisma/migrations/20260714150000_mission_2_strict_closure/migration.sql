-- Mission 2 strict closure: remove remaining active schema references to legacy assistant sessions.

DO $$
BEGIN
    IF to_regclass('public.audit_ai_events') IS NOT NULL
       AND EXISTS (
           SELECT 1
           FROM information_schema.columns
           WHERE table_schema = 'public'
             AND table_name = 'audit_ai_events'
             AND column_name = 'assistant_session_id'
       ) THEN
        ALTER TABLE audit_ai_events DROP COLUMN assistant_session_id;
    END IF;
END $$;
