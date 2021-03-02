from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

import database

session = requests.Session()

url = "https://roszdravnadzor.gov.ru/services/misearch"


def get_data_modal_window(table_name, number):
    """получить данные из модального окна"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        params = {
            "id": number,
            "table_name": table_name,
            "fancybox": True,
        }

        response = session.get(url=url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, "lxml")
        param = soup.find("table", {"class": "table-type-3"}).find("a").get("href")
        link = url + param
        print(f"Ссылка модальное окно - {response.url}")
        print(f"Ссылка на файл - {link}")
        return link

    except Exception as e:
        print(f"Файл для загрузки отсутствует")
        print(e)


def unique_registry_numbers():
    """получить из базы уникальные регистрационные номера"""
    fields = database.get_fields_data()
    lis = []

    for e, field in enumerate(fields, 1):
        dt_row_id = field["DT_RowId"]
        unique_numbers = field["col1"]["label"]
        table_name, number = dt_row_id.split("-")

        lis.append((unique_numbers, table_name, number))

        print(e, dt_row_id, "->", (unique_numbers, table_name, number))

    return lis


def download_file(unique_numbers, link):
    """сохранить файл и предать имя в базу"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }

        response = session.post(url=link, headers=headers, stream=True)
        file_name = response.headers['Content-Disposition'].split('"')[-2]

        print(f'Имя файла {file_name} был удачно сохранено')

        # with open(os.path.join(documents_directory_test, file_name), 'wb') as fd:
        #     for chunk in response.iter_content(chunk_size=1024):
        #         fd.write(chunk)

        database.update_data(unique_numbers, file_name)

    except Exception as e:
        print(f"ошибка сохранения: имя отсутствует - в базу будет передано 'Файл отсутствует'")
        print(e)
        database.update_data(unique_numbers, "Файл отсутствует")


count = 0


def doubler(list_numbers):
    """функция для обработки многопотоковом режиме"""
    global count
    count += 1

    unique_numbers, table_name, number = list_numbers

    print(f"{count}) | {unique_numbers} | {table_name} | {number}")

    link = get_data_modal_window(table_name, number)
    download_file(unique_numbers, link)

    print("=" * 100)


def main():
    """функция запуска"""
    list_numbers = unique_registry_numbers()

    print(list_numbers)

    pool = Pool(processes=30)
    pool.map(doubler, list_numbers)

    print("все поля загружены")


if __name__ == '__main__':
    main()

