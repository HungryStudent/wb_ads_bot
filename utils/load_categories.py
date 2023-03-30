import requests
import sqlite3
req = requests.get("https://static-basket-01.wb.ru/vol0/data/subject-base.json")
data = req.json()
print("Loading...")
for parent in data:
    for category in parent["childs"]:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO categories VALUES (?, ?)", (category["id"], category["name"]))
        connection.commit()
