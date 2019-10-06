import shlex
import sys
from subprocess import PIPE, Popen
from typing import List


class Executer:
    SUCCESS = 0
    ERROR = 1

    @staticmethod
    def run(command: str) -> None:
        p = Popen(shlex.split(command))
        print(f"-> {command}")
        p.communicate()
        if p.returncode == Executer.ERROR:
            sys.exit(Executer.ERROR)

    @staticmethod
    def run_pipe(command: str) -> List[str]:
        p = Popen(shlex.split(command), stdout=PIPE)
        print(f"-> {command}")
        result = p.communicate()
        if p.returncode == Executer.ERROR:
            sys.exit(Executer.ERROR)

        return_lines = result[0].decode("utf-8").split("\n")
        return return_lines

    @staticmethod
    def exit_error():
        sys.exit(Executer.ERROR)
