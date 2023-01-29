from telethon import TelegramClient
from spotybot import spotify
from telethon.events import NewMessage
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import yaml


music_provider_bot = yaml.safe_load(open("config.yml"))["music_provider_id"]
data_base_channel = yaml.safe_load(open("config.yml"))["data_base"]
database = {}


async def command(bot: TelegramClient):
    @bot.on(NewMessage(pattern="/current_file"))
    async def command(event):

        current_playback = spotify.auth().current_playback()

        song_url = current_playback["item"]["external_urls"]["spotify"]
        song_name = current_playback["item"]["name"]
        song_name = song_name.lower().replace(" ", "_")

        data = {
            "chat_id": event.chat_id,
            "message_id": event.message.id,
        }

        if database.get(song_name):
            database[song_name].append(data)
        else:
            database[song_name] = [data]
        # search for the song in the database channel
        async for message in bot.iter_messages(
            data_base_channel, search=current_playback["item"]["name"]
        ):
            # if song is found send it to the user
            if message.media:
                await bot.send_file(
                    event.chat_id, message.media, reply_to=event.message.id
                )
                break
        else:
            # if song is not found send the song url to the music provider bot
            await bot.send_message(music_provider_bot, song_url)


async def send(bot: TelegramClient):
    # listen for messages from the music provider bot
    @bot.on(NewMessage(from_users=music_provider_bot))
    async def send(event):
        # check if we have music file in event
        if event.media:
            # check if medis is a DocumentAttributeAudio
            if (
                event.media.document.attributes[0].__class__.__name__
                == "DocumentAttributeAudio"
            ):
                # get the song name from the message
                song_name = event.media.document.attributes[0].title
                # decapitalize the song name and replace spaces with underscores
                song_name = song_name.split("-")[0].strip().lower().replace(" ", "_")
                print(song_name)
                # get the data from redis
                print(database)
                data = database.get(song_name)
                print(data)
                for d in data:
                    chat_id = d["chat_id"]
                    message_id = d["message_id"]
                    # send the music file to the user
                    await bot.send_file(
                        int(chat_id), event.media, reply_to=int(message_id)
                    )
                    # send the song to the database channel
                    await bot.send_file(data_base_channel, event.media)

                # delete the data from database
                del database[song_name]

        # if bot sent a inline keyboard
        elif event.reply_markup:
            # search for the song name in the button text
            button = None
            for row in event.reply_markup.rows:
                for b in row.buttons:
                    print(b)
                    if b.text.lower().replace(" ", "_") in database:
                        button = b
                        break
            # if we found the button send query to the bot
            if button:
                await bot(GetBotCallbackAnswerRequest(event.chat_id, button.data))
