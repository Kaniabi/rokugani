


def handle_exception(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
    wrapper.__name__ = f.__name__

    return wrapper


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


    def on_double_click(self, index):
        try:
            advancement = self._builder.advancements[index.row()]
            value, ok = self._select_advancement(advancement)
            if ok:
                advancement.set_value(value)
        except Exception as e:
            print('EXCEPTION:{}'.format(str(e)))
            raise


    def update_view(self):
        self._list_widget.clear()
        for i in self._builder.advancements:
            self._list_widget.addItem(str(i))


    def buy_skill(self):
        from rokugani.model.advancements import AdvancementSkill
        self._buy_advancement(AdvancementSkill)


    def buy_merit(self):
        from rokugani.model.advancements import AdvancementMerit
        self._buy_advancement(AdvancementMerit)


    def buy_flaw(self):
        from rokugani.model.advancements import AdvancementFlaw
        self._buy_advancement(AdvancementFlaw)


    def buy_trait(self):
        from rokugani.model.advancements import AdvancementTrait
        self._buy_advancement(AdvancementTrait)


    @handle_exception
    def _buy_advancement(self, advancement_class):
        advancement = advancement_class(self._builder, buy=True)
        value, ok = self._select_advancement(advancement)
        if ok:
            self._builder.advancements.append(advancement)
            advancement.set_value(value)


    def _select_advancement(self, advancement):
        from PyQt5 import QtWidgets
        return QtWidgets.QInputDialog.getItem(
            self._list_widget,
            'SELECT',
            advancement.NAME,
            sorted(advancement.options),
        )




class DebugController(object):

    def __init__(self, list_widget, builder):
        self._builder = builder
        self._list_widget = list_widget

    def update_view(self):
        self._list_widget.clear()
        for i_name, i_attr_model in self._builder.list_model_attrs(''):
            self._list_widget.addItem('{}: {}'.format(i_name, i_attr_model.value))
