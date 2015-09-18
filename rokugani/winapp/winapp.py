from rokugani.winapp._base_app import BaseApplication
from rokugani.winapp.controller import Controller, CharacterInfoController, \
    AdvancementController, TraitController, SkillController, handle_exception



class RokuganiApplication2(BaseApplication):

    def _create_view(self):
        from PyQt5.QtWidgets import QMainWindow
        from rokugani.winapp.character_sheet_ui import Ui_MainWindow

        class MainWindow(Ui_MainWindow):

            def __init__(self):
                self.main_window = QMainWindow()
                self.setupUi(self.main_window)

        return MainWindow()


    def _configure_controllers(self):

        def register_controller(model_attr, widget_name=None, controller=Controller):
            if widget_name is None:
                widget_name = model_attr.replace('.', '_')
            widget_name = 'label_{}'.format(widget_name)
            view = getattr(self._view, widget_name)
            controller = controller(view, self._builder, model_attr)
            self._controllers[model_attr] = controller

        def register_skill_controller(widget_name, skill_index, skill_name):
            view = getattr(self._view, widget_name, None)
            if view is not None:
                controller = SkillController(view, self._builder, skill_index, skill_name)
                self._controllers[model_attr + '#' + skill_name] = controller

        register_controller('character.name', controller=CharacterInfoController)
        register_controller('clan', controller=AdvancementController)
        register_controller('family', controller=AdvancementController)
        register_controller('school', controller=AdvancementController)

        register_controller('rings.earth')
        register_controller('rings.air')
        register_controller('rings.water')
        register_controller('rings.fire')
        register_controller('rings.void', controller=TraitController)

        register_controller('traits.stamina', controller=TraitController)
        register_controller('traits.willpower', controller=TraitController)
        register_controller('traits.reflexes', controller=TraitController)
        register_controller('traits.awareness', controller=TraitController)
        register_controller('traits.strength', controller=TraitController)
        register_controller('traits.perception', controller=TraitController)
        register_controller('traits.agility', controller=TraitController)
        register_controller('traits.intelligence', controller=TraitController)

        register_controller('ranks.rank')
        register_controller('ranks.honor')
        register_controller('ranks.glory')
        register_controller('ranks.status')
        register_controller('ranks.taint')
        register_controller('xp')
        register_controller('ranks.insight')

        register_controller('wounds.healthy.penalty')
        register_controller('wounds.healthy')
        register_controller('wounds.nicked.penalty')
        register_controller('wounds.nicked')
        register_controller('wounds.grazed.penalty')
        register_controller('wounds.grazed')
        register_controller('wounds.hurt.penalty')
        register_controller('wounds.hurt')
        register_controller('wounds.injured.penalty')
        register_controller('wounds.injured')
        register_controller('wounds.crippled.penalty')
        register_controller('wounds.crippled')
        register_controller('wounds.down.penalty')
        register_controller('wounds.down')
        register_controller('wounds.out')

        register_controller('initiative.base')
        register_controller('initiative.modifiers')
        register_controller('initiative.current')

        register_controller('armor_tn.base')
        register_controller('armor_tn.reduction')
        register_controller('armor_tn.current')

        register_controller('armor.tn_bonus')
        register_controller('armor.quality')
        register_controller('armor.notes')

        for i in range(23):
            model_attr = 'skills.{}'.format(i)
            index = i + 1
            register_skill_controller('label_skill_school_{}'.format(index), i, 'school')
            register_skill_controller('label_skill_name_{}'.format(index), i, 'name')
            register_skill_controller('label_skill_rank_{}'.format(index), i, 'rank')
            register_skill_controller('label_skill_trait_{}'.format(index), i, 'trait_short')
            register_skill_controller('label_skill_roll_{}'.format(index), i, 'roll')
            register_skill_controller('label_skill_obs_{}'.format(index), i, 'obs')


        self._view.button_advancements.clicked.connect(self._on_advancements)
        self._view.button_page_1_page_2.clicked.connect(self._goto_page_2)
        self._view.button_page_2_page_1.clicked.connect(self._goto_page_1)


    @handle_exception
    def _goto_page_2(self, *args):
        self._view.pages.setCurrentIndex(1)


    @handle_exception
    def _goto_page_1(self, *args):
        self._view.pages.setCurrentIndex(0)


    @handle_exception
    def _on_advancements(self, *args):
        self._builder.set_advancement_value('clan', 'crab')
        self._builder.set_advancement_value('family', 'crab_hida')
        self._builder.set_advancement_value('school', 'crab_hida_bushi_school')



if __name__ == '__main__':
    import sys
    app = RokuganiApplication2(sys.argv)
    sys.exit(app.main())

