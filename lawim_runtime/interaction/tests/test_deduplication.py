from lawim_runtime.interaction.deduplication import InteractionDeduplicator, DeduplicationStatus


def test_new_message():
    dedup = InteractionDeduplicator()
    status = dedup.check("msg-001", "whatsapp")
    assert status == DeduplicationStatus.NEW


def test_duplicate_message():
    dedup = InteractionDeduplicator()
    dedup.check("msg-001", "whatsapp")
    status = dedup.check("msg-001", "whatsapp")
    assert status == DeduplicationStatus.DUPLICATE


def test_same_id_different_channel():
    dedup = InteractionDeduplicator()
    dedup.check("msg-001", "whatsapp")
    status = dedup.check("msg-001", "telegram")
    assert status == DeduplicationStatus.NEW


def test_delivery_deduplication():
    dedup = InteractionDeduplicator()
    assert dedup.is_delivery_duplicate("del-001") is False
    assert dedup.is_delivery_duplicate("del-001") is True


def test_empty_id():
    dedup = InteractionDeduplicator()
    status = dedup.check("", "whatsapp")
    assert status == DeduplicationStatus.NEW
