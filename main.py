import time
from random import randrange
from bs4 import BeautifulSoup
import requests
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.42'
}

def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    page_count = int(soup.find('ul', class_='news-listing__pagination').find_all('a', class_='news-listing__pagination-link')[-1].text)
    
    articles_urls_list = []

    for page in range(1, page_count + 1):
        response = s.get(url=f'https://www.mk.ru/economics/{page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        article_urls = soup.find_all('a', class_='listing-preview__content')

        for url in article_urls:
            art_url = url.get('href')
            articles_urls_list.append(art_url)
        time.sleep(randrange(2, 5))
        print(f'Обработана {page}/{page_count}')

    with open('articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')
        print('OK!')
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)


def get_text(filename):
    with open(filename, 'r') as file:
        urls_list = [line.strip() for line in file.readlines()]
    
    s = requests.Session()
    result_data = []
    count = 0
    count_urls = len(urls_list)

    for url in urls_list[:50]:
        count += 1
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        article_title = soup.find('h1', class_='article__title').text.replace('\n', '')
        article_date = soup.find('time', class_='meta__text').get('datetime').split('T')[0]
        article_text = soup.find('div', class_='article__body').text.strip()

        result_data.append(
            {
                'article_title': article_title,
                'article_date': article_date,
                'article_text': article_text
            }
        )
        # print(f"{article_title}\n{article_date}\n{article_text}\n{50*'#'}")
        print(f'Обработано {count}/{count_urls} ссылок')
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    # get_articles_urls('https://www.mk.ru/economics/')
    get_text('articles_urls.txt')

if __name__ == '__main__':
    main()