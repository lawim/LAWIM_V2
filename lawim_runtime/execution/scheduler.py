from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from ..runtime.errors import RuntimeError
from .plan import ActionExecutionPlan
from .request import ActionExecutionRequest


class SchedulerError(RuntimeError):
    pass


class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    DISPATCHED = "DISPATCHED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(order=True)
class ScheduledTask:
    priority: int
    scheduled_at: datetime
    schedule_id: str = ""
    request: ActionExecutionRequest | None = None
    plan: ActionExecutionPlan | None = None
    status: TaskStatus = TaskStatus.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.schedule_id:
            self.schedule_id = str(uuid4())


class ExecutionScheduler:
    def __init__(self) -> None:
        self._queue: list[ScheduledTask] = []
        self._tasks: dict[str, ScheduledTask] = {}
        self._max_queue_size: int = 10000
        self._default_priority: int = 100

    @property
    def queue_size(self) -> int:
        return len(self._queue)

    @property
    def task_count(self) -> int:
        return len(self._tasks)

    def schedule(
        self,
        execution_request: ActionExecutionRequest,
        plan: ActionExecutionPlan,
        priority: int | None = None,
    ) -> str:
        if self.queue_size >= self._max_queue_size:
            raise SchedulerError("Queue is full, cannot schedule more tasks")

        task = ScheduledTask(
            priority=priority if priority is not None else execution_request.priority,
            scheduled_at=datetime.now(timezone.utc),
            request=execution_request,
            plan=plan,
        )
        self._queue.append(task)
        self._tasks[task.schedule_id] = task
        self._queue.sort(key=lambda t: (t.priority, t.scheduled_at))
        return task.schedule_id

    def prioritize(self, schedule_id: str, priority: int) -> None:
        task = self._tasks.get(schedule_id)
        if task is None:
            raise SchedulerError(f"Task '{schedule_id}' not found")
        task.priority = priority
        self._queue.sort(key=lambda t: (t.priority, t.scheduled_at))

    def dequeue(self) -> ScheduledTask | None:
        if not self._queue:
            return None
        task = self._queue.pop(0)
        task.status = TaskStatus.DISPATCHED
        return task

    def peek(self) -> ScheduledTask | None:
        if not self._queue:
            return None
        return self._queue[0]

    def cancel(self, schedule_id: str) -> bool:
        task = self._tasks.get(schedule_id)
        if task is None:
            return False
        task.status = TaskStatus.CANCELLED
        self._queue[:] = [t for t in self._queue if t.schedule_id != schedule_id]
        return True

    def get_task(self, schedule_id: str) -> ScheduledTask | None:
        return self._tasks.get(schedule_id)

    def list_pending(self) -> list[ScheduledTask]:
        return [t for t in self._tasks.values() if t.status == TaskStatus.QUEUED]

    def clear(self) -> None:
        self._queue.clear()
        self._tasks.clear()
