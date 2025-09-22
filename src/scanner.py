from typing import overload

from src.tokens import IDENTIFIER_MAP, Token, TokenType
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
                elif self._match("*"):
                    cCommentStack: list[int] = [1]
                    while cCommentStack:
                        if self.isAtEnd:
                            self._log.lineError(
                                self._line, "Unterminated C-style comment."
                            )
                            return
                        if self._peek() == "\n":
                            self._line += 1
                        if self._peek() == "/" and self._peekNext() == "*":
                            cCommentStack.append(1)
                            self._current += 2
                            continue
                        if self._peek() == "*" and self._peekNext() == "/":
                            _ = cCommentStack.pop()
                            self._current += 2
                            continue
                        self._current += 1
                    return
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
                if c.isdigit():
                    self._number()
                    return
                if c.isalpha():
                    self._identifier()
                    return
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

    def _peekNext(self) -> str:
        if self._current + 1 > len(self._source):
            return "\0"
        nextPeek: int = self._current + 1
        return self._source[nextPeek]

    def _string(self) -> None:
        while self._peek() != '"' and not self.isAtEnd:
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

    def _number(self) -> None:
        while not self.isAtEnd and str.isdigit(self._source[self._current]):
            self._current += 1

        if self._peek() == "." and str.isdigit(self._peekNext()):
            self._current += 1

            while not self.isAtEnd and str.isdigit(self._source[self._current]):
                self._current += 1

        self._addToken(
            type=TokenType.NUMBER,
            literal=float(self._source[self._start : self._current]),
        )

    def _identifier(self) -> None:
        while self._isAlphaNumeric():
            self._current += 1

        text: str = self._source[self._start : self._current]
        type: TokenType | None = IDENTIFIER_MAP.get(text, None)
        if type is None:
            type = TokenType.IDENTIFIER
        self._addToken(type)

    def _isAlpha(self) -> bool:
        c: int = ord(self._source[self._current])
        return (
            (c >= ord("a") and c <= ord("z"))
            or (c >= ord("A") and c <= ord("Z"))
            or (c == ord("_"))
        )

    def _isAlphaNumeric(self) -> bool:
        return self._isAlpha() or str.isdigit(self._source[self._current])
