import pytest
from rokugani.model.character_model import CharacterModel
from rokugani.model.character_builder import CharacterBuilder, NoAdvancementError



def test_character_builder():

    ch = CharacterModel()

    builder = CharacterBuilder(ch)
    assert builder.tags == set()

    # Raises an error if trying to set a value that is not available on advancements.
    with pytest.raises(NoAdvancementError):
        builder.set_advancement_value('rubles', 'crab')

    with pytest.raises(KeyError):
        builder.set_advancement_value('clan', 'rubles')

    # We begin with one advancement only: the clan
    assert sorted([i.NAME for i in builder.advancements]) == ['clan']

    # These operations set a value defined by an advancement
    # They raise an error if no advancement is there to set.
    assert builder.get_value('clan') == ''
    builder.set_advancement_value('clan', 'crab')
    assert builder.get_value('clan') == 'crab'
    assert builder.tags == {'crab'}

    # Setting the clan will add the family advancement.
    assert sorted([i.NAME for i in builder.advancements]) == ['clan', 'family', 'school']
    assert builder.get_value('traits.strength') == 2
    builder.set_advancement_value('family', 'crab_hida')
    assert builder.get_value('traits.strength') == 3
    assert builder.tags == {'crab', 'crab_hida'}

    # Setting the family will add the school advancement
    assert sorted([i.NAME for i in builder.advancements]) == ['clan', 'family', 'school']
    assert builder.get_value('traits.stamina') == 2
    builder.set_advancement_value('school', 'crab_hida_bushi_school')

    assert builder.get_value('traits.stamina') == 3
    assert builder.get_value('skills.intimidation') == 1
    assert builder.get_value('skills.athletics') == 1
    assert builder.tags == {'crab', 'crab_hida', 'crab_bushi', 'bushi'}

    builder.add_trait('willpower', 1)
    builder.add_trait('agility', 1)

    builder.add_merit('large', 1)
    builder.add_merit('strength_of_the_earth', 1)
    builder.add_merit('quick_healer', 1)

    assert builder.get_value('skills.heavy_weapons') == 1
    builder.add_skill('heavy_weapons', 2)
    assert builder.get_value('skills.heavy_weapons') == 3

    builder.add_skill('lore_crab', 1)
    assert builder.get_value('skills.lore_crab') == 1


def test_add_merit():
    '''
    The usual merit price.
    '''
    ch = CharacterModel()
    builder = CharacterBuilder(ch)

    assert ch.get_value('xp') == 0
    builder.add_merit('large', 1, 'test merit', buy=True)
    assert ch.get_value('xp') == 4


def test_add_merit_special_cost():
    '''
    Crabs pay less for "large" merit.
    '''
    ch = CharacterModel()
    builder = CharacterBuilder(ch)
    builder.set_advancement_value('clan', 'crab')
    builder.set_advancement_value('family', 'crab_hida')
    builder.set_advancement_value('school', 'crab_hida_bushi_school')

    assert ch.get_value('xp') == 0
    builder.add_merit('large', 1, 'test merit', buy=True)
    assert ch.get_value('xp') == 3


def test_get_skills():
    ch = CharacterModel()
    builder = CharacterBuilder(ch)
    builder.set_advancement_value('clan', 'crab')
    builder.set_advancement_value('family', 'crab_hida')
    builder.set_advancement_value('school', 'crab_hida_bushi_school')

    skills = builder.get_skills()
    assert len(skills) == 6
    assert skills[0] == {
        'id': 'athletics',
        'model_attr': 'skills.athletics',
        'name': 'Athletics',
        'rank': 1,
        'trait': 'strength',
        'trait_short': 'str',
        'type': 'bugei',
        'obs' : '',
        'roll' : '4k3',
    }


def test_insight_rank():
    ch = CharacterModel()
    builder = CharacterBuilder(ch)
    assert builder.get_value('ranks.insight') == 100
    assert builder.get_value('ranks.rank') == 1

    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 110
    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 120
    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 130
    assert builder.get_value('ranks.rank') == 1
    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 140
    assert builder.get_value('ranks.rank') == 1

    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 150
    assert builder.get_value('ranks.rank') == 2

    builder.add_trait('void')
    builder.add_trait('void')
    builder.add_trait('void')
    assert builder.get_value('ranks.insight') == 180
    assert builder.get_value('ranks.rank') == 3
