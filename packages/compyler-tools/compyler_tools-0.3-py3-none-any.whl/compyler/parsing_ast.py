from __future__ import annotations
from typing import List, Union
from .lexer import Token

class ASTNode:
    """Stores a value and children
    """

    def __init__(self, name=Union[Token, str], children: List[Union[Token, ASTNode]] = None):
        self.name = name
        self.children: List[Union[Token, ASTNode]] = children if children is not None else list()

    def __str__(self) -> str:
        return self.name

    def __len__(self):
        return len(self.children)

    def __eq__(self, __value: object) -> bool:
        return self.name == str(__value)

    def __getitem__(self, __index):
        return self.children[__index]

    def __repr__(self) -> str:
        return self.name

    def add_children(self, *children: Union[Token, ASTNode]):
        """Adds children to the end of the children's list
        """
        for child in children:
            self.children.append(child)

    def representation(self, level: int = 1) -> str:
        """Returns a string representation of the
        ASTNode object and it's children

        It will be organised on a tree pattern

        Args:
            level (int, optional): the children level. Defaults to 1.

        Returns:
            str: the string representation of the ast
        """
        # print the name
        ast_string = f"{self.name}"

        # print the children
        for child in self.children:
            # add the indentation to the child
            ast_string += "\n" + "| "*level

            # recursively print the children
            if isinstance(child, ASTNode):
                ast_string += f"{str(child.representation(level+1))}"
                continue

            # just print the name of the token in case it isn't a child
            ast_string += f"{repr(child)}"

        return ast_string
