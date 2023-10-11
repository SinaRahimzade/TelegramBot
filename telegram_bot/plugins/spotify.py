from telethon.events import NewMessage
from telegram_bot import yaml_parser
from telethon import TelegramClient
import asyncio


async def spotify(bot: TelegramClient) -> None:

    cfg = yaml_parser()

    @bot.on(NewMessage(outgoing=True, blacklist_chats=[cfg['bot']]))
    async def listener(event) -> None:
        if cfg['pattern'] in event.raw_text:
            user = event.message.to_id.user_id
            message = event.raw_text
            await event.message.delete()
            
            robot_id = await bot.get_entity(cfg['bot'])
            await bot.send_message(robot_id, message)
            
            await asyncio.sleep(cfg['wait_for_response'])
            response_events = await bot.get_messages(
                robot_id, limit=cfg['response_count']
            )
            for response_event in response_events:
                if response_event.media and response_event.audio:
                    await bot.send_file(user, response_event.media)
                    return


__all__ = ['spotify']
