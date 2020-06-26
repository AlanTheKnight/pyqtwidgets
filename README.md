# PyQtWidgets

A small library of my custom PyQt5 widgets

## Available widgets

### CheckListWidget

![](images/chechlistwidget.png?raw=true)

```python
import sys
from PyQt5 import QtWidgets
from widgets import CheckListWidget

app = QtWidgets.QApplication(sys.argv)
data = list(dir(QtWidgets))
window = CheckListWidget(data=data)
window.resize(400, 400)
window.show()
sys.exit(app.exec_())
```
