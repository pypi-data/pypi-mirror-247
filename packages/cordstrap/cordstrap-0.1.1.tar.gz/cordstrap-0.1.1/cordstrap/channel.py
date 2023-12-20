import re
from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

TEXT_NAME_PATTERN = re.compile(r"^[a-z0-9-]{2,100}$")
VOICE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9- ]{2,100}$")


class Channel(BaseModel):
    name: str
    kind: Literal["text", "voice"] = "text"
    topic: str = Field(default="", max_length=1024)

    @model_validator(mode="after")
    def check_name(self) -> Self:
        pattern = TEXT_NAME_PATTERN if self.kind == "text" else VOICE_NAME_PATTERN

        if not pattern.match(self.name):
            raise ValueError(
                f"String should match pattern {pattern} for {self.kind} channel",
            )

        return self
