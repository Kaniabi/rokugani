import pytest
from rokugani.model.character_model import CharacterModel
from rokugani.model.character_builder import CharacterBuilder, NoAdvancementError



def test_character_builder():

    ch = CharacterModel()

    builder = CharacterBuilder(ch)

    # Raises an error if trying to set a value that is not available on advancements.
    with pytest.raises(NoAdvancementError):
        builder.set_advancement_value('rubles', 'crab')

    # We begin with one advancement only: the clan
    assert sorted([i.NAME for i in builder.advancements]) == ['clan']

    # These operations set a value defined by an advancement
    # They raise an error if no advancement is there to set.
    assert ch.get_value('clan') == ''
    builder.set_advancement_value('clan', 'crab')
    assert ch.get_value('clan') == 'crab'

    # Setting the clan will add the family advancement.
    assert sorted([i.NAME for i in builder.advancements]) == ['clan', 'family', 'school']
    assert ch.get_value('attribs.strength') == 2
    builder.set_advancement_value('family', 'crab_hida')
    assert ch.get_value('attribs.strength') == 3

    # Setting the family will add the school advancement
    assert sorted([i.NAME for i in builder.advancements]) == ['clan', 'family', 'school']
    assert ch.get_value('attribs.stamina') == 2
    builder.set_advancement_value('school', 'crab_hida_bushi_school')

    assert ch.get_value('attribs.stamina') == 3
    assert ch.get_value('skills.intimidation') == 1
    assert ch.get_value('skills.athletics') == 1

    builder.buy('attrib', 'willpower', 1)
    builder.buy('attrib', 'agility', 1)

    builder.buy('perk', 'large', 1)
    builder.buy('perk', 'strength_of_the_earth', 1)
    builder.buy('perk', 'quick_healer', 1)

    assert ch.get_value('skills.heavy_weapons') == 1
    builder.buy('skill', 'heavy_weapons', 2)
    assert ch.get_value('skills.heavy_weapons') == 3

    builder.buy('skill', 'lore_crab', 1)
    assert ch.get_value('skills.lore_crab') == 1
