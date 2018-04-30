import sys
from PyQt5.QtWidgets import QApplication
from gui import SieraWindow

app = QApplication(sys.argv)

gui = SieraWindow()

sys.exit(app.exec_())
