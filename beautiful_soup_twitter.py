from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
import json
from pprint import pprint
import csv


twitterurl = 'https://twitter.com/hashtag/ukraine?lang=en'
headers = {
    'User-Agent': 'Googlebot',  # Must spoof to prevent Twitter from blocking traffic
}


def scrapetwitter(url, storage_format):
    start_time = time.time()
    items = []
    content = []

    tweet_attrs = {
        'data-testid': 'tweet'
    }

    tweet_text_attrs = {
        'lang': 'en',
        'dir': 'auto'
    }

    if storage_format == 'json':
        fname = 'tweets.json'
    elif storage_format == 'csv':
        fname = 'tweets.csv'
    else:
        fname = 'tweets.txt'

    with open(fname, 'w', newline='') as fp:

        page = requests.get(url, headers=headers)
        soup = bs(page.content, 'html.parser')
        tweets = soup.find_all(attrs=tweet_attrs)

        for tweet in tweets:

            meta_attr = {
                'class': 'css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2'
            }

            metadata = tweet.find(attrs=meta_attr)

            spans = metadata.find_all('span')
            user = spans[0].get_text()
            username = spans[2].get_text()

            date = metadata.find('time')['datetime'].split('T')[0]

            text_search = tweet.find_all(attrs=tweet_text_attrs)
            text = text_search[0].get_text()

            tweet_dict = dict()
            tweet_dict['name'] = (str(user).encode('ascii', 'ignore').decode('ascii'))
            tweet_dict['username'] = username
            tweet_dict['text'] = (str(text).encode('ascii', 'ignore').decode('ascii'))
            tweet_dict['date'] = date

            if storage_format == 'json':
                json.dump(tweet_dict, fp)
            elif storage_format == 'csv':
                writer = csv.writer(fp, delimiter=',')
                writer.writerow([
                    tweet_dict['name'],
                    tweet_dict['username'],
                    tweet_dict['text'],
                    tweet_dict['date']
                ])
            else:
                pprint(tweet_dict, fp)


scrapetwitter(twitterurl, 'pprint')
