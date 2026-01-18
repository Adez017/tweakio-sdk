import asyncio
import functools
from Shared_Resources import logger

def ensure_chat_clicked():
    """Ensure that the chat click decorator is enabled"""

    def decorator(func):
        """Decorator"""

        @functools.wraps(func)
        async def wrapper(self, chat, *args, **kwargs):
            """Wrapper function with retry click logic"""
            for attempt in range(1, retries + 1):
                clicked = await self.chat_loader.click_chat(chat)
                if clicked:
                    break
                logger.warning(f"[{func.__name__}] Click attempt {attempt} failed.")
                await asyncio.sleep(delay)
            else:
                logger.error(f"[{func.__name__}] Failed to click chat after {retries} attempts.")
                raise Exception(f"[{func.__name__}] Chat click failed. Aborting.")

            return await func(self, chat, *args, **kwargs)

        return wrapper

    return decorator
