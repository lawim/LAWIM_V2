from ..project.model import ProjectRuntime
from ..project.status import ProjectStatus, ProjectType, ProjectStage


def test_project_creation():
    p = ProjectRuntime(project_type=ProjectType.BUY, owner="user1")
    assert p.project_id
    assert p.status == ProjectStatus.DRAFT
    assert p.stage == ProjectStage.INITIAL
    assert p.priority == 0


def test_project_to_dict():
    p = ProjectRuntime(project_type=ProjectType.RENT, owner="user2")
    d = p.to_dict()
    assert d["project_type"] == "RENT"
    assert d["status"] == "DRAFT"
    assert d["owner"] == "user2"


def test_project_with_profile():
    p = ProjectRuntime(
        project_type=ProjectType.BUY,
        owner="user3",
        profile={"city": "Douala", "budget_max": 100000},
    )
    assert p.profile["city"] == "Douala"
    assert p.profile["budget_max"] == 100000


def test_project_stage_updates():
    p = ProjectRuntime()
    assert p.stage == ProjectStage.INITIAL
    p.status = ProjectStatus.QUALIFYING
    assert p.stage == ProjectStage.QUALIFICATION
    p.status = ProjectStatus.MATCHING
    assert p.stage == ProjectStage.SEARCH
