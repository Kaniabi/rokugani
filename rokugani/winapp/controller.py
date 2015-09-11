from PyQt5.QtCore import pyqtSlot, QModelIndex



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
        from PyQt5 import QtWidgets

        try:
            advancement = self._builder.advancements[index.row()]

            value, ok = QtWidgets.QInputDialog.getItem(
                self._list_widget,
                'SELECT',
                advancement.NAME,
                sorted(advancement.options),
            )
            if ok:
                advancement.set_value(value)
        except Exception as e:
            print('EXCEPTION:{}'.format(str(e)))
            raise


    def update_view(self):
        self._list_widget.clear()
        for i in self._builder.advancements:
            self._list_widget.addItem(str(i))
