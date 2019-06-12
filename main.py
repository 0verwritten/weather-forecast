from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_Weather
import threading
import requests
import time
import sys

global state, ip, loc, city, for_five_day, now
state=True

class MainWindow(QtWidgets.QApplication, Ui_Weather):
	def __init__(self, th):
		super(MainWindow, self).__init__([])
		self.MainWindow = QtWidgets.QMainWindow()
		self.setupUi(self.MainWindow)
		th.start()													# Start second thread
		self.aboutToQuit.connect(self.closeEvent)
		self.MainWindow.show()

	def update_cur_data(self,cur):
		pass
	def update_forecast(self,forecast):
		print()
		print(forecast)
		print()
	def closeEvent(self):
		global state
		state=False

def setup_vars():
	global ip, loc, city, for_five_day, now
	ip = requests.get('https://api.ipify.org?format=json')			# get ip

	loc = requests.get(f"http://ip-api.com/json/{ip.json()['ip']}") 	# location info bt ip

	city = loc.json()['city'] 										# current city by ip

	for_five_day = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c"#""" - 5 days/3 hours """
	now =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - current """

setup_vars()

def forecast():
	weather = requests.get(for_five_day).json()
	result = [] 													# array with forecast data
	for x in weather['list']:
		result.append({'dt_txt':x['dt_txt'],'icon':x['weather'][0]['icon'],
			'temp_min':str(round(x['main']['temp_min'] - 273.15,2)),'temp_max':str(round(x['main']['temp_max'] - 273.15,2)),
			'humidity':x['main']['humidity'], 'cloudiness':x['clouds']['all']})
	return result

def update_info():
	global state
	i=0
	cur = requests.get(now).json()
	data = None
	app.update_cur_data({'temp':cur['main']['temp'] - 273.15,
						'desc':cur['weather'][0]['description'],
						'icon':cur['weather'][0]['icon'],
						'city':cur['name']})
	res = forecast()
	while state:
		i+=1
		if i == 10:
			setup_vars()
			cur = requests.get(now).json()
			data = None
			app.update_cur_data({'temp':cur['main']['temp'] - 273.15,
								'desc':cur['weather'][0]['description'],
								'icon':cur['weather'][0]['icon'],
								'city':cur['name']})
			res = forecast()
			app.update_forecast(res)
			i=0


update = threading.Thread(target=update_info)
app = MainWindow(update)
sys.exit(app.exec())
update.join()
