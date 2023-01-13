from pymongo import MongoClient
import random
import os
import delete_quiz
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

Create_New_Quiz = 1
Select_An_Existing_Quiz = 2
Delete_Quiz = 3
Quit_Program = 4

View_Quizzes = 1
Find_Quizzes = 2
Open_Quizzes = 3
Back_To_Menu = 4

db_connection_string = os.getenv("db_conn_str")
print(db_connection_string)

cluster = MongoClient(db_connection_string)
db = cluster["DB_Quiz"]
collection = db["Collection_Quiz"]


def main():
    choice = 0
    while choice != Quit_Program:
        print("~~~~~~~~~~~~~~~MENU~~~~~~~~~~~~~~~\n"
              "Choose the desired function.\n"
              "1) Create a new quiz.\n"
              "2) Take the quiz.\n"
              "3) Delete quiz.\n"
              "4) Quit.\n"
              "~~~~~~~~~~~~~~~MENU~~~~~~~~~~~~~~~\n")
        while True:         # The loop will repeat until choice becomes an integer
            try:
                choice = int(input("Enter the required option (1-4): "))
                break
            except ValueError:
                print("Enter integer number.")

        if choice == Create_New_Quiz:
            create_new_quiz_function()

        elif choice == Select_An_Existing_Quiz:
            select_an_existing_quiz()

        elif choice > Quit_Program or choice < Create_New_Quiz:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                  "Enter an option from 1 to 4.\n"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        elif choice == Delete_Quiz:
            delete_quiz.delete_quiz()


def create_new_quiz_function():
    quiz_name = input("Enter the name of the quiz: ")
    while True:     # The loop will repeat until number_of_questions becomes an integer
        try:
            number_of_questions = int(input("Enter number of questions: "))
            break
        except ValueError:
            print("Enter integer number.")
    create_test(quiz_name, number_of_questions)


def create_test(name, number_of_questions):    # This function creates a test
    quiz_id = random.randint(1, 9999)   # Create random ID from 1 to 9999
    ids = collection.find()             # Read db
    quiz_id_list = []                   # List with quiz ID
    for i in ids:                       # Add ID to quiz_id_list
        quiz_id_list.append(i["_id"])

    while quiz_id in quiz_id_list:      # While new random ID in quiz_id_list create new ID
        quiz_id = random.randint(1, 9999)

    quiz = {                            # Quiz dct
        "_id": quiz_id,
        "name": name,
        "questions": {},
        "correct_answer": []
    }

    question_counter = 1
    variant_counter = 1
    variants_list = []

    for i in range(1, number_of_questions + 1):
        question = input(f"Enter question number {question_counter}: ")
        while True:        # The loop will repeat until variants becomes an integer
            try:
                variants = int(input(f"Enter the number of variants in question number {question_counter}: "))
                break
            except ValueError:
                print("Enter integer number.")

        for v in range(1, variants+1):
            variant = input(f"Enter variant number {variant_counter}: ")
            variants_list.append(variant)
            variant_counter += 1
            quiz["questions"][question] = variants_list.copy()

        variants_list.clear()

        while True:    # The loop will repeat until correct_answer becomes an integer
            try:
                correct_answer = int(input(f"What number is the correct answer? Question number {question_counter}: "))
                break
            except ValueError:
                print("Enter integer number.")

        quiz["correct_answer"].append(correct_answer)

        question_counter += 1
        variant_counter = 1

    collection.insert_one(quiz)


def select_an_existing_quiz():     # This feature allows you to work with already created quizzes.
    choice = 0

    quiz_id_list = []                # List with ids in database
    ids = collection.find()
    for i in ids:
        quiz_id_list.append(i["_id"])

    while choice != Back_To_Menu:
        print("\n---------------Quiz Menu---------------\n"
              "1) View list of quizzes\n"
              "2) Find quiz by ID\n"
              "3) Enter the ID of the quiz you want to open\n"
              "4) Back to main menu\n")
        while True:      # The loop will repeat until choice becomes an integer
            try:
                choice = int(input("Enter your choice (1-4): "))
                break
            except ValueError:
                print("Enter integer number.")

        if choice == View_Quizzes:    # Show ID and name of the quiz
            view_quizzes()

        elif choice == Find_Quizzes:      # Find quiz by ID
            find_quizzes(quiz_id_list)

        elif choice == Open_Quizzes:   # Open Quiz
            open_quizzes(quiz_id_list)


def view_quizzes():    # Show ID and name of the quiz
    quizzes = collection.find()
    for i in quizzes:
        print(f"ID: {i['_id']:5}| Name of the quiz: {i['name']}")


def find_quizzes(quiz_id_list):   # Find quiz by ID
    while True:  # The loop will repeat until quiz_id becomes an integer
        try:
            quiz_id = int(input("Enter quiz ID: "))
            break
        except ValueError:
            print("ID is integer number.")

    if quiz_id in quiz_id_list:
        quiz_name = collection.find_one({"_id": quiz_id})["name"]
        print(f"Quiz name: {quiz_name}.")

    elif quiz_id not in quiz_id_list:
        print("ID not found.")


def open_quizzes(quiz_id_list):   # Open Quiz
    while True:  # The loop will repeat until quiz_id becomes an integer
        try:
            quiz_id = int(input("Enter quiz ID: "))
            break
        except ValueError:
            print("ID is integer number.")

    if quiz_id in quiz_id_list:
        quiz_name = collection.find_one({"_id": quiz_id})["name"]
        print(f"QUIZ: {quiz_name}")

        correct_list = collection.find_one({"_id": quiz_id})["correct_answer"]
        user_answers = []
        quiz_dct = collection.find_one({"_id": quiz_id})["questions"]
        questions = quiz_dct.keys()

        question_countre = 1
        variant_countre = 1

        for i in questions:

            print(f"\nQuestion {question_countre}) {i}")
            for v in quiz_dct[i]:
                print(f"Variant {variant_countre}: {v}")
                variant_countre += 1
            question_countre += 1
            variant_countre = 1

            while True:  # The loop will repeat until answer becomes an integer
                try:
                    answer = int(input("Enter the number of the correct answer: "))
                    break
                except ValueError:
                    print("Enter integer number.")

            user_answers.append(answer)

        total_correct_answers = 0
        total_wrong_answers = 0
        for i in range(len(correct_list)):
            if correct_list[i] == user_answers[i]:
                total_correct_answers += 1
            elif correct_list[i] != user_answers[i]:
                total_wrong_answers += 1

        print(f"\nNumber of correct answers = {total_correct_answers}\n"
              f"Number of wrong answers = {total_wrong_answers}")

    elif quiz_id not in quiz_id_list:
        print("ID not found.")


if __name__ == "__main__":
    main()
