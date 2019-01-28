#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# to calculate money needed 
import sys
import requests
import json
import os

from datetime import datetime

endpoint = 'https://api.clashroyale.com/v1/players/{playerTag}'

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwOWJkMjljLWYxY2ItNDM0Zi05MzVkLTBkMzg2OGQ1MDg1YiIsImlhdCI6MTUzNTMwNzA5Miwic3ViIjoiZGV2ZWxvcGVyLzA5YWU0ZmJmLWQxNTctODBjMS1jYWEyLTlmZmRkMGIyNmZkZSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3MC4xODEuNjYuMzQiXSwidHlwZSI6ImNsaWVudCJ9XX0.B9Zp7vUc7VuHSiDru00rInxuDfdUdp6o2Oogs_fYzMKUn-rPZkJyRuMT5d_7prOYS6zZHyWb39DFo_3_Pqrbgg",
    'cache-control': "no-cache",
    }


player = sys.argv[1]
writepath = '/home/pi/data/clash_royale/' + player + '_weekly'

player_escape = '%23' + player
ed = endpoint.replace('{playerTag}', player_escape)
response = requests.request("GET", ed, headers=headers)
result = json.loads(response.text)

level_count = [0, 0, 2, 6, 16, 36, 86, 186, 386, 786, 1586, 2586, 4586, 9586]
money_level = [100000, 50000, 20000, 8000, 4000, 2000, 1000, 400, 150, 50, 20, 5]
category_cost = {
    '13': 185625, 
    '11': 185600, 
    '8': 184400, 
    '5': 175000
    }
cost = 0
total_cost = 0
common = common_cards = common_cost = 0
rare = rare_cards = rare_cost = 0
epic = epic_cards = epic_cost = 0
lengendary = lengendary_cards = lengendary_cost = 0

for card in result['cards']:
    deck_cost = 0
    diff = card['maxLevel'] - card['level']
    for i in range(diff):
        cost += money_level[i]
        deck_cost += money_level[i]
    total_cost += category_cost[str(card['maxLevel'])]

    if card['maxLevel'] == 5:
        lengendary += level_count[card['level']] + card['count']
        lengendary_cost += deck_cost
        lengendary_cards += 1
    elif card['maxLevel'] == 8:
        epic += level_count[card['level']] + card['count']
        epic_cost += deck_cost
        epic_cards += 1
    elif card['maxLevel'] == 11:
        rare += level_count[card['level']] + card['count']
        rare_cost += deck_cost
        rare_cards += 1
    elif card['maxLevel'] == 13:
        common += level_count[card['level']] + card['count']
        common_cost += deck_cost
        common_cards += 1

content = 'Legen: {0}K, {1}K, {2}% \n'.format((lengendary_cards*category_cost['5'] - lengendary_cost)/1000, lengendary_cost/1000, round((lengendary_cards*category_cost['5'] - lengendary_cost)/float(lengendary_cards*category_cost['5'])*100, 4))
content += 'Legen: {0}, {1}, {2}% \n'.format(lengendary, lengendary_cards*level_count[5] - lengendary, round(lengendary/float(lengendary_cards*level_count[5])*100, 2))
content += 'Epics: {0}K, {1}K, {2}% \n'.format((epic_cards*category_cost['8'] - epic_cost)/1000, epic_cost/1000, round((epic_cards*category_cost['8'] - epic_cost)/float(epic_cards*category_cost['8'])*100, 4))
content += 'Epics: {0}, {1}, {2}% \n'.format(epic, epic_cards*level_count[8] - epic, round(epic/float(epic_cards*level_count[8])*100, 2))
content += 'Rares: {0}K, {1}K, {2}% \n'.format((rare_cards*category_cost['11'] - rare_cost)/1000, rare_cost/1000, round((rare_cards*category_cost['11'] - rare_cost)/float(rare_cards*category_cost['11'])*100, 4))
content += 'Epics: {0}, {1}, {2}% \n'.format(rare, rare_cards*level_count[11] - rare, round(rare/float(rare_cards*level_count[11])*100, 2))
content += 'Commo: {0}K, {1}K, {2}% \n'.format((common_cards*category_cost['13'] - common_cost)/1000, common_cost/1000, round((common_cards*category_cost['13'] - common_cost)/float(common_cards*category_cost['13'])*100, 4))
content += 'Commo: {0}, {1}, {2}% \n'.format(common, common_cards*level_count[13] - common, round(common/float(common_cards*level_count[13])*100, 2))
content += 'Total: {0}K, {1}K, {2}%'.format(str((total_cost-cost)/1000), str(cost/1000), str(round((total_cost-cost)/float(total_cost)*100, 4)))

mode = 'a' if os.path.exists(writepath) else 'w'

try:
    with open(writepath, mode) as fileIO:
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