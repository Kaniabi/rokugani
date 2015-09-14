from rokugani.model.advancements import AdvancementClan
from rokugani.model.character_model import SkillModel, PerkModel



class RokuganiError(RuntimeError):
    pass


class NoAdvancementError(RokuganiError):
    pass


class CharacterBuilder(object):

    DATADIR = 'x:/rokugani/.datadir'

    def __init__(self, character_model):
        from .data_access import DataAccess
        self.data_access = DataAccess('x:/l5rcm-data-packs')

        self.__character = character_model
        self.__advancements = []

        # First advancement to build a character
        self.add_advancement(AdvancementClan(self))


    # Duplicate character interface to avoid external access to __character. Is this good?

    def expand(self, text):
        import re

        def Replacer(matchobj):
            key = matchobj.group(1)
            return str(self.get_value(key))

        expand_regex = re.compile('\{(.*?)\}')
        return expand_regex.sub(Replacer, text)


    def get_value(self, name):
        return self.__character.get_value(name)


    def set_value(self, name, value):
        return self.__character.set_value(name, value)


    def add_model(self, model_attr, model_class, *args, **kwargs):
        return self.__character.add_model(model_attr, model_class, *args, **kwargs)


    def add_modifier(self, model_attr, value, source):
        return self.__character.add_modifier(model_attr, value, source)


    def add_skill(self, skill_id, rank, source, buy=False):
        skill = self.data_access.find_skill(skill_id)

        model_attr = 'skills.{}'.format(skill.id)
        if not self.__character.has_model(model_attr):
            attrib = 'attribs.{}'.format(skill.trait)
            self.__character.add_model(model_attr, SkillModel, attrib=attrib)

        self.__character.add_modifier(model_attr, rank, source)
        if buy:
            cost = self.__character.get_value(model_attr)
            self.__character.add_modifier('xp', -cost, source)


    def add_merit(self, merit_id, rank, source, buy=False):
        merit = self.data_access.find_merit(merit_id)

        model_attr = 'merits.{}'.format(merit.id)
        if self.__character.has_model(model_attr):
            raise KeyError(model_attr)
        self.__character.add_model(model_attr, PerkModel, rank)

        if buy:
            cost = merit.ranks[0].value
            self.__character.add_modifier('xp', -cost, source)


    def add_flaw(self, flaw_id, rank, source, buy=False):
        flaw = self.data_access.find_flaw(flaw_id)

        model_attr = 'flaws.{}'.format(flaw.id)
        if self.__character.has_model(model_attr):
            raise KeyError(model_attr)
        self.__character.add_model(model_attr, PerkModel, rank)

        if buy:
            cost = flaw.ranks[0].value
            self.__character.add_modifier('xp', cost, source)


    def list_model_attrs(self, prefix):
        return self.__character.list_model_attrs(prefix)

    # Advancements

    @property
    def advancements(self):
        return self.__advancements


    def _find_advancement(self, name):
        for i_advancement in self.__advancements:
            if i_advancement.NAME == name:
                return i_advancement
        return None


    def add_advancement(self, advancement):
        self.__advancements.append(advancement)


    def set_advancement_value(self, name, value):
        advancement = self._find_advancement(name)
        if advancement is None:
            raise NoAdvancementError(name)

        advancement.set_value(value)

    # Shopping

    def buy(self, name, field, value):

        if name == 'attrib':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy:{0}.{1}'.format(name, field)
            cost = 1
            self.__character.add_modifier(model_attr, value, source)
            self.__character.add_modifier('xp', -cost, source)

        elif name == 'perk':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy:{0}.{1}'.format(name, field)
            cost = 1

            perks = {i.id : i for i in self.data_access.merits}
            perk = perks.get(field)
            if perk is None:
                raise KeyError(field)

            self.__character.add_model(model_attr, PerkModel, 0)
            self.__character.add_modifier(model_attr, value, source)
            self.__character.add_modifier('xp', -cost, source)

        elif name == 'skill':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy:{0}.{1}'.format(name, field)
            cost = 1

            skills = {i.id : i for i in self.data_access.skills}
            skill  = skills.get(field)
            if skill is None:
                raise KeyError(field)

            self.__character.add_model(model_attr, SkillModel, attrib='attribs.agility')
            self.__character.add_modifier(model_attr, value, source)
            self.__character.add_modifier('xp', -cost, source)
        else:
            assert False, 'Unknown buy name {0}'.format(name)
