import pytest
from rokugani.model.character import CharacterModel
from rokugani.model.character_builder import CharacterBuilder, NoAdvancementError



def test_character_builder():

    ch = CharacterModel()

    builder = CharacterBuilder(ch)

    # Raises an error if trying to set a value that is not available on advancements.
    with pytest.raises(NoAdvancementError):
        builder.set('rubles', 'crab')

    # We begin with one advancement only: the clan
    assert builder.advancements == ['clan']

    # These operations set a value defined by an advancement
    # They raise an error if no advancement is there to set.
    assert ch.get_value('clan') is None
    builder.set('clan', 'crab')
    assert ch.get_value('clan') == 'crab'

    # Setting the clan will add the family advancement.
    assert builder.advancements == ['clan', 'family']
    assert ch.get_value('attribs.strength') == 2
    builder.set('family', 'crab_hida')
    assert ch.get_value('attribs.strength') == 3

    # Setting the family will add the school advancement
    assert builder.advancements == ['clan', 'family', 'school']
    assert ch.get_value('attribs.stamina') == 2
    builder.set('school', 'crab_hida_bushi_school')

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

    #ch.add_advancement(CharacterAdvancement('xp', id='xp', value=30))

    #ch.add_advancement(CharacterAdvancement('clan', id='crab'))

    #ch.add_advancement(CharacterAdvancement('family', id='crab_hida'))
    # ==> CharacterAdvancement('attrib', id='strength', value=1)

    #ch.add_advancement(CharacterAdvancement('school', id='hida_bushi'))
    # ==> CharacterAdvancement('attribs', id='stamina', value=1)
    # ==> CharacterAdvancement('skills', id='athletics', school_skill=True, value=1)
    # ==> CharacterAdvancement('skills', id='defense', school_skill=True, value=1)
    # ==> CharacterAdvancement('skills', id='heavy_weapons', school_skill=True, emphasis='tetsubo' value=1)
    # ==> CharacterAdvancement('skills', id='intimidation', school_skill=True, value=1)
    # ==> CharacterAdvancement('skills', id='kenjutsu', school_skill=True, value=1)
    # ==> CharacterAdvancement('skills', id='lore', school_skill=True, variation='shadowlands', value=1)
    # ==> CharacterAdvancement('skills', id='?', school_skill=True, wildcards='buguei', value=1)
    # ==> CharacterAdvancement('ranks', id='honor', value=3.5)

    # Select one or the other
    # ==> CharacterAdvancement('outfit', id='?armor', id='light_armor')
    # ==> CharacterAdvancement('outfit', id='?armor', id='heavy_armor')

    # ==> CharacterAdvancement('weapon', id='?weapon', id='heavy_weapon')
    # ==> CharacterAdvancement('weapon', id='?weapon', id='polearm')

    # ==> CharacterAdvancement('item', id='traveling_pack')
    # ==> CharacterAdvancement('money', id='koku', value=3)

