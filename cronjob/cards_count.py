#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import sys
import requests
import json
from datetime import datetime

endpoint = 'https://api.clashroyale.com/v1/players/{playerTag}'

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwOWJkMjljLWYxY2ItNDM0Zi05MzVkLTBkMzg2OGQ1MDg1YiIsImlhdCI6MTUzNTMwNzA5Miwic3ViIjoiZGV2ZWxvcGVyLzA5YWU0ZmJmLWQxNTctODBjMS1jYWEyLTlmZmRkMGIyNmZkZSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xODEuNjYuMzQiXSwidHlwZSI6ImNsaWVudCJ9XX0.B9Zp7vUc7VuHSiDru00rInxuDfdUdp6o2Oogs_fYzMKUn-rPZkJyRuMT5d_7prOYS6zZHyWb39DFo_3_Pqrbgg",
    'cache-control': "no-cache",
    }

player = sys.argv[1]
player_escape = '%23' + player
ed = endpoint.replace('{playerTag}', player_escape)
response = requests.request("GET", ed, headers=headers)
result = json.loads(response.text)

common = common_cards = 0
rare = rare_cards = 0
epic = epic_cards =0
lengendary = lengendary_cards = 0
level_count = [0, 0, 2, 6, 16, 36, 86, 186, 386, 786, 1586, 2586, 4586, 9586]
for card in result['cards']:
    if card['maxLevel'] == 5:
        lengendary += level_count[card['level']] + card['count']
        lengendary_cards += 1
    elif card['maxLevel'] == 8:
        epic += level_count[card['level']] + card['count']
        epic_cards += 1
    elif card['maxLevel'] == 11:
        rare += level_count[card['level']] + card['count']
        rare_cards += 1
    elif card['maxLevel'] == 13:
        common += level_count[card['level']] + card['count']
        common_cards += 1

content = (str(lengendary) + ',' + str(lengendary_cards*level_count[5] - lengendary) + ',' +
        str(epic) + ',' + str(epic_cards*level_count[8] - epic) + ',' + 
        str(rare) + ',' + str(rare_cards*level_count[11] - rare) + ',' +
        str(common) + ',' + str(common_cards*level_count[13] - common))
        

try:
    fileIO = open('/home/pi/data/clash_royale/' + player[1:], 'r+')
    lastLine=","
    for line in fileIO:
        lastLine = line

    fileIO.write(datetime.now().strftime("%Y%m%d"))
    fileIO.write(',')
    fileIO.write(content + '\n')
    fileIO.close
except NameError as e:
    print e
except ValueError as e:
    print e
except:
    print "Unexpected error:", sys.exc_info()