


class _AdvancementBase(object):

    NAME = '?'

    def __init__(self, builder):
        self._builder = builder
        self.value = '?'

    @property
    def source(self):
        return '{}:{}'.format(self.NAME, self.value)

    def __str__(self):
        return self.source

    def _set_option(self, value):
        result = self.options.get(value)
        if result is None:
            raise KeyError(value)
        self.value = value
        return result

    @property
    def options(self):
        return self._get_options()

    def _get_options(self):
        return {}


class AdvancementSkill(_AdvancementBase):

    NAME = 'skill'

    def __init__(self, builder, tags=(), buy=False, school_skill=False, new_skills=False):
        super(AdvancementSkill, self).__init__(builder)
        self._tags = set(tags)
        self._buy = buy
        self._new_skills = new_skills
        self.school_skill = school_skill

    def _get_options(self):
        skills = [i['id'] for i in self._builder.get_skills()]
        result = self._builder.data_access.skills[:]
        if self._new_skills:
            result = [i for i in result if i.id not in skills]
        return {
            i.id : i
            for i in result
            if not self._tags or set(i.tags).intersection(self._tags)
        }

    def set_value(self, value):
        skill = self._set_option(value)
        self._builder.add_skill(
            skill.id,
            1,
            self.source,
            buy=self._buy,
            school_skill=self.school_skill,
        )


class AdvancementMerit(_AdvancementBase):

    NAME = 'merit'

    def __init__(self, builder, tags=(), buy=False):
        super(AdvancementMerit, self).__init__(builder)
        self._tags = set(tags)
        self._buy = buy

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.merits
        }

    def set_value(self, value):
        merit = self._set_option(value)
        self._builder.add_merit(merit.id, 1, self.source, buy=self._buy)


class AdvancementFlaw(_AdvancementBase):

    NAME = 'flaw'

    def __init__(self, builder, tags=(), buy=False):
        super(AdvancementFlaw, self).__init__(builder)
        self._tags = set(tags)
        self._buy = buy

    def _get_options(self):
        return {
            i.id : i
            for i in self._builder.data_access.flaws
        }

    def set_value(self, value):
        flaw = self._set_option(value)
        self._builder.add_flaw(flaw.id, 1, self.source, buy=self._buy)


class AdvancementTrait(_AdvancementBase):

    NAME = 'trait'

    def __init__(self, builder, tags=(), buy=False):
        super(AdvancementTrait, self).__init__(builder)
        self._tags = set(tags)
        self._buy = buy

    def _get_options(self):
        result = {
            i.id : i
            for i in self._builder.data_access.traits
        }
        rings = {i.id : i for i in self._builder.data_access.rings}
        result['void'] = rings['void']
        return result

    def set_value(self, value):
        trait = self._set_option(value)
        self._builder.add_trait(trait.id, self.source, buy=self._buy)


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
            self._builder.add_modifier('traits.%s' % school.trait, 1, self.source)
        # Money
        self._builder.add_modifier('money.bu', school.money[0], self.source)
        self._builder.add_modifier('money.koku', school.money[1], self.source)
        self._builder.add_modifier('money.zeni', school.money[2], self.source)
        # Skills
        for i_skill in school.skills:
            self._builder.add_skill(
                i_skill.id,
                i_skill.rank,
                source=self.source,
                school_skill=True
            )
        # Skills (wildcards)
        for i_skill in school.skills_pc:
            tags = [i.value for i in i_skill.wildcards]
            self._builder.add_advancement(
                AdvancementSkill(
                    self._builder,
                    tags=tags,
                    school_skill=True,
                    new_skills=True,
                )
            )
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
            self._builder.add_modifier('traits.%s' % family.trait, 1, self.source)
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
