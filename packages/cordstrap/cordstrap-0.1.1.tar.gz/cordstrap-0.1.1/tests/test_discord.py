from cordstrap.discord import DiscordClient


def test_init_correct_headers() -> None:
    assert DiscordClient("token")._session.headers["Authorization"] == "Bot token"  # noqa: SLF001
