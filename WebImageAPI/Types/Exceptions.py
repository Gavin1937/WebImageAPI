
from .Types import PARENT_CHILD
from datetime import datetime, timezone


__all__ = [
    'WrongParentChildException',
    'FileMD5NotMatchingException',
    'NotSupportURLException',
    'EHentaiInPeekHourException',
    'EHentaiExcessViewingLimit',
]

class WrongParentChildException(Exception):
    def __init__(self, parent_child:PARENT_CHILD, message:str=None) -> None:
        self.parent_child:PARENT_CHILD = parent_child
        if message is not None:
            self.message:str = message
        else:
            self.message = f'Input WebItemInfo\'s parent_child state is wrong. ({self.parent_child.ToStr()})'
        super().__init__(self.message)

class FileMD5NotMatchingException(Exception):
    def __init__(self, md5_wanted:str, md5_has:str, filepath:str, message:str=None) -> None:
        self.md5_wanted:str = md5_wanted
        self.md5_has:str = md5_has
        self.filepath:str = filepath
        if message is not None:
            self.message:str = f'File MD5 Hash Not Matching.'
        else:
            self.message:str = message
        super().__init__(self.message)

class NotSupportURLException(Exception):
    def __init__(self, message:str=None) -> None:
        self.message:str = 'Supplied url not supported.'
        if message is not None:
            self.message = message
        super().__init__(self.message)


# H-Hentai

class EHentaiInPeekHourException(Exception):
    def __init__(self) -> None:
        now = datetime.now()
        self.datetime = now
        self.time_local = now.isoformat()
        self.time_utc = datetime.fromtimestamp(now.timestamp(), tz=timezone.utc).isoformat()
        self.message = (
            f'E-Hentai is in Peek Hour now, downloads may cause your GP.\n' +
            f'Time In Local Timezone: {self.time_local}\n' +
            f'Time In UTC: {self.time_utc}'
        )
        super().__init__(self.message)

class EHentaiExcessViewingLimit(Exception):
    def __init__(self, url:str) -> None:
        self.url:str = url
        self.message:str = f'You excess E-Hentai Viewing Limit'
        super().__init__(self.message)

