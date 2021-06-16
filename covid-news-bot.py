from datetime import datetime, timedelta
import time
import tweepy
import requests
import dateutil
import const as cn


INTERVAL = 60 * 5
auth = tweepy.OAuthHandler(cn.CONSUMER_KEY, cn.CONSUMER_SECRET)
auth.set_access_token(cn.ACCESS_TOKEN, cn.ACCESS_TOKEN_SECRET)

URL = 'https://data.bs.ch/api/records/1.0/search/?dataset=100073&q=&rows=1&sort=timestamp&facet=timestamp'

def get_data():
    """
    Retrieves the json data from opendata.bs and converts it to a panda dataframe
    """
    dic_values = {}
    time_stamp = datetime.now() - timedelta(days=30) # default timestamp 30 days ago
    try:
        data = requests.get(URL).json()
        dic_values = data['records'][0]['fields']
        time_stamp = dic_values['timestamp']
        time_stamp = datetime.fromisoformat(time_stamp)
    except:
        print(f"{datetime.now()} no data returned")

    return dic_values, time_stamp

def get_text(data):
    """
    builds the string to be tweeted
    """
    url = 'https://data.bs.ch/explore/dataset/100073/table/?sort=timestamp'
    text = f"""Covid-news BS: Neue Zahlen auf @OpenDataBS: Fälle neu: {int(data['ndiff_conf'])}, kumuliert: {int(data['ncumul_conf'])}, Aktive Fälle: {data['current_isolated']}, 
Hospitalisierte: {data['current_hosp']}, In Intensivstation: {data['current_icu']}. Alle Detailzahlen unter {url}
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