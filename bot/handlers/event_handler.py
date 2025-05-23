from enum import Enum

from fastapi.responses import JSONResponse

from bot.services.openai_client import get_openai_response
from bot.services.post_message import post_message_to_channel, post_message_to_user


class BotStatus(str, Enum):
    """Enum for bot status."""

    IGNORED = "ignored"
    OK = "ok"


async def process_event(data: dict) -> JSONResponse:
    event_type = data.get("type")
    source = data.get("source", {})
    channel_id = source.get("channelId")
    user_id = source.get("userId")

    if event_type == "join":
        await post_message_to_channel(
            channel_id=channel_id,
            message="Hello! I am a bot.",
        )
        return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    if event_type == "message":
        content = data.get("content", {})
        text = content.get("text", "")
        response = await get_openai_response(
            prompt="You are a helpful assistant.",
            input=text,
        )
        if channel_id:
            await post_message_to_channel(channel_id=channel_id, message=response)
            return JSONResponse(status_code=200, content={"status": BotStatus.OK})

        if user_id:
            await post_message_to_user(user_id=user_id, message=response)
            return JSONResponse(status_code=200, content={"status": BotStatus.OK})

    return JSONResponse(status_code=200, content={"status": BotStatus.IGNORED})
