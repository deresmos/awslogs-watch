from pathlib import Path
from typing import Optional


class AWSLogsWatchPath:
    CACHE_PATH = "~/.cache/awslogs_watch"

    def __init__(self, cache_path: Optional[str] = None) -> None:
        self.cache_dirpath: Path = Path(cache_path or self.CACHE_PATH).expanduser()

    def _create_dirpath(self, cache_dirpath: Path) -> None:
        if cache_dirpath.is_dir():
            return

        cache_dirpath.mkdir(parents=True, exist_ok=True)

    def create_filepath(self, filename) -> str:
        self._create_dirpath(self.cache_dirpath)
        return str(self.cache_dirpath / filename)
