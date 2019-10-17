from awslogs_watch.lib.path import AWSLogsWatchPath
from awslogs_watch.lib.profile_config import ProfileConfig
from awslogs_watch.model import AWSLogsCommand, AWSLogsOption
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.history import FileHistory


class Prompt:
    COMMAND_HISTORY_NAME = "command_history"
    PROFILE_HISTORY_NAME = "profile_history"

    AWS_CRED_PATH = "~/.aws/credentials"

    def __init__(self, is_latest_history=False):
        self.is_latest_history = is_latest_history
        self.alw_path = AWSLogsWatchPath()

    def input_group(self, groups, history_path) -> str:
        completer = FuzzyWordCompleter(groups, WORD=True)
        history = FileHistory(history_path)
        session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())
        default = self.find_latest_history(history)

        group_name = session.prompt(
            "Group  : ",
            completer=completer,
            complete_while_typing=True,
            default=default,
        )

        if group_name not in groups:
            return ""

        return group_name

    def input_command(self) -> str:
        commands = [command.name for command in list(AWSLogsCommand)]
        completer = FuzzyWordCompleter(commands)
        history = FileHistory(self.alw_path.create_filepath(self.COMMAND_HISTORY_NAME))
        session = PromptSession(history=history)
        default = self.find_latest_history(history)

        command_str = session.prompt(
            "Command: ",
            completer=completer,
            complete_while_typing=True,
            default=default,
        )

        if command_str not in commands:
            return ""

        return command_str

    def input_option(self, history_path, default="") -> str:
        options = [option.value for option in list(AWSLogsOption)]
        completer = FuzzyWordCompleter(options, WORD=True)

        history = FileHistory(history_path)
        session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())

        default = self.find_default_from_history(default, history)
        option_str = session.prompt(
            "Option : ",
            completer=completer,
            complete_while_typing=True,
            default=default,
        )

        return option_str

    def input_profile(self, default="") -> str:
        profiles = ProfileConfig.load_profiles(self.AWS_CRED_PATH)
        completer = FuzzyWordCompleter(profiles, WORD=True)
        history = FileHistory(self.alw_path.create_filepath(self.PROFILE_HISTORY_NAME))

        session = PromptSession(history=history)
        default = self.find_default_from_history(default, history)

        profile = session.prompt(
            "Profile: ",
            completer=completer,
            complete_while_typing=True,
            default=default,
        )

        if profile not in profiles:
            return ""

        return profile

    def find_default_from_history(self, default, history) -> str:
        default = self.find_latest_history(history) or default

        return default

    def find_latest_history(self, history: FileHistory) -> str:
        if not self.is_latest_history:
            return ""

        latest_history = history.load_history_strings()
        try:
            latest_value = next(latest_history)
        except StopIteration:
            latest_value = ""

        return str(latest_value)
