'''
Notion API interactions
'''


import requests

def patch_requester(data, url, header):
    res = requests.patch(url, headers=header, json=data)
    return res.status_code, res.content

def post_requester(data, url, header):
    res = requests.post(url, headers=header, json=data)
    return res.status_code, res.content

def update_page_property(pageName, propertyName, value, propertyType, bearerToken):
    
    header = {
    "Authorization": f"Bearer {bearerToken}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
        }
    
    
    body = {
        "properties": {
            propertyName: {
            propertyType: value
            }
        }
    }
    
    url = f"https://api.notion.com/v1/pages/{pageName}"
    
    return patch_requester(body, url, header)

def update_rich_text_page_property(pageName, propertyName, value, bearerToken):
    
    header = {
    "Authorization": f"Bearer {bearerToken}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
        }
    
    body = {
        "properties": {
            propertyName: {
            "rich_text": [
                {
                "type": "text",
                "text": {
                    "content": value,
                    "link": None
                },
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default"
                },
                "plain_text": value,
                "href": None
                }
            ]
            }
        }
        }

    url = f"https://api.notion.com/v1/pages/{pageName}"
    
    return patch_requester(body, url, header=header)


def get_database_columns(databaseID, bearerToken):
    pass

def get_database_values(databaseID, pageSize, bearerToken):
    
    header = {
    "Authorization": f"Bearer {bearerToken}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
        }
    
    data = {"page_size":pageSize}
    
    url = f"https://api.notion.com/v1/databases/{databaseID}/query"
    
    return post_requester(url=url, data=data, header=header)
