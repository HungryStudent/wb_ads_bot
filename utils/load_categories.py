import requests
import sqlite3

req = requests.get("https://static-basket-01.wb.ru/vol0/data/subject-base.json")
data = req.json()
print("Loading...")

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
# for parent in data:
#     for category in parent["childs"]:
#         cursor.execute("INSERT INTO categories VALUES (?, ?)", (category["id"], category["name"]))
#         connection.commit()
# print("Finish categories, start catalog...")
# req = requests.get("https://cache-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json")
# data = req.json()
# for parent in data:
#     cursor.execute("INSERT INTO catalog(id, name, parent_id, url) VALUES (?, ?, 0, ?)", (parent["id"], parent["name"], parent["url"]))
#     connection.commit()
#
# for parent in data:
#
#     try:
#         for catalog in parent["childs"]:
#             cursor.execute("INSERT INTO catalog(id, name, parent_id, url) VALUES (?, ?, ?, ?)",
#                            (catalog["id"], catalog["name"], parent["id"], catalog["url"]))
#             connection.commit()
#     except KeyError:
#         continue



# req = requests.get("https://cache-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json")
# data = req.json()
# for parent in data:
#     cursor.execute("UPDATE catalog SET url = ? where id = ?", (parent["url"], parent["id"]))
#     connection.commit()
#
# for parent in data:
#     try:
#         for catalog in parent["childs"]:
#             cursor.execute("UPDATE catalog SET url = ? where id = ?", (catalog["url"], catalog["id"]))
#             connection.commit()
#     except KeyError:
#         continue