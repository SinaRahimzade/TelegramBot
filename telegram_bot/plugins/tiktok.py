from telethon.events import NewMessage
from telegram_bot import yaml_parser
from telethon import TelegramClient


async def tiktok(bot: TelegramClient) -> None:

    cfg = yaml_parser()

    @bot.on(NewMessage(from_users=801042975))
    async def listener(event) -> None:
        # check if video is sent
        if event.media:
            if event.video:
                # sent the video to the user @sinooom
                for user in cfg:
                    await bot.send_file(user, event.media)


__ALL__ = [tiktok]
