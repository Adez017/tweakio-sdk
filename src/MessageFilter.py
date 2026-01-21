"""Independent class for Message Filtering"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from queue import Queue
from typing import List, Optional

from src.Interfaces.Chat_Interface import chat_interface
from src.Interfaces.Message_Interface import message_interface


@dataclass
class State:
    """Chat State"""
    defer_since: Optional[float]
    last_seen: Optional[float]
    window_start: float = field(default_factory=time.time)
    count: int = 0

    def reset(self) -> None:
        """Reset the state"""
        self.window_start = time.time()
        self.count = 0
        self.defer_since = None
        self.last_seen = None


@dataclass
class BindData:
    """Bind Data for the Queue Filtering"""
    chat: chat_interface
    Messages: List[message_interface]
    seen: float


class Filter:
    """
    Independent, shared Message Filter
    """

    StateMap: dict[str, State] = {}
    """State Map keep the state of the multiple chats."""
    Defer_queue: Queue[BindData] = Queue()
    """Decided which one to deliver  -- defer -- drop."""

    def __init__(
            self,
            LimitTime: int = 3600,
            Max_Messages_Per_Window: int = 10,
            Window_Seconds: int = 60,
    ):
        self.LimitTime = LimitTime
        self.Max_Messages_Per_Window = Max_Messages_Per_Window
        self.Window_Seconds = Window_Seconds

    def apply(
            self,
            messages: List[message_interface],
    ) -> List[message_interface]:
        """
        Applies the filter on any set of Messages.
        Filter is agnostic to message direction or type.
        """

        if not messages:
            return []

        # All messages in a batch belong to the same chat
        chat: chat_interface = messages[0].parent_chat

        # Interface-defined unique chat identity
        chat_key = chat._chat_key()
        now = time.time()

        # Fetch or initialize per-chat state
        state = self.StateMap.setdefault(chat_key, State(None, None))

        # Reset rate window if expired
        if now - state.window_start >= self.Window_Seconds:
            state.window_start = now
            state.count = 0

        batch_size = len(messages)

        # Hard drop: chat deferred too long
        if state.defer_since and (now - state.defer_since) > self.LimitTime:
            state.reset()
            return messages

        # Rate-limit hit → defer entire batch
        if state.count + batch_size > self.Max_Messages_Per_Window:
            state.defer_since = state.defer_since or now
            self.Defer_queue.put(BindData(chat, messages, now))
            return []

        # Deliver
        state.count += batch_size
        state.last_seen = now
        return messages
