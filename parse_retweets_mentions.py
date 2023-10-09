import pandas as pd
import re
import string

FILE = "from:NatlParkService (Bear OR Alaska OR Katmai)_tweets.csv"

df = pd.read_csv("Path/To/File"+FILE)
df["is_retweet"] = False
df["retweet_orig_account"] = ""
df['mentions'] = df['tweet_text'].str.findall(r'[＠@]([^][\s#<>|{}:]+)')

for index, row in df.iterrows():

    #check for retweets
    if "RT @" in row['tweet_text']:
        rt_accounts = re.search(r'(RT|retweet|from|via)(?:\b\W*@(\w+))+', row['tweet_text'])
        list_retweet_accounts = re.split(r'@(\w+)', rt_accounts.groups()[1])
        df.at[index, 'is_retweet'] = True
        df.at[index, 'retweet_orig_account'] = list_retweet_accounts[0]


df.to_excel(FILE.replace(".csv", "")+"_retweets_mentions.xlsx")



