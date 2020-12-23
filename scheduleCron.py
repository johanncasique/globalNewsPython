from crontab import CronTab

my_cron = CronTab(user='johanncasique')


#job = my_cron.new(command='python /Users/johanncasique/Python-Proyects/scrapingCaraota/main.py', comment='dateInfo')
#job.minute.every(1)

#my_cron.write()

for job in my_cron:
    if job.comment == 'dateInfo':
        job.hour.every(10)
        my_cron.write()
        print('Cron job modified successgully')




