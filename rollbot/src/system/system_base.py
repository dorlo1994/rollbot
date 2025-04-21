from abc import ABC, abstractmethod
from collections import namedtuple


Die = namedtuple('Die', ['min', 'max'])


class CharacterSheet(ABC):
    """
    This class encapsulates character sheets.
    """
    ...


class RolePlayingSystem(ABC):
    """
    This class encapsulates role-playing systems: Character sheets structure and Check handling.
    """
    @abstractmethod
    def character_sheet(self) -> CharacterSheet:
        ...

    @abstractmethod
    def check(self, *args):
        ...
