"""Define model helpers."""
from pydantic import BaseModel, ConfigDict


class NotionBaseModel(BaseModel):
    """Define a Notion-specific base model."""

    model_config = ConfigDict(frozen=True)
