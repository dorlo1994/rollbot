from abc import ABC, abstractmethod
from enum import Enum


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
