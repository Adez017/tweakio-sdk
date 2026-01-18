"""WhatsApp Message Class contracted with Message Interface Template"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Union

from playwright.async_api import ElementHandle, Locator

from RepositoryPattern.Interfaces.Message_Interface import Message_interface
from Chat import whatsapp_chat


@dataclass
class WhatsappMessage(Message_interface):
    """WhatsApp Message Class contracted with Message Interface Template"""

    System_Hit_Time: float = field(default_factory=time.time)
    raw_Data: str
    data_type: str
    Parent_Chat: whatsapp_chat
    MessageID: str
    MessageUI: Union[ElementHandle, Locator]

    def __post_init__(self):
        self.MessageID = self._message_key(self)

    @staticmethod
    def _message_key(message: WhatsappMessage) -> str:
        return str(id(message))
