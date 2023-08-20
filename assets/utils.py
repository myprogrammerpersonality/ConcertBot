import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Event(BaseModel):
    title: str
    image: str
    date_iran: str
    date_world: str


def scrape_webpage():
    url = 'https://www.darkoob.ir/tc/Concert/tehran'  # Replace with the URL of the web page you want to scrape
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    events_div = soup.find_all('div', class_="allmode_box allmode-default")[0]
    events_list = events_div.find_all('div', class_="allmode_item")
    results = []
    for event in events_list:
        title = event.find('h4', class_='allmode_title').find('a').text.strip()
        image = event.find('div', class_='allmode_img').find('img')['src']
        date = event.find('div', class_='allmode_text').find('div', class_='clearb').find('div', class_="event_detail").find('span', 'dt1').text
        date_iran = date.strip().split('\n')[0].strip()
        date_world = date.strip().split('\n')[-1].strip()

        result = Event(title=title, image=image, date_iran=date_iran, date_world=date_world)
        results.append(result)
    
    print(results)
    return results