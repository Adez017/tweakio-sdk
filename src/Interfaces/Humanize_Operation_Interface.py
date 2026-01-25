"""All the Humanized Operation Interface modules"""
from abc import ABC, abstractmethod

from playwright.async_api import Page


class humanize_operation(ABC):

    @abstractmethod
    def __init__(self, page: Page) -> None:
        self.page = page

    @abstractmethod
    async def typing(self, text: str, **kwargs) -> None:
        """This operation ensures the given text is typed on the Web UI with humanized Typing"""
        pass
