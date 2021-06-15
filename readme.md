# Covid-News Twitter-Bot
This application scans the opendata.bs platform every 5 minutes for new records and sends a tweet, if new data is discovered. In order to run this or a similar application, you require a twitter developer account. This app was implemented following instructions from [Real Python: How to Make a Twitter Bot in Python With Tweepy](https://realpython.com/twitter-bot-python-tweepy/#:~:text=Tweepy%20is%20an%20open%20source%20Python%20package%20that,implementation%20details%2C%20such%20as%3A%20Data%20encoding%20and%20decoding).

After cloning the repo, the file named const.py must be created and filled with your Twitter Authentification info, provided once your developer account is set up. Make sure that this file is kept secret.

# Authenticate to Twitter
CONSUMER_KEY = <CONSUMER_KEY>
CONSUMER_SECRET = <>
ACCESS_TOKEN= <CONSUMER_SECRET>
ACCESS_TOKEN_SECRET= <ACCESS_TOKEN_SECRET>
BEARER_TOKEN = <BEARER_TOKEN>