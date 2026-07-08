from __future__ import annotations

SUPPORTED_LANGUAGES: tuple[str, ...] = ("fr", "en", "pcm")
DEFAULT_LANGUAGE: str = "fr"
MESSAGE_KEYS: tuple[str, ...] = (
    "app.name",
    "language.fr",
    "language.en",
    "language.pcm",
    "auth.login.success",
    "auth.login.failed",
    "validation.required",
    "error.generic",
)

_SUPPORTED_LANGUAGE_SET: frozenset[str] = frozenset(SUPPORTED_LANGUAGES)
_LANGUAGE_ALIASES: dict[str, str] = {
    "pidgin": "pcm",
    "pidgin english": "pcm",
    "cameroon pidgin": "pcm",
    "cameroonian pidgin": "pcm",
}
_TRANSLATIONS: dict[str, dict[str, str]] = {
    "fr": {
        "app.name": "LAWIM_V2",
        "language.fr": "Français",
        "language.en": "Anglais",
        "language.pcm": "Pidgin camerounais",
        "auth.login.success": "Connexion réussie.",
        "auth.login.failed": "Connexion échouée.",
        "validation.required": "Ce champ est obligatoire.",
        "error.generic": "Une erreur inattendue est survenue.",
    },
    "en": {
        "app.name": "LAWIM_V2",
        "language.fr": "French",
        "language.en": "English",
        "language.pcm": "Cameroonian Pidgin",
        "auth.login.success": "Login successful.",
        "auth.login.failed": "Login failed.",
        "validation.required": "This field is required.",
        "error.generic": "An unexpected error occurred.",
    },
    "pcm": {
        "app.name": "LAWIM_V2",
        "language.fr": "French",
        "language.en": "English",
        "language.pcm": "Cameroon Pidgin",
        "auth.login.success": "Login don succeed.",
        "auth.login.failed": "Login no succeed.",
        "validation.required": "Dis field na must.",
        "error.generic": "Something don go wrong.",
    },
}

__all__ = [
    "DEFAULT_LANGUAGE",
    "MESSAGE_KEYS",
    "SUPPORTED_LANGUAGES",
    "normalize_language",
    "translate",
    "validate_language",
]


def _canonical_language(language: str | None) -> str | None:
    normalized = str(language or "").strip().lower().replace("_", "-")
    if not normalized:
        return None
    if normalized in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[normalized]
    base_language = normalized.split("-", 1)[0]
    if base_language in _SUPPORTED_LANGUAGE_SET:
        return base_language
    if base_language in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[base_language]
    return None


def normalize_language(language: str | None) -> str:
    canonical = _canonical_language(language)
    return canonical if canonical is not None else DEFAULT_LANGUAGE


def validate_language(language: str | None) -> bool:
    return _canonical_language(language) is not None


def translate(key: str, language: str | None = None) -> str:
    translation_key = str(key or "").strip()
    resolved_language = normalize_language(language)
    language_messages = _TRANSLATIONS[resolved_language]
    if translation_key in language_messages:
        return language_messages[translation_key]

    default_messages = _TRANSLATIONS[DEFAULT_LANGUAGE]
    if translation_key in default_messages:
        return default_messages[translation_key]

    return f"[{translation_key or 'missing.translation'}]"
