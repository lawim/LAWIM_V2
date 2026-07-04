from __future__ import annotations

import ast
from pathlib import Path
from unittest import TestCase

from lawim_v2 import i18n


class I18NLanguagesTest(TestCase):
    def test_default_language_is_french(self) -> None:
        self.assertEqual(i18n.DEFAULT_LANGUAGE, "fr")
        self.assertEqual(i18n.normalize_language(None), "fr")
        self.assertEqual(i18n.translate("app.name"), "LAWIM_V2")

    def test_supported_languages_are_official_codes(self) -> None:
        self.assertEqual(i18n.SUPPORTED_LANGUAGES, ("fr", "en", "pcm"))
        for language in i18n.SUPPORTED_LANGUAGES:
            with self.subTest(language=language):
                self.assertTrue(i18n.validate_language(language))
                self.assertEqual(i18n.normalize_language(language), language)

    def test_normalization_handles_locale_variants(self) -> None:
        cases = {
            "fr-FR": "fr",
            "en_US": "en",
            "pcm-CM": "pcm",
            "FR-fr": "fr",
            "EN-gb": "en",
        }
        for raw_language, expected_language in cases.items():
            with self.subTest(raw_language=raw_language):
                self.assertEqual(i18n.normalize_language(raw_language), expected_language)
                self.assertTrue(i18n.validate_language(raw_language))

    def test_unknown_language_falls_back_to_french(self) -> None:
        self.assertFalse(i18n.validate_language("es"))
        self.assertEqual(i18n.normalize_language("es"), "fr")
        self.assertEqual(i18n.translate("auth.login.failed", "es"), "Connexion échouée.")
        self.assertEqual(i18n.translate("auth.login.failed", None), "Connexion échouée.")

    def test_translation_by_key_uses_requested_language(self) -> None:
        self.assertEqual(i18n.translate("app.name", "fr"), "LAWIM_V2")
        self.assertEqual(i18n.translate("language.fr", "fr"), "Français")
        self.assertEqual(i18n.translate("language.en", "en"), "English")
        self.assertEqual(i18n.translate("language.pcm", "pcm"), "Cameroon Pidgin")
        self.assertEqual(i18n.translate("auth.login.success", "en"), "Login successful.")
        self.assertEqual(i18n.translate("auth.login.success", "pcm"), "Login don succeed.")
        self.assertEqual(i18n.translate("validation.required", "fr"), "Ce champ est obligatoire.")
        self.assertEqual(i18n.translate("error.generic", "en"), "An unexpected error occurred.")

    def test_missing_translation_key_uses_readable_placeholder(self) -> None:
        self.assertEqual(i18n.translate("missing.key", "en"), "[missing.key]")
        self.assertEqual(i18n.translate("missing.key", "pcm"), "[missing.key]")

    def test_module_has_no_external_dependency(self) -> None:
        source_path = Path(i18n.__file__).resolve()
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_modules: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.append(node.module)
        self.assertEqual(imported_modules, ["__future__"])
