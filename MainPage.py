from CaraotaRegionals import Regional
from CaraotaNews.CaraotaNationals import CaraotaNationals
from CaraotaNews.CaraotaInternationals import CaraotaInternationals
from CaraotaNews.CaraotaRedNews import CaraotaRedNews
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

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)






