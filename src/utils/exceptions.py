class PyLoxException(Exception):
    """Exception raised for Lox errors
    Attributes:
        errorName -- Name of raised error
        message -- Explanation of the error
    """

    def __init__(self, errorName: str, message: str) -> None:
        self.errorName: str = errorName
        self.message: str = message
        super().__init__(self.message)


class TooManyArguments(PyLoxException):
    """Exception raised when more than 1 file is passed to the compiler."""

    def __init__(self):
        super().__init__(
            "Too many arguments", "Too many arguments passed. Usage: pylox [script].lox"
        )


class LoxFileNotFound(PyLoxException):
    """Exception raised when the provided Lox file was not found"""

    def __init__(self):
        super().__init__(
            "FileNotFound", "Lox file could not be found. Provide an existing path."
        )
