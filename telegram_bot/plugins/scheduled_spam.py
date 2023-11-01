from telegram_bot import yaml_parser
from telethon import TelegramClient
from datetime import datetime
from random import randint
from pytz import timezone
from copy import deepcopy
import asyncio

from pprint import pprint
async def complete_tasks(
        bot: TelegramClient, 
        username: str, 
        task_configs: dict
    ) -> None:

    task_config = task_configs[randint(0, len(task_configs) - 1)]
    response_count = task_config.get('response_count', 1)
    if response_count == 0:
        return
    sleep = task_config.get('sleep', 0)
    response_message = task_config.get('response_message', None)
    if response_message is None:
        return
    multiple_character = task_config.get('mutiple_character', None)
    reverse = task_config.get('reverse', False)

    for i in range(response_count):
        if sleep != 0:
            await asyncio.sleep(sleep)
        if multiple_character is None:
            await bot.send_message(username, response_message)
        else:
            await bot.send_message(
                username, 
                response_message.replace(
                    multiple_character,
                    multiple_character * (i + 1)
                )
            )
    if not reverse:
        return

    for i in range(response_count - 1, -1, -1):
        if sleep != 0:
            await asyncio.sleep(sleep)
        if multiple_character is None:
            await bot.send_message(username, response_message)
        else:
            await bot.send_message(
                username, 
                response_message.replace(
                    multiple_character,
                    multiple_character * (i + 1)
                )
            )


async def scheduled_spam(bot: TelegramClient) -> None:

    cfg = yaml_parser()
    tz = timezone(cfg['timezone'])
    cfg = cfg['usernames']

    for username, configs in cfg.items():
        for config in configs:
            config['prev_run'] = None

    while True:
        current_time, tasks = datetime.now(tz), []
        print('new_loop')
        for username, configs in cfg.items():
            for config in configs:
                print(username)
                config_time = {
                    'minute': config.get('minute', None),
                    'hour': config.get('hour', None),
                    'day': config.get('day', None),
                    'month': config.get('month', None),
                    'year': config.get('year', None)
                }
                if config_time['minute'] is not None and \
                    config_time['minute'] != current_time.minute:
                    config['prev_run'] = None
                    continue
                if config_time['hour'] is not None and \
                    config_time['hour'] != current_time.hour:
                    config['prev_run'] = None
                    continue
                if config_time['day'] is not None and \
                    config_time['day'] != current_time.day:
                    config['prev_run'] = None
                    continue
                if config_time['month'] is not None and \
                    config_time['month'] != current_time.month:
                    config['prev_run'] = None
                    continue
                if config_time['year'] is not None and \
                    config_time['year'] != current_time.year:
                    config['prev_run'] = None
                    continue
                if config['prev_run'] == current_time.minute:
                    print('bega raf', current_time.minute)
                    continue
                print('naraft', current_time.minute)
                config['prev_run'] = current_time.minute
                entity = await bot.get_entity(username)
                tasks.append(complete_tasks(bot, entity, config['message_configs']))
        print('pre-wtf')
        await asyncio.gather(*tasks)
        print('wtf')
        await asyncio.sleep(20)


__all__ = ['scheduled_spam']
