from telegram_bot import yaml_parser
from telethon import TelegramClient
from datetime import datetime
from pytz import timezone
from copy import deepcopy
import asyncio


async def complete_tasks(
        bot: TelegramClient, 
        username: str, 
        task_config: dict
    ) -> None:

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


async def scheduled_spam(bot: TelegramClient) -> None:

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
                config = deepcopy(config)
                config_time = {
                    'minute': config.pop('minute', None),
                    'hour': config.pop('hour', None),
                    'day': config.pop('day', None),
                    'month': config.pop('month', None),
                    'year': config.pop('year', None)
                }
                if all(map(lambda x: x is None, config_time.values())):
                    config['prev_run'] = False
                    continue
                if config_time['minute'] is not None and \
                        config_time['minute'] != current_time.minute:
                    config['prev_run'] = False
                    continue
                if config_time['hour'] is not None and \
                        config_time['hour'] != current_time.hour:
                    config['prev_run'] = False
                    continue
                if config_time['day'] is not None and \
                        config_time['day'] != current_time.day:
                    config['prev_run'] = False
                    continue
                if config_time['month'] is not None and \
                        config_time['month'] != current_time.month:
                    config['prev_run'] = False
                    continue
                if config_time['year'] is not None and \
                        config_time['year'] != current_time.year:
                    config['prev_run'] = False
                    continue
                if config['prev_run']:
                    continue
                config['prev_run'] = True
                entity = await bot.get_entity(username)
                tasks.append(complete_tasks(bot, entity, config))
        await asyncio.gather(*tasks)
        await asyncio.sleep(30)


__all__ = ['scheduled_spam']
