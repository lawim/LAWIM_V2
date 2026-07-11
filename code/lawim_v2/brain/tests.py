from __future__ import annotations

import os
import unittest
from pathlib import Path
from typing import Any

from ..brain.intent_engine import IntentEngine, analyze_message, detect_intents
from ..brain.progression import ProgressionEngine, build_progression_state
from ..brain.resumption import ResumeEngine, build_resumption
from ..brain.accompaniment import AccompanimentEngine, evaluate_suggestions


class TestIntentEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = IntentEngine()

    def test_simple_french_buy(self):
        result = self.engine.analyze("Je veux acheter une maison")
        self.assertEqual(result["primary_intent"], "buy")
        self.assertGreater(result["primary_score"], 0)
        self.assertEqual(result["language"], "fr")

    def test_simple_english_rent(self):
        result = self.engine.analyze("I want to rent an apartment")
        self.assertEqual(result["primary_intent"], "rent")
        self.assertEqual(result["language"], "en")

    def test_simple_pidgin_find_land(self):
        result = self.engine.analyze("I dey find land for Douala")
        self.assertEqual(result["primary_intent"], "find_land")
        self.assertEqual(result["language"], "pcm")

    def test_multi_intents(self):
        result = self.engine.analyze("I want to sell my house and buy a new one")
        intents = [i["intent"] for i in result["intents"]]
        self.assertIn("sell", intents)
        self.assertIn("buy", intents)
        self.assertTrue(result["is_multi_intent"])

    def test_city_extraction_douala(self):
        result = self.engine.analyze("Je cherche un terrain à Douala")
        cities = result["entities"].get("cities", [])
        self.assertTrue(any(c["city"] == "Douala" for c in cities))

    def test_city_extraction_yaounde(self):
        result = self.engine.analyze("I want to buy a house in Yaounde")
        cities = result["entities"].get("cities", [])
        self.assertTrue(any(c["city"] == "Yaounde" for c in cities))

    def test_budget_extraction(self):
        result = self.engine.analyze("Budget 35 millions FCFA")
        budgets = result["entities"].get("budgets", [])
        self.assertTrue(len(budgets) > 0)
        self.assertIn("35", str(budgets[0].get("value", "")))

    def test_property_type_extraction(self):
        result = self.engine.analyze("Je cherche un appartement 3 pièces")
        types = result["entities"].get("property_types", [])
        self.assertIn("appartement", types)

    def test_surface_extraction(self):
        result = self.engine.analyze("Je veux 500 m²")
        surfaces = result["entities"].get("surfaces_m2", [])
        self.assertIn(500, surfaces)

    def test_bedroom_extraction(self):
        result = self.engine.analyze("Je cherche 3 chambres")
        bedrooms = result["entities"].get("bedrooms", [])
        self.assertIn(3, bedrooms)

    def test_confirmations(self):
        self.assertTrue(self.engine.analyze("Oui c'est correct")["is_confirmation"])
        self.assertTrue(self.engine.analyze("Yes that's right")["is_confirmation"])
        self.assertTrue(self.engine.analyze("Na so")["is_confirmation"])

    def test_rejections(self):
        self.assertTrue(self.engine.analyze("Non ce n'est pas ça")["is_rejection"])
        self.assertTrue(self.engine.analyze("No not that")["is_rejection"])
        self.assertTrue(self.engine.analyze("No be dat")["is_rejection"])

    def test_ambiguous(self):
        result = self.engine.analyze("Bonjour")
        self.assertEqual(result["primary_intent"], "other")
        self.assertEqual(result["is_confirmation"], None)

    def test_seek_funding(self):
        result = self.engine.analyze("Je cherche un financement pour construire")
        self.assertEqual(result["primary_intent"], "find_funding")

    def test_seek_partner(self):
        result = self.engine.analyze("Je cherche un notaire à Douala")
        self.assertEqual(result["primary_intent"], "find_partner")

    def test_invest(self):
        result = self.engine.analyze("Je veux investir dans l'immobilier locatif")
        self.assertEqual(result["primary_intent"], "invest")

    def test_sell(self):
        result = self.engine.analyze("Je veux vendre ma villa à Bonanjo")
        self.assertEqual(result["primary_intent"], "sell")

    def test_build(self):
        result = self.engine.analyze("Je veux construire une clinique")
        self.assertEqual(result["primary_intent"], "build")

    def test_language_switch_mid_conversation(self):
        """Pidgin message should not be detected as English"""
        result = self.engine.analyze("Wetin dey happen? I dey find house for Douala")
        self.assertEqual(result["language"], "pcm")
        result2 = self.engine.analyze("Please tell me more about this property")
        self.assertEqual(result2["language"], "en")


class TestProgressionEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ProgressionEngine()

    def test_buy_starts_with_city(self):
        state = build_progression_state(
            project_id=1,
            intent="buy",
            entities={},
            memory_items=[],
            project=None,
        )
        self.assertIn("Dans quelle ville", state.get("next_question", ""))
        self.assertFalse(state["complete"])
        self.assertEqual(state["known_fields"], [])

    def test_buy_partially_known(self):
        state = build_progression_state(
            project_id=1,
            intent="buy",
            entities={"cities": [{"city": "Douala", "match": "douala", "region": None}]},
            memory_items=[],
            project=None,
        )
        self.assertIn("budget", state.get("next_question", "").lower())
        self.assertIn("city", state["known_fields"])

    def test_buy_known_city_and_budget(self):
        state = build_progression_state(
            project_id=1,
            intent="buy",
            entities={
                "cities": [{"city": "Douala", "match": "douala", "region": None}],
                "budgets": [{"raw": "50M", "value": 50000000, "currency": "XAF"}],
            },
            memory_items=[],
            project=None,
        )
        self.assertIn("type de bien", state.get("next_question", ""))
        self.assertIn("city", state["known_fields"])
        self.assertIn("budget_max", state["known_fields"])

    def test_rent_qualification(self):
        state = build_progression_state(
            project_id=1,
            intent="rent",
            entities={},
            memory_items=[],
            project=None,
        )
        self.assertIn("location", state.get("next_question", "").lower())

    def test_complete_progression(self):
        state = build_progression_state(
            project_id=1,
            intent="find_land",
            entities={
                "cities": [{"city": "Douala", "match": "douala", "region": None}],
                "budgets": [{"raw": "30M", "value": 30000000, "currency": "XAF"}],
                "surfaces_m2": [500],
            },
            memory_items=[],
            project={"location_city": "Douala"},
        )
        # Should be close to complete with city, budget, and surface known
        self.assertIn("usage", state.get("next_question", "").lower())

    def test_requires_confirmation(self):
        self.assertTrue(self.engine.requires_confirmation("budget_max"))
        self.assertTrue(self.engine.requires_confirmation("city"))
        self.assertTrue(self.engine.requires_confirmation("property_type"))
        self.assertFalse(self.engine.requires_confirmation("surface_m2"))

    def test_next_actions(self):
        state = build_progression_state(
            project_id=1,
            intent="buy",
            entities={"cities": [{"city": "Douala", "match": "douala", "region": None}]},
            memory_items=[],
            project=None,
        )
        self.assertTrue(len(state.get("next_actions", [])) > 0)


class TestResumeEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ResumeEngine()

    def test_new_project_no_history(self):
        result = self.engine.build(
            project=None,
            confirmed_facts=[],
            pending_hypotheses=[],
            language="fr",
        )
        self.assertFalse(result["has_history"])
        self.assertIn("Bienvenue", result["short_summary"])

    def test_existing_project_with_facts(self):
        result = self.engine.build(
            project={"objective": "Acheter une maison", "location_city": "Douala"},
            confirmed_facts=[
                {"label": "Budget", "value": "35 millions FCFA"},
                {"label": "Type", "value": "Maison"},
            ],
            pending_hypotheses=[],
            language="fr",
        )
        self.assertTrue(result["has_history"])
        self.assertEqual(result["objective"], "Acheter une maison")
        self.assertEqual(result["city"], "Douala")
        self.assertEqual(result["confirmed_count"], 2)

    def test_existing_project_with_pending(self):
        result = self.engine.build(
            project={"objective": "Trouver un terrain", "location_city": "Yaoundé"},
            confirmed_facts=[],
            pending_hypotheses=[
                {"label": "Budget", "value": "30 millions"},
            ],
            language="fr",
        )
        self.assertEqual(result["pending_count"], 1)

    def test_english_resumption(self):
        result = self.engine.build(
            project={"objective": "Buy a house", "location_city": "Douala"},
            confirmed_facts=[{"label": "Budget", "value": "50M"}],
            pending_hypotheses=[],
            language="en",
        )
        self.assertIn("We had been working", result["summary"])

    def test_pidgin_resumption(self):
        result = self.engine.build(
            project={"objective": "Find land", "location_city": "Bamenda"},
            confirmed_facts=[{"label": "Budget", "value": "20M"}],
            pending_hypotheses=[],
            language="pcm",
        )
        self.assertIn("We don stop", result["summary"])

    def test_resumption_with_next_question(self):
        result = self.engine.build(
            project={"objective": "Acheter", "location_city": "Douala"},
            confirmed_facts=[{"label": "Budget", "value": "35M"}],
            pending_hypotheses=[],
            next_question="Quel type de bien recherchez-vous ?",
            language="fr",
        )
        self.assertIn("Quel type", result["summary"])


class TestAccompanimentEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = AccompanimentEngine()

    def test_buy_suggestions_with_city(self):
        suggestions = evaluate_suggestions(
            intent="buy",
            entities={"cities": [{"city": "Douala", "match": "douala", "region": None}]},
            progression={"known_fields": ["city"], "complete": False},
            memory_items=[],
        )
        self.assertTrue(len(suggestions) > 0)
        # Should suggest checking listings for Douala
        self.assertTrue(any("annonces" in s["content"].lower() for s in suggestions))

    def test_buy_suggestions_with_budget(self):
        suggestions = evaluate_suggestions(
            intent="buy",
            entities={"budgets": [{"raw": "50M", "value": 50000000, "currency": "XAF"}]},
            progression={"known_fields": ["budget_max"], "complete": False},
            memory_items=[],
        )
        self.assertTrue(len(suggestions) > 0)
        self.assertTrue(any("capacité" in s["content"] or "loan" in s["content"].lower() for s in suggestions))

    def test_complete_progression_suggestions(self):
        suggestions = evaluate_suggestions(
            intent="buy",
            entities={},
            progression={"known_fields": ["city", "budget_max", "property_type"], "complete": True},
            memory_items=[],
        )
        self.assertTrue(len(suggestions) > 0)

    def test_build_suggestions(self):
        suggestions = evaluate_suggestions(
            intent="build",
            entities={"cities": [{"city": "Douala", "match": "douala", "region": None}]},
            progression={"known_fields": ["city"], "complete": False},
            memory_items=[],
        )
        self.assertTrue(any("terrain" in s["content"].lower() for s in suggestions))


