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

_PCM_STRONG_MARKERS: set[str] = {
    "abeg", "wetin", "sabi", "komot", "broda", "sista",
    "pikin", "una", "wuna", "dey", "abi", "kom",
}

_PCM_BIGRAM_MARKERS: set[str] = {
    "no be", "wey dey", "make i", "i wan", "i di", "i dey", "i don",
    "i go", "e dey", "e don", "na so", "na which", "how much",
    "make we", "i no", "no vex", "na rent", "na buy", "don register",
    "i fit", "i sabi", "make dem", "na my", "na your", "na di",
    "wan make", "wan buy", "wan rent", "wan find", "dey find",
    "fit pay", "go check", "check am", "register am", "create am",
    "talk am", "tell dem", "make we go",
    "ma budget", "ma money", "ma house", "ma land", "ma car",
    "my money", "my budget", "my house", "my land",
    "make e", "e no", "make am", "make dem", "no pass",
    "na correct", "na good", "na fine", "na big",
}

_PCM_MARKERS: set[str] = {
    "dey", "na", "di", "wey", "fit", "abi", "komot", "wetin",
    "sabi", "abeg", "broda", "sista", "pikin", "una", "wuna", "ma",
}


class LawimLanguagePolicy:
    _MIN_SWITCH_COUNT = 2

    def detect_language(self, text: str) -> str | None:
        if not text or not text.strip():
            return None
        words = text.lower().split()
        word_set = set(words)
        if not word_set:
            return None
        text_lower = text.lower()

        # Explicit switch patterns
        for p in ['continue en français', 'parle français', 'utilise le français',
                  'continue en francais']:
            if p in text_lower: return "fr"
        for p in ['please continue in english', 'speak english', 'use english',
                  'continue en anglais', 'switch to english', 'english please',
                  'talk for english']:
            if p in text_lower: return "en"
        for p in ['abeg talk for pidgin', 'make we talk pidgin', 'speak pidgin',
                  'continue for pidgin', 'talk for pidgin']:
            if p in text_lower: return "pcm"

        # Strong PCM bigram markers (strip punctuation)
        import re as _re_pcm
        clean_words = [_re_pcm.sub(r'[^\w\s]', '', w) for w in words]
        bigram_hits = 0
        for i in range(len(clean_words) - 1):
            if clean_words[i] and clean_words[i+1]:
                bigram = clean_words[i] + " " + clean_words[i+1]
                if bigram in _PCM_BIGRAM_MARKERS:
                    bigram_hits += 1
        if bigram_hits >= 2:
            return "pcm"
        # Single bigram + PCM verb is strong enough
        if bigram_hits >= 1 and ("i" in word_set or "na" in word_set) and len(words) >= 3:
            pcm_verbs = {"wan", "dey", "fit", "sabi", "kom", "komot", "go"}
            if word_set & pcm_verbs:
                return "pcm"

        # Count markers
        fr_score = len(word_set & _FRENCH_MARKERS)
        en_score = len(word_set & _ENGLISH_MARKERS)
        pcm_score = len(word_set & _PCM_MARKERS)
        pcm_score += bigram_hits

        # Remove PCM false positives from EN
        en_score -= pcm_score // 2

        if fr_score > en_score and fr_score > pcm_score:
            return "fr"
        if pcm_score > en_score and pcm_score > fr_score:
            return "pcm"
        if en_score > 0 and en_score > fr_score and en_score > pcm_score:
            return "en"
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
        # Short messages never switch language alone
        if len(words) <= 3 and detected != current_language:
            return False
        # Real-estate domain terms in one language don't trigger switch
        domain_terms = {"house", "apartment", "studio", "villa", "land", "plot", "office",
                        "shop", "rent", "buy", "sale", "budget", "bedroom", "bedrooms",
                        "property", "month", "price", "city", "room", "flat", "maison",
                        "appartement", "terrain", "chambre", "location", "achat", "prix"}
        nondomain = [w for w in words if w.lower() not in domain_terms]
        if len(nondomain) < 2:
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
