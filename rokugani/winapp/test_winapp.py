from rokugani.winapp.winapp import RokuganiApplication2
from PyQt5 import QtCore



def test_winapp(qtbot, mock):
    app = RokuganiApplication2([])
    qtbot.addWidget(app._view.main_window)

    # click in the Greet button and make sure it updates the appropriate label
    assert app._view.label_clan.text() == 'clan:?'
    with mock.patch('rokugani.winapp._dialogs.InputDialog.select_item', return_value=('crab', True)):
        qtbot.mouseDClick(app._view.label_clan, QtCore.Qt.LeftButton)

    assert app._view.label_school.text() == 'school:?'
    assert app._view.label_family.text() == 'family:?'

    with mock.patch('rokugani.winapp._dialogs.InputDialog.select_item', return_value=('crab_hida', True)):
        qtbot.mouseDClick(app._view.label_family, QtCore.Qt.LeftButton)

    assert app._view.label_skill_school_1.text() == ''
    assert app._view.label_skill_name_1.text() == ''
    assert app._view.label_skill_rank_1.text() == ''

    with mock.patch('rokugani.winapp._dialogs.InputDialog.select_item', return_value=('crab_hida_bushi_school', True)):
        qtbot.mouseDClick(app._view.label_school, QtCore.Qt.LeftButton)

    assert app._view.label_skill_school_1.text() == 'X'
    assert app._view.label_skill_name_1.text() == 'Athletics'
    assert app._view.label_skill_rank_1.text() == '1'

