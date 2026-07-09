from __future__ import annotations

import sqlite3
import tempfile
from http import HTTPStatus
from pathlib import Path

from lawim_v2.communication.constants import (
    CHANNEL_TYPES,
    MESSAGE_DIRECTIONS,
    MESSAGE_PRIORITIES,
    MESSAGE_STATUSES,
    THREAD_STATUSES,
    NOTIFICATION_TYPES,
    NOTIFICATION_STATUSES,
    DELIVERY_STATUSES,
    CAMPAIGN_STATUSES,
    CAMPAIGN_TYPES,
    QUEUE_JOB_STATUSES,
    QUEUE_JOB_TYPES,
    WORKER_STATUSES,
    TEMPLATE_STATUSES,
    CONSENT_TYPES,
    CONSENT_STATUSES,
    SMS_PROVIDERS,
    EMAIL_PROVIDERS,
    WHATSAPP_PROVIDERS,
    PUSH_PLATFORMS,
    EVENT_KINDS,
    OFFICIAL_TELEGRAM_BOT,
    OFFICIAL_WHATSAPP_HANDLE,
)
from lawim_v2.communication.engines import (
    AiCommunicationRecommendationEngine,
    AnalyticsEngine,
    CampaignEngine,
    CommunicationEngine,
    CommunicationPlatformEngine,
    CommunicationStatisticsEngine,
    ConversationEngine,
    DeliveryScheduler,
    EmailEngine,
    IntegrationBridge,
    NotificationEngine,
    PreferenceEngine,
    PriorityEngine,
    PushEngine,
    QueueEngine,
    RetryEngine,
    RoutingEngine,
    SmsEngine,
    TelegramEngine,
    TemplateEngine,
    WhatsappEngine,
)
from lawim_v2.communication.schema_v17_ddl import V17_TABLE_NAMES
from lawim_v2.crm.schema_v14_ddl import V14_TABLE_NAMES
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.marketplace.schema_v15_ddl import V15_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.security.schema_v16_ddl import V16_TABLE_NAMES
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness

class ReleaseProgramKPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v17(self) -> None:
        self.assertEqual(self.repository.schema_version(), 19)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 19)

    def test_communication_tables_present(self) -> None:
        self.assertTrue(self.repository.communication_tables_present())

    def test_all_v17_tables_exist(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V17_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v16_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V16_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v15_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V15_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v14_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v13_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v12_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_communication_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM communication_channels'), 1)
        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM notification_templates'), 1)
        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM notification_rules'), 1)

    def test_v16_to_v17_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / 'v16.sqlite3'
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute('PRAGMA foreign_keys = OFF')
        for table in V17_TABLE_NAMES:
            conn.execute(f'DROP TABLE IF EXISTS {table}')
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute("UPDATE schema_meta SET value='16' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn('communication_channels', names)
        for table in V16_TABLE_NAMES:
            self.assertIn(table, names)

    def test_seed_communication_catalog_idempotent(self) -> None:
        before = self.repository.scalar('SELECT COUNT(*) FROM communication_channels')
        self.repository.seed_communication_catalog()
        after = self.repository.scalar('SELECT COUNT(*) FROM communication_channels')
        self.assertEqual(before, after)

class ReleaseProgramKConstantsTests(LawimTestHarness):
    def test_channel_types_email(self) -> None:
        self.assertIn('email', CHANNEL_TYPES)

    def test_channel_types_in_app(self) -> None:
        self.assertIn('in_app', CHANNEL_TYPES)

    def test_channel_types_push(self) -> None:
        self.assertIn('push', CHANNEL_TYPES)

    def test_channel_types_sms(self) -> None:
        self.assertIn('sms', CHANNEL_TYPES)

    def test_channel_types_telegram(self) -> None:
        self.assertIn('telegram', CHANNEL_TYPES)

    def test_channel_types_webhook(self) -> None:
        self.assertIn('webhook', CHANNEL_TYPES)

    def test_channel_types_whatsapp(self) -> None:
        self.assertIn('whatsapp', CHANNEL_TYPES)

    def test_message_directions_inbound(self) -> None:
        self.assertIn('inbound', MESSAGE_DIRECTIONS)

    def test_message_directions_internal(self) -> None:
        self.assertIn('internal', MESSAGE_DIRECTIONS)

    def test_message_directions_outbound(self) -> None:
        self.assertIn('outbound', MESSAGE_DIRECTIONS)

    def test_message_priorities_critical(self) -> None:
        self.assertIn('critical', MESSAGE_PRIORITIES)

    def test_message_priorities_high(self) -> None:
        self.assertIn('high', MESSAGE_PRIORITIES)

    def test_message_priorities_low(self) -> None:
        self.assertIn('low', MESSAGE_PRIORITIES)

    def test_message_priorities_normal(self) -> None:
        self.assertIn('normal', MESSAGE_PRIORITIES)

    def test_message_priorities_urgent(self) -> None:
        self.assertIn('urgent', MESSAGE_PRIORITIES)

    def test_message_statuses_archived(self) -> None:
        self.assertIn('archived', MESSAGE_STATUSES)

    def test_message_statuses_cancelled(self) -> None:
        self.assertIn('cancelled', MESSAGE_STATUSES)

    def test_message_statuses_delivered(self) -> None:
        self.assertIn('delivered', MESSAGE_STATUSES)

    def test_message_statuses_draft(self) -> None:
        self.assertIn('draft', MESSAGE_STATUSES)

    def test_message_statuses_expired(self) -> None:
        self.assertIn('expired', MESSAGE_STATUSES)

    def test_message_statuses_failed(self) -> None:
        self.assertIn('failed', MESSAGE_STATUSES)

    def test_message_statuses_queued(self) -> None:
        self.assertIn('queued', MESSAGE_STATUSES)

    def test_message_statuses_sending(self) -> None:
        self.assertIn('sending', MESSAGE_STATUSES)

    def test_message_statuses_sent(self) -> None:
        self.assertIn('sent', MESSAGE_STATUSES)

    def test_thread_statuses_archived(self) -> None:
        self.assertIn('archived', THREAD_STATUSES)

    def test_thread_statuses_closed(self) -> None:
        self.assertIn('closed', THREAD_STATUSES)

    def test_thread_statuses_open(self) -> None:
        self.assertIn('open', THREAD_STATUSES)

    def test_thread_statuses_spam(self) -> None:
        self.assertIn('spam', THREAD_STATUSES)

    def test_notification_types_admin(self) -> None:
        self.assertIn('admin', NOTIFICATION_TYPES)

    def test_notification_types_ai(self) -> None:
        self.assertIn('ai', NOTIFICATION_TYPES)

    def test_notification_types_api(self) -> None:
        self.assertIn('api', NOTIFICATION_TYPES)

    def test_notification_types_assistant(self) -> None:
        self.assertIn('assistant', NOTIFICATION_TYPES)

    def test_notification_types_critical(self) -> None:
        self.assertIn('critical', NOTIFICATION_TYPES)

    def test_notification_types_crm(self) -> None:
        self.assertIn('crm', NOTIFICATION_TYPES)

    def test_notification_types_deferred(self) -> None:
        self.assertIn('deferred', NOTIFICATION_TYPES)

    def test_notification_types_external(self) -> None:
        self.assertIn('external', NOTIFICATION_TYPES)

    def test_notification_types_internal(self) -> None:
        self.assertIn('internal', NOTIFICATION_TYPES)

    def test_notification_types_knowledge(self) -> None:
        self.assertIn('knowledge', NOTIFICATION_TYPES)

    def test_notification_types_marketplace(self) -> None:
        self.assertIn('marketplace', NOTIFICATION_TYPES)

    def test_notification_types_rei(self) -> None:
        self.assertIn('rei', NOTIFICATION_TYPES)

    def test_notification_types_security(self) -> None:
        self.assertIn('security', NOTIFICATION_TYPES)

    def test_notification_types_silent(self) -> None:
        self.assertIn('silent', NOTIFICATION_TYPES)

    def test_notification_types_system(self) -> None:
        self.assertIn('system', NOTIFICATION_TYPES)

    def test_notification_types_urgent(self) -> None:
        self.assertIn('urgent', NOTIFICATION_TYPES)

    def test_notification_types_user(self) -> None:
        self.assertIn('user', NOTIFICATION_TYPES)

    def test_notification_types_webhook(self) -> None:
        self.assertIn('webhook', NOTIFICATION_TYPES)

    def test_notification_types_workflow(self) -> None:
        self.assertIn('workflow', NOTIFICATION_TYPES)

    def test_notification_statuses_acknowledged(self) -> None:
        self.assertIn('acknowledged', NOTIFICATION_STATUSES)

    def test_notification_statuses_cancelled(self) -> None:
        self.assertIn('cancelled', NOTIFICATION_STATUSES)

    def test_notification_statuses_delivered(self) -> None:
        self.assertIn('delivered', NOTIFICATION_STATUSES)

    def test_notification_statuses_delivering(self) -> None:
        self.assertIn('delivering', NOTIFICATION_STATUSES)

    def test_notification_statuses_failed(self) -> None:
        self.assertIn('failed', NOTIFICATION_STATUSES)

    def test_notification_statuses_pending(self) -> None:
        self.assertIn('pending', NOTIFICATION_STATUSES)

    def test_notification_statuses_queued(self) -> None:
        self.assertIn('queued', NOTIFICATION_STATUSES)

    def test_delivery_statuses_bounced(self) -> None:
        self.assertIn('bounced', DELIVERY_STATUSES)

    def test_delivery_statuses_delivered(self) -> None:
        self.assertIn('delivered', DELIVERY_STATUSES)

    def test_delivery_statuses_failed(self) -> None:
        self.assertIn('failed', DELIVERY_STATUSES)

    def test_delivery_statuses_pending(self) -> None:
        self.assertIn('pending', DELIVERY_STATUSES)

    def test_delivery_statuses_processing(self) -> None:
        self.assertIn('processing', DELIVERY_STATUSES)

    def test_delivery_statuses_sent(self) -> None:
        self.assertIn('sent', DELIVERY_STATUSES)

    def test_delivery_statuses_skipped(self) -> None:
        self.assertIn('skipped', DELIVERY_STATUSES)

    def test_campaign_statuses_archived(self) -> None:
        self.assertIn('archived', CAMPAIGN_STATUSES)

    def test_campaign_statuses_cancelled(self) -> None:
        self.assertIn('cancelled', CAMPAIGN_STATUSES)

    def test_campaign_statuses_completed(self) -> None:
        self.assertIn('completed', CAMPAIGN_STATUSES)

    def test_campaign_statuses_draft(self) -> None:
        self.assertIn('draft', CAMPAIGN_STATUSES)

    def test_campaign_statuses_paused(self) -> None:
        self.assertIn('paused', CAMPAIGN_STATUSES)

    def test_campaign_statuses_running(self) -> None:
        self.assertIn('running', CAMPAIGN_STATUSES)

    def test_campaign_statuses_scheduled(self) -> None:
        self.assertIn('scheduled', CAMPAIGN_STATUSES)

    def test_campaign_types_email(self) -> None:
        self.assertIn('email', CAMPAIGN_TYPES)

    def test_campaign_types_multichannel(self) -> None:
        self.assertIn('multichannel', CAMPAIGN_TYPES)

    def test_campaign_types_push(self) -> None:
        self.assertIn('push', CAMPAIGN_TYPES)

    def test_campaign_types_sms(self) -> None:
        self.assertIn('sms', CAMPAIGN_TYPES)

    def test_campaign_types_whatsapp(self) -> None:
        self.assertIn('whatsapp', CAMPAIGN_TYPES)

    def test_queue_job_statuses_cancelled(self) -> None:
        self.assertIn('cancelled', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_completed(self) -> None:
        self.assertIn('completed', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_dead_letter(self) -> None:
        self.assertIn('dead_letter', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_failed(self) -> None:
        self.assertIn('failed', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_pending(self) -> None:
        self.assertIn('pending', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_processing(self) -> None:
        self.assertIn('processing', QUEUE_JOB_STATUSES)

    def test_queue_job_statuses_retrying(self) -> None:
        self.assertIn('retrying', QUEUE_JOB_STATUSES)

    def test_queue_job_types_process_batch(self) -> None:
        self.assertIn('process_batch', QUEUE_JOB_TYPES)

    def test_queue_job_types_retry_delivery(self) -> None:
        self.assertIn('retry_delivery', QUEUE_JOB_TYPES)

    def test_queue_job_types_run_campaign(self) -> None:
        self.assertIn('run_campaign', QUEUE_JOB_TYPES)

    def test_queue_job_types_send_message(self) -> None:
        self.assertIn('send_message', QUEUE_JOB_TYPES)

    def test_queue_job_types_send_notification(self) -> None:
        self.assertIn('send_notification', QUEUE_JOB_TYPES)

    def test_worker_statuses_busy(self) -> None:
        self.assertIn('busy', WORKER_STATUSES)

    def test_worker_statuses_draining(self) -> None:
        self.assertIn('draining', WORKER_STATUSES)

    def test_worker_statuses_idle(self) -> None:
        self.assertIn('idle', WORKER_STATUSES)

    def test_worker_statuses_offline(self) -> None:
        self.assertIn('offline', WORKER_STATUSES)

    def test_template_statuses_active(self) -> None:
        self.assertIn('active', TEMPLATE_STATUSES)

    def test_template_statuses_archived(self) -> None:
        self.assertIn('archived', TEMPLATE_STATUSES)

    def test_template_statuses_deprecated(self) -> None:
        self.assertIn('deprecated', TEMPLATE_STATUSES)

    def test_template_statuses_draft(self) -> None:
        self.assertIn('draft', TEMPLATE_STATUSES)

    def test_consent_types_analytics(self) -> None:
        self.assertIn('analytics', CONSENT_TYPES)

    def test_consent_types_email(self) -> None:
        self.assertIn('email', CONSENT_TYPES)

    def test_consent_types_marketing(self) -> None:
        self.assertIn('marketing', CONSENT_TYPES)

    def test_consent_types_push(self) -> None:
        self.assertIn('push', CONSENT_TYPES)

    def test_consent_types_sms(self) -> None:
        self.assertIn('sms', CONSENT_TYPES)

    def test_consent_types_transactional(self) -> None:
        self.assertIn('transactional', CONSENT_TYPES)

    def test_consent_types_whatsapp(self) -> None:
        self.assertIn('whatsapp', CONSENT_TYPES)

    def test_consent_statuses_expired(self) -> None:
        self.assertIn('expired', CONSENT_STATUSES)

    def test_consent_statuses_granted(self) -> None:
        self.assertIn('granted', CONSENT_STATUSES)

    def test_consent_statuses_pending(self) -> None:
        self.assertIn('pending', CONSENT_STATUSES)

    def test_consent_statuses_revoked(self) -> None:
        self.assertIn('revoked', CONSENT_STATUSES)

    def test_sms_providers_aws_sns(self) -> None:
        self.assertIn('aws_sns', SMS_PROVIDERS)

    def test_sms_providers_infobip(self) -> None:
        self.assertIn('infobip', SMS_PROVIDERS)

    def test_sms_providers_messagebird(self) -> None:
        self.assertIn('messagebird', SMS_PROVIDERS)

    def test_sms_providers_mtn(self) -> None:
        self.assertIn('mtn', SMS_PROVIDERS)

    def test_sms_providers_orange(self) -> None:
        self.assertIn('orange', SMS_PROVIDERS)

    def test_sms_providers_twilio(self) -> None:
        self.assertIn('twilio', SMS_PROVIDERS)

    def test_email_providers_aws_ses(self) -> None:
        self.assertIn('aws_ses', EMAIL_PROVIDERS)

    def test_email_providers_mailgun(self) -> None:
        self.assertIn('mailgun', EMAIL_PROVIDERS)

    def test_email_providers_sendgrid(self) -> None:
        self.assertIn('sendgrid', EMAIL_PROVIDERS)

    def test_email_providers_smtp(self) -> None:
        self.assertIn('smtp', EMAIL_PROVIDERS)

    def test_whatsapp_providers_green_api(self) -> None:
        self.assertIn('green_api', WHATSAPP_PROVIDERS)

    def test_whatsapp_providers_meta_cloud(self) -> None:
        self.assertIn('meta_cloud', WHATSAPP_PROVIDERS)

    def test_push_platforms_android(self) -> None:
        self.assertIn('android', PUSH_PLATFORMS)

    def test_push_platforms_desktop(self) -> None:
        self.assertIn('desktop', PUSH_PLATFORMS)

    def test_push_platforms_ios(self) -> None:
        self.assertIn('ios', PUSH_PLATFORMS)

    def test_push_platforms_web(self) -> None:
        self.assertIn('web', PUSH_PLATFORMS)

    def test_event_kinds_AssistantConversationCreated(self) -> None:
        self.assertIn('AssistantConversationCreated', EVENT_KINDS)

    def test_event_kinds_AssistantRecommendation(self) -> None:
        self.assertIn('AssistantRecommendation', EVENT_KINDS)

    def test_event_kinds_AuditCompleted(self) -> None:
        self.assertIn('AuditCompleted', EVENT_KINDS)

    def test_event_kinds_ContractActivated(self) -> None:
        self.assertIn('ContractActivated', EVENT_KINDS)

    def test_event_kinds_CustomerCreated(self) -> None:
        self.assertIn('CustomerCreated', EVENT_KINDS)

    def test_event_kinds_CustomerUpdated(self) -> None:
        self.assertIn('CustomerUpdated', EVENT_KINDS)

    def test_event_kinds_InvoiceGenerated(self) -> None:
        self.assertIn('InvoiceGenerated', EVENT_KINDS)

    def test_event_kinds_KnowledgeIndexed(self) -> None:
        self.assertIn('KnowledgeIndexed', EVENT_KINDS)

    def test_event_kinds_LeadQualified(self) -> None:
        self.assertIn('LeadQualified', EVENT_KINDS)

    def test_event_kinds_MarketplaceQuoteAccepted(self) -> None:
        self.assertIn('MarketplaceQuoteAccepted', EVENT_KINDS)

    def test_event_kinds_MarketplaceRequestCreated(self) -> None:
        self.assertIn('MarketplaceRequestCreated', EVENT_KINDS)

    def test_event_kinds_MissionAssigned(self) -> None:
        self.assertIn('MissionAssigned', EVENT_KINDS)

    def test_event_kinds_MissionCompleted(self) -> None:
        self.assertIn('MissionCompleted', EVENT_KINDS)

    def test_event_kinds_PaymentPrepared(self) -> None:
        self.assertIn('PaymentPrepared', EVENT_KINDS)

    def test_event_kinds_PropertyPublished(self) -> None:
        self.assertIn('PropertyPublished', EVENT_KINDS)

    def test_event_kinds_PropertySold(self) -> None:
        self.assertIn('PropertySold', EVENT_KINDS)

    def test_event_kinds_SecurityAlertRaised(self) -> None:
        self.assertIn('SecurityAlertRaised', EVENT_KINDS)

    def test_event_kinds_SecurityIncident(self) -> None:
        self.assertIn('SecurityIncident', EVENT_KINDS)

    def test_event_kinds_SubscriptionExpired(self) -> None:
        self.assertIn('SubscriptionExpired', EVENT_KINDS)

    def test_event_kinds_WorkflowCompleted(self) -> None:
        self.assertIn('WorkflowCompleted', EVENT_KINDS)

    def test_event_kinds_WorkflowStarted(self) -> None:
        self.assertIn('WorkflowStarted', EVENT_KINDS)

    def test_official_whatsapp_handle_set(self) -> None:
        self.assertTrue(len(OFFICIAL_WHATSAPP_HANDLE) > 0)

    def test_official_telegram_bot_set(self) -> None:
        self.assertTrue(len(OFFICIAL_TELEGRAM_BOT) > 0)

class ReleaseProgramKEnginesTests(LawimTestHarness):
    def test_communication_engine_validate_channel_email(self) -> None:
        self.assertEqual(CommunicationEngine().validate_channel('email'), 'email')

    def test_communication_engine_validate_channel_invalid(self) -> None:
        self.assertEqual(CommunicationEngine().validate_channel('invalid'), 'email')

    def test_communication_engine_validate_status_sent(self) -> None:
        self.assertEqual(CommunicationEngine().validate_status('sent'), 'sent')

    def test_communication_engine_build_payload(self) -> None:
        payload = CommunicationEngine().build_message_payload(channel_type='sms', body='Hello', subject='Hi')
        self.assertEqual(payload['channel_type'], 'sms')

    def test_communication_engine_format_outbound_body(self) -> None:
        text = CommunicationEngine().format_outbound_body('Hello', include_signature=False)
        self.assertEqual(text, 'Hello')

    def test_notification_engine_validate_type(self) -> None:
        self.assertEqual(NotificationEngine().validate_type('workflow'), 'workflow')

    def test_notification_engine_should_deliver_default(self) -> None:
        result = NotificationEngine().should_deliver(notification_type='user', channel_type='email', preferences=None)
        self.assertTrue(result['deliver'])

    def test_notification_engine_should_deliver_quiet_hours(self) -> None:
        result = NotificationEngine().should_deliver(notification_type='user', channel_type='email', preferences=None, quiet_hours_active=True)
        self.assertFalse(result['deliver'])

    def test_notification_engine_should_deliver_critical_quiet_hours(self) -> None:
        result = NotificationEngine().should_deliver(notification_type='critical', channel_type='email', preferences=None, quiet_hours_active=True)
        self.assertTrue(result['deliver'])

    def test_email_engine_build_payload(self) -> None:
        payload = EmailEngine().build_payload(to_email='a@example.com', subject='S', body='B')
        self.assertEqual(payload['to_email'], 'a@example.com')

    def test_email_engine_stub_send(self) -> None:
        result = EmailEngine().stub_send({'to_email': 'a@example.com'})
        self.assertTrue(result['sent'])

    def test_sms_engine_normalize_provider(self) -> None:
        self.assertEqual(SmsEngine().normalize_provider('orange'), 'orange')

    def test_sms_engine_build_payload(self) -> None:
        payload = SmsEngine().build_payload(to_number='+237600000000', body='Hi')
        self.assertEqual(payload['channel'], 'sms')

    def test_sms_engine_stub_send(self) -> None:
        result = SmsEngine().stub_send({'provider': 'orange'})
        self.assertTrue(result['sent'])

    def test_whatsapp_engine_build_payload(self) -> None:
        payload = WhatsappEngine().build_payload(to_number='+237600000000', body='Hi')
        self.assertEqual(payload['channel'], 'whatsapp')

    def test_whatsapp_engine_stub_send(self) -> None:
        result = WhatsappEngine().stub_send({})
        self.assertTrue(result['sent'])

    def test_telegram_engine_build_payload(self) -> None:
        payload = TelegramEngine().build_payload(chat_id='123', body='Hi')
        self.assertEqual(payload['channel'], 'telegram')

    def test_telegram_engine_stub_send(self) -> None:
        result = TelegramEngine().stub_send({})
        self.assertTrue(result['sent'])

    def test_push_engine_build_payload(self) -> None:
        payload = PushEngine().build_payload(title='T', body='B')
        self.assertEqual(payload['channel'], 'push')

    def test_push_engine_stub_send(self) -> None:
        result = PushEngine().stub_send({})
        self.assertTrue(result['sent'])

    def test_campaign_engine_validate_status(self) -> None:
        self.assertEqual(CampaignEngine().validate_status('running'), 'running')

    def test_campaign_engine_can_transition_draft_running(self) -> None:
        self.assertTrue(CampaignEngine().can_transition(current='draft', target='running'))

    def test_campaign_engine_can_transition_completed_running(self) -> None:
        self.assertFalse(CampaignEngine().can_transition(current='completed', target='running'))

    def test_campaign_engine_plan_execution(self) -> None:
        plan = CampaignEngine().plan_execution(campaign={'id': 1}, channels=['email', 'sms'])
        self.assertEqual(len(plan['steps']), 2)

    def test_queue_engine_validate_job_status(self) -> None:
        self.assertEqual(QueueEngine().validate_job_status('pending'), 'pending')

    def test_queue_engine_should_retry(self) -> None:
        self.assertTrue(QueueEngine().should_retry(attempt_count=1, max_attempts=3))

    def test_queue_engine_next_retry_delay(self) -> None:
        self.assertEqual(QueueEngine().next_retry_delay(2), 120)

    def test_template_engine_extract_variables(self) -> None:
        vars_ = TemplateEngine().extract_variables('Hello {{name}}')
        self.assertIn('name', vars_)

    def test_template_engine_render(self) -> None:
        rendered = TemplateEngine().render(template='Hi {{name}}', variables={'name': 'Ada'})
        self.assertEqual(rendered, 'Hi Ada')

    def test_template_engine_validate(self) -> None:
        result = TemplateEngine().validate(subject='Hi {{name}}', body='Body', required=['name'])
        self.assertTrue(result['valid'])

    def test_preference_engine_merge_preferences(self) -> None:
        pref = PreferenceEngine().merge_preferences(user_prefs=[{'channel_type': 'email', 'enabled': True}], channel_type='email')
        self.assertIsNotNone(pref)

    def test_preference_engine_is_quiet_hours_none(self) -> None:
        self.assertFalse(PreferenceEngine().is_quiet_hours(quiet_hours=None))

    def test_analytics_engine_aggregate_metrics(self) -> None:
        result = AnalyticsEngine().aggregate_metrics(counters={'channel_email': 3, 'channel_sms': 2})
        self.assertEqual(result['total'], 5)

    def test_statistics_engine_compute_rates(self) -> None:
        result = CommunicationStatisticsEngine().compute_rates(sent=10, delivered=8, failed=2)
        self.assertEqual(result['sent'], 10)

    def test_ai_recommendation_engine(self) -> None:
        result = AiCommunicationRecommendationEngine().recommend_followup(contact_id=1, last_channel='email', days_since_contact=10)
        self.assertEqual(result['recommended_channel'], 'email')

    def test_delivery_scheduler_is_due_no_schedule(self) -> None:
        self.assertTrue(DeliveryScheduler().is_due(scheduled_at=None))

    def test_retry_engine_plan_retry(self) -> None:
        plan = RetryEngine().plan_retry(attempt_count=1, max_attempts=3)
        self.assertTrue(plan['retry'])

    def test_priority_engine_weight_critical(self) -> None:
        self.assertEqual(PriorityEngine().weight('critical'), 50)

    def test_routing_engine_route_security(self) -> None:
        result = RoutingEngine().route(channel_type='email', event_kind='SecurityAlertRaised')
        self.assertEqual(result['channel_type'], 'in_app')

    def test_conversation_engine_thread_key(self) -> None:
        key = ConversationEngine().thread_key_for_participants(user_id=1, contact_id=2)
        self.assertIn('u1', key)

    def test_integration_bridge_sources(self) -> None:
        self.assertIn('crm', IntegrationBridge().sources())

    def test_integration_bridge_map_event_kind(self) -> None:
        result = IntegrationBridge().map_event_kind('LeadQualified')
        self.assertTrue(result['valid'])

    def test_platform_engine_has_communication_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().communication, CommunicationEngine)

    def test_platform_engine_has_email_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().email, EmailEngine)

    def test_platform_engine_has_sms_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().sms, SmsEngine)

    def test_platform_engine_has_whatsapp_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().whatsapp, WhatsappEngine)

    def test_platform_engine_has_telegram_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().telegram, TelegramEngine)

    def test_platform_engine_has_push_engine(self) -> None:
        self.assertIsInstance(CommunicationPlatformEngine().push, PushEngine)

    def test_platform_engine_integration_sources(self) -> None:
        self.assertIn('security', CommunicationPlatformEngine().integration_sources())

class ReleaseProgramKRepositoryTests(LawimTestHarness):
    def _user_id(self) -> int:
        return int(self.repository.one('SELECT id FROM users LIMIT 1')['id'])

    def _channel_id(self) -> int:
        return int(self.repository.one('SELECT id FROM communication_channels LIMIT 1')['id'])

    def test_list_communication_messages(self) -> None:
        rows = self.repository.list_communication_messages()
        self.assertIsInstance(rows, list)

    def test_create_communication_message(self) -> None:
        message = self.repository.create_communication_message(body='Repo body', subject='Repo subject')
        self.assertIn('message_key', message)

    def test_get_communication_message(self) -> None:
        message = self.repository.create_communication_message(body='Get body')
        row = self.repository.get_communication_message(int(message['id']))
        self.assertEqual(row['body'], 'Get body')

    def test_update_communication_message(self) -> None:
        message = self.repository.create_communication_message(body='Old')
        updated = self.repository.update_communication_message(int(message['id']), status='sent')
        self.assertEqual(updated['status'], 'sent')

    def test_list_communication_channels(self) -> None:
        rows = self.repository.list_communication_channels()
        self.assertGreaterEqual(len(rows), 1)

    def test_get_communication_channel(self) -> None:
        channel = self.repository.get_communication_channel(self._channel_id())
        self.assertIn('channel_type', channel)

    def test_create_communication_thread(self) -> None:
        thread = self.repository.create_communication_thread(subject='Thread')
        self.assertIn('thread_key', thread)

    def test_list_communication_threads(self) -> None:
        rows = self.repository.list_communication_threads()
        self.assertIsInstance(rows, list)

    def test_create_notification_event(self) -> None:
        event = self.repository.create_notification_event(notification_type='user', title='Hello', body='World')
        self.assertIn('event_key', event)

    def test_list_notification_events(self) -> None:
        rows = self.repository.list_notification_events()
        self.assertIsInstance(rows, list)

    def test_create_notification_template(self) -> None:
        template = self.repository.create_notification_template(name='Repo Template', channel_type='email', subject='S', body='B')
        self.assertEqual(template['name'], 'Repo Template')

    def test_list_notification_templates(self) -> None:
        rows = self.repository.list_notification_templates()
        self.assertGreaterEqual(len(rows), 1)

    def test_get_notification_template(self) -> None:
        template = self.repository.create_notification_template(name='Get Template', channel_type='sms', subject='', body='B')
        row = self.repository.get_notification_template(int(template['id']))
        self.assertEqual(row['name'], 'Get Template')

    def test_record_delivery(self) -> None:
        email = self.repository.send_email(to_email='delivery@example.com', subject='S', body='B')
        delivery = self.repository.record_delivery(
            channel_type='email',
            resource_type='email_message',
            resource_id=int(email['id']),
            delivery_status='delivered',
        )
        self.assertIn('log_key', delivery)

    def test_send_email(self) -> None:
        result = self.repository.send_email(to_email='client@example.com', subject='Subject', body='Body')
        self.assertIn('message_key', result)

    def test_list_email_messages(self) -> None:
        rows = self.repository.list_email_messages()
        self.assertIsInstance(rows, list)

    def test_send_sms(self) -> None:
        result = self.repository.send_sms(to_number='+237600000000', body='SMS')
        self.assertIn('message_key', result)

    def test_list_sms_messages(self) -> None:
        rows = self.repository.list_sms_messages()
        self.assertIsInstance(rows, list)

    def test_send_whatsapp(self) -> None:
        result = self.repository.send_whatsapp(to_number='+237600000000', body='WA')
        self.assertIn('message_key', result)

    def test_list_whatsapp_messages(self) -> None:
        rows = self.repository.list_whatsapp_messages()
        self.assertIsInstance(rows, list)

    def test_send_telegram(self) -> None:
        result = self.repository.send_telegram(chat_id='12345', body='TG')
        self.assertIn('message_key', result)

    def test_list_telegram_messages(self) -> None:
        rows = self.repository.list_telegram_messages()
        self.assertIsInstance(rows, list)

    def test_send_push(self) -> None:
        result = self.repository.send_push(title='Push', body='Body')
        self.assertIn('notification_key', result)

    def test_list_push_notifications(self) -> None:
        rows = self.repository.list_push_notifications()
        self.assertIsInstance(rows, list)

    def test_create_campaign(self) -> None:
        campaign = self.repository.create_campaign(name='Repo Campaign')
        self.assertEqual(campaign['name'], 'Repo Campaign')

    def test_list_campaigns(self) -> None:
        rows = self.repository.list_campaigns()
        self.assertIsInstance(rows, list)

    def test_update_campaign(self) -> None:
        campaign = self.repository.create_campaign(name='Update Campaign')
        updated = self.repository.update_campaign(int(campaign['id']), campaign_status='scheduled')
        self.assertEqual(updated['campaign_status'], 'scheduled')

    def test_execute_campaign(self) -> None:
        campaign = self.repository.create_campaign(name='Exec Campaign')
        execution = self.repository.execute_campaign(int(campaign['id']))
        self.assertIn('execution_key', execution)

    def test_enqueue_message(self) -> None:
        job = self.repository.enqueue_message(channel_type='email', payload={'message_id': 1})
        self.assertIn('job_key', job)

    def test_list_queue_jobs(self) -> None:
        rows = self.repository.list_queue_jobs()
        self.assertIsInstance(rows, list)

    def test_retry_job(self) -> None:
        job = self.repository.enqueue_message(channel_type='sms', payload={'test': True})
        retried = self.repository.retry_job(int(job['id']))
        self.assertIn(retried['job_status'], {'retrying', 'dead_letter'})

    def test_process_next_queue_job(self) -> None:
        self.repository.enqueue_message(channel_type='email', payload={'ready': True})
        processed = self.repository.process_next_queue_job()
        self.assertIsNotNone(processed)

    def test_get_communication_preference(self) -> None:
        pref = self.repository.upsert_communication_preference(user_id=self._user_id(), channel_type='email', enabled=True)
        row = self.repository.get_communication_preference(user_id=self._user_id(), channel_type='email')
        self.assertEqual(int(row['id']), int(pref['id']))

    def test_list_communication_consents(self) -> None:
        rows = self.repository.list_communication_consents(user_id=self._user_id())
        self.assertIsInstance(rows, list)

    def test_record_communication_consent(self) -> None:
        consent = self.repository.record_communication_consent(user_id=self._user_id(), consent_type='email', consent_status='granted')
        self.assertEqual(consent['consent_status'], 'granted')

    def test_list_communication_events(self) -> None:
        rows = self.repository.list_communication_events()
        self.assertIsInstance(rows, list)

    def test_list_communication_history(self) -> None:
        rows = self.repository.list_communication_history()
        self.assertIsInstance(rows, list)

    def test_list_communication_groups(self) -> None:
        rows = self.repository.list_communication_groups()
        self.assertIsInstance(rows, list)

    def test_list_inapp_notifications(self) -> None:
        rows = self.repository.list_inapp_notifications(user_id=self._user_id())
        self.assertIsInstance(rows, list)

    def test_search_communication_messages(self) -> None:
        self.repository.create_communication_message(body='Searchable unique token xyz')
        rows = self.repository.search_communication_messages(query='Searchable')
        self.assertGreaterEqual(len(rows), 1)

    def test_snapshot_communication_dashboard(self) -> None:
        snapshot = self.repository.snapshot_communication_dashboard()
        self.assertIn('messages', snapshot)

    def test_list_ai_recommendations(self) -> None:
        rows = self.repository.list_ai_recommendations(user_id=self._user_id())
        self.assertIsInstance(rows, list)

    def test_export_communication_snapshot(self) -> None:
        payload = self.repository.export_communication_snapshot()
        self.assertIn('stats', payload)

    def test_integration_sources(self) -> None:
        payload = self.repository.integration_sources()
        self.assertIn('programs', payload)

class ReleaseProgramKApiTests(LawimTestHarness):
    def _admin_token(self) -> str:
        return self.login(email='admin@lawim.local')

    def test_get_api_v2_communication_integrations(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/integrations', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('sources', response.body_json())

    def test_get_api_v2_communication_health(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/health', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('status', response.body_json())

    def test_get_api_v2_communication_messages(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/messages', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('messages', response.body_json())

    def test_get_api_v2_communication_channels(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/channels', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('channels', response.body_json())

    def test_get_api_v2_communication_conversations(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/conversations', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('threads', response.body_json())

    def test_get_api_v2_communication_history(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/history', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('history', response.body_json())

    def test_get_api_v2_communication_groups(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/groups', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('groups', response.body_json())

    def test_get_api_v2_communication_events(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/events', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('events', response.body_json())

    def test_get_api_v2_communication_templates(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/templates', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('templates', response.body_json())

    def test_get_api_v2_communication_preferences(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/preferences', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('preference', response.body_json())

    def test_get_api_v2_communication_campaigns(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/campaigns', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('campaigns', response.body_json())

    def test_get_api_v2_communication_notifications(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/notifications', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('notifications', response.body_json())

    def test_get_api_v2_communication_email(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/email', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('messages', response.body_json())

    def test_get_api_v2_communication_sms(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/sms', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('messages', response.body_json())

    def test_get_api_v2_communication_whatsapp(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/whatsapp', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('messages', response.body_json())

    def test_get_api_v2_communication_telegram(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/telegram', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('messages', response.body_json())

    def test_get_api_v2_communication_push(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/push', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('notifications', response.body_json())

    def test_get_api_v2_communication_inapp(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/inapp', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('notifications', response.body_json())

    def test_get_api_v2_communication_queue(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/queue', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('jobs', response.body_json())

    def test_get_api_v2_communication_statistics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/statistics', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('stats', response.body_json())

    def test_get_api_v2_communication_dashboard(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/dashboard', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('dashboard', response.body_json())

    def test_get_api_v2_communication_analytics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/analytics', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('analytics', response.body_json())

    def test_get_api_v2_communication_reports(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/reports', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('report', response.body_json())

    def test_get_api_v2_communication_search_q_test(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/search?q=test', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('results', response.body_json())

    def test_get_api_v2_communication_export(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/export', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('export', response.body_json())

    def test_post_api_v2_communication_messages(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/messages', method='POST', token=token, body={'body': 'API body', 'subject': 'API subject'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('message', response.body_json())

    def test_post_api_v2_communication_messages_send(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'email', 'to_email': 'api@example.com', 'subject': 'Hi', 'body': 'Hello'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('delivery', response.body_json())

    def test_post_api_v2_communication_conversations(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/conversations', method='POST', token=token, body={'subject': 'API thread'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('thread', response.body_json())

    def test_post_api_v2_communication_templates(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/templates', method='POST', token=token, body={'name': 'API Template', 'channel_type': 'email', 'subject': 'S', 'body': 'B'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('template', response.body_json())

    def test_post_api_v2_communication_preferences(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/preferences', method='POST', token=token, body={'channel_type': 'email', 'enabled': True})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('preference', response.body_json())

    def test_post_api_v2_communication_campaigns(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/campaigns', method='POST', token=token, body={'name': 'API Campaign'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('campaign', response.body_json())

    def test_post_api_v2_communication_notifications(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/notifications', method='POST', token=token, body={'title': 'API Notice', 'body': 'Body'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('notification', response.body_json())

    def test_post_api_v2_communication_queue(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/queue', method='POST', token=token, body={'channel_type': 'email', 'payload': {'test': True}})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('job', response.body_json())

    def test_post_api_v2_communication_events(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/events', method='POST', token=token, body={'event_kind': 'LeadQualified', 'source_program': 'crm', 'payload': {}})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('result', response.body_json())

    def test_post_api_v2_communication_seed(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/communication/seed', method='POST', token=token, body={})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('seeded', response.body_json())

    def test_integrations_api_no_auth(self) -> None:
        response = self.invoke('/api/v2/communication/integrations')
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIn('sources', response.body_json())

class ReleaseProgramKUiTests(LawimTestHarness):
    def test_index_has_communication_center_section(self) -> None:
        html = self.invoke('/')
        self.assertIn('Communication Center', html.body_text())

    def test_app_js_references_refresh_communication_admin(self) -> None:
        js = self.invoke('/app.js')
        self.assertIn('refreshCommunicationAdmin', js.body_text())

    def test_app_js_references_communication_stats_api(self) -> None:
        js = self.invoke('/app.js')
        self.assertIn('/api/v2/communication/statistics', js.body_text())

    def test_app_js_references_communication_messages_api(self) -> None:
        js = self.invoke('/app.js')
        self.assertIn('/api/v2/communication/messages', js.body_text())

    def test_index_has_communication_admin_stats(self) -> None:
        html = self.invoke('/')
        self.assertIn('id="communication-admin-stats"', html.body_text())

class ReleaseProgramKHealthTests(LawimTestHarness):
    def test_health_schema_v17(self) -> None:
        health = self.invoke('/api/health')
        self.assertEqual(health.body_json()['database']['schema_version'], 18)

    def test_migration_strategy_v17(self) -> None:
        self.assertEqual(migration_strategy_profile()['schema_version'], 18)

    def test_bootstrap_schema_v17(self) -> None:
        bootstrap = self.invoke('/api/bootstrap')
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        self.assertEqual(self.repository.schema_version(), 19)

    def test_metrics_include_communication_counters(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/statistics', token=token)
        metrics = self.invoke('/api/metrics', token=token)
        snapshot = metrics.body_json()['metrics']
        self.assertGreaterEqual(snapshot.get('communication_requests_total', 0), 1)

class ReleaseProgramKV17TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v17_table_communication_messages(self) -> None:
        self.assertIn('communication_messages', self._table_names())

    def test_v17_table_communication_threads(self) -> None:
        self.assertIn('communication_threads', self._table_names())

    def test_v17_table_communication_channels(self) -> None:
        self.assertIn('communication_channels', self._table_names())

    def test_v17_table_communication_recipients(self) -> None:
        self.assertIn('communication_recipients', self._table_names())

    def test_v17_table_communication_groups(self) -> None:
        self.assertIn('communication_groups', self._table_names())

    def test_v17_table_communication_events(self) -> None:
        self.assertIn('communication_events', self._table_names())

    def test_v17_table_communication_logs(self) -> None:
        self.assertIn('communication_logs', self._table_names())

    def test_v17_table_communication_history(self) -> None:
        self.assertIn('communication_history', self._table_names())

    def test_v17_table_communication_archives(self) -> None:
        self.assertIn('communication_archives', self._table_names())

    def test_v17_table_communication_metadata(self) -> None:
        self.assertIn('communication_metadata', self._table_names())

    def test_v17_table_notification_events(self) -> None:
        self.assertIn('notification_events', self._table_names())

    def test_v17_table_notification_rules(self) -> None:
        self.assertIn('notification_rules', self._table_names())

    def test_v17_table_notification_templates(self) -> None:
        self.assertIn('notification_templates', self._table_names())

    def test_v17_table_notification_preferences(self) -> None:
        self.assertIn('notification_preferences', self._table_names())

    def test_v17_table_notification_deliveries(self) -> None:
        self.assertIn('notification_deliveries', self._table_names())

    def test_v17_table_notification_batches(self) -> None:
        self.assertIn('notification_batches', self._table_names())

    def test_v17_table_notification_acknowledgements(self) -> None:
        self.assertIn('notification_acknowledgements', self._table_names())

    def test_v17_table_notification_failures(self) -> None:
        self.assertIn('notification_failures', self._table_names())

    def test_v17_table_notification_statistics(self) -> None:
        self.assertIn('notification_statistics', self._table_names())

    def test_v17_table_notification_queue(self) -> None:
        self.assertIn('notification_queue', self._table_names())

    def test_v17_table_email_accounts(self) -> None:
        self.assertIn('email_accounts', self._table_names())

    def test_v17_table_email_templates(self) -> None:
        self.assertIn('email_templates', self._table_names())

    def test_v17_table_email_messages(self) -> None:
        self.assertIn('email_messages', self._table_names())

    def test_v17_table_email_attachments(self) -> None:
        self.assertIn('email_attachments', self._table_names())

    def test_v17_table_email_threads(self) -> None:
        self.assertIn('email_threads', self._table_names())

    def test_v17_table_email_delivery_logs(self) -> None:
        self.assertIn('email_delivery_logs', self._table_names())

    def test_v17_table_email_statistics(self) -> None:
        self.assertIn('email_statistics', self._table_names())

    def test_v17_table_email_bounces(self) -> None:
        self.assertIn('email_bounces', self._table_names())

    def test_v17_table_email_click_tracking(self) -> None:
        self.assertIn('email_click_tracking', self._table_names())

    def test_v17_table_email_open_tracking(self) -> None:
        self.assertIn('email_open_tracking', self._table_names())

    def test_v17_table_sms_templates(self) -> None:
        self.assertIn('sms_templates', self._table_names())

    def test_v17_table_sms_messages(self) -> None:
        self.assertIn('sms_messages', self._table_names())

    def test_v17_table_sms_delivery_logs(self) -> None:
        self.assertIn('sms_delivery_logs', self._table_names())

    def test_v17_table_sms_statistics(self) -> None:
        self.assertIn('sms_statistics', self._table_names())

    def test_v17_table_sms_providers(self) -> None:
        self.assertIn('sms_providers', self._table_names())

    def test_v17_table_sms_queue(self) -> None:
        self.assertIn('sms_queue', self._table_names())

    def test_v17_table_whatsapp_accounts(self) -> None:
        self.assertIn('whatsapp_accounts', self._table_names())

    def test_v17_table_whatsapp_templates(self) -> None:
        self.assertIn('whatsapp_templates', self._table_names())

    def test_v17_table_whatsapp_messages(self) -> None:
        self.assertIn('whatsapp_messages', self._table_names())

    def test_v17_table_whatsapp_media(self) -> None:
        self.assertIn('whatsapp_media', self._table_names())

    def test_v17_table_whatsapp_sessions(self) -> None:
        self.assertIn('whatsapp_sessions', self._table_names())

    def test_v17_table_whatsapp_delivery_logs(self) -> None:
        self.assertIn('whatsapp_delivery_logs', self._table_names())

    def test_v17_table_whatsapp_statistics(self) -> None:
        self.assertIn('whatsapp_statistics', self._table_names())

    def test_v17_table_telegram_bots(self) -> None:
        self.assertIn('telegram_bots', self._table_names())

    def test_v17_table_telegram_messages(self) -> None:
        self.assertIn('telegram_messages', self._table_names())

    def test_v17_table_telegram_updates(self) -> None:
        self.assertIn('telegram_updates', self._table_names())

    def test_v17_table_telegram_statistics(self) -> None:
        self.assertIn('telegram_statistics', self._table_names())

    def test_v17_table_push_devices(self) -> None:
        self.assertIn('push_devices', self._table_names())

    def test_v17_table_push_notifications(self) -> None:
        self.assertIn('push_notifications', self._table_names())

    def test_v17_table_push_delivery_logs(self) -> None:
        self.assertIn('push_delivery_logs', self._table_names())

    def test_v17_table_push_subscriptions(self) -> None:
        self.assertIn('push_subscriptions', self._table_names())

    def test_v17_table_push_statistics(self) -> None:
        self.assertIn('push_statistics', self._table_names())

    def test_v17_table_inapp_notifications(self) -> None:
        self.assertIn('inapp_notifications', self._table_names())

    def test_v17_table_inapp_categories(self) -> None:
        self.assertIn('inapp_categories', self._table_names())

    def test_v17_table_inapp_read_status(self) -> None:
        self.assertIn('inapp_read_status', self._table_names())

    def test_v17_table_inapp_statistics(self) -> None:
        self.assertIn('inapp_statistics', self._table_names())

    def test_v17_table_campaigns(self) -> None:
        self.assertIn('campaigns', self._table_names())

    def test_v17_table_campaign_channels(self) -> None:
        self.assertIn('campaign_channels', self._table_names())

    def test_v17_table_campaign_audiences(self) -> None:
        self.assertIn('campaign_audiences', self._table_names())

    def test_v17_table_campaign_segments(self) -> None:
        self.assertIn('campaign_segments', self._table_names())

    def test_v17_table_campaign_executions(self) -> None:
        self.assertIn('campaign_executions', self._table_names())

    def test_v17_table_campaign_statistics(self) -> None:
        self.assertIn('campaign_statistics', self._table_names())

    def test_v17_table_campaign_results(self) -> None:
        self.assertIn('campaign_results', self._table_names())

    def test_v17_table_campaign_logs(self) -> None:
        self.assertIn('campaign_logs', self._table_names())

    def test_v17_table_queue_jobs(self) -> None:
        self.assertIn('queue_jobs', self._table_names())

    def test_v17_table_queue_workers(self) -> None:
        self.assertIn('queue_workers', self._table_names())

    def test_v17_table_queue_failures(self) -> None:
        self.assertIn('queue_failures', self._table_names())

    def test_v17_table_queue_retry_history(self) -> None:
        self.assertIn('queue_retry_history', self._table_names())

    def test_v17_table_queue_batches(self) -> None:
        self.assertIn('queue_batches', self._table_names())

    def test_v17_table_template_categories(self) -> None:
        self.assertIn('template_categories', self._table_names())

    def test_v17_table_template_versions(self) -> None:
        self.assertIn('template_versions', self._table_names())

    def test_v17_table_template_variables(self) -> None:
        self.assertIn('template_variables', self._table_names())

    def test_v17_table_template_translations(self) -> None:
        self.assertIn('template_translations', self._table_names())

    def test_v17_table_communication_preferences(self) -> None:
        self.assertIn('communication_preferences', self._table_names())

    def test_v17_table_communication_consent_history(self) -> None:
        self.assertIn('communication_consent_history', self._table_names())

    def test_v17_table_communication_blacklists(self) -> None:
        self.assertIn('communication_blacklists', self._table_names())

    def test_v17_table_communication_whitelists(self) -> None:
        self.assertIn('communication_whitelists', self._table_names())

    def test_v17_table_communication_quiet_hours(self) -> None:
        self.assertIn('communication_quiet_hours', self._table_names())

    def test_v17_table_communication_dashboard_snapshots(self) -> None:
        self.assertIn('communication_dashboard_snapshots', self._table_names())

    def test_v17_table_communication_analytics(self) -> None:
        self.assertIn('communication_analytics', self._table_names())

    def test_v17_table_communication_ai_recommendations(self) -> None:
        self.assertIn('communication_ai_recommendations', self._table_names())

class ReleaseProgramKIntegrationTests(LawimTestHarness):
    def test_program_a_projects_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/projects', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_b_partners_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/partners', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_d_assistant_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/assistant/agents', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_e_knowledge_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/knowledge/documents', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_f_workflow_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/workflows/instances', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_g_rei_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/properties', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_h_crm_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/crm/contacts', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_i_marketplace_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/marketplace/providers', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_j_security_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        response = self.invoke('/api/v2/security/roles', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_program_c_decisions_route_still_works(self) -> None:
        token = self.login(email='agent@lawim.local')
        project_id = int(self.invoke('/api/v2/projects?limit=1', token=token).body_json()['projects'][0]['id'])
        response = self.invoke(f'/api/v2/decisions?project_id={project_id}', token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_integration_sources_include_security(self) -> None:
        payload = self.repository.integration_sources()
        self.assertTrue(payload['programs']['security'])

    def test_integration_sources_include_crm(self) -> None:
        payload = self.repository.integration_sources()
        self.assertTrue(payload['programs']['crm'])

    def test_integration_sources_engine_sources(self) -> None:
        payload = self.repository.integration_sources()
        self.assertIn('marketplace', payload['sources'])

class ReleaseProgramKObservabilityTests(LawimTestHarness):
    def _admin_metrics(self) -> dict[str, object]:
        return self.invoke('/api/metrics', token=self.login(email='admin@lawim.local')).body_json()['metrics']

    def test_communication_stats_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/statistics', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_messages_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/messages', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_channels_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/channels', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_dashboard_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/dashboard', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_analytics_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/analytics', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_notifications_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/notifications', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_queue_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/queue', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_communication_email_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/email', token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('communication_requests_total', 0), 1)

    def test_email_messages_total_counter(self) -> None:
        token = self.login(email='admin@lawim.local')
        self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'email', 'to_email': 'metrics@example.com', 'subject': 'M', 'body': 'B'})
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get('email_messages_total', 0), 1)

class ReleaseProgramKChannelTests(LawimTestHarness):
    def test_email_stub_send_sent(self) -> None:
        result = EmailEngine().stub_send(EmailEngine().build_payload(to_email='c@example.com', subject='S', body='B'))
        self.assertTrue(result['sent'])

    def test_sms_stub_send_sent(self) -> None:
        result = SmsEngine().stub_send(SmsEngine().build_payload(to_number='+237600000000', body='SMS'))
        self.assertTrue(result['sent'])

    def test_whatsapp_stub_send_sent(self) -> None:
        result = WhatsappEngine().stub_send(WhatsappEngine().build_payload(to_number='+237600000000', body='WA'))
        self.assertTrue(result['sent'])

    def test_telegram_stub_send_sent(self) -> None:
        result = TelegramEngine().stub_send(TelegramEngine().build_payload(chat_id='99', body='TG'))
        self.assertTrue(result['sent'])

    def test_push_stub_send_sent(self) -> None:
        result = PushEngine().stub_send(PushEngine().build_payload(title='T', body='B'))
        self.assertTrue(result['sent'])

    def test_repository_send_email(self) -> None:
        result = self.repository.send_email(to_email='repo@example.com', subject='S', body='B')
        self.assertIn('message_key', result)

    def test_repository_send_sms(self) -> None:
        result = self.repository.send_sms(to_number='+237600000001', body='SMS')
        self.assertIn('message_key', result)

    def test_repository_send_whatsapp(self) -> None:
        result = self.repository.send_whatsapp(to_number='+237600000002', body='WA')
        self.assertIn('message_key', result)

    def test_repository_send_telegram(self) -> None:
        result = self.repository.send_telegram(chat_id='chat-1', body='TG')
        self.assertIn('message_key', result)

    def test_repository_send_push(self) -> None:
        result = self.repository.send_push(title='Push', body='Body')
        self.assertIn('notification_key', result)

    def test_api_send_email(self) -> None:
        token = self.login(email='admin@lawim.local')
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'email', 'to_email': 'api-send@example.com', 'subject': 'S', 'body': 'B'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_api_send_sms(self) -> None:
        token = self.login(email='admin@lawim.local')
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'sms', 'to_number': '+237600000003', 'body': 'SMS'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_api_send_whatsapp(self) -> None:
        token = self.login(email='admin@lawim.local')
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'whatsapp', 'to_number': '+237600000004', 'body': 'WA'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_api_send_telegram(self) -> None:
        token = self.login(email='admin@lawim.local')
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'telegram', 'chat_id': '555', 'body': 'TG'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

    def test_api_send_push(self) -> None:
        token = self.login(email='admin@lawim.local')
        response = self.invoke('/api/v2/communication/messages/send', method='POST', token=token, body={'channel_type': 'push', 'title': 'T', 'body': 'Push'})
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})

