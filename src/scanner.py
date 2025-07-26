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
            case "!":
                bangType: TokenType = (
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
                self._addToken(bangType)
            case "=":
                equalType: TokenType = (
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
                self._addToken(equalType)
            case ">":
                greaterType: TokenType = (
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
                self._addToken(greaterType)
            case "<":
                lessType: TokenType = (
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
                self._addToken(lessType)

            # NOTE: Longer cases
            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self.isAtEnd:
                        self._current += 1
                else:
                    self._addToken(TokenType.SLASH)
            # NOTE: Handle strings
            case '"':
                self._string()

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

    def _match(self, expected: str) -> bool:
        if self.isAtEnd:
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self) -> str:
        if self.isAtEnd:
            return "\0"
        return self._source[self._current]

    def _string(self) -> None:
        while self._peek()!= '"' and not self.isAtEnd:
            if self._source[self._current] == "\n":
                self._line += 1
            self._current += 1

        if self.isAtEnd:
            self._log.lineError(self._line, "Unterminated string found.")
            return
        self._current += 1

        # Add the token removing Quotes
        self._addToken(
            TokenType.STRING, self._source[self._start + 1 : self._current - 1]
        )
