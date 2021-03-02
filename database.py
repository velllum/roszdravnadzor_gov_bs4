from pymongo import MongoClient

connection = "mongodb+srv://velllum:0sxfeDlou9i66twP@cluster0.fs8kg.mongodb.net/freelancers?retryWrites=true&w=majority"

client = MongoClient(connection)
db = client.freelancers["roszdravnadzor_gov_bs4"]


def get_fields_data():
    """Получить поля из базы"""
    try:
        return db.find({}, {"_id": 0})
    except Exception as e:
        print(f"Произошла ошибка {e}")



def create_data(dic):
    """- Сохраняет собранные данные в удаленную базу mongodb"""
    try:
        db.insert(dic)
    except Exception as e:
        print(f"Произошла ошибка {e}")


def remove_data():
    """- Отчистить базу от всех данных"""
    db.delete_many({})


def update_data(id_, file_name):
    """- Обновить и добавить данные"""
    db.update_one({"col1": {"label": id_}}, {"$set": {"file_name": file_name}})





