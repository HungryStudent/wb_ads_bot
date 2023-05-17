from urllib import parse

import aiohttp
import requests

from utils import db

numbers_emoji = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def get_emoji_text(index):
    return "".join([numbers_emoji[int(i)] for i in str(index)])


def get_search(query, curr_page, city):
    parse_query = parse.quote(query)
    req = requests.get("https://catalog-ads.wildberries.ru/api/v5/search?keyword=" + parse_query,
                       cookies={"__dst": city})
    data = req.json()
    if data["pages"] is None:
        return None

    msg_text = f"<b>Актуальные ставки рекламодателей по запросу <u><a href='https://www.wildberries.ru/catalog/0/search.aspx?search={query}'>{query}</a></u>:</b>\n\n"

    msg_text += "<b>Приоритет категорий:</b>\n"
    for category_id in data["prioritySubjects"]:
        category = db.get_category(category_id)
        msg_text += f"ID {category['id']} - {category['name']}\n"

    msg_text += "\n<b>Реклама отображается на страницах:</b>\n"
    for page in data["pages"]:
        msg_text += f"- Страница {page['page']}, Позиции: {', '.join(map(str, page['positions']))}\n"

    msg_text += "\n<b>Рекламодатели:</b>\n\n"

    for index, product in enumerate(data["adverts"][curr_page * 7 - 7:curr_page * 7]):
        req = requests.get(f"https://card.wb.ru/cards/detail?nm={product['id']}")
        brand = req.json()["data"]["products"][0]["brand"]
        page_index = curr_page * 7 - (7 - index) + 1
        emoji = get_emoji_text(page_index)
        msg_text += f"{emoji} <b>CPM {product['cpm']} руб</b>, Артикул: <u><a href='https://www.wildberries.ru/catalog/{product['id']}/detail.aspx'>{product['id']}</a></u>, Бренд: {brand}\n\n"

    msg_text += "<i>🔥 Хотите продвинуть товар без трат на рекламу?</i>\n👉 @automate_mp"
    return_data = {"msg_text": msg_text, "products_count": len(data["adverts"])}
    return return_data


def get_card(article_id, curr_page, city):
    req = requests.get("https://carousel-ads.wildberries.ru/api/v4/carousel?nm=" + article_id, cookies={"__dst": city})
    data = req.json()

    msg_text = f"<b>Актуальные ставки рекламодателей по артикулу <u><a href='https://www.wildberries.ru/catalog/{article_id}/detail.aspx'>{article_id}</a></u>:</b>\n\n"

    msg_text += "<b>Рекламодатели:</b>\n\n"

    for index, product in enumerate(data[curr_page * 7 - 7:curr_page * 7]):
        req = requests.get(f"https://card.wb.ru/cards/detail?nm={product['nmId']}")
        brand = req.json()["data"]["products"][0]["brand"]
        page_index = curr_page * 7 - (7 - index) + 1
        emoji = get_emoji_text(page_index)
        msg_text += f"{emoji} <b>CPM {product['cpm']} руб</b>, Артикул: <u><a href='https://www.wildberries.ru/catalog/{product['nmId']}/detail.aspx'>{product['nmId']}</a></u>, Бренд: {brand}\n\n"

    msg_text += "<i>🔥 Хотите продвинуть товар без трат на рекламу?</i>\n👉 @automate_mp"
    return_data = {"msg_text": msg_text, "products_count": len(data)}
    return return_data


def get_catalog(catalog_id, curr_page, city):
    req = requests.get(f"https://catalog-ads.wildberries.ru/api/v5/catalog?menuid={catalog_id}",
                       cookies={"__dst": city})
    data = req.json()
    if data["pages"] is None:
        return None
    catalog = db.get_catalog_by_id(catalog_id)
    msg_text = f"<b>Актуальные ставки в категории <u><a href='https://www.wildberries.ru/{catalog['url']}'>{catalog['name']}</a></u>:</b>\n\n<b>РЕКЛАМОДАТЕЛИ:</b>\n\n"

    for index, product in enumerate(data["adverts"][curr_page * 7 - 7:curr_page * 7]):
        req = requests.get(f"https://card.wb.ru/cards/detail?nm={product['id']}")
        brand = req.json()["data"]["products"][0]["brand"]
        page_index = curr_page * 7 - (7 - index) + 1
        emoji = get_emoji_text(page_index)
        msg_text += f"{emoji} <b>CPM {product['cpm']} руб</b>, Артикул: <u><a href='https://www.wildberries.ru/catalog/{product['id']}/detail.aspx'>{product['id']}</a></u>, Бренд: {brand}\n\n"

    msg_text += "<i>🔥 Хотите продвинуть товар без трат на рекламу?</i>\n👉 @automate_mp"
    return_data = {"msg_text": msg_text, "products_count": len(data["adverts"])}
    return return_data


async def get_card_details(article_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://card.wb.ru/cards/detail?curr=rub&dest=-1257786&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,48,110,22,31,71,114,111&spp=0&nm={article_id}') as resp:
            if resp.status == 404:
                return
            response = await resp.json()

            if not response["data"]["products"]:
                return
            return response["data"]["products"][0]


async def get_ads(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={query}') as resp:
            response = await resp.json()
            return response
