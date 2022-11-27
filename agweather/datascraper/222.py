# import datetime 

# d = datetime.datetime.now().replace(minute=0,second=0, microsecond=0).isoformat()

# d = d.fromisoformat()
from datetime import datetime

d = datetime.now().isoformat()
print(type(d))
  
d = datetime.fromisoformat(d)
print(d)
# dd = datetime.date.fromisoformat(d)

# print(d)
