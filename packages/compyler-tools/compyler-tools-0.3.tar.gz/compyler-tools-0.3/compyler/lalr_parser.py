"""Contains a class ready to register productions
and one to store expressions
"""
from typing import Tuple, List, Union, Dict

from .lexer import Token
from .production import Production
from .parsing_ast import ASTNode


class LALRParser:
    """Composed by a list of productions.\n
    Uses LALR parsing on a token buffer to build an
    Abstract Syntax Tree.
    """

    def __init__(self) -> None:
        self.productions = list()

    def __len__(self):
        return len(self.productions)

    def __getitem__(self, __index):
        return self.productions[__index]


    def add_production(self, name: str, rules: Dict[Tuple[str], Tuple[int]]):
        """Adds a production to the production list

        Args:
            name (str): the name of the production
            rules (Dict[Tuple[str], Tuple[int]]): the rules of the production
        """
        self.productions.append(Production(name, rules))

    def try_reduce(self, stack: List[Union[Token, ASTNode]]) -> bool:
        """Attempts to reduce the stack to a production in the list

        Args:
            stack (List[Token | ASTNode]): A list of tokens or AST Nodes
        """
        if not stack:
            return False

        # check each production
        for production in self.productions:

            # check each rule
            for rule in production:

                # stack smaller than rule -> cannot be reduced
                if len(stack) < len(rule):
                    continue

                for i, string in enumerate(rule):
                    # top of stack doesnt follow rule -> cannot be reduced
                    if stack[i] != string:
                        break

                # top of stack follows rule -> reduce
                else:
                    # create AST Node
                    node = ASTNode(str(production))
                    for index in production.get_indices(rule):
                        node.add_children(stack[index])

                    for _ in range(len(rule)):
                        stack.pop(0)
                    stack.insert(0, node)

                    return True
        return False

    def parse(self, token_buffer: List[Token]) -> Union[ASTNode, Token]:
        """Parses the given token buffer and returns the Abstract Syntax Tree\n
        If the parser is unable to reduce all of the productions to a single one
        then the first element on the stack will be returned

        Args:
            token_buffer (List[Token]): a list of tokens returned by a lexer

        Returns:
            (ASTNode | Token): The AST
        """

        inverted_buffer = token_buffer[::-1]

        stack = []

        i = -1
        while i < len(inverted_buffer):

            if self.try_reduce(stack):
                continue

            i += 1

            if i < len(inverted_buffer):
                stack.insert(0, inverted_buffer[i])

        return stack[0]
