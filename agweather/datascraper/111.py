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