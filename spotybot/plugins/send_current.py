import asyncio
from telethon import TelegramClient
from spotybot import spotify
from telethon.events import NewMessage
from typing import Dict


def formatter(playback: Dict):
    # format playback data
    return f"Artist: **{playback['item']['artists'][0]['name']}**\nSong: {playback['item']['name']}"


async def send_current(bot: TelegramClient):
    @bot.on(NewMessage(pattern="/current"))
    async def send(event):
        current_playback = spotify.auth().current_playback()
        if current_playback is None:
            await event.reply("Nothing is playing")
        else:
            await event.reply(formatter(current_playback))
