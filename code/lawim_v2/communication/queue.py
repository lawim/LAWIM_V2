from __future__ import annotations

from .engines import CommunicationPlatformEngine


class QueueModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().queue

    def enqueue(self, **kwargs: object) -> dict[str, object]:
        return self.repository.enqueue_message(**kwargs)

    def list_jobs(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_queue_jobs(**kwargs)

    def retry(self, job_id: int) -> dict[str, object]:
        return self.repository.retry_job(job_id)

    def process_next(self) -> dict[str, object] | None:
        return self.repository.process_next_queue_job()
