import requests
from bs4 import BeautifulSoup
import pandas as pd


def collect_urls():
    try:
        
        urls = ['https://www.avito.ma/fr/maroc/ordinateurs_portables-%C3%A0_vendre',
                'https://www.avito.ma/fr/maroc/ordinateurs_portables-%C3%A0_vendre?o=2',
                'https://www.avito.ma/fr/maroc/t%C3%A9l%C3%A9phones-%C3%A0_vendre',
                'https://www.avito.ma/fr/maroc/t%C3%A9l%C3%A9phones-%C3%A0_vendre?o=2',
                'https://www.avito.ma/fr/maroc/ordinateurs_bureau-%C3%A0_vendre',
                'https://www.avito.ma/fr/maroc/ordinateurs_bureau-%C3%A0_vendre?o=2',
                'https://www.avito.ma/fr/maroc/tablettes-%C3%A0_vendre',
                'https://www.avito.ma/fr/maroc/tablettes-%C3%A0_vendre?o=2']

        data_urls = pd.DataFrame(columns=['url'])

        for url in urls:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            for div in soup.find_all('div', class_='oan6tk-0 hEwuhz'):
                print("LInk")
                url_item = div.find('a')['href']
                print(url_item)
                data_urls = data_urls.append({'url' : url_item}, ignore_index=True)
                
        data_urls.to_csv('urls_avito.csv', index=False)
    except Exception as e:
        print(e)
            