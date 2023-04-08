
from datetime import datetime, timezone

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


