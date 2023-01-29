from spotybot.plugins.send_current import send_current
from spotybot.plugins.next import next_track
from spotybot.plugins.current_file import command, send
from spotybot.plugins.lyrics import lyrics
from spotybot.plugins.download import download, download_bot


from typing import List, Callable


ALL: List[Callable] = [
    send_current,
    next_track,
    command,
    send,
    lyrics,
    download,
    download_bot,
]
