import urllib3
import pyrebase
from bs4 import BeautifulSoup
import schedule
import time
import json
import re
from CaraotaNews.CaraotaCommons import CaraotaCommons
import uuid


class CaraotaNationals:
    ARTICLES_DIV_ClASS_NAME = "tdb_module_loop_2"
    ARTICLES_DIV_KEY = "div"
    
    firebase = pyrebase.initialize_app(CaraotaCommons.configFirebase)
    http = urllib3.PoolManager()
    req = http.request('GET', CaraotaCommons.nationalEndpoint, headers=CaraotaCommons.headerRequest)

    # Query the website and return the html to the variable 'page'
    #jsonPage = json.loads(req.data.decode('utf-8'))

    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(req.data, "html.parser")
    # print(soup.prettify())

    nationalsCategory = soup.find_all(ARTICLES_DIV_KEY, ARTICLES_DIV_ClASS_NAME)

    nationalDescriptionList = list()

    results = []

    # Get reference to the database service
    db = firebase.database()
    # Pass the data to the database
    # results.append(db.child("nationals").child("news").set(nationalList))

    def getNationalNews(self):

        national_list = []

        for national in self.nationalsCategory:

            title = national.find("h3", "entry-title").next.get("title")
            subtitle = national.find("div", {"class": "td-excerpt"}).next
            news_link = national.find("h3", "entry-title").find("a").get("href")
            newsDate = national.find("time", "entry-date").get("datetime")

            img = ""
            if national.find("a", "td-image-wrap"):
                img_temp = national.find("a", "td-image-wrap").next.get('style')
                img = re.search("(?P<url>https?://[^\s]+)", img_temp).group("url")
            else:
                print("national image nil")
                img = "NIL"

            national_list.append(
                dict(title=title, 
                subtitle=subtitle,  
                img=img, 
                newsDate=newsDate, 
                newsLink=news_link,
                id=str(uuid.uuid4()))
                )
        #national_remote = self.db.child('nationals').child('news').get()
        self.db.child('nationals').child('news').remove()
        self.db.child("nationals").child("news").set(national_list)


    # Get Description news
    def getNationalDescription(self, national_url):

        req = urllib3.request.Request(national_url, headers=self.hdr)

        # Query the website and return the html to the variable 'page'
        page = urllib3.request.urlopen(req)

        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        nationalSoup = BeautifulSoup(page, "html.parser")

        nationalsCategoryBody = nationalSoup.find_all("article")
        nationalDescriptionString = nationalsCategoryBody[0].find_all("div", {'class': 'entry-content'})

        for nationalText in nationalDescriptionString:
            for text in nationalText.find_all("ul", {"class": "essb_links_list"}):
                print(text)
                text.decompose()
            return nationalText.find("h3").text, str(nationalText)

    def job(self):
        time.sleep(10)
        print("I'm working...")
        schedule.every(5).seconds.do(self.getNationalNews())

        while True:
            schedule.run_pending()
            time.sleep(1)