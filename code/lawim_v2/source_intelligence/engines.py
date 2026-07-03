from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote, urlparse

from ..contact import PHONE_E164
from .constants import DEFAULT_SOURCE_TARGET, REFERENCE_CODE_LENGTH, REFERENCE_CODE_PREFIX, SOURCE_CHANNELS


class ReferenceCodeEngine:
    _ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

    def generate(self, *, seed: str | None = None, length: int = REFERENCE_CODE_LENGTH) -> str:
        payload = seed.encode("utf-8") if seed else uuid.uuid4().bytes
        digest = hashlib.sha256(payload).digest()
        value = int.from_bytes(digest, "big")
        chars: list[str] = []
        for _ in range(length):
            value, index = divmod(value, len(self._ALPHABET))
            chars.append(self._ALPHABET[index])
        return f"{REFERENCE_CODE_PREFIX}{''.join(chars)}"


class SourceAnalysisEngine:
    _CITY_HINTS = (
        "douala",
        "yaounde",
        "yaoundé",
        "kribi",
        "bafoussam",
        "limbe",
        "buea",
        "mutengene",
        "gare",
        "bonanjo",
        "makepe",
    )
    _PROPERTY_HINTS: tuple[tuple[str, str], ...] = (
        ("apartment", "apartment"),
        ("appartement", "apartment"),
        ("studio", "studio"),
        ("villa", "villa"),
        ("terrain", "land"),
        ("land", "land"),
        ("commercial", "commercial"),
        ("bureau", "commercial"),
        ("office", "commercial"),
        ("duplex", "duplex"),
        ("house", "house"),
        ("maison", "house"),
    )
    _NETWORK_ALIASES = {
        "facebook.com": "facebook",
        "fb.com": "facebook",
        "instagram.com": "instagram",
        "tiktok.com": "tiktok",
        "linkedin.com": "linkedin",
        "t.me": "telegram",
        "telegram.me": "telegram",
        "wa.me": "whatsapp",
        "whatsapp.com": "whatsapp",
        "mail.google.com": "email",
        "outlook.live.com": "email",
    }

    def _normalize(self, text: str | None) -> str:
        return re.sub(r"\s+", " ", str(text or "").strip().lower())

    def infer_network(self, url: str | None, *, fallback: str = "web") -> str:
        parsed = urlparse(str(url or ""))
        host = parsed.netloc.lower()
        path = parsed.path.lower()
        for marker, network in self._NETWORK_ALIASES.items():
            if marker in host or marker in path:
                return network
        if parsed.scheme == "mailto" or "@" in host and not parsed.scheme:
            return "email"
        if "qr" in host or "qr" in path:
            return "qr_code"
        return fallback if fallback in SOURCE_CHANNELS else "other"

    def infer_city(self, text: str | None) -> str:
        normalized = self._normalize(text)
        for city in self._CITY_HINTS:
            if city in normalized:
                return city.title()
        return ""

    def infer_property_type(self, text: str | None) -> str:
        normalized = self._normalize(text)
        for hint, label in self._PROPERTY_HINTS:
            if hint in normalized:
                return label
        return ""

    def infer_language(self, text: str | None) -> str:
        normalized = self._normalize(text)
        if not normalized:
            return "fr"
        french_markers = ("bonjour", "merci", "vente", "location", "appartement", "maison", "terrain", "quartier")
        english_markers = ("hello", "rent", "sale", "apartment", "house", "land", "district")
        french_hits = sum(1 for marker in french_markers if marker in normalized)
        english_hits = sum(1 for marker in english_markers if marker in normalized)
        return "en" if english_hits > french_hits else "fr"

    def extract_tags(self, text: str | None) -> list[str]:
        tags = re.findall(r"#([A-Za-z0-9_À-ÿ-]+)", str(text or ""))
        normalized: list[str] = []
        for tag in tags:
            cleaned = tag.strip().lower()
            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)
        return normalized

    def infer_format(self, text: str | None, url: str | None) -> str:
        if url and not str(text or "").strip():
            return "link"
        if str(text or "").strip():
            return "text"
        return "unknown"

    def infer_classification(self, *, network: str, text: str | None, url: str | None) -> str:
        normalized = self._normalize(text)
        if network in {"facebook", "instagram", "tiktok", "linkedin", "telegram", "whatsapp"}:
            return "social_post"
        if network in {"email", "sms"}:
            return "message"
        if network in {"qr_code", "flyer"}:
            return "offline_acquisition"
        if "partner" in normalized or "referral" in normalized:
            return "partner_referral"
        if url:
            return "web_publication"
        return "manual_import"

    def analyze(
        self,
        *,
        source_name: str,
        source_key: str,
        reference_code: str,
        url: str | None = None,
        title: str | None = None,
        text: str | None = None,
        author: str | None = None,
        campaign: str | None = None,
        city: str | None = None,
        district: str | None = None,
        property_type: str | None = None,
        target_audience: str | None = None,
        format_name: str | None = None,
        language: str | None = None,
        tags: list[str] | None = None,
        notes: str | None = None,
        network: str | None = None,
    ) -> dict[str, object]:
        normalized_text = self._normalize(text)
        inferred_network = network or self.infer_network(url, fallback="web")
        inferred_city = city or self.infer_city(normalized_text)
        inferred_property_type = property_type or self.infer_property_type(normalized_text)
        inferred_language = language or self.infer_language(text)
        inferred_format = format_name or self.infer_format(text, url)
        inferred_tags = list(dict.fromkeys((tags or []) + self.extract_tags(text) + [source_key, inferred_network]))
        confidence = 0.55
        if url:
            confidence += 0.15
        if title:
            confidence += 0.05
        if text:
            confidence += 0.1
        if inferred_city:
            confidence += 0.05
        if inferred_property_type:
            confidence += 0.05
        if inferred_tags:
            confidence += min(0.1, len(inferred_tags) * 0.02)
        confidence = round(min(0.99, confidence), 2)
        analysis = {
            "source_name": source_name,
            "source_key": source_key,
            "reference_code": reference_code,
            "url": url or "",
            "title": title or "",
            "text": text or "",
            "author": author or "",
            "campaign": campaign or "",
            "city": inferred_city,
            "district": district or "",
            "property_type": inferred_property_type,
            "target_audience": target_audience or DEFAULT_SOURCE_TARGET,
            "format": inferred_format,
            "language": inferred_language,
            "tags": inferred_tags,
            "network": inferred_network,
            "classification": self.infer_classification(network=inferred_network, text=text, url=url),
            "notes": notes or "",
        }
        return {
            "network": inferred_network,
            "publication_url": url or "",
            "publication_title": title or source_name,
            "publication_text": text or "",
            "publication_author": author or "",
            "campaign": campaign or "",
            "city": inferred_city,
            "district": district or "",
            "property_type": inferred_property_type,
            "target_audience": target_audience or DEFAULT_SOURCE_TARGET,
            "format": inferred_format,
            "language": inferred_language,
            "tags_json": inferred_tags,
            "ai_classification": analysis["classification"],
            "ai_confidence": confidence,
            "analysis_json": analysis,
            "notes": notes or "",
        }


