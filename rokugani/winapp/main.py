# Configure environment variables here so we can execute this script from inside PyCharm.
from PyQt5.QtCore import pyqtSlot
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
        from rokugani.model.character_model import CharacterModel
        from rokugani.model.character_builder import CharacterBuilder
        from PyQt5 import QtWidgets, QtCore

        self._app = QtWidgets.QApplication(argv)
        QtCore.QCoreApplication.setApplicationName(Constants.app_name)
        QtCore.QCoreApplication.setApplicationVersion(Constants.app_version)
        QtCore.QCoreApplication.setOrganizationName(Constants.app_org)

        self._view = MainWindow()
        self._view.show()

        self._character_model = CharacterModel()
        self._builder = CharacterBuilder(self._character_model)

        self._controllers = {}
        self._configure_controllers()

        self._update_view()

        # Connect callbacks.
        self._character_model.on_model_change.Register(self._model_changed)

        return self._app.exec_()


    def _model_changed(self, model_attr):
        # Now, we update the entire interface, ignoring the model_attr.
        self._update_view()


    def _configure_controllers(self):
        from rokugani.winapp.controller import ListWidgetController, AdvancementsController, DebugController

        self._controllers['skills'] = ListWidgetController(self._view.listwidget_skills, self._builder, 'skills')
        self._controllers['spells'] = ListWidgetController(self._view.listwidget_spells, self._builder, 'spells')
        self._controllers['merits'] = ListWidgetController(self._view.listwidget_merits, self._builder, 'merits')
        self._controllers['flaws'] = ListWidgetController(self._view.listwidget_flaws, self._builder, 'flaws')
        self._controllers['advancements'] = AdvancementsController(self._view.lvBuild, self._builder)
        self._controllers['debug'] = DebugController(self._view.lvDebug, self._builder)

        self._view.button_buy_skill.clicked.connect(self._controllers['advancements'].buy_skill)
        self._view.button_buy_merit.clicked.connect(self._controllers['advancements'].buy_merit)
        self._view.button_buy_flaw.clicked.connect(self._controllers['advancements'].buy_flaw)
        self._view.button_buy_trait.clicked.connect(self._controllers['advancements'].buy_trait)


    def _update_view(self):
        self._update_view_editor(self._view.edClan, 'clan')
        self._update_view_editor(self._view.edFamily, 'family')
        self._update_view_editor(self._view.edSchool, 'school')

        self._update_view_editor(self._view.edXp, 'xp')
        self._update_view_editor(self._view.edInsight, 'ranks.insight')

        self._update_view_editor(self._view.edEarth, 'rings.earth')
        self._update_view_editor(self._view.edStamina, 'attribs.stamina')
        self._update_view_editor(self._view.edWillpower, 'attribs.willpower')

        self._update_view_editor(self._view.edAir, 'rings.air')
        self._update_view_editor(self._view.edReflexes, 'attribs.reflexes')
        self._update_view_editor(self._view.edAwareness, 'attribs.awareness')

        self._update_view_editor(self._view.edWater, 'rings.water')
        self._update_view_editor(self._view.edStrength, 'attribs.strength')
        self._update_view_editor(self._view.edPerception, 'attribs.perception')

        self._update_view_editor(self._view.edFire, 'rings.fire')
        self._update_view_editor(self._view.edAgility, 'attribs.agility')
        self._update_view_editor(self._view.edIntelligence, 'attribs.intelligence')

        self._update_view_editor(self._view.edVoid, 'rings.void')

        self._update_view_editor(self._view.edHonor, 'ranks.honor')
        self._update_view_editor(self._view.edGlory, 'ranks.glory')
        self._update_view_editor(self._view.edStatus, 'ranks.status')
        self._update_view_editor(self._view.edTaint, 'ranks.taint')
        self._update_view_editor(self._view.edInfamy, 'ranks.infamy')

        for i_controller in self._controllers.values():
            i_controller.update_view()

        self._view.browser_wounds.setText(
            self._builder.expand(
                '''
                    Healthy ({wounds.healthy.penalty}): <B><BIG>{wounds.healthy}</BIG></B><BR/>
                    Nicked ({wounds.nicked.penalty}): <B><BIG>{wounds.nicked}</BIG></B><BR/>
                    Grazed ({wounds.grazed.penalty}): <B><BIG>{wounds.grazed}</BIG></B><BR/>
                    Hurt ({wounds.hurt.penalty}): <B><BIG>{wounds.hurt}</BIG></B><BR/>
                    Injured ({wounds.injured.penalty}): <B><BIG>{wounds.injured}</BIG></B><BR/>
                    Crippled({wounds.crippled.penalty}): <B><BIG>{wounds.crippled}</BIG></B><BR/>
                    Down ({wounds.down.penalty}): <B><BIG>{wounds.down}</BIG></B><BR/>
                    Out: {wounds.out}</P>
                '''
            )
        )


    def _update_view_editor(self, view, model_attr):
        '''
        Connects a view (widget) with a model-attribute from the character-model.
        '''
        # Set the view value.
        value = self._character_model.get_value(model_attr)
        value = str(value)
        view.setText(value)

        # Set the view tool-tip with the "value-explanation".
        explanation = ''
        for i_source, i_value in self._character_model.explain_value(model_attr):
            explanation += '{0}&nbsp;{1}<br/>'.format(i_source, i_value)
        if explanation:
            view.setToolTip(explanation)



if __name__ == '__main__':
    import sys
    app = RokuganiApplication()
    sys.exit(app.main(sys.argv))
