from telegram_bot.plugins.auto_reaction import auto_reaction
from telegram_bot.plugins.tiktok import tiktok
from telegram_bot.plugins.reels import reels
from telegram_bot.plugins.spam import spam
from typing import List, Callable


PLUGINS: List[Callable] = [
    auto_reaction,
    reels, 
    tiktok,
    spam,
]

__ALL__ = [
    PLUGINS,
]
