from rollbot.src.system.system_base import CharacterSheet, RolePlayingSystem, Die, roll_die
from enum import Enum

# Define the Die struct and dice used in DnD
d4 = Die(1, 4)
d6 = Die(1, 6)
d8 = Die(1, 8)
d10 = Die(1, 10)
d00 = Die(1, 100)
d12 = Die(1, 12)
d20 = Die(1, 20)


class Dnd5eCheckMod(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2


class Dnd5ECharacterSheet(CharacterSheet):
    ...


class Dnd5e(RolePlayingSystem):
    def check(self, stat: int = 0, check_mod: Dnd5eCheckMod = Dnd5eCheckMod.NONE) -> int:
        roll = roll_die(d20) + stat
        if check_mod == Dnd5eCheckMod.NONE:
            return roll
        alt_roll = roll_die(d20) + stat
        if check_mod == Dnd5eCheckMod.ADVANTAGE:
            return max(roll, alt_roll)
        elif check_mod == Dnd5eCheckMod.DISADVANTAGE:
            return min(roll, alt_roll)
        else:
            raise ValueError(f'Unknown roll modifier {check_mod}')

    @staticmethod
    def roll(desc: str) -> int:
        ...

    def character_sheet(self) -> Dnd5ECharacterSheet:
        ...

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition'
