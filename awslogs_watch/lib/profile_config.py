import codecs
from configparser import ConfigParser
from pathlib import Path
from typing import List


class ProfileConfig:
    @staticmethod
    def load_profiles(path: str) -> List[str]:
        _path = Path(path).expanduser()
        if not _path.is_file():
            return []

        config = ConfigParser()
        config.read_file(codecs.open(str(_path), "r", "utf-8"))

        return config.sections()
