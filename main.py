from PySide2 import QtCore, QtWidgets, QtGui
import PySide2
import sys
import os
from PySide2.QtGui import QPixmap
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
dir_name = os.path.dirname(os.path.abspath(__file__))

from widgets.main_widget import MyWidget


def main():
    app = QtWidgets.QApplication([])
    my_widget = MyWidget()
    my_widget.setWindowTitle("np2img")

    my_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()