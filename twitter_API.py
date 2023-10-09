import csv
import os
import tweepy
import datetime
from tqdm import tqdm
import time
from random import uniform
import json

############# GLOBAL VARS ############################
API_KEY = ""
API_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
BEARER_TOKEN = ""

TWEET_FIELDS = ["attachments", "author_id","conversation_id", "created_at",
                "entities", "geo", "id", "in_reply_to_user_id", "lang", "possibly_sensitive", "referenced_tweets", "reply_settings",
                "source", "text", "withheld"]

####################### SET UP EXCEL FILES ##################################

def write_headers_tweets(query):
    with open('%s_tweets.csv' % query, 'w', encoding='utf8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["tweet_url", "tweet_text", "tweet_author", "tweet_author_name", "tweet_author_id", "tweet_language", "tweet_date",
                            "hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5", "ur1", "url2", "url3", "url4", "in_reply"])

def write_headers_following(query):
    with open('%s_following.csv' % query, 'w', encoding='utf8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(
            ["origin_account_url", "origin_account", "name", "screen_name", "id", "account_created", "profile", "location", "n_followers",
             "n_following"])

def write_headers_followers(query):
    with open('%s_followers.csv' % query, 'w', encoding='utf8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(
            ["origin_account_url", "origin_account", "name", "screen_name", "id", "account_created", "profile", "location", "n_followers",
             "n_following"])

############### GET FOLLOWERS/FOLLOWING DATA #######################

# These endpoints were removed by X in June 2023 and no longer work

def get_followers(user):
    api = tweepy.Client(bearer_token=BEARER_TOKEN,  wait_on_rate_limit=True)
    write_headers_followers(user)
    user_id = api.get_user(username=user).data.id
    followers = api.get_users_followers(id=user_id)
    profile_url = "https://twitter.com/" + user
    for follower in api.get_list_followers(id=user_id):
        row = [profile_url, user, follower.name, follower.screen_name, follower.id, follower.created_at, follower.description]
        with open('%s_followers.csv' % user, 'a', encoding='utf8') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(row)

def get_following(user):
    api = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
    write_headers_followers(user)
    user_id = api.get_user(username=user).data.id
    followers = api.get_users_following(id=user_id)
    profile_url = "https://twitter.com/" + user
    for friend in api.following(screen_name=user).data:
        row = [profile_url, user, friend.name, friend.screen_name, friend.id, friend.created_at, friend.description]
        with open('%s_followers.csv' % user, 'a', encoding='utf8') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(row)

######################################## FUNCTION TO PARSE A STATUS ##############################################

def parse_tweet(tweet, query):

    #GET BASIC DATA
    api = tweepy.Client(BEARER_TOKEN)
    tweet_text = tweet.text
    tweet_id = tweet.id
    author_id = tweet.author_id
    user_data = api.get_user(id=author_id).data
    tweet_author = user_data.username
    tweet_author_name = user_data.name
    tweet_language = tweet.lang
    tweet_date = tweet.created_at
    tweet_url = 'https://www.twitter.com/' + tweet_author + '/status/' + str(tweet_id)

    # CHECK FOR TWEET DATA: HASHTAGS, URLS
    hashtag1 = None
    hashtag2 = None
    hashtag3 = None
    hashtag4 = None
    hashtag5 = None

    url1 = None
    url2 = None
    url3 = None
    url4 = None

    try:
        if 'hashtags' in tweet.entities:
            hashtag1 = tweet.entities["hashtags"][0]["tag"]
            if len(tweet.entities["hashtags"]) > 1:
                hashtag2 = tweet.entities["hashtags"][1]["tag"]
            if len(tweet.entities["hashtags"]) > 2:
                hashtag3 = tweet.entities["hashtags"][2]["tag"]
            if len(tweet.entities["hashtags"]) > 3:
                hashtag4 = tweet.entities["hashtags"][3]["tag"]
            if len(tweet.entities["hashtags"]) > 4:
                hashtag5 = tweet.entities["hashtags"]["tag"]
        if 'urls' in tweet.entities:
            url1 = tweet.entities["urls"][0]["expanded_url"]
            if len(tweet.entities["urls"]) > 1:
                url2 = tweet.entites["urls"][1]["expanded_url"]
            if len(tweet.entities["urls"]) > 2:
                url3 = tweet.entites["urls"][2]["expanded_url"]
            if len(tweet.entities["urls"]) > 3:
                url4 = tweet.entites["urls"][3]["expanded_url"]
    except:
        print("no additional data")
        pass

    # CHECK IF TWEET IS A REPLY
    reply_to_user = None
    try:
        reply_id = tweet.in_reply_to_user_id
        if reply_id != author_id:
            reply_to_user = api.get_user(id=reply_id).data
        else:
            reply_to_user = "self"
    except:
        pass

    new_row = [tweet_url, tweet_text, tweet_author, tweet_author_name, author_id, tweet_language, tweet_date,
     hashtag1, hashtag2, hashtag3, hashtag4, hashtag5, url1, url2, url3, url4, reply_to_user]

    print(new_row)

    with open('%s_tweets.csv' % query, 'a', encoding='utf8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(new_row)

def query_builder(user_bool, user_handle, keywords_bool, keywords, and_or):
    if user_bool:
        user_query = "from:"+user_handle
    else:
        user_query = ""
    if keywords_bool:
        if and_or.lower() == "and" and len(keywords) > 1:
            keywords_query = (" OR ").join(keywords)
        elif and_or.lower() == "and" and len(keywords) > 1:
            keywords_query = (" ").join(keywords)
        else:
            keywords_query = ""
    return (user_query + " " + "("+keywords_query+")").strip()


def extract_tweets(query):
    api = tweepy.Client(BEARER_TOKEN)
    write_headers_tweets(query)
    tweets = tweepy.Paginator(api.search_recent_tweets, query=query)
    for tweet in tweepy.Paginator(api.search_recent_tweets, query=query, tweet_fields=TWEET_FIELDS).flatten(limit=1000):
        time.sleep(uniform(0.5, 1.3))
        parse_tweet(tweet, query)


# RUN TWEET EXTRACTIONS #
query = query_builder(user_bool=True, user_handle="NatlParkService", keywords_bool=True, keywords=['Bear', 'Alaska', 'Katmai'], and_or="And")
extract_tweets(query)
get_following("NatlParkService")
get_followers("NatlParkService")
#see link for other advanced queries to build your own queries: https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators





































