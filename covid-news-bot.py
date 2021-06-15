from datetime import datetime, timedelta
import time
import tweepy
import requests
import pandas as pd



INTERVAL = 60 * 5
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

URL = 'https://data.bs.ch/api/records/1.0/search/?dataset=100073&q=&rows=1&sort=timestamp&facet=timestamp'

def get_data():
    """
    Retrieves the json data from opendata.bs and converts it to a panda dataframe
    """
    
    record_time_stamp = datetime.now() - timedelta(days=30) # default timestamp 30 days ago
    try:
        data = requests.get(URL).json()
        data = data['records']
        #df = pd.DataFrame(data)['record_timestamp']
        record_time_stamp = data[0]['record_timestamp'][:10]
        record_time_stamp = datetime.strptime(record_time_stamp, '%Y-%m-%d')
        df = pd.DataFrame(data)['fields']
        df = pd.DataFrame(x for x in df)
        record_time_stamp = record_time_stamp
    except:
        print(f"{datetime.now()} no data returned")
        df = pd.DataFrame()

    return df, record_time_stamp

def get_text(data):
    """
    verifies whether passed date is older than date in ogd-record
    """

    text = f"""Covid-news BS: Neue Zahlen auf @OpenDataBS: Fälle neu: {int(data['ndiff_conf'][0])}, kumuliert: {int(data['ncumul_conf'][0])}, Aktive Fälle: {data['current_isolated'][0]}, 
Hospitalisierte: {data['current_hosp'][0]}, In Intensivstation: {data['current_icu'][0]}. Alle Detailzahlen unter https://data.bs.ch/explore/dataset/100073/table/?sort=timestamp
        """
    return text

def main():
    api = tweepy.API(auth)
    data, last_date_published = get_data()
    
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
                    #api.update_status(text)
                    print(f"{datetime.now()} Tweet has been sent")
                except Exception as ex:
                    print(f"{datetime.now()} {ex}")
            else:
                print(f"{datetime.now()} no change")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()