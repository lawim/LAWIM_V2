from __future__ import annotations

from typing import Any


def collection_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "collection_key", "title", "domain", "description", "status")}


def document_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "document_key": row.get("document_key"),
        "title": row.get("title"),
        "format": row.get("format"),
        "status": row.get("status"),
        "author": row.get("author"),
        "category_key": row.get("category_key"),
        "collection_id": row.get("collection_id"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def article_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "article_key": row.get("article_key"),
        "title": row.get("title"),
        "slug": row.get("slug"),
        "status": row.get("status"),
        "summary": row.get("summary"),
        "published_at": row.get("published_at"),
        "document_id": row.get("document_id"),
    }


def category_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "category_key", "domain", "title", "parent_key", "description")}


def tag_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "tag_key", "label", "domain")}


def source_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "source_key", "title", "source_type", "url", "publisher", "trust_score")}


def citation_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "citation_key", "label", "source_ref", "page", "quote", "chunk_id")}


def reference_dto(row: dict[str, object]) -> dict[str, object]:
    return {k: row.get(k) for k in ("id", "from_document_id", "to_document_id", "reference_type", "label")}


def search_result_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "type": row.get("result_type"),
        "id": row.get("id"),
        "title": row.get("title"),
        "score": row.get("score"),
        "snippet": row.get("snippet"),
        "domain": row.get("domain"),
        "category_key": row.get("category_key"),
    }


def rag_dto(payload: dict[str, Any]) -> dict[str, object]:
    return {
        "query": payload.get("query"),
        "chunks": payload.get("chunks", []),
        "context": payload.get("context", {}),
        "citations": payload.get("citations", []),
    }
