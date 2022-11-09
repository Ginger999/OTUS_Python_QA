# -*- coding: utf-8 -*-

"""
    Data processing: distribute all books from the csv file to users
"""

import csv
import inspect
import json
import os

CURRENT_PATH = os.path.split(inspect.getfile(inspect.currentframe()))[0]


def get_data_path():
    data_path = os.path.abspath(os.path.join(CURRENT_PATH, "./data"))
    if os.path.exists(data_path):
        return data_path
    else:
        return CURRENT_PATH


def get_file_path(filename):
    return os.path.join(DATA_PATH, filename)


# define file paths
DATA_PATH = get_data_path()
FILE_USERS_PATH = get_file_path("users.json")
FILE_BOOKS_PATH = get_file_path("books.csv")
FILE_RESULT_PATH = get_file_path("result.json")

with open(FILE_USERS_PATH, "r") as f_users:
    json_users = json.load(f_users)

# collect the necessary information about users in the resulting list
result = []
for user in json_users:
    result.append(
        {
            "name": user["name"],
            "gender": user["gender"],
            "address": user["address"],
            "age": user["age"],
            "books": [],
        }
    )

# collect all books in a list
books = []
with open(FILE_BOOKS_PATH) as f_books:
    csv_reader = csv.reader(f_books, delimiter=",")
    csv_header = next(csv_reader)

    for row in csv_reader:
        books.append(
            {
                "title": row[csv_header.index("Title")],
                "author": row[csv_header.index("Author")],
                "pages": int(row[csv_header.index("Pages")]),
                "genre": row[csv_header.index("Genre")],
            }
        )

# distribute books to users
i = 0
for book in books:
    result[i]["books"].append(book)
    i += 1
    i = i % result.__len__()

# create final json file
json_result = json.dumps(result, indent=4)
f_res = open(FILE_RESULT_PATH, "w")
f_res.write(json_result)
f_res.write("\n")
