"""Message Processor Interface Must be implemented by every Message Processor implementation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from MessageInterface import Message_Interface

from Storage import Storage


class Message_Processor_Interface(ABC):
    """
    Message Processor Interface for Messages
    """
    Storage: Optional[Storage]

    @abstractmethod
    async def _get_wrapped_Messages(self, *args, **kwargs) -> List[Message_Interface]: pass

    @abstractmethod
    async def Fetcher(self, *args, **kwargs) -> List[Message_Interface]:
        """
        Returns the List of Total messages in that open Chat/Contact.
        Flexibility with batch processing & Safer Filtering approaches.
        """
        pass
