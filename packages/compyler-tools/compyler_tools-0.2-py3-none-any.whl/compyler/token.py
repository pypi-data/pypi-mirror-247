from typing import Any

class Token:
    """A token is a representation of a sequence of symbols
    with an associated value

    Examples:
        ```
        >>> Token(name='INT', value=123)
        INT: 123
        ```
    """
    def __init__(self, name: str, value: Any) -> None:
        self.name: str = name
        self.value: Any = value

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __value: object) -> bool:
        return self.name == str(__value)

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"