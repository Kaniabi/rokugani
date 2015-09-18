

class ModelAttributeNotFound(KeyError):
    pass


class _ModelAttr(object):
    '''
    Base class for model attributes.
    '''

    def __init__(self, model):
        self._model = model


class AttribModel(_ModelAttr):

    def __init__(self, model, value):
        _ModelAttr.__init__(self, model)
        self._value = value

    @property
    def value(self):
        return self._value


class VoidRingModel(AttribModel):
    pass


class _ValueModelAttr(_ModelAttr):

    def __init__(self, model, value=None):
        _ModelAttr.__init__(self, model)
        self._value = value

    @property
    def value(self):
        return self._value


class CharacterInfoModel(_ValueModelAttr):
    pass


class ClanModel(_ValueModelAttr):
    pass


class FamilyModel(_ValueModelAttr):
    pass


class SchoolModel(_ValueModelAttr):
    pass


class MoneyModel(_ValueModelAttr):
    pass


class RankModel(_ValueModelAttr):
    pass


class PerkModel(_ValueModelAttr):
    pass


class DamageReductionModel(_ValueModelAttr):
    pass


class XpModel(_ValueModelAttr):
    pass


class RingModel(_ModelAttr):

    def __init__(self, model, attrib1, attrib2):
        _ModelAttr.__init__(self, model)
        self._attrib = [attrib1, attrib2]

    @property
    def value(self):
        value1 = self._model.get_value(self._attrib[0])
        value2 = self._model.get_value(self._attrib[1])
        return min(value1, value2)


class InsightModel(_ModelAttr):

    @property
    def value(self):
        rings = (
            self._model.get_value('rings.earth')
            + self._model.get_value('rings.air')
            + self._model.get_value('rings.water')
            + self._model.get_value('rings.fire')
            + self._model.get_value('rings.void')
        )
        skills = 0
        for i_name, i_skill in self._model.list_model_attrs('skills'):
            skills += self._model.get_value(i_name)
        return rings * 10 + skills


class InsightRankModel(_ModelAttr):

    @property
    def value(self):
        ranks = [
            300,
            275,
            250,
            225,
            200,
            175,
            150,
            0,
        ]
        insight = self._model.get_value('ranks.insight')
        return max(1, (insight - 100) // 25)


class SkillModel(_ModelAttr):

    def __init__(self, model, attrib, school_skill=False):
        _ModelAttr.__init__(self, model)
        self._value = 0
        self.attrib = attrib
        self.school_skill =  school_skill

    @property
    def value(self):
        return self._value


class WoundsModel(_ModelAttr):

    USAGE = 'wounds'

    def __init__(self, model, index):
        _ModelAttr.__init__(self, model)
        self._index = index

    @property
    def value(self):
        earth_ring = self._model.get_value('rings.earth')
        result = earth_ring * 5
        for i in range(self._index):
            result += earth_ring * 2
        return result


class WoundsPenaltyModel(_ModelAttr):

    _VALUES = [0,3,5,10,15,20,40,None]

    def __init__(self, model, index):
        _ModelAttr.__init__(self, model)
        self._index = index

    @property
    def value(self):
        return self._VALUES[self._index]


class InitiativeModel(_ModelAttr):

    def __init__(self, model, variation):
        _ModelAttr.__init__(self, model)
        self._variation = variation

    @property
    def value(self):
        if self._variation == 'modifiers':
            return '0k0'
        insight = self._model.get_value('ranks.rank')
        reflexes = self._model.get_value('traits.reflexes')
        return '{}k{}'.format(insight + reflexes, reflexes)


class ArmorTnBase(_ModelAttr):

    @property
    def value(self):
        reflexes = self._model.get_value('traits.reflexes')
        return 5 * (reflexes + 1)


class ArmorTnReduction(_ModelAttr):

    @property
    def value(self):
        reflexes = self._model.get_value('traits.reflexes')
        return 5 * (reflexes + 1)


class ArmorTnCurrent(_ModelAttr):

    @property
    def value(self):
        reflexes = self._model.get_value('traits.reflexes')
        return 5 * (reflexes + 1)


class _ModelAttrModifier(object):
    '''
    Attribute modifier, holding value and source.
    '''

    def __init__(self, value, source):
        self.value = value
        self.source = source
