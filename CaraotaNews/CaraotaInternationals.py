import urllib.request
import pyrebase
from bs4 import BeautifulSoup
import schedule
import time
from CaraotaNews.CaraotaCommons import CaraotaCommons


class caraota_international:
    site = "https://www.lapatilla.com/site/secciones/internacionales/"

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    # config firebase
    config = {
        "apiKey": "AIzaSyAQWkofqy88scr-ckLlT-jSg3jIn4bYrTg",
        "authDomain": "venezuelanews-7a888.firebaseapp.com",
        "databaseURL": "https://venezuelanews-7a888.firebaseio.com",
        "storageBucket": "projectId.appspot.com"
    }

    firebase = pyrebase.initialize_app(CaraotaCommons.configFirebase)

    req = urllib.request.Request(CaraotaCommons.internationalEndpoint, headers=CaraotaCommons.headerRequest)

    # Query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(req)

    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")
    # print(soup.prettify())

    nationalsCategory = soup.find_all("article")

    nationalDescriptionList = list()

    results = []

    # Get reference to the database service
    db = firebase.database()
    # Pass the data to the database
    # results.append(db.child("nationals").child("news").set(nationalList))

    def getInternationalsNews(self):

        national_list = []

        for national in self.nationalsCategory:

            title = national.find("a").get("title")
            subtitle = national.find("div", {"class": "entry-content"}).find('p').text
            img = ""
            news_link = national.find("div", {"class": "entry-content"}).find("a").get("href")

            if national.find("img"):
                print("national image %s\n" % national.find("img").get('src'))
                img = national.find("img").get('src')
            elif national.find('iframe'):
                print("national image %s\n" % national.find("iframe").get('src'))
                img = national.find("iframe").get('src')
            else:
                print("national image nil")

            detail_sub, body_detail = self.getNationalDescription(news_link)

            national_list.append(
                dict(title=title, subtitle=subtitle, img=img, detailTitle=detail_sub, detailBody=body_detail))

        self.db.child('internationals').child('news').remove()
        self.db.child("internationals").child("news").set(national_list)


    # Get Description news
    def getNationalDescription(self, national_url):

        req = urllib.request.Request(national_url, headers=self.hdr)

        # Query the website and return the html to the variable 'page'
        page = urllib.request.urlopen(req)

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

