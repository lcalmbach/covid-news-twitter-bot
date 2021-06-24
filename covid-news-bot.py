from datetime import datetime, timedelta
import time
import tweepy
import requests
import const as cn

__version__ = '0.0.4' 
__author__ = 'Lukas Calmbach'
__author_email__ = 'lcalmbach@gmail.com'
app_name = 'covid-new-twitter-bot'
version_date = '2021-06-20'

INTERVAL = 60 * 5
auth = tweepy.OAuthHandler(cn.CONSUMER_KEY, cn.CONSUMER_SECRET)
auth.set_access_token(cn.ACCESS_TOKEN, cn.ACCESS_TOKEN_SECRET)

URL = 'https://data.bs.ch/api/records/1.0/search/?dataset=100073&q=&rows=1&sort=timestamp&facet=timestamp'

def get_data():
    """
    Retrieves the data in json format from opendata.bs and converts it to a panda dataframe.
    """
    dic_values = {}
    time_stamp = datetime.now() - timedelta(days=30) # default timestamp 30 days ago
    try:
        data = requests.get(URL).json()
        dic_values = data['records'][0]['fields']
        time_stamp = datetime.fromisoformat(dic_values['timestamp'])
    except:
        print(f"{datetime.now()} no data returned")

    return dic_values, time_stamp

def get_text(data):
    """
    Builds the string to be tweeted.
    """

    url = 'https://data.bs.ch/explore/dataset/100073/table/?sort=timestamp'
    time_stamp = f"{data['date']} {data['time']}"
    hospitalized= f", Hospitalisierte: {data['current_hosp']}" if  'current_hosp' in data else ""
    icu = f", In Intensivstation: {data['current_icu']}" if  'current_icu' in data else ""
    text = f"Covid-news BS: Zahlen auf @OpenDataBS Stand: {time_stamp}: Fälle: {int(data['ncumul_conf'])}(+{int(data['ndiff_conf'])}), Aktive Fälle: {data['current_isolated']}, Verstorbene: {data['ncumul_deceased']}(+{data['ndiff_deceased']}){hospitalized}{icu}. Alle Detailzahlen unter {url}"
    return text

def sleep_until(days, hour, minute):
    """
    sleeps until a specified hour and minute in the future
    """
    now = datetime.now()
    tomorrow = now + timedelta(days=days)
    tomorrow = datetime(tomorrow.year,tomorrow.month,tomorrow.day,hour,minute)
    seconds = (tomorrow - now).total_seconds()
    print(f"going to sleep until {tomorrow} ({seconds} seconds)")
    time.sleep(seconds)
    print(f"woke up at {datetime.now()}")

def main():
    """
    A initial datarecord is fetched from opendata.bs and stored as last_record. then the data is fetched every 5 minutes
    and the timestamp is compared with the last record. if the new record has a different timestamp, then a message is 
    tweeted and the current record timestamp is set to the last record timestamp. The system sleeps until next day 10:00. 
    Then the loop is continued comparing the fetched data to the last timestamp until a difference is found.
    """
    api = tweepy.API(auth)
    data, last_date_published = get_data()
    start_message = f"Started {app_name} version {__version__} ({version_date}). Most recent iso-timestamp is {last_date_published}"
    print(start_message)
    while True:
        #get must recent data record from opendata.bs
        data, record_datum = get_data()
        #verify if record timestamp is more recent than last published records timestamp
        if len(data) > 0:
            has_changes = (record_datum > last_date_published)
            if has_changes:
                text  = get_text(data)                
                last_date_published = record_datum
                try:
                    print(text)
                    api.update_status(text) #comment for testing
                    # print(f"{datetime.now()} Tweet has been sent") # uncomment for testing
                    # linux server is 2 hours ahead
                    sleep_until(days=1, hour=8, minute=0) 
                except Exception as ex:
                    print(f"{datetime.now()} {ex}")
            else:
                print(f"{datetime.now()} no change")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()