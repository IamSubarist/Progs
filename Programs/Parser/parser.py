from bs4 import BeautifulSoup
import requests

def get_data():
    url = 'https://oldl.ru/'

    response = requests.get(url=url)

    soup = BeautifulSoup(response.text, "lxml")

    page_count = int(soup.find("div", class_="pgntn-page-pagination-block").find_all("a")[-1].text)