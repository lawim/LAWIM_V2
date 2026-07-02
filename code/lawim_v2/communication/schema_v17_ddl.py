"""Schema v17 DDL — Communication platform (RELEASE PROGRAM K)."""

V17_TABLE_NAMES: tuple[str, ...] = (
    "communication_messages",
    "communication_threads",
    "communication_channels",
    "communication_recipients",
    "communication_groups",
    "communication_events",
    "communication_logs",
    "communication_history",
    "communication_archives",
    "communication_metadata",
    "notification_events",
    "notification_rules",
    "notification_templates",
    "notification_preferences",
    "notification_deliveries",
    "notification_batches",
    "notification_acknowledgements",
    "notification_failures",
    "notification_statistics",
    "notification_queue",
    "email_accounts",
    "email_templates",
    "email_messages",
    "email_attachments",
    "email_threads",
    "email_delivery_logs",
    "email_statistics",
    "email_bounces",
    "email_click_tracking",
    "email_open_tracking",
    "sms_templates",
    "sms_messages",
    "sms_delivery_logs",
    "sms_statistics",
    "sms_providers",
    "sms_queue",
    "whatsapp_accounts",
    "whatsapp_templates",
    "whatsapp_messages",
    "whatsapp_media",
    "whatsapp_sessions",
    "whatsapp_delivery_logs",
    "whatsapp_statistics",
    "telegram_bots",
    "telegram_messages",
    "telegram_updates",
    "telegram_statistics",
    "push_devices",
    "push_notifications",
    "push_delivery_logs",
    "push_subscriptions",
    "push_statistics",
    "inapp_notifications",
    "inapp_categories",
    "inapp_read_status",
    "inapp_statistics",
    "campaigns",
    "campaign_channels",
    "campaign_audiences",
    "campaign_segments",
    "campaign_executions",
    "campaign_statistics",
    "campaign_results",
    "campaign_logs",
    "queue_jobs",
    "queue_workers",
    "queue_failures",
    "queue_retry_history",
    "queue_batches",
    "template_categories",
    "template_versions",
    "template_variables",
    "template_translations",
    "communication_preferences",
    "communication_consent_history",
    "communication_blacklists",
    "communication_whitelists",
    "communication_quiet_hours",
    "communication_dashboard_snapshots",
    "communication_analytics",
    "communication_ai_recommendations",
)

