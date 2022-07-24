from xmlrpc.client import Boolean
import requests
from bs4 import BeautifulSoup
import csv
import json
import re

class Parser():

    def __init__(self, number) -> None:
        self.validate_number(number)
        self.number = number


    @classmethod
    def validate_number(cls, number):
        result = re.match(r'^\w{2}\d{7}', number)
        if not result:
            print ("Номер не соответсвтует шаблону")
        

    def get_page_data(self) -> Boolean:
        params = {'tracking_number' : self.number}
        r = requests.get('https://litemf.com/ru/tracking',params=params)
        self.my_response = requests.get('https://litemf.com/ru/tracking',params=params).text
        if r.status_code == 200:
            try:
                self.page_data = BeautifulSoup(self.my_response, 'html.parser')
                self.final_page_data = list(self.page_data.find_all('li',attrs={"class": "checkpoint"}))
                self.date = [item.find(class_ = "date").get_text() for item in self.final_page_data]
                self.desc = [item.find(class_ = "description").get_text() for item in self.final_page_data ]
                self.name = [item.find(class_ = "name").get_text() for item in self.final_page_data ]
                self.weight, self.gab = self.page_data.find_all('dd')[0].get_text(), self.page_data.find_all('dd')[1].get_text().replace('\n','').replace(' ','')
                return True
            except:
                return False 
        else:
            raise ConnectionError


    def create_csv(self):
        with open("app/output_files/data.csv", mode="w", encoding='utf-8') as f:
            fields = ['Дата', 'Описание', 'Пункт назанчения', 'Вес', 'Габариты']
            file_writer = csv.writer(f, delimiter = ",")
            file_writer.writerow(fields)
            for row in range(len(self.date)):
                if row == 0:
                    file_writer.writerow([self.date[row], self.desc[row], self.name[row], self.weight, self.gab])
                else:
                    file_writer.writerow([self.date[row], self.desc[row], self.name[row]])


    def create_json(self):
        js = {
            'Даты': self.date,
            'Описания': self.desc,
            'Пункты назначения': self.name,
            'Вес': self.weight,
            'Габариты' : self.gab
        }
        with open('app/output_files/data.json', 'w') as f:
            json.dump(js, f, ensure_ascii=False)



b = Parser('LP2056555')
print(b.get_page_data())






