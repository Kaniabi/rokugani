from rokugani.model.character import SkillModel, PerkModel



class RokuganiError(RuntimeError):
    pass


class NoAdvancementError(RokuganiError):
    pass


class CharacterBuilder(object):

    def __init__(self, model):
        import dal

        self._locations = [
            u'C:\\Users\\Alexandre\\AppData\\Roaming\\openningia\\l5rcm\\core.data',
            u'C:\\Users\\Alexandre\\AppData\\Roaming\\openningia\\l5rcm\\data',
            u'C:\\Users\\Alexandre\\AppData\\Roaming\\openningia\\l5rcm\\data.en_US',
        ]
        self.dstore = dal.Data(self._locations, [])

        self._model = model

        self.advancements = []
        self.advancements.append('clan')


    def _find_advancement(self, name):
        for i_advancement in self.advancements:
            if i_advancement == name:
                return True
        return


    def set(self, name, value):
        advancement = self._find_advancement(name)
        if advancement is None:
            raise NoAdvancementError(name)

        if name == 'clan':
            clans = {i.id : i for i in self.dstore.clans}
            clan = clans.get(value)
            if clan is None:
                raise KeyError(value)
            self.advancements.append('family')

        elif name == 'family':
            clanid = self._model.get_value('clan')
            families = {i.id : i for i in self.dstore.families if i.clanid == clanid}
            family = families.get(value)
            if family is None:
                raise KeyError(value)

            source = 'family:%s' % value

            self._model.add_modifier('attribs.%s' % family.trait, 1, source)
            self.advancements.append('school')

        elif name == 'school':
            clanid = self._model.get_value('clan')
            schools = {i.id : i for i in self.dstore.schools if i.clanid == clanid and len(i.require) == 0}
            school = schools.get(value)
            if value is None:
                raise KeyError(value)

            source = 'school:%s' % value

            # Honor
            self._model.add_modifier('ranks.honor', school.honor, source)
            # Attrib
            self._model.add_modifier('attribs.%s' % school.trait, 1, source)
            # Money
            self._model.add_modifier('money.bu', school.money[0], source)
            self._model.add_modifier('money.koku', school.money[1], source)
            self._model.add_modifier('money.zeni', school.money[2], source)
            # Skills
            for i_skill in school.skills:
                model_attr = 'skills.{}'.format(i_skill.id)
                self._model.add_model(model_attr, SkillModel, attrib='attribs.agility')
                self._model.add_modifier(model_attr, i_skill.rank, source)
            # Skills (wildcards)
            for i_skill in school.skills_pc:
                tags = [i.value for i in i_skill.wildcards]
                self.advancements.append('skill:%s' % ':'.join(tags))
            # Techs?
            for i_tech in school.techs:
                pass
                #self.advancements.append('skill:%s' % ':'.join(tags))

        else:
            raise KeyError(name)

        self._model.set_value(name, value)


    def buy(self, name, field, value):

        if name == 'attrib':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy {0}.{1}'.format(name, field)
            cost = 1
            self._model.add_modifier(model_attr, value, source)
            self._model.add_modifier('xp', -cost, source)

        elif name == 'perk':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy {0}.{1}'.format(name, field)
            cost = 1

            perks = {i.id : i for i in self.dstore.merits}
            perk = perks.get(field)
            if perk is None:
                raise KeyError(field)

            self._model.add_model(model_attr, PerkModel, 0)
            self._model.add_modifier(model_attr, value, source)
            self._model.add_modifier('xp', -cost, source)

        elif name == 'skill':
            model_attr = '{0}s.{1}'.format(name, field)
            source = 'buy {0}.{1}'.format(name, field)
            cost = 1

            skills = {i.id : i for i in self.dstore.skills}
            skill  = skills.get(field)
            if skill is None:
                raise KeyError(field)

            self._model.add_model(model_attr, SkillModel, attrib='attribs.agility')
            self._model.add_modifier(model_attr, value, source)
            self._model.add_modifier('xp', -cost, source)
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