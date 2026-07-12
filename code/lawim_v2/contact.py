"""Official LAWIM public contact configuration — single source of truth (Release Program H)."""

from __future__ import annotations

BRAND_SLOGAN = "L’immobilier autrement"
BRAND_SUBSLOGAN = ""
INSTITUTIONAL_TAGLINE = "Intelligent Real Estate Relationships"
BRAND_MESSAGE = (
    "Plateforme d'intelligence immobilière qui connecte les bonnes personnes, "
    "aux bons biens, au bon moment grâce à l'intelligence artificielle."
)
BRAND_POSITIONING = "Connecting people, properties and opportunities."

COMPANY_NAME = "LAWIM"
PHONE_NUMBER = "686 822 667"
PHONE_E164 = "+237686822667"
PHONE_INTERNATIONAL = "+237 686 822 667"
WHATSAPP_NUMBER = PHONE_NUMBER
GREEN_API_NUMBER = PHONE_NUMBER
FACEBOOK_USERNAME = "@lawimofficial"
WHATSAPP_USERNAME = "@lawimofficial"
TELEGRAM_BOT = "@lawim_bot"
DEFAULT_COUNTRY = "Cameroon"
SUPPORT_EMAIL = "contact@lawim.app"
WEBSITE_URL = "https://lawim.app"

SUPPORT_CONTACT = (
    f"{COMPANY_NAME}\n"
    f"{BRAND_SLOGAN}\n"
    f"📞 WhatsApp/Appel : {PHONE_NUMBER}\n"
    f"✉️ Email : {SUPPORT_EMAIL}\n"
    f"Facebook : {FACEBOOK_USERNAME}\n"
    f"WhatsApp : {WHATSAPP_USERNAME}\n"
    f"Telegram Bot : {TELEGRAM_BOT}\n"
    f"Site : {WEBSITE_URL}"
)


def official_signature_block() -> str:
    return SUPPORT_CONTACT


def whatsapp_link() -> str:
    digits = PHONE_E164.lstrip("+")
    return f"https://wa.me/{digits}"


def telegram_link() -> str:
    handle = TELEGRAM_BOT.lstrip("@")
    return f"https://t.me/{handle}"


def facebook_link() -> str:
    handle = FACEBOOK_USERNAME.lstrip("@")
    return f"https://facebook.com/{handle}"


def to_public_dict() -> dict[str, str]:
    return {
        "company_name": COMPANY_NAME,
        "brand_slogan": BRAND_SLOGAN,
        "brand_subslogan": BRAND_SUBSLOGAN,
        "institutional_tagline": INSTITUTIONAL_TAGLINE,
        "brand_message": BRAND_MESSAGE,
        "brand_positioning": BRAND_POSITIONING,
        "phone_number": PHONE_NUMBER,
        "phone_e164": PHONE_E164,
        "phone_international": PHONE_INTERNATIONAL,
        "whatsapp_number": WHATSAPP_NUMBER,
        "green_api_number": GREEN_API_NUMBER,
        "facebook_username": FACEBOOK_USERNAME,
        "whatsapp_username": WHATSAPP_USERNAME,
        "telegram_bot": TELEGRAM_BOT,
        "support_contact": SUPPORT_CONTACT,
        "support_email": SUPPORT_EMAIL,
        "default_country": DEFAULT_COUNTRY,
        "website_url": WEBSITE_URL,
        "whatsapp_link": whatsapp_link(),
        "telegram_link": telegram_link(),
        "facebook_link": facebook_link(),
    }
