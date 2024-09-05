#Code based on discogs_client python package.
from locale import currency
import discogs_client
import datetime, requests, re
from bs4 import BeautifulSoup

d = discogs_client.Client(
    'NotionDiscogs/1.0',
    consumer_key='', #consumer_key discogs
    consumer_secret='', #consumer_secret discogs
    token=u'', #token discogs
    secret=u'' #secret discogs
)


me = d.identity()

def returnWantlist():
    return me.wantlist

def returnCollection():
    return me.collection_folders[0].releases

def returnPriceInfo(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    section = soup.find('section', id='release-stats')
    if section is not None:
        ul = section.find_all('ul')
        span = ul[1].find_all('span')
        time = ul[1].find('time')
        if time is not None: 
            res = {
                "lastSold": time.text,
                "low": float(span[0].text.strip()[1:6]),
                "medium": float(span[1].text.strip()[1:6]),
                "high": float(span[2].text.strip()[1:6])
            }
        else: 
            res = {
                "lastSold": None,
                "low": None,
                "medium": None,
                "high": None
            }
    else: 
        res = {
            "lastSold": None,
            "low": None,
            "medium": None,
            "high": None
        }
    return res

def returnReleaseInfo(release):
    #set currentrelease
    currentRelease = release

    #create arrays
    artists = []
    for artist in currentRelease.artists:
        artists.append({"name": re.sub(",", "", artist.name) })
    labels = []
    for label in currentRelease.labels:
        labels.append({"name": label.name})
    genres = []
    for genre in currentRelease.genres:
        genres.append({"name":  re.sub(",", "", genre)})
    #convert dates to strings
    strYear = str(currentRelease.year)

    discogs = currentRelease.url

    album = currentRelease.title

    coverURL = currentRelease.images[0]['uri']
    iconURL = currentRelease.images[0]['uri150']

    res = {
        "release": release.id,
        "year": strYear,
        "artists": artists,
        "labels": labels,
        "genres": genres,
        "album": album,
        "discogs": discogs,
        "cover": coverURL,
        "icon": iconURL
        
    }

    return res

