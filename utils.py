import re
import datetime

def convertToDate(date:str):
    return datetime.datetime.strptime(date, '%Y-%m-%d')

def convertFromDate(date:datetime.date):
    return date.strftime('%Y-%m-%d')

def checkBatch(batch:str):
    if re.match('\d\d\d\d[-]\d\d\d\d',batch):
        return batch
    raise ValueError('Invalid batch. Use format YYYY-YYYY')