import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
from pprint import pprint
import datetime
import json


'''Делаем запрос к искомой странице'''
def conn():
    url = 'https://spb.hh.ru/search/vacancy?text=python%2C+flask%2C+django&from=suggest_post&salary=&clusters=true&area=1&area=2&ored_clusters=true&enable_snippets=true'
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}

    res = requests.get(url=url, headers=fake_ua)
    soup = BeautifulSoup(res.text, 'lxml')
    # with open('index.html', 'w', encoding='utf8') as f:
    #     f.write(soup.text)
    # pprint(soup)
    return soup

def scrap_info():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y")
    req = conn()
    all_items = req.find_all('div', class_='vacancy-serp-item__layout')
    # pprint(all_items)
    job_data = []
    for item in all_items:
        name = item.find('a', class_='serp-item__title').text
        link = item.find('a', class_='serp-item__title').get('href')
        employer = item.find('a', class_="bloko-link bloko-link_kind-tertiary").text
        city = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        try:
            salary = item.find('span', class_='bloko-header-section-3').text
        except:
            salary = 'Заработная плата не указана'

        job_data.append(
            {
                'name': name,
                'link': link,
                'employer': employer,
                'city': city,
                'salary': salary
            }
        )
    with open(f'hh_python{cur_time}.json', 'w') as file:
        json.dump(job_data, file, indent=4, ensure_ascii=False)




def main():
    # conn()
    scrap_info()

if __name__ == '__main__':
    main()