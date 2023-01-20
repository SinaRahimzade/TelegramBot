from spotybot.plugins.config import ALL
import yaml
from telethon import TelegramClient
import asyncio
from socks import SOCKS5


async def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)["telegram"]

    proxy = (SOCKS5, cfg["proxy"]["host"], cfg["proxy"]["port"])
    bot = TelegramClient(cfg["username"], cfg["app_id"], cfg["api_hash"], proxy=proxy)
    await bot.start()
    print("Bot started")
    for plugin in ALL:
        asyncio.gather(plugin(bot))
    await bot.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
