import pytest

from cordstrap.channel import Channel


def test_name_validation() -> None:
    assert Channel(name="general").name == "general"

    with pytest.raises(ValueError, match="String should match pattern"):
        Channel(name="General!")

    with pytest.raises(ValueError, match="String should match pattern"):
        Channel(name="{", kind="voice")


def test_kind_validation() -> None:
    assert Channel(name="general", kind="text").kind == "text"

    with pytest.raises(ValueError, match="Input should be 'text' or 'voice'"):
        Channel(name="general", kind="invalid")  # type: ignore[arg-type]


def test_topic_validation() -> None:
    assert Channel(name="general", topic="Talk about stuff").topic == "Talk about stuff"

    with pytest.raises(ValueError, match="should have at most 1024 characters"):
        Channel(name="general", topic="x" * 1025)
