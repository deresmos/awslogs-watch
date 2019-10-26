import os
from argparse import ArgumentParser

from awslogs_watch._version import __version__
from awslogs_watch.base import AWSLogsWatch
from awslogs_watch.exceptions import AWSLogsWatchException
from awslogs_watch.lib.execute import Executer
from awslogs_watch.lib.path import AWSLogsWatchPath
from awslogs_watch.lib.prompt import Prompt
from awslogs_watch.model import AWSLogsCommand


class AWSLogsWatchConsole:
    OPTION_CACHE_NAME = "options"

    def __init__(self):
        parser = ArgumentParser(
            description="awslogs wrapper command.", usage="%(prog)s [options]"
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
        )
        parser.add_argument(
            "--cache_path", type=str, default="", help="Cache dirctory path"
        )
        parser.add_argument(
            "--profile", type=str, default="", help="AWS Account profile"
        )
        parser.add_argument("--option", type=str, default="", help="awslogs option")
        parser.add_argument(
            "-i", "--interactive", action="store_true", help="interactive mode"
        )
        parser.add_argument(
            "-r",
            "--recent_default",
            action="store_true",
            help="default value is recent history",
        )
        parser.add_argument("--update", action="store_true", help="Update group names")
        parser.add_argument("--tail", action="store_true", help="Tail log")
        parser.add_argument("--get", action="store_true", help="Get log")
        self.parser = parser
        self.parse_args = parser.parse_args()

        if self.parse_args.cache_path:
            AWSLogsWatchPath.CACHE_PATH = self.parse_args.cache_path

        self.prompt = Prompt(is_recent_history=self.parse_args.recent_default)

    def run(self):
        profile = self.parse_args.profile or os.environ.get("AWS_PROFILE", "default")
        profile = self.load_profile(profile, self.parse_args.interactive)
        awslogs_watch = AWSLogsWatch(profile=profile)
        command = self.load_command()

        if command.is_update():
            awslogs_watch.update_groups()
            return

        awslogs_watch.awslogs.option = self.load_option(
            self.parse_args.option, self.parse_args.interactive
        )
        group = self.load_group(awslogs_watch)
        if command.is_get():
            awslogs_watch.get(group)

        if command.is_tail():
            awslogs_watch.tail(group)

    def load_command(self):
        command = ""
        if self.parse_args.update:
            command = AWSLogsCommand.update
        elif self.parse_args.get:
            command = AWSLogsCommand.get
        elif self.parse_args.tail:
            command = AWSLogsCommand.tail

        if not command:
            command_str = self.prompt.input_command()
            if not command_str:
                raise AWSLogsWatchException(f"No such command.")
            command = AWSLogsCommand[command_str]

        return command

    def load_option(self, option, is_interactive=False):
        if not is_interactive:
            return option

        option_history_path = AWSLogsWatchPath().create_filepath(self.OPTION_CACHE_NAME)
        option = self.prompt.input_option(option_history_path, default=option)

        return option

    def load_profile(self, profile, is_interactive=False):
        if not is_interactive:
            return profile

        _profile = self.prompt.input_profile(default=profile)
        if not _profile:
            raise AWSLogsWatchException(f"Please select correct profile.")

        return _profile

    def load_group(self, awslogs_watch):
        groups = awslogs_watch.load_groups()
        history_path = awslogs_watch.awslogs.history_path
        group_name = self.prompt.input_group(groups, history_path)

        if not group_name:
            raise AWSLogsWatchException(f"No such group.")

        return group_name


def start_console():
    try:
        AWSLogsWatchConsole().run()
    except KeyboardInterrupt:
        print("Quit awslogs-watch")
    except AWSLogsWatchException as e:
        print(e)
        Executer.exit_error()
