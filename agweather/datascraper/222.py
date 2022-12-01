from json import load

with open("agweather/datascraper/datascraper_config.json") as file:
    json_data = load(file)

print(json_data)
