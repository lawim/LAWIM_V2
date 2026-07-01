from __future__ import annotations

import hashlib
import re
from typing import Any

from .constants import DEFAULT_CHUNK_SIZE, DEFAULT_EMBEDDING_MODEL


class ChunkingEngine:
    def chunk(self, text: str, *, chunk_size: int = DEFAULT_CHUNK_SIZE) -> list[str]:
        words = text.split()
        if not words:
            return []
        chunks: list[str] = []
        current: list[str] = []
        length = 0
        for word in words:
            if length + len(word) + 1 > chunk_size and current:
                chunks.append(" ".join(current))
                current = [word]
                length = len(word)
            else:
                current.append(word)
                length += len(word) + 1
        if current:
            chunks.append(" ".join(current))
        return chunks


class LexicalIndexEngine:
    def normalize(self, text: str) -> str:
        lowered = text.lower()
        cleaned = re.sub(r"[^a-zàâäéèêëïîôùûüç0-9\s]", " ", lowered)
        return re.sub(r"\s+", " ", cleaned).strip()

    def tokenize(self, text: str) -> list[str]:
        return [token for token in self.normalize(text).split() if len(token) > 2]

    def build_lexical_index(self, text: str) -> str:
        return " ".join(sorted(set(self.tokenize(text))))


class SemanticIndexEngine:
    """Deterministic pseudo-embedding — architecture prête pour vecteurs réels."""

    def embed(self, text: str, *, dimensions: int = 16) -> list[float]:
        tokens = LexicalIndexEngine().tokenize(text)
        if not tokens:
            return [0.0] * dimensions
        vector = [0.0] * dimensions
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index in range(dimensions):
                vector[index] += digest[index % len(digest)] / 255.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [round(value / norm, 6) for value in vector]


class RankingEngine:
    def score_lexical(self, query: str, content: str) -> int:
        tokens = set(LexicalIndexEngine().tokenize(query))
        if not tokens:
            return 0
        haystack = LexicalIndexEngine().normalize(content)
        hits = sum(1 for token in tokens if token in haystack)
        return min(100, hits * 18)

    def rerank(self, rows: list[dict[str, object]], *, query: str) -> list[dict[str, object]]:
        for row in rows:
            base = int(row.get("score", 0))
            freshness = int(row.get("freshness_score", 70))
            confidence = int(row.get("confidence_score", 70))
            row["score"] = min(100, base + freshness // 10 + confidence // 10)
        return sorted(rows, key=lambda row: int(row.get("score", 0)), reverse=True)


class CitationEngine:
    def build_citations(self, chunk_content: str, *, source_label: str) -> list[dict[str, object]]:
        excerpt = chunk_content[:160].strip()
        if not excerpt:
            return []
        return [{"label": source_label, "quote": excerpt, "source_ref": source_label}]


class RAGFoundationEngine:
    def __init__(self) -> None:
        self.chunker = ChunkingEngine()
        self.lexical = LexicalIndexEngine()
        self.semantic = SemanticIndexEngine()
        self.ranking = RankingEngine()
        self.citations = CitationEngine()

    def retrieve(
        self,
        *,
        query: str,
        chunks: list[dict[str, object]],
        limit: int = 8,
        domain: str | None = None,
        category: str | None = None,
        tag: str | None = None,
    ) -> list[dict[str, object]]:
        filtered = chunks
        if domain:
            filtered = [c for c in filtered if str(c.get("domain", "")) == domain or not c.get("domain")]
        if category:
            filtered = [c for c in filtered if str(c.get("category_key", "")) == category or not c.get("category_key")]
        if tag:
            filtered = [c for c in filtered if tag in (c.get("tags") or [])]
        scored = [
            {
                **chunk,
                "score": self.ranking.score_lexical(query, str(chunk.get("content", ""))),
                "provenance": chunk.get("source_key") or chunk.get("document_key"),
            }
            for chunk in filtered
        ]
        ranked = self.ranking.rerank(scored, query=query)
        return [row for row in ranked if int(row.get("score", 0)) > 0][:limit]

    def build_context(self, chunks: list[dict[str, object]]) -> dict[str, object]:
        return {
            "chunks": chunks,
            "context_size": sum(len(str(c.get("content", ""))) for c in chunks),
            "citations": [
                cite
                for chunk in chunks
                for cite in self.citations.build_citations(str(chunk.get("content", "")), source_label=str(chunk.get("title", "source")))
            ],
            "confidence": round(sum(int(c.get("confidence_score", 70)) for c in chunks) / max(len(chunks), 1), 2),
            "freshness": round(sum(int(c.get("freshness_score", 70)) for c in chunks) / max(len(chunks), 1), 2),
        }

    def deterministic_embedding_record(self, chunk_id: int, content: str) -> dict[str, object]:
        vector = self.semantic.embed(content)
        return {
            "chunk_id": chunk_id,
            "model_key": DEFAULT_EMBEDDING_MODEL,
            "vector_json": vector,
            "dimensions": len(vector),
        }
