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


    def get_trait_value(self, trait):
        if trait == 'void':
            return self.get_value('rings.void')
        else:
            return self.get_value('traits.{}'.format(trait))


    def explain_value(self, name):
        return self.__character.explain_value(name)


    def set_value(self, name, value):
        return self.__character.set_value(name, value)


    def add_model(self, model_attr, model_class, *args, **kwargs):
        return self.__character.add_model(model_attr, model_class, *args, **kwargs)


    def add_modifier(self, model_attr, value, source):
        return self.__character.add_modifier(model_attr, value, source)


    def get_skills(self):
        """
        Returns the list of character skills as dicts.
        """
        result = []
        for i_model_attr, i_skill_model in self.list_model_attrs('skills'):
            skill_name = i_model_attr.split('.')[-1]
            skill_data = self.data_access.find_skill(skill_name)
            skill_value = self.get_value(i_model_attr)
            try:
                trait_value = self.get_trait_value(skill_data.trait)
            except KeyError:
                trait_value = 0
            result.append(
                {
                    'model_attr' : i_model_attr,
                    'id' : skill_data.id,
                    'name' : skill_data.name,
                    'trait' : skill_data.trait,
                    'trait_short' : skill_data.trait[:3],
                    'type' : skill_data.type,
                    'rank' : skill_value,
                    'roll' : '{}k{}'.format(skill_value + trait_value, trait_value),
                    'obs' : '',
                    'school' : 'X' if i_skill_model.school_skill else '',
                }
            )
        for i_advancement in self.__advancements:
            if i_advancement.NAME == 'skill' and i_advancement.value == '?':
                result.append(
                    {
                        'advancement' : i_advancement,
                        'model_attr' : '',
                        'id' : '',
                        'name' : '?',
                        'trait' : '?',
                        'trait_short' : '?',
                        'type' : '',
                        'rank' : 1,
                        'roll' : '?',
                        'obs' : ','.join(i_advancement._tags),
                        'school' : 'X' if i_advancement.school_skill else '',
                    }
                )
        return result


    def add_skill(self, skill_id, rank, source='', buy=False, school_skill=False):
        skill = self.data_access.find_skill(skill_id)

        model_attr = 'skills.{}'.format(skill.id)
        if not self.__character.has_model(model_attr):
            attrib = 'traits.{}'.format(skill.trait)
            self.__character.add_model(
                model_attr,
                SkillModel,
                attrib=attrib,
                school_skill=school_skill,
            )

        self.__character.add_modifier(model_attr, rank, source)
        if buy:
            cost = self.__character.get_value(model_attr)
            self.__character.add_modifier('xp', cost, source)


    def add_merit(self, merit_id, rank, source='', buy=False):
        merit = self.data_access.find_merit(merit_id)

        model_attr = 'merits.{}'.format(merit.id)
        if self.__character.has_model(model_attr):
            raise KeyError(model_attr)
        self.__character.add_model(model_attr, PerkModel, rank)

        if buy:
            cost = self._get_perk_cost(merit)
            self.__character.add_modifier('xp', cost, source)


    def add_flaw(self, flaw_id, rank, source='', buy=False):
        flaw = self.data_access.find_flaw(flaw_id)

        model_attr = 'flaws.{}'.format(flaw.id)
        if self.__character.has_model(model_attr):
            raise KeyError(model_attr)
        self.__character.add_model(model_attr, PerkModel, rank)

        if buy:
            bonus = self._get_perk_cost(flaw)
            self.__character.add_modifier('xp', - bonus, source)


    def add_trait(self, trait_id, source='', buy=False):

        cost_multiplier = 4
        if '.' in trait_id:
            model_attr = trait_id
        elif trait_id == 'void':
            model_attr = 'rings.{}'.format(trait_id)
        else:
            model_attr = 'traits.{}'.format(trait_id)

        if 'void' in model_attr:
            cost_multiplier = 5

        if not self.__character.has_model(model_attr):
            raise KeyError(model_attr)
        self.__character.add_modifier(model_attr, 1, source)

        if buy:
            cost = self.get_value(model_attr) * cost_multiplier
            self.__character.add_modifier('xp', cost, source)


    def _get_perk_cost(self, perk):
        """
        Returns the cost of a given perk object considering rank and exceptions.
        """
        for i_rank in perk.ranks:
            for j_exception in i_rank.exceptions:
                if self._match_tags(j_exception.tag):
                    return j_exception.value
            return i_rank.value
        raise RuntimeError()


    def _match_tags(self, tag):
        if tag in self.tags:
            return True
        return False


    @property
    def tags(self):
        result = set()
        clan = self.__character.get_value('clan')
        if clan:
            result.add(clan)
        family = self.__character.get_value('family')
        if family:
            result.add(family)
        school_id = self.__character.get_value('school')
        if school_id:
            school = self.data_access.find_school(school_id)
        else:
            school = None
        if school:
            result = result.union(set(school.tags))
        return result


    def list_model_attrs(self, prefix):
        return self.__character.list_model_attrs(prefix)

    # Advancements

    @property
    def advancements(self):
        return self.__advancements


    def find_advancement(self, name):
        for i_advancement in self.__advancements:
            if i_advancement.NAME == name:
                return i_advancement
        return None


    def add_advancement(self, advancement):
        self.__advancements.append(advancement)


    def get_advancement_value(self, name):
        advancement = self.find_advancement(name)
        if advancement is None:
            return '?'
        return self.get_value(name)


    def set_advancement_value(self, name, value):
        advancement = self.find_advancement(name)
        if advancement is None:
            raise NoAdvancementError(name)

        advancement.set_value(value)

    # # Shopping
    #
    # def buy(self, name, field, value):
    #
    #     if name == 'attrib':
    #         model_attr = '{0}s.{1}'.format(name, field)
    #         source = 'buy:{0}.{1}'.format(name, field)
    #         cost = 1
    #         self.__character.add_modifier(model_attr, value, source)
    #         self.__character.add_modifier('xp', -cost, source)
    #
    #     elif name == 'perk':
    #         model_attr = '{0}s.{1}'.format(name, field)
    #         source = 'buy:{0}.{1}'.format(name, field)
    #         cost = 1
    #
    #         perks = {i.id : i for i in self.data_access.merits}
    #         perk = perks.get(field)
    #         if perk is None:
    #             raise KeyError(field)
    #
    #         self.__character.add_model(model_attr, PerkModel, 0)
    #         self.__character.add_modifier(model_attr, value, source)
    #         self.__character.add_modifier('xp', -cost, source)
    #
    #     elif name == 'skill':
    #         model_attr = '{0}s.{1}'.format(name, field)
    #         source = 'buy:{0}.{1}'.format(name, field)
    #         cost = 1
    #
    #         skills = {i.id : i for i in self.data_access.skills}
    #         skill  = skills.get(field)
    #         if skill is None:
    #             raise KeyError(field)
    #
    #         self.__character.add_model(model_attr, SkillModel, attrib='traits.agility')
    #         self.__character.add_modifier(model_attr, value, source)
    #         self.__character.add_modifier('xp', -cost, source)
    #     else:
    #         assert False, 'Unknown buy name {0}'.format(name)
