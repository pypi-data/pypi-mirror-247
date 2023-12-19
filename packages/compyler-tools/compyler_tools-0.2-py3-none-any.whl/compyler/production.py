from typing import Tuple, Union, Dict, Iterator

class Production:
    """Stores the combinations of tokens that compose a production\n
    A production must also include the indices of which tokens or other
    productions will be used as children on the AST.\n\n

    This means that if the production is:
        `Vardecl: ID EQ INT PLUS INT SEMICOLON`
    
    And the indices are (2,4)\n
    
    The result in the AST would be:
    \n
    ```
    Vardecl
    |   INT
    |   INT
    ```
    
    Examples:
        ```
        >>> production = Production(
        ...     {
        ...         ("TOKEN1", "TOKEN2", "TOKEN3"): (1, 2),
        ...         ("TOKEN1", "TOKEN4", "TOKEN3"): (1, 2)
        ...     }
        ... )
        ```
    """
    def __init__(self, name: str, rules: Dict[Tuple[str], Tuple[int]]) -> None:
        self.name = name
        self.rules = rules

    def __str__(self) -> str:
        return self.name

    def __contains__(self, __value: Tuple[str]) -> bool:
        return __value in self.rules

    def __iter__(self) -> Iterator[Dict]:
        return iter(self.rules)

    def __eq__(self, __value: object) -> bool:
        return self.name == str(__value)

    def __len__(self):
        return len(self.rules)

    def get_indices(self, rule: Tuple[str]) -> Union[Tuple[int], None]:
        """Returns the indices of a given rule

        Args:
            rule (Tuple[str]): the rule to access on the map via hashing

        Returns:
            Tuple[int] | None: the indices of the given rule or None if the rule does not exist
        """
        return self.rules[rule] if rule in self.rules else None

    def add_rule(self, new_rule: Dict[Tuple[str], Tuple[int]]):
        """Adds a new rule to the rule dictionary

        Args:
            new_rule (Dict[Tuple[str], Tuple[int]]): the rule to add to the map
        """
        self.rules.update(new_rule)

    def __repr__(self) -> str:
        representation = f"{self.name}:  "

        for i, rule in enumerate(self.rules):
            # add the rule's tokens
            for token in rule:
                representation += f"{token} "
            representation += "->"

            # add the rule's indices
            for index in self.rules[rule]:
                representation += f" ${index}"

            # add a separator
            if i < len(self.rules) - 1:
                representation += "\n" + " "*len(self.name) + " | "

        return representation
