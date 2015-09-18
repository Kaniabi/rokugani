from .model_attr import *
from rokugani.model.model_attr import _ModelAttrModifier



class CharacterModel(object):

    def __init__(self):
        from ben10.foundation.callback import Callback

        self._model = {}
        self._fill_model()
        self._modifiers = {}

        self.on_model_change = Callback()


    def _fill_model(self):
        self._model['character.name'] = CharacterInfoModel(self, '')

        self._model['traits.stamina'] = AttribModel(self, 2)
        self._model['traits.willpower'] = AttribModel(self, 2)
        self._model['traits.reflexes'] = AttribModel(self, 2)
        self._model['traits.awareness'] = AttribModel(self, 2)
        self._model['traits.strength'] = AttribModel(self, 2)
        self._model['traits.perception'] = AttribModel(self, 2)
        self._model['traits.agility'] = AttribModel(self, 2)
        self._model['traits.intelligence'] = AttribModel(self, 2)

        self._model['rings.earth'] = RingModel(self, 'traits.stamina', 'traits.willpower')
        self._model['rings.air'] = RingModel(self, 'traits.reflexes', 'traits.awareness')
        self._model['rings.water'] = RingModel(self, 'traits.perception', 'traits.strength')
        self._model['rings.fire'] = RingModel(self, 'traits.agility', 'traits.intelligence')
        self._model['rings.void'] = VoidRingModel(self, 2)

        self._model['ranks.honor'] = RankModel(self, 0.0)
        self._model['ranks.glory'] = RankModel(self, 0.0)
        self._model['ranks.status'] = RankModel(self, 0.0)
        self._model['ranks.taint'] = RankModel(self, 0.0)
        self._model['ranks.infamy'] = RankModel(self, 0.0)

        self._model['ranks.rank'] = InsightRankModel(self)
        self._model['ranks.insight'] = InsightModel(self)

        self._model['wounds.healthy'] = WoundsModel(self, 0)
        self._model['wounds.healthy.penalty'] = WoundsPenaltyModel(self, 0)
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

        self._model['armor_tn.base'] = ArmorTnBase(self)
        self._model['armor_tn.reduction'] = ArmorTnReduction(self)
        self._model['armor_tn.current'] = ArmorTnCurrent(self)

        self._model['armor.tn_bonus'] = ArmorTnCurrent(self)
        self._model['armor.quality'] = ArmorTnCurrent(self)
        self._model['armor.notes'] = ArmorTnCurrent(self)

        self._model['damage_reduction'] = DamageReductionModel(self, 0)

        self._model['money.bu'] = MoneyModel(self, 0)
        self._model['money.koku'] = MoneyModel(self, 0)
        self._model['money.zeni'] = MoneyModel(self, 0)

        self._model['clan'] = ClanModel(self, '')
        self._model['family'] = FamilyModel(self, '')
        self._model['school'] = SchoolModel(self, '')

        self._model['xp'] = XpModel(self, 0)
        self._model['xp_pool'] = XpModel(self, 40)

        self._model['initiative.base'] = InitiativeModel(self, 'base')
        self._model['initiative.modifiers'] = InitiativeModel(self, 'modifiers')
        self._model['initiative.current'] = InitiativeModel(self, 'current')


    def has_model(self, model_attr):
        return model_attr in self._model

    def add_model(self, model_attr, model_class, *args, **kwargs):
        self._model[model_attr] = model_class(self, *args, **kwargs)


    def get_value(self, model_attr):
        '''
        Returns a model-attribute value considering all modifiers.

        :param unicode model_attr:
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
        self.on_model_change(model_attr)


    def add_modifier(self, model_attr, value, source):
        '''
        Adds a modifiers to a model-attribute.

        :param unicode model_attr:
        :param int value:
        :param unicode source:
        '''
        if not self.has_model(model_attr):
            raise ModelAttributeNotFound(model_attr)
        model_attr_modifiers = self._modifiers.setdefault(model_attr, [])
        model_attr_modifiers.append(_ModelAttrModifier(value, source))
        self.on_model_change(model_attr)


    def list_model_attrs(self, prefix):
        for i_name, i_value in sorted(self._model.items()):
            if i_name.startswith(prefix):
                yield i_name, i_value
