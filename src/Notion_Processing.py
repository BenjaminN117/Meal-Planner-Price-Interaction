import json
from NotionAPI import functions
import os

class processing():
    def __init__(self, NotionBearerToken):
        self.extractedData = {"Products": []}
        self.NotionToken = NotionBearerToken
        
    def fetch_data(self, databaseID):
        '''
        Fetches the database values from the database ID using Notion API
        '''
        # Page size is set to the maximum
        response = functions.get_database_values("b6649294692740c280fb8f49cece0147", 100, self.NotionToken)
        
        return response[1].decode('utf-8')
    
    def extract_data(self, data):
        
        '''
        Extract the data into so it fits into the new dict
        '''
        
        data = json.loads(data)
        
        for object in data["results"]:
            temporaryDict = {}
            try:
                temporaryDict["Category"] = object["properties"]["Category"]["select"]["name"]
            except TypeError:
                temporaryDict["Category"] = ""
            for item in object["properties"]["Item Name"]["title"]:
                temporaryDict["Name"] = item["plain_text"]

            temporaryDict["Page ID"] = self.pageID_extraction(object["url"])
            
            self.extractedData["Products"].append(temporaryDict)
        
        json_string = json.dumps(self.extractedData, indent=2)    
        return json_string

    def pageID_extraction(self, url):
        '''
        Extracts the Page ID from the Page URL
        '''
        return url.split("-")[-1]
    
    def update_page(self, value, dataType, pageID):
        
        if dataType == "url":
            functions.update_page_property(pageName=pageID, propertyName="Product URL", value=value, propertyType="url", bearerToken=self.NotionToken)
        elif dataType == "rich_text":
            functions.update_rich_text_page_property(pageName=pageID, propertyName="Supermarket", value=value, bearerToken=self.NotionToken)
        elif dataType == "number":
            print(functions.update_page_property(pageName=pageID, propertyName="Price", value=value, propertyType="number", bearerToken=self.NotionToken))
        else:
            return "unknown data type"
        

if __name__ == "__main__":
    
    pass
    