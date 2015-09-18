from rokugani.model.character_model import CharacterModel



def test_rings():
    ch = CharacterModel()
    assert ch.get_value('rings.earth') == 2

    ch.set_value('traits.stamina', 3)
    assert ch.get_value('rings.earth') == 2

    ch.set_value('traits.willpower', 3)
    assert ch.get_value('rings.earth') == 3


def test_wounds():
    ch = CharacterModel()
    assert ch.get_value('wounds.healthy') == 10
    assert ch.get_value('wounds.injured') == 26

    ch.set_value('traits.stamina', 3)
    ch.set_value('traits.willpower', 3)
    assert ch.get_value('wounds.healthy') == 15
    assert ch.get_value('wounds.injured') == 39


def test_wounds_penalty():
    ch = CharacterModel()
    assert ch.get_value('wounds.healthy.penalty') == 0
    assert ch.get_value('wounds.nicked.penalty') == 3
    assert ch.get_value('wounds.grazed.penalty') == 5
    assert ch.get_value('wounds.hurt.penalty') == 10
    assert ch.get_value('wounds.crippled.penalty') == 20
    assert ch.get_value('wounds.down.penalty') == 40


def test_modifiers():
    ch = CharacterModel()
    assert ch.get_value('traits.stamina') == 2
    assert ch.get_value('traits.willpower') == 2
    assert ch.get_value('rings.earth') == 2

    ch.add_modifier('traits.stamina', 1, 'test_modifier')
    assert ch.get_value('traits.stamina') == 3
    assert ch.get_value('traits.willpower') == 2
    assert ch.get_value('rings.earth') == 2

    ch.add_modifier('traits.willpower', 1, 'test_modifier')
    assert ch.get_value('traits.stamina') == 3
    assert ch.get_value('traits.willpower') == 3
    assert ch.get_value('rings.earth') == 3


def test_initiative():
    ch = CharacterModel()
    assert ch.get_value('initiative.base') == '3k2'
    assert ch.get_value('initiative.modifiers') == '0k0'
    assert ch.get_value('initiative.current') == '3k2'


def test_armor_tn():
    ch = CharacterModel()
    ch.add_modifier('traits.reflexes', 1, source='test_armor_tn')
    assert ch.get_value('armor_tn.base') == 20
    assert ch.get_value('armor_tn.reduction') == 20
    assert ch.get_value('armor_tn.current') == 20

