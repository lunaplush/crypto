from datetime import datetime, timedelta
import re


def getDates(dateShift):
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

    dd = {
        'dateStart': formatDate(dateStart),
        'dateEnd': formatDate(dateEnd)
    }
    
    return dd
    #td = timedelta()


def formatDate(dt):
    return dt.strftime("%Y-%m-%d")