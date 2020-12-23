import urllib.request
from bs4 import BeautifulSoup

class CaraotaScarping:

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    caraotaURL = "http://www.caraotadigital.net/"


    def getCaraotaHTML(url, headers):
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)

        html = BeautifulSoup(response, "lxml")
        todayArticles = html.find_all("article", {"class": "category-hoy"})
        print(todayArticles, todayArticles.count)

        for article in todayArticles:
            title = article.find("a").get("title")
            print(title, end='\n')

    getCaraotaHTML(caraotaURL, headers)




