import os
import json
from os.path import join
import csv
from typing import List

FIND_ARR = []


def index(path):
    with open('index.csv', 'w', encoding='utf-8') as f:
        f.write('id;title\n')
        folder_list = os.listdir(path)
        for folder in folder_list:
            tmp_path = join(path, folder, 'data.json')
            try:
                with open(tmp_path, 'r', encoding="utf-8") as file_data:
                    data = json.load(file_data)
                data_id = data['id']
                title = data['title']
                tmp_string = f"{data_id};{title}\n"

                f.write(tmp_string)
            except Exception:
                print(f"While processing {tmp_path} error occurred!")

    with open("index.csv", encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for dict_line in reader:
            FIND_ARR.append((dict_line['id'], dict_line['title'].lower()))


def find(substr: str) -> List[str]:
    substr = substr.lower()
    id_arr = []
    for data_id, title in FIND_ARR:
        if substr in title:
            id_arr.append(data_id)
    return id_arr