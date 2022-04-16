import csv
from bs4 import BeautifulSoup
import requests

CSV = 'houses.csv'
HOST = 'https://spb.cian.ru'
URL = 'https://spb.cian.ru/kupit-dom/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60 '
}


def get_html(url, params=''):
    res = requests.get(url, headers=HEADERS, params=params)
    res.raise_for_status()
    return res


def get_content(html_):
    soup = BeautifulSoup(html_, 'html.parser')
    items = soup.find_all('div', class_='_93444fe79c--card--ibP42')
    houses = []
    for item in items:
        houses.append({
            "title": item.find('div', class_='_93444fe79c--row--kEHOK').get_text(strip=True),
            "price": item.find('div', class_='_93444fe79c--container--aWzpE').get_text(strip=True),
            "house_img": HOST + item.find('img', class_='_93444fe79c--image--ddBFT').get('src'),
            'link_': HOST + item.find('a', class_='_93444fe79c--link--eoxce').get('href'),

        })
    return houses


def save_data(items, path):
    with open(path, 'w', newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['House info', 'Price', 'Link', 'Image'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link_'], item['house_img']])


def parser():
    PAGINATION = input("How many pages you like to parse? ")
    PAGINATION = int(PAGINATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        houses = []
        for page in range(1, PAGINATION+1):
            print(f'Parsing of page number {page} in progress.')
            html = get_html(URL, params={'p': page})
            houses.extend(get_content(html.text))
            save_data(houses, CSV)

    else:
        print('Something wrong')

parser()

    #

#
# html = get_html(URL)
# pprint(get_content(html.text))
