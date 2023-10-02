from telegram_bot.plugins.auto_reaction import auto_reaction
from telegram_bot.plugins.tiktok import tiktok
from telegram_bot.plugins.reels import reels
from typing import List, Callable


PLUGINS: List[Callable] = [
    auto_reaction,
    reels, 
    tiktok,
]

__ALL__ = [
    PLUGINS,
]
