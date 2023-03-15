import requests
from bs4 import BeautifulSoup as BS

r = requests.get("https://1wgsm.top/bets/live/18")
html = BS(r.content, 'html.parser')

for el in html.select(".tournament-list > .tournament-item"):
    title = el.select('.match-statistics > .match-time-passed')
    print(title[0].text)

# response = requests.get('https://1wgsm.top/bets/live/18')
# soup = BeautifulSoup(response.content, 'html.parser')
# data = soup.find('div').text
# print(data)
