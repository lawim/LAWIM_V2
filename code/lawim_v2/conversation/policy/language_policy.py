from __future__ import annotations

_FRENCH_MARKERS: set[str] = {
    "bonjour", "je", "j'", "mon", "ma", "mes", "ton", "ta", "ses",
    "nous", "vous", "ils", "elles", "le", "la", "les", "un", "une",
    "des", "du", "au", "aux", "est", "sont", "dans", "pour", "avec",
    "sur", "que", "qui", "quoi", "comment", "pourquoi", "quand", "ou",
    "où", "merci", "s'il vous plaît", "s'il te plaît", "svp", "stp",
}

_ENGLISH_MARKERS: set[str] = {
    "hello", "hi", "the", "a", "an", "my", "your", "his", "her",
    "our", "their", "i", "you", "he", "she", "it", "we", "they",
    "is", "are", "was", "were", "in", "on", "at", "for", "with",
    "to", "from", "this", "that", "please", "thank", "would", "could",
    "should", "want", "need",
}

_PCM_MARKERS: set[str] = {
    "dey", "na", "di", "wey", "fit", "abi", "komot", "wetin",
    "make", "sabi", "abeg", "broda", "sista",
}


class LawimLanguagePolicy:
    _MIN_SWITCH_COUNT = 2

    def detect_language(self, text: str) -> str | None:
        if not text or not text.strip():
            return None
        words = set(text.lower().split())
        if not words:
            return None
        fr_score = len(words & _FRENCH_MARKERS)
        en_score = len(words & _ENGLISH_MARKERS)
        pcm_score = len(words & _PCM_MARKERS)
        en_score -= pcm_score // 2
        if fr_score > en_score and fr_score > pcm_score:
            return "fr"
        if pcm_score > en_score and pcm_score > fr_score:
            return "pcm"
        if en_score > 0:
            return "en"
        return None

    def should_switch(
        self,
        current_language: str,
        detected: str | None,
        message: str,
        previous_messages_in_other_lang: int = 0,
    ) -> bool:
        if current_language == "fr" and detected is None:
            return False
        lower_msg = message.lower()
        if current_language == "fr" and "i don't understand english" in lower_msg:
            return False
        if detected is None or detected == current_language:
            return False
        words = message.strip().split()
        if len(words) <= 3 and detected != current_language:
            return False
        if previous_messages_in_other_lang < self._MIN_SWITCH_COUNT:
            return False
        return True

    def is_translation(self, text: str) -> bool:
        lower = text.lower()
        translation_markers = [
            "french for", "in english", "in french",
            "fran\u00e7ais signifie", "en anglais",
        ]
        return any(marker in lower for marker in translation_markers)

    def is_grammar_correction(self, text: str) -> bool:
        lower = text.lower()
        grammar_markers = [
            "correct spelling is", "the correct phrasing",
            "you wrote", "vous avez \u00e9crit",
            "l'orthographe correcte", "la bonne orthographe",
        ]
        return any(marker in lower for marker in grammar_markers)
