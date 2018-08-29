#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
import requests
import sys

cgitb.enable()
print "Content-Type: text/plain;charset=utf-8"
print

para = cgi.FieldStorage()
if "player" not in para or "action" not in para:
    print "<H1>Error</H1>"
    print "Please fill the player and action para."
    sys.exit(0)

player = para['player'].value
player_escape = player.replace('#', '%23', 1)

action = para['action'].value

##2L92QYGLP
playerEP = {
    "info": "https://api.clashroyale.com/v1/players/{playerTag}",
    "chest": "https://api.clashroyale.com/v1/players/{playerTag}/upcomingchests",
    "battle": "https://api.clashroyale.com/v1/players/{playerTag}/battlelog",
}

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwOWJkMjljLWYxY2ItNDM0Zi05MzVkLTBkMzg2OGQ1MDg1YiIsImlhdCI6MTUzNTMwNzA5Miwic3ViIjoiZGV2ZWxvcGVyLzA5YWU0ZmJmLWQxNTctODBjMS1jYWEyLTlmZmRkMGIyNmZkZSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xODEuNjYuMzQiXSwidHlwZSI6ImNsaWVudCJ9XX0.B9Zp7vUc7VuHSiDru00rInxuDfdUdp6o2Oogs_fYzMKUn-rPZkJyRuMT5d_7prOYS6zZHyWb39DFo_3_Pqrbgg",
    'cache-control': "no-cache",
    }

ed = playerEP[action].replace('{playerTag}', player_escape)
response = requests.request("GET", ed, headers=headers)

print str(response.text)

