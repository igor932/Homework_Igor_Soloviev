import requests
import json
import sqlite3
from pprint import pprint

url = "https://understat.com/match/26840"

response = requests.get(url)
    
html_code = response.text

def extract_between(text, start, end):
    start_index = text.find(start)
    end_index = text.find(end, start_index + 1)

    if start_index != -1 and end_index != -1:
        return text[start_index + len(start):end_index]
    else:
        return "Подстрока не найдена"

text = response.text
start = "JSON.parse('"
end = "'),"
result = extract_between(text, start, end)

decoded_string = result.encode('utf-8').decode('unicode_escape')

data = json.loads(decoded_string)


conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS match_data (
                    id INTEGER PRIMARY KEY,
                    match_id INTEGER,
                    season TEXT,
                    date TEXT,
                    h_team TEXT,
                    a_team TEXT,
                    h_goals INTEGER,
                    a_goals INTEGER,
                    result TEXT,
                    player_id INTEGER,
                    player TEXT,
                    player_assisted TEXT,
                    minute INTEGER,
                    lastAction TEXT,
                    shotType TEXT,
                    situation TEXT,
                    xG REAL,
                    X REAL,
                    Y REAL,
                    h_a TEXT,
                    URL TEXT
                )''')


for team in data:
    for shot in data[team]:
        cursor.execute('''INSERT INTO match_data (
                            match_id, season, date, h_team, a_team, h_goals, a_goals, result,
                            player_id, player, player_assisted, minute, lastAction, shotType,
                            situation, xG, X, Y, h_a, URL
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (shot['match_id'], shot['season'], shot['date'], shot['h_team'], shot['a_team'],
                         shot['h_goals'], shot['a_goals'], shot['result'], shot['player_id'], shot['player'],
                         shot['player_assisted'], shot['minute'], shot['lastAction'], shot['shotType'],
                         shot['situation'], shot['xG'], shot['X'], shot['Y'], shot['h_a'], url))

conn.commit()


conn.close()
