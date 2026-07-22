from __future__ import annotations

from abc import ABC, abstractmethod

from .models import DocumentData


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: DocumentData) -> None:
        ...

    @abstractmethod
    def get(self, doc_id: str) -> DocumentData | None:
        ...

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[DocumentData]:
        ...

    @abstractmethod
    def list_by_status(self, status: str) -> list[DocumentData]:
        ...

    @abstractmethod
    def update_status(self, doc_id: str, new_status: str) -> None:
        ...


class InMemoryDocumentRepository(DocumentRepository):

    def __init__(self) -> None:
        self._documents: dict[str, DocumentData] = {}

    def save(self, document: DocumentData) -> None:
        self._documents[document.doc_id] = document

    def get(self, doc_id: str) -> DocumentData | None:
        return self._documents.get(doc_id)

    def list_by_project(self, project_id: str) -> list[DocumentData]:
        return [d for d in self._documents.values() if d.project_id == project_id]

    def list_by_status(self, status: str) -> list[DocumentData]:
        return [d for d in self._documents.values() if d.status == status]

    def update_status(self, doc_id: str, new_status: str) -> None:
        doc = self._documents.get(doc_id)
        if doc:
            doc.status = new_status
