import token
from pathlib import Path

from src.scanner import Scanner
from src.utils.exceptions import (LoxFileNotFound, PyLoxException,
                                  TooManyArguments)
from src.utils.logger import PyLoxLogger


class PyLox:
    """
    PyLox compiler Class. A Lox compiler written in python.
    """

    def __init__(self) -> None:
        self._log: PyLoxLogger = PyLoxLogger()
        self._hadError: bool = False

    def __call__(self, args: list[str]) -> None:

        try:
            if len(args) > 1:
                raise TooManyArguments

            if len(args) == 1:
                self._runFile(args[0])
            else:
                self._runPrompt()
        except PyLoxException as e:
            self._handleError(e.message)
            pass

    def _runFile(self, path: str) -> None:
        """
        When a single argument provided extract the file content to compile.
        Arguments:
            path(str): Path to the lox file to compile
        """
        # NOTE: Check for existing path
        if not Path(path).exists():
            raise LoxFileNotFound

        # TODO: Check for .lox extension

        # NOTE: Extract file content
        fileContent: str | None = None
        with open(Path(path).absolute(), mode="r") as target:
            fileContent = target.read()

        # NOTE: Run lox code
        self._run(fileContent)

        # NOTE: Exit if error is found
        if self._hadError:
            return

    def _runPrompt(self):
        while True:
            try:
                line = input("> ")
                if not line:
                    break
                self._run(line)
                self._hadError = False
            except (KeyboardInterrupt, EOFError):
                break

    def _handleError(self, message: str) -> None:
        """
        Private method to handle error state for the compiler.
        Attribute:
            message(str): Message for the logger to display the message.
        """
        self._hadError = True
        self._log.error(message)

    def _run(self, stream: str):
        # NOTE: Run scanner on the stream
        scanner: Scanner = Scanner(stream)
        tokens = scanner.scanTokens()
        for token in tokens:
            print(token)
