import csv
import requests
import os 


def download():
    path = os.getcwd()

    death_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    confiermed_url =('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    recovered_url=('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')


    req = requests.get(death_url)
    url_content = req.content
    csv_file = open(path+'/static/data/death.csv','wb')
    csv_file.write(url_content)
    csv_file.close()

    req = requests.get(confiermed_url)
    url_content = req.content
    csv_file = open(path+'/static/data/confiermd.csv','wb')
    csv_file.write(url_content)
    csv_file.close()

    req = requests.get(recovered_url)
    url_content = req.content
    csv_file = open(path+'/static/data/recovered.csv','wb')
    csv_file.write(url_content)
    csv_file.close()