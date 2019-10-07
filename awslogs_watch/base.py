import sys
from pathlib import Path
from typing import Optional

from awslogs_watch.exceptions import AWSLogsWatchException
from awslogs_watch.lib.execute import Executer
from awslogs_watch.lib.path import AWSLogsWatchPath
from awslogs_watch.lib.prompt import Prompt


class AWSLogsExecutor:
    GROUP_CACHE_NAME = "groups-{profile}.cache"
    HISTORY_CACHE_FILENAME = "history-{profile}.cache"

    def __init__(
        self, profile: str = "default", *, option: Optional[str] = None
    ) -> None:
        self.profile = profile
        self.option = option
        self.path = AWSLogsWatchPath()

    def create_command(self, cmd_str):
        cmd = f"awslogs {cmd_str} --profile {self.profile}"
        if self.option:
            cmd += f" {self.option}"

        return cmd

    def load_groups(self):
        cmd = self.create_command("groups")
        groups = Executer.run_pipe(cmd)
        groups = [group for group in groups if group]

        return groups

    def load_groups_from_cache(self):
        if not Path(self.cache_path).is_file():
            print("ERROR: Please --update")
            sys.exit(1)

        with open(self.cache_path, "r") as f:
            text = f.read()

        return text.split("\n")

    def cache_groups(self):
        groups = self.load_groups()
        with open(self.cache_path, "w") as f:
            f.write("\n".join(groups))

    @property
    def cache_path(self) -> str:
        cache_filename = self.GROUP_CACHE_NAME.format(profile=self.profile)
        cache_path = self.path.create_filepath(cache_filename)
        return cache_path

    @property
    def history_path(self) -> str:
        history_filename = self.HISTORY_CACHE_FILENAME.format(profile=self.profile)
        history_path = self.path.create_filepath(history_filename)
        return history_path


class AWSLogsWatch:
    def __init__(self, profile="default"):
        self.awslogs = AWSLogsExecutor(profile)
        self.path = AWSLogsWatchPath()

    def tail(self):
        group = self.prompt_group()
        cmd = self.awslogs.create_command(f"get {group} --watch")
        Executer.run(cmd)
        print(f"Stop {group}")

    def get(self):
        try:
            group = self.prompt_group()
            if not group:
                raise AWSLogsWatchException(f"No such group. ({group})")
            cmd = self.awslogs.create_command(f"get {group}")
            Executer.run(cmd)
        except KeyboardInterrupt:
            print(f"Stop awslogs: {group}")

    def update_groups(self):
        print("Updating...")
        self.awslogs.cache_groups()
        print("Updated!")

    def prompt_group(self):
        groups = self.awslogs.load_groups_from_cache()
        history_path = self.awslogs.history_path
        group_name = Prompt.input_group(groups, history_path)

        return group_name
