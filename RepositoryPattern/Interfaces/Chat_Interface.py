"""
This is an ChatInterFace to implement and usage
for every Platform Chat Based Objects.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from playwright.async_api import ElementHandle


class chat_interface(ABC):
    """Interface for Chat for every Platform """

    chatName: Optional[str]
    chatID: Optional[str]
    ChatUI: Optional[Union[ElementHandle, Locator]]
    System_Hit_Time: float

    @staticmethod
    @abstractmethod
    async def _chat_key(*args, **kwargs) -> str:
        """Returns the Unique key of the chat Object"""
        pass
