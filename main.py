import requests
import csv
from bs4 import BeautifulSoup as BS

BASE_URL = 'https://svetofor.info/sotovye-telefony-i-aksessuary/vse-smartfony/smartfony-s-podderzhkoy-4g-ru/'



def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    phones = soup.find_all('div', class_ = 'ty-column4')

    list_data = []

    for phone in phones:
        try:
            title = phone.find('a', class_ ='product-title').text.strip()
        except:
            title = ''
        try:
            image = phone.find('img', class_='ty-pict').get('data-ssrc')
        except:
            image = ''
        try:    
            price = phone.find('span', class_ = 'ty-price-update').text
        except:
            price = ''

        list_data.append({
            'title': title,
            'price': price,
            'image': image
            })
    return list_data

def write_csv(data):
    with open('phones.csv', 'a') as file:
        names = ['title', 'price', 'image']
        write = csv.DictWriter(file, delimiter = ',', fieldnames=names)
        write.writerows(data)


def main():
    for i in range(1,14):
        url = BASE_URL + f'page-{i}/'
        
        html = get_html(url)
        soup = get_soup(html)
        data = get_data(soup)
        write_csv(data)

        print(f'спарсили - {i} страницу')
if __name__ == '__main__':
    main()