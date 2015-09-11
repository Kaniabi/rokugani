from rokugani.model.l5rcm_data_access import L5rcmDataAccess



def test_data_access():
    d = L5rcmDataAccess('x:/l5rcm-data-packs/packs')
    assert len(d.clans) == 36
    assert len(d.schools) == 209
    assert len(d.skills) == 118
