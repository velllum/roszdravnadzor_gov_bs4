import math

import requests
from bs4 import BeautifulSoup

import database

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}

url_post_req = "https://roszdravnadzor.gov.ru/ajax/services/misearch"

data = {
    "start": 0,
    "length": 100,
    "id_sclass": None
}


def get_amount_database():
    """получить количество всех данных"""
    response = session.post(url=url_post_req, headers=headers, data=data)
    return response.json()["recordsTotal"]


def calculate_data_page():
    """получить округленное число страниц"""
    number_page = get_amount_database() / data["length"]
    return math.ceil(number_page)


def get_all_data():
    """получить все данные с сайта в виде словаря"""
    number_page = calculate_data_page()

    print(number_page)

    for i in range(1, number_page+1):
        response = session.post(url=url_post_req, headers=headers, data=data)
        data_ = response.json()["data"]
        data["start"] += 100

        database.create_data(data_)

        print(f"{i}), собрана данных - {data['start']}, всего страниц - {number_page}")
        print("_" * 100)


def get_numbers_class():
    """получить количество option из выпадающего списка"""
    response = session.get("https://roszdravnadzor.gov.ru/services/misearch", headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    uls = soup.find("select", {"id": "id_id_sclass"}).find_all("option")
    number_option = uls[-1].get("value")
    return number_option


def main():
    option_list = get_numbers_class()
    count = 0

    while count < int(option_list):

        count += 1

        # if count == 1:
        #     continue

        data["id_sclass"] = count

        print(count, get_amount_database(), data)
        print("=" * 100)

        get_all_data()

        data["start"] = 0

        print("*" * 100)



if __name__ == '__main__':
    main()

