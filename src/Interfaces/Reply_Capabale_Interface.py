"""Every Reply must implement a ReplyCapable interface"""
from abc import ABC, abstractmethod
from typing import Optional

from playwright.async_api import Page

from src.Interfaces.Message_Interface import message_interface
from src.Interfaces.Humanize_Operation_Interface import humanize_operation

class ReplyCapableInterface(ABC):
    """AAbstract class to represent ReplyCapable interface"""
    def __init__(self, page : Page):
        self.page = page
    @abstractmethod
    async def reply(self, Message : message_interface, humanize : humanize_operation, text : Optional[str]) -> bool:
        """Reply  to the message and returns True on success else False"""
        pass