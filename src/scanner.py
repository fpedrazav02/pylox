from typing import overload

from src.tokens import Token, TokenType
from src.utils.errors import *
from src.utils.logger import PyLoxLogger


class Scanner:
    def __init__(self, source: str) -> None:
        self._log: PyLoxLogger = PyLoxLogger()
        self._source: str = source
        self._tokens: list[Token] = []

        self._start: int = 0
        self._current: int = 0
        self._line: int = 1

    def scanTokens(self) -> list[Token]:
        # NOTE: Scann everything until the end
        while not self.isAtEnd:
            self._start = self._current
            _ = self._scanToken()

        # NOTE: Append EOF token at the end
        self._tokens.append(Token(0, TokenType.EOF, None, ""))
        return self._tokens

    def _scanToken(self) -> None:
        c: str = self._source[self._current]
        self._current += 1

        match c:
            case "[":
                self._addToken(TokenType.LEFT_BRACE)
            case "]":
                self._addToken(TokenType.RIGHT_BRACE)
            case "(":
                self._addToken(TokenType.LEFT_PAREN)
            case ")":
                self._addToken(TokenType.RIGHT_PAREN)
            case "{":
                self._addToken(TokenType.LEFT_BRACE)
            case "}":
                self._addToken(TokenType.RIGHT_BRACE)
            case ",":
                self._addToken(TokenType.COMMA)
            case ".":
                self._addToken(TokenType.DOT)
            case "-":
                self._addToken(TokenType.MINUS)
            case "+":
                self._addToken(TokenType.PLUS)
            case ";":
                self._addToken(TokenType.SEMICOLON)
            case "*":
                self._addToken(TokenType.STAR)

            # NOTE: Whitespace handling
            case " " | "\r" | "\t":
                pass
            case "\n":
                self._line += 1

            # NOTE: Handle any other case
            case _:
                self._log.lineError(self._line, f"Unexpected character {ord(c)} found.")

    @overload
    def _addToken(self, type: TokenType) -> None: ...
    @overload
    def _addToken(self, type: TokenType, literal: object) -> None: ...

    def _addToken(self, type: TokenType, literal: object = None) -> None:
        tokenString: str = self._source[self._start : self._current]
        token = Token(self._line, type, literal, tokenString)
        self._tokens.append(token)

    @property
    def isAtEnd(self) -> bool:
        """Return boolean if source has finished"""
        return self._current >= len(self._source)
