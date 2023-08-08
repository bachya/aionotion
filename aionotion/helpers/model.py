"""Define model helpers."""
from typing import TypeVar

from pydantic import BaseModel, ConfigDict


class NotionBaseModel(BaseModel):
    """Define a Notion-specific base model."""

    model_config = ConfigDict(frozen=True)


NotionBaseModelT = TypeVar("NotionBaseModelT", bound=NotionBaseModel)
