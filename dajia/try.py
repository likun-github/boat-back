import datetime

now = datetime.datetime.now()
print(now)
nowtime = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
print(nowtime)


