from __future__ import annotations

import re


class ConversationResolver:
    WHATSAPP_NORMALIZE = re.compile(r"[^0-9+]")

    def resolve(
        self,
        channel: str,
        external_conversation_id: str,
        actor_id: int | str | None = None,
    ) -> tuple[str, bool]:
        if channel == "whatsapp":
            session_id = self._normalize_whatsapp(external_conversation_id)
        elif channel == "telegram":
            session_id = external_conversation_id
        elif channel == "web":
            user_part = str(actor_id or "anon")
            session_part = external_conversation_id or "default"
            session_id = f"{user_part}:{session_part}"
        else:
            session_id = external_conversation_id

        return session_id, False

    def _normalize_whatsapp(self, raw: str) -> str:
        cleaned = self.WHATSAPP_NORMALIZE.sub("", raw or "")
        if not cleaned:
            return raw
        digits = re.sub(r"\D", "", cleaned)
        if len(digits) == 12 and digits.startswith("237"):
            return f"+{digits}"
        if len(digits) == 9 and digits.startswith("6"):
            return f"+237{digits}"
        if digits:
            return f"+{digits}"
        return cleaned
