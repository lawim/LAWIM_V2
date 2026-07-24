from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
import urllib.error
from typing import Any

from ..llm import LLMAdapter, LLMContract

logger = logging.getLogger(__name__)


class OpenAIAdapter(LLMAdapter):
    provider_name = "openai"

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self._model = model

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        if not self._api_key:
            return LLMContract(intent="unknown", confidence=0.0)
        system = "Tu es un assistant immobilier. Analyse le message et retourne UNIQUEMENT un JSON valide avec : intent, confidence (0-1), entities (objet), missing_information (liste), summary, needs_clarification (bool). Ne prends aucune decision metier."
        messages = [{"role": "system", "content": system}, {"role": "user", "content": text}]
        payload = json.dumps({"model": self._model, "messages": messages, "temperature": 0.1, "max_tokens": 500}).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions", data=payload,
            headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                choice = data.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                return self._parse_response(content)
        except Exception as e:
            logger.error("OpenAI adapter error: %s", e)
            return LLMContract(intent="unknown", confidence=0.0)

    def _parse_response(self, content: str) -> LLMContract:
        try:
            data = json.loads(content) if content.startswith("{") else json.loads(content[content.index("{"):content.rindex("}")+1])
            return LLMContract(
                intent=data.get("intent", "unknown"),
                confidence=float(data.get("confidence", 0.0)),
                entities=data.get("entities", {}),
                missing_information=data.get("missing_information", []),
                summary=data.get("summary", ""),
                needs_clarification=bool(data.get("needs_clarification", False)),
                raw_response=content,
            )
        except (ValueError, KeyError, AttributeError):
            return LLMContract(intent="unknown", confidence=0.0, raw_response=content)


class DeepSeekAdapter(LLMAdapter):
    provider_name = "deepseek"

    def __init__(self, api_key: str | None = None, model: str = "deepseek-chat") -> None:
        self._api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self._model = model

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        if not self._api_key:
            return LLMContract(intent="unknown", confidence=0.0)
        system = "Tu es un assistant immobilier. Analyse le message et retourne UNIQUEMENT un JSON valide avec : intent, confidence, entities, missing_information, summary, needs_clarification."
        messages = [{"role": "system", "content": system}, {"role": "user", "content": text}]
        payload = json.dumps({"model": self._model, "messages": messages, "temperature": 0.1, "max_tokens": 500}).encode()
        req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions", data=payload,
                                     headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return OpenAIAdapter._parse_response(self, content)
        except Exception as e:
            logger.error("DeepSeek adapter error: %s", e)
            return LLMContract(intent="unknown", confidence=0.0)


class ClaudeAdapter(LLMAdapter):
    provider_name = "claude"

    def __init__(self, api_key: str | None = None, model: str = "claude-3-haiku-20240307") -> None:
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self._model = model

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        if not self._api_key:
            return LLMContract(intent="unknown", confidence=0.0)
        system = "Analyse ce message immobilier. Retourne UNIQUEMENT du JSON valide avec : intent, confidence (0-1), entities, missing_information, summary, needs_clarification."
        messages = [{"role": "user", "content": text}]
        payload = json.dumps({"model": self._model, "system": system, "messages": messages, "max_tokens": 500}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
                                     headers={"x-api-key": self._api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                content = " ".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
                return OpenAIAdapter._parse_response(self, content)
        except Exception as e:
            logger.error("Claude adapter error: %s", e)
            return LLMContract(intent="unknown", confidence=0.0)


class GeminiAdapter(LLMAdapter):
    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.0-flash") -> None:
        self._api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self._model = model

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        if not self._api_key:
            return LLMContract(intent="unknown", confidence=0.0)
        prompt = f"Analyse ce message immobilier. Retourne UNIQUEMENT du JSON avec : intent, confidence, entities, missing_information, summary, needs_clarification. Message: {text}"
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1, "maxOutputTokens": 500}}).encode()
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent?key={self._api_key}",
                                     data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                candidates = data.get("candidates", [])
                text_content = ""
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text_content = " ".join(p.get("text", "") for p in parts)
                return OpenAIAdapter._parse_response(self, text_content)
        except Exception as e:
            logger.error("Gemini adapter error: %s", e)
            return LLMContract(intent="unknown", confidence=0.0)


class MistralAdapter(LLMAdapter):
    provider_name = "mistral"

    def __init__(self, api_key: str | None = None, model: str = "mistral-small-latest") -> None:
        self._api_key = api_key or os.getenv("MISTRAL_API_KEY", "")
        self._model = model

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        if not self._api_key:
            return LLMContract(intent="unknown", confidence=0.0)
        system = "Analyse ce message immobilier. Retourne UNIQUEMENT du JSON valide."
        messages = [{"role": "system", "content": system}, {"role": "user", "content": text}]
        payload = json.dumps({"model": self._model, "messages": messages, "temperature": 0.1, "max_tokens": 500}).encode()
        req = urllib.request.Request("https://api.mistral.ai/v1/chat/completions", data=payload,
                                     headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return OpenAIAdapter._parse_response(self, content)
        except Exception as e:
            logger.error("Mistral adapter error: %s", e)
            return LLMContract(intent="unknown", confidence=0.0)
