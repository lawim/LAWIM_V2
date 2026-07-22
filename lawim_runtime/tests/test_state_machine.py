from ..project.status import ProjectStatus, VALID_TRANSITIONS, STAGE_MAP, ProjectStage
from ..runtime.state_machine import RuntimeStateMachine
from ..runtime.errors import InvalidTransitionError


def test_draft_to_active():
    result = RuntimeStateMachine.transition(ProjectStatus.DRAFT, ProjectStatus.ACTIVE)
    assert result == ProjectStatus.ACTIVE


def test_invalid_transition():
    try:
        RuntimeStateMachine.transition(ProjectStatus.DRAFT, ProjectStatus.COMPLETED)
        assert False, "Should have raised"
    except InvalidTransitionError:
        pass


def test_can_transition():
    assert RuntimeStateMachine.can_transition(ProjectStatus.DRAFT, ProjectStatus.ACTIVE)
    assert not RuntimeStateMachine.can_transition(
        ProjectStatus.DRAFT, ProjectStatus.COMPLETED
    )


def test_full_journey():
    path = [
        (ProjectStatus.DRAFT, ProjectStatus.ACTIVE),
        (ProjectStatus.ACTIVE, ProjectStatus.QUALIFYING),
        (ProjectStatus.QUALIFYING, ProjectStatus.MATCHING),
        (ProjectStatus.MATCHING, ProjectStatus.VISIT_PENDING),
        (ProjectStatus.VISIT_PENDING, ProjectStatus.NEGOTIATING),
        (ProjectStatus.NEGOTIATING, ProjectStatus.TRANSACTION_PENDING),
        (ProjectStatus.TRANSACTION_PENDING, ProjectStatus.COMPLETED),
        (ProjectStatus.COMPLETED, ProjectStatus.ARCHIVED),
    ]
    for current, target in path:
        assert RuntimeStateMachine.can_transition(
            current, target
        ), f"Cannot go {current.value} -> {target.value}"


def test_cancellation_at_any_stage():
    for status in ProjectStatus:
        if status not in (ProjectStatus.CANCELLED, ProjectStatus.ARCHIVED):
            can_cancel = RuntimeStateMachine.can_transition(
                status, ProjectStatus.CANCELLED
            )
            expected = status != ProjectStatus.COMPLETED
            assert can_cancel == expected, (
                f"Cancellation from {status.value}: expected {expected}"
            )


def test_next_statuses():
    next_s = RuntimeStateMachine.next_statuses(ProjectStatus.DRAFT)
    assert ProjectStatus.ACTIVE in next_s
    assert ProjectStatus.CANCELLED in next_s
    assert ProjectStatus.COMPLETED not in next_s


def test_stage_map_consistency():
    for status, stage in STAGE_MAP.items():
        assert isinstance(stage, ProjectStage), f"{status.value} -> {stage}"
