from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv


def delete_quiz():
    load_dotenv(find_dotenv())

    db_connection_string = os.getenv("db_conn_str")

    cluster = MongoClient(db_connection_string)
    db = cluster["DB_Quiz"]
    collection = db["Collection_Quiz"]

    quiz_id_list = []
    ids = collection.find()
    for i in ids:
        quiz_id_list.append(i["_id"])

    while True:
        try:
            quiz_id = int(input("Enter the ID of the quiz you want to delete: "))
            break
        except ValueError:
            print('ID is integer number.')

    if quiz_id in quiz_id_list:
        collection.delete_one({"_id": quiz_id})

        print(f"Quiz ID {quiz_id} removed")

    elif quiz_id not in quiz_id_list:
        print(f"Quiz ID {quiz_id} not found.")
