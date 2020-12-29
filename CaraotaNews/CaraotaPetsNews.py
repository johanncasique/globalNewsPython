import urllib3
import pyrebase
from bs4 import BeautifulSoup
import schedule
import time 
import json
import re 
from CaraotaNews.CaraotaCommons import CaraotaCommons
import uuid

class CaraotaPetsNews:
    ARTICLES_DIV_ClASS_NAME = "tdb_module_loop_2"
    ARTICLES_DIV_KEY = "div"
    
    firebase = pyrebase.initialize_app(CaraotaCommons.configFirebase)
    http = urllib3.PoolManager()
    req = http.request('GET', CaraotaCommons.petsNewsEndpoint,
     headers=CaraotaCommons.headerRequest)

    # Query the website and return the html to the variable 'page'
    #jsonPage = json.loads(req.data.decode('utf-8'))

    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(req.data, "html.parser")
    # print(soup.prettify())

    petsNewsCategory = soup.find_all(ARTICLES_DIV_KEY, ARTICLES_DIV_ClASS_NAME)

    results = []

    # Get reference to the database service
    db = firebase.database()

    def getPetsNews(self):
        petsNews = []
        
        for news in self.petsNewsCategory:
            title = news.find("h3", "entry-title").next.get("title")
            subtitle = news.find("div", {"class": "td-excerpt"}).next
            news_link = news.find("h3", "entry-title").find("a").get("href")
            newsDate = news.find("time", "entry-date").get("datetime")

            img = ""
            if news.find("a", "td-image-wrap"):
                img_temp = news.find("a", "td-image-wrap").next.get('style')
                img = re.search("(?P<url>https?://[^\s]+)", img_temp).group("url")
            else:
                print("redNew image nil")
                img = "NIL"

            petsNews.append(
                dict(title=title, 
                subtitle=subtitle,  
                img=img, 
                newsDate=newsDate, 
                newsLink=news_link,
                id=str(uuid.uuid4()))
                )
        self.db.child("petsNews").child("news").remove()
        self.db.child("petsNews").child("news").set(petsNews)