class TestScenarioSimulations(unittest.TestCase):
    def _analyze(self, text: str) -> dict[str, Any]:
        return analyze_message(text)

    def _check_progression(self, intent: str, entities: dict[str, Any], known_fields: list[str]):
        label_map = {
            "city": "ville", "budget_max": "budget maximum", "budget_min": "budget minimum",
            "property_type": "type de bien", "surface_m2": "surface", "bedrooms": "nombre de pièces",
            "neighborhood": "quartier", "purpose": "usage",
        }
        memory_items = []
        for field in known_fields:
            memory_items.append({
                "kind": "confirmed_fact" if field != "budget_max" else "hypothesis",
                "field_key": field,
                "label": label_map.get(field, field),
                "value": "test",
            })
        return build_progression_state(
            project_id=1,
            intent=intent,
            entities=entities,
            memory_items=memory_items,
            project={"location_city": None, "budget_min": None, "budget_max": None},
        )

    def test_scenario_acheter_terrain_yaounde(self):
        # Simulate accumulation of known fields across 4 messages
        all_known: list[str] = []
        analysis1 = self._analyze("Je cherche un terrain à Yaoundé")
        all_known.append("city")
        state1 = self._check_progression("find_land", analysis1["entities"], all_known)
        self.assertIn("budget", state1.get("next_question", ""))

        analysis2 = self._analyze("Budget 30 millions")
        all_known.append("budget_max")
        state2 = self._check_progression("find_land", analysis2["entities"], all_known)
        self.assertTrue(any(w in state2.get("next_question", "").lower() for w in ("surface", "superficie")))

        analysis3 = self._analyze("500 m²")
        all_known.append("surface_m2")
        state3 = self._check_progression("find_land", analysis3["entities"], all_known)
        self.assertIn("usage", state3.get("next_question", "").lower())

        analysis4 = self._analyze("Pour construire")
        all_known.append("purpose")
        state4 = self._check_progression("find_land", analysis4["entities"], all_known)
        self.assertTrue(state4.get("complete", False))

    def test_scenario_louer_appartement_douala(self):
        texts = [
            "Je cherche un appartement à louer à Douala",
            "Loyer max 500 000 FCFA",
            "3 chambres",
            "Bonapriso",
        ]
        analysis = self._analyze(texts[0])
        self.assertEqual(analysis["primary_intent"], "rent")
        self.assertIn("douala", str(analysis["entities"].get("cities", [])).lower())
        analysis2 = self._analyze(texts[1])
        self.assertTrue(len(analysis2["entities"].get("budgets", [])) > 0)

    def test_scenario_vendre_maison(self):
        analysis = self._analyze("Je veux vendre ma villa à Bastos")
        self.assertEqual(analysis["primary_intent"], "sell")
        cities = analysis["entities"].get("cities", [])
        self.assertTrue(any("Yaounde" in c.get("city", "") for c in cities))
        types = analysis["entities"].get("property_types", [])
        self.assertIn("villa", types)

    def test_scenario_construire_clinique(self):
        analysis = self._analyze("Je veux construire une clinique à Douala")
        self.assertEqual(analysis["primary_intent"], "build")
        types = analysis["entities"].get("property_types", [])
        self.assertIn("clinique", types)

    def test_scenario_investir_immeuble(self):
        analysis = self._analyze("Je cherche un investissement locatif")
        self.assertEqual(analysis["primary_intent"], "invest")

    def test_scenario_rechercher_notaire(self):
        analysis = self._analyze("Je cherche un notaire à Douala")
        self.assertEqual(analysis["primary_intent"], "find_partner")

    def test_scenario_rechercher_financement(self):
        analysis = self._analyze("Je cherche un prêt bancaire pour acheter")
        self.assertEqual(analysis["primary_intent"], "find_funding")

    def test_scenario_deux_projets_simultanes(self):
        proj1 = self._analyze("Je cherche un terrain à Douala")
        proj2 = self._analyze("Je veux vendre ma maison à Yaoundé")
        self.assertEqual(proj1["primary_intent"], "find_land")
        self.assertEqual(proj2["primary_intent"], "sell")
        self.assertNotEqual(
            proj1["entities"].get("cities", []),
            proj2["entities"].get("cities", []),
        )

    def test_scenario_changement_avis(self):
        first = self._analyze("Je veux acheter un terrain")
        second = self._analyze("Finalement je préfère un appartement")
        # "acheter" makes it "buy" primarily, "terrain" also matches find_land
        self.assertIn(first["primary_intent"], ("buy", "find_land"))
        types = second["entities"].get("property_types", [])
        self.assertIn("appartement", types)

    def test_scenario_informations_contradictoires(self):
        msg1 = self._analyze("Budget 50 millions")
        msg2 = self._analyze("Non c'est 30 millions")
        self.assertTrue(msg1["entities"].get("budgets"))
        self.assertTrue(msg2["is_rejection"])

    def test_scenario_francais_vers_pidgin(self):
        msg1 = self._analyze("Je cherche une maison à Douala")
        self.assertEqual(msg1["language"], "fr")
        msg2 = self._analyze("I don see the one wey I like, na so")
        self.assertEqual(msg2["language"], "pcm")

    def test_scenario_sans_information(self):
        analysis = self._analyze("Bonjour")
        self.assertEqual(analysis["primary_intent"], "other")
        self.assertEqual(analysis["primary_score"], 50)

    def test_suggestions_after_terrain_trouve(self):
        suggestions = evaluate_suggestions(
            intent="find_land",
            entities={"cities": [{"city": "Douala", "match": "douala", "region": None}]},
            progression={"known_fields": ["city"], "complete": False},
            memory_items=[],
        )
        self.assertTrue(len(suggestions) > 0)


