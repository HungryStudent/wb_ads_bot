from urllib import parse
import requests

from utils import db


def get_search(query, curr_page, city):
    parse_query = parse.quote(query)
    req = requests.get("https://catalog-ads.wildberries.ru/api/v5/search?keyword=" + parse_query,
                       cookies={"__dst": city})
    data = req.json()
    if data["pages"] is None:
        return None

    msg_text = f"<b>Актуальные ставки рекламодателей по запросу <u>{query}</u>:</b>\n\n"

    msg_text += "<b>Приоритет категорий:</b>\n"
    for category_id in data["prioritySubjects"]:
        category = db.get_category(category_id)
        msg_text += f"ID {category['id']} - {category['name']}\n"

    msg_text += "\n<b>Реклама отображается на страницах:</b>\n"
    for page in data["pages"]:
        msg_text += f"- Страница {page['page']}, Позиции: {', '.join(map(str, page['positions']))}\n"

    msg_text += "\n<b>Рекламодатели:</b>\n\n"
    numbers_emoji = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣"]
    for index, product in enumerate(data["adverts"][curr_page * 7 - 7:curr_page * 7]):
        req = requests.get(f"https://card.wb.ru/cards/detail?nm={product['id']}")
        brand = req.json()["data"]["products"][0]["brand"]
        msg_text += f"{numbers_emoji[index]} <b>CPM {product['cpm']} руб</b>, Артикул: <u>{product['id']}</u>, Бренд: {brand}\n\n"
        pass

    msg_text += "<i>🔥 Хотите продвинуть товар без трат на рекламу?</i>\n👉 @automate_mp"
    return_data = {"msg_text": msg_text, "products_count": len(data["adverts"])}
    return return_data


def get_card(article_id, curr_page, city):
    req = requests.get("https://carousel-ads.wildberries.ru/api/v4/carousel?nm=" + article_id, cookies={"__dst": city})
    data = req.json()

    msg_text = f"<b>Актуальные ставки рекламодателей по артикулу <u>{article_id}</u>:</b>\n\n"

    msg_text += "<b>Рекламодатели:</b>\n\n"
    numbers_emoji = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣"]

    for index, product in enumerate(data[curr_page * 7 - 7:curr_page * 7]):
        req = requests.get(f"https://card.wb.ru/cards/detail?nm={product['nmId']}")
        brand = req.json()["data"]["products"][0]["brand"]
        msg_text += f"{numbers_emoji[index]} <b>CPM {product['cpm']} руб</b>, Артикул: <u>{product['nmId']}</u>, Бренд: {brand}\n\n"

    msg_text += "<i>🔥 Хотите продвинуть товар без трат на рекламу?</i>\n👉 @automate_mp"
    return_data = {"msg_text": msg_text, "products_count": len(data)}
    return return_data
