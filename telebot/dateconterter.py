from datetime import datetime, timedelta
import re


def getDates(dateShift, type="date"):
    print(dateShift)
    dsign = {
        "-": -1,
        "+": 1
    }

    result = re.findall(r'^(\-||\+)(\d+)(\w+)$', dateShift)

    sign, num, de = (result[0][0], result[0][1], result[0][2])

    td = {
        "d" : timedelta(days= dsign[sign]*int(num)),
        "m" : timedelta(days= dsign[sign]*int(num)*30),
        "y" : timedelta(days= dsign[sign]*int(num)*365),
    }


    dateEnd = datetime.now()
    dateStart = dateEnd + td[de]

    if (type == "date"):
        dd = {
            'dateStart': formatDate(dateStart),
            'dateEnd': formatDate(dateEnd)
        }
    else:
        dd = {
            'dateStart': int(dateStart.timestamp())*1000,
            'dateEnd': int(dateEnd.timestamp())*1000
        } 
    
    return dd
    #td = timedelta()


def formatDate(dt):
    return dt.strftime("%Y-%m-%d")