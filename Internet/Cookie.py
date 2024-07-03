from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# путь к chromedriver
chromedriver_path = r'D:\chromedriver-win64\chromedriver.exe'

# Настройка браузера
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Открытие веб-страницы
driver.get('https://example.com')

# Установка значения в cookie
driver.add_cookie({'name': 'myCookie', 'value': 'Cookie'})

# Получение значения из cookie
cookie = driver.get_cookie('myCookie')
print("Значение из Cookie:", cookie)

# Удаление значения из cookie
driver.delete_cookie('myCookie')

# Закрытие браузера
driver.quit()