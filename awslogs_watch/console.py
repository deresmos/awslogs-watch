import os
from argparse import ArgumentParser

from awslogs_watch.base import AWSLogsWatch
from awslogs_watch.exceptions import AWSLogsWatchException
from awslogs_watch.lib.execute import Executer
from awslogs_watch.lib.prompt import Prompt
from awslogs_watch.model import AWSLogsCommand


class AWSLogsWatchConsole:
    OPTION_CACHE_NAME = "options"

    def __init__(self):
        parser = ArgumentParser(
            description="awslogs wrapper command.", usage="%(prog)s [options]"
        )
        parser.add_argument(
            "--profile", type=str, default="", help="AWS Account profile"
        )
        parser.add_argument("--option", type=str, default="", help="awslogs option")
        parser.add_argument(
            "-i", "--interactive", action="store_true", help="interactive mode"
        )
        parser.add_argument("--update", action="store_true", help="Update group names")
        parser.add_argument("--tail", action="store_true", help="Tail log")
        parser.add_argument("--get", action="store_true", help="Get log")
        self.parser = parser

    def run(self):
        args = self.parser.parse_args()

        profile = args.profile or os.environ.get("AWS_PROFILE", "default")
        profile = self.load_profile(profile, args.interactive)
        awslogs_watch = AWSLogsWatch(profile=profile)
        command = self.load_command()
        awslogs_watch.awslogs.option = self.load_option(args.option, args.interactive)

        if command.is_update():
            awslogs_watch.update_groups()
            return

        if command.is_get():
            awslogs_watch.get()

        if command.is_tail():
            awslogs_watch.tail()

    def load_command(self):
        args = self.parser.parse_args()

        command = ""
        if args.update:
            command = AWSLogsCommand.update
        elif args.get:
            command = AWSLogsCommand.get
        elif args.tail:
            command = AWSLogsCommand.tail

        if not command:
            command_str = Prompt.input_command()
            if not command_str:
                raise AWSLogsWatchException(f"No such command. ({command_str})")
            command = AWSLogsCommand[command_str]

        return command

    def load_option(self, option, is_interactive=False):
        if not is_interactive:
            return option

        option = Prompt.input_option(self.OPTION_CACHE_NAME, default=option)

        return option

    def load_profile(self, profile, is_interactive=False):
        if not is_interactive:
            return profile

        _profile = Prompt.input_profile(default=profile)
        if not _profile:
            raise AWSLogsWatchException(f"Please input profile.")

        return _profile


def start_console():
    try:
        AWSLogsWatchConsole().run()
    except KeyboardInterrupt:
        print("Quit awslogs-watch")
    except AWSLogsWatchException as e:
        print(e)
        Executer.exit_error()
