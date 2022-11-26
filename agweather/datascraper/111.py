from datetime import datetime
from json import dumps

# print dumps(datetime.now(), default=json_serial)

a = datetime.now().isoformat()

b = a

b = datetime.fromisoformat(b)

print(type(a))
print(type(b))
