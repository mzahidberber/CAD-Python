import sys
from PyQt5.QtWidgets import *
from UI.View import View

app=QApplication(sys.argv)
pencere=View()
pencere.show()
sys.exit(app.exec_())