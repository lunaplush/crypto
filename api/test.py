from datetime import datetime


dt = datetime.now()

ts = int(dt.timestamp())*1000

dt2 = datetime.fromtimestamp(ts / 1000)

print(dt)
print(ts)
print(dt2)


datetime_str = '09/19/22 13:55:26'
datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
datetime_str = '19.09.1982'
datetime_object = datetime.strptime(datetime_str, '%d.%m.%Y')

print(datetime_object)