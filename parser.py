'''
Created on 20 нояб. 2021 г.

@author: Arthur Stankevich
'''

from bs4 import BeautifulSoup
import requests

data = {
    'BankId': 'centrocredit-121',
    'BankMenu': 'struktura_balansa',
    }
url = "https://analizbankov.ru/bank.php?BankId=centrokredit-121&BankMenu=struktura_balansa"
# url = "https://analizbankov.ru/bank.php"

headers = {
    'Accept': '*|*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=2b5ooqj8jcr00jkq6uq9h3c256; forum_cookie_581a9d=NjAwOXxlYzUyODViNjk0NTdjMGU5Yzk0NmQ1MTY3OTNmYjU5MjA4ODE5NTRhfDE2Mzg2MjQyMTB8ZTc3YWM4OWI0NjM1OWYzZTI1Yzc3NzIwYjZkOTM2OGU5ZjU4M2M5ZQ%3D%3D',
    'DNT': '1',
    'Host': 'analizbankov.ru',
    'Referer': 'https://analizbankov.ru/bank.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }
req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w") as file:
    file.write(src)

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "html5lib")

securities = soup.find_all(id="fold2-5")

for item in securities:
    item_sec = item.find(class_="refnum").get_text()
    print(item_sec)
    # print(f"{item_text}: {item_regn}")

overdue_le = soup.find_all(id="fold4-36")
for item in overdue_le:
    item_ovle = item.find(class_="refnum").get_text()
    print(item_ovle)

overdue_fe = soup.find_all(id="fold4-44")
for item in overdue_fe:
    item_ovfe = item.find(class_="refnum").get_text()
    print(item_ovfe)