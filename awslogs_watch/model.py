from enum import Enum, auto


class AWSLogsCommand(Enum):
    update = auto()
    get = auto()
    tail = auto()

    def is_update(self):
        if self == AWSLogsCommand.update:
            return True

        return False

    def is_get(self):
        if self == AWSLogsCommand.get:
            return True

        return False

    def is_tail(self):
        if self == AWSLogsCommand.tail:
            return True

        return False
