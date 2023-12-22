# pyqtexcept
`pyqtexcept` is a Python package that provides a convenient exception handling mechanism for PyQt5 applications.

It includes a function to create a custom exception hook for displaying critical errors using `QMessageBox`.

## Installation
You can install `pyqtexcept` using pip:
```bash
pip install pyqtexcept
```

## Usage
```python
import sys
from PyQt5 import QtWidgets
from pyqtexcept import create_exceptions_hook

# Create a PyQt application window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

# Set up the custom exception hook
sys.excepthook = create_exceptions_hook(window)

# Your PyQt application code goes here

# Start the application
window.show()
sys.exit(app.exec_())
```
The `create_exceptions_hook` function sets up a custom exception hook using `sys.excepthook` to display critical errors in a `QMessageBox`.

## License
This package is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.

