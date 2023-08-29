'''
Product: Main script
Description: Main script for runnung the price fetcher
Author: Benjamin Norman 2023
'''

import time
from Notion_Processing import processing
from Trolley_Interaction import trolley_functions
import os
import json


def data_loop(productsJSON):
    '''
    - Read in the JSON from the data extract
    - loop through all the product names and fetch the latest data for them
    - then update all of pages
    '''
    
    productsJSON = json.loads(productsJSON)
    
    for products in productsJSON["Products"]:
        itemName = products["Name"]
        pageID = products["Page ID"]
        category = products["Category"]

        # Fetch product info
        
        availableProducts = trolleyFunctions.query_product_database(productName=itemName, sort="relevant")
        
        # Iterate throught the list and store the results in a json object, then find the cheapest price in that JSON object and use that data
        availableProductsJSON = {"products": []}
        for product in availableProducts:
            tempJsonObj = {}
            try:
                productURL, supermarketName, price = trolleyFunctions.fetch_product_information(product)
                tempJsonObj["url"] = productURL
                tempJsonObj["price"] = price
                tempJsonObj["supermarketName"] = supermarketName
                
                availableProductsJSON["products"].append(tempJsonObj)
            except ValueError:
                pass
            
        # Find the cheapest product from this JSON obj
        # High starting number
        itemPrice = 1000000.0
        itemURL = ""
        itemSupermarketName = ""
        for item in availableProductsJSON["products"]:
            if float(item["price"]) < float(itemPrice):
                itemPrice = item["price"]
                itemURL = item["url"]
                itemSupermarketName = item["supermarketName"]
        
        # forward these details to the Notion processor
        notionFunctions.update_page(value=itemURL, dataType="url", pageID=pageID)
        notionFunctions.update_page(value=itemSupermarketName, dataType="rich_text", pageID=pageID)
        notionFunctions.update_page(value=itemPrice, dataType="number", pageID=pageID)
        
if __name__ == "__main__":
     
    databaseID = os.environ['DATABASEID']
    notionFunctions = processing(os.environ['NOTIONTOKEN'])
    
    while True:
        
        trolleyFunctions = trolley_functions()
        
        # Fetch the dataset
        
        tableData = notionFunctions.fetch_data(databaseID=databaseID)
        extractedData = notionFunctions.extract_data(tableData)
        
        data_loop(extractedData)
        
        print("Timer started")
        time.sleep(300)