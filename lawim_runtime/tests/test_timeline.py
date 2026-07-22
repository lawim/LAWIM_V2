from ..project.timeline import Timeline, TimelineEntry


def test_timeline_append():
    tl = Timeline()
    entry = TimelineEntry(project_id="p1", event_type="TEST")
    tl.append(entry)
    assert len(tl.get_entries("p1")) == 1


def test_timeline_filter():
    tl = Timeline()
    tl.append(TimelineEntry(project_id="p1", event_type="A"))
    tl.append(TimelineEntry(project_id="p2", event_type="B"))
    tl.append(TimelineEntry(project_id="p1", event_type="C"))
    assert len(tl.get_entries("p1")) == 2
    assert len(tl.get_entries("p2")) == 1
    assert len(tl.get_entries()) == 3


def test_timeline_replay():
    tl = Timeline()
    tl.append(TimelineEntry(project_id="p1", event_type="A"))
    tl.append(TimelineEntry(project_id="p1", event_type="B"))
    entries = tl.replay("p1", from_index=1)
    assert len(entries) == 1
    assert entries[0].event_type == "B"
