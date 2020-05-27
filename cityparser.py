from typing import Dict, List, Any

from bs4 import BeautifulSoup
import requests


def parse(city: str):
    URL = 'https://sinoptik.ua/погода-' + city.lower()
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/81.0.4044.138 Safari/537.36'
    }

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='tabsContentInner')
    weather: List[Dict[str, Any]] = []

    for item in items:
        weather.append({
            'temp': item.find('p', class_='today-temp').get_text(strip=True),
            'description': item.findAll('div', class_='description'),
            'feels like': item.findAll('td', class_='cur')[3].get_text(strip=True),
            'pressure': item.findAll('td', class_='cur')[4].get_text(strip=True),
            'humidity': item.findAll('td', class_='cur')[5].get_text(strip=True),
            'wind': item.findAll('td', class_='cur')[6].get_text(strip=True),
        })

    try:
        if(len(weather[0]['description']) == 3):
            weather[0]['description'] = weather[0]['description'][1].get_text(strip=True) + '\n'\
                                        + weather[0]['description'][0].get_text(strip=True).capitalize() + '.'
        else:
            weather[0]['description'] = weather[0]['description'][0].get_text(strip=True)
    except IndexError:
        return None
    return weather
