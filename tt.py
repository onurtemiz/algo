from datetime import datetime
from datetime import timedelta

dt_string = "2018-06-20"
dt_object1 = datetime.strptime(dt_string, "%Y-%m-%d")

print(dt_object1 + timedelta(days=-30))