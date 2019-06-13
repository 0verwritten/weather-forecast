from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_Weather
from threading import Thread
from requests import get
import sys

global state, ip, loc, city, for_five_day, now
state=True

class MainWindow(QtWidgets.QApplication, Ui_Weather):
	def __init__(self, th, data):
		super(MainWindow, self).__init__([])
		self.MainWindow = QtWidgets.QMainWindow()
		self.setupUi(self.MainWindow)
		self.first_update_forecast(data)
		th.start()													# Start second thread
		self.aboutToQuit.connect(self.closeEvent)
		self.MainWindow.show()

	def update_cur_data(self,cur):
		self.cur_img.setPixmap(QtGui.QPixmap(F"imgs/{cur['icon']}.png"))
		self.cur_city.setText(cur['city'])
		self.cur_description.setText(cur['desc'])
		self.cur_temp.setText(str(cur['temp'])+"°")
	def update_forecast(self,forecast):
		pass
	def first_update_forecast(self, forecast):
		self.widgets = [] 											# Array of widgets with forecast
		for x in range(0,len(forecast)):
			widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
			widget.setMinimumSize(QtCore.QSize(70, 181))
			widget.setMaximumSize(QtCore.QSize(70, 181))
			widget.setStyleSheet("background-color:#F4f4f4; border-radius:8px;")
			widget.setObjectName("widget_"+str(x+1))
			date = QtWidgets.QLabel(widget)
			date.setGeometry(QtCore.QRect(0, 10, 70, 36))
			font = QtGui.QFont()
			font.setFamily("Lucida Grande")
			font.setPointSize(10)
			date.setFont(font)
			date.setAlignment(QtCore.Qt.AlignTop)
			date.setWordWrap(True)
			#date.setObjectName("date")
			img = QtWidgets.QLabel(widget)
			img.setGeometry(QtCore.QRect(10, 32, 50, 50))
			sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
			sizePolicy.setHorizontalStretch(0)
			sizePolicy.setVerticalStretch(0)
			sizePolicy.setHeightForWidth(img.sizePolicy().hasHeightForWidth())
			img.setSizePolicy(sizePolicy)
			img.setMaximumSize(QtCore.QSize(50, 50))
			img.setText("")
			img.setPixmap(QtGui.QPixmap(f"imgs/{forecast[x]['icon']}.png"))
			img.setIndent(0)
			#img.setObjectName("img")
			desc = QtWidgets.QLabel(widget)
			desc.setGeometry(QtCore.QRect(0, 78, 70, 101))
			font = QtGui.QFont()
			font.setFamily("Lucida Grande")
			font.setPointSize(11)
			desc.setFont(font)
			desc.setWordWrap(True)
			_translate = QtCore.QCoreApplication.translate
			date.setText(_translate("Weather", f"<html><head/><body><center><p>{forecast[x]['dt_txt']}</p></center></body></html>"))
			desc.setText(_translate("Weather", f"<html><head/><body><p align=\"center\">{forecast[x]['temp_min']}°/{forecast[x]['temp_max']}°</p><p align=\"center\"><span style=\" font-family:\'Lucida Grande\'; color:#000000;\">Humidity<br/>{forecast[x]['humidity']}% </span></p><p align=\"center\"><span style=\" font-family:\'Lucida Grande\'; color:#000000;\">Cloudiness<br>{forecast[x]['cloudiness']}%</span></p></body></html>"))
			#desc.setObjectName("desc")
			self.widgets.append(widget)
			self.horizontalLayout_2.addWidget(self.widgets[x])
	def closeEvent(self):
		global state
		state=False

def setup_vars():
	global ip, loc, city, for_five_day, now
	ip = get('https://api.ipify.org?format=json')			# get ip

	loc = get(f"http://ip-api.com/json/{ip.json()['ip']}") 	# location info bt ip

	city = loc.json()['city'] 										# current city by ip

	for_five_day = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c"#""" - 5 days/3 hours """
	now =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - current """

setup_vars()

def forecast():
	weather = get(for_five_day).json()
	result = [] 													# array with forecast data
	for x in weather['list']:
		result.append({'dt_txt':x['dt_txt'],'icon':x['weather'][0]['icon'],
			'temp_min':str(round(x['main']['temp_min'] - 273.15,2)),'temp_max':str(round(x['main']['temp_max'] - 273.15,2)),
			'humidity':x['main']['humidity'], 'cloudiness':x['clouds']['all']})
	return result

def update_info():
	global state
	i=0
	cur = get(now).json()
	data = None
	app.update_cur_data({'temp':cur['main']['temp'] - 273.15,
						'desc':cur['weather'][0]['description'],
						'icon':cur['weather'][0]['icon'],
						'city':cur['name']})
	forecas = forecast()
	app.update_forecast(forecas)
	while state:
		i+=1
		if i == 10:
			setup_vars()
			cur = get(now).json()
			data = None
			app.update_cur_data({'temp':cur['main']['temp'] - 273.15,
								'desc':cur['weather'][0]['description'],
								'icon':cur['weather'][0]['icon'],
								'city':cur['name']})
			res = forecast()
			app.update_forecast(res)
			i=0


update = Thread(target=update_info)
app = MainWindow(update,forecast())
sys.exit(app.exec())
update.join()
