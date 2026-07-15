from __future__ import annotations

from enum import Enum


class Direction(str, Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    INTERNAL = "INTERNAL"
    SYSTEM = "SYSTEM"

    @classmethod
    def from_communication_direction(cls, d: str) -> Direction:
        mapping = {"inbound": Direction.INBOUND, "outbound": Direction.OUTBOUND,
                    "internal": Direction.INTERNAL}
        return mapping.get(d.lower(), Direction.SYSTEM)


class ContentType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    LOCATION = "LOCATION"
    CONTACT = "CONTACT"
    PROPERTY = "PROPERTY"
    PAYMENT = "PAYMENT"
    SYSTEM_EVENT = "SYSTEM_EVENT"

    @classmethod
    def from_mime(cls, mime: str) -> ContentType:
        if not mime:
            return ContentType.TEXT
        m = mime.lower()
        if m.startswith("image/"):
            return ContentType.IMAGE
        if m.startswith("audio/"):
            return ContentType.AUDIO
        if m.startswith("video/"):
            return ContentType.VIDEO
        if any(x in m for x in ("pdf", "document", "sheet", "text/plain", "application/")):
            return ContentType.DOCUMENT
        return ContentType.TEXT


class ExchangeType(str, Enum):
    INFORMATION_REQUEST = "INFORMATION_REQUEST"
    PROPERTY_SEARCH = "PROPERTY_SEARCH"
    PROPERTY_OFFER = "PROPERTY_OFFER"
    QUALIFICATION = "QUALIFICATION"
    MATCHING = "MATCHING"
    VISIT_REQUEST = "VISIT_REQUEST"
    NEGOTIATION = "NEGOTIATION"
    DOCUMENT_REQUEST = "DOCUMENT_REQUEST"
    PAYMENT = "PAYMENT"
    COMPLAINT = "COMPLAINT"
    SUPPORT = "SUPPORT"
    RELATIONSHIP_FOLLOW_UP = "RELATIONSHIP_FOLLOW_UP"
    HUMAN_HANDOVER = "HUMAN_HANDOVER"

    @classmethod
    def from_intent(cls, intent: str | None) -> ExchangeType:
        if not intent:
            return ExchangeType.INFORMATION_REQUEST
        i = intent.upper()
        if "BUY" in i or "RENT" in i or "SEARCH" in i:
            return ExchangeType.PROPERTY_SEARCH
        if "SELL" in i or "OFFER" in i:
            return ExchangeType.PROPERTY_OFFER
        if "QUALIF" in i:
            return ExchangeType.QUALIFICATION
        if "MATCH" in i:
            return ExchangeType.MATCHING
        if "VISIT" in i:
            return ExchangeType.VISIT_REQUEST
        if "NEGO" in i:
            return ExchangeType.NEGOTIATION
        if "DOC" in i:
            return ExchangeType.DOCUMENT_REQUEST
        if "PAY" in i or "PAIEM" in i:
            return ExchangeType.PAYMENT
        if "HANDOVER" in i or "HUMAIN" in i or "AGENT" in i:
            return ExchangeType.HUMAN_HANDOVER
        if "SUPPORT" in i or "AIDE" in i or "ASSIST" in i:
            return ExchangeType.SUPPORT
        if "RELATION" in i or "FOLLOW" in i:
            return ExchangeType.RELATIONSHIP_FOLLOW_UP
        return ExchangeType.INFORMATION_REQUEST


class ExchangeResult(str, Enum):
    RECEIVED = "RECEIVED"
    UNDERSTOOD = "UNDERSTOOD"
    ANSWERED = "ANSWERED"
    ACTION_TRIGGERED = "ACTION_TRIGGERED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"
    IGNORED = "IGNORED"
    DUPLICATE = "DUPLICATE"
