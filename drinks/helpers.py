import random
from datetime import datetime

import convertdate.persian as iran_calender


def create_uuid():
    letters = '1234567890abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(5))


def convert_date_to_gregorian(date):
    '''
    Converts date from format persian date(YYYY-MM-DD) to Gregorian YYYY-MM-DD as date class
    '''
    year, month, day = (int(x) for x in date.split('-'))
    gregorian_date = iran_calender.to_gregorian(year, month, day)
    string_gregorian_date = '-'.join(str(x) for x in gregorian_date)
    date = datetime.strptime(string_gregorian_date, '%Y-%m-%d')
    return date
