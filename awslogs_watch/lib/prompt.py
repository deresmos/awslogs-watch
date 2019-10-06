from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import prompt

from awslogs_watch.model import AWSLogsCommand


class Prompt:
    @staticmethod
    def input_group(groups, history_path) -> str:
        completer = FuzzyWordCompleter(groups)
        history = FileHistory(history_path)
        session = PromptSession(history=history)
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
