import json
from flask import render_template
from flask import Flask
import pandas as pd
from collect_data import *
from collect_item_data import *
from os import path


def read_csv():
    return pd.read_csv('products_data.csv')


app = Flask('main')

PRODUCTS_DF = read_csv()

@app.route('/')
def hello():
    return render_template('index.html', results=pd.DataFrame())

@app.route('/<sub_cat>')
def get_products(sub_cat):
    data = PRODUCTS_DF.loc[PRODUCTS_DF['subcat'] == sub_cat]
    
    return render_template('index.html', results = data[['title', 'hd_images', 'price', 'id']])


@app.route('/product/<id>')
def get_product_details(id):
    data = PRODUCTS_DF.loc[PRODUCTS_DF['id'] == int(id)]
    data = data.iloc[0].to_dict()
    data['phone'] = "0"+str(data['phone']).replace('.0', '')
    return render_template('details.html', result = data)

if __name__ == '__main__':
    
    if path.exists('urls_avito.csv') == False:
        collect_urls()
        collect_items()
        
    app.run(use_reloader=True)
