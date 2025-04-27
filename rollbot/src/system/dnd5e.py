from rollbot.src.system.system_base import CharacterSheet, RolePlayingSystem, Die, roll_die
from enum import Enum, Flag, auto

############################################
# CONSTANTS
############################################

# Define the Die struct and dice used in DnD
d4 = Die(1, 4)
d6 = Die(1, 6)
d8 = Die(1, 8)
d10 = Die(1, 10)
d00 = Die(1, 100)
d12 = Die(1, 12)
d20 = Die(1, 20)


class SkillModifier(Flag):
    PROFICIENCY = auto()
    EXPERTISE = auto()


class Dnd5eCheckMod(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2

############################################
# UTILITY CLASSES
############################################

class Stat:
    def __init__(self, score: int):
        self.score = score

    @property
    def modifier(self) -> int:
        return int((self.score - 10) / 2)


class Skill:
    def __init__(self, stat: Stat, modifier: SkillModifier):
        self.stat = stat
        self.modifier = modifier

    def score(self, prof_bonus: int) -> int:
        prof_multiplier = 0
        if SkillModifier.PROFICIENCY in self.modifier:
            prof_multiplier += 1
            if SkillModifier.EXPERTISE in self.modifier:
                prof_multiplier += 1
        return self.stat.modifier + (prof_bonus * prof_multiplier)

STATS = ['str', 'dex', 'con', 'int', 'wis', 'cha']
SKILLS = {
    'acrobatics': 'dex',
    'animal handling': 'wis',
    'arcana': 'int',
    'athletics': 'str',
    'deception': 'cha',
    'history': 'int',
    'insight': 'wis',
    'intimidation': 'cha',
    'investigation': 'int',
    'medicine': 'wis',
    'nature': 'int',
    'perception': 'wis',
    'performance': 'cha',
    'persuasion': 'cha',
    'religion': 'int',
    'sleight of hand': 'dex',
    'stealth': 'dex',
    'survival': 'wis'
}


class Dnd5ECharacterSheet(CharacterSheet):
    def __init__(self, name: str, level: int, stat_scores: list[int], proficiencies: list[str], expertise: list[str] = None):
        assert len(stat_scores) == len(STATS) and all([1 <= stat <= 20 for stat in stat_scores])
        self._stats = {stat: Stat(score) for stat, score in zip(STATS, stat_scores)}
        self.name = name
        self.level = level
        modifiers: dict[str, SkillModifier] = {skill: SkillModifier(0) for skill in SKILLS.keys()}
        for skill in proficiencies:
            modifiers[skill] |= SkillModifier.PROFICIENCY
        if expertise:
            for skill in expertise:
                assert skill in proficiencies
                modifiers[skill] |= SkillModifier.EXPERTISE
        self._skills = {skill: Skill(self._stats[stat], modifiers[skill]) for skill, stat in SKILLS.items()}

    @property
    def proficiency_modifier(self):
        return 2 + (self.level - 1) // 4

    def __repr__(self):
        character_str: str = ''
        character_str += f'Name: {self.name}\n'
        character_str += f'Level: {self.level}\n'
        character_str += f'Stats: {'\t\n'.join([f'{stat}: {s.score}' for stat, s in self._stats.items()])}'
        return character_str

class Dnd5e(RolePlayingSystem):
    EXP = 'EXPERTISE'
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

    def character_sheet(self, args_list: list[str]) -> Dnd5ECharacterSheet:
        name = args_list.pop(0)
        level = int(args_list.pop(0))
        stats = [int(stat) for stat in args_list[0:len(STATS)]]
        proficiencies = [prof for prof in args_list[len(STATS): args_list.index(self.EXP) if self.EXP in args_list else len(args_list)]]
        expertise = None
        if self.EXP in args_list:
            expertise = args_list[args_list.index(self.EXP)+1:]
        return Dnd5ECharacterSheet(name, level, stats, proficiencies, expertise)

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition'
