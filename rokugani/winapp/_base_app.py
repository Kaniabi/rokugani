# Configure environment variables here so we can execute this script from inside PyCharm.
import os
os.environ['QTDIR'] = r'd:\shared\python3\lib\site-packages\PyQt5'
os.environ['QT_PLUGIN_PATH'] = r'd:\shared\python3\lib\site-packages\PyQt5\plugins'
os.environ['QML2_IMPORT_PATH'] = r'd:\shared\python3\lib\site-packages\PyQt5\qml'



class Constants(object):
    app_name = 'Rokugani'
    app_version = '0.1'
    app_org = 'Kaniabi'



class BaseApplication(object):

    def __init__(self, argv):
        from PyQt5 import QtWidgets, QtCore
        from rokugani.model.character_model import CharacterModel
        from rokugani.model.character_builder import CharacterBuilder

        self._app = QtWidgets.QApplication(argv)
        QtCore.QCoreApplication.setApplicationName(Constants.app_name)
        QtCore.QCoreApplication.setApplicationVersion(Constants.app_version)
        QtCore.QCoreApplication.setOrganizationName(Constants.app_org)

        self._view = self._create_view()
        self._view.main_window.show()

        self._character_model = CharacterModel()
        self._builder = CharacterBuilder(self._character_model)

        self._controllers = {}
        self._configure_controllers()

        self._update_view()
        self._update_controllers()

        # Connect callbacks.
        self._character_model.on_model_change.Register(self._model_changed)


    def main(self):
        return self._app.exec_()


    def _model_changed(self, model_attr):
        self._update_view()
        self._update_controllers()


    def _create_view(self):
        pass


    def _update_controllers(self):
        for i_controller in self._controllers.values():
            i_controller.update_view()


    def _configure_controllers(self):
        pass


    def _update_view(self):
        pass


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

