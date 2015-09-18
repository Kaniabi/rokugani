from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtCore import pyqtSignal


def handle_exception(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
    wrapper.__name__ = f.__name__

    return wrapper


class Controller(QObject):

    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, view, builder, model_attr):
        super(Controller, self).__init__()
        self._view = view
        self._view.installEventFilter(self)
        self._builder = builder
        self._model_attr = model_attr
        self._configure()

    def _configure(self):
        pass

    def update_view(self):
        self._view.setText(self._get_value())

        explanation = ''
        for i_source, i_value in self._builder.explain_value(self._model_attr):
            explanation += '{0}&nbsp;{1}<br/>'.format(i_source, i_value)
        if explanation:
            self._view.setToolTip(explanation)

    def _get_value(self):
        value = self._builder.get_value(self._model_attr)
        return str(value)

    def eventFilter(self, obj, event):

        if obj == self._view:
            if event.type() == QEvent.MouseButtonRelease:
                if obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
            elif event.type() == QEvent.MouseButtonDblClick:
                if obj.rect().contains(event.pos()):
                    self.doubleClicked.emit()
                    return True

        return False

    def _select_advancement(self, advancement):
        from rokugani.winapp._dialogs import InputDialog
        value, ok = InputDialog.select_item(
            self._view,
            str(advancement.__class__.__name__),
            advancement.NAME,
            advancement.options,
        )
        if ok:
            advancement.set_value(value)


    def _buy_advancement(self, advancement_class, **kwargs):
        advancement = advancement_class(self._builder, buy=True, **kwargs)
        self._select_advancement(advancement)



class CharacterInfoController(Controller):

    def _configure(self):
        self.doubleClicked.connect(self._edit_value)

    @handle_exception
    def _edit_value(self, *args):
        from rokugani.winapp._dialogs import InputDialog
        current = self._builder.get_value(self._model_attr)
        value, ok = InputDialog.select_text(
            self._view,
            'SELECT',
            self._model_attr,
            text=current
        )
        if ok:
            self._builder.set_value(self._model_attr, value)


class AdvancementController(Controller):

    def _configure(self):
        self.doubleClicked.connect(self._edit_value)

    def _get_value(self):
        advancement = self._builder.find_advancement(self._model_attr)
        if advancement and advancement.value == '?':
            return str(advancement)
        return self._builder.get_value(self._model_attr)

    @handle_exception
    def _edit_value(self, *args):
        advancement = self._builder.find_advancement(self._model_attr)
        self._select_advancement(advancement)


class TraitController(Controller):

    def _configure(self):
        self.doubleClicked.connect(self._edit_value)

    @handle_exception
    def _edit_value(self, *args):
        self._builder.add_trait(
            self._model_attr,
            'buy by double-click',
            buy=True
        )


class SkillController(Controller):

    def __init__(self, view, builder, skill_index, skill_attr):
        self._skill_index = skill_index
        self._skill_attr = skill_attr
        super(SkillController, self).__init__(view, builder, 'skills.[{}]'.format(skill_index))

    def _configure(self):
        self.doubleClicked.connect(self._edit_value)

    def _get_value(self):
        skills = self._builder.get_skills()
        try:
            skill_dict = skills[self._skill_index]
        except IndexError:
            return ''
        else:
            return str(skill_dict[self._skill_attr])

    @handle_exception
    def _edit_value(self, *args):
        skills = self._builder.get_skills()
        if self._skill_index >= len(skills):
            from rokugani.model.advancements import AdvancementSkill
            self._buy_advancement(AdvancementSkill, new_skills=True)
            return

        skill_dict = skills[self._skill_index]
        advancement = skill_dict.get('advancement')
        if advancement is not None:
            self._select_advancement(advancement)
            return

        if self._skill_attr == 'rank':
            self._builder.add_skill(skill_dict['id'], 1, buy=True)
            return


class ListWidgetController(object):

    def __init__(self, list_widget, builder, prefix):
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

        self._list_widget = list_widget
        if not isinstance(self._list_widget.itemDelegate(), MyItemDelegate):
            self._list_widget.setItemDelegate(MyItemDelegate(self._list_widget))
        self._builder = builder
        self._prefix = prefix


    def update_view(self):
        items = self._builder.list_model_attrs(self._prefix)
        self._list_widget.clear()
        for i_name, i_model_attr in items:
            self._list_widget.addItem(
                '{1} <B><BIG>{0}</BIG></B>'.format(self._builder.get_value(i_name), i_name)
            )


class AdvancementsController(object):

    def __init__(self, list_widget, builder):
        self._builder = builder
        self._list_widget = list_widget
        self._list_widget.doubleClicked.connect(self.on_double_click)


    @handle_exception
    def on_double_click(self, index):
        try:
            advancement = self._builder.advancements[index.row()]
            self._select_advancement(advancement)
        except Exception as e:
            print('EXCEPTION:{}'.format(str(e)))
            raise


    def update_view(self):
        self._list_widget.clear()
        for i in self._builder.advancements:
            self._list_widget.addItem(str(i))


    @handle_exception
    def buy_skill(self, *args):
        from rokugani.model.advancements import AdvancementSkill
        self._buy_advancement(AdvancementSkill)


    @handle_exception
    def buy_merit(self, *args):
        from rokugani.model.advancements import AdvancementMerit
        self._buy_advancement(AdvancementMerit)


    @handle_exception
    def buy_flaw(self, *args):
        from rokugani.model.advancements import AdvancementFlaw
        self._buy_advancement(AdvancementFlaw)


    @handle_exception
    def buy_trait(self, *args):
        from rokugani.model.advancements import AdvancementTrait
        self._buy_advancement(AdvancementTrait)



class DebugController(object):

    def __init__(self, list_widget, builder):
        self._builder = builder
        self._list_widget = list_widget

    def update_view(self):
        self._list_widget.clear()
        for i_name, i_attr_model in self._builder.list_model_attrs(''):
            self._list_widget.addItem('{}: {}'.format(i_name, i_attr_model.value))
