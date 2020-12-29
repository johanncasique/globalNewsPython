from CaraotaNews.CaraotaLgbtNews import CaraotaLgtbNews
from CaraotaNews.CaraotaFunzoneNew import CaraotaFunZoneNews
from CaraotaRegionals import Regional
from CaraotaNews.CaraotaNationals import CaraotaNationals
from CaraotaNews.CaraotaInternationals import CaraotaInternationals
from CaraotaNews.CaraotaRedNews import CaraotaRedNews
from CaraotaNews.CaraotaTechNews import CaraotaTechNews
from CaraotaNews.CaraotaEntertainment import CaraotaEntertainmentNews
from CaraotaNews.CaraotaHotZoneNews import CaraotaHotZoneNews
from CaraotaNews.CaraotaSportNews import CaraotaSportNews
from CaraotaNews.CaraotaTipsNews import CaraotaTipsNews
from CaraotaNews.CaraotaMisteryNews import CaraotaMisteryNews
from CaraotaNews.CaraotaPetsNews import CaraotaPetsNews
import time
import schedule


def job():
    #regional call
      #request = Regional()
      #request.getRegionalNews()
    #national call
      nationalsRequest = CaraotaNationals()
      nationalsRequest.getNationalNews()
    #internationals
      internationalRequest =  CaraotaInternationals()
      internationalRequest.getInternationalsNews()
      #print("working...")
    #redNews
      redNewsRequest = CaraotaRedNews()
      redNewsRequest.getRedNews()
    #techNews
      techNewsRequest = CaraotaTechNews()
      techNewsRequest.getTechNews()
    #entertaimentNews
      entertaimentNews = CaraotaEntertainmentNews()
      entertaimentNews.getEntertainmentNews()
    #hotNews
      hotNews = CaraotaHotZoneNews()
      hotNews.getHotNews()
    #funNews
      funNews = CaraotaFunZoneNews()
      funNews.getFunNews()
    #SportNews
      sportNew = CaraotaSportNews()
      sportNew.getSportNews()
    #tipsNews
      tipNews = CaraotaTipsNews()
      tipNews.getTipsNews()
    #misteryNews
      misteryNews = CaraotaMisteryNews()
      misteryNews.getMisteryNews()
    #petsNews
      petsNews = CaraotaPetsNews()
      petsNews.getPetsNews()
    #lgtbNews
      lgtbNews = CaraotaLgtbNews()
      lgtbNews.getLgbtNews()
      

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)






