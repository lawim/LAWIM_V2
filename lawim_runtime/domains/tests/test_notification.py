from lawim_runtime.domains.notification import NotificationHandler, NotificationRuntime
from lawim_runtime.domains.notification.models import NotificationStatus
from lawim_runtime.domains.notification.events import NotificationEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-notif",
    )
    return runtime.execute(req)


def test_notification_prepare():
    runtime = NotificationRuntime()
    result = _execute(runtime, "PREPARE_NOTIFICATION", {
        "project_id": "proj-001",
        "template_name": "visit_confirmation",
        "recipient_type": "buyer",
        "channel": "whatsapp",
        "parameters": {"visit_date": "2026-07-25"},
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == NotificationStatus.PREPARED.value
    assert result.output["notification_id"] != ""
    assert result.output["deduplicated"] is False


def test_notification_schedule():
    runtime = NotificationRuntime()
    prep = _execute(runtime, "PREPARE_NOTIFICATION", {
        "project_id": "proj-001",
        "template_name": "visit_confirmation",
        "recipient_type": "buyer",
        "channel": "whatsapp",
    })
    notif_id = prep.output["notification_id"]

    sched = _execute(runtime, "SCHEDULE_NOTIFICATION", {
        "project_id": "proj-001",
        "template_name": "visit_confirmation",
        "notification_id": notif_id,
    })
    assert sched.output["status"] == NotificationStatus.SCHEDULED.value
    assert sched.output["notification_id"] == notif_id


def test_notification_cancel():
    runtime = NotificationRuntime()
    prep = _execute(runtime, "PREPARE_NOTIFICATION", {
        "project_id": "proj-001",
        "template_name": "cancel_test",
        "recipient_type": "buyer",
        "channel": "whatsapp",
    })
    notif_id = prep.output["notification_id"]

    cancel = _execute(runtime, "CANCEL_NOTIFICATION", {
        "project_id": "proj-001",
        "template_name": "cancel_test",
        "notification_id": notif_id,
    })
    assert cancel.output["status"] == NotificationStatus.CANCELLED.value


def test_notification_duplicate():
    runtime = NotificationRuntime()
    params = {
        "project_id": "proj-dup",
        "template_name": "dup_template",
        "recipient_type": "buyer",
        "channel": "whatsapp",
    }
    r1 = _execute(runtime, "PREPARE_NOTIFICATION", params)
    assert r1.output["deduplicated"] is False

    r2 = _execute(runtime, "PREPARE_NOTIFICATION", params)
    assert r2.output["deduplicated"] is True
    assert r2.output["notification_id"] == r1.output["notification_id"]


def test_notification_event_produced():
    assert NotificationEventType.NOTIFICATION_PREPARED.value == "NOTIFICATION_PREPARED"
    assert NotificationEventType.NOTIFICATION_SCHEDULED.value == "NOTIFICATION_SCHEDULED"
    assert NotificationEventType.NOTIFICATION_CANCELLED.value == "NOTIFICATION_CANCELLED"
    assert NotificationEventType.NOTIFICATION_SENT.value == "NOTIFICATION_SENT"
    assert NotificationEventType.NOTIFICATION_FAILED.value == "NOTIFICATION_FAILED"
    assert len(NotificationEventType) == 6
