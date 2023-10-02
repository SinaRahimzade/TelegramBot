from telegram_bot import yaml_parser
from telethon import TelegramClient
from telegram_bot import PLUGINS
from socks import SOCKS5
import asyncio


async def telegram_client() -> None:

    """
    This is the main function that runs the Telegram bot
    """

    cfg = yaml_parser()

    bot = TelegramClient(
        cfg['username'], 
        cfg['api_id'], 
        cfg['api_hash'], 
        proxy=(SOCKS5, cfg['proxy']['host'], cfg['proxy']['port']) \
            if cfg['use_proxy'] else None
    )

    await bot.start()

    asyncio.gather(*[plugin(bot) for plugin in PLUGINS])
    
    await bot.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(telegram_client())
