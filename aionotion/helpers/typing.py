"""Define typing helpers."""
from typing import TypeVar

from pydantic.v1 import BaseModel

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
