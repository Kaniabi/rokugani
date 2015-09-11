from rokugani.model.character_model import CharacterModel


def test_rings():
    ch = CharacterModel()
    assert ch.get_value('rings.earth') == 2

    ch.set_value('attribs.stamina', 3)
    assert ch.get_value('rings.earth') == 2

    ch.set_value('attribs.willpower', 3)
    assert ch.get_value('rings.earth') == 3


def test_wounds():
    ch = CharacterModel()
    assert ch.get_value('wounds.healty') == 10
    assert ch.get_value('wounds.injured') == 26

    ch.set_value('attribs.stamina', 3)
    ch.set_value('attribs.willpower', 3)
    assert ch.get_value('wounds.healty') == 15
    assert ch.get_value('wounds.injured') == 39


def test_wounds_penalty():
    ch = CharacterModel()
    assert ch.get_value('wounds.healty.penalty') == 0
    assert ch.get_value('wounds.nicked.penalty') == 3
    assert ch.get_value('wounds.grazed.penalty') == 5
    assert ch.get_value('wounds.hurt.penalty') == 10
    assert ch.get_value('wounds.crippled.penalty') == 20
    assert ch.get_value('wounds.down.penalty') == 40


def test_modifiers():
    ch = CharacterModel()
    assert ch.get_value('attribs.stamina') == 2
    assert ch.get_value('attribs.willpower') == 2
    assert ch.get_value('rings.earth') == 2

    ch.add_modifier('attribs.stamina', 1, 'test_modifier')
    assert ch.get_value('attribs.stamina') == 3
    assert ch.get_value('attribs.willpower') == 2
    assert ch.get_value('rings.earth') == 2

    ch.add_modifier('attribs.willpower', 1, 'test_modifier')
    assert ch.get_value('attribs.stamina') == 3
    assert ch.get_value('attribs.willpower') == 3
    assert ch.get_value('rings.earth') == 3
