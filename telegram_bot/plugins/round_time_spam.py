from telegram_bot import yaml_parser
from telethon import TelegramClient
from numpy.random import choice
from datetime import datetime
from pytz import timezone
from copy import deepcopy
import asyncio


async def complete_tasks(
        bot: TelegramClient, 
        username: str, 
        task_config: dict,
        minute: str
    ) -> None:

    if task_config['response_message'] is None:
        await bot.send_message(username, f'{minute.zfill(2)}:{minute.zfill(2)}')
        return

    for i in range(task_config['response_count']):
        if task_config['sleep'] != 0:
            await asyncio.sleep(task_config['sleep'])
        await bot.send_message(
            username, 
            task_config['response_message'].replace(
                task_config['mutiple_character'],
                task_config['mutiple_character'] * (i + 1)
            )
        )
    if not task_config['reverse']:
        return
    for i in range(task_config['response_count'] - 1, -1, -1):
        if task_config['sleep'] != 0:
            await asyncio.sleep(task_config['sleep'])
        await bot.send_message(
            username, 
            task_config['response_message'].replace(
                task_config['mutiple_character'],
                task_config['mutiple_character'] * (i + 1)
            )
        )


async def round_time_spam(bot: TelegramClient) -> None:

    cfg = yaml_parser()
    tz = timezone(cfg['timezone'])
    cfg = cfg['usernames']
    for username in cfg:
        for config in cfg[username]:
            config['prev_run'] = False

    while True:

        current_time = datetime.now(tz)
        tasks = []
        for username, configs_list in cfg.items():
            for config in configs_list:
                if current_time.minute != current_time.hour:
                    config['prev_run'] = False
                    continue
                if config['prev_run']:
                    continue
                if choice([True, False], p=[config['prob'], 1 - config['prob']]):
                    config['prev_run'] = True
                    entity = await bot.get_entity(username)
                    tasks.append(complete_tasks(
                        bot, entity, config, str(current_time.minute)
                    ))
                    
        await asyncio.gather(*tasks)
        await asyncio.sleep(30)


__all__ = ['round_time_spam']
