from telethon.events import NewMessage
from telethon import functions, types
from telegram_bot import yaml_parser
from telethon import TelegramClient


async def auto_reaction(bot: TelegramClient) -> None:

    cfg = yaml_parser()

    @bot.on(NewMessage(pattern=r".*", from_users=list(cfg.keys())))
    async def listener(event) -> None:
        # for group chats
        if event.sender:
            username = event.sender.username.lower()
        else:
            username = event.sender_id
            # get username from id
            user = await bot.get_entity(username)
            username = user.username.lower()

        emoticon = cfg[username]
        reaction = types.ReactionEmoji(emoticon=emoticon)
        await bot(
            functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.message.id,
                reaction=[reaction],
            )
        )


__ALL__ = [auto_reaction]
