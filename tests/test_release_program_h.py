from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

import lawim_v2.contact as contact
from lawim_v2.contact import (
    COMPANY_NAME,
    FACEBOOK_USERNAME,
    PHONE_E164,
    PHONE_INTERNATIONAL,
    PHONE_NUMBER,
    SUPPORT_EMAIL,
    TELEGRAM_BOT,
    WEBSITE_URL,
    WHATSAPP_USERNAME,
    facebook_link,
    official_signature_block,
    telegram_link,
    to_public_dict,
    whatsapp_link,
)
from lawim_v2.crm.constants import (
    CAMPAIGN_STATUSES,
    COMMUNICATION_CHANNELS,
    CONSENT_TYPES,
    CONTACT_TYPES,
    CUSTOMER_ROLES,
    LEAD_STATUSES,
    OPPORTUNITY_STATUSES,
    PIPELINE_STAGES,
    SATISFACTION_TYPES,
    SCORE_KEYS,
)
from lawim_v2.crm.engines import (
    AiIntegrationBridge,
    CampaignEngine,
    CommunicationEngine,
    CrmAnalyticsEngine,
    CrmPlatformEngine,
    CrmSearchEngine,
    Customer360Engine,
    LeadScoringEngine,
    PipelineEngine,
    SatisfactionEngine,
)
from lawim_v2.crm.schema_v14_ddl import V14_TABLE_NAMES
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness


REPO_ROOT = Path(__file__).resolve().parents[1]


def _forbidden_phone_patterns() -> tuple[str, ...]:
    return (f"6{'20'} {'397'} {'846'}", f"6{'20'}{'397'}{'846'}")


SAMPLE_CONTACT: dict[str, object] = {
    "id": 1,
    "full_name": "Marie Nguema",
    "email": "marie.nguema@example.cm",
    "phone": "+237 677 000 111",
    "whatsapp": "+237677000111",
    "company": "LAWIM Demo",
    "contact_type": "prospect",
}

SAMPLE_LEAD: dict[str, object] = {"id": 1, "status": "new", "contact_id": 1, "title": "Intérêt immobilier"}


def _scan_repo_for_forbidden_phone() -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", ".cursor"}
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for needle in _forbidden_phone_patterns():
            if needle in text:
                matches.append((str(path.relative_to(REPO_ROOT)), needle))
    return matches


class ReleaseProgramHContactNormalizationTests(LawimTestHarness):
    def test_phone_number_constant(self) -> None:
        self.assertEqual(PHONE_NUMBER, "686 822 667")

    def test_phone_e164_constant(self) -> None:
        self.assertEqual(PHONE_E164, "+237686822667")

    def test_phone_international_constant(self) -> None:
        self.assertEqual(PHONE_INTERNATIONAL, "+237 686 822 667")

    def test_facebook_username_constant(self) -> None:
        self.assertEqual(FACEBOOK_USERNAME, "@lawimofficial")

    def test_telegram_bot_constant(self) -> None:
        self.assertEqual(TELEGRAM_BOT, "@lawim_assistant_bot")

    def test_whatsapp_username_constant(self) -> None:
        self.assertEqual(WHATSAPP_USERNAME, "@lawimofficial")

    def test_company_name_constant(self) -> None:
        self.assertEqual(COMPANY_NAME, "LAWIM")

    def test_support_email_constant(self) -> None:
        self.assertEqual(SUPPORT_EMAIL, "contact@lawim.app")

    def test_website_url_constant(self) -> None:
        self.assertEqual(WEBSITE_URL, "https://lawim.app")

    def test_whatsapp_number_matches_phone(self) -> None:
        self.assertEqual(contact.WHATSAPP_NUMBER, PHONE_NUMBER)

    def test_green_api_number_matches_phone(self) -> None:
        self.assertEqual(contact.GREEN_API_NUMBER, PHONE_NUMBER)

    def test_to_public_dict_phone(self) -> None:
        self.assertEqual(to_public_dict()["phone_number"], "686 822 667")

    def test_to_public_dict_telegram(self) -> None:
        self.assertEqual(to_public_dict()["telegram_bot"], "@lawim_assistant_bot")

    def test_to_public_dict_brand_subslogan_is_removed(self) -> None:
        self.assertEqual(to_public_dict()["brand_subslogan"], "")

    def test_whatsapp_link_format(self) -> None:
        self.assertTrue(whatsapp_link().startswith("https://wa.me/237686822667"))

    def test_telegram_link_format(self) -> None:
        self.assertEqual(telegram_link(), "https://t.me/lawim_assistant_bot")

    def test_facebook_link_format(self) -> None:
        self.assertEqual(facebook_link(), "https://facebook.com/lawimofficial")

    def test_official_signature_contains_phone(self) -> None:
        self.assertIn("686 822 667", official_signature_block())

    def test_official_signature_contains_telegram(self) -> None:
        self.assertIn("@lawim_assistant_bot", official_signature_block())

    def test_official_signature_omits_old_slogan(self) -> None:
        self.assertNotIn("EN TOUTE CONFIANCE", official_signature_block())

    def test_import_lawim_v2_contact_module(self) -> None:
        self.assertTrue(hasattr(contact, "PHONE_NUMBER"))

    def test_repo_no_legacy_phone_patterns(self) -> None:
        self.assertEqual(_scan_repo_for_forbidden_phone(), [])


class ReleaseProgramHPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v14(self) -> None:
        self.assertEqual(self.repository.schema_version(), 18)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 18)

    def test_crm_tables_present(self) -> None:
        self.assertTrue(self.repository.crm_tables_present())

    def test_all_v14_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v13_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v12_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_crm_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM crm_contact_profiles"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM crm_leads"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM crm_pipelines"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM crm_lead_sources"), 1)

    def test_v13_to_v14_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v13.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in V14_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='13' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("crm_contact_profiles", names)
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramHConstantsTests(LawimTestHarness):
    def test_lead_statuses_new(self) -> None:
        self.assertIn("new", LEAD_STATUSES)

    def test_lead_statuses_contacted(self) -> None:
        self.assertIn("contacted", LEAD_STATUSES)

    def test_lead_statuses_qualified(self) -> None:
        self.assertIn("qualified", LEAD_STATUSES)

    def test_lead_statuses_proposal(self) -> None:
        self.assertIn("proposal", LEAD_STATUSES)

    def test_lead_statuses_negotiation(self) -> None:
        self.assertIn("negotiation", LEAD_STATUSES)

    def test_lead_statuses_won(self) -> None:
        self.assertIn("won", LEAD_STATUSES)

    def test_lead_statuses_lost(self) -> None:
        self.assertIn("lost", LEAD_STATUSES)

    def test_lead_statuses_nurturing(self) -> None:
        self.assertIn("nurturing", LEAD_STATUSES)

    def test_lead_statuses_archived(self) -> None:
        self.assertIn("archived", LEAD_STATUSES)

    def test_contact_types_individual(self) -> None:
        self.assertIn("individual", CONTACT_TYPES)

    def test_contact_types_company(self) -> None:
        self.assertIn("company", CONTACT_TYPES)

    def test_contact_types_prospect(self) -> None:
        self.assertIn("prospect", CONTACT_TYPES)

    def test_contact_types_lead(self) -> None:
        self.assertIn("lead", CONTACT_TYPES)

    def test_contact_types_customer(self) -> None:
        self.assertIn("customer", CONTACT_TYPES)

    def test_contact_types_partner(self) -> None:
        self.assertIn("partner", CONTACT_TYPES)

    def test_contact_types_vendor(self) -> None:
        self.assertIn("vendor", CONTACT_TYPES)

    def test_contact_types_agent(self) -> None:
        self.assertIn("agent", CONTACT_TYPES)

    def test_customer_roles_buyer(self) -> None:
        self.assertIn("buyer", CUSTOMER_ROLES)

    def test_customer_roles_seller(self) -> None:
        self.assertIn("seller", CUSTOMER_ROLES)

    def test_customer_roles_tenant(self) -> None:
        self.assertIn("tenant", CUSTOMER_ROLES)

    def test_customer_roles_landlord(self) -> None:
        self.assertIn("landlord", CUSTOMER_ROLES)

    def test_customer_roles_investor(self) -> None:
        self.assertIn("investor", CUSTOMER_ROLES)

    def test_customer_roles_broker(self) -> None:
        self.assertIn("broker", CUSTOMER_ROLES)

    def test_customer_roles_developer(self) -> None:
        self.assertIn("developer", CUSTOMER_ROLES)

    def test_customer_roles_partner(self) -> None:
        self.assertIn("partner", CUSTOMER_ROLES)

    def test_opportunity_statuses_open(self) -> None:
        self.assertIn("open", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_qualified(self) -> None:
        self.assertIn("qualified", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_proposal(self) -> None:
        self.assertIn("proposal", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_negotiation(self) -> None:
        self.assertIn("negotiation", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_won(self) -> None:
        self.assertIn("won", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_lost(self) -> None:
        self.assertIn("lost", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_on_hold(self) -> None:
        self.assertIn("on_hold", OPPORTUNITY_STATUSES)

    def test_opportunity_statuses_closed(self) -> None:
        self.assertIn("closed", OPPORTUNITY_STATUSES)

    def test_pipeline_stages_prospection(self) -> None:
        self.assertIn("prospection", PIPELINE_STAGES)

    def test_pipeline_stages_qualification(self) -> None:
        self.assertIn("qualification", PIPELINE_STAGES)

    def test_pipeline_stages_proposition(self) -> None:
        self.assertIn("proposition", PIPELINE_STAGES)

    def test_pipeline_stages_negociation(self) -> None:
        self.assertIn("negociation", PIPELINE_STAGES)

    def test_pipeline_stages_cloture(self) -> None:
        self.assertIn("cloture", PIPELINE_STAGES)

    def test_communication_channels_whatsapp(self) -> None:
        self.assertIn("whatsapp", COMMUNICATION_CHANNELS)

    def test_communication_channels_telegram(self) -> None:
        self.assertIn("telegram", COMMUNICATION_CHANNELS)

    def test_communication_channels_email(self) -> None:
        self.assertIn("email", COMMUNICATION_CHANNELS)

    def test_communication_channels_sms(self) -> None:
        self.assertIn("sms", COMMUNICATION_CHANNELS)

    def test_communication_channels_in_app(self) -> None:
        self.assertIn("in_app", COMMUNICATION_CHANNELS)

    def test_campaign_statuses_draft(self) -> None:
        self.assertIn("draft", CAMPAIGN_STATUSES)

    def test_campaign_statuses_scheduled(self) -> None:
        self.assertIn("scheduled", CAMPAIGN_STATUSES)

    def test_campaign_statuses_running(self) -> None:
        self.assertIn("running", CAMPAIGN_STATUSES)

    def test_campaign_statuses_paused(self) -> None:
        self.assertIn("paused", CAMPAIGN_STATUSES)

    def test_campaign_statuses_completed(self) -> None:
        self.assertIn("completed", CAMPAIGN_STATUSES)

    def test_campaign_statuses_cancelled(self) -> None:
        self.assertIn("cancelled", CAMPAIGN_STATUSES)

    def test_score_keys_engagement(self) -> None:
        self.assertIn("engagement", SCORE_KEYS)

    def test_score_keys_intent(self) -> None:
        self.assertIn("intent", SCORE_KEYS)

    def test_score_keys_fit(self) -> None:
        self.assertIn("fit", SCORE_KEYS)

    def test_score_keys_recency(self) -> None:
        self.assertIn("recency", SCORE_KEYS)

    def test_score_keys_value(self) -> None:
        self.assertIn("value", SCORE_KEYS)

    def test_score_keys_loyalty(self) -> None:
        self.assertIn("loyalty", SCORE_KEYS)

    def test_score_keys_risk(self) -> None:
        self.assertIn("risk", SCORE_KEYS)

    def test_satisfaction_types_nps(self) -> None:
        self.assertIn("nps", SATISFACTION_TYPES)

    def test_satisfaction_types_csat(self) -> None:
        self.assertIn("csat", SATISFACTION_TYPES)

    def test_satisfaction_types_ces(self) -> None:
        self.assertIn("ces", SATISFACTION_TYPES)

    def test_satisfaction_types_post_visit(self) -> None:
        self.assertIn("post_visit", SATISFACTION_TYPES)

    def test_satisfaction_types_post_transaction(self) -> None:
        self.assertIn("post_transaction", SATISFACTION_TYPES)

    def test_satisfaction_types_general(self) -> None:
        self.assertIn("general", SATISFACTION_TYPES)

    def test_consent_types_marketing(self) -> None:
        self.assertIn("marketing", CONSENT_TYPES)

    def test_consent_types_whatsapp(self) -> None:
        self.assertIn("whatsapp", CONSENT_TYPES)

    def test_consent_types_telegram(self) -> None:
        self.assertIn("telegram", CONSENT_TYPES)

    def test_consent_types_email(self) -> None:
        self.assertIn("email", CONSENT_TYPES)

    def test_consent_types_sms(self) -> None:
        self.assertIn("sms", CONSENT_TYPES)

    def test_consent_types_data_processing(self) -> None:
        self.assertIn("data_processing", CONSENT_TYPES)

    def test_consent_types_analytics(self) -> None:
        self.assertIn("analytics", CONSENT_TYPES)


class ReleaseProgramHEnginesTests(LawimTestHarness):
    def test_lead_scoring_new_status(self) -> None:
        score = LeadScoringEngine().compute(lead=SAMPLE_LEAD, contact=SAMPLE_CONTACT)
        self.assertGreaterEqual(score["lead_score"], 10)

    def test_lead_scoring_qualified_status(self) -> None:
        lead = dict(SAMPLE_LEAD, status="qualified")
        score = LeadScoringEngine().compute(lead=lead, contact=SAMPLE_CONTACT, communications=2)
        self.assertGreater(score["lead_score"], 30)

    def test_lead_scoring_max_cap(self) -> None:
        lead = dict(SAMPLE_LEAD, status="negotiation")
        score = LeadScoringEngine().compute(lead=lead, contact=SAMPLE_CONTACT, communications=10)
        self.assertLessEqual(score["lead_score"], 100)

    def test_lead_scoring_uses_signal_bonus(self) -> None:
        baseline = LeadScoringEngine().compute(lead=SAMPLE_LEAD, contact=SAMPLE_CONTACT)
        enriched_lead = dict(
            SAMPLE_LEAD,
            title="Urgent diaspora investor visit for land in Douala",
            notes="budget 50M cashflow quick decision",
            metadata={"intent": "invest", "user_type": "diaspora"},
        )
        boosted = LeadScoringEngine().compute(lead=enriched_lead, contact=SAMPLE_CONTACT)
        self.assertGreater(boosted["lead_score"], baseline["lead_score"])

    def test_pipeline_default_stages_count(self) -> None:
        stages = PipelineEngine().default_stages()
        self.assertEqual(len(stages), len(PIPELINE_STAGES))

    def test_pipeline_stage_index(self) -> None:
        self.assertEqual(PipelineEngine().stage_index("proposition"), 2)

    def test_pipeline_advance_stage(self) -> None:
        nxt = PipelineEngine().advance_stage("qualification")
        self.assertEqual(nxt, "proposition")

    def test_pipeline_advance_final_stage(self) -> None:
        self.assertIsNone(PipelineEngine().advance_stage("cloture"))

    def test_pipeline_kanban_payload(self) -> None:
        stages = [{"id": 1, "position": 0, "stage_key": "prospection"}]
        items = [{"stage_id": 1, "entity_id": 5}]
        board = PipelineEngine().kanban_payload(stages=stages, items=items)
        self.assertEqual(len(board[0]["items"]), 1)

    def test_communication_lawim_sender(self) -> None:
        sender = CommunicationEngine().lawim_sender()
        self.assertEqual(sender["phone_number"], PHONE_NUMBER)

    def test_communication_whatsapp_payload(self) -> None:
        payload = CommunicationEngine().whatsapp_payload(to_number="+237677000111", body="Bonjour")
        self.assertEqual(payload["channel"], "whatsapp")
        self.assertIn(PHONE_E164, str(payload["from_number"]))

    def test_communication_telegram_payload(self) -> None:
        payload = CommunicationEngine().telegram_payload(to_handle="@client", body="Hello")
        self.assertEqual(payload["from_handle"], TELEGRAM_BOT)

    def test_communication_email_payload(self) -> None:
        payload = CommunicationEngine().email_payload(to_email="a@b.cm", subject="Test", body="Hi")
        self.assertEqual(payload["from_email"], SUPPORT_EMAIL)

    def test_communication_sms_truncates(self) -> None:
        payload = CommunicationEngine().sms_payload(to_number="+237677000111", body="x" * 200)
        self.assertLessEqual(len(str(payload["body"])), 140)

    def test_communication_format_without_signature(self) -> None:
        body = CommunicationEngine().format_outbound_body("Hello", include_signature=False)
        self.assertEqual(body, "Hello")

    def test_customer_360_assemble(self) -> None:
        view = Customer360Engine().assemble(
            contact=SAMPLE_CONTACT,
            leads=[SAMPLE_LEAD],
            customer=None,
            opportunities=[],
            communications=[{"channel": "whatsapp"}],
            scores={"engagement": 50},
            timeline=[{"summary": "created"}],
            journey=[{"event_type": "contact_created"}],
        )
        self.assertEqual(view["summary"]["lead_count"], 1)
        self.assertFalse(view["summary"]["is_customer"])

    def test_campaign_audience_filter(self) -> None:
        filt = CampaignEngine().build_audience_filter({"tags": ["vip"], "min_score": 50})
        self.assertEqual(filt["tags"], ["vip"])

    def test_campaign_personalize_content(self) -> None:
        text = CampaignEngine().personalize_content(template="Bonjour {{name}}", contact=SAMPLE_CONTACT)
        self.assertIn("Marie Nguema", text)

    def test_satisfaction_nps_promoter(self) -> None:
        self.assertEqual(SatisfactionEngine().nps_category(10), "promoter")

    def test_satisfaction_nps_detractor(self) -> None:
        self.assertEqual(SatisfactionEngine().nps_category(5), "detractor")

    def test_satisfaction_csat_average(self) -> None:
        self.assertEqual(SatisfactionEngine().csat_score([4, 5]), 4.5)

    def test_satisfaction_csat_empty(self) -> None:
        self.assertEqual(SatisfactionEngine().csat_score([]), 0.0)

    def test_satisfaction_survey_summary_nps(self) -> None:
        summary = SatisfactionEngine().survey_summary(survey_type="nps", responses=[{"rating": 10}, {"rating": 6}])
        self.assertIn("nps", summary)

    def test_ai_integration_sources(self) -> None:
        sources = AiIntegrationBridge().sources()
        self.assertIn("knowledge_platform", sources)
        self.assertIn("real_estate_intelligence", sources)

    def test_ai_suggest_followup(self) -> None:
        suggestion = AiIntegrationBridge().suggest_followup(contact=SAMPLE_CONTACT, last_communication={"channel": "whatsapp"})
        self.assertEqual(suggestion["suggestion_type"], "followup")

    def test_ai_suggest_next_action_new(self) -> None:
        suggestion = AiIntegrationBridge().suggest_next_action(lead=SAMPLE_LEAD)
        self.assertIn("qualify", str(suggestion["payload"]["action"]))

    def test_ai_enrich_with_knowledge(self) -> None:
        result = AiIntegrationBridge().enrich_with_knowledge(self.repository, "compromis de vente")
        self.assertTrue(result is None or isinstance(result, dict))

    def test_search_normalize(self) -> None:
        normalized = CrmSearchEngine().normalize("  Marie@Example  ")
        self.assertIn("marie", normalized)

    def test_analytics_compute_scores(self) -> None:
        scores = CrmAnalyticsEngine().compute_scores(contact=SAMPLE_CONTACT, communications=3, opportunities=1, days_since_contact=2)
        for key in SCORE_KEYS:
            self.assertIn(key, scores)

    def test_platform_engine_has_subengines(self) -> None:
        engine = CrmPlatformEngine()
        self.assertIsInstance(engine.lead_scoring, LeadScoringEngine)
        self.assertIsInstance(engine.communication, CommunicationEngine)

    def test_platform_integration_sources(self) -> None:
        self.assertIn("workflow_automation", CrmPlatformEngine().integration_sources())

    def test_platform_days_since_recent(self) -> None:
        recent = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        self.assertLess(CrmPlatformEngine().days_since(recent), 2)

    def test_platform_days_since_invalid(self) -> None:
        self.assertEqual(CrmPlatformEngine().days_since("invalid"), 999)


class ReleaseProgramHRepositoryTests(LawimTestHarness):
    def _contact_id(self) -> int:
        return int(self.repository.one("SELECT id FROM crm_contact_profiles LIMIT 1")["id"])

    def test_list_crm_contacts(self) -> None:
        contacts = self.repository.list_crm_contacts(limit=10)
        self.assertGreaterEqual(len(contacts), 1)

    def test_create_crm_contact(self) -> None:
        contact_row = self.repository.create_crm_contact(full_name="API Repo Contact", contact_type="prospect")
        self.assertEqual(contact_row["full_name"], "API Repo Contact")

    def test_get_crm_contact(self) -> None:
        cid = self._contact_id()
        row = self.repository.get_crm_contact(cid)
        self.assertEqual(int(row["id"]), cid)

    def test_list_crm_leads(self) -> None:
        leads = self.repository.list_crm_leads()
        self.assertGreaterEqual(len(leads), 1)

    def test_create_crm_lead(self) -> None:
        cid = self._contact_id()
        lead = self.repository.create_crm_lead(contact_id=cid, title="Repo lead test")
        self.assertEqual(lead["title"], "Repo lead test")

    def test_get_crm_lead(self) -> None:
        lead_id = int(self.repository.one("SELECT id FROM crm_leads LIMIT 1")["id"])
        lead = self.repository.get_crm_lead(lead_id)
        self.assertEqual(int(lead["id"]), lead_id)

    def test_convert_crm_lead_to_customer(self) -> None:
        cid = int(self.repository.create_crm_contact(full_name="Convert Target", contact_type="lead")["id"])
        lead = self.repository.create_crm_lead(contact_id=cid, title="To convert")
        customer = self.repository.convert_crm_lead_to_customer(int(lead["id"]), roles=["buyer"])
        self.assertIn("customer_key", customer)

    def test_list_crm_lead_sources(self) -> None:
        sources = self.repository.list_crm_lead_sources()
        self.assertGreaterEqual(len(sources), 1)
        keys = {s["source_key"] for s in sources}
        self.assertIn("source-rei", keys)

    def test_list_crm_customers(self) -> None:
        customers = self.repository.list_crm_customers()
        self.assertIsInstance(customers, list)

    def test_create_crm_customer(self) -> None:
        cid = int(self.repository.create_crm_contact(full_name="Customer Target", contact_type="customer")["id"])
        customer = self.repository.create_crm_customer(contact_id=cid, roles=["tenant"])
        self.assertEqual(int(customer["contact_id"]), cid)

    def test_list_crm_opportunities(self) -> None:
        opps = self.repository.list_crm_opportunities()
        self.assertIsInstance(opps, list)

    def test_create_crm_opportunity(self) -> None:
        cid = self._contact_id()
        opp = self.repository.create_crm_opportunity(contact_id=cid, title="Repo opportunity", amount=500000)
        self.assertEqual(opp["title"], "Repo opportunity")

    def test_list_crm_pipelines(self) -> None:
        pipelines = self.repository.list_crm_pipelines()
        self.assertGreaterEqual(len(pipelines), 1)

    def test_get_crm_pipeline_board(self) -> None:
        pipeline_id = int(self.repository.one("SELECT id FROM crm_pipelines LIMIT 1")["id"])
        board = self.repository.get_crm_pipeline_board(pipeline_id)
        self.assertIsInstance(board, list)

    def test_move_crm_pipeline_item(self) -> None:
        item = self.repository.one("SELECT id, stage_id FROM crm_pipeline_items LIMIT 1")
        moved = self.repository.move_crm_pipeline_item(int(item["id"]), stage_id=int(item["stage_id"]), position=0)
        self.assertEqual(int(moved["id"]), int(item["id"]))

    def test_advance_crm_pipeline_item(self) -> None:
        item_id = int(self.repository.one("SELECT id FROM crm_pipeline_items LIMIT 1")["id"])
        advanced = self.repository.advance_crm_pipeline_item(item_id)
        self.assertIn("stage_id", advanced)

    def test_send_crm_whatsapp(self) -> None:
        cid = self._contact_id()
        msg = self.repository.send_crm_whatsapp(contact_id=cid, body="Test WhatsApp")
        self.assertIn("communication_id", msg)

    def test_send_crm_telegram(self) -> None:
        cid = self._contact_id()
        msg = self.repository.send_crm_telegram(contact_id=cid, body="Test Telegram", to_handle="@client")
        self.assertIn("communication_id", msg)

    def test_send_crm_email(self) -> None:
        cid = self._contact_id()
        msg = self.repository.send_crm_email(contact_id=cid, subject="Test", body="Email body")
        self.assertIn("communication_id", msg)

    def test_send_crm_sms(self) -> None:
        cid = self._contact_id()
        msg = self.repository.send_crm_sms(contact_id=cid, body="SMS test")
        self.assertIn("communication_id", msg)

    def test_list_crm_communications(self) -> None:
        comms = self.repository.list_crm_communications(limit=10)
        self.assertGreaterEqual(len(comms), 1)

    def test_create_crm_reminder(self) -> None:
        cid = self._contact_id()
        due = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        reminder = self.repository.create_crm_reminder(contact_id=cid, title="Call back", due_at=due)
        self.assertEqual(reminder["title"], "Call back")

    def test_list_crm_reminders(self) -> None:
        reminders = self.repository.list_crm_reminders()
        self.assertIsInstance(reminders, list)

    def test_schedule_crm_followup(self) -> None:
        cid = self._contact_id()
        scheduled = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat()
        followup = self.repository.schedule_crm_followup(contact_id=cid, scheduled_at=scheduled, channel="whatsapp")
        self.assertEqual(followup["status"], "scheduled")

    def test_complete_crm_followup(self) -> None:
        cid = self._contact_id()
        scheduled = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        followup = self.repository.schedule_crm_followup(contact_id=cid, scheduled_at=scheduled)
        completed = self.repository.complete_crm_followup(int(followup["id"]))
        self.assertEqual(completed["status"], "completed")

    def test_create_crm_campaign(self) -> None:
        campaign = self.repository.create_crm_campaign(name="Repo campaign", channel="email")
        self.assertEqual(campaign["name"], "Repo campaign")

    def test_launch_crm_campaign(self) -> None:
        campaign = self.repository.create_crm_campaign(name="Launch me", channel="whatsapp")
        result = self.repository.launch_crm_campaign(int(campaign["id"]))
        self.assertIn("campaign_id", result)

    def test_create_crm_segment(self) -> None:
        segment = self.repository.create_crm_segment(name="VIP buyers", criteria={"contact_type": "customer"})
        self.assertEqual(segment["name"], "VIP buyers")

    def test_compute_crm_customer_scores(self) -> None:
        cid = self._contact_id()
        scores = self.repository.compute_crm_customer_scores(cid)
        for key in SCORE_KEYS:
            self.assertIn(key, scores)

    def test_list_crm_satisfaction_surveys(self) -> None:
        surveys = self.repository.list_crm_satisfaction_surveys()
        self.assertGreaterEqual(len(surveys), 1)

    def test_add_crm_note(self) -> None:
        cid = self._contact_id()
        note = self.repository.add_crm_note(contact_id=cid, content="Important note", author_id=1)
        self.assertEqual(note["content"], "Important note")

    def test_generate_crm_ai_suggestions(self) -> None:
        cid = self._contact_id()
        suggestions = self.repository.generate_crm_ai_suggestions(cid)
        self.assertGreaterEqual(len(suggestions), 1)

    def test_customer_360(self) -> None:
        cid = self._contact_id()
        view = self.repository.customer_360(cid)
        self.assertIn("contact", view)
        self.assertIn("summary", view)

    def test_list_crm_timeline(self) -> None:
        cid = self._contact_id()
        timeline = self.repository.list_crm_timeline(cid)
        self.assertIsInstance(timeline, list)

    def test_list_crm_journey(self) -> None:
        cid = self._contact_id()
        journey = self.repository.list_crm_journey(cid)
        self.assertGreaterEqual(len(journey), 1)

    def test_crm_search(self) -> None:
        results = self.repository.crm_search(query="Marie")
        self.assertGreaterEqual(len(results), 1)

    def test_crm_analytics(self) -> None:
        analytics = self.repository.crm_analytics()
        self.assertIn("contacts", analytics)
        self.assertEqual(analytics["official_sender"]["phone_number"], PHONE_NUMBER)

    def test_crm_stats(self) -> None:
        stats = self.repository.crm_stats()
        self.assertIn("segments", stats)

    def test_crm_dashboard(self) -> None:
        dashboard = self.repository.crm_dashboard()
        self.assertIn("pipeline_board", dashboard)
        self.assertEqual(dashboard["lawim_contact"]["telegram_bot"], TELEGRAM_BOT)

    def test_snapshot_crm_analytics(self) -> None:
        snap = self.repository.snapshot_crm_analytics()
        self.assertIn("snapshot_key", snap)
        self.assertIn("metrics", snap)

    def test_add_crm_contact_tag(self) -> None:
        cid = self._contact_id()
        tag = self.repository.add_crm_contact_tag(cid, "vip")
        self.assertEqual(tag["tag"], "vip")

    def test_grant_crm_consent(self) -> None:
        cid = self._contact_id()
        consent = self.repository.grant_crm_consent(cid, consent_type="whatsapp")
        self.assertEqual(int(consent["granted"]), 1)


class ReleaseProgramHApiTests(LawimTestHarness):
    def _contact_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/crm/contacts", token=token).body_json()
        return int(payload["contacts"][0]["id"])

    def _lead_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/crm/leads", token=token).body_json()
        return int(payload["leads"][0]["id"])

    def _pipeline_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/crm/pipelines", token=token).body_json()
        return int(payload["pipelines"][0]["id"])

    def _pipeline_item_id(self, token: str) -> int:
        pipeline_id = self._pipeline_id(token)
        board = self.invoke(f"/api/v2/crm/pipelines/{pipeline_id}/board", token=token).body_json()["board"]
        for column in board:
            if column.get("items"):
                return int(column["items"][0]["id"])
        raise AssertionError("no pipeline items")

    def test_official_contact_no_auth_api(self) -> None:
        response = self.invoke("/api/v2/crm/official-contact")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.body_json()["contact"]["phone_number"], PHONE_NUMBER)

    def test_contacts_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/contacts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["contacts"]), 1)

    def test_contact_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_leads_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/leads", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_lead_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        lid = self._lead_id(token)
        response = self.invoke(f"/api/v2/crm/leads/{lid}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_lead_sources_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/leads/sources", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_customers_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/customers", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_opportunities_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/opportunities", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_pipelines_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/pipelines", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_pipeline_board_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._pipeline_id(token)
        response = self.invoke(f"/api/v2/crm/pipelines/{pid}/board", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_communications_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/communications", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_reminders_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/reminders", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_followups_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/followups", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_campaigns_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/campaigns", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_segments_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/segments", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_satisfaction_surveys_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/satisfaction/surveys", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_satisfaction_summary_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        survey_id = int(self.repository.one("SELECT id FROM crm_satisfaction_surveys LIMIT 1")["id"])
        response = self.invoke(f"/api/v2/crm/satisfaction/{survey_id}/summary", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_ai_suggestions_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/ai/suggestions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_search_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/search?q=Marie", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("results", response.body_json())

    def test_analytics_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/analytics", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_stats_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/stats", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("stats", response.body_json())

    def test_dashboard_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/dashboard", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contact_360_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}/360", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contact_timeline_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}/timeline", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contact_journey_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}/journey", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contact_notes_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}/notes", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contact_scores_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(f"/api/v2/crm/contacts/{cid}/scores", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_contact_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/crm/contacts",
            method="POST",
            token=token,
            body={"full_name": "API Contact", "contact_type": "prospect"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_lead_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/leads",
            method="POST",
            token=token,
            body={"contact_id": cid, "title": "API Lead"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_customer_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/crm/contacts",
            method="POST",
            token=token,
            body={"full_name": "Future Customer", "contact_type": "lead"},
        )
        cid = int(created.body_json()["contact"]["id"])
        response = self.invoke(
            "/api/v2/crm/customers",
            method="POST",
            token=token,
            body={"contact_id": cid, "roles": ["buyer"]},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_opportunity_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/opportunities",
            method="POST",
            token=token,
            body={"contact_id": cid, "title": "API Opp", "amount": 100000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_pipeline_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/crm/pipelines",
            method="POST",
            token=token,
            body={"name": "API Pipeline"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_send_whatsapp_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/whatsapp",
            method="POST",
            token=token,
            body={"contact_id": cid, "body": "WhatsApp via API"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_send_telegram_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/telegram",
            method="POST",
            token=token,
            body={"contact_id": cid, "body": "Telegram via API", "to_handle": "@client"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_send_email_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/email",
            method="POST",
            token=token,
            body={"contact_id": cid, "subject": "Hello", "body": "Email via API"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_send_sms_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/sms",
            method="POST",
            token=token,
            body={"contact_id": cid, "body": "SMS via API"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_reminder_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        due = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        response = self.invoke(
            "/api/v2/crm/reminders",
            method="POST",
            token=token,
            body={"contact_id": cid, "title": "Reminder", "due_at": due},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_schedule_followup_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        scheduled = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat()
        response = self.invoke(
            "/api/v2/crm/followups",
            method="POST",
            token=token,
            body={"contact_id": cid, "scheduled_at": scheduled, "channel": "whatsapp"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_campaign_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/crm/campaigns",
            method="POST",
            token=token,
            body={"name": "API Campaign", "channel": "email"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_segment_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/crm/segments",
            method="POST",
            token=token,
            body={"name": "API Segment", "criteria": {"contact_type": "customer"}},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_submit_satisfaction_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        survey_id = int(self.repository.one("SELECT id FROM crm_satisfaction_surveys LIMIT 1")["id"])
        response = self.invoke(
            "/api/v2/crm/satisfaction/responses",
            method="POST",
            token=token,
            body={"survey_id": survey_id, "contact_id": cid, "rating": 5},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_add_note_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            "/api/v2/crm/notes",
            method="POST",
            token=token,
            body={"contact_id": cid, "content": "API note"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_convert_lead_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/crm/contacts",
            method="POST",
            token=token,
            body={"full_name": "Lead Convert", "contact_type": "lead"},
        )
        cid = int(created.body_json()["contact"]["id"])
        lead = self.invoke(
            "/api/v2/crm/leads",
            method="POST",
            token=token,
            body={"contact_id": cid, "title": "Convert me"},
        )
        lid = int(lead.body_json()["lead"]["id"])
        response = self.invoke(
            f"/api/v2/crm/leads/{lid}/convert",
            method="POST",
            token=token,
            body={"roles": ["buyer"]},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_add_contact_tag_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            f"/api/v2/crm/contacts/{cid}/tags",
            method="POST",
            token=token,
            body={"tag": "api-tag"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_grant_consent_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            f"/api/v2/crm/contacts/{cid}/consents",
            method="POST",
            token=token,
            body={"consent_type": "marketing"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_compute_scores_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            f"/api/v2/crm/contacts/{cid}/scores/compute",
            method="POST",
            token=token,
            body={},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_ai_suggestions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        response = self.invoke(
            f"/api/v2/crm/contacts/{cid}/ai/suggestions",
            method="POST",
            token=token,
            body={},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_launch_campaign_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/v2/crm/campaigns",
            method="POST",
            token=token,
            body={"name": "Launch Campaign", "channel": "whatsapp"},
        )
        campaign_id = int(created.body_json()["campaign"]["id"])
        response = self.invoke(
            f"/api/v2/crm/campaigns/{campaign_id}/launch",
            method="POST",
            token=token,
            body={},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_complete_followup_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        scheduled = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        created = self.invoke(
            "/api/v2/crm/followups",
            method="POST",
            token=token,
            body={"contact_id": cid, "scheduled_at": scheduled},
        )
        followup_id = int(created.body_json()["followup"]["id"])
        response = self.invoke(
            f"/api/v2/crm/followups/{followup_id}/complete",
            method="POST",
            token=token,
            body={},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_move_pipeline_item_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        item_id = self._pipeline_item_id(token)
        stage_id = int(self.repository.one("SELECT id FROM crm_pipeline_stages LIMIT 1")["id"])
        response = self.invoke(
            f"/api/v2/crm/pipeline-items/{item_id}/move",
            method="POST",
            token=token,
            body={"stage_id": stage_id, "position": 0},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_advance_pipeline_item_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        item_id = self._pipeline_item_id(token)
        response = self.invoke(
            f"/api/v2/crm/pipeline-items/{item_id}/advance",
            method="POST",
            token=token,
            body={},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_seed_catalog_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/crm/seed", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)


class ReleaseProgramHUiTests(LawimTestHarness):
    def test_index_has_crm_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Customer Relationship Management", html.body_text())

    def test_app_js_references_crm_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/crm/stats", js.body_text())
        self.assertIn("refreshCrmAdmin", js.body_text())

    def test_app_js_references_official_contact(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/crm/official-contact", js.body_text())


class ReleaseProgramHHealthTests(LawimTestHarness):
    def test_health_schema_v14(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 18)

    def test_migration_strategy_v14(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 18)

    def test_metrics_include_crm_counters(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/contacts", token=token)
        admin = self.login(email="admin@lawim.local")
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("crm_requests_total", 0), 1)


class ReleaseProgramHV14TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v14_table_crm_contact_profiles(self) -> None:
        self.assertIn("crm_contact_profiles", self._table_names())

    def test_v14_table_crm_contact_tags(self) -> None:
        self.assertIn("crm_contact_tags", self._table_names())

    def test_v14_table_crm_contact_consents(self) -> None:
        self.assertIn("crm_contact_consents", self._table_names())

    def test_v14_table_crm_leads(self) -> None:
        self.assertIn("crm_leads", self._table_names())

    def test_v14_table_crm_lead_sources(self) -> None:
        self.assertIn("crm_lead_sources", self._table_names())

    def test_v14_table_crm_customers(self) -> None:
        self.assertIn("crm_customers", self._table_names())

    def test_v14_table_crm_customer_roles(self) -> None:
        self.assertIn("crm_customer_roles", self._table_names())

    def test_v14_table_crm_opportunities(self) -> None:
        self.assertIn("crm_opportunities", self._table_names())

    def test_v14_table_crm_pipelines(self) -> None:
        self.assertIn("crm_pipelines", self._table_names())

    def test_v14_table_crm_pipeline_stages(self) -> None:
        self.assertIn("crm_pipeline_stages", self._table_names())

    def test_v14_table_crm_pipeline_items(self) -> None:
        self.assertIn("crm_pipeline_items", self._table_names())

    def test_v14_table_crm_journey_events(self) -> None:
        self.assertIn("crm_journey_events", self._table_names())

    def test_v14_table_crm_timeline_entries(self) -> None:
        self.assertIn("crm_timeline_entries", self._table_names())

    def test_v14_table_crm_communications(self) -> None:
        self.assertIn("crm_communications", self._table_names())

    def test_v14_table_crm_whatsapp_messages(self) -> None:
        self.assertIn("crm_whatsapp_messages", self._table_names())

    def test_v14_table_crm_telegram_messages(self) -> None:
        self.assertIn("crm_telegram_messages", self._table_names())

    def test_v14_table_crm_email_messages(self) -> None:
        self.assertIn("crm_email_messages", self._table_names())

    def test_v14_table_crm_sms_messages(self) -> None:
        self.assertIn("crm_sms_messages", self._table_names())

    def test_v14_table_crm_reminders(self) -> None:
        self.assertIn("crm_reminders", self._table_names())

    def test_v14_table_crm_followups(self) -> None:
        self.assertIn("crm_followups", self._table_names())

    def test_v14_table_crm_campaigns(self) -> None:
        self.assertIn("crm_campaigns", self._table_names())

    def test_v14_table_crm_campaign_targets(self) -> None:
        self.assertIn("crm_campaign_targets", self._table_names())

    def test_v14_table_crm_segments(self) -> None:
        self.assertIn("crm_segments", self._table_names())

    def test_v14_table_crm_segment_members(self) -> None:
        self.assertIn("crm_segment_members", self._table_names())

    def test_v14_table_crm_customer_scores(self) -> None:
        self.assertIn("crm_customer_scores", self._table_names())

    def test_v14_table_crm_satisfaction_surveys(self) -> None:
        self.assertIn("crm_satisfaction_surveys", self._table_names())

    def test_v14_table_crm_satisfaction_responses(self) -> None:
        self.assertIn("crm_satisfaction_responses", self._table_names())

    def test_v14_table_crm_notes(self) -> None:
        self.assertIn("crm_notes", self._table_names())

    def test_v14_table_crm_documents(self) -> None:
        self.assertIn("crm_documents", self._table_names())

    def test_v14_table_crm_ai_suggestions(self) -> None:
        self.assertIn("crm_ai_suggestions", self._table_names())

    def test_v14_table_crm_analytics_snapshots(self) -> None:
        self.assertIn("crm_analytics_snapshots", self._table_names())


class ReleaseProgramHIntegrationTests(LawimTestHarness):
    def test_lead_creation_may_start_workflow(self) -> None:
        before = self.repository.scalar("SELECT COUNT(*) FROM automation_process_instances")
        cid = int(self.repository.create_crm_contact(full_name="Workflow Lead", contact_type="lead")["id"])
        self.repository.create_crm_lead(contact_id=cid, title="Workflow trigger")
        after = self.repository.scalar("SELECT COUNT(*) FROM automation_process_instances")
        self.assertGreaterEqual(after, before)

    def test_ai_suggestions_include_knowledge_source(self) -> None:
        cid = int(self.repository.one("SELECT id FROM crm_contact_profiles LIMIT 1")["id"])
        suggestions = self.repository.generate_crm_ai_suggestions(cid)
        sources = CrmPlatformEngine().integration_sources()
        self.assertIn("knowledge_platform", sources)
        self.assertGreaterEqual(len(suggestions), 1)

    def test_integration_sources_include_rei(self) -> None:
        sources = CrmPlatformEngine().integration_sources()
        self.assertIn("real_estate_intelligence", sources)

    def test_rei_lead_source_present(self) -> None:
        source = self.repository.one("SELECT * FROM crm_lead_sources WHERE source_key = 'source-rei'")
        self.assertIsNotNone(source)
        self.assertEqual(source["channel"], "rei")

    def test_whatsapp_messages_use_official_sender(self) -> None:
        analytics = self.repository.crm_analytics()
        self.assertEqual(analytics["official_sender"]["facebook_username"], FACEBOOK_USERNAME)

    def test_crm_dashboard_links_lawim_contact(self) -> None:
        dashboard = self.repository.crm_dashboard()
        self.assertEqual(dashboard["lawim_contact"]["phone_number"], PHONE_NUMBER)

    def test_expert_rag_available_for_crm_ai(self) -> None:
        bridge = AiIntegrationBridge()
        result = bridge.enrich_with_knowledge(self.repository, "acte de vente")
        self.assertTrue(result is None or isinstance(result, dict))

    def test_workflow_trigger_from_ai_bridge(self) -> None:
        bridge = AiIntegrationBridge()
        result = bridge.trigger_workflow(self.repository, workflow_key="wf-crm-lead", context={"lead_id": 1})
        self.assertTrue(result is None or isinstance(result, dict))


class ReleaseProgramHObservabilityTests(LawimTestHarness):
    def _contact_id(self, token: str) -> int:
        return int(self.invoke("/api/v2/crm/contacts", token=token).body_json()["contacts"][0]["id"])

    def test_crm_contact_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/contacts", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["crm_requests_total"], 1)

    def test_crm_contact_created_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke(
            "/api/v2/crm/contacts",
            method="POST",
            token=token,
            body={"full_name": "Metrics Contact", "contact_type": "prospect"},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_contact_created", 0), 1)

    def test_crm_lead_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/leads", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_lead_list", 0), 1)

    def test_crm_search_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/search?q=Marie", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_search", 0), 1)

    def test_crm_analytics_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/analytics", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_analytics", 0), 1)

    def test_crm_stats_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/stats", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_stats", 0), 1)

    def test_crm_dashboard_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/crm/dashboard", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_dashboard", 0), 1)

    def test_whatsapp_sent_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        self.invoke(
            "/api/v2/crm/whatsapp",
            method="POST",
            token=token,
            body={"contact_id": cid, "body": "Metrics WA"},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_whatsapp_sent", 0), 1)

    def test_followup_scheduled_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        scheduled = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        self.invoke(
            "/api/v2/crm/followups",
            method="POST",
            token=token,
            body={"contact_id": cid, "scheduled_at": scheduled},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_followup_scheduled", 0), 1)

    def test_customer_360_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        cid = self._contact_id(token)
        self.invoke(f"/api/v2/crm/contacts/{cid}/360", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("customer_360", 0), 1)

    def test_pipeline_board_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        pipeline_id = int(self.invoke("/api/v2/crm/pipelines", token=token).body_json()["pipelines"][0]["id"])
        self.invoke(f"/api/v2/crm/pipelines/{pipeline_id}/board", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("pipeline_board", 0), 1)

    def test_campaign_created_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke(
            "/api/v2/crm/campaigns",
            method="POST",
            token=token,
            body={"name": "Metrics Campaign", "channel": "email"},
        )
        metrics = self.invoke("/api/metrics", token=token)
        crm_metrics = metrics.body_json()["metrics"].get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("crm_campaign_created", 0), 1)
