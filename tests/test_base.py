from pathlib import Path

from awslogs_watch.base import AWSLogsExecutor
from awslogs_watch.lib.execute import Executer
from awslogs_watch.lib.path import AWSLogsWatchPath


def test_awslogs_load_groups(mocker):
    _groups = ["a", "b", "c", ""]

    awslogs = AWSLogsExecutor()

    create_command = "awslogs groups --profile default"
    tmp_run_pipe = Executer.run_pipe
    Executer.run_pipe = mocker.MagicMock(return_value=_groups)
    groups = awslogs.load_groups()
    Executer.run_pipe = tmp_run_pipe

    assert awslogs.create_command("groups") == create_command
    assert groups == _groups[:-1]


def test_awslogs_cache_groups(mocker):
    try:
        _groups = ["a", "b", "c"]

        awslogs = AWSLogsExecutor()

        awslogs.load_groups = mocker.MagicMock(return_value=_groups)
        awslogs.path = AWSLogsWatchPath("./")

        awslogs.cache_groups()

        groups = awslogs.load_groups_from_cache()

        assert groups == _groups
    finally:
        Path(awslogs.cache_path).unlink()
