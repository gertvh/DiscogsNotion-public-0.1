from operator import truediv
from discogs import *
from notion import *
from dateutil import parser


collectionDB = '' #ID for collection db in notion
wantlistDB = '' #ID for wantlist db in notion

##First iterate the collections
#get Collections in both Discogs and Notion
discogsCollection = returnCollection()

startCursor = "initial"
has_more = True
NotionCollection = []
while(has_more):
    res = returnNotionDB(collectionDB,startCursor)
    NotionCollection = NotionCollection + res["results"]
    startCursor = res["next_cursor"]
    has_more = res["has_more"]

for item in discogsCollection:
    match = False
    i = 0
    while i < len(NotionCollection):
        if item.id == NotionCollection[i]["properties"]["release_id"]["number"]:
            match = True
            break
        i += 1    
    if match == False:
        releaseInfo = returnReleaseInfo(item.release)
        priceInfo = returnPriceInfo(releaseInfo["discogs"])
        properties = setProperties(releaseInfo["release"],releaseInfo["album"],releaseInfo[ "artists"], releaseInfo["year"], item.date_added.date(),releaseInfo["genres"],releaseInfo["labels"],priceInfo["lastSold"],priceInfo["low"],priceInfo["medium"],priceInfo["high"],releaseInfo["discogs"])
        createPage(collectionDB,properties,releaseInfo["cover"],releaseInfo["icon"])

## Next do the same for wantlist
##Some extra comments
discogsWantlist = returnWantlist()
startCursor = "initial"
has_more = True
NotionWantlist = []
while(has_more):
    res = returnNotionDB(wantlistDB,startCursor)
    NotionWantlist = NotionWantlist + res["results"]
    startCursor = res["next_cursor"]
    has_more = res["has_more"]

for item in discogsWantlist:
    match = False
    i = 0
    while i < len(NotionWantlist):
        if item.id == NotionWantlist[i]["properties"]["release_id"]["number"]:
            match = True
            break
        i += 1    
    if match == False:
        releaseInfo = returnReleaseInfo(item.release)
        priceInfo = returnPriceInfo(releaseInfo["discogs"])
        properties = setProperties(releaseInfo["release"],releaseInfo["album"],releaseInfo[ "artists"], releaseInfo["year"], parser.parse(item.data["date_added"]),releaseInfo["genres"],releaseInfo["labels"],priceInfo["lastSold"],priceInfo["low"],priceInfo["medium"],priceInfo["high"],releaseInfo["discogs"])
        createPage(wantlistDB,properties,releaseInfo["cover"],releaseInfo["icon"])