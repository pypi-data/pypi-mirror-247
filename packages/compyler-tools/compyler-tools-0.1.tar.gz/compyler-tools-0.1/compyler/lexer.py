"""Contains a class ready to register tokens
"""
import re
from typing import List, Set
from .token import Token

class Lexer:
    """A lexer is composed by tokens\n
    The tokens are registered in order of importance
    """
    def __init__(self):
        self.tokens: List[Token] = list()

    def __len__(self):
        return len(self.tokens)

    def __contains__(self, _value) -> bool:
        for token in self.tokens:
            if token[0] == _value:
                return True
        return False

    def __repr__(self) -> str:
        return f"Lexer with {len(self.tokens)} registered tokens"

    def filter(self, filters: Set[str], token_buffer: List[Token]):
        """Removes the specified tokens from the token buffer

        Args:
            filters (Set[str]): the names of the tokens to remove
            token_buffer (List[Token]): the list of gathered tokens
        """
        i = 0
        while i < len(token_buffer):
            if token_buffer[i] in filters:
                token_buffer.pop(i)
                continue
            i += 1


    def add_token(self, name: str, regex: str):
        """A token can be registered by giving
        - its name
        - the regular expression that defines it

        Args:
            name (str): the name of the token
            regex (str): the regular expression that defines the token
        """
        self.tokens.append((name, regex))

    def get_regex(self) -> str:
        """Returns the entire regex of the lexer\n
        In this case, the formed regex is composed by groups

        Returns:
            str: the regular expression of the lexer
        """
        return "|".join(f"(?P<{token[0]}>{token[1]})" for token in self.tokens)

    def tokenize(self, text: str) -> List[Token]:
        """Uses the registered tokens to tokenize a given string\n
        Returns a buffer with the matched tokens.\n
        All the characters that did not match on the regex are ignored and will not be included

        Args:
            text (str): the string to tokenize

        Returns:
            List[Token]: a list of tuples composed by the name of the token
            and it's value in the string
        """

        matches = re.finditer(self.get_regex(), text)

        tokenized_string = list()

        for match in matches:
            tokenized_string.append(
                Token(name=match.lastgroup, value=match.group())
            )

        return tokenized_string
