import asyncio
from telethon import TelegramClient
from spotybot import spotify
from telethon.events import NewMessage
from typing import Dict
from telethon import functions, types
import yaml


all_users = yaml.safe_load(open("config.yml"))["reactions"]


async def react(bot: TelegramClient):
    @bot.on(NewMessage(pattern=r".*", from_users=list(all_users.keys())))
    async def react(event):
        # for group chats
        if event.sender:
            username = event.sender.username.lower()
        else:
            username = event.sender_id
            # get username from id
            user = await bot.get_entity(username)
            username = user.username.lower()

        emoticon = all_users[username]
        reaction = types.ReactionEmoji(emoticon=emoticon)
        result = await bot(
            functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.message.id,
                reaction=[reaction],
            ),
        )
        print(result)
