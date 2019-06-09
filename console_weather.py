import requests

r = requests.get('https://api.ipify.org?format=json')

loc = requests.get(f"http://ip-api.com/json/{r.json()['ip']}")

city = loc.json()['city']

for_five_day = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - 5 days/3 hours """
now =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - current """

cur = requests.get(now).json()

print(f"In {city} now is {cur['weather'][0]['description']} "
	f"(temperature {cur['main']['temp']-273.15})")

def forecast(days):
	weather = requests.get(for_five_day).json()
	cur_day = int(weather['list'][0]['dt_txt'].split(' ')[0].split('-')[-1])
	res = cur_day
	for x in weather['list']:
		day = int(x['dt_txt'].split(' ')[0].split('-')[-1])-res
		if day == days:
			break
		print(x['dt_txt'] + ' ' + x['weather'][0]['description'] + ' (temperature from ' \
			+ str(round(x['main']['temp_min'] - 273.15,2)) + ' to ' + str(round(x['main']['temp_max'] - 273.15,2))+')')

a = input()
while a != "":
	if "forecast" in a[:9].lower():
		a = a.split(' ')
		if len(a)<3:
			print("You have to enter vaild command")
		try:
			days = int(a[-2])
			forecast(days)
		except Exception as e:
			print(e)
			print("Enter vaild command")
	elif "help" in a.lower():
		print("Enter 'forecast for <x> days' - to get forecast for x days (replace x with number from 1 to 5")
	a = input()


