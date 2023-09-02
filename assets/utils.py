import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Event(BaseModel):
    title: str
    title_link: str
    image: str
    date_iran: str
    date_world: str
    done: bool

    def __str__(self):
        return f"<a href='{self.title_link}'>{self.title}</a>\n{self.date_iran}\n{self.date_world}"


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
        title_link = event.find('h4', class_='allmode_title').find('a')['href']
        image = event.find('div', class_='allmode_img').find('img')['src']
        date = event.find('div', class_='allmode_text').find('div', class_='clearb').find('div', class_="event_detail").find('span', 'dt1').text
        date_iran = date.strip().split('\n')[0].strip()
        date_world = date.strip().split('\n')[-1].strip()
        done = False
        for detail in event.find('div', class_='allmode_text').find_all('div', class_='event_detail'):
            data = detail.find('span', 'dt1').find('font', attrs={'color': 'red'})
            if data:
                if data.text.strip() == "برگزار شده":
                    done = True

        result = Event(title=title, title_link=title_link, image=image, date_iran=date_iran, date_world=date_world, done=done)
        results.append(result)
    
    print(results)
    return results
