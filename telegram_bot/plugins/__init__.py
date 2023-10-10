from telegram_bot.plugins.scheduled_spam import scheduled_spam
from telegram_bot.plugins.auto_reaction import auto_reaction
from telegram_bot.plugins.global_spam import global_spam
from telegram_bot.plugins.tiktok import tiktok
from telegram_bot.plugins.reels import reels
from telegram_bot.plugins.spam import spam
from typing import List, Callable


PLUGINS: List[Callable] = [
    scheduled_spam,
    auto_reaction,
    global_spam,
    reels, 
    tiktok,
    spam,
]

__all__ = [
    'PLUGINS',
]
