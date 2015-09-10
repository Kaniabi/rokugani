

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


class InsightRankModel(_ValueModelAttr):
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


class SkillModel(_ModelAttr):

    def __init__(self, model, attrib):
        _ModelAttr.__init__(self, model)
        self._attrib = attrib
        self._value = 0

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


class _ModelAttrModifier(object):
    '''
    Attribute modifier, holding value and source.
    '''

    def __init__(self, value, source):
        self.value = value
        self.source = source


class CharacterModel(object):

    USAGE_TN = 'tn'
    USAGE_ATTACK = 'attack'
    USAGE_KIHO = 'kiho'
    USAGE_KATA = 'kata'
    USAGE_SPELL = 'spell'

    def __init__(self):
        self._model = {}
        self._fill_model()
        self._modifiers = {}


    def _fill_model(self):
        self._model['attribs.stamina'] = AttribModel(self, 2)
        self._model['attribs.willpower'] = AttribModel(self, 2)
        self._model['attribs.reflexes'] = AttribModel(self, 2)
        self._model['attribs.awareness'] = AttribModel(self, 2)
        self._model['attribs.strength'] = AttribModel(self, 2)
        self._model['attribs.perception'] = AttribModel(self, 2)
        self._model['attribs.agility'] = AttribModel(self, 2)
        self._model['attribs.intelligence'] = AttribModel(self, 2)

        self._model['rings.earth'] = RingModel(self, 'attribs.stamina', 'attribs.willpower')
        self._model['rings.air'] = RingModel(self, 'attribs.reflexes', 'attribs.awareness')
        self._model['rings.water'] = RingModel(self, 'attribs.perception', 'attribs.strength')
        self._model['rings.fire'] = RingModel(self, 'attribs.agility', 'attribs.intelligence')
        self._model['rings.void'] = VoidRingModel(self, 2)

        self._model['ranks.honor'] = RankModel(self, 0.0)
        self._model['ranks.glory'] = RankModel(self, 0.0)
        self._model['ranks.status'] = RankModel(self, 0.0)
        self._model['ranks.taint'] = RankModel(self, 0.0)
        self._model['ranks.infamy'] = RankModel(self, 0.0)

        self._model['ranks.insight'] = InsightRankModel(self, 0)

        self._model['wounds.healty'] = WoundsModel(self, 0)
        self._model['wounds.healty.penalty'] = WoundsPenaltyModel(self, 0)
        self._model['wounds.nicked'] = WoundsModel(self, 1)
        self._model['wounds.nicked.penalty'] = WoundsPenaltyModel(self, 1)
        self._model['wounds.grazed'] = WoundsModel(self, 2)
        self._model['wounds.grazed.penalty'] = WoundsPenaltyModel(self, 2)
        self._model['wounds.hurt'] = WoundsModel(self, 3)
        self._model['wounds.hurt.penalty'] = WoundsPenaltyModel(self, 3)
        self._model['wounds.injured'] = WoundsModel(self, 4)
        self._model['wounds.injured.penalty'] = WoundsPenaltyModel(self, 4)
        self._model['wounds.crippled'] = WoundsModel(self, 5)
        self._model['wounds.crippled.penalty'] = WoundsPenaltyModel(self, 5)
        self._model['wounds.down'] = WoundsModel(self, 6)
        self._model['wounds.down.penalty'] = WoundsPenaltyModel(self, 6)
        self._model['wounds.out'] = WoundsModel(self, 7)
#        self._model['wounds.out.penalty'] = WoundsPenaltyModel(self, 7)

        self._model['damage_reduction'] = DamageReductionModel(self, 0)

        self._model['money.bu'] = MoneyModel(self, 0)
        self._model['money.koku'] = MoneyModel(self, 0)
        self._model['money.zeni'] = MoneyModel(self, 0)

        self._model['clan'] = ClanModel(self)
        self._model['family'] = FamilyModel(self)
        self._model['school'] = SchoolModel(self)

        self._model['xp'] = XpModel(self, 30)

        # self._model['skills'] = []
        # self._model['kihos'] = []
        # self._model['katas'] = []
        # self._model['spells'] = []


    def add_model(self, model_attr, model_class, *args, **kwargs):
        self._model[model_attr] = model_class(self, *args, **kwargs)


    def get_value(self, model_attr, usage=None):
        '''
        Returns a model-attribute value considering all modifiers.

        :param unicode model_attr:
        :param USAGE_XXX usage:
        :return int:
        '''
        result = self._model[model_attr].value
        assert result is not None, 'Invalid value for model-attribute: "{0}"'.format(model_attr)
        for i in self._modifiers.get(model_attr, []):
            result += i.value
        return result


    def explain_value(self, model_attr):
        '''
        Explains all the bonuses for the given model-attribute.
        '''
        result = []
        for i in self._modifiers.get(model_attr, []):
            result.append((i.source, i.value))
        return result


    def set_value(self, model_attr, value):
        '''
        Sets the value of a model-attribute.

        * Sets the value directly, not using a modifier
        * The model-attribute may not accept setting its value => exception

        :param unicode model_attr:
        :param int value:
        '''
        attr = self._model[model_attr]
        attr._value = value


    def add_modifier(self, model_attr, value, source):
        '''
        Adds a modifiers to a model-attribute.

        :param unicode model_attr:
        :param int value:
        :param unicode source:
        '''
        if model_attr not in self._model:
            raise ModelAttributeNotFound(model_attr)
        model_attr_modifiers = self._modifiers.setdefault(model_attr, [])
        model_attr_modifiers.append(_ModelAttrModifier(value, source))


    def list_model_attrs(self, prefix):
        for i_name, i_value in sorted(self._model.items()):
            if i_name.startswith(prefix):
                yield i_name, i_value
