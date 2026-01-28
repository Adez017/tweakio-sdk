"""
Unit tests for Chat_Processor class.

This module demonstrates how to mock external dependencies like Playwright's Page
and Python's Logger for testing Chat_Processor in isolation.
"""

from urllib3 import Retry
import logging
import pytest
import logging
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from typing import Optional
from playwright.async_api import Page, Locator, ElementHandle

from src.WhatsApp.Chat_Processor import chat_processor
from src.WhatsApp.DefinedClasses.Chat import whatsapp_chat
from src.Exceptions.tweakio_exceptions import ChatNotFoundError, ChatClickError


# ============================================================================
# FIXTURES - Reusable Mock Objects
# ============================================================================

def get_mock_logger():
    """Create a mock logger for testing.
    
    This mock logger tracks all log calls without actually logging to console.
    You can assert on log calls like: mock_logger.error.assert_called_once()
    """
    logger = Mock(spec=logging.Logger)
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    logger.critical = Mock()
    return logger


def get_mock_page():
    """Creates a Mocked playwright page Object.
    Also adds a mock Locator for the page.
    """
    page = AsyncMock(spec=Page)
    page.locator =AsyncMock(spec=Locator)
    page.wait_for_timeout = AsyncMock()
    page.click = AsyncMock()


@pytest.mark.asyncio
@patch("src.WhatsApp.Chat_Processor.sc")
async def test_get_wrapped_chat_with_data(mock_sc):
    """Test _get_Wrapped_Chat returns 2 chat objects."""
    
    # Setup mock locator
    mock_locator = AsyncMock(spec=Locator)
    mock_locator.count = AsyncMock(return_value=2)  

    # mock elements that nth() will return
    mock_element_0 = AsyncMock(spec=ElementHandle)
    mock_element_1 = AsyncMock(spec=ElementHandle)
    
    mock_locator.nth = Mock(side_effect=lambda i: [mock_element_0, mock_element_1][i])
    
    mock_sc.chat_items = Mock(return_value=mock_locator) 

    async def get_chat_name_side_effect(element):
        if element == mock_element_0:
            return "Chat 1"
        elif element == mock_element_1:
            return "Chat 2"
        return "Unknown"
    
    mock_sc.getChatName = AsyncMock(side_effect=get_chat_name_side_effect)
    
    p = chat_processor(page=get_mock_page(), log=get_mock_logger())
    chats = await p._get_Wrapped_Chat(limit=2, retry=2)
    
    assert len(chats) == 2
    assert chats[0].chatName == "Chat 1"  
    assert chats[1].chatName == "Chat 2"
    
    mock_locator.nth.assert_any_call(0)
    mock_locator.nth.assert_any_call(1)

@pytest.mark.asyncio
@patch("src.WhatsApp.Chat_Processor.sc")
async def test_get_wrapped_chat_with_no_data(mock_sc):
    """Test _get_Wrapped_Chat returns empty list when no chats found."""
    
    mock_locator = AsyncMock(spec=Locator)
    mock_locator.count = AsyncMock(return_value=0)  
    
    mock_sc.chat_items = Mock(return_value=mock_locator)
    
    p = chat_processor(page=get_mock_page(), log=get_mock_logger())
    chats = await p._get_Wrapped_Chat(limit=2, retry=2)
    
    assert len(chats) == 0
    assert chats == []
    

@pytest.mark.asyncio
async def test_fetch_chats():
    #chat obj mock
    mock_whatsapp_chat_0 = Mock(spec = whatsapp_chat)
    mock_whatsapp_chat_1 = Mock(spec = whatsapp_chat)

    #mock get_wrapped_chat
    mock_wrappedChats = AsyncMock(return_value=[mock_whatsapp_chat_0, mock_whatsapp_chat_1])

    p = chat_processor(page=get_mock_page(), log=get_mock_logger())
    p._get_Wrapped_Chat = mock_wrappedChats
    data = await p.fetch_chats(limit = 2 , retry = 2)

    assert data == [mock_whatsapp_chat_0, mock_whatsapp_chat_1]

    # Mock empty dataset 
    p._get_Wrapped_Chat = AsyncMock(return_value=[])
    data = await p.fetch_chats(limit = 2 , retry = 2)
    assert data == []

@pytest.mark.asyncio
async def test_click_chat():
    """Test _click_chat successfully clicks a chat."""
    # Create mock chat object
    mock_chat = Mock(spec=whatsapp_chat)
    
    # Create mock element that will be returned by element_handle
    mock_element = AsyncMock()
    mock_element.click = AsyncMock()
    
    # Setup chatUI as Locator with element_handle method
    mock_chat.chatUI = AsyncMock(spec=Locator)
    # ✅ FIXED: element_handle is a METHOD that returns an element
    mock_chat.chatUI.element_handle = AsyncMock(return_value=mock_element)
    
    p = chat_processor(page=get_mock_page(), log=get_mock_logger())
    
    # Test successful click
    check = await p._click_chat(chat=mock_chat)
    assert check == True
    
    # Verify calls
    mock_chat.chatUI.element_handle.assert_called_once()
    mock_element.click.assert_called_once()


@pytest.mark.asyncio
async def test_click_chat_with_none():
    """Test _click_chat handles None chat gracefully."""
    p = chat_processor(page=get_mock_page(), log=get_mock_logger())
    
    # Test with None chat
    check = await p._click_chat(chat=None)
    assert check == False

@pytest.mark.asyncio
async def test_is_unread():
    