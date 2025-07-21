from tokens import Token, TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._tokens: list[Token] = []
        
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd:
            self._start = self._current
            _ = self.scanTokens()
        self._tokens.append(Token(0, TokenType.EOF, None, ""))
        return self._tokens

    def scanToken(self) -> None:
        pass

    @property
    def isAtEnd(self) -> bool:
        """Return boolean if source has finished"""
        return self._current >= len(self._source)
