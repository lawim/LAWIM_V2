from lawim_runtime.interaction.normalization import MessageNormalizer


def test_normalize_trim():
    n = MessageNormalizer()
    result = n.normalize("  hello world  ")
    assert result.normalized_content == "hello world"


def test_empty_content():
    n = MessageNormalizer()
    result = n.normalize("")
    assert result.is_empty is True


def test_is_empty_noise():
    n = MessageNormalizer()
    assert n.is_empty_or_noise("...") is True
    assert n.is_empty_or_noise("hello") is False


def test_normalize_unicode_spaces():
    n = MessageNormalizer()
    result = n.normalize("hello\u00a0world")
    assert result.normalized_content == "hello world"


def test_normalize_multiline_whatsapp():
    n = MessageNormalizer()
    result = n.normalize("hello\nworld", channel="whatsapp")
    assert " " in result.normalized_content
