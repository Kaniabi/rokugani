# Configure environment variables here so we can execute this script from inside PyCharm.
import os
os.environ['QTDIR'] = r'd:\shared\python3\lib\site-packages\PyQt5'
os.environ['QT_PLUGIN_PATH'] = r'd:\shared\python3\lib\site-packages\PyQt5\plugins'
os.environ['QML2_IMPORT_PATH'] = r'd:\shared\python3\lib\site-packages\PyQt5\qml'



class Constants(object):
    app_name = 'Rokugani'
    app_version = '0.1'
    app_org = 'Kaniabi'


class RokuganiApplication(object):

    def __init__(self):
        self._app = None


    def main(self, argv):
        from rokugani.winapp.main_window import MainWindow
        from rokugani.model.character import CharacterModel
        from PyQt5 import QtWidgets, QtCore

        self._app = QtWidgets.QApplication(argv)
        QtCore.QCoreApplication.setApplicationName(Constants.app_name)
        QtCore.QCoreApplication.setApplicationVersion(Constants.app_version)
        QtCore.QCoreApplication.setOrganizationName(Constants.app_org)

        self._view = MainWindow()
        self._view.show()

        self._character_model = CharacterModel()
        self._configure_model()

        self._connect_model(self._view.edClan, 'clan')
        self._connect_model(self._view.edFamily, 'family')
        self._connect_model(self._view.edSchool, 'school')

        self._connect_model(self._view.edEarth, 'rings.earth')
        self._connect_model(self._view.edStamina, 'attribs.stamina')
        self._connect_model(self._view.edWillpower, 'attribs.willpower')

        self._connect_model(self._view.edAir, 'rings.air')
        self._connect_model(self._view.edReflexes, 'attribs.reflexes')
        self._connect_model(self._view.edAwareness, 'attribs.awareness')

        self._connect_model(self._view.edWater, 'rings.water')
        self._connect_model(self._view.edStrength, 'attribs.strength')
        self._connect_model(self._view.edPerception, 'attribs.perception')

        self._connect_model(self._view.edFire, 'rings.fire')
        self._connect_model(self._view.edAgility, 'attribs.agility')
        self._connect_model(self._view.edIntelligence, 'attribs.intelligence')

        self._connect_model(self._view.edVoid, 'rings.void')

        self._connect_model(self._view.edHonor, 'ranks.honor')
        self._connect_model(self._view.edGlory, 'ranks.glory')
        self._connect_model(self._view.edStatus, 'ranks.status')
        self._connect_model(self._view.edTaint, 'ranks.taint')
        self._connect_model(self._view.edInfamy, 'ranks.infamy')

        self._connect_list_view(self._view.lvSkills, 'skills')
        self._connect_list_view(self._view.lvPerks, 'perks')
        self._connect_list_view(self._view.lvSpells, 'spells')
        self._connect_list_view(self._view.lvDebug, '')

        return self._app.exec_()


    def _configure_model(self):
        '''
        Configures the character-model with a sample character for testing.
        '''
        from rokugani.model.character_builder import CharacterBuilder

        builder = CharacterBuilder(self._character_model)
        builder.set('clan', 'crab')
        builder.set('family', 'crab_hida')
        builder.set('school', 'crab_hida_bushi_school')

        builder.buy('attrib', 'willpower', 1)
        builder.buy('attrib', 'agility', 1)

        builder.buy('perk', 'large', 1)
        builder.buy('perk', 'strength_of_the_earth', 1)
        builder.buy('perk', 'quick_healer', 1)
        builder.buy('skill', 'heavy_weapons', 2)


    def _connect_model(self, view, model_attr):
        '''
        Connects a view (widget) with a model-attribute from the character-model.
        '''
        value = self._character_model.get_value(model_attr)
        value = str(value)
        view.setText(value)

        explanation = ''
        for i_source, i_value in self._character_model.explain_value(model_attr):
            explanation += '{0}&nbsp;+{1}<br/>'.format(i_source, i_value)
        if explanation:
            view.setToolTip(explanation)


    def _connect_list_view(self, view, model_attr_prefix):
        from PyQt5 import QtWidgets, QtGui
        from PyQt5.QtCore import Qt, QSize

        class MyItemDelegate(QtWidgets.QItemDelegate):

            def _drawHtml(self, painter, rect, text):
                painter.translate(rect.topLeft());
                painter.setClipRect(rect.translated(-rect.topLeft()))

                doc = QtGui.QTextDocument(self)
                doc.setHtml(text)
                doc.setTextWidth(rect.width())
                paint_context = QtGui.QAbstractTextDocumentLayout.PaintContext()
                doc.documentLayout().draw(painter, paint_context)

            def sizeHint(self, *args):
                return QSize(24, 24)

            def paint(self, painter, option, index):
                if not index.isValid():
                    super(MyItemDelegate, self).paint(painter, option, index)
                    return

                painter.save()
                try:
                    if option.state & QtWidgets.QStyle.State_Selected == QtWidgets.QStyle.State_Selected:
                        painter.fillRect(option.rect, option.palette.highlight())
                        #painter.setPen(option.palette.highlightedText())
                    else:
                        painter.fillRect(option.rect, option.palette.base().color())
                    text = index.data(Qt.DisplayRole)
                    self._drawHtml(painter, option.rect, text)
                except Exception as e:
                    print(str(e))
                painter.restore()

        delegate = MyItemDelegate(view.parent())
        view.setItemDelegate(delegate)
        for i_name, i_model_attr in self._character_model.list_model_attrs(model_attr_prefix):
            view.addItem('{1} <B><BIG>{0}</BIG></B>'.format(self._character_model.get_value(i_name), i_name))



if __name__ == '__main__':
    import sys
    app = RokuganiApplication()
    sys.exit(app.main(sys.argv))
