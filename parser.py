import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/uk/car/infiniti/?page=1'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}
FILE = 'cars.csv'

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)

    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='content-bar')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('div', class_='head-ticket').get_text(strip=True),
            'link': item.find('a', class_='m-link-ticket').get('href'),
            'price': item.find('div', class_='price-ticket').get_text(strip=True),
            'Discription': item.find('div', class_='definition-data').get_text(),

        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена', 'Описание'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['Discription']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()   # Удаляем пробелы в начале и конце строки

    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, 'FILE.csv')
        print(f'Получено {len(cars)} автомобилей')
        os.startfile('FILE.csv')
    else:
        print('Error')


parse()