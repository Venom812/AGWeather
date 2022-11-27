from datetime import datetime
from json import dumps
from models import ForecastsRecord

# print dumps(datetime.now(), default=json_serial)

a = datetime.now().isoformat()

b = a

b = datetime.fromisoformat(b)

print(type(a))
print(type(b))

a = ForecastsRecord.objects.latest('rec_date')

print(a)

# forecasts_json_filename = datetime.now().replace(minute=0).strftime("forecasts_%d.%m_%H:%M")
# folder_database_json = ("database_json/forecasts/")
# if not os.path.exists(folder_database_json):
#     os.mkdir(folder_database_json)
# path_to_json_file = folder_database_json + "/" + forecasts_json_filename + ".json"

# if os.path.isfile(path_to_json_file):
#     with open(path_to_json_file) as file:
#         json_data = json.load(file)
#         file.close()
#         json_data[0] = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in json_data[0]]
#     return json_data

# with open("rp5.html", "w") as file:
#     file.write(src)
# return

# with open("rp5.html") as file:
#     src = file.read()
# src = req.text

# forecast_all = [forecast_scarp(id,14) for id in range(0, len(forecast_sources_names)-1)]

# forecast_all_T = list(zip(*forecast_all)) #[list(i) for i in zip(*forecast_all)]
# forecast_all_T[1] = forecast_all_T[1][0]

# with open(f"{folder_database_json}/{forecasts_json_filename}.json", "w", encoding="utf-8") as file:
#     json.dump(forecasts_database_record, file, indent=4, sort_keys=True, default=str) #ensure_ascii=False)

# (дата_вермя_ось_Х, дата_вермя_вспл), ((имя источника, цвет),(тепература, давление, скорость ветра))

# def read_forecasts_record_from_json_file(path_to_json_file):
#     with open(path_to_json_file) as file:
#         data = json.load(file)
#     print(data[0][])
#     return "fuck"