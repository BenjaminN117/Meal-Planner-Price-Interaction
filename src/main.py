'''
Product: Main script
Description:
Author: Benjamin Norman 2023
'''

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
        
        availableProducts = trolleyFunctions.query_product_database(productName=itemName, sort="price")
        productURL, supermarketName, price = trolleyFunctions.fetch_product_information(availableProducts)
        
        print(f"{productURL}, {supermarketName}, {price}")
        
        # forward these details to the Notion processor
        notionFunctions.update_page(value=productURL, dataType="url", pageID=pageID)
        notionFunctions.update_page(value=supermarketName, dataType="rich_text", pageID=pageID)
        notionFunctions.update_page(value=price, dataType="number", pageID=pageID)
        
if __name__ == "__main__":
     
    databaseID = "b6649294692740c280fb8f49cece0147"
    
    notionFunctions = processing(os.environ['NOTIONTOKEN'])
    trolleyFunctions = trolley_functions()
    
    
    # Fetch the dataset
    
    tableData = notionFunctions.fetch_data(databaseID=databaseID)
    extractedData = notionFunctions.extract_data(tableData)
    
    
    data_loop(extractedData)