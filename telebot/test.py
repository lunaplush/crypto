#from datetime import datetime, timedelta
import dateconterter

dif = "-7d"
dif = "+1m"
dif = "-10m"
dif = "-1y"
test = dateconterter.getDates(dif)
print(test)


"""
d = datetime.now()
print(d)

td = timedelta(days=10)
print(td)

nd = d-td
print(nd.strftime("%Y-%m-%d"))
"""