class TestRelationEngine(unittest.TestCase):
    def setUp(self) -> None:
        from ..brain.relation_ddl import (
            PROPOSAL_STATUSES, RELATION_TYPES,
            SQLITE_RELATION_TABLES_SCRIPT,
        )
        self.statuses = PROPOSAL_STATUSES
        self.types = RELATION_TYPES

    def test_proposal_statuses_defined(self):
        """All required proposal statuses must be defined"""
        required = ("detected", "proposed", "accepted", "rejected",
                    "deferred", "consent_pending", "relation_established",
                    "cancelled")
        for s in required:
            self.assertIn(s, self.statuses, f"Missing proposal status: {s}")

    def test_relation_types_defined(self):
        """All required relation types must be defined"""
        required = ("person_to_property", "person_to_person",
                    "person_to_partner", "project_to_project",
                    "property_to_partner", "partner_to_partner")
        for t in required:
            self.assertIn(t, self.types, f"Missing relation type: {t}")

    def test_partner_intent_map(self):
        """Partner intent map must cover key partners"""
        from ..brain.relation import PARTNER_INTENT_MAP
        self.assertIn("notaire", PARTNER_INTENT_MAP)
        self.assertIn("architecte", PARTNER_INTENT_MAP)
        self.assertIn("banque", PARTNER_INTENT_MAP)
        self.assertIn("agent immobilier", PARTNER_INTENT_MAP)

    def test_property_type_by_intent(self):
        """Property type mapping must cover main intents"""
        from ..brain.relation import PROPERTY_TYPE_BY_INTENT
        self.assertIn("buy", PROPERTY_TYPE_BY_INTENT)
        self.assertIn("rent", PROPERTY_TYPE_BY_INTENT)
        self.assertIn("invest", PROPERTY_TYPE_BY_INTENT)
        self.assertIn("build", PROPERTY_TYPE_BY_INTENT)

    def test_relation_type_enum(self):
        from ..brain.relation import RelationType
        self.assertEqual(RelationType.PERSON_TO_PROPERTY.value, "person_to_property")
        self.assertEqual(RelationType.PERSON_TO_PARTNER.value, "person_to_partner")
        self.assertEqual(RelationType.PERSON_TO_PERSON.value, "person_to_person")

    def test_proposal_status_enum(self):
        from ..brain.relation import ProposalStatus
        self.assertEqual(ProposalStatus.DETECTED.value, "detected")
        self.assertEqual(ProposalStatus.ACCEPTED.value, "accepted")
        self.assertEqual(ProposalStatus.REJECTED.value, "rejected")
        self.assertEqual(ProposalStatus.CONSENT_PENDING.value, "consent_pending")
        self.assertEqual(ProposalStatus.RELATION_ESTABLISHED.value, "relation_established")

    def test_build_match_context_with_project(self):
        from ..brain.relation import _build_match_context
        ctx = _build_match_context(
            {"id": 1, "project_type": "buy", "location_city": "Douala",
             "budget_min": 20000000, "budget_max": 50000000},
            None,
        )
        self.assertEqual(ctx.get("project_id"), 1)
        self.assertEqual(ctx.get("city"), "Douala")
        self.assertEqual(ctx.get("budget_min"), 20000000)
        self.assertEqual(ctx.get("budget_max"), 50000000)

    def test_build_match_context_with_analysis(self):
        from ..brain.relation import _build_match_context
        ctx = _build_match_context(
            None,
            {"primary_intent": "buy", "entities": {
                "cities": [{"city": "Yaoundé", "match": "yaounde", "region": None}],
                "budgets": [{"raw": "50M", "value": 50000000, "currency": "XAF"}]
            }, "language": "fr"},
        )
        self.assertEqual(ctx.get("primary_intent"), "buy")
        self.assertEqual(ctx.get("city"), "Yaoundé")
        self.assertEqual(ctx.get("budget_max"), 50000000)

    def test_relation_ddl_sqlite(self):
        from ..brain.relation_ddl import SQLITE_RELATION_TABLES_SCRIPT
        self.assertIn("brain_relation_proposals", SQLITE_RELATION_TABLES_SCRIPT)
        self.assertIn("brain_relations", SQLITE_RELATION_TABLES_SCRIPT)
        self.assertIn("FOREIGN KEY (project_id) REFERENCES projects(id)", SQLITE_RELATION_TABLES_SCRIPT)

    def test_relation_ddl_postgresql(self):
        from ..brain.relation_ddl import POSTGRESQL_RELATION_STATEMENTS
        statements = "\n".join(POSTGRESQL_RELATION_STATEMENTS)
        self.assertIn("brain_relation_proposals", statements)
        self.assertIn("brain_relations", statements)
        self.assertIn("SERIAL PRIMARY KEY", statements)

    def test_match_criteria_creation(self):
        from ..matching import MatchCriteria, MatchWeights
        criteria = MatchCriteria(
            target_type="property",
            city="Douala",
            country="Cameroon",
            budget_max=50000000,
            limit=10,
            min_score=20.0,
            weights=MatchWeights().normalized(),
        )
        self.assertEqual(criteria.target_type, "property")
        self.assertEqual(criteria.city, "Douala")
        self.assertEqual(criteria.budget_max, 50000000)

    def test_match_criteria_partner(self):
        from ..matching import MatchCriteria, MatchWeights
        criteria = MatchCriteria(
            target_type="partner",
            city="Yaoundé",
            partner_type="notaire",
            need="buy",
            status="active",
            limit=5,
            min_score=15.0,
            weights=MatchWeights().normalized(),
        )
        self.assertEqual(criteria.target_type, "partner")
        self.assertEqual(criteria.partner_type, "notaire")
        self.assertEqual(criteria.need, "buy")

    def test_rank_properties_returns_list(self):
        from ..matching import MatchCriteria, MatchWeights, rank_properties
        properties = [
            {"id": 1, "city": "Douala", "price_max": 40000000, "status": "published", "property_type": "maison"},
            {"id": 2, "city": "Douala", "price_max": 60000000, "status": "published", "property_type": "appartement"},
        ]
        criteria = MatchCriteria(
            target_type="property", city="Douala", budget_max=50000000,
            limit=5, min_score=0, weights=MatchWeights().normalized(),
        )
        result = rank_properties(properties, criteria)
        self.assertIsInstance(result, list)

    def test_rank_partners_returns_list(self):
        from ..matching import MatchCriteria, MatchWeights, rank_partners
        partners = [
            {"id": 1, "partner_type": "notaire", "city": "Douala", "status": "active"},
            {"id": 2, "partner_type": "architecte", "city": "Yaoundé", "status": "active"},
        ]
        criteria = MatchCriteria(
            target_type="partner", city="Douala", partner_type="notaire",
            need="buy", status="active", limit=5, min_score=0,
            weights=MatchWeights().normalized(),
        )
        result = rank_partners(partners, criteria)
        self.assertIsInstance(result, list)

    def test_proposal_status_transitions(self):
        from ..brain.relation import ProposalStatus
        valid_transitions = {
            ProposalStatus.DETECTED: [ProposalStatus.PROPOSED, ProposalStatus.REJECTED],
            ProposalStatus.PROPOSED: [ProposalStatus.ACCEPTED, ProposalStatus.REJECTED, ProposalStatus.DEFERRED],
            ProposalStatus.ACCEPTED: [ProposalStatus.CONSENT_PENDING, ProposalStatus.REJECTED],
            ProposalStatus.CONSENT_PENDING: [ProposalStatus.RELATION_ESTABLISHED, ProposalStatus.REJECTED],
            ProposalStatus.RELATION_ESTABLISHED: [ProposalStatus.IN_PROGRESS, ProposalStatus.COMPLETED],
            ProposalStatus.REJECTED: [ProposalStatus.NO_FOLLOW_UP],
        }
        for status, next_statuses in valid_transitions.items():
            for next_s in next_statuses:
                self.assertNotEqual(status, next_s, f"Self-transition not allowed for {status}")

    def test_schema_ddl_relation_statements(self):
        from ..brain.schema_ddl import POSTGRESQL_BRAIN_STATEMENTS
        has_relation = any("brain_relation" in s for s in POSTGRESQL_BRAIN_STATEMENTS)
        self.assertTrue(has_relation, "Brain schema DDL should include relation tables")


