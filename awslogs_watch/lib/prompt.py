from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import prompt

from awslogs_watch.lib.profile_config import ProfileConfig
from awslogs_watch.model import AWSLogsCommand, AWSLogsOption


class Prompt:
    def __init__(self, is_latest_history=False):
        self.is_latest_history = is_latest_history

    @staticmethod
    def input_group(groups, history_path) -> str:
        completer = FuzzyWordCompleter(groups, WORD=True)
        history = FileHistory(history_path)
        session = PromptSession(
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
        )
        group_name = session.prompt(
            "Input Group: ", completer=completer, complete_while_typing=True
        )

        if group_name not in groups:
            return ""

        return group_name

    @staticmethod
    def input_command() -> str:
        commands = [command.name for command in list(AWSLogsCommand)]
        completer = FuzzyWordCompleter(commands)
        command_str = prompt(
            "Input Command: ", completer=completer, complete_while_typing=True
        )

        if command_str not in commands:
            return ""

        return command_str

    def input_option(self, history_path, default="") -> str:
        options = [option.value for option in list(AWSLogsOption)]
        completer = FuzzyWordCompleter(options, WORD=True)

        history = FileHistory(history_path)
        session = PromptSession(
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
        )

        default = self.find_default_from_history(default, history)
        option_str = session.prompt(
            "Input Option: ",
            completer=completer,
            complete_while_typing=True,
            default=default,
        )

        return option_str

    def input_profile(self, default="") -> str:
        profiles = ProfileConfig.load_profiles("~/.aws/credentials")
        completer = FuzzyWordCompleter(profiles, WORD=True)

        profile = prompt(
            "Input Profile: ",
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
