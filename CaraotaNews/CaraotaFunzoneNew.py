import urllib3
import pyrebase
from bs4 import BeautifulSoup
import schedule
import time 
import json
import re 
from CaraotaNews.CaraotaCommons import CaraotaCommons
import uuid

class CaraotaFunZoneNews:
    ARTICLES_DIV_ClASS_NAME = "tdb_module_loop_2"
    ARTICLES_DIV_KEY = "div"

    firebase = pyrebase.initialize_app(CaraotaCommons.configFirebase)
    http = urllib3.PoolManager()
    req = http.request('GET', CaraotaCommons.funZoneNews, 
    headers=CaraotaCommons.headerRequest)

    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(req.data, "html.parser")
    # print(soup.prettify())

    funNewsBody = soup.find_all(ARTICLES_DIV_KEY, ARTICLES_DIV_ClASS_NAME)

    results = []

    # Get reference to the database service
    db = firebase.database()

    def getFunNews(self):
        funNewsList = []

        for funNews in self.funNewsBody:
            title = funNews.find("h3", "entry-title").next.get("title")
            subtitle = funNews.find("div", {"class": "td-excerpt"}).next
            news_link = funNews.find("h3", "entry-title").find("a").get("href")
            newsDate = funNews.find("time", "entry-date").get("datetime")

            img = ""
            if funNews.find("a", "td-image-wrap"):
                img_temp = funNews.find("a", "td-image-wrap").next.get('style')
                img = re.search("(?P<url>https?://[^\s]+)", img_temp).group("url")
            else:
                print("redNew image nil")
                img = "NIL"
            
            funNewsList.append(
                dict(title=title, 
                subtitle=subtitle,  
                img=img, 
                newsDate=newsDate, 
                newsLink=news_link,
                id=str(uuid.uuid4())
                )
            )
        self.db.child("funNews").child("news").remove()
        self.db.child("funNews").child("news").set(funNewsList)