class WhatsAppLinkEngine:
    def build_message(self, *, reference_code: str, source_name: str | None = None) -> str:
        label = source_name or "LAWIM source"
        return f"{label} {reference_code}".strip()

    def build_link(
        self,
        *,
        reference_code: str,
        source_name: str | None = None,
        phone_e164: str | None = None,
    ) -> str:
        number = (phone_e164 or PHONE_E164).lstrip("+")
        message = self.build_message(reference_code=reference_code, source_name=source_name)
        return f"https://wa.me/{number}?text={quote(message)}"


class DashboardEngine:
    def build_stats(self, rows: list[dict[str, object]]) -> dict[str, object]:
        total_sources = len(rows)
        active_sources = sum(1 for row in rows if str(row.get("status") or "") == "active")
        with_context = sum(1 for row in rows if row.get("publication_url") or row.get("publication_title"))
        total_leads = sum(int(row.get("lead_count") or 0) for row in rows)
        total_customers = sum(int(row.get("customer_count") or 0) for row in rows)
        total_whatsapp = sum(int(row.get("whatsapp_count") or 0) for row in rows)
        conversion_rate = round((total_customers / total_leads) * 100.0, 2) if total_leads else 0.0
        return {
            "sources_total": total_sources,
            "active_sources": active_sources,
            "sources_with_context": with_context,
            "leads_total": total_leads,
            "customers_total": total_customers,
            "whatsapp_messages_total": total_whatsapp,
            "conversion_rate": conversion_rate,
        }

    def top_sources(self, rows: list[dict[str, object]], *, limit: int = 10) -> list[dict[str, object]]:
        ranked = sorted(
            rows,
            key=lambda row: (
                int(row.get("lead_count") or 0),
                int(row.get("customer_count") or 0),
                str(row.get("created_at") or ""),
            ),
            reverse=True,
        )
        return ranked[:limit]
