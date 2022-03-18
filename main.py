from os import write
import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    art_names = soup.find_all('a', class_='art__name__href')
    art_authors = soup.find_all('div', class_='art__author')
    rating = soup.find_all('div', class_='inline-elem bottomline-rating')
    count = soup.find_all('div', class_='bottomline-rating-count')
    for i in range(0, len(art_authors)):

        print(art_names[i].get('title'))
        print(art_authors[i].find('a').get('title'))
        print(rating[i].text)
        print(count[i].text)
        catalog.append({
            'name': art_names[i].get('title'),
            'author': art_authors[i].find('a').get('title'),
            'rating': rating[i].text,
            'number of reviews': count[i].text,
        })
    return catalog


def save_file(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название', 'Авторы', 'Рейтинг', 'Количество отзывов'])
        for item in items:
            writer.writerow([item['name'], item['author'], item['rating'], item['number of reviews']])


def parse():
    for URL in ['https://www.litres.ru/klassicheskaya-literatura/', ]:
        html = get_html(URL)
        if html.status_code == 200:
            html = get_content(html.text)
        else:
            print('Error')
        filename = 'nsuparse.csv'
        save_file(html, filename)


parse()
