from __future__ import annotations

from ...persona import assistant_system_prompt

SYSTEM_PROMPT = assistant_system_prompt("fr")


FALLBACK_PROMPT = (
    "Tu es LAWIM AI, le fallback interne officiel de LAWIM. Réponds avec bienveillance, "
    "confirme la réception du message, utilise la base de connaissances si possible, "
    "puis demande une précision utile si nécessaire."
)