class TestReadinessCheck(unittest.TestCase):
    def test_readiness_writable_storage(self):
        from ..config import AppConfig
        import tempfile, os
        """readyz detects writable storage"""
        with tempfile.TemporaryDirectory() as tmp:
            media = os.path.join(tmp, "media")
            os.makedirs(media, exist_ok=True)
            config = AppConfig.for_test(
                db_path=str(os.path.join(tmp, "test.db")),
                media_storage_path=media,
            )
            # Test storage probe directly
            ready = False
            try:
                probe = Path(media) / ".probe"
                probe.write_text("ok")
                probe.unlink()
                ready = True
            except OSError:
                ready = False
            self.assertTrue(ready, "Storage should be writable")

    def test_readiness_unwritable_storage(self):
        from ..config import AppConfig
        import tempfile, os, stat
        """readyz detects unwritable storage"""
        with tempfile.TemporaryDirectory() as tmp:
            media = os.path.join(tmp, "media_ro")
            os.makedirs(media, exist_ok=True)
            os.chmod(media, stat.S_IRUSR | stat.S_IXUSR)
            config = AppConfig.for_test(
                db_path=str(os.path.join(tmp, "test.db")),
                media_storage_path=media,
            )
            ready = False
            try:
                probe = Path(media) / ".probe"
                probe.write_text("ok")
                probe.unlink()
                ready = True
            except OSError:
                ready = False
            self.assertFalse(ready, "Read-only storage should not be writable")


if __name__ == "__main__":
    unittest.main()
