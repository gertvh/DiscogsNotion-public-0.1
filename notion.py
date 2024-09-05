from contextlib import nullcontext
import requests, json, datetime
#set variables and headers for notion
token = '' #authentication token notion -> probably needs to be updated, this was configured with notion version 2022-02-22
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22",
    "Content-Type":"application/json"
}

def setProperties(releaseID,album,artists,year,dateAdded,genres,labels,lastSold,low,median,high,discogs):
    #convert parameters to strings
    strDdateAdded = '{:%Y-%m-%d}'.format(dateAdded)
    strYear = str(year)
    if lastSold is not None: 
        properties = {
            "release_id": {
            "number": releaseID
            },
            "Date Added": {
                "date": {
                    "start": strDdateAdded
                }
            },
            "Year": {
                "rich_text": [{ "type": "text", "text": { "content": strYear } }]    },
            "Artist(s)": {
                "multi_select": artists
            },
            "Label": {
                "multi_select": labels
            },
            "Album": {
                "title": [
                    {
                        "text": {
                            "content": album,
                        }
                    }
                ]
            },
            "Date Last Sold": {
                "rich_text": [{ "type": "text", "text": { "content": lastSold } }]    },
            "Lowest Price": {
                "number": low
            },
            "Median Price": {
                "number": median
            },
            "Highest Price": {
                "number": high
            },
            "Discogs": {
                "url": discogs
            },
            "Genres": {
                "multi_select": genres
            }
        }
    else:
        properties = {
            "release_id": {
            "number": releaseID
            },
            "Date Added": {
                "date": {
                    "start": strDdateAdded
                }
            },
            "Year": {
                "rich_text": [{ "type": "text", "text": { "content": strYear } }]    },
            "Artist(s)": {
                "multi_select": artists
            },
            "Label": {
                "multi_select": labels
            },
            "Album": {
                "title": [
                    {
                        "text": {
                            "content": album,
                        }
                    }
                ]
            },
            "Discogs": {
                "url": discogs
            },
            "Genres": {
                "multi_select": genres
            }
        }
    return properties

def returnNotionDB(databaseId,cursor):
    readUrl =  f"https://api.notion.com/v1/databases/{databaseId}/query"
    data = {"start_cursor": cursor
    }
    jsonData = json.dumps(data)
    if cursor == "initial":
        res = requests.request("POST", readUrl, headers=headers)
    else:
        res = requests.request("POST", readUrl, headers=headers,data=jsonData)
    data = res.json()
    print(res.status_code)
    return data

def createPage(databaseId, properties, cover, icon):
    createUrl = ' https://api.notion.com/v1/pages'
    newPageData = {
         "parent": { "database_id": databaseId },
         "properties": properties,
         "cover": {
		    "external": {
			    "url": cover
		    }
        },
        "icon": {
            "external": {
			    "url": icon
		    }
        }
    }
    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)
    if(res.status_code != 200):
        print(res.text)
        print(data)

def prepareSalesProperties(lastSold, low, median, high):
    properties = {
        "Date Last Sold": {
            "rich_text": [{ "type": "text", "text": { "content": lastSold } }]    },
        "Lowest Price": {
            "number": low
        },
        "Median Price": {
            "number": median
        },
        "Highest Price": {
            "number": high
        }
    }


def updatePage(properties, page_id):
    updateURL = f"https://api.notion.com/v1/pages/{page_id}"
    updatePageData = {
        "properties": properties
    }
    data = json.dumps(updatePageData)
    res = requests.request("PATCH", updateURL, headers=headers, data=data)


   

