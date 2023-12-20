from pathlib import Path

import typer
from pydantic_yaml import parse_yaml_file_as

from cordstrap.discord import DiscordClient
from cordstrap.template import Template


def main_command(
    token: str,
    guild_id: int,
    template_path: Path = Path("server.cordstrap.yaml"),
) -> None:
    client = DiscordClient(token)

    template = parse_yaml_file_as(Template, template_path)

    client.update_guild(guild_id, {"name": template.name})

    for channel in template.channels:
        client.create_channel(guild_id, channel)


def main() -> None:
    typer.run(main_command)


if __name__ == "__main__":
    main()
