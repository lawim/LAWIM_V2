from lawim_runtime.interaction.project_resolution import ProjectResolver, ProjectResolutionStatus


def test_new_project():
    resolver = ProjectResolver()
    result = resolver.resolve("user-001")
    assert result.status == ProjectResolutionStatus.NEW_PROJECT


def test_single_active():
    resolver = ProjectResolver()
    resolver.register_project("user-001", "proj-001")
    result = resolver.resolve("user-001")
    assert result.status == ProjectResolutionStatus.RESOLVED
    assert result.project_id == "proj-001"


def test_multiple_active():
    resolver = ProjectResolver()
    resolver.register_project("user-001", "proj-001")
    resolver.register_project("user-001", "proj-002")
    result = resolver.resolve("user-001")
    assert result.status == ProjectResolutionStatus.AMBIGUOUS
    assert len(result.candidate_ids) == 2


def test_closed_project():
    resolver = ProjectResolver()
    resolver.register_project("user-001", "proj-001", status="closed")
    result = resolver.resolve("user-001")
    assert result.status == ProjectResolutionStatus.CLOSED


def test_no_user():
    resolver = ProjectResolver()
    result = resolver.resolve("")
    assert result.status == ProjectResolutionStatus.NOT_FOUND