SQLITE_V17_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS communication_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_key TEXT NOT NULL UNIQUE,
    thread_id INTEGER,
    channel_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    direction TEXT NOT NULL DEFAULT 'outbound',
    priority TEXT NOT NULL DEFAULT 'normal',
    status TEXT NOT NULL DEFAULT 'draft',
    sender_user_id INTEGER,
    recipient_user_id INTEGER,
    contact_id INTEGER,
    organization_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    sent_at TEXT,
    expires_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES communication_threads(id) ON DELETE SET NULL,
    FOREIGN KEY (channel_id) REFERENCES communication_channels(id) ON DELETE SET NULL,
    FOREIGN KEY (sender_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (recipient_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_messages_status ON communication_messages(status, created_at);
CREATE INDEX IF NOT EXISTS idx_communication_messages_channel ON communication_messages(channel_type, status);
CREATE TABLE IF NOT EXISTS communication_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_key TEXT NOT NULL UNIQUE,
    channel_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',
    organization_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES communication_channels(id) ON DELETE SET NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_threads_status ON communication_threads(status, created_at);
CREATE TABLE IF NOT EXISTS communication_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_key TEXT NOT NULL UNIQUE,
    channel_type TEXT NOT NULL DEFAULT 'email',
    name TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    config_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_channels_status ON communication_channels(status, created_at);
CREATE TABLE IF NOT EXISTS communication_recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    recipient_type TEXT NOT NULL DEFAULT 'user',
    user_id INTEGER,
    contact_id INTEGER,
    address TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_recipients_status ON communication_recipients(status, created_at);
CREATE TABLE IF NOT EXISTS communication_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    organization_id INTEGER,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_groups_status ON communication_groups(status, created_at);
CREATE TABLE IF NOT EXISTS communication_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    event_kind TEXT NOT NULL DEFAULT 'system',
    source_program TEXT NOT NULL DEFAULT 'platform',
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_events_status ON communication_events(status, created_at);
CREATE TABLE IF NOT EXISTS communication_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_logs_status ON communication_logs(status, created_at);
CREATE TABLE IF NOT EXISTS communication_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    action TEXT NOT NULL DEFAULT '',
    actor_user_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_history_status ON communication_history(status, created_at);
CREATE TABLE IF NOT EXISTS communication_archives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    archive_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    archived_at TEXT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_communication_archives_status ON communication_archives(status, created_at);
CREATE TABLE IF NOT EXISTS communication_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metadata_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    resource_type TEXT NOT NULL DEFAULT 'message',
    resource_id INTEGER NOT NULL DEFAULT 0,
    meta_key TEXT NOT NULL DEFAULT '',
    meta_value_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_metadata_status ON communication_metadata(status, created_at);
CREATE TABLE IF NOT EXISTS notification_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_type TEXT NOT NULL DEFAULT 'system',
    user_id INTEGER,
    contact_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    priority TEXT NOT NULL DEFAULT 'normal',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_notification_events_status ON notification_events(status, created_at);
CREATE TABLE IF NOT EXISTS notification_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    event_kind TEXT NOT NULL DEFAULT 'system',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    rules_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notification_rules_status ON notification_rules(status, created_at);
CREATE TABLE IF NOT EXISTS notification_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notification_templates_status ON notification_templates(status, created_at);
CREATE TABLE IF NOT EXISTS notification_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notification_preferences_status ON notification_preferences(status, created_at);
CREATE TABLE IF NOT EXISTS notification_deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    delivered_at TEXT,
    FOREIGN KEY (notification_event_id) REFERENCES notification_events(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notification_deliveries_status ON notification_deliveries(status, created_at);
CREATE TABLE IF NOT EXISTS notification_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_notification_batches_status ON notification_batches(status, created_at);
CREATE TABLE IF NOT EXISTS notification_acknowledgements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ack_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    user_id INTEGER,
    acknowledged_at TEXT NOT NULL,
    FOREIGN KEY (notification_event_id) REFERENCES notification_events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notification_acknowledgements_status ON notification_acknowledgements(status, created_at);
CREATE TABLE IF NOT EXISTS notification_failures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    FOREIGN KEY (notification_event_id) REFERENCES notification_events(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notification_failures_status ON notification_failures(status, created_at);
CREATE TABLE IF NOT EXISTS notification_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notification_statistics_status ON notification_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS notification_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    FOREIGN KEY (notification_event_id) REFERENCES notification_events(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notification_queue_status ON notification_queue(status, created_at);
CREATE TABLE IF NOT EXISTS email_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    organization_id INTEGER,
    email_address TEXT NOT NULL DEFAULT '',
    display_name TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_email_accounts_status ON email_accounts(status, created_at);
CREATE TABLE IF NOT EXISTS email_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body_html TEXT NOT NULL DEFAULT '',
    body_text TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_templates_status ON email_templates(status, created_at);
CREATE TABLE IF NOT EXISTS email_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_email TEXT NOT NULL DEFAULT '',
    from_email TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    email_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    FOREIGN KEY (account_id) REFERENCES email_accounts(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_email_messages_status ON email_messages(status, created_at);
CREATE TABLE IF NOT EXISTS email_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attachment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    filename TEXT NOT NULL DEFAULT '',
    content_type TEXT NOT NULL DEFAULT 'application/octet-stream',
    size_bytes INTEGER NOT NULL DEFAULT 0,
    storage_ref TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (email_message_id) REFERENCES email_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_email_attachments_status ON email_attachments(status, created_at);
CREATE TABLE IF NOT EXISTS email_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT '',
    thread_status TEXT NOT NULL DEFAULT 'open',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_threads_status ON email_threads(status, created_at);
CREATE TABLE IF NOT EXISTS email_delivery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    FOREIGN KEY (email_message_id) REFERENCES email_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_email_delivery_logs_status ON email_delivery_logs(status, created_at);
CREATE TABLE IF NOT EXISTS email_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_statistics_status ON email_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS email_bounces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bounce_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    bounce_type TEXT NOT NULL DEFAULT 'hard',
    reason TEXT NOT NULL DEFAULT '',
    bounced_at TEXT NOT NULL,
    FOREIGN KEY (email_message_id) REFERENCES email_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_email_bounces_status ON email_bounces(status, created_at);
CREATE TABLE IF NOT EXISTS email_click_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    click_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    link_url TEXT NOT NULL DEFAULT '',
    clicked_at TEXT NOT NULL,
    FOREIGN KEY (email_message_id) REFERENCES email_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_email_click_tracking_status ON email_click_tracking(status, created_at);
CREATE TABLE IF NOT EXISTS email_open_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    open_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    opened_at TEXT NOT NULL,
    FOREIGN KEY (email_message_id) REFERENCES email_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_email_open_tracking_status ON email_open_tracking(status, created_at);
CREATE TABLE IF NOT EXISTS sms_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sms_templates_status ON sms_templates(status, created_at);
CREATE TABLE IF NOT EXISTS sms_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    provider_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    from_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    sms_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    FOREIGN KEY (provider_id) REFERENCES sms_providers(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_sms_messages_status ON sms_messages(status, created_at);
CREATE TABLE IF NOT EXISTS sms_delivery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    FOREIGN KEY (sms_message_id) REFERENCES sms_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_sms_delivery_logs_status ON sms_delivery_logs(status, created_at);
CREATE TABLE IF NOT EXISTS sms_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sms_statistics_status ON sms_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS sms_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    provider_type TEXT NOT NULL DEFAULT 'twilio',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sms_providers_status ON sms_providers(status, created_at);
CREATE TABLE IF NOT EXISTS sms_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    FOREIGN KEY (sms_message_id) REFERENCES sms_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_sms_queue_status ON sms_queue(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    handle TEXT NOT NULL DEFAULT '@lawimofficial',
    phone_e164 TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT 'meta_cloud',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_accounts_status ON whatsapp_accounts(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    template_name TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT 'fr',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_templates_status ON whatsapp_templates(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    whatsapp_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    FOREIGN KEY (account_id) REFERENCES whatsapp_accounts(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_messages_status ON whatsapp_messages(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    media_type TEXT NOT NULL DEFAULT 'document',
    filename TEXT NOT NULL DEFAULT '',
    storage_ref TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (whatsapp_message_id) REFERENCES whatsapp_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_media_status ON whatsapp_media(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    contact_id INTEGER,
    session_status TEXT NOT NULL DEFAULT 'open',
    opened_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_status ON whatsapp_sessions(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_delivery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    FOREIGN KEY (whatsapp_message_id) REFERENCES whatsapp_messages(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_delivery_logs_status ON whatsapp_delivery_logs(status, created_at);
CREATE TABLE IF NOT EXISTS whatsapp_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_statistics_status ON whatsapp_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS telegram_bots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_handle TEXT NOT NULL DEFAULT '@lawim_assistant_bot',
    bot_token_ref TEXT NOT NULL DEFAULT '',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_telegram_bots_status ON telegram_bots(status, created_at);
CREATE TABLE IF NOT EXISTS telegram_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    message_id INTEGER,
    chat_id TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    telegram_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    FOREIGN KEY (bot_id) REFERENCES telegram_bots(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_telegram_messages_status ON telegram_messages(status, created_at);
CREATE TABLE IF NOT EXISTS telegram_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    update_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    update_type TEXT NOT NULL DEFAULT 'message',
    payload_json TEXT NOT NULL DEFAULT '{}',
    received_at TEXT NOT NULL,
    FOREIGN KEY (bot_id) REFERENCES telegram_bots(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_telegram_updates_status ON telegram_updates(status, created_at);
CREATE TABLE IF NOT EXISTS telegram_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_telegram_statistics_status ON telegram_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS push_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    platform TEXT NOT NULL DEFAULT 'web',
    device_token TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_push_devices_status ON push_devices(status, created_at);
CREATE TABLE IF NOT EXISTS push_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    device_id INTEGER,
    message_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    push_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    FOREIGN KEY (device_id) REFERENCES push_devices(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES communication_messages(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_push_notifications_status ON push_notifications(status, created_at);
CREATE TABLE IF NOT EXISTS push_delivery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    push_notification_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    FOREIGN KEY (push_notification_id) REFERENCES push_notifications(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_push_delivery_logs_status ON push_delivery_logs(status, created_at);
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    topic TEXT NOT NULL DEFAULT '',
    subscription_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_status ON push_subscriptions(status, created_at);
CREATE TABLE IF NOT EXISTS push_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_push_statistics_status ON push_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS inapp_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    category_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    action_json TEXT NOT NULL DEFAULT '{}',
    read_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES inapp_categories(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_inapp_notifications_status ON inapp_notifications(status, created_at);
CREATE TABLE IF NOT EXISTS inapp_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_inapp_categories_status ON inapp_categories(status, created_at);
CREATE TABLE IF NOT EXISTS inapp_read_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    read_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_id INTEGER,
    user_id INTEGER,
    read_at TEXT NOT NULL,
    FOREIGN KEY (notification_id) REFERENCES inapp_notifications(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_inapp_read_status_status ON inapp_read_status(status, created_at);
CREATE TABLE IF NOT EXISTS inapp_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_inapp_statistics_status ON inapp_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    campaign_type TEXT NOT NULL DEFAULT 'multichannel',
    organization_id INTEGER,
    campaign_status TEXT NOT NULL DEFAULT 'draft',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    config_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_channels_status ON campaign_channels(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_audiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audience_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    audience_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_audiences_status ON campaign_audiences(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    criteria_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_segments_status ON campaign_segments(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    execution_status TEXT NOT NULL DEFAULT 'pending',
    started_at TEXT,
    completed_at TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_executions_status ON campaign_executions(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_statistics_status ON campaign_statistics(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    result_type TEXT NOT NULL DEFAULT 'summary',
    result_json TEXT NOT NULL DEFAULT '{}',
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_results_status ON campaign_results(status, created_at);
CREATE TABLE IF NOT EXISTS campaign_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_campaign_logs_status ON campaign_logs(status, created_at);
CREATE TABLE IF NOT EXISTS queue_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_type TEXT NOT NULL DEFAULT 'send_message',
    channel_type TEXT NOT NULL DEFAULT 'email',
    priority TEXT NOT NULL DEFAULT 'normal',
    job_status TEXT NOT NULL DEFAULT 'pending',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3
);
CREATE INDEX IF NOT EXISTS idx_queue_jobs_status ON queue_jobs(status, created_at);
CREATE TABLE IF NOT EXISTS queue_workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    worker_name TEXT NOT NULL DEFAULT '',
    worker_status TEXT NOT NULL DEFAULT 'idle',
    last_heartbeat_at TEXT,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_queue_workers_status ON queue_workers(status, created_at);
CREATE TABLE IF NOT EXISTS queue_failures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES queue_jobs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_queue_failures_status ON queue_failures(status, created_at);
CREATE TABLE IF NOT EXISTS queue_retry_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    retry_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    retry_at TEXT NOT NULL,
    result TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (job_id) REFERENCES queue_jobs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_queue_retry_history_status ON queue_retry_history(status, created_at);
CREATE TABLE IF NOT EXISTS queue_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    job_count INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_queue_batches_status ON queue_batches(status, created_at);
CREATE TABLE IF NOT EXISTS template_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_template_categories_status ON template_categories(status, created_at);
CREATE TABLE IF NOT EXISTS template_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    category_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    version_number INTEGER NOT NULL DEFAULT 1,
    content_json TEXT NOT NULL DEFAULT '{}',
    published_at TEXT,
    FOREIGN KEY (category_id) REFERENCES template_categories(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_template_versions_status ON template_versions(status, created_at);
CREATE TABLE IF NOT EXISTS template_variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variable_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    variable_name TEXT NOT NULL DEFAULT '',
    default_value TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (template_version_id) REFERENCES template_versions(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_template_variables_status ON template_variables(status, created_at);
CREATE TABLE IF NOT EXISTS template_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    locale TEXT NOT NULL DEFAULT 'fr',
    content_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (template_version_id) REFERENCES template_versions(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_template_translations_status ON template_translations(status, created_at);
CREATE TABLE IF NOT EXISTS communication_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_communication_preferences_status ON communication_preferences(status, created_at);
CREATE TABLE IF NOT EXISTS communication_consent_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consent_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    consent_type TEXT NOT NULL DEFAULT 'marketing',
    consent_status TEXT NOT NULL DEFAULT 'granted',
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_consent_history_status ON communication_consent_history(status, created_at);
CREATE TABLE IF NOT EXISTS communication_blacklists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blacklist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    blocked_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_blacklists_status ON communication_blacklists(status, created_at);
CREATE TABLE IF NOT EXISTS communication_whitelists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    whitelist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    allowed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_whitelists_status ON communication_whitelists(status, created_at);
CREATE TABLE IF NOT EXISTS communication_quiet_hours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiet_hours_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    timezone TEXT NOT NULL DEFAULT 'Africa/Douala',
    start_time TEXT NOT NULL DEFAULT '22:00',
    end_time TEXT NOT NULL DEFAULT '07:00',
    days_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_communication_quiet_hours_status ON communication_quiet_hours(status, created_at);
CREATE TABLE IF NOT EXISTS communication_dashboard_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    snapshot_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_dashboard_snapshots_status ON communication_dashboard_snapshots(status, created_at);
CREATE TABLE IF NOT EXISTS communication_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analytics_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    period TEXT NOT NULL DEFAULT 'daily',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_analytics_status ON communication_analytics(status, created_at);
CREATE TABLE IF NOT EXISTS communication_ai_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    recommendation_type TEXT NOT NULL DEFAULT 'followup',
    recommendation_json TEXT NOT NULL DEFAULT '{}',
    score REAL NOT NULL DEFAULT 0,
    generated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_communication_ai_recommendations_status ON communication_ai_recommendations(status, created_at);
"""

POSTGRESQL_V17_STATEMENTS: tuple[str, ...] = (
    """
CREATE TABLE IF NOT EXISTS communication_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    thread_id INTEGER,
    channel_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    direction TEXT NOT NULL DEFAULT 'outbound',
    priority TEXT NOT NULL DEFAULT 'normal',
    status TEXT NOT NULL DEFAULT 'draft',
    sender_user_id INTEGER,
    recipient_user_id INTEGER,
    contact_id INTEGER,
    organization_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    sent_at TEXT,
    expires_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    thread_id INTEGER REFERENCES communication_threads(id) ON DELETE SET NULL,
    channel_id INTEGER REFERENCES communication_channels(id) ON DELETE SET NULL,
    sender_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    recipient_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_messages_status ON communication_messages(status, created_at)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_messages_channel ON communication_messages(channel_type, status)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_threads (
    id SERIAL PRIMARY KEY,
    thread_key TEXT NOT NULL UNIQUE,
    channel_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',
    organization_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    channel_id INTEGER REFERENCES communication_channels(id) ON DELETE SET NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_threads_status ON communication_threads(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_channels (
    id SERIAL PRIMARY KEY,
    channel_key TEXT NOT NULL UNIQUE,
    channel_type TEXT NOT NULL DEFAULT 'email',
    name TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    config_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_channels_status ON communication_channels(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_recipients (
    id SERIAL PRIMARY KEY,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    recipient_type TEXT NOT NULL DEFAULT 'user',
    user_id INTEGER,
    contact_id INTEGER,
    address TEXT NOT NULL DEFAULT '',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_recipients_status ON communication_recipients(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_groups (
    id SERIAL PRIMARY KEY,
    group_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    organization_id INTEGER,
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_groups_status ON communication_groups(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    event_kind TEXT NOT NULL DEFAULT 'system',
    source_program TEXT NOT NULL DEFAULT 'platform',
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_events_status ON communication_events(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_logs_status ON communication_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    action TEXT NOT NULL DEFAULT '',
    actor_user_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE CASCADE,
    actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_history_status ON communication_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_archives (
    id SERIAL PRIMARY KEY,
    archive_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    archived_at TEXT NOT NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_archives_status ON communication_archives(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_metadata (
    id SERIAL PRIMARY KEY,
    metadata_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    resource_type TEXT NOT NULL DEFAULT 'message',
    resource_id INTEGER NOT NULL DEFAULT 0,
    meta_key TEXT NOT NULL DEFAULT '',
    meta_value_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_metadata_status ON communication_metadata(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_type TEXT NOT NULL DEFAULT 'system',
    user_id INTEGER,
    contact_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    priority TEXT NOT NULL DEFAULT 'normal',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_events_status ON notification_events(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_rules (
    id SERIAL PRIMARY KEY,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    event_kind TEXT NOT NULL DEFAULT 'system',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    rules_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_rules_status ON notification_rules(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_templates_status ON notification_templates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_preferences (
    id SERIAL PRIMARY KEY,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_preferences_status ON notification_preferences(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_deliveries (
    id SERIAL PRIMARY KEY,
    delivery_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    delivered_at TEXT,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_deliveries_status ON notification_deliveries(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_batches (
    id SERIAL PRIMARY KEY,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    completed_at TEXT
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_batches_status ON notification_batches(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_acknowledgements (
    id SERIAL PRIMARY KEY,
    ack_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    user_id INTEGER,
    acknowledged_at TEXT NOT NULL,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_acknowledgements_status ON notification_acknowledgements(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_failures (
    id SERIAL PRIMARY KEY,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_failures_status ON notification_failures(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_statistics_status ON notification_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS notification_queue (
    id SERIAL PRIMARY KEY,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_notification_queue_status ON notification_queue(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_accounts (
    id SERIAL PRIMARY KEY,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    organization_id INTEGER,
    email_address TEXT NOT NULL DEFAULT '',
    display_name TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_accounts_status ON email_accounts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body_html TEXT NOT NULL DEFAULT '',
    body_text TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_templates_status ON email_templates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_email TEXT NOT NULL DEFAULT '',
    from_email TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    email_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    account_id INTEGER REFERENCES email_accounts(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_messages_status ON email_messages(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_attachments (
    id SERIAL PRIMARY KEY,
    attachment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    filename TEXT NOT NULL DEFAULT '',
    content_type TEXT NOT NULL DEFAULT 'application/octet-stream',
    size_bytes INTEGER NOT NULL DEFAULT 0,
    storage_ref TEXT NOT NULL DEFAULT '',
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_attachments_status ON email_attachments(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_threads (
    id SERIAL PRIMARY KEY,
    thread_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT '',
    thread_status TEXT NOT NULL DEFAULT 'open',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_threads_status ON email_threads(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_delivery_logs_status ON email_delivery_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_statistics_status ON email_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_bounces (
    id SERIAL PRIMARY KEY,
    bounce_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    bounce_type TEXT NOT NULL DEFAULT 'hard',
    reason TEXT NOT NULL DEFAULT '',
    bounced_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_bounces_status ON email_bounces(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_click_tracking (
    id SERIAL PRIMARY KEY,
    click_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    link_url TEXT NOT NULL DEFAULT '',
    clicked_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_click_tracking_status ON email_click_tracking(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS email_open_tracking (
    id SERIAL PRIMARY KEY,
    open_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    opened_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_email_open_tracking_status ON email_open_tracking(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_templates_status ON sms_templates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    provider_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    from_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    sms_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    provider_id INTEGER REFERENCES sms_providers(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_messages_status ON sms_messages(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    sms_message_id INTEGER REFERENCES sms_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_delivery_logs_status ON sms_delivery_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_statistics_status ON sms_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_providers (
    id SERIAL PRIMARY KEY,
    provider_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    provider_type TEXT NOT NULL DEFAULT 'twilio',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_providers_status ON sms_providers(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS sms_queue (
    id SERIAL PRIMARY KEY,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    sms_message_id INTEGER REFERENCES sms_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_sms_queue_status ON sms_queue(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_accounts (
    id SERIAL PRIMARY KEY,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    handle TEXT NOT NULL DEFAULT '@lawimofficial',
    phone_e164 TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT 'meta_cloud',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_accounts_status ON whatsapp_accounts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    template_name TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT 'fr',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_templates_status ON whatsapp_templates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    whatsapp_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    account_id INTEGER REFERENCES whatsapp_accounts(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_messages_status ON whatsapp_messages(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_media (
    id SERIAL PRIMARY KEY,
    media_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    media_type TEXT NOT NULL DEFAULT 'document',
    filename TEXT NOT NULL DEFAULT '',
    storage_ref TEXT NOT NULL DEFAULT '',
    whatsapp_message_id INTEGER REFERENCES whatsapp_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_media_status ON whatsapp_media(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_sessions (
    id SERIAL PRIMARY KEY,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    contact_id INTEGER,
    session_status TEXT NOT NULL DEFAULT 'open',
    opened_at TEXT NOT NULL,
    closed_at TEXT,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_status ON whatsapp_sessions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    whatsapp_message_id INTEGER REFERENCES whatsapp_messages(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_delivery_logs_status ON whatsapp_delivery_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS whatsapp_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_whatsapp_statistics_status ON whatsapp_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS telegram_bots (
    id SERIAL PRIMARY KEY,
    bot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_handle TEXT NOT NULL DEFAULT '@lawim_assistant_bot',
    bot_token_ref TEXT NOT NULL DEFAULT '',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_telegram_bots_status ON telegram_bots(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS telegram_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    message_id INTEGER,
    chat_id TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    telegram_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    bot_id INTEGER REFERENCES telegram_bots(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_telegram_messages_status ON telegram_messages(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS telegram_updates (
    id SERIAL PRIMARY KEY,
    update_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    update_type TEXT NOT NULL DEFAULT 'message',
    payload_json TEXT NOT NULL DEFAULT '{}',
    received_at TEXT NOT NULL,
    bot_id INTEGER REFERENCES telegram_bots(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_telegram_updates_status ON telegram_updates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS telegram_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_telegram_statistics_status ON telegram_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS push_devices (
    id SERIAL PRIMARY KEY,
    device_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    platform TEXT NOT NULL DEFAULT 'web',
    device_token TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_push_devices_status ON push_devices(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS push_notifications (
    id SERIAL PRIMARY KEY,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    device_id INTEGER,
    message_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    push_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    device_id INTEGER REFERENCES push_devices(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_push_notifications_status ON push_notifications(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS push_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    push_notification_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    push_notification_id INTEGER REFERENCES push_notifications(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_push_delivery_logs_status ON push_delivery_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    subscription_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    topic TEXT NOT NULL DEFAULT '',
    subscription_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_status ON push_subscriptions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS push_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_push_statistics_status ON push_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS inapp_notifications (
    id SERIAL PRIMARY KEY,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    category_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    action_json TEXT NOT NULL DEFAULT '{}',
    read_at TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES inapp_categories(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_inapp_notifications_status ON inapp_notifications(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS inapp_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_inapp_categories_status ON inapp_categories(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS inapp_read_status (
    id SERIAL PRIMARY KEY,
    read_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_id INTEGER,
    user_id INTEGER,
    read_at TEXT NOT NULL,
    notification_id INTEGER REFERENCES inapp_notifications(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_inapp_read_status_status ON inapp_read_status(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS inapp_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_inapp_statistics_status ON inapp_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    campaign_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    campaign_type TEXT NOT NULL DEFAULT 'multichannel',
    organization_id INTEGER,
    campaign_status TEXT NOT NULL DEFAULT 'draft',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_channels (
    id SERIAL PRIMARY KEY,
    channel_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    config_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_channels_status ON campaign_channels(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_audiences (
    id SERIAL PRIMARY KEY,
    audience_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    audience_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_audiences_status ON campaign_audiences(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_segments (
    id SERIAL PRIMARY KEY,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    criteria_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_segments_status ON campaign_segments(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_executions (
    id SERIAL PRIMARY KEY,
    execution_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    execution_status TEXT NOT NULL DEFAULT 'pending',
    started_at TEXT,
    completed_at TEXT,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_executions_status ON campaign_executions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_statistics_status ON campaign_statistics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    result_type TEXT NOT NULL DEFAULT 'summary',
    result_json TEXT NOT NULL DEFAULT '{}',
    recorded_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_results_status ON campaign_results(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS campaign_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_campaign_logs_status ON campaign_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS queue_jobs (
    id SERIAL PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_type TEXT NOT NULL DEFAULT 'send_message',
    channel_type TEXT NOT NULL DEFAULT 'email',
    priority TEXT NOT NULL DEFAULT 'normal',
    job_status TEXT NOT NULL DEFAULT 'pending',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_queue_jobs_status ON queue_jobs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS queue_workers (
    id SERIAL PRIMARY KEY,
    worker_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    worker_name TEXT NOT NULL DEFAULT '',
    worker_status TEXT NOT NULL DEFAULT 'idle',
    last_heartbeat_at TEXT,
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_queue_workers_status ON queue_workers(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS queue_failures (
    id SERIAL PRIMARY KEY,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    job_id INTEGER REFERENCES queue_jobs(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_queue_failures_status ON queue_failures(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS queue_retry_history (
    id SERIAL PRIMARY KEY,
    retry_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    retry_at TEXT NOT NULL,
    result TEXT NOT NULL DEFAULT '',
    job_id INTEGER REFERENCES queue_jobs(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_queue_retry_history_status ON queue_retry_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS queue_batches (
    id SERIAL PRIMARY KEY,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    job_count INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_queue_batches_status ON queue_batches(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS template_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_template_categories_status ON template_categories(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS template_versions (
    id SERIAL PRIMARY KEY,
    version_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    category_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    version_number INTEGER NOT NULL DEFAULT 1,
    content_json TEXT NOT NULL DEFAULT '{}',
    published_at TEXT,
    category_id INTEGER REFERENCES template_categories(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_template_versions_status ON template_versions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS template_variables (
    id SERIAL PRIMARY KEY,
    variable_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    variable_name TEXT NOT NULL DEFAULT '',
    default_value TEXT NOT NULL DEFAULT '',
    template_version_id INTEGER REFERENCES template_versions(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_template_variables_status ON template_variables(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS template_translations (
    id SERIAL PRIMARY KEY,
    translation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    locale TEXT NOT NULL DEFAULT 'fr',
    content_json TEXT NOT NULL DEFAULT '{}',
    template_version_id INTEGER REFERENCES template_versions(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_template_translations_status ON template_translations(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_preferences (
    id SERIAL PRIMARY KEY,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_preferences_status ON communication_preferences(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_consent_history (
    id SERIAL PRIMARY KEY,
    consent_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    consent_type TEXT NOT NULL DEFAULT 'marketing',
    consent_status TEXT NOT NULL DEFAULT 'granted',
    recorded_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_consent_history_status ON communication_consent_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_blacklists (
    id SERIAL PRIMARY KEY,
    blacklist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    blocked_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_blacklists_status ON communication_blacklists(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_whitelists (
    id SERIAL PRIMARY KEY,
    whitelist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    allowed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_whitelists_status ON communication_whitelists(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_quiet_hours (
    id SERIAL PRIMARY KEY,
    quiet_hours_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    timezone TEXT NOT NULL DEFAULT 'Africa/Douala',
    start_time TEXT NOT NULL DEFAULT '22:00',
    end_time TEXT NOT NULL DEFAULT '07:00',
    days_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_quiet_hours_status ON communication_quiet_hours(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    snapshot_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_dashboard_snapshots_status ON communication_dashboard_snapshots(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_analytics (
    id SERIAL PRIMARY KEY,
    analytics_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    period TEXT NOT NULL DEFAULT 'daily',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_analytics_status ON communication_analytics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS communication_ai_recommendations (
    id SERIAL PRIMARY KEY,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    recommendation_type TEXT NOT NULL DEFAULT 'followup',
    recommendation_json TEXT NOT NULL DEFAULT '{}',
    score REAL NOT NULL DEFAULT 0,
    generated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_communication_ai_recommendations_status ON communication_ai_recommendations(status, created_at)
    """,
)
