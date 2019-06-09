import requests

r = requests.get('https://api.ipify.org?format=json')

loc = requests.get(f"http://ip-api.com/json/{r.json()['ip']}")

city = loc.json()['city']

f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c" """ - 5 days/3 hours """
f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=377ef42e9dc5e87b6c24eb7dc069c30c"  """ - current """

