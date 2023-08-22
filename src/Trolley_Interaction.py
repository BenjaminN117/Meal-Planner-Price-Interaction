'''
Product:
Description:
Author:
'''

import requests
from bs4 import BeautifulSoup
from requests.utils import requote_uri

class trolley_functions():
    def __init__(self):
        pass

    def query_product_database(self, productName, sort):
        '''
        productName - Name of the product you want to query for
        sort - Sorting value, either by "relevant" or by "price"
        '''
        productsURLList = []
        url = self.url_encoder(f"https://www.trolley.co.uk/search/?NR=1&q={productName}&order={sort}")
        
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # TODO Combine this into a single line
        results = soup.find(id="search-results")
        rawProductHTML = results.find("div", class_="tile").find("div", class_="products-grid-cn").find("div", class_="products-grid").find_all("div", class_="product-item")

        for job_element in rawProductHTML:
            for a in job_element.find_all('a', href=True):
                productsURLList.append(f"https://trolley.co.uk{a['href']}")
                
        return productsURLList
        
        
    def fetch_product_information(self, productsURLList):
        
        productPage = requests.get(productsURLList[0])

        productPageSoup = BeautifulSoup(productPage.content, "html.parser")

        results = productPageSoup.find("body", class_="_JS-body").find("div", class_= "parent product-profile").find_all("div", class_= "tile")
        for element in results:
            try:
                output = element.find("div", class_ = "comparison-table").find("div", class_= "collapse").find("div", class_ = "_item").find_all("div")
                # Find Price and Supermarket
                for divElement in output:
                    try:
                        productPrice = divElement.find("div", class_= "_price").find("b").text
                    except AttributeError:
                        pass
                    try:
                        supermarketName = divElement.find('svg').find('title').text
                    except AttributeError:
                        pass
            except AttributeError:
                pass
            
        if 'productPrice' in locals() and 'supermarketName' in locals():
                        
            return productsURLList[0], supermarketName, productPrice.replace("£", '')
        else:
            return productsURLList[0]
    
    def url_encoder(self, url):
        return requote_uri(url)