'''
Created on 21 нояб. 2021 г.

@author: Arthur Stankevich
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import requests
from excelwork import save_to_excel, read_bankId
from datetime import datetime
# from tqdm import tqdm

headers = {
    'Accept': '*|*',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}
s = Service('C:/Programming/eclipse-workspace/banks_analysis/chromedriver.exe')
DRIVER = webdriver.Chrome(service=s)
current_date = datetime.now().date()


def login():
    log_in = str(input("Логин: "))
    passw = str(input("Пароль: "))
    DRIVER.get("https://analizbankov.ru/login.php")
    login_field = DRIVER.find_element(By.ID, "fld1")
    password_field = DRIVER.find_element(By.ID, "fld2")
    login_field.send_keys(log_in)
    password_field.send_keys(passw)
    DRIVER.find_element(By.NAME, "login").click()


def quarterdate(offset):
    first = [1, 2, 3, -11, -10, -9]
    second = [4, 5, 6, -6, -7, -8]
    third = [7, 8, 9, -3, -4, -5]
    d = datetime.now().month - offset * 3
    year = datetime.now().year
    if d <= 0:
        year -= 1
    if d in first:
        return f'{year}-01-01'
    elif d in second:
        return f'{year}-04-01'
    elif d in third:
        return f'{year}-07-01'
    else:
        return f'{year}-10-01'


def month_date(offset):
    if datetime.now().month - offset < 1:
        mon = datetime.now().month - offset + 12
        if mon < 10:
            month = f'0{mon}'
        else:
            month = mon
        year = datetime.now().year - 1
    else:
        mon = datetime.now().month - offset
        if mon < 10:
            month = f'0{mon}'
        else:
            month = mon
        year = datetime.now().year
    value_date = f'{year}-{month}-01'
    return value_date

# def name():


def bs_structure(bank_id):
    print('Балансовые данные...', end=" ")
    asset_list = []
    wa_list = []
    prov_list = []
    last_date_params = []
    DRIVER.get(f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=struktura_balansa')
    soup = BeautifulSoup(DRIVER.page_source, "lxml")
    codes = ['fold2-5', 'fold4-36', 'fold4-44', 'fold1-15', 'fold2-32', 'fold1-16', 'fold0-3']

    for par in codes:
        l_d_p = soup.find_all(id=par)
        for item in l_d_p:
            item_par = item.find(class_="refnum").get_text()
            param = int(''.join(item_par.split()))
            last_date_params.append(param)

    for qdate in reversed(range(5)):
        d = quarterdate(qdate)
        sel_date = DRIVER.find_element(By.ID, 'CurrentDate')
        select = Select(sel_date)
        select.select_by_value(d)
        time.sleep(.5)
        DRIVER.get(f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=struktura_balansa')
        soup = BeautifulSoup(DRIVER.page_source, "lxml")
        assets = soup.find_all(id="fold1-13")
        for item in assets:
            item_asst = item.find(class_="refnum").get_text()
            asset = int(''.join(item_asst.split()))
            asset_list.append(asset)
        work_ast = soup.find_all(id="fold0-2")
        for item in work_ast:
            item_wa = item.find(class_="refnum").get_text()
            wa = int(''.join(item_wa.split()))
            wa_list.append(wa)
        provisions = soup.find_all(id="fold1-16")
        for item in provisions:
            item_pr = item.find(class_="refnum").get_text()
            pr = int(''.join(item_pr.split()))
            prov_list.append(pr)
    print('OK')
    return last_date_params, asset_list, wa_list, prov_list


def ratings(bank_id):
    print('Позиции в рейтингах... ', end=' ')
    asset_rating = []
    DRIVER.get(f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=rating_pos')
    for offset in reversed(range(12)):
        if offset == 0 and datetime.now().day < 15:
            continue
        sel_date = DRIVER.find_element(By.ID, 'CurrentDate')
        select = Select(sel_date)
        try:
            select.select_by_value(month_date(offset))
            # print(month_date(offset))
            DRIVER.get(f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=rating_pos')
            soup = BeautifulSoup(DRIVER.page_source, "lxml")
            table = soup.find(class_='maxi_tab').find_all('td')
            asset_rating.append(int(table[8].get_text()))
            asset_rating.append(int(table[50].get_text()))
        except:
            None
        time.sleep(1)
    print('OK')
    return asset_rating


def basel3(bank_id):
    print('Капитал... ', end=' ')
    try:
        url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f123&year={datetime.now().year}&mon={datetime.now().month}'
        src = requests.get(url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        capital_table = soup.find(id="table134").find_all("td")
        cap = int(''.join(capital_table[5].get_text().split()))
    except:
        url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f123&year={datetime.now().year}&mon={datetime.now().month-1}'
        src = requests.get(url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        capital_table = soup.find(id="table134").find_all("td")
        cap = int(''.join(capital_table[5].get_text().split()))
    print('OK')
    return cap


def revenue(bank_id):
    print('Выручка... ', end=' ')
    rev_list = []
    profit_list = []
    for offset in range(5):
        url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f102&year={quarterdate(offset)[0:4]}&mon={quarterdate(offset)[5:7]}'
        time.sleep(1)
        src = requests.get(url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        rev_table = soup.find_all("td")
        rev_raw = str(rev_table[rev_table.index(next(r for r in rev_table if "19999" in r))+1])

        if offset == 0 or quarterdate(offset) == f'{datetime.now().year}-01-01' or offset == 4:
            try:
                prof_raw = str(rev_table[rev_table.index(next(r for r in rev_table if "02000" in r)) + 1])
                prof = int(''.join(prof_raw[4:len(prof_raw) - 5].split()))*-1
            except:
                prof_raw = str(rev_table[rev_table.index(next(r for r in rev_table if "01000" in r)) + 1])
                prof = int(''.join(prof_raw[4:len(prof_raw) - 5].split()))
            profit_list.append(prof)
        rev = int(''.join(rev_raw[4:len(rev_raw)-5].split()))
        rev_list.append(rev)
    print('OK')
    return rev_list, profit_list


def coefficients(bank_id):
    coef_list = []
    print('Нормативы ЦБ... ', end=' ')
    try:
        url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f135&year={datetime.now().year}&mon={datetime.now().month}'
        src = requests.get(url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        coef_table = soup.find(id="table134").find_all("td")
        coef = float(''.join(coef_table[3].get_text().split()))
        for offset in reversed(range(6)):
            if datetime.now().month-offset < 1:
                month = datetime.now().month-offset+12
                year = datetime.now().year-1
            else:
                month = datetime.now().month - offset
                year = datetime.now().year
            url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f135&year={year}&mon={month}'
            time.sleep(1)
            src = requests.get(url, headers=headers).text
            soup = BeautifulSoup(src, "lxml")
            coef_table = soup.find(id="table134").find_all("td")
            for c in range(3, 24, 3):
                coef = float(coef_table[c].get_text())
                coef_list.append(coef)
        print('OK')
        return coef_list
    except:
        for offset in reversed(range(6)):
            if datetime.now().month-offset < 1:
                month = datetime.now().month - offset + 12 - 1
                year = datetime.now().year-1
            else:
                month = datetime.now().month - offset - 1
                year = datetime.now().year
            url = f'https://analizbankov.ru/bank.php?BankId={bank_id}&BankMenu=f135&year={year}&mon={month}'
            time.sleep(1)
            src = requests.get(url, headers=headers).text
            soup = BeautifulSoup(src, "lxml")
            coef_table = soup.find(id="table134").find_all("td")
            for c in range(3, 24, 3):
                coef = float(coef_table[c].get_text())
                coef_list.append(coef)
        print('OK')
        return coef_list

login()

for bank, id_ in read_bankId().items():
    all_data = []
    print(f'Получение данных по {bank}')
    last_date_params, asset_list, wa_list, prov_list = bs_structure(id_)
    ratings_list = ratings(id_)
    capital = basel3(id_)
    rev_list, profit_list = revenue(id_)
    profit = profit_list[2]+profit_list[1]-profit_list[0]
    all_data.append(bank)
    all_data.append(current_date)
    all_data = all_data+last_date_params+rev_list+asset_list+wa_list+prov_list
    coef_list = coefficients(id_)
    all_data.append(capital)
    all_data.append(profit)
    all_data.extend(coef_list)
    all_data.extend(ratings_list)
    # print(all_data)
    formatted_name = bank.replace('"', '')
    file = f'{formatted_name}_{quarterdate(0)}'
    print(f'Сохраняем в файл {file}')
    save_to_excel(file, all_data)
    print(f'Данные по банку {bank} сохранены.\n\n')
    time.sleep(1)

DRIVER.close()

# if __name__ == "__main__":
#     main()
#
