import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class CheckListWidget(QtWidgets.QWidget):
    """
    PyQt5 widget - a list widget with checkboxes.
    """
    def __init__(
        self,
        parent=None, 
        data=None,
        checked: bool = False,
        editable: bool = False):
        """
        Initializes a new widget.

        Arguments:
            parent - parent widget or window
            data (dict) - a list with initial data for widget
            checked (bool) - indicates wether the initial data needs to be checked or not
            editable (bool) - gives user the permission to edit data in the widget
        """
        super().__init__(parent)
        if data is None:
            data = []
        self.setup()
        self.data = {}
        if not editable:
            self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.addNewElements(data)

    def setup(self):
        """Setup for widget layout."""
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()
        self.listView.setModel(self.model)
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.listView)
        vbox.addLayout(hbox)

    def get_selected_indexes(self) -> list:
        """Get list of selected elements's indexes."""
        self.refresh_data()
        items = list(self.data.items())
        return [i for i in range(len(items)) if items[i][1]]

    def get_selected(self) -> list:
        """Get list of selected values."""
        self.refresh_data()
        return [key for key in self.data if self.data[key]]

    def select(self):
        """Select all items in the list & refresh it."""
        for i in self.data:
            self.data[i] = True
        self.refresh()

    def unselect(self):
        """Unselect all items in the list & refresh it."""
        for i in self.data:
            self.data[i] = False
        self.refresh()

    def printData(self):
        self.refresh_data()
        print(self.data)

    def addNewElements(self, data: list, checked: bool = False) -> None:
        """
        Add new elements into the widget.

        Args:
            data - A list with data to be added.
            checked - Indicated wether new elements need to be
                checked or not.
        """
        for i in data:
            self.addNewElement(i, checked=checked)

    def addNewElement(self, value: str, checked: bool = False) -> None:
        """
        Add a new element into the widget.

        Args:
            value - A value of the element
            checked - Indicated wether the element needs to be
                checked or not.
        """
        if value not in self.data:
            item = QtGui.QStandardItem(value)
            item.setCheckable(True)
            item.setCheckState((QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked))
            self.model.appendRow(item)
            self.data[value] = checked
        self.refresh()

    def refresh(self) -> None:
        """Refreshes data in the widget."""
        self.model.clear()
        for key in self.data:
            item = QtGui.QStandardItem(key)
            item.setCheckable(True)
            item.setCheckState((QtCore.Qt.Checked if self.data[key] else QtCore.Qt.Unchecked))
            self.model.appendRow(item)

    def refresh_data(self) -> None:
        """Refresh self.data with values from widget."""
        self.data = {
            self.model.item(i).text(): (True if self.model.item(i).checkState() == QtCore.Qt.Checked else False)
            for i in range(self.model.rowCount())}

    def deleteSelected(self, function=None) -> None:
        """
        Delete selected elements from the list.
        
        Args:
            function - function will be called before the deletion of every element.
                This element is passed into the function.
        """
        indexes = self.get_selected_indexes()
        while indexes:
            i = indexes.pop(0)
            if function: function(self.model.item(i))
            self.model.removeRow(i)
            indexes = list(map(lambda x: x - 1 if (x > i) else x, indexes))
        self.refresh_data()


def main():
    app = QtWidgets.QApplication(sys.argv)
    data = list(dir(QtWidgets))
    window = CheckListWidget(data=data)
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
