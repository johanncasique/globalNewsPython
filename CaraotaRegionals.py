import pip._vendor.urllib3.request
import pyrebase
from bs4 import BeautifulSoup
import schedule
import time
from requests.packages import urllib3

class Regional:
    # regionalDescriptionList = list()
    # regional_description_list
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

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    regionalResults = []
    regionalDescription = list()


    def getRegionalNews(self):

        regionalSite = "http://www.caraotadigital.net/category/regionales/"

        regionalRequest = urllib3.request(regionalSite, headers=self.hdr)
        # Query the website and return the html to the variable 'page'
        regionalPage = urllib3.request.urlopen(regionalRequest)

        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        regionalSoup = BeautifulSoup(regionalPage, "lxml")

        regionalCategory = (regionalSoup.find_all("article"))

        regionalList = []

        for regional in regionalCategory:

            title = regional.find("a").get("title")
            subtitle = regional.find("div", {"class": "entry-content"}).find('p').text
            img = ""
            news_link = regional.find("div", {"class": "entry-content"}).find("a").get("href")

            if regional.find("img"):
                print("regional image %s\n" % regional.find("img").get('src'))
                img = regional.find("img").get('src')
            elif regional.find('iframe'):
                print("regional image %s\n" % regional.find("iframe").get('src'))
                img = regional.find("iframe").get('src')
            else:
                print("regional image nil")

            detail_sub, body_detail = self.getRegionalDescription(news_link)

            regionalList.append(
                dict(title=title, subtitle=subtitle, img=img, detailTitle=detail_sub, detailBody=body_detail))

        self.db.child('regionals').child('news').remove()
        self.db.child("regionals").child("news").set(regionalList)



    def getRegionalDescription(self, national_url):

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
        time.sleep(30)
        schedule.every(10).seconds.do(self.getRegionalNews())
        print("I'm working...")

        # schedule.every(10).minutes.do(job)

        # schedule.every().hour.do(job)
        # schedule.every().day.at("10:30").do(job)
        while 1:
            schedule.run_pending()
            time.sleep(10)