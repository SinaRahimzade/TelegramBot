from spotybot.plugins.auto_react import react
from spotybot.plugins.reel import reel, tiktok


from typing import List, Callable


ALL: List[Callable] = [reel, tiktok, react]
