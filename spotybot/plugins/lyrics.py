from telethon import TelegramClient
from spotybot import spotify
from telethon.events import NewMessage
import requests
import lyricsgenius as lg


import yaml

token = yaml.safe_load(open("config.yml"))["genius"]["access_token"]
lg = lg.Genius(token)


data_base_channel = yaml.safe_load(open("config.yml"))["data_base"]
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


async def lyrics(bot: TelegramClient) -> None:
    @bot.on(NewMessage(pattern="/lyrics"))
    async def lyrics(event):
        current_playback = spotify.auth().current_playback()
        artist_name = current_playback["item"]["artists"][0]["name"]
        song_name = current_playback["item"]["name"]
        gennius_url = f"https://genius.com/{artist_name.replace(' ','-')}-{song_name.replace(' ','-')}-lyrics"
        # send genius url to the user
        await bot.send_message(event.chat_id, gennius_url, reply_to=event.message.id)
