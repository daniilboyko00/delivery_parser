from xmlrpc.client import Boolean
import requests
from bs4 import BeautifulSoup
import csv
import json
import re

# def validate_number(func):
#     def wrapper(number):
#         if not type(number) == int:
#             print('1')


def get_page_data(number):
        params = {'tracking_number': number}
        fields = ['Дата', 'Описание', 'Пункт назанчения', 'Вес', 'Габариты']
        r = requests.get('https://litemf.com/ru/tracking',params=params)
        page_text = r.text
        try:
            page_data = BeautifulSoup(page_text, 'html.parser')
            tracking_list = page_data.find_all('li',attrs={"class": "checkpoint"})
            date = [item.find(class_ = "date").get_text() for item in tracking_list]
            desc = [item.find(class_ = "description").get_text() for item in tracking_list ]
            name = [item.find(class_ = "name").get_text() for item in tracking_list ]
            weight_and_gab = page_data.find_all('dd')[0].get_text(), page_data.find_all('dd')[1].get_text().replace('\n','').replace(' ','')
        except:
            return False
        with open("output_files/data.csv", mode="w", encoding='utf-8') as f_csv:
            file_writer = csv.writer(f_csv, delimiter = ",")
            file_writer.writerow(fields)
            for row in range(len(date)):
                if row == 0:
                    file_writer.writerow([date[row], desc[row], name[row], weight_and_gab[0], weight_and_gab[1]])
                else:
                    file_writer.writerow([date[row], desc[row], name[row]])

        with open('output_files/data.json', 'w') as f_json:
            json.dump({
        'Даты': date,
        'Описания': desc,
        'Пункты назначения': name,
        'Вес': weight_and_gab[0],
        'Габариты' : weight_and_gab[1]
        }, f_json, ensure_ascii=False)
        return True
