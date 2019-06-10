from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_Weather
import sys

class MainWindow(QtWidgets.QApplication, Ui_Weather):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__([])
		self.get_info()
		self.MainWindow = QtWidgets.QMainWindow()
		self.setupUi(self.MainWindow)
		self.MainWindow.show()

	def get_info(self):
		pass

sys.exit(MainWindow().exec())
