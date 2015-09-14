from rokugani.model.data_access import DataAccess



def test_data_access():
    d = DataAccess('x:/l5rcm-data-packs/packs')
    assert len(d.clans) == 37
    assert len(d.schools) == 246
    assert len(d.skills) == 118
