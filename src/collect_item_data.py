import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime


def getProperDict(theDict, startWith):
    d = {key:val for key, val in theDict.items() if key.startswith(startWith.capitalize())}
    return  list(d.values())[0]
    
def collect_data(url):
    item = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        js_script = json.loads(soup.find(id='__NEXT_DATA__').get_text())
        product_data, seller_data = js_script['props']['pageProps']['componentProps']['targetingArguments'], js_script['props']['pageProps']['apolloState']
    except:
        js_script = None
    
    if js_script is None:
        return None
    
    try:
        item['city'] = product_data['city']
    except:
        item['city'] = ''
        
    try:
        item['subcat'] = product_data['subcat']
    except:
        item['subcat'] = ''
        
    try:
        item['title'] = product_data['title']
    except:
        item['title'] = ''
        
    try:    
        item['type'] = product_data['type']
    except:
        item['type'] = ''
        
    try:
        item['price'] = product_data['price']
    except:
        item['price'] = ''
    
    d1, d2 = getProperDict(seller_data, 'seller'), getProperDict(seller_data, 'ad')
    
    try:
        item['sellerName'] = d1['name']
    except:
        item['sellerName'] = ''
        
    try:
        item['website'] = d1['website']
    except:
        item['website']
    
    try:
        item['description'] = d2['description']
    except:
        item['desctiption'] = ''
        
    try:
        item['phone'] = d2['phone']
    except:
        item['phone'] = ''
        
    try:
        item['date'] = d2['listTime']['raw']
    except:
        item['date'] = ''
        
    images = []
    
    for img in d2['images']:
        images.append(img['hdSrc'])
    
    try:
        item['hd_images'] = images[0]
    except:
        item['hd_images'] = ''
        
    return item
    

def collect_items():
    df = pd.read_csv('urls_avito.csv')
    df_products = pd.DataFrame(columns=['id', 'city', 'subcat', 'title', 'type', 'price', 'sellerName', 'website', 'description', 'phone', 'date', 'hd_images'])
    x = 0
    start_date = datetime.now()
    for url in df['url']:
        print(url)
        try:
            item = collect_data(url)
            if item is not None:
                x=x+1
                item['id']=x
                df_products = df_products.append(item, ignore_index=True)
        except Exception as e:
            print(e)

    print('#'*60)
    ending_time = datetime.now()
    print(ending_time - start_date)

    df_products.to_csv('products_data.csv', index=False)


