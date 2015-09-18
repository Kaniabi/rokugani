from rokugani.winapp._base_app import BaseApplication



class RokuganiApplication(BaseApplication):


    def _create_view(self):
        from rokugani.winapp.main_window import MainWindow
        return MainWindow()


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
        self._update_view_editor(self._view.edStamina, 'traits.stamina')
        self._update_view_editor(self._view.edWillpower, 'traits.willpower')

        self._update_view_editor(self._view.edAir, 'rings.air')
        self._update_view_editor(self._view.edReflexes, 'traits.reflexes')
        self._update_view_editor(self._view.edAwareness, 'traits.awareness')

        self._update_view_editor(self._view.edWater, 'rings.water')
        self._update_view_editor(self._view.edStrength, 'traits.strength')
        self._update_view_editor(self._view.edPerception, 'traits.perception')

        self._update_view_editor(self._view.edFire, 'rings.fire')
        self._update_view_editor(self._view.edAgility, 'traits.agility')
        self._update_view_editor(self._view.edIntelligence, 'traits.intelligence')

        self._update_view_editor(self._view.edVoid, 'rings.void')

        self._update_view_editor(self._view.edHonor, 'ranks.honor')
        self._update_view_editor(self._view.edGlory, 'ranks.glory')
        self._update_view_editor(self._view.edStatus, 'ranks.status')
        self._update_view_editor(self._view.edTaint, 'ranks.taint')
        self._update_view_editor(self._view.edInfamy, 'ranks.infamy')

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
                    Out: <B><BIG>{wounds.out}</BIG></B></P>
                '''
            )
        )



if __name__ == '__main__':
    import sys
    app = RokuganiApplication()
    sys.exit(app.main(sys.argv))
