import requests

r = requests.get('https://api.ipify.org?format=json')

loc = requests.get(f"http://ip-api.com/json/{r.json()['ip']}")

city = loc.json()['city']

for_five_day = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - 5 days/3 hours """
now =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" # """ - current """

cur = requests.get(now).json()

print(f"In {city} now is {cur['weather'][0]['description']} "
	f"(temperature {cur['main']['temp']-273.15})")
