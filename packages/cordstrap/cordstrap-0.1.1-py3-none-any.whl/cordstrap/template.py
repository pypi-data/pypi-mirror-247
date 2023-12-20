from pydantic import BaseModel

from cordstrap.channel import Channel


class Template(BaseModel):
    name: str
    channels: list[Channel]
