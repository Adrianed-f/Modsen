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

# Установка значения в LocalStorage
driver.execute_script("localStorage.setItem('myKey', 'Storage');")

# Получение значения из LocalStorage
value = driver.execute_script("return localStorage.getItem('myKey');")
print("Значение из LocalStorage:", value)

# Удаление значения из LocalStorage
driver.execute_script("localStorage.removeItem('myKey');")

# Закрытие браузера
driver.quit()