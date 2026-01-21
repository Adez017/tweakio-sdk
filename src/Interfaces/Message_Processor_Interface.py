"""Message Processor Interface Must be implemented by every Message Processor implementation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.Interfaces.Chat_Interface import chat_interface
from src.MessageFilter import Filter
from Message_Interface import message_interface
from sql_lite_storage import SQL_Lite_Storage


class message_processor_interface(ABC):
    """
    Message Processor Interface for Messages
    """

    def __init__(
            self,
            storage_obj: Optional[SQL_Lite_Storage] = None,
            filter_obj: Optional[Filter] = None
    ) -> None:
        self.storage = storage_obj
        self.filter = filter_obj

    @abstractmethod
    async def _get_wrapped_Messages(self, retry: int, *args, **kwargs) -> List[message_interface]: pass

    @abstractmethod
    async def Fetcher(self, chat: chat_interface, retry: int, *args, **kwargs) -> List[message_interface]:
        """
        Returns the List of Total messages in that open Chat/Contact.
        Flexibility with batch processing & Safer Filtering approaches.
        """
        pass
