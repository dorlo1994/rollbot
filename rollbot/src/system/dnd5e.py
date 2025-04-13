from system_base import CharacterSheet
from system_base import RolePlayingSystem
from random import randint
from enum import Enum


class Dnd5eCheckMod(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2


class Dnd5ECharacterSheet(CharacterSheet):
    ...


class Dnd5e(RolePlayingSystem):
    def check(self, stat: int, check_mod: Dnd5eCheckMod) -> int:
        roll = self.roll_d20() + stat
        if not check_mod:
            return roll
        alt_roll = self.roll_d20() + stat
        if check_mod == Dnd5eCheckMod.ADVANTAGE:
            return max(roll, alt_roll)
        else:
            return min(roll, alt_roll)

    @staticmethod
    def roll_d20():
        return randint(1, 20)

    def character_sheet(self) -> Dnd5ECharacterSheet:
        ...
