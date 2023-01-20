import asyncio
from telethon import TelegramClient
from spotybot import spotify
from telethon.events import NewMessage
from typing import Dict


async def next_track(bot: TelegramClient):
    @bot.on(NewMessage(pattern="/next_track"))
    async def send(event):
        spotify.auth().next_track()
        await event.reply("going to next track")


    