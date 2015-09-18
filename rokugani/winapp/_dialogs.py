class InputDialog(object):

    @classmethod
    def select_text(cls, parent, title, caption, options):
        from PyQt5 import QtWidgets
        return QtWidgets.QInputDialog.getItem(
            parent,
            title,
            caption,
            sorted(options),
        )


    @classmethod
    def select_item(cls, parent, title, caption, options):
        from PyQt5 import QtWidgets
        result = QtWidgets.QInputDialog.getItem(
            parent,
            title,
            caption,
            sorted(options),
        )
        return result

