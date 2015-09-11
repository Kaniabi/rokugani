from rokugani.model.character_model import SkillModel, PerkModel



class RokuganiError(RuntimeError):
    pass


class NoAdvancementError(RokuganiError):
    pass


class _AdvancementBase(object):

    NAME = '?'

    def __init__(self, builder):
        self._builder = builder
        self._value = '?'

    @property
    def source(self):
        return '{}:{}'.format(self.NAME, self._value)

    def __str__(self):
        return self.source


class AdvancementSchool(_AdvancementBase):

    NAME = 'school'

    def __init__(self, builder, clanid):
        super(AdvancementSchool, self).__init__(builder)
        self._clanid = clanid
        self.options = {
            i.id : i
            for i in self._builder.data_access.schools
            if i.clanid == self._clanid and len(i.require) == 0
        }

    def set_value(self, value):
        school = self.options.get(value)
        if value is None:
            raise KeyError(value)
        self._value = value

        # Honor
        self._builder.add_modifier('ranks.honor', school.honor, self.source)
        # Attrib
        if school.trait in ('void',):
            self._builder.add_modifier('rings.%s' % school.trait, 1, self.source)
        else:
            self._builder.add_modifier('attribs.%s' % school.trait, 1, self.source)
        # Money
        self._builder.add_modifier('money.bu', school.money[0], self.source)
        self._builder.add_modifier('money.koku', school.money[1], self.source)
        self._builder.add_modifier('money.zeni', school.money[2], self.source)
        # Skills
        for i_skill in school.skills:
            model_attr = 'skills.{}'.format(i_skill.id)
            self._builder.add_model(model_attr, SkillModel, attrib='attribs.agility')
            self._builder.add_modifier(model_attr, i_skill.rank, self.source)
        # Skills (wildcards)
        for i_skill in school.skills_pc:
            tags = [i.value for i in i_skill.wildcards]
            #self._builder.add_advancement('skill:{}'.format(':'.join(tags)))
        self._builder.set_value(self.NAME, value)


class AdvancementFamily(_AdvancementBase):

    NAME = 'family'

    def __init__(self, builder, clanid):
        super(AdvancementFamily, self).__init__(builder)
        self._clanid = clanid
        self.options = {
            i.id : i
            for i in self._builder.data_access.families
            if i.clanid == self._clanid
        }

    def set_value(self, value):
        family = self.options.get(value)
        if family is None:
            raise KeyError(value)
        self._value = value

        if family.trait in ('void',):
            self._builder.add_modifier('rings.%s' % family.trait, 1, self.source)
        else:
            self._builder.add_modifier('attribs.%s' % family.trait, 1, self.source)
        self._builder.set_value(self.NAME, value)


class AdvancementClan(_AdvancementBase):

    NAME = 'clan'

    def __init__(self, builder):
        super(AdvancementClan, self).__init__(builder)
        self.options = {
            i.id : i
            for i in self._builder.data_access.clans
        }

    def set_value(self, value):
        clan = self.options.get(value)
        if clan is None:
            raise KeyError(value)
        self._value = value

        self._builder.add_advancement(AdvancementFamily(self._builder, value))
        self._builder.add_advancement(AdvancementSchool(self._builder, value))
        self._builder.set_value(self.NAME, value)


class CharacterBuilder(object):

    DATADIR = 'x:/rokugani/.datadir'

    def __init__(self, character_model):
        from .l5rcm_data_access import L5rcmDataAccess
        self.data_access = L5rcmDataAccess('x:/l5rcm-data-packs')

        self.__character = character_model
        self.__advancements = []

        # First advancement to build a character
        self.add_advancement(AdvancementClan(self))


    # Duplicate character interface to avoid external access to __character. Is this good?

    def get_value(self, name):
        return self.__character.get_value(name)


    def set_value(self, name, value):
        return self.__character.set_value(name, value)


    def add_model(self, model_attr, model_class, *args, **kwargs):
        return self.__character.add_model(model_attr, model_class, *args, **kwargs)


    def add_modifier(self, model_attr, value, source):
        return self.__character.add_modifier(model_attr, value, source)


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


TECHS = {
    'crab_the_way_of_the_crab' : [
        dict(attr_model='skill.rolls', tag='agility', except_='stealth', source='heavy_armor', value=0),
        dict(attr_model='rolls.damage', condition='wearing:heavy_weapon', value='1k0'),
    ],
    'crab_the_mountain_does_not_move' : [
        dict(attr_model='damage_reduction', value='rings.earth'),
    ],
    'crab_two_pincers_one_mind' : [
        dict(attr_model='actions.attack.action_type', value='simple'),
    ],
}