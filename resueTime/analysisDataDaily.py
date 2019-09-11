#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import requests
import os

from datetime import datetime, timedelta

endpoint = 'https://www.rescuetime.com/anapi/data?key=B63ipO0EvRhYBr29VG5JJmqdXrv4ABb4sNWF_7gV&format=csv&resolution_time=day&perspective=interval&'

# 20190702
if  len(sys.argv) > 1:
    date = sys.argv[1]
    dt = datetime.strptime(date, "%Y%m%d")
else:
    dt = datetime.now() - timedelta(1)
    date = datetime.strftime(dt, "%Y%m%d")
writepath = "/home/pi/data/rescuetime/analysisData_{0}".format(dt.year)
ed = endpoint + 'restrict_begin=' + date
response = requests.request("GET", ed)
content = ""
for line in response.text.splitlines()[1:]:
    blocks = line.split(',')
    if int(blocks[1]) <= 15:
        continue
    content +=  "{0},{1}\n".format(date, u','.join(blocks[1:]).encode('utf-8').strip())
print content

# mode = 'a'
# if not os.path.exists(writepath):
#     mode = 'w'
#     content = "Date,Time Spent (seconds),Number of People,Activity,Category,Productivity\n" + content

# try:
#     with open(writepath, mode) as fileIO:
#         fileIO.write(content)
#         fileIO.close
# except NameError as e:
#     print e
# except ValueError as e:
#     print e
# except:
#     print "Unexpected error:", sys.exc_info()

