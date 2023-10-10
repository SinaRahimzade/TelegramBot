from telethon.events import NewMessage
from telegram_bot import yaml_parser
from telethon import TelegramClient
import asyncio


async def spam(bot: TelegramClient) -> None:

    cfg = yaml_parser()

    @bot.on(NewMessage(chats=list(cfg['usernames']), outgoing=True))
    async def listener(event) -> None:

        receiver_id = event.message.to_id.user_id
        username = await bot.get_entity(receiver_id)
        username = username.username

        for plan in cfg['usernames'][username.lower()]:
            if event.message.text.startswith(plan['trigger_message']):
                for i in range(plan['response_count']):
                    if plan['sleep'] != 0:
                        await asyncio.sleep(plan['sleep'])
                    await bot.send_message(
                        receiver_id, 
                        plan['response_message'].replace(
                            plan['mutiple_character'],
                            plan['mutiple_character'] * (i + 1)
                        )
                    )
                if not plan['reverse']:
                    continue
                for i in range(plan['response_count'] - 1, -1, -1):
                    if plan['sleep'] != 0:
                        await asyncio.sleep(plan['sleep'])
                    await bot.send_message(
                        receiver_id, 
                        plan['response_message'].replace(
                            plan['mutiple_character'],
                            plan['mutiple_character'] * (i + 1)
                        )
                    )


__ALL__ = [spam]
