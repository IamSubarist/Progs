from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib

chromedriver = 'C:\chromedriver\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

browser.get('https://www.flashscore.com/basketball/')
# Получение HTML-содержимого
requiredHtml = browser.page_source

soup = BeautifulSoup(requiredHtml, 'html5lib')
table = soup.findChildren('main-table')

rows = table.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.text
        print (value)