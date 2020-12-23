from CaraotaRegionals import Regional
from CaraotaNationals import CaraotaNationals
import time
import schedule

nationalRequest = CaraotaNationals()
nationalRequest.getNationalNews()

# def job():
#     #regional call
#       #request = Regional()
#       #request.getRegionalNews()
#     #national call
#       nationalsRequest = CaraotaNationals()
#       nationalsRequest.getNationalNews
#     #internationals
#      # internationalRequest =  caraota_international()
#       #internationalRequest.getInternationalsNews()
#       #print("working...")

# schedule.every(50).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)






