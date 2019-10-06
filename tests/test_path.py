import shutil
from pathlib import Path

from awslogs_watch.lib.path import AWSLogsWatchPath


def test_create_filepath():
    try:
        cache_path = "./cache"
        path = AWSLogsWatchPath(cache_path=cache_path)
        filename = path.create_filepath("filename")

        assert Path(cache_path).is_dir()
        assert Path(filename) == Path("./cache/filename")
    finally:
        shutil.rmtree(cache_path)
        assert Path(cache_path).is_dir() == False
