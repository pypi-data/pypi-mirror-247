from dataclasses import dataclass, field
from typing import Any

import requests

from cordstrap.channel import Channel


@dataclass
class DiscordClient:
    token: str

    _session: requests.Session = field(init=False, default_factory=requests.Session)

    def __post_init__(self) -> None:
        self._session.headers.update({"Authorization": f"Bot {self.token}"})

    def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any],
    ) -> requests.Response:
        return self._session.request(
            method,
            f"https://discord.com/api/v8/{path}",
            json=json,
        )

    def create_channel(self, guild_id: int, channel: Channel) -> None:
        self._request(
            "POST",
            f"guilds/{guild_id}/channels",
            json={
                "name": channel.name,
                "type": 0 if channel.kind == "text" else 2,
                "topic": channel.topic,
            },
        )

    def update_guild(self, guild_id: int, data: dict[str, Any]) -> None:
        self._request(
            "PATCH",
            f"guilds/{guild_id}",
            json=data,
        )
