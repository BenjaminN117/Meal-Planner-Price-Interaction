'''
Product: Trolley Interactions
Description: Scrapes data from trolley.co.uk
Author: Benjamin Norman 2023
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
        
        
    def fetch_product_information(self, productsURL):
        
        productPage = requests.get(productsURL)

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
            if productPrice.count("£") > 1:
                # Some products have more than one price, formatted like this -> £3.00 £̶3̶.̶5̶0̶
                productPrice = productPrice.split(" ")[0]
            return productsURL, supermarketName, productPrice.replace("£", '')
        else:
            return productsURL
    
    def url_encoder(self, url):
        return requote_uri(url)