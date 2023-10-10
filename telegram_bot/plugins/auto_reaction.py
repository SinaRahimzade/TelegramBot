from telethon.events import NewMessage
from telethon import functions, types
from telegram_bot import yaml_parser
from telethon import TelegramClient
from random import choice
from numpy.random import choice as np_choice


async def auto_reaction(bot: TelegramClient) -> None:

    cfg = yaml_parser()['usernames']

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

        in_group_prob = cfg[username]['in_group_prob']
        in_private_prob = cfg[username]['in_private_prob']
        if not event.is_private:
            if not np_choice([True, False], p=[in_group_prob, 1 - in_group_prob]):
                return
            emoticon = choice(cfg[username]['group_reacts'])
        else:
            if not np_choice([True, False], p=[in_private_prob, 1 - in_private_prob]):
                return
            emoticon = choice(cfg[username]['private_reacts'])

        reaction = types.ReactionEmoji(emoticon=emoticon)
        await bot(
            functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.message.id,
                reaction=[reaction],
            )
        )


__all__ = ['auto_reaction']
