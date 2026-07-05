from __future__ import annotations

SOURCE_STATUSES: frozenset[str] = frozenset({"active", "draft", "paused", "archived", "disabled"})

SOURCE_CHANNELS: frozenset[str] = frozenset(
    {
        "web",
        "facebook",
        "instagram",
        "tiktok",
        "linkedin",
        "telegram",
        "whatsapp",
        "email",
        "sms",
        "qr_code",
        "flyer",
        "partner",
        "referral",
        "client",
        "ambassador",
        "group",
        "publication",
        "internal",
        "rei",
        "other",
    }
)

SOURCE_IMPORT_STATUSES: frozenset[str] = frozenset({"pending", "imported", "analyzed", "validated", "failed"})

REFERENCE_CODE_PREFIX = "#"
REFERENCE_CODE_LENGTH = 6
DEFAULT_SOURCE_TARGET = "acquisition"

SOURCE_LANGUAGE_MARKERS: dict[str, tuple[str, ...]] = {
    "fr": (
        "bonjour",
        "merci",
        "vente",
        "location",
        "appartement",
        "maison",
        "terrain",
        "quartier",
        "cherche",
        "recherche",
        "acheter",
        "louer",
    ),
    "en": (
        "hello",
        "thanks",
        "rent",
        "sale",
        "apartment",
        "house",
        "land",
        "district",
        "looking for",
        "buy",
        "lease",
    ),
    "pcm": (
        "i wan",
        "i dey",
        "i di",
        "i fit",
        "no vex",
        "how far",
        "wahala",
        "wetin",
        "small small",
        "na so",
        "make i",
        "dey find",
        "abeg",
    ),
}
