from telethon.events import NewMessage
from telethon import TelegramClient
import yaml

REEL_USERS = yaml.safe_load(open("config.yml"))["reel"]
TIKTOK_USERS = yaml.safe_load(open("config.yml"))["tiktok"]


async def reel(bot: TelegramClient):
    # check every message comes from 1856992318
    @bot.on(NewMessage(from_users=1856992318))
    async def reel(event):
        # check if video is sent
        if event.media:
            if event.video:
                # sent the video to the user @sinooom
                for user in REEL_USERS:
                    await bot.send_file(user, event.media)


async def tiktok(bot: TelegramClient):
    @bot.on(NewMessage(from_users=801042975))
    async def tiktok(event):
        # check if video is sent
        if event.media:
            if event.video:
                # sent the video to the user @sinooom
                for user in TIKTOK_USERS:
                    await bot.send_file(user, event.media)
