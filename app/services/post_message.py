### app/services/post_message.py
import httpx
from retry import retry

from app.config.settings import settings
from app.logger import logger
from app.services.access_token import token_manager

CHANNEL_MESSAGE_URL = (
    "https://www.worksapis.com/v1.0/bots/{bot_id}/channels/{channel_id}/messages"
)
USER_MESSAGE_URL = (
    "https://www.worksapis.com/v1.0/bots/{bot_id}/users/{user_id}/messages"
)


def _set_headers() -> dict[str, str]:
    token = token_manager.get_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _set_message_payload(message: str) -> dict[str, dict[str, str]]:
    return {"content": {"type": "text", "text": message}}


@retry(tries=3, delay=1, backoff=2, exceptions=(httpx.RequestError, httpx.HTTPError))
async def post_message_to_channel(message: str, channel_id: str) -> None:
    url = CHANNEL_MESSAGE_URL.format(bot_id=settings.bot_id, channel_id=channel_id)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, headers=_set_headers(), json=_set_message_payload(message)
            )
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(f"Async post to channel failed: {e}")
            raise


@retry(tries=3, delay=1, backoff=2, exceptions=(httpx.RequestError, httpx.HTTPError))
async def post_message_to_user(message: str, user_id: str) -> None:
    url = USER_MESSAGE_URL.format(bot_id=settings.bot_id, user_id=user_id)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, headers=_set_headers(), json=_set_message_payload(message)
            )
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(f"Async post to user failed: {e}")
            raise
