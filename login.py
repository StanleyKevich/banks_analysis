'''
Created on 21 нояб. 2021 г.

@author: Arthur Stankevich
'''
from selenium import webdriver
from selenium.webdriver.common.by import By

LOG_IN = str(input("Логин: "))
PASSW = str(input("Пароль: "))

# class LogIn():
#     def __init__(self, driver, log_in, password, session_id):
#         self.
#         self.log_in = LOG_IN
#         self.password = PASSW
#         self.session_id = ""



def login():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://analizbankov.ru/login.php")
    login_field = driver.find_element(By.ID, "fld1")
    password_field = driver.find_element(By.ID, "fld2")
    login_field.send_keys(LOG_IN)
    password_field.send_keys(PASSW)
    driver.find_element(By.NAME,"login").click()
    # session_id = driver.session_id
    
# if __name__ == "__main__":
#     main()
