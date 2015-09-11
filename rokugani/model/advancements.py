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

    def _set_option(self, value):
        result = self.options.get(value)
        if result is None:
            raise KeyError(value)
        self._value = value
        return result

    @property
    def options(self):
        return self._get_options()

    def _get_options(self):
        return {}



class AdvancementSkill(_AdvancementBase):

    NAME = 'skill'

    def __init__(self, builder, tags=()):
        super(AdvancementSkill, self).__init__(builder)
        self._tags = set(tags)

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.skills
            if not self._tags or set(i.tags).intersection(self._tags)
        }

    def set_value(self, value):
        skill = self._set_option(value)
        self._builder.add_skill(skill.id, 1, self.source)


class AdvancementSchool(_AdvancementBase):

    NAME = 'school'

    def __init__(self, builder, clanid):
        super(AdvancementSchool, self).__init__(builder)
        self._clanid = clanid

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.schools
            if i.clanid == self._clanid and len(i.require) == 0
        }

    def set_value(self, value):
        school = self._set_option(value)

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
            self._builder.add_skill(i_skill.id, i_skill.rank, self.source)
        # Skills (wildcards)
        for i_skill in school.skills_pc:
            tags = [i.value for i in i_skill.wildcards]
            self._builder.add_advancement(AdvancementSkill(self._builder, tags=tags))
        self._builder.set_value(self.NAME, value)


class AdvancementFamily(_AdvancementBase):

    NAME = 'family'

    def __init__(self, builder, clanid):
        super(AdvancementFamily, self).__init__(builder)
        self._clanid = clanid

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.families
            if i.clanid == self._clanid
        }

    def set_value(self, value):
        family = self._set_option(value)

        if family.trait in ('void',):
            self._builder.add_modifier('rings.%s' % family.trait, 1, self.source)
        else:
            self._builder.add_modifier('attribs.%s' % family.trait, 1, self.source)
        self._builder.set_value(self.NAME, value)


class AdvancementClan(_AdvancementBase):

    NAME = 'clan'

    def __init__(self, builder):
        super(AdvancementClan, self).__init__(builder)

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.clans
        }

    def set_value(self, value):
        clan = self._set_option(value)

        self._builder.add_advancement(AdvancementFamily(self._builder, value))
        self._builder.add_advancement(AdvancementSchool(self._builder, value))
        self._builder.set_value(self.NAME, value)
