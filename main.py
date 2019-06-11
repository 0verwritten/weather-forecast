from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_Weather
import threading
import requests
import time
import sys

class MainWindow(QtWidgets.QApplication, Ui_Weather):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__([])
		self.is_working = True
		self.MainWindow = QtWidgets.QMainWindow()
		r = requests.get('https://api.ipify.org?format=json')
		self.setupUi(self.MainWindow)
		self.MainWindow.show()

	def update_cur_data(self,cur):
		pass

app = MainWindow()

r = requests.get('https://api.ipify.org?format=json')

loc = requests.get(f"http://ip-api.com/json/{r.json()['ip']}")

city = loc.json()['city']

for_five_day = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - 5 days/3 hours """
limit = 5 # days
now =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - current """

def forecast(days):
	weather = requests.get(for_five_day).json()
	cur_day = int(weather['list'][0]['dt_txt'].split(' ')[0].split('-')[-1])
	res = cur_day
	result = []
	for x in weather['list']:
		day = int(x['dt_txt'].split(' ')[0].split('-')[-1])-res
		if day == days:
			break
		result.append({'dt_txt':x['dt_txt'],'desc':x['weather'][0]['description'],
			'temp_min':str(round(x['main']['temp_min'] - 273.15,2)),'temp_max':str(round(x['main']['temp_max'] - 273.15,2)),
			'humidity':x['main']['humidity'], 'cloudiness':x['clouds']['all']})
		print(x['dt_txt'] + ' ' + x['weather'][0]['description'] + ' (temperature from ' \
			+ str(round(x['main']['temp_min'] - 273.15,2)) + ' to ' + str(round(x['main']['temp_max'] - 273.15,2))+')')

def update_info():
	while app.is_working:
		cur = requests.get(now).json()
		app.update_cur_data(cur)
		r = forecast(6)
		print(r)
		print(cur)
		time.sleep(3600)

update = threading.Thread(target=update_info)
update.start()
sys.exit(app.exec())
